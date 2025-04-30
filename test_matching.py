from string_matching.str_matcher import detect_duplicate_phrases, realtime_keyword_search, detect_plagiarized_phrases, merge_overlapping_phrases

# Read documents for testing
with open("documents/doc1.txt", "r", encoding="utf-8") as f:
    doc1 = f.read()

with open("documents/doc2.txt", "r", encoding="utf-8") as f:
    doc2 = f.read()

# Test 1: Detect duplicate phrases between two documents
print("Test 1: Detect Duplicate Phrases")
phrase = "preserving marine biodiversity"
results = detect_duplicate_phrases(doc1, phrase)
print("Duplicate Detection Results:", results)
print()

# Test 2: Real-time keyword search in one document
print("Test 2: Real-Time Keyword Search")
keyword = "conservation"
realtime_results = realtime_keyword_search(doc2, keyword)
print(f"Keyword '{keyword}' found at positions:", realtime_results)
print()

# Test 3: Detect plagiarized phrases
print("Test 3: Detect Plagiarized Phrases")
plagiarized_phrases = detect_plagiarized_phrases(doc1, doc2, phrase_length=7)
print("Plagiarized Phrases Found:")
for match in plagiarized_phrases:
    print(f"- Phrase: \"{match['phrase']}\"")
    print(f"  Found in: doc1.txt at {match['doc1_pos']}, doc2.txt at {match['doc2_pos']}")

# Test 4: Merge overlapping plagiarized phrases for clearer output
print("Test 4: Merged Plagiarized Phrases")
merged_phrases = merge_overlapping_phrases(plagiarized_phrases, doc1, doc2)
for match in merged_phrases:
    print(f"- Phrase: \"{match['phrase']}\"")
    print(f"  Found in: doc1.txt at {match['doc1_pos']}, doc2.txt at {match['doc2_pos']}")
print()