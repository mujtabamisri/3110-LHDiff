from .matching import content_similarity

# Detect split lines in the old and new source files based on a similarity threshold and maximum span
# Returns a list of tuples containing the old line index, a tuple of matching new line indices, and the similarity score
def detect_splits(old: list[str], new: list[str], remaining_old: list[int], remaining_new: list[int], threshold: float = 0.72, max_span: int = 8) -> list[tuple[int, tuple[int, ...], float]]:
    
    # Track segments that are available for matching
    available = set(remaining_new)

    # Store all potential split matches before selecting the best ones
    proposals = []

    # Examine each unmatched original segment
    for i in remaining_old:

        # Skip empty original segments
        if not old[i]:
            continue

        # Try matching the unmatched original segment against sequences of consecutive unmatched updated segments
        for start in remaining_new:

            # Store the indices of the new segments that are being considered for matching
            parts = []

            # Set temporary variable to track the previous similarity score for comparison
            previous = -1.0

            # Extend the sequence up to the maximum allowed span or until the end of the updated content is reached
            for j in range(start, min(start + max_span, len(new))):

                # Stop if the next segment is not available for matching
                if j not in available:
                    break

                # Add the segment to the current sequence
                parts.append(j)

                # Calculate the similarity score between the original segment and the concatenated updated segments
                score = content_similarity(old[i], ''.join(new[p] for p in parts))

                # If the similarity score decreases (ignoring small fluctuations), remove the last segment and stop extending the sequence
                if score < previous - 1e-9:
                    parts.pop()
                    break

                # Update the previous similarity score for the next iteration
                previous = score

            # If the concatenated updated segments' similarity score meets or exceeds the threshold,
            # add the match to the proposals list
            if len(parts) >= 2 and previous >= threshold:
                # proposals = (old line index, tuple of new line indices, similarity score)
                proposals.append((i, tuple(parts), previous))

    # Rank candidates by:
    # 1. Highest similarity score (x[2])
    # 2. Largest number of matched segments (len(x[1]))
    # 3. Lowest original segment index (x[0])
    # 4. Lowest starting index in the new content (x[1][0])
    proposals.sort(key=lambda x: (-x[2], -len(x[1]), x[0], x[1][0]))

    # Greedily select the highest-ranked non-conflicting proposals
    used_old, used_new, result = set(), set(), []
    for i, parts, score in proposals:
        if i not in used_old and not (set(parts) & used_new):
            result.append((i, parts, score))
            used_old.add(i)
            used_new.update(parts)
    return sorted(result)
