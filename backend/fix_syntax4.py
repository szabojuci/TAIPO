import os
import subprocess

filepath = r"C:\wamp64\www\AIKanbanLatest\AIKanban\app.py"

def fix_code():
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    # Fix line 838: f"{course['name']}  ({course['code']})  "  " -> f"{course['name']}  ({course['code']})  "
    text = text.replace('f"{course[\'name\']}  ({course[\'code\']})  "  "', 'f"{course[\'name\']}  ({course[\'code\']})  "')
    
    # Also check if there are any others like it
    text = text.replace(')  "  "', ')  "')

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)

fix_code()
result = subprocess.run(["python", "-m", "py_compile", filepath], capture_output=True, text=True)
if result.returncode == 0:
    print("Syntax is finally clean!")
else:
    print("Final error:\n" + result.stderr)
