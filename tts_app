import streamlit as st
from gtts import gTTS
from io import BytesIO
import re

# --- 1. Text Normalization Function (NLP Component) ---

def normalize_text(text):
    """
    Performs basic text normalization to improve TTS pronunciation.
    - Expands common abbreviations.
    - Handles currency symbols.
    """
    # Simple abbreviation dictionary
    abbreviations = {
        "Mr.": "Mister",
        "Dr.": "Doctor",
        "Vs.": "Versus",
        "Mrs.": "Missus",
        "e.g.": "for example",
    }
    
    # 1. Expand abbreviations
    for abbr, full in abbreviations.items():
        text = text.replace(abbr, full)

    # 2. Handle currency (simple replacement for $ to dollars)
    text = re.sub(r'\$(\d+)', r'\1 dollars', text)
    
    # You can add more rules here (e.g., handling dates, percentages)
    return text

# --- 2. Core TTS Function ---

def text_to_audio(text, lang='en'):
    """
    Converts text to an MP3 audio stream using gTTS.
    """
    # Create an in-memory byte stream to store the MP3 data
    mp3_fp = BytesIO() 
    
    try:
        # Create the gTTS object
        tts = gTTS(text=text, lang=lang, slow=False)
        
        # Write the audio data to the byte stream
        tts.write_to_fp(mp3_fp)
        
        # Reset stream position to the beginning before returning
        mp3_fp.seek(0)
        return mp3_fp
    
    except Exception as e:
        st.error(f"An error occurred during speech generation: {e}")
        return None

# --- 3. Streamlit UI (The Web Application) ---

st.set_page_config(page_title="Custom TTS Reader", layout="centered")

st.title("🎙️ Custom Text-to-Speech Generator")
st.markdown("Enter text below, select a language, and generate the audio. The text is processed for better pronunciation!")

# Input Text Area
input_text = st.text_area(
    "Enter the text you want to convert to speech:", 
    "Dr. Smith said the new phone costs $850. The battery life is great, Vs. the old model."
)

# Language Selector
lang_options = {
    "English (en)": "en",
    "Spanish (es)": "es",
    "French (fr)": "fr",
    "Hindi (hi)": "hi",
}
selected_lang_name = st.selectbox("Select Language:", list(lang_options.keys()))
selected_lang_code = lang_options[selected_lang_name]

# Generate Button
if st.button("Generate Speech 🔊"):
    if input_text:
        with st.spinner("Generating audio..."):
            
            # 1. NLP Step: Normalize the text
            processed_text = normalize_text(input_text)
            st.info(f"**Processed Text (Normalization Applied):** {processed_text}")

            # 2. TTS Step: Convert to audio
            audio_stream = text_to_audio(processed_text, selected_lang_code)

            if audio_stream:
                # 3. Streamlit Step: Display the audio player
                st.audio(audio_stream, format='audio/mp3')

                # 4. Streamlit Step: Provide a download button
                st.download_button(
                    label="Download MP3",
                    data=audio_stream,
                    file_name="generated_speech.mp3",
                    mime="audio/mp3"
                )
    else:
        st.warning("Please enter some text to generate speech.")

st.markdown("---")
st.caption("Project demonstrating NLP (Normalization) and Sequence-to-Sequence (gTTS API) capabilities.")
