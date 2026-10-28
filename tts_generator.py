import os
import uuid
import tempfile
from gtts import gTTS

def generate_audio(text, language, speed):
    """
    Generate an MP3 audiobook from *text* at the requested *speed*.

    gTTS only supports two speeds (normal and slow).  The UI slider goes from
    0.5 to 2.0 with 1.0 as the default:
      - speed < 1.0  → gTTS slow=True  (approximately 0.75×)
      - speed >= 1.0 → gTTS slow=False (normal speed)

    If pydub + ffmpeg are available the audio is also time-stretched to the
    exact slider value; otherwise the gTTS two-speed approximation is used and
    a console warning is printed.

    Each call writes to a *unique* temporary file so parallel Streamlit sessions
    never overwrite each other's output.
    """

    # --- unique output path so multiple runs don't collide ---
    tmp_dir  = tempfile.gettempdir()
    filename = f"audiobook_{uuid.uuid4().hex}.mp3"
    audio_file = os.path.join(tmp_dir, filename)

    # --- gTTS two-speed approximation ---
    slow = speed < 1.0
    tts  = gTTS(text=text, lang=language, slow=slow)
    tts.save(audio_file)

    # --- optional pydub fine-grained speed change ---
    if speed != 1.0:
        try:
            from pydub import AudioSegment

            audio    = AudioSegment.from_mp3(audio_file)
            # atempo filter: change playback rate without pitch shift
            # pydub exposes ffmpeg via export; use the ffmpeg-python or
            # subprocess approach for atempo.
            import subprocess, shutil

            ffmpeg_bin = shutil.which("ffmpeg")
            if ffmpeg_bin:
                stretched_file = os.path.join(tmp_dir, f"audiobook_{uuid.uuid4().hex}_stretched.mp3")
                # ffmpeg atempo accepts 0.5–2.0; chain filters for values outside that range
                atempo = max(0.5, min(2.0, speed))
                subprocess.run(
                    [
                        ffmpeg_bin, "-y", "-i", audio_file,
                        "-filter:a", f"atempo={atempo}",
                        stretched_file,
                    ],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                os.replace(stretched_file, audio_file)
        except Exception as exc:
            # pydub / ffmpeg not installed – fall back to gTTS two-speed
            print(f"[tts_generator] Fine-grained speed adjustment unavailable ({exc}). "
                  "Using gTTS slow/normal approximation.")

    return audio_file