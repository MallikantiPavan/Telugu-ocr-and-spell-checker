import unicodedata
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence


DEFAULT_LEXICON_ENG = {
    "a",
    "an",
    "and",
    "assignment",
    "algorithm",
    "algorithms",
    "backoff",
    "benchmark",
    "button",
    "check",
    "checker",
    "click",
    "content",
    "correct",
    "correctness",
    "data",
    "distance",
    "document",
    "edit",
    "english",
    "example",
    "feed",
    "file",
    "hamming",
    "highlight",
    "image",
    "images",
    "input",
    "language",
    "last",
    "levenshtein",
    "longest",
    "lcs",
    "morphological",
    "portal",
    "probable",
    "program",
    "rich",
    "segment",
    "sequence",
    "spell",
    "spelling",
    "statistics",
    "submission",
    "telugu",
    "text",
    "textarea",
    "token",
    "tokens",
    "user",
    "word",
    "wrong",
}

DEFAULT_LEXICON_TEL = {
    "అక్షరం",
    "అక్షరాలు",
    "అది",
    "అనేది",
    "అని",
    "అన్నీ",
    "ఆ",
    "ఆమె",
    "ఆయన",
    "ఇది",
    "ఇలా",
    "ఈ",
    "ఈరోజు",
    "ఉంది",
    "ఉన్న",
    "ఉన్నాయి",
    "ఎక్కడ",
    "ఎలా",
    "ఏం",
    "ఒక",
    "ఒక్క",
    "కాదు",
    "కాని",
    "కంటే",
    "కలదు",
    "కావాలి",
    "కి",
    "కూడా",
    "కోసం",
    "గురించి",
    "చాలా",
    "చేస్తుంది",
    "చేయాలి",
    "చేసి",
    "చేసింది",
    "చేసిన",
    "జరిగింది",
    "తెలుగు",
    "తెలుసు",
    "తన",
    "తర్వాత",
    "తప్పు",
    "తప్పులు",
    "దాని",
    "దీని",
    "ద్వారా",
    "నాకు",
    "నుండి",
    "నేను",
    "పదం",
    "పదాలు",
    "పరీక్ష",
    "ప్రతి",
    "ప్రధాన",
    "ప్రోగ్రామ్",
    "భాష",
    "మంచి",
    "మరియు",
    "మొత్తం",
    "యొక్క",
    "లేదా",
    "లో",
    "వంటి",
    "వారు",
    "విషయం",
    "సరైన",
    "సరిగా",
    "సమయం",
    "సమాచారం",
    "సహాయం",
}


def _is_telugu_word(token: str) -> bool:
    if not token:
        return False
    has_telugu_base = False
    for ch in token:
        code = ord(ch)
        cat = unicodedata.category(ch)
        if 0x0C00 <= code <= 0x0C7F:
            if cat.startswith("L"):
                has_telugu_base = True
            continue
        if cat in {"Mn", "Mc", "Me"}:
            continue
        return False
    return has_telugu_base


def _is_english_word(token: str) -> bool:
    if not token:
        return False
    cleaned = token.replace("'", "")
    return len(cleaned) >= 2 and cleaned.isascii() and cleaned.isalpha()


def _load_corpus_words(corpus_path) -> set:
    from pathlib import Path

    p = Path(corpus_path)
    if not p.exists() or p.suffix.lower() != ".txt":
        return set()

    words = set()
    for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
        current = []
        for ch in line.strip():
            cat = unicodedata.category(ch)
            if ch.isalpha() or ch.isdigit() or cat in {"Mn", "Mc", "Me"}:
                current.append(ch)
            else:
                if current:
                    words.add(unicodedata.normalize("NFC", "".join(current)))
                    current = []
        if current:
            words.add(unicodedata.normalize("NFC", "".join(current)))
    return words


def _load_telugu_corpus_words_from_dir(corpus_dir) -> set:
    from pathlib import Path

    directory = Path(corpus_dir)
    if not directory.exists():
        return set()

    merged = set()
    for path in sorted(directory.glob("*.txt")):
        merged.update(_load_corpus_words(path))
    return {w for w in merged if len(w) >= 2 and _is_telugu_word(w)}


def _load_telugu_dictionary_words_from_dir(corpus_dir) -> set:
    from pathlib import Path

    directory = Path(corpus_dir)
    if not directory.exists():
        return set()

    merged = set()
    for path in sorted(directory.glob("*.txt")):
        lower_name = path.name.lower()
        if "dict" not in lower_name:
            continue
        merged.update(_load_corpus_words(path))
    return {w for w in merged if len(w) >= 2 and _is_telugu_word(w)}


