import gradio as gr
from gtts import gTTS
import tempfile
import os

# --- TTS Function ---
def text_to_speech_gtts(text, language='en'):
    """Generates audio from input text using gTTS and saves it to a temp file."""
    
    if not text:
        return None, "Error: Please enter text."

    try:
        # Create a gTTS object
        tts = gTTS(text=text, lang=language)
        
        # Use a temporary file to save the mp3 output
        # Gradio will read from this path and handle cleanup
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
            audio_path = tmp.name
        
        # Save the audio stream to the temporary file
        tts.save(audio_path)
        
        return audio_path, "Success! Audio generated using gTTS."

    except Exception as e:
        return None, f"An error occurred: {e}"

# --- Gradio Interface ---
iface = gr.Interface(
    fn=text_to_speech_gtts,
    inputs=[
        gr.Textbox(
            lines=5, 
            placeholder="Enter text here...",
            label="Input Text for gTTS"
        ),
        gr.Dropdown(
            choices=['en', 'es', 'fr', 'de'], # Simple selection of popular languages
            label="Select Language (ISO 639-1 code)",
            value='en'
        )
    ],
    outputs=[
        gr.Audio(type="filepath", label="Generated Audio"),
        gr.Text(label="Status")
    ],
    title="gTTS Text-to-Speech Deployment 🗣️",
    description="A simple Text-to-Speech application using the gTTS library."
)

if __name__ == "__main__":
    # Crucial for container deployment!
    iface.launch(server_name='0.0.0.0', server_port=7860)
