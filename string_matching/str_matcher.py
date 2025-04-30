from string_matching.rabin_karp import rabin_karp
from string_matching.kmp import kmp_search
from string_matching.naive_search import naive_search
import re

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

def strip_after_references(text):
    """
    Cut the text off at "References" or "Works Cited" to exclude bibliography.
    """
    ref_match = re.search(r'\b(References|Works Cited)\b', text, re.IGNORECASE)
    return text[:ref_match.start()] if ref_match else text

def clean_phrase(phrase):
    """
    Remove parentheses from the phrase for cleaner comparison.
    """
    return re.sub(r'\([^)]*\)', '', phrase).strip()

def detect_plagiarized_phrases(doc1_text, doc2_text, phrase_length=5):
    """
    Detect matching phrases between two documents by splitting into small phrases
    and checking if they exist across documents.
    Ignoring citations and references.
    """
    matches = []
    doc1_main = strip_after_references(doc1_text)
    doc2_main = strip_after_references(doc2_text)
    
    doc1_words = doc1_text.split()

    for i in range(len(doc1_words) - phrase_length + 1):
        phrase = " ".join(doc1_words[i:i + phrase_length])
        cleaned = clean_phrase(phrase) # Clean the phrase for comparison

        if len(cleaned.split()) < 3:  # Skip very short cleaned phrases
            continue

        if any(m['phrase'] == cleaned for m in matches):
            continue

        result = detect_duplicate_phrases(doc2_main, cleaned)
        if any(result[algo] for algo in result):
            match_info = {
                "phrase": cleaned,
                "doc1_pos": doc1_text.find(cleaned),
                "doc2_pos": doc2_text.find(cleaned)
            }
            matches.append(match_info)

    return matches

def merge_overlapping_phrases(plagiarized_phrases, doc1, doc2):
    """
    Merge overlapping/adjacent phrases for cleaner visualization.
    """
    if not plagiarized_phrases:
        return []

    plagiarized_phrases.sort(key=lambda x: x['doc1_pos'])

    merged = []
    current = plagiarized_phrases[0]

    for next_phrase in plagiarized_phrases[1:]:
        curr_end = current['doc1_pos'] + len(current['phrase'])
        next_start = next_phrase['doc1_pos']

        if next_start <= curr_end + 1:
            # Extend current phrase
            end = max(curr_end, next_start + len(next_phrase['phrase']))
            current['phrase'] = doc1[current['doc1_pos']:end]
        else:
            merged.append(current)
            current = next_phrase

    merged.append(current)
    return merged