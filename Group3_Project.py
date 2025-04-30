# Main Program
import os
from string_matching import str_matcher
from compression.huffman_encoding import compress_phrases

# Huffman encoding and compression
def display_and_compress(results):
    for result in results:
        doc1, doc2 = result['pair'] 
        matches = [match[0] for match in result['matches']]
        print(f"\n[Match] Between {doc1} and {doc2}:")
        for phrase, method in result['matches']:
            print(f"  - {phrase} (via {method})")
 
 # If any matches were found, proceed to compress them using Huffman coding
        if matches:
            codes, encoded = compress_phrases(matches)
            print(f"[Compression] Huffman Codes: {codes}")
            print(f"[Compression] Encoded Matches: {encoded}")

# Load documents from a folder
def load_documents_from_folder(folder_path="documents"):
    if not os.path.exists(folder_path):  # Check if folder exists
        print(f"Error: Folder '{folder_path}' not found!")
        return {}
    
    documents = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
                documents[filename] = file.read()
    return documents

# Function to load files, detect plagiarism, and compress results
def main():
    text = load_documents_from_folder()
    detected_results = str_matcher.detect_duplicate_phrases(text)
    display_and_compress(detected_results)

if __name__ == "__main__":
    main()