_CORPUS_DIR = __file__  
import os as _os
_TEL_CORPUS_DIR = _os.path.normpath(
    _os.path.join(_os.path.dirname(_CORPUS_DIR), "..", "corpus")
)
_TEL_CORPUS_WORDS: set = _load_telugu_corpus_words_from_dir(_TEL_CORPUS_DIR)
_TEL_BENCHMARK_WORDS: set = _load_telugu_dictionary_words_from_dir(_TEL_CORPUS_DIR)
_ENG_CORPUS_FILE = _os.path.normpath(
    _os.path.join(_os.path.dirname(_CORPUS_DIR), "..", "corpus", "english_words.txt")
)
_ENG_CORPUS_WORDS: set = {
    w.lower() for w in _load_corpus_words(_ENG_CORPUS_FILE) if _is_english_word(w)
}


def get_default_lexicon(language: str) -> set:
    if (language or "").lower().startswith("tel"):
        base = set(DEFAULT_LEXICON_TEL)
        base.update(_TEL_CORPUS_WORDS) 
        return base

    base = set(DEFAULT_LEXICON_ENG)
    base.update(_ENG_CORPUS_WORDS)
    return base


@dataclass
class WordResult:
    word: str
    hamming: Optional[str]
    lcs: str
    levenshtein: str
    jaro: str
    benchmark: str
    backoff_parts: List[Dict[str, str]]


def tokenize(text: str) -> List[str]:
    tokens: List[str] = []
    current: List[str] = []
    has_base_char = False

    for ch in text:
        cat = unicodedata.category(ch)
        if ch.isalpha() or ch.isdigit():
            current.append(ch)
            has_base_char = True
            continue

        if cat in {"Mn", "Mc", "Me"} and current:
            current.append(ch)
            continue

        if current and has_base_char:
            tokens.append("".join(current))
        current = []
        has_base_char = False

    if current and has_base_char:
        tokens.append("".join(current))

    return tokens


def normalize_lexicon(words: Sequence[str]) -> List[str]:
    normalized = []
    seen = set()
    for w in words:
        candidate = w.strip().lower()
        if candidate and candidate not in seen:
            seen.add(candidate)
            normalized.append(candidate)
    return normalized


def hamming_distance(a: str, b: str) -> Optional[int]:
    if len(a) != len(b):
        return None
    return sum(ch1 != ch2 for ch1, ch2 in zip(a, b))


def lcs_length(a: str, b: str) -> int:
    m = len(a)
    n = len(b)
    prev = [0] * (n + 1)
    for i in range(1, m + 1):
        curr = [0] * (n + 1)
        ai = a[i - 1]
        for j in range(1, n + 1):
            if ai == b[j - 1]:
                curr[j] = prev[j - 1] + 1
            else:
                curr[j] = max(prev[j], curr[j - 1])
        prev = curr
    return prev[n]


def levenshtein_distance(a: str, b: str) -> int:
    m = len(a)
    n = len(b)
    if m == 0:
        return n
    if n == 0:
        return m

    prev = list(range(n + 1))
    for i in range(1, m + 1):
        curr = [i] + [0] * n
        ai = a[i - 1]
        for j in range(1, n + 1):
            cost = 0 if ai == b[j - 1] else 1
            curr[j] = min(
                prev[j] + 1,
                curr[j - 1] + 1,
                prev[j - 1] + cost,
            )
        prev = curr
    return prev[n]


def jaro_distance(a: str, b: str) -> float:
    if a == b:
        return 1.0
    len_a = len(a)
    len_b = len(b)
    if len_a == 0 or len_b == 0:
        return 0.0

    match_distance = max(len_a, len_b) // 2 - 1
    a_matches = [False] * len_a
    b_matches = [False] * len_b

    matches = 0
    for i in range(len_a):
        start = max(0, i - match_distance)
        end = min(i + match_distance + 1, len_b)
        for j in range(start, end):
            if b_matches[j] or a[i] != b[j]:
                continue
            a_matches[i] = True
            b_matches[j] = True
            matches += 1
            break

    if matches == 0:
        return 0.0

    transpositions = 0
    j = 0
    for i in range(len_a):
        if not a_matches[i]:
            continue
        while not b_matches[j]:
            j += 1
        if a[i] != b[j]:
            transpositions += 1
        j += 1

    transpositions /= 2
    return (
        (matches / len_a)
        + (matches / len_b)
        + ((matches - transpositions) / matches)
    ) / 3.0


