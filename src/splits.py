from .matching import content_similarity


def detect_splits(old: list[str], new: list[str], old_ids: list[int], new_ids: list[int], threshold: float = 0.72, max_span: int = 8) -> list[tuple[int, tuple[int, ...], float]]:
    available = set(new_ids)
    proposals = []
    for i in old_ids:
        if not old[i]:
            continue
        for start in new_ids:
            parts = []
            previous = -1.0
            for j in range(start, min(start + max_span, len(new))):
                if j not in available:
                    break
                parts.append(j)
                score = content_similarity(old[i], ''.join(new[p] for p in parts))
                if score < previous - 1e-9:
                    parts.pop()
                    break
                previous = score
            if len(parts) >= 2 and previous >= threshold:
                proposals.append((i, tuple(parts), previous))
    proposals.sort(key=lambda x: (-x[2], -len(x[1]), x[0], x[1][0]))
    used_old, used_new, result = set(), set(), []
    for i, parts, score in proposals:
        if i not in used_old and not (set(parts) & used_new):
            result.append((i, parts, score))
            used_old.add(i)
            used_new.update(parts)
    return sorted(result)
