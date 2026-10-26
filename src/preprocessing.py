from pathlib import Path
import re


def read_lines(path: str) -> list[str]:
    return Path(path).read_text(encoding='utf-8-sig').splitlines()


def normalize(line: str) -> str:
    return re.sub(r'\s+', '', line)


def normalized_lines(lines: list[str]) -> list[str]:
    return [normalize(line) for line in lines]
