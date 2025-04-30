import heapq

# Huffman Tree Node
class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    
    def __lt__(self, other):
        return self.freq < other.freq

# Build Huffman Tree
def build_huffman_tree(freq_map):
    heap = [HuffmanNode(char, freq) for char, freq in freq_map.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    return heap[0]

# Recursively build code map
def build_codes(node, prefix="", code_map={}):
    if node is None:
        return
    if node.char is not None:
        code_map[node.char] = prefix
    build_codes(node.left, prefix + "0", code_map)
    build_codes(node.right, prefix + "1", code_map)
    return code_map

# Main compression function
def compress_phrases(phrases):
    if not phrases:
        return {}, ""
    
    combined_text = " ".join(phrases)
    freq_map = {char: combined_text.count(char) for char in set(combined_text)}

    root = build_huffman_tree(freq_map)
    codes = build_codes(root)
    encoded_text = "".join(codes[char] for char in combined_text)

    return codes, encoded_text