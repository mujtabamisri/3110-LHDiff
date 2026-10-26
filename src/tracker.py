from .preprocessing import normalized_lines
from .unchanged import unchanged_matches
from .candidates import shortlist
from .matching import resolve
from .splits import detect_splits


def track(old_raw: list[str], new_raw: list[str], threshold: float = 0.55) -> list[dict]:
    old, new = normalized_lines(old_raw), normalized_lines(new_raw)
    exact = unchanged_matches(old, new)
    result = [{'old': i+1, 'new': [j+1], 'type': 'unchanged', 'score': 1.0} for i, j in exact]
    used_old = {i for i, _ in exact}
    used_new = {j for _, j in exact}
    remaining_old = [i for i in range(len(old)) if i not in used_old]
    remaining_new = [j for j in range(len(new)) if j not in used_new]

    # Split detection precedes fuzzy one-to-one assignment so that a partial
    # first line cannot consume a complete multi-line correspondence.
    splits = detect_splits(old, new, remaining_old, remaining_new)
    for i, js, score in splits:
        used_old.add(i)
        used_new.update(js)
        result.append({'old': i+1, 'new': [j+1 for j in js], 'type': 'split', 'score': round(score, 4)})

    remaining_old = [i for i in range(len(old)) if i not in used_old]
    remaining_new = [j for j in range(len(new)) if j not in used_new]
    candidates = shortlist(old, new, remaining_old, remaining_new)
    for i, j, score in resolve(old, new, candidates, threshold):
        used_old.add(i)
        used_new.add(j)
        result.append({'old': i+1, 'new': [j+1], 'type': 'modified', 'score': round(score, 4)})

    for i in range(len(old)):
        if i not in used_old:
            result.append({'old': i+1, 'new': [], 'type': 'deleted', 'score': 0.0})
    for j in range(len(new)):
        if j not in used_new:
            result.append({'old': None, 'new': [j+1], 'type': 'added', 'score': 0.0})
    return sorted(result, key=lambda r: (r['old'] is None, r['old'] if r['old'] is not None else r['new'][0]))
