from merge_sort import merge_sort, load_documents
from counting_sort import counting_sort_by_year

def print_documents(docs, header="Documents"):
    print(f"\n{header}:")
    print("-" * 60)
    for doc in docs:
        print(f"Title: {doc[0]}")
        print(f"Author: {doc[1]}")
        print(f"Date: {doc[2]}")
        print("-" * 60)

def main():
    # Step 1: Load documents with metadata
    docs = load_documents()

    if not docs:
        print("No documents loaded.")
        return

    print_documents(docs, "Original Documents")

    # Step 2: Sort by Title using Merge Sort
    merge_sorted_title = docs[:]
    merge_sort(merge_sorted_title, key_index=0)  # 0 = title
    print_documents(merge_sorted_title, "Sorted by Title (Merge Sort)")

    # Step 3: Sort by Year using Counting Sort
    counting_sorted_year = counting_sort_by_year(docs)
    print_documents(counting_sorted_year, "Sorted by Year (Counting Sort)")

if __name__ == "__main__":
    main()