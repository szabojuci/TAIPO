import os
import subprocess

filepath = r"C:\wamp64\www\AIKanbanLatest\AIKanban\app.py"

def fix_code():
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    # Fix button texts that got mangled into "'""
    text = text.replace('c_del.button("\'""', 'c_del.button("[X]"')
    text = text.replace('button("\'""', 'button("[X]"')
    
    # Let's fix any stray "'"" just in case
    text = text.replace('\'""', '"')

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)

fix_code()

# Check syntax
result = subprocess.run(["python", "-m", "py_compile", filepath], capture_output=True, text=True)
if result.returncode == 0:
    print("Syntax is clean!")
else:
    print("Still has errors:\n" + result.stderr)
