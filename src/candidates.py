import hashlib
import re
from collections import Counter


def tokens(text: str) -> list[str]:
    return re.findall(r'[A-Za-z_][A-Za-z_0-9]*|\d+|[^\s]', text)


def simhash(text: str, bits: int = 64) -> int:
    counts = Counter(tokens(text))
    weights = [0] * bits
    for token, count in counts.items():
        digest = hashlib.blake2b(token.encode('utf-8'), digest_size=8).digest()
        value = int.from_bytes(digest, 'big')
        for bit in range(bits):
            weights[bit] += count if (value >> bit) & 1 else -count
    return sum(1 << bit for bit, weight in enumerate(weights) if weight > 0)


def context(lines: list[str], index: int, radius: int = 4) -> str:
    before = lines[max(0, index - radius):index]
    after = lines[index + 1:index + radius + 1]
    return ' '.join(before + after)


def shortlist(old: list[str], new: list[str], old_ids: list[int], new_ids: list[int], k: int = 15) -> dict[int, list[int]]:
    new_hashes = {j: (simhash(new[j]), simhash(context(new, j))) for j in new_ids}
    result = {}
    for i in old_ids:
        a, ac = simhash(old[i]), simhash(context(old, i))
        ranked = sorted(new_ids, key=lambda j: (
            0.6 * (a ^ new_hashes[j][0]).bit_count() +
            0.4 * (ac ^ new_hashes[j][1]).bit_count(),
            abs(i-j), j
        ))
        result[i] = ranked[:k]
    return result
