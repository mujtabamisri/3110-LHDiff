import argparse
from src.preprocessing import read_lines
from src.tracker import track
from src.report import print_report, export


def main():
    parser = argparse.ArgumentParser(description='Language-independent source line tracker')
    parser.add_argument('old', help='Original source file')
    parser.add_argument('new', help='Updated source file')
    parser.add_argument('--threshold', type=float, default=0.55)
    parser.add_argument('--export', help='Output .json or .csv file')
    args = parser.parse_args()
    if not 0 <= args.threshold <= 1:
        parser.error('--threshold must be between 0 and 1')
    rows = track(read_lines(args.old), read_lines(args.new), args.threshold)
    print_report(rows)
    if args.export:
        export(rows, args.export)
        print(f'Exported to {args.export}')


if __name__ == '__main__':
    main()
