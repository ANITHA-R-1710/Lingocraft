
import streamlit as st
from deep_translator import GoogleTranslator, MyMemoryTranslator
from gtts import gTTS
import streamlit.components.v1 as components
import io
import requests
import html
import json

from langdetect import detect, DetectorFactory, LangDetectException

DetectorFactory.seed = 0


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="LingoCraft - AI Translator",
    page_icon="🌍",
    layout="wide"
)


# =====================================================
# LANGUAGE CODES
# =====================================================

MYMEMORY_CODE = {
    "en": "en-GB",
    "ta": "ta-IN",
    "hi": "hi-IN",
    "te": "te-IN",
    "ml": "ml-IN",
    "kn": "kn-IN",
    "mr": "mr-IN",
    "bn": "bn-IN",
    "gu": "gu-IN",
    "pa": "pa-IN",
    "ur": "ur-PK",
    "fr": "fr-FR",
    "es": "es-ES",
    "de": "de-DE",
    "it": "it-IT",
    "pt": "pt-PT",
    "ru": "ru-RU",
    "ja": "ja-JP",
    "ko": "ko-KR",
    "zh-CN": "zh-CN",
    "ar": "ar-SA",
    "tr": "tr-TR",
    "nl": "nl-NL",
    "th": "th-TH",
    "vi": "vi-VN",
    "id": "id-ID"
}


VOICE_CODES = {
    "en": "en",
    "ta": "ta",
    "hi": "hi",
    "te": "te",
    "ml": "ml",
    "kn": "kn",
    "fr": "fr",
    "es": "es",
    "de": "de",
    "it": "it",
    "pt": "pt",
    "ru": "ru",
    "ja": "ja",
    "ko": "ko",
    "zh-CN": "zh-CN",
    "ar": "ar",
    "tr": "tr",
    "nl": "nl",
    "th": "th",
    "vi": "vi",
    "id": "id"
}


LANGUAGE_NAMES = {
    "en": "English",
    "ta": "Tamil",
    "hi": "Hindi",
    "te": "Telugu",
    "ml": "Malayalam",
    "kn": "Kannada",
    "mr": "Marathi",
    "bn": "Bengali",
    "gu": "Gujarati",
    "pa": "Punjabi",
    "ur": "Urdu",
    "fr": "French",
    "es": "Spanish",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "ru": "Russian",
    "ja": "Japanese",
    "ko": "Korean",
    "zh-CN": "Chinese",
    "ar": "Arabic",
    "tr": "Turkish",
    "nl": "Dutch",
    "th": "Thai",
    "vi": "Vietnamese",
    "id": "Indonesian",
    "sa": "Sanskrit",
    "or": "Odia",
    "as": "Assamese"
}


# =====================================================
# LANGUAGE CODE NORMALIZATION
# =====================================================

def normalize_language(code):

    if not code:
        return None

    code = code.lower().replace("_", "-")

    aliases = {
        "zh": "zh-CN",
        "zh-cn": "zh-CN",
        "zh-tw": "zh-CN",
        "iw": "he",
        "in": "id"
    }

    return aliases.get(code, code)


# =====================================================
# LANGUAGE DETECTION
# =====================================================

