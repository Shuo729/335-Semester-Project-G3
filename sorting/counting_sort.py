from datetime import datetime

def counting_sort_by_year(documents):
    """
    Sorts a list of document tuples by date using Counting Sort.
    Assumes year is part of the date string (YYYY-MM-DD).
    
    Input: List of (title, author, date) tuples
    Output: Sorted list by year, month, and date (oldest to newest)
    """
    if not documents:
        return []

    # Define valid year range
    MIN_YEAR = 1900
    MAX_YEAR = 2026
    freq = [[] for _ in range(MIN_YEAR, MAX_YEAR + 1)]

    for doc in documents:
        title, author, date_str = doc

        try:
            # Parse full date string
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            # Fallback for invalid or missing dates
            date_obj = datetime.strptime("1900-01-01", "%Y-%m-%d").date()

        freq[date_obj.year - MIN_YEAR].append((date_obj, doc))

    # Sort the buckets by year and then by month and day
    sorted_docs = []
    for bucket in freq:
        if bucket:
            # Sort each bucket by full date
            bucket.sort(key=lambda x: x[0])  # x[0] is date_obj
            sorted_docs.extend(doc for date_obj, doc in bucket)

    return sorted_docs