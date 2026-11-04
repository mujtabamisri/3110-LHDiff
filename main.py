import argparse
from src.preprocessing import read_lines
from src.tracker import track
from src.report import print_report, export


def main():
    
    # Create an argument parser to handle command-line inputs
    parser = argparse.ArgumentParser(description='Language-independent source line tracker')

    # Define the required input files: the original and updated source files
    parser.add_argument('old', help='Original source file')
    parser.add_argument('new', help='Updated source file')

    # Set an optional similarity threshold, defaulting to 0.55 (55%)
    # Higher thresholds will result in fewer matches, while lower thresholds may yield more matches
    parser.add_argument('--threshold', type=float, default=0.55)

    # Define an optional output file for exporting results in JSON or CSV format
    parser.add_argument('--export', help='Output .json or .csv file')

    # Parse the command-line arguments provided by the user
    args = parser.parse_args()

    # Validate that the similarity threshold is between 0 and 1
    if not 0 <= args.threshold <= 1:
        parser.error('--threshold must be between 0 and 1')

    # Read both source files using the read_lines function
    # and compare their lines based on the specified threshold using the track function
    rows = track(read_lines(args.old), read_lines(args.new), args.threshold)

    # Display the line-tracking results in the console using the print_report function
    print_report(rows)

    # If an export file was specified, save the results and confirm the export
    if args.export:
        export(rows, args.export)
        print(f'Exported to {args.export}')

# Standard main function check to allow the script to be run directly
if __name__ == '__main__':
    main()
