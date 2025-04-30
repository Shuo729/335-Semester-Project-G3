def naive_search(text, pattern):
    """
    Naive string matching algorithm to find all occurrences of a pattern in a text.
    """
    positions = []
    n = len(text)
    m = len(pattern)

    for i in range(n - m + 1):
        match = True
        for j in range(m):
            if text[i + j] != pattern[j]:
                match = False
                break
        if match:
            positions.append(i)
    return positions