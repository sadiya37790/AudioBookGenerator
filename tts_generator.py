from gtts import gTTS

def generate_audio(text, language, speed):

    audio_file = "audiobook.mp3"

    tts = gTTS(text=text, lang=language)
    tts.save(audio_file)

    return audio_file