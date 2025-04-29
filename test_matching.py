from string_matching.str_matcher import detect_duplicate_phrases, realtime_keyword_search

# Sample documents for testing
doc1 = """
Forests are critical ecosystems that support countless species and provide essential services to humans.
They act as carbon sinks, absorbing vast amounts of carbon dioxide and mitigating the effects of climate change.
Forests are home to over 80% of terrestrial biodiversity.
"""

doc2 = """
Forests provide essential services to both humans and wildlife.
They absorb carbon dioxide and help reduce the impacts of climate change across the globe.
More than 80% of all terrestrial species live in forests, making conservation efforts critical to biodiversity protection.
"""

# Test 1: Detect duplicate phrases between two documents
print("Test 1: Detect Duplicate Phrases")
phrase = "absorbing vast amounts of carbon dioxide"
results = detect_duplicate_phrases(doc1, phrase)
print("Duplicate Detection Results:", results)
print()

# Test 2: Real-time keyword search in one document
print("Test 2: Real-Time Keyword Search")
keyword = "biodiversity"
realtime_results = realtime_keyword_search(doc2, keyword)
print(f"Keyword '{keyword}' found at positions:", realtime_results)
print()
