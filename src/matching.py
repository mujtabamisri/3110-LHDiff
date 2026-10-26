from collections import Counter
from math import sqrt
from .candidates import context, tokens


def levenshtein(a: str, b: str) -> int:
    if len(a) < len(b):
        a, b = b, a
    previous = list(range(len(b) + 1))
    for i, char_a in enumerate(a, 1):
        current = [i]
        for j, char_b in enumerate(b, 1):
            current.append(min(current[-1] + 1, previous[j] + 1,
                               previous[j-1] + (char_a != char_b)))
        previous = current
    return previous[-1]


def content_similarity(a: str, b: str) -> float:
    length = max(len(a), len(b))
    return 1.0 if length == 0 else 1 - levenshtein(a, b) / length


def cosine(a: str, b: str) -> float:
    ca, cb = Counter(tokens(a)), Counter(tokens(b))
    if not ca or not cb:
        return 0.0
    dot = sum(value * cb.get(token, 0) for token, value in ca.items())
    norm_a = sqrt(sum(value * value for value in ca.values()))
    norm_b = sqrt(sum(value * value for value in cb.values()))
    return dot / (norm_a * norm_b)


def combined(old: list[str], new: list[str], i: int, j: int) -> float:
    return 0.6 * content_similarity(old[i], new[j]) + 0.4 * cosine(context(old, i), context(new, j))


def resolve(old: list[str], new: list[str], candidates: dict[int, list[int]], threshold: float = 0.55) -> list[tuple[int, int, float]]:
    edges = []
    for i, choices in candidates.items():
        for j in choices:
            score = combined(old, new, i, j)
            if score >= threshold and (old[i] or new[j]):
                edges.append((i, j, score))
    edges.sort(key=lambda item: (-item[2], abs(item[0] - item[1]), item[0], item[1]))
    used_old, used_new, result = set(), set(), []
    for i, j, score in edges:
        if i not in used_old and j not in used_new:
            result.append((i, j, score))
            used_old.add(i)
            used_new.add(j)
    return sorted(result)
