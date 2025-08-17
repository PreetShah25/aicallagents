import re
PROPER = re.compile(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b")
STOP = {"System","Investor","Expert","Moderator","Q","A"}
def redact_names_simple(text: str) -> str:
    def repl(m):
        name = m.group(1)
        return "[REDACTED_NAME]" if name not in STOP else name
    return PROPER.sub(repl, text)
