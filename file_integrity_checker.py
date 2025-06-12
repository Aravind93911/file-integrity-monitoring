
import os
import hashlib
import json

HASH_FILE = 'hashes.json'

def calculate_hash(filepath, algo='sha256'):
    h = hashlib.new(algo)
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def generate_hashes(directory, algo='sha256'):
    file_hashes = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if file == HASH_FILE or file.endswith('.pyc'):
                continue
            path = os.path.join(root, file)
            file_hashes[path] = calculate_hash(path, algo)
    return file_hashes

def save_hashes(hashes):
    with open(HASH_FILE, 'w') as f:
        json.dump(hashes, f, indent=4)

def load_hashes():
    if not os.path.exists(HASH_FILE):
        return {}
    with open(HASH_FILE, 'r') as f:
        return json.load(f)

def compare_hashes(old, new):
    for file, old_hash in old.items():
        if file not in new:
            print(f"[DELETED] {file}")
        elif old_hash != new[file]:
            print(f"[MODIFIED] {file}")
    for file in new:
        if file not in old:
            print(f"[NEW] {file}")

def main():
    print("1. Generate & Save Hashes")
    print("2. Verify Hashes")
    choice = input("Choose an option (1 or 2): ")

    directory = input("Enter the directory to scan: ").strip()

    if choice == '1':
        hashes = generate_hashes(directory)
        save_hashes(hashes)
        print("✅ Hashes saved successfully!")
    elif choice == '2':
        old_hashes = load_hashes()
        new_hashes = generate_hashes(directory)
        compare_hashes(old_hashes, new_hashes)
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()
