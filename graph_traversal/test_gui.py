import tkinter as tk
from tkinter import filedialog, messagebox
import os
from bfs import visualize_bfs
from dfs import visualize_dfs
from graph import build_reference_graph
from extractor import extract_references

def browse_file(entry_widget):
    """
    Open file dialog to select a document.
    """
    file_path = filedialog.askopenfilename(
        initialdir="documents",
        title="Select a Document",
        filetypes=(("Text files", "*.txt"),)
    )
    entry_widget.delete(0, tk.END)
    entry_widget.insert(0, file_path)

def start_analysis():
    """
    Start analysis based on selected documents and traversal method.
    """
    doc1_path = doc1_entry.get()
    doc2_path = doc2_entry.get()

    if not os.path.isfile(doc1_path) or not os.path.isfile(doc2_path):
        messagebox.showerror("Error", "Please select valid document files.")
        return

    method = method_var.get()
    run_analysis(doc1_path, doc2_path, method)

def run_analysis(doc1_path, doc2_path, method):
    """
    Main function to perform BFS/DFS analysis and visualize results.
    """
    doc1_name = os.path.basename(doc1_path)
    doc2_name = os.path.basename(doc2_path)

    # Use the extractor module to get references
    doc1_refs = extract_references(doc1_path)
    doc2_refs = extract_references(doc2_path)

    documents = [
        (doc1_name, doc1_refs),
        (doc2_name, doc2_refs)
    ]

    graph = build_reference_graph(documents)

    if method == "BFS":
        visualize_bfs(graph, doc1_name)
    else:
        visualize_dfs(graph, doc1_name)

# Test GUI Setup
root = tk.Tk()
root.title("Graph Traversal Document Analyzer")

# Document 1 selection
tk.Label(root, text="Select Document 1:").grid(row=0, column=0, sticky="w")
doc1_entry = tk.Entry(root, width=50)
doc1_entry.grid(row=0, column=1)
tk.Button(root, text="Browse", command=lambda: browse_file(doc1_entry)).grid(row=0, column=2)

# Document 2 selection
tk.Label(root, text="Select Document 2:").grid(row=1, column=0, sticky="w")
doc2_entry = tk.Entry(root, width=50)
doc2_entry.grid(row=1, column=1)
tk.Button(root, text="Browse", command=lambda: browse_file(doc2_entry)).grid(row=1, column=2)

# Traversal method selection
tk.Label(root, text="Select Traversal Method:").grid(row=2, column=0, sticky="w")
method_var = tk.StringVar(value="BFS")
tk.OptionMenu(root, method_var, "BFS", "DFS").grid(row=2, column=1, sticky="w")

# Start button
tk.Button(root, text="Start Analysis", command=start_analysis).grid(row=3, column=1, pady=10)

# Start GUI loop
root.mainloop()