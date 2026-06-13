from deep_translator import GoogleTranslator

def translate_text(text, language):

    if language == "en":
        return text

    translated = GoogleTranslator(source='auto', target=language).translate(text)

    return translated