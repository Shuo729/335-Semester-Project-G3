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

def detect_plagiarized_phrases(doc1_text, doc2_text, phrase_length=5):
    """
    Detect matching phrases between two documents by splitting into small phrases
    and checking if they exist across documents.
    """
    matches = []
    doc1_words = doc1_text.split()

    for i in range(len(doc1_words) - phrase_length + 1):
        phrase = " ".join(doc1_words[i:i + phrase_length])

        # Skip likely citations
        if "(" in phrase and ")" in phrase and "." in phrase:
            continue

        # Only skip short phrases if phrase_length >= 5
        if phrase_length >= 5 and len(phrase.split()) < 5:
            continue

        # Avoid duplicates
        if any(m['phrase'] == phrase for m in matches):
            continue

        result = detect_duplicate_phrases(doc2_text, phrase)
        if any(result[algo] for algo in result):
            match_info = {
                "phrase": phrase,
                "doc1_pos": doc1_text.find(phrase),
                "doc2_pos": doc2_text.find(phrase)
            }
            matches.append(match_info)

    return matches

def merge_overlapping_phrases(plagiarized_phrases, doc1, doc2):
    """
    Merge overlapping plagiarized phrases for clearer output.
    """
    merged_phrases = []
    i = 0
    while i < len(plagiarized_phrases):
        current_phrase = plagiarized_phrases[i]
        # Check if this phrase has an overlap with the next phrase
        merged_phrase = current_phrase['phrase']
        doc1_pos = current_phrase['doc1_pos']
        doc2_pos = current_phrase['doc2_pos']

        # Look ahead for overlap with the next phrase
        while i + 1 < len(plagiarized_phrases):
            next_phrase = plagiarized_phrases[i + 1]
            # If the current and next phrases overlap (i.e., last part of current, first part of next)
            if merged_phrase.split()[-(len(next_phrase['phrase'].split()) - 1):] == next_phrase['phrase'].split()[:-1]:
                # Merge the phrases
                merged_phrase = merged_phrase + " " + next_phrase['phrase'].split()[-1]
                doc1_pos = min(doc1_pos, next_phrase['doc1_pos'])  # Adjust the position
                doc2_pos = min(doc2_pos, next_phrase['doc2_pos'])  # Adjust the position
                i += 1  # Move to the next phrase
            else:
                break
        
        # Now check if the merged phrase is exactly the same in both documents
        if merged_phrase in doc1 and merged_phrase in doc2:
            merged_phrases.append({
                'phrase': merged_phrase,
                'doc1_pos': doc1_pos,
                'doc2_pos': doc2_pos
            })
        i += 1

    return merged_phrases