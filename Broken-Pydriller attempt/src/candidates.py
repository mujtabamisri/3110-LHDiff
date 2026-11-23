import hashlib
import re
from collections import Counter

# Split text into tokens, preserving identifiers, numbers, and punctuation
# Returns a list of tokens extracted from the input text
def tokens(text: str) -> list[str]:
    return re.findall(r'[A-Za-z_][A-Za-z_0-9]*|\d+|[^\s]', text)

# Simhash algorithm implementation for generating a hash value that represents the content of the text
def simhash(text: str, bits: int = 64) -> int:

    # Count the occurrences of each token in the text
    counts = Counter(tokens(text))

    # Initialize a list of weights for each bit position in the hash
    weights = [0] * bits

    # Iterate through each token and its count
    for token, count in counts.items():

        # Generate a 64-bit hash digest for each token using BLAKE2b
        digest = hashlib.blake2b(token.encode('utf-8'), digest_size=8).digest()

        # Convert the hash digest to an integer
        value = int.from_bytes(digest, 'big')

        # Update the weights for each bit position based on the token's count and its hash value
        for bit in range(bits):
            weights[bit] += count if (value >> bit) & 1 else -count

    # Return the final simhash value by setting bits with positive weights to 1 and those with non-positive weights to 0
    return sum(1 << bit for bit, weight in enumerate(weights) if weight > 0)

# Extract surrounding lines to provide additional context for a segment
# Greater radius values yield more context, but may introduce noise
def context(lines: list[str], index: int, radius: int = 4) -> str:

    # Get the lines before and after the specified index, within the given radius
    before = lines[max(0, index - radius):index]
    after = lines[index + 1:index + radius + 1]

    # Return a single string that combines the lines before and after the specified index, providing context for that line
    return ' '.join(before + after)

# Shortlist potential matches for each line in the original file based on simhash similarity
# Higher k values yield more candidates, but may introduce noise
def shortlist(old: list[str], new: list[str], old_ids: list[int], new_ids: list[int], k: int = 15) -> dict[int, list[int]]:
    
    # Precompute simhash values for the all new lines and their contexts to speed up the matching process
    new_hashes = {j: (simhash(new[j]), simhash(context(new, j))) for j in new_ids}

    # Save each line in the original file along with its context and rank potential matches from the new file based on simhash similarity
    result = {}

    # Iterate through each line in the original file
    for i in old_ids:

        # Compute the simhash values for the current line and its context
        a, ac = simhash(old[i]), simhash(context(old, i))

        # Rank potential matches from the new file based on simhash similarity, considering both the line and its context
        ranked = sorted(new_ids, key=lambda j: (

            # Similarity score is calculated based on Hamming distance (number of differing bits)
            0.6 * (a ^ new_hashes[j][0]).bit_count() +
            0.4 * (ac ^ new_hashes[j][1]).bit_count(),

            # Use the absolute difference in line indices as a secondary ranking criterion to prioritize matches that are closer together in the files
            abs(i-j), 
            
            # Use the line index in the new file as a final ranking criterion to break ties and ensure consistent ordering of matches
            j
        ))

        # Store the top k ranked matches for the current line in the result dictionary
        result[i] = ranked[:k]
    return result
