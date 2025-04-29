from string_matching.rabin_karp import rabin_karp
from string_matching.kmp import kmp_search
from string_matching.naive_search import naive_search


def detect_duplicate_phrases(text, pattern):
    """
    Use Rabin-Karp and KMP to detect duplicate phrases between documents.
    """
    results = {
        "Rabin-Karp": rabin_karp(text, pattern),
        "KMP": kmp_search(text, pattern)
    }
    return results


def realtime_keyword_search(text, pattern):
    """
    Use Naive Search for real-time single keyword search inside a document.
    """
    return naive_search(text, pattern)
