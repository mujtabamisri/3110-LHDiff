from difflib import SequenceMatcher


def unchanged_matches(old: list[str], new: list[str]) -> list[tuple[int, int]]:
    matcher = SequenceMatcher(None, old, new, autojunk=False)
    matches = []
    for block in matcher.get_matching_blocks():
        for offset in range(block.size):
            matches.append((block.a + offset, block.b + offset))
    return matches
