import gradio as gr
from transformers import VitsModel, AutoTokenizer
import torch
import soundfile as sf
import os
import tempfile # <--- New import!

# --- Model Loading ---
MODEL_ID = "facebook/mms-tts-eng"
device = "cuda" if torch.cuda.is_available() else "cpu"

try:
    model = VitsModel.from_pretrained(MODEL_ID).to(device)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
except Exception as e:
    print(f"Error loading model: {e}")
    model, tokenizer = None, None

# --- TTS Function ---
def text_to_speech(text):
    """Generates audio from input text using the loaded model."""
    if model is None or tokenizer is None:
        return None, "Error: Model failed to load."

    # 1. Tokenize the input text
    inputs = tokenizer(text, return_tensors="pt").to(device)

    # 2. Generate the audio
    with torch.no_grad():
        output = model(**inputs)

    audio_data = output.waveform.cpu().numpy().squeeze()
    sampling_rate = model.config.sampling_rate

    # 3. Save the audio to a unique temporary file <--- THE KEY CHANGE
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        audio_path = tmp.name
    
    sf.write(audio_path, audio_data, sampling_rate)

    # Gradio will read the audio from this path and handle the cleanup!
    return audio_path, "Success! Audio generated."

# --- Gradio Interface ---
iface = gr.Interface(
    fn=text_to_speech,
    inputs=gr.Textbox(
        lines=5,
        placeholder="Enter text here...",
        label="Input Text for TTS"
    ),
    outputs=[
        gr.Audio(type="filepath", label="Generated Audio"),
        gr.Text(label="Status")
    ],
    title="Hugging Face TTS Deployment Example 🗣️",
    description=f"A simple Text-to-Speech application using the **{MODEL_ID}** model."
)

if __name__ == "__main__":
    # Ensure this launch line is still present for container deployment!
    iface.launch(server_name='0.0.0.0', server_port=7860)
