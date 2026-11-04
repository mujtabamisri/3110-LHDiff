from collections import Counter
from math import sqrt
from .candidates import context, tokens

# Calculate the Levenshtein distance between two strings
# Levenshtein distance -> the minimum number of single-character edits needed to transform one string into another
def levenshtein(a: str, b: str) -> int:

    # Ensure that the first string is the longer one for efficiency
    if len(a) < len(b):
        a, b = b, a

    # Initialize the previous row of the dynamic programming table
    previous = list(range(len(b) + 1))

    # Iterate through each character in the first string
    for i, char_a in enumerate(a, 1):

        # Initialize the current row of the dynamic programming table
        current = [i]

        # Iterate through each character in the second string
        for j, char_b in enumerate(b, 1):

            # Calculate the cost of edits
            # current[-1] + 1 -> insertion
            # previous[j] + 1 -> deletion
            # previous[j-1] + (char_a != char_b) -> substitution
            current.append(min(current[-1] + 1, previous[j] + 1,
                               previous[j-1] + (char_a != char_b)))

        # Update the previous row to be the current row for the next iteration
        previous = current

    # Return the last value in the previous row, which represents the Levenshtein distance
    return previous[-1]

# Calculate the content similarity between two strings based on the Levenshtein distance
def content_similarity(a: str, b: str) -> float:
    length = max(len(a), len(b))
    return 1.0 if length == 0 else 1 - levenshtein(a, b) / length

# Calculate the cosine similarity between two strings based on their token counts
# Cosine similarity -> treat tokens as vectors in a high-dimensional space and compute the cosine of the angle between them
def cosine(a: str, b: str) -> float:

    # Get the token counts for both strings using the Counter class
    ca, cb = Counter(tokens(a)), Counter(tokens(b))

    # Return 0.0 if either string has no tokens
    if not ca or not cb:
        return 0.0

    # Calculate the dot product of the token counts
    dot = sum(value * cb.get(token, 0) for token, value in ca.items())

    # Calculate the norms of both strings based on their token counts
    norm_a = sqrt(sum(value * value for value in ca.values()))
    norm_b = sqrt(sum(value * value for value in cb.values()))

    return dot / (norm_a * norm_b)

# Use a combination of content similarity and cosine similarity to calculate an overall similarity score between two lines
def combined(old: list[str], new: list[str], i: int, j: int) -> float:
    return 0.6 * content_similarity(old[i], new[j]) + 0.4 * cosine(context(old, i), context(new, j))

# Resolve the best matches between lines in the original and updated files based on the provided candidates and similarity threshold
def resolve(old: list[str], new: list[str], candidates: dict[int, list[int]], threshold: float = 0.55) -> list[tuple[int, int, float]]:

    # Create list of potential matches
    edges = []

    # Iterate through each line in the original file and its corresponding candidate matches in the updated file
    for i, choices in candidates.items():

        # Iterate through each candidate match for the current line in the original file
        for j in choices:

            # Calculate the combined similarity score for the current pair of lines
            score = combined(old, new, i, j)

            # If the similarity score meets or exceeds the threshold and at least one of the lines is non-empty, 
            # add the match to the list of potential matches
            if score >= threshold and (old[i] or new[j]):
                edges.append((i, j, score))

    # Sort the potential matches to prioritize the best matches
    # 1. descending similarity scores
    # 2. absolute difference in line indices (ascending)
    # 3. line indices themselves (ascending)
    edges.sort(key=lambda item: (-item[2], abs(item[0] - item[1]), item[0], item[1]))

    # Greedily select the highest-ranked non-conflicting proposals
    used_old, used_new, result = set(), set(), []
    for i, j, score in edges:
        if i not in used_old and j not in used_new:
            result.append((i, j, score))
            used_old.add(i)
            used_new.add(j)
    return sorted(result)
