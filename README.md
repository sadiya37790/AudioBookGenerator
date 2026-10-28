AI Audiobook Generator

Turn documents and images into narrated audiobooks. Upload a PDF, Word file, text file or image, and the app rewrites the content as audiobook-style narration with Google Gemini, optionally translates it, and converts it to an MP3 you can play or download.

Built with Python and Streamlit.

Features
Multiple input formats: PDF, DOCX, TXT, and images (PNG/JPG/JPEG via OCR)
AI narration rewrite: Gemini (gemini-2.5-flash) rewrites the text as audiobook narration at a chosen difficulty level
Translation: translate the narration into other languages before generating audio
Text-to-speech: MP3 output using gTTS, with in-app playback and download
How it works
Upload file -> extraction.py -> llm_enhancer.py -> translator.py -> tts_generator.py -> audiobook.mp3
               (read text)      (Gemini rewrite)   (optional)       (gTTS)
File	Role
app.py	Streamlit interface
extraction.py	Extracts text from PDF, DOCX, TXT and images (pdfplumber, python-docx, pytesseract)
llm_enhancer.py	Rewrites text as narration using the Gemini API
translator.py	Translates text with deep-translator
tts_generator.py	Converts text to speech with gTTS
Setup

1. Clone and install

bash
git clone https://github.com/sadiya37790/AudioBookGenerator.git
cd AudioBookGenerator
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

2. Install Tesseract OCR (needed only for image input)

Windows: install from the Tesseract releases page and add it to your PATH
macOS: brew install tesseract
Linux: sudo apt install tesseract-ocr

3. Set your Gemini API key

Get a key from Google AI Studio, then set it as an environment variable:

bash
export GEMINI_API_KEY="your-key-here"       # Windows PowerShell: $env:GEMINI_API_KEY="your-key-here"

Never commit your key to the repository.

4. Run

bash
streamlit run app.py
Tech stack

Python, Streamlit, Google Gemini API, gTTS, deep-translator, pdfplumber, python-docx, pytesseract, Pillow

Known limitations
Internet connection required (Gemini, gTTS and translation all call online services)
DOCX tables are not extracted, only paragraphs
Speech speed control is not yet applied to the audio
Very long documents may hit API limits
Roadmap
Chunking for long documents
Working speech-speed control
More natural voices
Project evolution

Started as a simple offline text-to-speech reader built with pyttsx3 for .txt files. It grew into a Streamlit app that reads PDF, DOCX and images, rewrites text as narration with Gemini, translates it, and generates downloadable MP3 audio.

Author

Shaik Sadiya, LinkedIn
