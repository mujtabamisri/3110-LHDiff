# COMP 3110 - LHDiff Source Code Line Tracker

A Python-based, language-independent source code line-tracking tool developed for **COMP 3110 - Introduction to Software Engineering**.

The project implements a simplified version of the **LHDiff (Language-Independent Hybrid Diff)** algorithm to identify corresponding lines between two versions of a source code file.

## Project Goal 1

Given two different versions of a source code file, identify and print which lines from the old file correspond to lines in the new file.

### Features

- Compare two versions of a source code file.
- Detect unchanged and modified lines.
- Identify reordered or moved lines.
- Detect when a line is split into multiple lines.
- Calculate similarity scores using Levenshtein distance, cosine similarity, SimHash, and Hamming distance.
- Export comparison results to JSON or CSV.
- Run automated unit tests.
- Support text-based source files from different programming languages.

## Requirements

- Python 3.10 or newer
- Visual Studio Code (recommended)
- Windows, macOS, or Linux

No external Python packages or paid APIs are required.

## Installation and Setup

### Step 1 — Open the project

1. Download and extract the project ZIP file.
2. Open Visual Studio Code.
3. Select **File → Open Folder**.
4. Open the `3110-LHDiff` folder.
5. Open the integrated terminal using **Terminal → New Terminal**.

### Step 2 — Verify Python

Run the following command:

```powershell
py --version
```

Example output:

```text
Python 3.14.3
```

**Note:** On macOS or Linux, use `python3` instead of `py` in the commands below.

## Running the Application

### Step 3 — Compare two files

Run:

```powershell
py main.py examples/old.java examples/new.java
```

The program compares the two Java files and prints their corresponding line mappings.

### Example Output

```text
OLD LINE -> NEW LINE(S) | STATUS | SCORE
------------------------------------------------------
       1 -> 1            | unchanged | 1.0000
       2 -> 2            | unchanged | 1.0000
       3 -> 3            | modified  | 0.7457
       4 -> 4            | modified  | 0.7310
       5 -> 5            | unchanged | 1.0000
       6 -> 6            | unchanged | 1.0000
```

The output includes:

- **Old Line:** Original line number.
- **New Line:** Corresponding line number in the updated file.
- **Status:** Classification of the matched line.
- **Score:** Similarity score calculated by the algorithm.

## Exporting Results

### Step 4 — Export as JSON

```powershell
py main.py examples/old.java examples/new.java --export results/mapping.json
```

The comparison results will be saved to:

```text
results/mapping.json
```

### Step 5 — Export as CSV

```powershell
py main.py examples/old.java examples/new.java --export results/mapping.csv
```

The comparison results will be saved to:

```text
results/mapping.csv
```

## Running Automated Tests

### Step 6 — Execute unit tests

Run:

```powershell
py -m unittest discover -s tests -v
```

The included tests cover:

1. Whitespace normalization
2. Identical lines
3. Inserted lines
4. Deleted lines
5. Reordered lines
6. Split lines
7. Content similarity

Expected successful test summary:

```text
Ran 7 tests

OK
```

## Comparing Your Own Source Files

### Step 7 — Add custom files

Place your source files in the `examples` directory.

For example:

```text
examples/
├── old.py
└── new.py
```

Run:

```powershell
py main.py examples/old.py examples/new.py
```

The application will compare the two Python files and generate line mappings.

The same process can be used for Java, JavaScript, C++, C#, and other text-based source files.

## Project Structure

```text
COMP3110-LHDiff/
│
├── main.py
├── README.md
│
├── src/
│   ├── __init__.py
│   ├── preprocessing.py
│   ├── unchanged.py
│   ├── candidates.py
│   ├── matching.py
│   ├── splits.py
│   ├── tracker.py
│   └── report.py
│
├── examples/
│   ├── old.java
│   └── new.java
│
├── tests/
│   └── test_tracking.py
│
└── results/
    ├── mapping.json
    └── mapping.csv
```

The `results` files are generated when the corresponding export commands are run.

## LHDiff Algorithm

The application follows five primary algorithm stages:

### 1. Preprocessing

Normalizes source code lines to reduce differences caused by whitespace and formatting.

**File:** `src/preprocessing.py`

### 2. Detect Unchanged Lines

Identifies unchanged sequences of lines between the old and new files.

**File:** `src/unchanged.py`

### 3. Generate Candidate Matches

Uses SimHash and Hamming distance to identify likely matches for changed lines.

**File:** `src/candidates.py`

### 4. Resolve Conflicts

Calculates content and contextual similarity scores to select suitable line mappings.

**File:** `src/matching.py`

The combined similarity score is:

`Similarity = 0.6 × Content Similarity + 0.4 × Context Similarity`

### 5. Detect Line Splitting

Identifies cases where a single original line corresponds to multiple consecutive lines in the new file.

**File:** `src/splits.py`

The implementation performs split detection before final fuzzy matching to reduce interference from partial matches.

## Project Goals

| Goal | Description | Status |
|---|---|---|
| Goal 1 | Source code line tracking | Implemented |
| Goal 2 | Create and evaluate a 25-file dataset | Planned |
| Goal 3 | Identify bug-introducing changes using Git history | Planned |

## Current Limitations

- The application currently uses a command-line interface.
- Matching is heuristic and may produce incorrect results for ambiguous or heavily modified code.
- Accuracy on large real-world datasets has not yet been established.
- Goals 2 and 3 are not included in this implementation.

## Quick Command Reference

**Run the application:**

```powershell
py main.py examples/old.java examples/new.java
```

**Export JSON:**

```powershell
py main.py examples/old.java examples/new.java --export results/mapping.json
```

**Export CSV:**

```powershell
py main.py examples/old.java examples/new.java --export results/mapping.csv
```

**Run tests:**

```powershell
py -m unittest discover -s tests -v
```

---

**Course:** COMP 3110 — Introduction to Software Engineering

**Project:** A Language-Independent Approach for Tracking Source Code Lines

**Implementation:** Python

**Current Scope:** Goal 1 — Source Code Line Tracking