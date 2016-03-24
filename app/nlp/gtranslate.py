from gtts import gTTS
import goslate

verbose = True

def save_google_voice(phrase, lang, filename):
    tts = gTTS(text=phrase, lang=lang)
    tts.save(filename)

def speak_english(resp, lang, filename):
    gs = goslate.Goslate()

    if(lang!='en'):
        resp = gs.translate(resp,lang)
        save_google_voice(resp, 'en', filename)
    else: save_google_voice(resp, lang, filename)