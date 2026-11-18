import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import io, time
import requests, urllib.parse

st.set_page_config(page_title="LingoCraft - AI Translator", page_icon="🌍", layout="wide")

# --- SAFE TRANSLATE FUNCTION - 100% WORK AAGUM ---
MYMEMORY_CODE = {
    "auto": "en-GB", "en": "en-GB", "ta": "ta-IN", "hi": "hi-IN",
    "te": "te-IN", "ml": "ml-IN", "kn": "kn-IN", "mr": "mr-IN",
    "bn": "bn-IN", "gu": "gu-IN", "pa": "pa-IN", "ur": "ur-PK",
    "fr": "fr-FR", "es": "es-ES", "de": "de-DE", "it": "it-IT",
    "pt": "pt-PT", "ru": "ru-RU", "ja": "ja-JP", "ko": "ko-KR",
    "zh-CN": "zh-CN", "ar": "ar-SA", "tr": "tr-TR", "nl": "nl-NL",
    "th": "th-TH", "vi": "vi-VN", "id": "id-ID", "sa": "sa-IN",
    "or": "or-IN", "as": "as-IN"
}

def safe_translate(text, src, dest):
    # Auto Detect fix: Tamil letter irundha Tamil, illa na English
    if src == "auto":
        if any('\u0b80' <= c <= '\u0bff' for c in text):
            src = "ta"
        else:
            src = "en"
    if dest == "auto":
        dest = "en"

    # METHOD 1: Google Direct API - Idhu dhan super strong! Enna word kuduthalum varum!
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={src}&tl={dest}&dt=t&q={urllib.parse.quote(text)}"
        r = requests.get(url, timeout=10)
        data = r.json()
        result = "".join([x[0] for x in data[0] if x[0]])
        if result and result.strip() != "":
            return result
    except:
        pass

    # METHOD 2: Backup - MyMemory
    try:
        from deep_translator import MyMemoryTranslator
        s = MYMEMORY_CODE.get(src, "en-GB")
        d = MYMEMORY_CODE.get(dest, "en-GB")
        res2 = MyMemoryTranslator(source=s, target=d).translate(text)
        if res2 and res2.strip() != "":
            return res2
    except:
        pass

    # METHOD 3: Backup 2 - GoogleTranslator library
    try:
        time.sleep(0.5)
        res3 = GoogleTranslator(source=src, target=dest).translate(text)
        if res3 and res3.strip() != "":
            return res3
    except:
        pass

    return None

# --- LANGUAGE MODE: PURE TAMIL / PURE ENGLISH ---
mode = st.sidebar.radio("🌐 Website Language / இணையதள மொழி", ["English", "தமிழ்"])

if mode == "தமிழ்":
    T = {
        "title": "🌍 லிங்கோகிராஃப்ட்",
        "subtitle": "செயற்கை நுண்ணறிவு மொழிபெயர்ப்பாளர்",
        "desc": "அனைவருக்கும் பயனுள்ளது | தமிழ் • ஆங்கிலம் • அனைத்து மொழிகள்",
        "access": "♿ வசதிகள்",
        "font": "எழுத்து அளவு",
        "contrast": "அதிக தெளிவு (கண் பிரச்சனை உள்ளவர்களுக்கு)",
        "voice": "குரலில் கேட்க வேண்டும்",
        "features": "✨ சிறப்புகள்",
        "from": "எந்த மொழியில் இருந்து?",
        "to": "எந்த மொழிக்கு மாற்ற வேண்டும்?",
        "quick": "உடனே முயற்சி செய்யுங்கள்:",
        "type": "✍️ மொழிபெயர்க்க வேண்டிய வார்த்தையை இங்கே எழுதுங்கள்:",
        "btn": "✨ இப்போது மொழிபெயர்க்கவும் ✨",
        "warn": "⚠️ முதலில் ஏதாவது எழுதுங்கள்!",
        "success": "வெற்றிகரமாக மொழிபெயர்க்கப்பட்டது ✅",
        "listen": "🔊 குரலில் கேட்க:",
        "history": "🕑 சமீபத்திய மொழிபெயர்ப்புகள்",
        "footer": "அனைவருக்காக அன்புடன் உருவாக்கப்பட்டது | லிங்கோகிராஃப்ட் © 2026",
        "download": "📥 பதிவிறக்கவும்",
        "translated": "🎯 மொழிபெயர்க்கப்பட்ட வார்த்தை:",
        "chars": "எழுத்துக்கள்",
        "words": "வார்த்தைகள்",
        "wait": "⚠️ கொஞ்சம் காத்திருந்து மீண்டும் முயற்சி செய்யுங்கள்!"
    }
else:
    T = {
        "title": "🌍 LingoCraft",
        "subtitle": "AI Powered Language Translator",
        "desc": "Useful For Everyone | Tamil • English • All Languages",
        "access": "♿ Accessibility",
        "font": "Text Size",
        "contrast": "High Contrast (For Eye Problem)",
        "voice": "Want to Listen in Voice",
        "features": "✨ Features",
        "from": "From Language?",
        "to": "To Language?",
        "quick": "Quick Try:",
        "type": "✍️ Type the text to translate here:",
        "btn": "✨ TRANSLATE NOW ✨",
        "warn": "⚠️ Please type something first!",
        "success": "Translated Successfully ✅",
        "listen": "🔊 Listen in Voice:",
        "history": "🕑 Recent Translations",
        "footer": "Made with ❤️ for Everyone | LingoCraft © 2026",
        "download": "📥 Download",
        "translated": "🎯 Translated Text:",
        "chars": "Characters",
        "words": "Words",
        "wait": "⚠️ Please wait a moment and try again!"
    }

