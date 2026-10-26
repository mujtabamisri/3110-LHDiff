import csv
import json
from pathlib import Path


def print_report(rows: list[dict]) -> None:
    print('OLD LINE -> NEW LINE(S) | STATUS | SCORE')
    print('-' * 54)
    for row in rows:
        old = '-' if row['old'] is None else str(row['old'])
        new = ','.join(map(str, row['new'])) or '-'
        print(f"{old:>8} -> {new:<12} | {row['type']:<9} | {row['score']:.4f}")


def export(rows: list[dict], path: str) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.suffix.lower() == '.json':
        target.write_text(json.dumps(rows, indent=2), encoding='utf-8')
    elif target.suffix.lower() == '.csv':
        with target.open('w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['old', 'new', 'type', 'score'])
            writer.writeheader()
            for row in rows:
                writer.writerow({**row, 'new': ','.join(map(str, row['new']))})
    else:
        raise ValueError('Export filename must end in .json or .csv')
