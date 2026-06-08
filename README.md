# NLP OCR Project

A small OCR + spellchecking project for English (and Telugu assets) that extracts text from images and post-processes it using a simple spellchecker and corpora.

## Repository Structure

- [backend/](backend/): OCR and spellcheck backend services
  - [backend/main.py](backend/main.py) — application entry point
  - [backend/ocr.py](backend/ocr.py) — OCR-related utilities
  - [backend/spellcheck.py](backend/spellcheck.py) — simple spellchecking functions
- [frontend/](frontend/) — minimal frontend runner ([frontend/index.py](frontend/index.py))
- [corpus/](corpus/) — text corpora and wordlists
  - [corpus/english_corpus.txt](corpus/english_corpus.txt)
  - [corpus/english_words.txt](corpus/english_words.txt)
- `requirements.txt` — Python dependencies

## Requirements

- Python 3.8+
- Install dependencies from `requirements.txt`.

```bash
python -m pip install -r requirements.txt
```

## Running

Backend (OCR + spellcheck):

```bash
python backend/main.py
```

Frontend (simple runner):

```bash
python frontend/index.py
```

Adjust commands if you prefer running modules with `-m` or via a virtual environment.

## Corpus and Data

Place or update corpora in the `corpus/` folder. The repo already includes sample files:

- [corpus/english_corpus.txt](corpus/english_corpus.txt)
- [corpus/english_words.txt](corpus/english_words.txt)

## Development Notes

- The backend contains OCR and spellcheck logic in `backend/`. Review [backend/ocr.py](backend/ocr.py) and [backend/spellcheck.py](backend/spellcheck.py) to adapt models, thresholds, or external OCR engines.
- The frontend is a small runner at [frontend/index.py](frontend/index.py).

## Contributing

Contributions welcome. Open an issue or submit a PR with a short description of the change.

## License

This project has no license file by default. Add a `LICENSE` file (e.g., MIT) if you intend to make this public.

---
Generated README for local development. If you'd like, I can add a `LICENSE`, CI workflow, or expand README sections with examples and API docs.