def _best_match_hamming(word: str, lexicon: Sequence[str]) -> Optional[str]:
    candidates = [w for w in lexicon if len(w) == len(word)]
    if not candidates:
        return None
    return min(candidates, key=lambda w: hamming_distance(word, w))


def _best_match_lcs(word: str, lexicon: Sequence[str]) -> str:
    return max(lexicon, key=lambda w: (lcs_length(word, w), -abs(len(word) - len(w))))


def _best_match_levenshtein(word: str, lexicon: Sequence[str]) -> str:
    return min(
        lexicon,
        key=lambda w: (
            levenshtein_distance(word, w),
            -lcs_length(word, w),
            abs(len(word) - len(w)),
        ),
    )


def _best_match_jaro(word: str, lexicon: Sequence[str]) -> str:
    return max(lexicon, key=lambda w: (jaro_distance(word, w), -abs(len(word) - len(w))))


def _build_backoff_parts(
    word: str,
    benchmark: str,
    lexicon_set: set,
    lev_suggestion: str,
) -> List[Dict[str, str]]:
    if benchmark == "Correct":
        return [{"text": word, "status": "correct"}]

    best_prefix_len = 0
    for i in range(1, len(word)):
        if word[:i] in lexicon_set:
            best_prefix_len = i

    if best_prefix_len > 0:
        return [
            {"text": word[:best_prefix_len], "status": "correct"},
            {
                "text": word[best_prefix_len:],
                "status": "wrong",
                "suggestion": lev_suggestion,
            },
        ]

    lcs_len = lcs_length(word, lev_suggestion)
    if lcs_len <= 1:
        return [{"text": word, "status": "wrong", "suggestion": lev_suggestion}]

    keep = []
    i = 0
    j = 0
    while i < len(word) and j < len(lev_suggestion):
        if word[i] == lev_suggestion[j]:
            keep.append(i)
            i += 1
            j += 1
        elif len(word) - i > len(lev_suggestion) - j:
            i += 1
        else:
            j += 1

    parts = []
    start = 0
    while start < len(word):
        current_status = "correct" if start in keep else "wrong"
        end = start + 1
        while end < len(word) and ((end in keep) == (start in keep)):
            end += 1
        segment = {"text": word[start:end], "status": current_status}
        if current_status == "wrong":
            segment["suggestion"] = lev_suggestion
        parts.append(segment)
        start = end
    return parts


def spell_check_text(
    text: str,
    custom_lexicon: Optional[Sequence[str]] = None,
    language: str = "eng",
) -> Dict[str, object]:
    tokens = [unicodedata.normalize("NFC", t.lower()) for t in tokenize(text)]

    base_lexicon = get_default_lexicon(language)

    if custom_lexicon:
        custom = normalize_lexicon(custom_lexicon)
        base_lexicon.update(custom)

    lexicon = sorted(base_lexicon)
    if not lexicon:
        return {"tokens": [], "complexity": {}}

    results: List[WordResult] = []
    for token in tokens:
        hamming_match = _best_match_hamming(token, lexicon)
        lcs_match = _best_match_lcs(token, lexicon)
        lev_match = _best_match_levenshtein(token, lexicon)
        jaro_match = _best_match_jaro(token, lexicon)
        benchmark = "Correct" if token in base_lexicon else "Wrong"
        backoff_parts = _build_backoff_parts(token, benchmark, base_lexicon, lev_match)

        results.append(
            WordResult(
                word=token,
                hamming=hamming_match,
                lcs=lcs_match,
                levenshtein=lev_match,
                jaro=jaro_match,
                benchmark=benchmark,
                backoff_parts=backoff_parts,
            )
        )

    avg_token_len = (sum(len(t) for t in tokens) / len(tokens)) if tokens else 0.0
    avg_lex_len = (sum(len(w) for w in lexicon) / len(lexicon)) if lexicon else 0.0
    complexity = {
        "token_count": len(tokens),
        "lexicon_size": len(lexicon),
        "avg_token_length": round(avg_token_len, 2),
        "avg_lexicon_word_length": round(avg_lex_len, 2),
        "per_comparison": {
            "hamming": "O(L)",
            "lcs": "O(L^2)",
            "levenshtein": "O(L^2)",
            "jaro": "O(L)",
            "backoff": "O(L^2)",
        },
        "overall": "O(T * D * L^2), where T=tokens, D=lexicon size, L=average word length",
    }

    return {
        "tokens": [r.__dict__ for r in results],
        "complexity": complexity,
    }