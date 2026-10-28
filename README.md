# AI Audiobook Generator

Turn documents and images into narrated audiobooks. Upload a PDF, Word file, text file or image, and the app rewrites the content as audiobook-style narration with Google Gemini, optionally translates it, and converts it to an MP3 you can play or download.

Built with Python and Streamlit.

---

## Features

- **Multiple input formats** – PDF, DOCX, TXT, and images (PNG / JPG / JPEG via OCR)
- **AI narration rewrite** – Gemini (`gemini-2.5-flash`) rewrites the text as audiobook narration at a chosen difficulty level and returns structured JSON with `narration` and `tone` fields
- **Translation** – translate the narration into other languages before generating audio
- **Text-to-speech** – MP3 output using gTTS, with in-app playback and download
- **Speed control** – speeds below 1.0 use gTTS `slow=True`; if ffmpeg is installed the exact slider value is applied via the `atempo` filter
- **Collision-safe output** – each generation writes to a unique temp file so parallel sessions never overwrite each other

---

## How it works

```
Upload file → extraction.py → llm_enhancer.py → translator.py → tts_generator.py → audiobook_<uuid>.mp3
              (read text)      (Gemini JSON)      (optional)      (gTTS + ffmpeg)
```

| File | Role |
|---|---|
| `app.py` | Streamlit interface |
| `extraction.py` | Extracts text from PDF, DOCX, TXT and images (pdfplumber, python-docx, pytesseract) |
| `llm_enhancer.py` | Rewrites text as narration via Gemini API; returns JSON `{narration, tone}` |
| `translator.py` | Translates text with deep-translator |
| `tts_generator.py` | Converts text to speech with gTTS; applies speed via ffmpeg atempo when available |

---

## Setup

### 1. Clone and install

```bash
git clone https://github.com/sadiya37790/AudioBookGenerator.git
cd AudioBookGenerator
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Install Tesseract OCR *(needed only for image input)*

- **Windows** – install from the [Tesseract releases page](https://github.com/UB-Mannheim/tesseract/wiki) and add it to your PATH
- **macOS** – `brew install tesseract`
- **Linux** – `sudo apt install tesseract-ocr`

### 3. Install ffmpeg *(optional – enables exact speed control)*

- **Windows** – download from [ffmpeg.org](https://ffmpeg.org/download.html) and add `ffmpeg.exe` to your PATH
- **macOS** – `brew install ffmpeg`
- **Linux** – `sudo apt install ffmpeg`

Without ffmpeg the app still works; speeds below 1.0 use the gTTS `slow` mode and speeds above 1.0 play at normal speed.

### 4. Set your Gemini API key

Get a key from [Google AI Studio](https://aistudio.google.com/), then set it as an environment variable:

```bash
export GEMINI_API_KEY="your-key-here"
# Windows PowerShell:
$env:GEMINI_API_KEY="your-key-here"
```

> **Never commit your key to the repository.**

### 5. Run

```bash
streamlit run app.py
```

---

## Tech stack

Python · Streamlit · Google Gemini API · gTTS · deep-translator · pdfplumber · python-docx · pytesseract · Pillow · ffmpeg (optional)

---

## Known limitations

| Limitation | Detail |
|---|---|
| Internet required | Gemini, gTTS and translation all call online services |
| DOCX tables | Only paragraphs are extracted; tables and text boxes are skipped |
| Speed resolution | Without ffmpeg, only two speeds are available (normal ≥ 1.0, slow < 1.0) via gTTS |
| Long documents | Very long texts may hit Gemini API token limits; consider chunking |
| Image-only PDFs | Pages with no selectable text are silently skipped (OCR is not applied to PDF pages) |
| gTTS language coverage | Not all gTTS language codes support the `slow` parameter equally |

---

## Roadmap

- [ ] Chunking for long documents
- [ ] Per-chunk speed + tone control
- [ ] More natural TTS voices (e.g. Google Cloud TTS / ElevenLabs)
- [ ] OCR fallback for image-only PDF pages

---

## Project evolution

Started as a simple offline text-to-speech reader built with pyttsx3 for `.txt` files. It grew into a Streamlit app that reads PDF, DOCX and images, rewrites text as narration with Gemini, translates it, and generates downloadable MP3 audio.

---

## Author

Shaik Sadiya · [LinkedIn](https://linkedin.com)
