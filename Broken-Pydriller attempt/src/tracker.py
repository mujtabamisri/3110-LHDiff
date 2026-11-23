from .preprocessing import normalized_lines
from .unchanged import unchanged_matches
from .candidates import shortlist
from .matching import resolve
from .splits import detect_splits

# Takes two lists of raw lines (old and new) and a similarity threshold
# Returns a list of dictionaries representing the line tracking results
def track(old_raw: list[str], new_raw: list[str], threshold: float = 0.55) -> list[dict]:

    # Normalize lines from both files to make comparisons more consistent
    old, new = normalized_lines(old_raw), normalized_lines(new_raw)

    # Identify lines that match exactly between the original and updated files using the unchanged_matches function
    exact = unchanged_matches(old, new)

    # Record all exact matches as unchanged and their corresponding line numbers
    result = [{'old': i+1, 'new': [j+1], 'type': 'unchanged', 'score': 1.0} for i, j in exact]

    # Keep track of original and updated line indices that have already been matched
    # Get first element of each tuple in exact and store in used_old, and second element in used_new
    used_old = {i for i, _ in exact}
    used_new = {j for _, j in exact}

    # Identify lines that have not yet been matched in either file
    remaining_old = [i for i in range(len(old)) if i not in used_old]
    remaining_new = [j for j in range(len(new)) if j not in used_new]

    # Split detection precedes fuzzy one-to-one assignment so that a partial
    # first line cannot consume a complete multi-line correspondence
    splits = detect_splits(old, new, remaining_old, remaining_new)

    # Record all split matches, marking the original line as split and the corresponding new lines
    for i, js, score in splits:
        used_old.add(i)
        used_new.update(js)
        result.append({'old': i+1, 'new': [j+1 for j in js], 'type': 'split', 'score': round(score, 4)})

    # Recalculate the unmatched lines after processing split relationships
    remaining_old = [i for i in range(len(old)) if i not in used_old]
    remaining_new = [j for j in range(len(new)) if j not in used_new]

    # Shortlist potential matches for each line in the original file based on simhash similarity
    candidates = shortlist(old, new, remaining_old, remaining_new)

    # Resolve the shortlisted candidates into final matches based on combined similarity metrics
    for i, j, score in resolve(old, new, candidates, threshold):
        used_old.add(i)
        used_new.add(j)
        result.append({'old': i+1, 'new': [j+1], 'type': 'modified', 'score': round(score, 4)})

    # Identify remaining lines in the original file that were not matched and mark them as deleted
    for i in range(len(old)):
        if i not in used_old:
            result.append({'old': i+1, 'new': [], 'type': 'deleted', 'score': 0.0})

    # Identify remaining lines in the updated file that were not matched and mark them as added
    for j in range(len(new)):
        if j not in used_new:
            result.append({'old': None, 'new': [j+1], 'type': 'added', 'score': 0.0})

    # Sort the results first by whether the original line is None (added lines come last),
    # and then by the original line number (or the first new line number if the original line is None)
    return sorted(result, key=lambda r: (r['old'] is None, r['old'] if r['old'] is not None else r['new'][0]))
