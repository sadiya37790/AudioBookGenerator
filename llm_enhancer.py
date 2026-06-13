import os
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def rewrite_text_for_audio(text, difficulty):

    prompt = f"""
    Convert the following text into audiobook narration.

    Difficulty level: {difficulty}

    Also detect tone of the text (happy, sad, serious, motivational).

    Text:
    {text}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    enhanced_text = response.text

    tone = "neutral"

    if "happy" in enhanced_text.lower():
        tone = "happy"
    elif "sad" in enhanced_text.lower():
        tone = "sad"
    elif "motivational" in enhanced_text.lower():
        tone = "motivational"
    elif "serious" in enhanced_text.lower():
        tone = "serious"

    return enhanced_text, tone