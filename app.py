import streamlit as st
from extraction import extract_text
from llm_enhancer import rewrite_text_for_audio
from translator import translate_text
from tts_generator import generate_audio


st.set_page_config(page_title="AI Audiobook Generator", page_icon="🎧", layout="wide")


st.markdown("""
<style>

.main {
background: linear-gradient(120deg,#f6f9fc,#eef2ff);
}

.title {
font-size:45px;
font-weight:700;
text-align:center;
background: -webkit-linear-gradient(#4f46e5,#9333ea);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
}

.card {
padding:25px;
border-radius:12px;
background:white;
box-shadow:0px 8px 25px rgba(0,0,0,0.08);
margin-bottom:20px;
}

.stButton>button{
background: linear-gradient(90deg,#6366f1,#9333ea);
color:white;
border:none;
border-radius:8px;
padding:10px 22px;
font-weight:bold;
}

.stButton>button:hover{
background: linear-gradient(90deg,#4f46e5,#7e22ce);
}

</style>
""", unsafe_allow_html=True)


st.markdown('<p class="title">🎧 AI Audiobook Generator</p>', unsafe_allow_html=True)
st.write("Turn your documents into immersive AI audiobooks")


# session states
if "extracted_text" not in st.session_state:
    st.session_state.extracted_text = ""

if "enhanced_text" not in st.session_state:
    st.session_state.enhanced_text = ""

if "tone" not in st.session_state:
    st.session_state.tone = ""

if "audio_file" not in st.session_state:
    st.session_state.audio_file = ""


# upload
st.markdown('<div class="card">', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload your file",
    type=["pdf","docx","txt","png","jpg","jpeg"]
)

st.markdown('</div>', unsafe_allow_html=True)


if uploaded_file:

    if st.button("Extract Text"):

        with st.spinner("Extracting text..."):
            text = extract_text(uploaded_file)

        st.session_state.extracted_text = text
        st.session_state.enhanced_text = ""
        st.session_state.audio_file = ""



# extracted text
if st.session_state.extracted_text:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("📄 Extracted Text")

    with st.expander("Preview"):
        st.write(st.session_state.extracted_text)

    word_count = len(st.session_state.extracted_text.split())
    listen_time = max(1, round(word_count / 150))

    col1,col2 = st.columns(2)

    with col1:
        st.metric("Word Count",word_count)

    with col2:
        st.metric("Listening Time",f"{listen_time} min")

    difficulty = st.selectbox(
        "Difficulty Level",
        ["easy","medium","hard"]
    )

    if st.button("Enhance with AI"):

        with st.spinner("Enhancing text..."):

            enhanced_text, tone = rewrite_text_for_audio(
                st.session_state.extracted_text,
                difficulty
            )

        st.session_state.enhanced_text = enhanced_text
        st.session_state.tone = tone

    st.markdown('</div>', unsafe_allow_html=True)



# enhanced text
if st.session_state.enhanced_text:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("✨ AI Enhanced Text")

    with st.expander("Preview Enhanced Text"):
        st.write(st.session_state.enhanced_text)

    st.info(f"🎭 Narration Tone Detected: {st.session_state.tone}")

    language_name = st.selectbox(
        "Select Language",
        ["English","Hindi","Telugu","French","Spanish"]
    )

    language_map = {
        "English":"en",
        "Hindi":"hi",
        "Telugu":"te",
        "French":"fr",
        "Spanish":"es"
    }

    language = language_map[language_name]

    speed = st.slider(
        "Playback Speed",
        0.5,
        2.0,
        1.0
    )

    if st.button("Generate Audiobook"):

        with st.spinner("Generating audiobook..."):

            translated_text = translate_text(
                st.session_state.enhanced_text,
                language
            )

            audio_file = generate_audio(
                translated_text,
                language,
                speed
            )

        st.session_state.audio_file = audio_file

    st.markdown('</div>', unsafe_allow_html=True)



# audio output
if st.session_state.audio_file:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("🎧 Audiobook")

    st.audio(st.session_state.audio_file)

    with open(st.session_state.audio_file,"rb") as f:

        st.download_button(
            "Download Audiobook",
            f,
            file_name="audiobook.mp3"
        )

    st.markdown('</div>', unsafe_allow_html=True)



st.markdown("---")
st.markdown(
"""
<center>
AI Audiobook Generator • Built with Streamlit
</center>
""",
unsafe_allow_html=True
)