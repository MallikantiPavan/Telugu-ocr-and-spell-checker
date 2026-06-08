
# NLP OCR Project

Lightweight OCR + spellchecking utilities for English (and assets for Telugu). Use this repository to extract text from images and post-process it with simple spell correction and corpora lookups.

## Quick Start

- Python 3.8 or newer
- Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the backend (basic invocation):

```bash
python backend/main.py
```

Run the frontend demo (if present):

```bash
python frontend/index.py
```

You can redirect script output to a file to save extracted text, for example:

```bash
python backend/main.py > extracted_text.txt
```

## Folder Structure

Top-level layout (important files and folders):

- [backend/](backend/) — OCR and spellcheck logic
  - [backend/main.py](backend/main.py) — application entry point / runner
  - [backend/ocr.py](backend/ocr.py) — OCR utilities and image-to-text helpers
  - [backend/spellcheck.py](backend/spellcheck.py) — spell-check and correction utilities
- [frontend/](frontend/) — minimal frontend/demo runner
  - [frontend/index.py](frontend/index.py)
- [corpus/](corpus/) — corpora and wordlists used for post-processing
  - [corpus/english_corpus.txt](corpus/english_corpus.txt)
  - [corpus/english_words.txt](corpus/english_words.txt)
  - [corpus/telugu_words.txt](corpus/telugu_words.txt) (if present)
- `requirements.txt` — Python dependencies
- `.gitignore` — files to ignore (venv, zip bundles, images, caches)

## Inputs and Outputs

This section explains the expected inputs, where to put them, and where outputs appear.

Inputs
- Images: JPEG/PNG/TIFF images containing text to extract. You can keep them anywhere; a recommended location is `data/images/` (create this folder).
- Text files: plain `.txt` files used as corpora or dictionaries are under `corpus/`.

Outputs
- Extracted text: by default the scripts print extracted text to standard output. Redirect to a file to save results (see Quick Start example).
- Spellchecked text: the spellchecking utilities operate on text strings or files and will either print corrected text or return corrected strings when used as a module.

Example workflows

1) Basic image -> text (single file)

```bash
python backend/main.py path/to/image.jpg > output.txt
```

2) Batch processing (all images in a folder)

```bash
for img in data/images/*.{jpg,png}; do python backend/main.py "$img" >> all_outputs.txt; done
```

3) Spellcheck a saved text file

```bash
python -c "from backend import spellcheck; print(spellcheck.correct(open('output.txt').read()))" > output_corrected.txt
```

Note: the concrete CLI flags and behavior depend on the scripts in `backend/`. If you want, I can add explicit flags (e.g., `--input`, `--output`, `--batch`) to `backend/main.py` to make these workflows deterministic.

## Corpus and Data

Place custom corpora, dictionaries or additional wordlists in the `corpus/` folder. The repository includes sample English word lists and a corpus to get started.

## Development Notes

- Inspect and adapt OCR settings in [backend/ocr.py](backend/ocr.py) if you swap OCR engines or change preprocessing.
- Update or extend spell correction logic in [backend/spellcheck.py](backend/spellcheck.py) to use different algorithms, weighting, or external libraries.

## Contributing

Contributions welcome. File an issue describing the feature, then open a PR with a concise change and tests/examples where appropriate.

## License

No license file is included. Add a `LICENSE` (for example MIT) if you intend to publish this repository publicly.

---
If you'd like, I can update `backend/main.py` to accept `--input`/`--output` flags and add a small integration example — tell me which behavior you prefer.
