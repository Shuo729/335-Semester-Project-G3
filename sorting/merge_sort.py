import time

# Merge Sort function for sorting documents by a specified field (author, title, date)
def merge_sort(documents, key_index):
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

# Take user input for document details (author, title, date)
def load_documents():
    num_documents = int(input("Enter number of documents: "))
    documents = []

    for _ in range(num_documents):
        title = input("Enter document title: ")
        author = input("Enter author name: ")
        date = input("Enter publication date (YYYY-MM-DD): ")

        documents.append((title, author, date))  # Store as tuple (title, author, date)

    return documents