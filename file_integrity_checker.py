import os
import hashlib
import json
from datetime import datetime

HASH_FILE = "hashes.json"
DEFAULT_ALGO = "sha256"

def calculate_hash(filepath, algo=DEFAULT_ALGO):
    try:
        h = hashlib.new(algo)
        with open(filepath, "rb") as f:
            while chunk := f.read(8192):
                h.update(chunk)
        return h.hexdigest()
    except (PermissionError, FileNotFoundError):
        return None

def generate_hashes(directory, algo=DEFAULT_ALGO):
    file_hashes = {}
    directory = os.path.abspath(directory)

    for root, _, files in os.walk(directory):
        for file in files:
            if file == HASH_FILE or file.endswith(".pyc"):
                continue

            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, directory)

            file_hash = calculate_hash(full_path, algo)
            if file_hash:
                file_hashes[rel_path] = file_hash

    return file_hashes

def save_hashes(hashes):
    data = {
        "timestamp": datetime.now().isoformat(),
        "hashes": hashes
    }
    with open(HASH_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_hashes():
    if not os.path.exists(HASH_FILE):
        return {}

    with open(HASH_FILE, "r") as f:
        data = json.load(f)
        return data.get("hashes", {})

def compare_hashes(old, new):
    modified = deleted = added = 0

    for file, old_hash in old.items():
        if file not in new:
            print(f"[DELETED]  {file}")
            deleted += 1
        elif old_hash != new[file]:
            print(f"[MODIFIED] {file}")
            modified += 1

    for file in new:
        if file not in old:
            print(f"[NEW]      {file}")
            added += 1

    print("\n=== Scan Summary ===")
    print(f"Modified: {modified}")
    print(f"Deleted : {deleted}")
    print(f"New     : {added}")

def main():
    print("\n🔐 File Integrity Checker")
    print("1. Generate & Save Baseline")
    print("2. Verify Against Baseline")

    choice = input("Choose an option (1 or 2): ").strip()
    directory = input("Enter directory to scan: ").strip()

    if not os.path.isdir(directory):
        print("Invalid directory!")
        return

    if choice == "1":
        hashes = generate_hashes(directory)
        save_hashes(hashes)
        print("✅ Baseline created successfully.")

    elif choice == "2":
        old_hashes = load_hashes()
        if not old_hashes:
            print("No baseline found. Generate baseline first.")
            return

        new_hashes = generate_hashes(directory)
        compare_hashes(old_hashes, new_hashes)

    else:
        print("Invalid option.")

if __name__ == "__main__":
    main()
