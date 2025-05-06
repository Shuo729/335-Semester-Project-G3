from utils import extract_metadata
import os

def merge_sort(documents, key_index):
    """
    Sorts the documents list in place using merge sort algorithm based on the key_index.
    key_index: 0 for title, 1 for author, or 2 for date.
    """
    if len(documents) > 1:
        mid = len(documents) // 2  # Find the middle index
        left_half = documents[:mid]  # Divide list into left half
        right_half = documents[mid:]  # Divide list into right half

        # Recursively call merge_sort on the two halves
        merge_sort(left_half, key_index)
        merge_sort(right_half, key_index)

        i = j = k = 0

        # Merge the sorted halves based on the key_index (author, title, or date)
        while i < len(left_half) and j < len(right_half):
            if left_half[i][key_index] < right_half[j][key_index]:  # Compare based on chosen key
                documents[k] = left_half[i]
                i += 1
            else:
                documents[k] = right_half[j]
                j += 1
            k += 1

        # Check if any element was left in the left_half
        while i < len(left_half):
            documents[k] = left_half[i]
            i += 1
            k += 1

        # Check if any element was left in the right_half
        while j < len(right_half):
            documents[k] = right_half[j]
            j += 1
            k += 1

def load_documents(folder="documents"):
    """
    Loads all .txt files from the folder and extracts metadata.
    Returns list of (title, author, date) tuples.
    """
    docs = []
    # Iterate through all files in the specified folder
    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            path = os.path.join(folder, filename)
            title, author, date = extract_metadata(path)
            docs.append((title, author, date))
    return docs