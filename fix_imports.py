import os
import re

def fix_imports_in_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    changed = False
    new_lines = []
    for line in lines:
        # Remove leading dots in 'from ... import ...'
        new_line = re.sub(r'^(from\s+)(\.+)(\w+)', r'\1\3', line)
        # Remove leading dots in 'import ...'
        new_line = re.sub(r'^(import\s+)(\.+)(\w+)', r'\1\3', new_line)
        if new_line != line:
            changed = True
        new_lines.append(new_line)

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f"Fixed imports in {filepath}")

def walk_and_fix(folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.py'):
                fix_imports_in_file(os.path.join(root, file))

if __name__ == "__main__":
    # Change '.' to your project root if needed
    walk_and_fix('.')