# --- ACCESSIBILITY ---
st.sidebar.title(T["access"])
font_size = st.sidebar.slider(T["font"], 16, 32, 22)
high_contrast = st.sidebar.checkbox(T["contrast"])
voice_on = st.sidebar.checkbox(T["voice"], value=True)

bg_color = "#000000" if high_contrast else "linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%)"
text_color = "#FFFF00" if high_contrast else "white"

st.markdown(f"""
<style>
.stApp {{ background: {bg_color}; }}
.stButton > button {{ background: linear-gradient(90deg, #667eea, #764ba2); color: white; font-weight: 700; border-radius: 15px; padding: 15px 30px; border: none; width: 100%; font-size: 20px; }}
.result-box {{ background: #e0f7ff; padding: 20px; border-radius: 20px; border-left: 6px solid #764ba2; font-size: {font_size}px; font-weight: 600; color: #222; }}
</style>
""", unsafe_allow_html=True)

st.markdown(f"<h1 style='text-align:center; color:{text_color}; font-size:50px;'>{T['title']}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:{text_color}; font-size:20px;'>{T['subtitle']}</p>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:{text_color};'>{T['desc']}</p>", unsafe_allow_html=True)

with st.sidebar:
    st.write("---")
    st.subheader(T["features"])
    if mode == "தமிழ்":
        st.write("✅ 30+ மொழிகள்")
        st.write("✅ தானாகவே கண்டறியும்")
        st.write("✅ பெரிய எழுத்து (கண் பிரச்சனை)")
        st.write("✅ குரல் உச்சரிப்பு")
        st.write("✅ அதிக தெளிவு வசதி")
    else:
        st.write("✅ 30+ Languages")
        st.write("✅ Auto Detect")
        st.write("✅ Large Text (Eye Problem)")
        st.write("✅ Voice Pronunciation")
        st.write("✅ High Contrast Mode")

langs = {
    "Auto Detect": "auto",
    "Tamil - தமிழ்": "ta", "English": "en",
    "Hindi - हिंदी": "hi", "Telugu - తెలుగు": "te", "Malayalam - മലയാളം": "ml",
    "Kannada - ಕನ್ನಡ": "kn", "Marathi - मराठी": "mr", "Bengali - বাংলা": "bn",
    "Gujarati - ગુજરાતી": "gu", "Punjabi - ਪੰਜਾਬੀ": "pa", "Urdu - اردو": "ur",
    "French - Français": "fr", "Spanish - Español": "es", "German - Deutsch": "de",
    "Italian - Italiano": "it", "Portuguese - Português": "pt", "Russian - Русский": "ru",
    "Japanese - 日本語": "ja", "Korean - 한국어": "ko", "Chinese - 中文": "zh-CN",
    "Arabic - العربية": "ar", "Turkish - Türkçe": "tr", "Dutch - Nederlands": "nl",
    "Thai - ไทย": "th", "Vietnamese - Tiếng Việt": "vi", "Indonesian - Bahasa": "id",
    "Sanskrit - संस्कृतम्": "sa", "Odia - ଓଡ଼ିଆ": "or", "Assamese - অসমীয়া": "as"
}

col1, col2 = st.columns(2)
with col1:
    src = st.selectbox(T["from"], list(langs.keys()), index=0)
with col2:
    dest = st.selectbox(T["to"], list(langs.keys()), index=2)

st.write(f"**{T['quick']}**")
e1, e2, e3 = st.columns(3)
if e1.button("👋 Vanakkam / வணக்கம்"):
    st.session_state.txt = "Vanakkam, eppadi irukkinga?" if mode == "English" else "வணக்கம், எப்படி இருக்கிறீர்கள்?"
if e2.button("❤️ I Love You"):
    st.session_state.txt = "I love you" if mode == "English" else "நான் உன்னை நேசிக்கிறேன்"
if e3.button("🙏 Thank You / நன்றி"):
    st.session_state.txt = "Thank you so much" if mode == "English" else "மிக்க நன்றி"

text = st.text_area(T["type"], value=st.session_state.get("txt", ""), height=120)
st.caption(f"{T['chars']}: {len(text)} | {T['words']}: {len(text.split()) if text else 0}")

if "history" not in st.session_state:
    st.session_state.history = []

if st.button(T["btn"]):
    if text.strip() == "":
        st.warning(T["warn"])
    else:
        result_text = safe_translate(text, langs[src], langs[dest])
        if result_text is None:
            st.warning(T["wait"])
        else:
            st.markdown(f"<div class='result-box'>{T['translated']}<br>{result_text}</div>", unsafe_allow_html=True)
            st.success(f"{src} → {dest} | {T['success']}")
            st.session_state.history.insert(0, f"{text} → {result_text}")
            if voice_on:
                try:
                    lang_for_voice = langs[dest] if langs[dest] != 'auto' else 'en'
                    tts = gTTS(text=result_text, lang=lang_for_voice)
                    buf = io.BytesIO()
                    tts.write_to_fp(buf)
                    st.markdown(T["listen"])
                    st.audio(buf.getvalue(), format="audio/mp3")
                except:
                    pass
            st.download_button(T["download"], data=f"Original: {text}\nTranslated: {result_text}", file_name="translation.txt")

if st.session_state.history:
    st.markdown(f"<h3 style='color:{text_color};'>{T['history']}</h3>", unsafe_allow_html=True)
    for h in st.session_state.history[:5]:
        st.markdown(f"<p style='background:white; padding:10px; border-radius:10px;'> {h} </p>", unsafe_allow_html=True)

st.markdown(f"<p style='text-align:center; color:{text_color}; margin-top:30px;'>{T['footer']}</p>", unsafe_allow_html=True)