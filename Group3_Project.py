# Main Program
import os
from string_matching.str_matcher import detect_plagiarized_phrases, merge_overlapping_phrases
from compression.huffman_encoding import compress_phrases
from sorting import merge_sort

# Display and compress results
def display_and_compress(doc1_name, doc2_name, matches):
    print(f"\n[Match] Between {doc1_name} and {doc2_name}:")
    for match in matches:
        print(f"  - Phrase: \"{match['phrase']}\"")
        print(f"    Found in: {doc1_name} at {match['doc1_pos']}, {doc2_name} at {match['doc2_pos']}")

    # If any matches were found, proceed to compress them using Huffman coding
    if matches:
        phrases = [match['phrase'] for match in matches]
        codes, encoded = compress_phrases(phrases)
        print(f"[Compression] Huffman Codes: {codes}")
        print(f"[Compression] Encoded Matches: {encoded}")

# Load all .txt files from the documents folder
def load_documents_from_folder(folder_path="documents"):
    if not os.path.exists(folder_path):
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
    documents = load_documents_from_folder()
    doc_names = list(documents.keys())

    for i in range(len(doc_names)):
        for j in range(i + 1, len(doc_names)):
            doc1_name = doc_names[i]
            doc2_name = doc_names[j]
            doc1_text = documents[doc1_name]
            doc2_text = documents[doc2_name]
            # Detect plagiarized phrases of length 7
            raw_matches = detect_plagiarized_phrases(doc1_text, doc2_text, phrase_length=7)
            # Merge overlapping phrases
            merged_matches = merge_overlapping_phrases(raw_matches, doc1_text, doc2_text)

            if merged_matches: # If there are any matches, display and compress them
                display_and_compress(doc1_name, doc2_name, merged_matches)

# Main function to execute document sorting
def main():
    documents = load_documents_from_folder()

    # Ask the user how they want to sort the documents
    print("Sort documents by:")
    print("1. Title")
    print("2. Author")
    print("3. Date")
    sort_choice = int(input("Enter your choice (1-3): "))
    
    key_index = sort_choice - 1
    merge_sort(documents, key_index)

    # Display the sorted documents
    print("\nDocuments sorted:")
    for document in documents:
        print(f"Title: {document[0]}, Author: {document[1]}, Date: {document[2]}")

if __name__ == "__main__":
    main()
