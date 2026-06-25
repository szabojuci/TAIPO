import os
import subprocess

filepath = r"C:\wamp64\www\AIKanbanLatest\AIKanban\app.py"

def fix_code():
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    # Fix line 643: text-align:center;'>"</div>" -> text-align:center;'></div>"
    text = text.replace("'>\"</div>\",", "'></div>\",")
    text = text.replace("'>\"</div>\"", "'></div>\"")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)

while True:
    result = subprocess.run(["python", "-m", "py_compile", filepath], capture_output=True, text=True)
    if result.returncode == 0:
        print("Syntax is clean!")
        break
    else:
        # If there's an error, let's print it and we will manually add more replaces.
        print("Still has errors:\n" + result.stderr)
        
        # Auto-fix some known patterns based on stderr?
        if "'>\"</div>\"" in result.stderr:
            fix_code()
        else:
            break

fix_code()
result = subprocess.run(["python", "-m", "py_compile", filepath], capture_output=True, text=True)
if result.returncode == 0:
    print("Syntax is finally clean!")
else:
    print("Final error:\n" + result.stderr)
