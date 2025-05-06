import os
import re

def extract_metadata(file_path):
    """
    Extracts title, author, and date from the top of a .txt document.
    Assumes first three lines contain this info in format:
        Title: ...
        Author: ...
        Date: YYYY-MM-DD or YYYY
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = []
            while len(lines) < 3:
                line = f.readline()
                if not line:
                    break  # End of file
                stripped = line.strip()
                if stripped:
                    lines.append(stripped)

        title = ""
        author = ""
        date = "Unknown"

        if len(lines) > 0 and "title:" in lines[0].lower():
            title = lines[0].split(":", 1)[1].strip()
        elif len(lines) > 0:
            title = lines[0]

        if len(lines) > 1 and "author:" in lines[1].lower():
            author = lines[1].split(":", 1)[1].strip()
        elif len(lines) > 1:
            author = lines[1]

        if len(lines) > 2:
            date_line = lines[2]
            match = re.search(r"\b\d{4}-\d{2}-\d{2}\b", date_line)
            if match:
                date = match.group()
            else:
                match = re.search(r"\b\d{4}\b", date_line)
                if match:
                    date = f"{match.group()}-01-01"
                else:
                    date = "Unknown"

        return title, author, date

    except Exception as e:
        print(f"Error extracting metadata from {file_path}: {e}")
        return "Unknown Title", "Unknown Author", "Unknown"