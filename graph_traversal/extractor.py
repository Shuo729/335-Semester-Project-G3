def extract_references(file_path):
    """
    Extract references from a document.
    Looks for the section that starts with 'Works Cited' or 'References'.
    Returns list of extracted author + title strings.
    """
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    start = None
    for i, line in enumerate(lines):
        if "Works Cited" in line or "References" in line:
            start = i + 1
            break

    if start is not None:
        refs = [line.strip() for line in lines[start:] if line.strip()]
        return [parse_author_title(ref) for ref in refs]
    else:
        return []

def parse_author_title(reference_str):
    """
    Extract author(s) and title from a reference string.
    """
    try:
        # Split at first period after author name
        parts = reference_str.split(".")
        title = parts[1].strip()
        author = parts[0].strip()
        return f"{author}: {title}"
    except Exception:
        # Fallback if parsing fails
        return reference_str[:50]  # Just show first 50 chars