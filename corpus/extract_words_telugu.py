import html
import re
import unicodedata
from pathlib import Path

CORPUS_HTML = Path(__file__).parent / "telugu_corpus.html"
OUTPUT_FILE = Path(__file__).parent / "telugu_words.txt"
TELUGU_CHAR = re.compile(r"[\u0C00-\u0C7F]")


def strip_html(raw: str) -> str:
    raw = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", raw, flags=re.DOTALL | re.IGNORECASE)
    raw = re.sub(r"<[^>]+>", " ", raw)
    return html.unescape(raw)


def tokenize_telugu(text: str):
    tokens = []
    current = []
    has_telugu = False

    for ch in text:
        cat = unicodedata.category(ch)

        if ch.isalpha() or ch.isdigit():
            current.append(ch)
            if TELUGU_CHAR.match(ch):
                has_telugu = True
            continue
        if cat in {"Mn", "Mc", "Me"} and current:
            current.append(ch)
            continue
        if current and has_telugu:
            tokens.append("".join(current))
        current = []
        has_telugu = False

    if current and has_telugu:
        tokens.append("".join(current))

    return tokens


def main():
    print(f"Reading: {CORPUS_HTML}")
    raw = CORPUS_HTML.read_text(encoding="utf-8", errors="replace")

    plain = strip_html(raw)

    words = tokenize_telugu(plain)
    seen = set()
    unique_words = []
    for w in words:
        key = unicodedata.normalize("NFC", w)
        if key not in seen and len(key) >= 2:  
            seen.add(key)
            unique_words.append(key)

    unique_words.sort()

    OUTPUT_FILE.write_text("\n".join(unique_words), encoding="utf-8")

    print(f"Done. {len(unique_words)} unique Telugu words → {OUTPUT_FILE}")
    print("First 20 words preview:")
    for w in unique_words[:20]:
        print(" ", w)


if __name__ == "__main__":
    main()
