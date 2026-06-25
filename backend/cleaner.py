import re

# Paths
input_file = r"C:\wamp64\www\AIKanbanLatest\AIKanban\app.py"
output_file = r"C:\Users\szjud\.gemini\antigravity\brain\1789015c-e5ac-4c3a-88e7-dc6d64d3f58e\clean_app.py"

with open(input_file, "r", encoding="utf-8", errors="replace") as f:
    text = f.read()

# Known mojibake mappings based on previous grep and screenshot
replacements = {
    "Ă˘â€ â€™": "->",           # Right arrow
    "Ă˘Ĺ›ĹąÄŹÂ¸Ĺą": "(Edit)",    # Pencil
    "Ă˘â€ťâ‚¬": "-",            # Box drawing horizontal
    "Ă˘Ĺ›â€¦": "[Save]",        # Save icon
    "Ă˘ĹĄĹš": "[X]",           # Cross mark
    "Ă˘Ĺ›â€ś": "[OK]",          # Check mark
    "€ťâ‚¬": "-",             # Stray box drawing part
    "Ä'ĹşĹ”â€šĂ©Ĺ›": "🎓",      # Graduation cap (from screenshot: page_icon)
    "Ä'ĹşĹ”": "🎓",
    "â€ś": '"',               # Smart quote right
    "â€ť": '"',               # Smart quote left
    "â€™": "'",               # Smart quote single
    "â€“": "-",               # En-dash
    "â€”": "-",               # Em-dash
}

for k, v in replacements.items():
    text = text.replace(k, v)

# Generic regex to strip any remaining ugly mojibake (sequences of Ă˘, Ä, etc.)
# We will just replace any character outside basic ASCII + Hungarian vowels with a space,
# EXCEPT if they are valid remaining emojis or box drawing (though we want it clean).
# To be safe, let's keep all standard characters, Hungarian chars, and replace the weird ones.

def clean_char(char):
    code = ord(char)
    # ASCII printable + newline/tab
    if 32 <= code <= 126 or code in (9, 10, 13):
        return char
    # Hungarian
    if char in "áéíóöőúüűÁÉÍÓÖŐÚÜŰ":
        return char
    # Graduation cap or other valid emoji we explicitly added
    if char == "🎓":
        return char
    # Everything else becomes empty string
    return ""

cleaned_text = "".join(clean_char(c) for c in text)

# Write output
with open(output_file, "w", encoding="utf-8") as f:
    f.write(cleaned_text)

print("Cleanup complete. Saved to artifact.")
