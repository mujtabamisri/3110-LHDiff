from src.preprocessing import read_lines
from src.tracker import track
from src.report import print_report, export
from pydriller import Repository
import os
import shutil

def main():
    local_repo_path = r"C:\Users\avapa\Downloads\3110-LHDiff-main\3110-LHDiff-main" 
    
    commit_hashes = []
    for commit in Repository(local_repo_path).traverse_commits():
        commit_hashes.append(commit.hash)

    if not commit_hashes:
        print("Error: No commits found in the repository.")
        return

    # Get the oldest commit (first in history)
    for commit in Repository(local_repo_path, single=commit_hashes[0]).traverse_commits():
        print(f"Old Commit: {commit.msg}")
        for mod in commit.modified_files:
            if mod.source_code:
                with open("old.java", "w", encoding="utf-8") as file:
                    file.write(mod.source_code)

    # Get the newest commit (last in history)
    for commit in Repository(local_repo_path, single=commit_hashes[-1]).traverse_commits():
        print(f"New Commit: {commit.msg}")
        for mod in commit.modified_files:
            if mod.source_code:
                with open("new.java", "w", encoding="utf-8") as file:
                    file.write(mod.source_code)

    # Ensure dataset directory exists
    os.makedirs("dataset", exist_ok=True)
    
    old_dest = os.path.join("dataset", "old.java")
    new_dest = os.path.join("dataset", "new.java")
    
    if os.path.exists("old.java"):
        shutil.move("old.java", old_dest)
    if os.path.exists("new.java"):
        shutil.move("new.java", new_dest)

    # Run tracker directly using the generated dataset paths
    threshold = 0.55
    rows = track(read_lines(old_dest), read_lines(new_dest), threshold)

    # Display results
    print_report(rows)

if __name__ == '__main__':
    main()