import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import io
import sys
from datetime import datetime # For calculating original size of compressed data

# Project module imports
from string_matching.str_matcher import detect_plagiarized_phrases, merge_overlapping_phrases
from compression.huffman_encoding import compress_phrases
from sorting.merge_sort import load_documents as load_docs_for_sorting, merge_sort
from sorting.counting_sort import counting_sort_by_year
from graph_traversal.extractor import extract_references
from graph_traversal.graph import build_reference_graph
from graph_traversal.bfs import visualize_bfs
from graph_traversal.dfs import visualize_dfs

class DocumentScannerGUI:
    def __init__(self, master):
        self.master = master
        master.title("CSUF Document Scanner & Pattern Extractor")
        
        # Set size and center the main window
        WINDOW_WIDTH = 800
        WINDOW_HEIGHT = 600
        self.center_window(master, WINDOW_WIDTH, WINDOW_HEIGHT)
        
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        # Tab 1: Plagiarism Detection & Compression
        self.plagiarism_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.plagiarism_tab, text='Plagiarism & Compression')
        self.setup_plagiarism_tab(self.plagiarism_tab)

        # Tab 2: Document Sorting
        self.sorting_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.sorting_tab, text='Document Sorting')
        self.setup_sorting_tab(self.sorting_tab)
        self.loaded_documents_for_sorting = [] # To store documents loaded for sorting

        # Tab 3: Citation Graph Analysis
        self.graph_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.graph_tab, text='Citation Graph Analysis')
        self.setup_graph_tab(self.graph_tab)
        
        # Tab 4: Document Optimization (Uses greedy prioritization)
        self.optimization_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.optimization_tab, text='Optimization')
        self.setup_optimization_tab(self.optimization_tab)

    def browse_file(self, entry_widget):
        file_path = filedialog.askopenfilename(
            initialdir="documents",
            title="Select a Document",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )
        if file_path:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, file_path)

    # Center the window on the screen
    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        window.geometry(f"{width}x{height}+{x}+{y}")

    # --- Plagiarism & Compression Tab ---
    def setup_plagiarism_tab(self, tab):
        frame = ttk.Frame(tab, padding="10")
        frame.pack(expand=True, fill='both')

        # File 1
        ttk.Label(frame, text="Document 1:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.plag_doc1_entry = ttk.Entry(frame, width=60)
        self.plag_doc1_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(frame, text="Browse", command=lambda: self.browse_file(self.plag_doc1_entry)).grid(row=0, column=2, padx=5, pady=5)

        # File 2
        ttk.Label(frame, text="Document 2:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.plag_doc2_entry = ttk.Entry(frame, width=60)
        self.plag_doc2_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(frame, text="Browse", command=lambda: self.browse_file(self.plag_doc2_entry)).grid(row=1, column=2, padx=5, pady=5)
        
        # Phrase length (optional, could be hardcoded)
        ttk.Label(frame, text="Min Phrase Length:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.phrase_length_var = tk.StringVar(value="7")
        self.phrase_length_entry = ttk.Entry(frame, textvariable=self.phrase_length_var, width=10)
        self.phrase_length_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")


        # Analyze Button
        analyze_button = ttk.Button(frame, text="Detect Plagiarism & Compress Matches", command=self.analyze_plagiarism_and_compress)
        analyze_button.grid(row=3, column=0, columnspan=3, pady=10)

        # Results Area
        self.plag_results_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, height=20)
        self.plag_results_text.grid(row=4, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)

        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(4, weight=1)

    def analyze_plagiarism_and_compress(self):
        doc1_path = self.plag_doc1_entry.get()
        doc2_path = self.plag_doc2_entry.get()
        
        try:
            phrase_length = int(self.phrase_length_var.get())
            if phrase_length < 2:
                messagebox.showerror("Error", "Phrase length must be at least 2.")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid phrase length. Must be an integer.")
            return

        if not (doc1_path and os.path.isfile(doc1_path)):
            messagebox.showerror("Error", "Please select a valid file for Document 1.")
            return
        if not (doc2_path and os.path.isfile(doc2_path)):
            messagebox.showerror("Error", "Please select a valid file for Document 2.")
            return

        try:
            with open(doc1_path, 'r', encoding='utf-8', errors='ignore') as f:
                doc1_text = f.read()
            with open(doc2_path, 'r', encoding='utf-8', errors='ignore') as f:
                doc2_text = f.read()
        except Exception as e:
            messagebox.showerror("File Error", f"Error reading files: {e}")
            return

        self.plag_results_text.delete('1.0', tk.END)
        # Configure a tag for highlighting
        self.plag_results_text.tag_configure("highlight", background="yellow", foreground="black")

        self.plag_results_text.insert(tk.END, f"Analyzing plagiarism between:\nDoc 1: {os.path.basename(doc1_path)}\nDoc 2: {os.path.basename(doc2_path)}\nWith minimum phrase length: {phrase_length}\n\n")

        raw_matches = detect_plagiarized_phrases(doc1_text, doc2_text, phrase_length=phrase_length)
        merged_matches = merge_overlapping_phrases(raw_matches, doc1_text, doc2_text)

        if not merged_matches:
            self.plag_results_text.insert(tk.END, "No significant matching phrases found.\n")
            return

        self.plag_results_text.insert(tk.END, f"Found {len(merged_matches)} matching phrase(s):\n\n")
        match_phrases_for_compression = []
        
        CONTEXT_CHARS = 60 # Number of characters for context on each side

        for i, match_info in enumerate(merged_matches):
            # phrase_from_doc1 is the actual merged text segment from document 1
            phrase_from_doc1 = match_info['phrase']
            len_phrase_from_doc1 = len(phrase_from_doc1)
            
            doc1_match_start_actual = match_info['doc1_pos']
            # doc2_match_start_original is the start of the *first cleaned sub-phrase* in doc2
            # that contributed to this merged phrase from doc1.
            doc2_match_start_original = match_info['doc2_pos']

            self.plag_results_text.insert(tk.END, f"Match {i+1}:\n")
            # The "detected phrase" is the segment from doc1
            self.plag_results_text.insert(tk.END, f"  Detected phrase (from {os.path.basename(doc1_path)}):\n    \"", "bold") # Make title bold
            self.plag_results_text.insert(tk.END, phrase_from_doc1)
            self.plag_results_text.insert(tk.END, "\"\n\n")


            # --- Display context from Document 1 ---
            self.plag_results_text.insert(tk.END, f"  In {os.path.basename(doc1_path)}:\n    ")
            
            context_start1 = max(0, doc1_match_start_actual - CONTEXT_CHARS)
            # Text before the highlight in doc1
            prefix_text1 = doc1_text[context_start1:doc1_match_start_actual]
            if context_start1 > 0:
                prefix_text1 = "..." + prefix_text1
            
            # Text after the highlight in doc1
            context_end1_after_phrase = doc1_match_start_actual + len_phrase_from_doc1
            context_end1_display = min(len(doc1_text), context_end1_after_phrase + CONTEXT_CHARS)
            suffix_text1 = doc1_text[context_end1_after_phrase : context_end1_display]
            if context_end1_display < len(doc1_text):
                suffix_text1 = suffix_text1 + "..."

            # Insert into text widget for doc1
            self.plag_results_text.insert(tk.END, prefix_text1)
            tag_start_idx1 = self.plag_results_text.index(tk.INSERT) # Get current position
            self.plag_results_text.insert(tk.END, phrase_from_doc1) # Insert the phrase from doc1
            tag_end_idx1 = self.plag_results_text.index(tk.INSERT)   # Get position after insertion
            self.plag_results_text.tag_add("highlight", tag_start_idx1, tag_end_idx1)
            self.plag_results_text.insert(tk.END, suffix_text1 + "\n\n")

            # --- Display context from Document 2 ---
            # We will highlight the segment in doc2 that corresponds in position and length
            # to the phrase_from_doc1, starting at doc2_match_start_original.
            self.plag_results_text.insert(tk.END, f"  Corresponds in {os.path.basename(doc2_path)} (original match at index {doc2_match_start_original}):\n    ")
            
            # The text from doc2 that we intend to highlight. Its length is len_phrase_from_doc1.
            # Ensure we don't go out of bounds for doc2_text.
            doc2_highlight_end = min(len(doc2_text), doc2_match_start_original + len_phrase_from_doc1)
            highlight_text_in_doc2 = doc2_text[doc2_match_start_original : doc2_highlight_end]
            
            context_start2 = max(0, doc2_match_start_original - CONTEXT_CHARS)
            # Text before the highlight in doc2
            prefix_text2 = doc2_text[context_start2:doc2_match_start_original]
            if context_start2 > 0:
                prefix_text2 = "..." + prefix_text2
            
            # Text after the highlight in doc2
            # The end of the actual highlighted part in doc2 is doc2_match_start_original + len(highlight_text_in_doc2)
            context_end2_after_phrase = doc2_match_start_original + len(highlight_text_in_doc2)
            context_end2_display = min(len(doc2_text), context_end2_after_phrase + CONTEXT_CHARS)
            suffix_text2 = doc2_text[context_end2_after_phrase : context_end2_display]
            if context_end2_display < len(doc2_text):
                suffix_text2 = suffix_text2 + "..."

            # Insert into text widget for doc2
            self.plag_results_text.insert(tk.END, prefix_text2)
            tag_start_idx2 = self.plag_results_text.index(tk.INSERT)
            self.plag_results_text.insert(tk.END, highlight_text_in_doc2) # Insert the actual text from doc2
            tag_end_idx2 = self.plag_results_text.index(tk.INSERT)
            self.plag_results_text.tag_add("highlight", tag_start_idx2, tag_end_idx2)
            self.plag_results_text.insert(tk.END, suffix_text2 + "\n\n")
            
            match_phrases_for_compression.append(phrase_from_doc1) # Use phrase from doc1 for compression
        
        self.plag_results_text.insert(tk.END, "\n--- Compression of Matched Phrases ---\n")
        if match_phrases_for_compression:
            codes, encoded_text = compress_phrases(match_phrases_for_compression)
            
            original_text_for_compression = " ".join(match_phrases_for_compression)
            original_size_chars = len(original_text_for_compression)
            # Assuming 1 byte per char for original size in bits for comparison with Huffman
            original_size_bits = original_size_chars * 8 
            compressed_size_bits = len(encoded_text)

            self.plag_results_text.insert(tk.END, f"Huffman Codes: {codes}\n\n")
            # self.plag_results_text.insert(tk.END, f"Encoded Text: {encoded_text}\n\n") # Can be very long
            self.plag_results_text.insert(tk.END, f"Original Size (concatenated matched phrases): {original_size_chars} characters ({original_size_bits} bits)\n")
            self.plag_results_text.insert(tk.END, f"Compressed Size (Huffman encoded): {compressed_size_bits} bits\n")

            if original_size_bits > 0:
                ratio = (compressed_size_bits / original_size_bits) * 100
                self.plag_results_text.insert(tk.END, f"Compression Ratio: {ratio:.2f}%\n")
                self.plag_results_text.insert(tk.END, f"Space Saved: {(100-ratio):.2f}%\n")
            else:
                self.plag_results_text.insert(tk.END, "Cannot calculate compression ratio for empty input.\n")
        else:
            self.plag_results_text.insert(tk.END, "No phrases to compress.\n")


    # --- Document Sorting Tab ---
    def setup_sorting_tab(self, tab):
        frame = ttk.Frame(tab, padding="10")
        frame.pack(expand=True, fill='both')

        load_button = ttk.Button(frame, text="Load Documents from 'documents' folder", command=self.load_and_display_docs_for_sorting)
        load_button.grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(frame, text="Sort by:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.sort_key_var = tk.StringVar(value="Title")
        sort_options = ["Title", "Date"]
        ttk.OptionMenu(frame, self.sort_key_var, self.sort_key_var.get(), *sort_options).grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        sort_button = ttk.Button(frame, text="Sort and Display", command=self.sort_and_display_docs)
        sort_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.sort_results_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, height=20)
        self.sort_results_text.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        frame.columnconfigure(1, weight=1) # Allow text area to expand
        frame.rowconfigure(3, weight=1)


    def load_and_display_docs_for_sorting(self):
        self.sort_results_text.delete('1.0', tk.END)
        try:
            # Assuming load_docs_for_sorting is from sorting.merge_sort
            # and it uses sorting.utils.extract_metadata
            self.loaded_documents_for_sorting = load_docs_for_sorting(folder="documents") 
            if not self.loaded_documents_for_sorting:
                self.sort_results_text.insert(tk.END, "No documents found or loaded from 'documents' folder.\n")
                return
            
            self.sort_results_text.insert(tk.END, f"Loaded {len(self.loaded_documents_for_sorting)} documents:\n")
            for title, author, date in self.loaded_documents_for_sorting:
                self.sort_results_text.insert(tk.END, f"  Title: {title}\n  Author: {author}\n  Date: {date}\n---\n")
        except Exception as e:
            messagebox.showerror("Loading Error", f"Failed to load documents: {e}")
            self.sort_results_text.insert(tk.END, f"Error loading documents: {e}\n")

    def sort_and_display_docs(self):
        if not self.loaded_documents_for_sorting:
            messagebox.showinfo("Info", "Please load documents first.")
            return

        sort_key = self.sort_key_var.get()
        self.sort_results_text.delete('1.0', tk.END)
        
        docs_to_sort = list(self.loaded_documents_for_sorting) # Make a copy

        if sort_key == "Title":
            # merge_sort sorts in place, key_index=0 for title
            merge_sort(docs_to_sort, key_index=0)
            self.sort_results_text.insert(tk.END, "Documents sorted by Title (Merge Sort):\n")
        elif sort_key == "Date":
            # counting_sort_by_year returns a new sorted list
            docs_to_sort = counting_sort_by_year(docs_to_sort)
            self.sort_results_text.insert(tk.END, "Documents sorted by Date (Counting Sort):\n")
        
        for title, author, date in docs_to_sort:
            self.sort_results_text.insert(tk.END, f"  Title: {title}\n  Author: {author}\n  Date: {date}\n---\n")

    # --- Citation Graph Analysis Tab ---
    def setup_graph_tab(self, tab):
        frame = ttk.Frame(tab, padding="10")
        frame.pack(expand=True, fill='both')

        # File 1 (Start Node for traversal)
        ttk.Label(frame, text="Document 1 (Start Node):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.graph_doc1_entry = ttk.Entry(frame, width=50)
        self.graph_doc1_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(frame, text="Browse", command=lambda: self.browse_file(self.graph_doc1_entry)).grid(row=0, column=2, padx=5, pady=5)

        # File 2 (To build a more complex graph, optional for simple graph)
        ttk.Label(frame, text="Document 2 (Optional):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.graph_doc2_entry = ttk.Entry(frame, width=50)
        self.graph_doc2_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(frame, text="Browse", command=lambda: self.browse_file(self.graph_doc2_entry)).grid(row=1, column=2, padx=5, pady=5)

        ttk.Label(frame, text="Traversal Method:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.traversal_method_var = tk.StringVar(value="BFS")
        traversal_options = ["BFS", "DFS"]
        ttk.OptionMenu(frame, self.traversal_method_var, self.traversal_method_var.get(), *traversal_options).grid(row=2, column=1, padx=5, pady=5, sticky="w")

        analyze_button = ttk.Button(frame, text="Analyze Citations & Visualize Graph", command=self.analyze_citations)
        analyze_button.grid(row=3, column=0, columnspan=3, pady=10)

        self.graph_results_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, height=15)
        self.graph_results_text.grid(row=4, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(4, weight=1)

    def analyze_citations(self):
        doc1_path = self.graph_doc1_entry.get()
        doc2_path = self.graph_doc2_entry.get() # Optional

        if not (doc1_path and os.path.isfile(doc1_path)):
            messagebox.showerror("Error", "Please select a valid file for Document 1 (Start Node).")
            return
        
        documents_for_graph = []
        try:
            doc1_name = os.path.basename(doc1_path)
            doc1_refs = extract_references(doc1_path)
            documents_for_graph.append((doc1_name, doc1_refs))

            if doc2_path and os.path.isfile(doc2_path):
                doc2_name = os.path.basename(doc2_path)
                doc2_refs = extract_references(doc2_path)
                documents_for_graph.append((doc2_name, doc2_refs))
            elif doc2_path: # Path given but not a file
                 messagebox.showwarning("Warning", f"Document 2 path '{doc2_path}' is not a valid file. Proceeding with Document 1 only for graph.")


        except Exception as e:
            messagebox.showerror("File Error", f"Error processing document files for graph: {e}")
            return

        self.graph_results_text.delete('1.0', tk.END)
        if not documents_for_graph:
            self.graph_results_text.insert(tk.END, "No documents to build graph from.\n")
            return
            
        try:
            graph = build_reference_graph(documents_for_graph)
            if not graph.nodes():
                self.graph_results_text.insert(tk.END, "Graph is empty. No nodes found (document or references).\n")
                messagebox.showinfo("Graph Info", "The citation graph is empty. Check if the document(s) have 'Works Cited' or 'References' sections.")
                return
        except Exception as e:
            messagebox.showerror("Graph Error", f"Error building reference graph: {e}")
            self.graph_results_text.insert(tk.END, f"Error building graph: {e}\n")
            return


        method = self.traversal_method_var.get()
        start_node = os.path.basename(doc1_path)

        if start_node not in graph:
            alt_start_node = list(graph.nodes())[0] if graph.nodes() else None
            if alt_start_node:
                 messagebox.showwarning("Graph Warning", f"Start node '{start_node}' not in graph. Using '{alt_start_node}' instead.")
                 start_node = alt_start_node
            else: # Should have been caught by graph.nodes() check earlier
                messagebox.showerror("Graph Error", "Start node not in graph and graph has no nodes.")
                self.graph_results_text.insert(tk.END, "Start node not in graph and graph is empty.\n")
                return


        self.graph_results_text.insert(tk.END, f"Performing {method} traversal starting from '{start_node}'...\n")
        
        # Capture print output from visualize_bfs/dfs
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        
        try:
            if method == "BFS":
                visualize_bfs(graph, start_node)
            else: # DFS
                visualize_dfs(graph, start_node)
        except Exception as e:
            sys.stdout = old_stdout # Restore stdout
            messagebox.showerror("Traversal Error", f"Error during graph traversal or visualization: {e}")
            self.graph_results_text.insert(tk.END, f"Error during {method} visualization: {e}\n")
            return
        finally:
            sys.stdout = old_stdout # Restore stdout in case of error too

        traversal_info = captured_output.getvalue()
        self.graph_results_text.insert(tk.END, traversal_info)
        self.graph_results_text.insert(tk.END, "\nGraph visualization should have popped up in a new window.\n")
        messagebox.showinfo("Graph Visualization", "Graph visualization (if any nodes/edges) should have appeared in a separate Matplotlib window.")

    def setup_optimization_tab(self, tab):
        frame = ttk.Frame(tab, padding="10")
        frame.pack(expand=True, fill='both')

        # Button to run optimization
        self.optimize_button = ttk.Button(frame, text="Prioritize Most Relevant Documents", command=self.run_greedy_optimization)
        self.optimize_button.grid(row=0, column=0, columnspan=2, pady=10)

        # Results display area
        self.optimize_results_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, height=20)
        self.optimize_results_text.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        frame.rowconfigure(1, weight=1)
        frame.columnconfigure(1, weight=1)
        
    def run_greedy_optimization(self):
        # List of documents
        doc_files = [f for f in os.listdir("documents") if f.endswith(".txt")]
        if len(doc_files) < 2:
            messagebox.showinfo("Not Enough Docs", "At least two documents are required for comparison.")
            return

        # Create loading popup
        self.loading_popup = tk.Toplevel(self.master)
        self.loading_popup.title("Processing")
        self.loading_popup.geometry("300x100")

        label = ttk.Label(self.loading_popup, text="Prioritization in progress, please wait...", font=("Arial", 10))
        label.pack(pady=20)
        
        # Center the popup
        self.center_window(self.loading_popup, 300, 100)

        # Disable main window interaction while popup is open
        self.loading_popup.transient(self.master)
        self.loading_popup.grab_set()

        # Run actual work after short delay to allow UI update
        self.master.after(100, lambda: self._perform_optimization(doc_files))
    
    def _perform_optimization(self, doc_files):
        doc_paths = [os.path.join("documents", f) for f in doc_files]
        doc_texts = []

        try:
            for path in doc_paths:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    doc_texts.append(f.read())
        except Exception as e:
            messagebox.showerror("File Error", f"Error reading files: {e}")
            self.loading_popup.destroy()
            return

        match_counts = []
        for i in range(len(doc_texts)):
            for j in range(i + 1, len(doc_texts)):
                phrase_matches = detect_plagiarized_phrases(doc_texts[i], doc_texts[j], phrase_length=7)
                match_count = len(phrase_matches)
                if match_count > 0:
                    match_counts.append((doc_files[i], doc_files[j], match_count))

        # Sort descending by match count
        match_counts.sort(key=lambda x: x[2], reverse=True)

        # Clear results area
        self.optimize_results_text.delete('1.0', tk.END)

        # Display result
        if not match_counts:
            self.optimize_results_text.insert(tk.END, "No overlaps detected among documents.\n")
        else:
            self.optimize_results_text.insert(tk.END, "Top Document Pairs by Overlap Count:\n\n")
            for d1, d2, count in match_counts:
                self.optimize_results_text.insert(tk.END, f"{d1} ↔ {d2}\nMatches Found: {count}\n------------------------------\n")

        # Close loading popup
        self.loading_popup.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = DocumentScannerGUI(root)
    root.mainloop() 