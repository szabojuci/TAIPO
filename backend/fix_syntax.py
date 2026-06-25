import re

filepath = r"C:\wamp64\www\AIKanbanLatest\AIKanban\app.py"
with open(filepath, "r", encoding="utf-8") as f:
    text = f.read()

text = re.sub(r'f"### \(Edit\) Edit User "\s*`\{en\}`"', r'f"### (Edit) Edit User `{en}`"', text)
text = re.sub(r'f"### \(Edit\) Edit Course "\s*`\{ec\}`"', r'f"### (Edit) Edit Course `{ec}`"', text)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(text)

print("Syntax fixed")