def detect_language(text):

    # METHOD 1: GOOGLE LANGUAGE DETECTION

    try:

        response = requests.get(
            "https://translate.googleapis.com/translate_a/single",
            params={
                "client": "gtx",
                "sl": "auto",
                "tl": "en",
                "dt": "t",
                "q": text
            },
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        if len(data) > 2 and data[2]:

            detected = normalize_language(data[2])

            if detected and detected != "auto":
                return detected

    except Exception:
        pass

    # METHOD 2: LANGDETECT BACKUP

    try:

        detected = normalize_language(detect(text))

        if detected:
            return detected

    except LangDetectException:
        pass

    except Exception:
        pass

    return None


# =====================================================
# GOOGLE TRANSLATION
# =====================================================

def google_translate(text, src, dest):

    params = {
        "client": "gtx",
        "sl": src,
        "tl": dest,
        "dt": "t",
        "q": text
    }

    response = requests.get(
        "https://translate.googleapis.com/translate_a/single",
        params=params,
        timeout=20
    )

    response.raise_for_status()

    data = response.json()

    if not data or not data[0]:
        return None

    translated = "".join(
        item[0]
        for item in data[0]
        if item and item[0]
    )

    return translated.strip() if translated else None


# =====================================================
# SAFE TRANSLATION FUNCTION
# =====================================================

def safe_translate(text, src, dest):

    if not text or not text.strip():
        return None, None

    detected_language = None

    # AUTO DETECTION

    if src == "auto":

        detected_language = detect_language(text)

        if not detected_language:
            return None, None

        actual_source = detected_language

    else:

        actual_source = src
        detected_language = src

    # SAME LANGUAGE: RETURN ORIGINAL TEXT

    if actual_source == dest:

        return text, detected_language

    # METHOD 1: GOOGLE TRANSLATION

    try:

        result = google_translate(
            text,
            actual_source,
            dest
        )

        if result:
            return result, detected_language

    except Exception:
        pass

    # METHOD 2: DEEP-TRANSLATOR GOOGLE BACKUP

    try:

        translator = GoogleTranslator(
            source=actual_source,
            target=dest
        )

        result = translator.translate(text)

        if result and result.strip():
            return result, detected_language

    except Exception:
        pass

    # METHOD 3: MYMEMORY BACKUP

    try:

        source_code = MYMEMORY_CODE.get(actual_source)
        target_code = MYMEMORY_CODE.get(dest)

        if source_code and target_code:

            translator = MyMemoryTranslator(
                source=source_code,
                target=target_code
            )

            result = translator.translate(text)

            if result and result.strip():
                return result, detected_language

    except Exception:
        pass

    return None, detected_language


# =====================================================
# COPY BUTTON
# =====================================================

def copy_button(text):

    safe_text = json.dumps(text)

    components.html(
        f"""
        <button id="copyBtn"
        style="
            background: linear-gradient(90deg,#667eea,#764ba2);
            color:white;
            border:none;
            border-radius:12px;
            padding:12px 25px;
            font-size:16px;
            font-weight:bold;
            cursor:pointer;
            width:100%;
        ">
        📋 Copy Translation
        </button>

        <script>

        const textToCopy = {safe_text};

        const button = document.getElementById("copyBtn");

        button.addEventListener("click", async function() {{

            try {{

                await navigator.clipboard.writeText(textToCopy);

                button.innerText = "✅ Copied Successfully!";

            }} catch (error) {{

                const textarea = document.createElement("textarea");

                textarea.value = textToCopy;

                document.body.appendChild(textarea);

                textarea.select();

                const copied = document.execCommand("copy");

                document.body.removeChild(textarea);

                button.innerText = copied
                    ? "✅ Copied Successfully!"
                    : "⚠️ Please copy manually";

            }}

        }});

        </script>
        """,
        height=60
    )


# =====================================================
# WEBSITE LANGUAGE MODE
# =====================================================

mode = st.sidebar.radio(
    "🌐 Website Language / இணையதள மொழி",
    ["English", "தமிழ்"]
)


if mode == "தமிழ்":

    T = {
        "title": "🌍 லிங்கோகிராஃப்ட்",
        "subtitle": "செயற்கை நுண்ணறிவு மொழிபெயர்ப்பாளர்",
        "desc": "அனைவருக்கும் பயனுள்ளது | தமிழ் • ஆங்கிலம் • அனைத்து மொழிகள்",
        "access": "♿ வசதிகள்",
        "font": "எழுத்து அளவு",
        "contrast": "அதிக தெளிவு",
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
        "wait": "⚠️ மொழிபெயர்ப்பு செய்ய முடியவில்லை. மீண்டும் முயற்சி செய்யுங்கள்!",
        "copy": "மொழிபெயர்ப்பை நகலெடுக்கவும்",
        "same": "ℹ️ தேர்ந்தெடுத்த மொழிகள் ஒன்றே. அசல் உரை கீழே காட்டப்பட்டுள்ளது."
    }

else:

    T = {
        "title": "🌍 LingoCraft",
        "subtitle": "AI Powered Language Translator",
        "desc": "Useful For Everyone | Tamil • English • All Languages",
        "access": "♿ Accessibility",
        "font": "Text Size",
        "contrast": "High Contrast",
        "voice": "Listen in Voice",
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
        "wait": "⚠️ Translation failed. Please try again!",
        "copy": "Copy Translation",
        "same": "ℹ️ Both languages are the same. The original text is displayed below."
    }


# =====================================================
# ACCESSIBILITY SETTINGS
# =====================================================

st.sidebar.title(T["access"])

font_size = st.sidebar.slider(
    T["font"],
    16,
    32,
    22
)

high_contrast = st.sidebar.checkbox(
    T["contrast"]
)

voice_on = st.sidebar.checkbox(
    T["voice"],
    value=True
)


bg_color = (
    "#000000"
    if high_contrast
    else "linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%)"
)

text_color = "#FFFF00" if high_contrast else "white"


# =====================================================
# CSS DESIGN
# =====================================================

st.markdown(f"""

<style>

.stApp {{
    background: {bg_color};
}}

.stButton > button {{

    background: linear-gradient(90deg, #667eea, #764ba2);

    color: white;

    font-weight: 700;

    border-radius: 15px;

    padding: 15px 30px;

    border: none;

    width: 100%;

    font-size: 20px;

}}

.result-box {{

    background: #e0f7ff;

    padding: 20px;

    border-radius: 20px;

    border-left: 6px solid #764ba2;

    font-size: {font_size}px;

    font-weight: 600;

    color: #222;

    overflow-wrap: break-word;

}}

</style>

""", unsafe_allow_html=True)


# =====================================================
# HEADER
# =====================================================

st.markdown(
    f"<h1 style='text-align:center;color:{text_color};font-size:50px;'>{T['title']}</h1>",
    unsafe_allow_html=True
)

st.markdown(
    f"<p style='text-align:center;color:{text_color};font-size:20px;'>{T['subtitle']}</p>",
    unsafe_allow_html=True
)

st.markdown(
    f"<p style='text-align:center;color:{text_color};'>{T['desc']}</p>",
    unsafe_allow_html=True
)


# =====================================================
# SIDEBAR FEATURES
# =====================================================

with st.sidebar:

    st.write("---")

    st.subheader(T["features"])

    if mode == "தமிழ்":

        st.write("✅ 29 மொழிகள் + Auto Detect")
        st.write("✅ தானாகவே மொழி கண்டறிதல்")
        st.write("✅ பெரிய எழுத்து வசதி")
        st.write("✅ குரல் உச்சரிப்பு")
        st.write("✅ அதிக தெளிவு வசதி")

    else:

        st.write("✅ 29 Languages + Auto Detect")
        st.write("✅ Automatic Language Detection")
        st.write("✅ Large Text Accessibility")
        st.write("✅ Voice Pronunciation")
        st.write("✅ High Contrast Mode")


# =====================================================
# LANGUAGE SELECTION
# =====================================================

langs = {

    "Auto Detect": "auto",
    "Tamil - தமிழ்": "ta",
    "English": "en",
    "Hindi - हिंदी": "hi",
    "Telugu - తెలుగు": "te",
    "Malayalam - മലയാളം": "ml",
    "Kannada - ಕನ್ನಡ": "kn",
    "Marathi - मराठी": "mr",
    "Bengali - বাংলা": "bn",
    "Gujarati - ગુજરાતી": "gu",
    "Punjabi - ਪੰਜਾਬੀ": "pa",
    "Urdu - اردو": "ur",
    "French - Français": "fr",
    "Spanish - Español": "es",
    "German - Deutsch": "de",
    "Italian - Italiano": "it",
    "Portuguese - Português": "pt",
    "Russian - Русский": "ru",
    "Japanese - 日本語": "ja",
    "Korean - 한국어": "ko",
    "Chinese - 中文": "zh-CN",
    "Arabic - العربية": "ar",
    "Turkish - Türkçe": "tr",
    "Dutch - Nederlands": "nl",
    "Thai - ไทย": "th",
    "Vietnamese - Tiếng Việt": "vi",
    "Indonesian - Bahasa": "id",
    "Sanskrit - संस्कृतम्": "sa",
    "Odia - ଓଡ଼ିଆ": "or",
    "Assamese - অসমীয়া": "as"

}


# =====================================================
# SOURCE AND TARGET
# =====================================================

col1, col2 = st.columns(2)

with col1:

    src = st.selectbox(
        T["from"],
        list(langs.keys()),
        index=0
    )

with col2:

    target_options = [
        name for name in langs.keys()
        if name != "Auto Detect"
    ]

    dest = st.selectbox(
        T["to"],
        target_options,
        index=1
    )


# =====================================================
# QUICK TRANSLATION BUTTONS
# =====================================================

st.write(f"**{T['quick']}**")

e1, e2, e3 = st.columns(3)


if e1.button("👋 Vanakkam / வணக்கம்"):

    st.session_state.translation_input = (
        "Vanakkam, eppadi irukkinga?"
        if mode == "English"
        else "வணக்கம், எப்படி இருக்கிறீர்கள்?"
    )


if e2.button("❤️ I Love You"):

    st.session_state.translation_input = (
        "I love you"
        if mode == "English"
        else "நான் உன்னை நேசிக்கிறேன்"
    )


if e3.button("🙏 Thank You / நன்றி"):

    st.session_state.translation_input = (
        "Thank you so much"
        if mode == "English"
        else "மிக்க நன்றி"
    )


# =====================================================
# TEXT INPUT
# =====================================================

if "translation_input" not in st.session_state:
    st.session_state.translation_input = ""

text = st.text_area(
    T["type"],
    height=120,
    key="translation_input"
)


st.caption(
    f"{T['chars']}: {len(text)} | "
    f"{T['words']}: {len(text.split()) if text else 0}"
)


# =====================================================
# TRANSLATION HISTORY
# =====================================================

if "history" not in st.session_state:
    st.session_state.history = []


# =====================================================
# TRANSLATE BUTTON
# =====================================================

if st.button(T["btn"]):

    if not text.strip():

        st.warning(T["warn"])

    else:

        source_code = langs[src]
        target_code = langs[dest]

        with st.spinner("Translating..."):

            result_text, detected_language = safe_translate(
                text,
                source_code,
                target_code
            )

        if result_text is None:

            st.warning(T["wait"])

        else:

            st.session_state.result_text = result_text
            st.session_state.original_text = text
            st.session_state.detected_language = detected_language
            st.session_state.target_language = target_code

            st.session_state.same_language = (
                detected_language == target_code
            )

            if source_code == "auto":
                source_name = LANGUAGE_NAMES.get(
                    detected_language,
                    detected_language
                )
            else:
                source_name = LANGUAGE_NAMES.get(
                    source_code,
                    source_code
                )

            target_name = LANGUAGE_NAMES.get(
                target_code,
                target_code
            )

            st.session_state.source_name = source_name
            st.session_state.target_name = target_name

            history_item = f"{text} → {result_text}"

            st.session_state.history.insert(
                0,
                history_item
            )

            st.session_state.history = (
                st.session_state.history[:10]
            )


# =====================================================
# DISPLAY TRANSLATION RESULT
# =====================================================

if "result_text" in st.session_state:

    result_text = st.session_state.result_text

    safe_result = html.escape(result_text)

    st.markdown(
        f"""
        <div class='result-box'>
        {T['translated']}
        <br><br>
        {safe_result}
        </div>
        """,
        unsafe_allow_html=True
    )

    source_name = st.session_state.source_name
    target_name = st.session_state.target_name

    if st.session_state.same_language:

        st.info(T["same"])

    else:

        st.success(
            f"{source_name} → {target_name} | {T['success']}"
        )

    # ONE-CLICK COPY BUTTON

    copy_button(result_text)

    # =================================================
    # TEXT TO SPEECH
    # =================================================

    if voice_on:

        target = st.session_state.target_language

        if target in VOICE_CODES:

            try:

                tts = gTTS(
                    text=result_text,
                    lang=VOICE_CODES[target]
                )

                audio_buffer = io.BytesIO()

                tts.write_to_fp(audio_buffer)

                st.markdown(T["listen"])

                st.audio(
                    audio_buffer.getvalue(),
                    format="audio/mp3"
                )

            except Exception:

                st.info(
                    "Voice pronunciation is temporarily unavailable."
                )

        else:

            st.info(
                "Voice pronunciation is not available for this language."
            )

    # =================================================
    # DOWNLOAD TRANSLATION
    # =================================================

    download_content = (
        f"Original Text:\n"
        f"{st.session_state.original_text}\n\n"
        f"Translated Text:\n"
        f"{result_text}"
    )

    st.download_button(
        label=T["download"],
        data=download_content,
        file_name="LingoCraft_Translation.txt",
        mime="text/plain"
    )


# =====================================================
# HISTORY DISPLAY
# =====================================================

if st.session_state.history:

    st.markdown(
        f"<h3 style='color:{text_color};'>{T['history']}</h3>",
        unsafe_allow_html=True
    )

    for item in st.session_state.history[:5]:

        safe_item = html.escape(item)

        st.markdown(
            f"""
            <p style='background:white;padding:10px;border-radius:10px;color:#222;'>
            {safe_item}
            </p>
            """,
            unsafe_allow_html=True
        )


# =====================================================
# FOOTER
# =====================================================

st.markdown(
    f"""
    <p style='text-align:center;color:{text_color};margin-top:30px;'>
    {T['footer']}
    </p>
    """,
    unsafe_allow_html=True
)
