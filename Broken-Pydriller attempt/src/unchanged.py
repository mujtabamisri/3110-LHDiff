from difflib import SequenceMatcher

# Identifies unchanged lines between two lists of strings (old and new) using SequenceMatcher
# Returns a list of tuples containing the indices of matching lines in the old and new lists
def unchanged_matches(old: list[str], new: list[str]) -> list[tuple[int, int]]:

    # SequenceMatcher -> no junk, reference old, read new, autojunk=False to avoid ignoring any lines
    matcher = SequenceMatcher(None, old, new, autojunk=False)

    # Save matching line tuples (old index, new index) for each matching block
    matches = []

    # Iterate through the matching blocks identified by SequenceMatcher
    for block in matcher.get_matching_blocks():

        # Since each matching block may contain multiple lines, we need to iterate through each line in the block
        for offset in range(block.size):
            matches.append((block.a + offset, block.b + offset))
    return matches
