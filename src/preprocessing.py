from pathlib import Path
import re

# Read lines from a file, handling UTF-8 with BOM encoding
# Returns a list of strings based on the lines read from the specified file
def read_lines(path: str) -> list[str]:
    return Path(path).read_text(encoding='utf-8-sig').splitlines()

# Normalize a line by removing all whitespace characters
def normalize(line: str) -> str:
    return re.sub(r'\s+', '', line)

# Normalize a list of lines by applying the normalize function to each line
def normalized_lines(lines: list[str]) -> list[str]:
    return [normalize(line) for line in lines]
