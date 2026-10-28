import os
import json
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def rewrite_text_for_audio(text, difficulty):
    """
    Ask Gemini to rewrite *text* as audiobook narration and detect its tone.

    The model is instructed to return **only** a JSON object with two fields:
      {
        "narration": "<rewritten text>",
        "tone":      "<happy | sad | serious | motivational | neutral>"
      }

    Parsing is done with json.loads() so the result is always reliable.
    If the response cannot be parsed as JSON (e.g. network error or unexpected
    format), we fall back gracefully: return the raw text with tone="neutral".
    """

    prompt = f"""You are an expert audiobook narrator.

Convert the following text into engaging audiobook narration suitable for a
"{difficulty}" audience.

Rules:
- Respond with ONLY a JSON object – no markdown fences, no extra commentary.
- The JSON must have exactly two keys:
    "narration" : the rewritten text, ready to be read aloud
    "tone"      : one word from this list – happy, sad, serious, motivational, neutral

Text to convert:
{text}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    raw = response.text.strip()

    # Strip optional markdown code fences that some model versions add
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    try:
        data = json.loads(raw)
        enhanced_text = data.get("narration", raw)
        tone          = data.get("tone", "neutral").lower().strip()
    except (json.JSONDecodeError, AttributeError):
        # Fallback: treat entire response as narration text
        enhanced_text = raw
        tone          = "neutral"

    # Normalise tone to one of the expected values
    valid_tones = {"happy", "sad", "serious", "motivational", "neutral"}
    if tone not in valid_tones:
        tone = "neutral"

    return enhanced_text, tone