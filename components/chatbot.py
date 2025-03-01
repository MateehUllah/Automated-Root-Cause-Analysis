import os
import streamlit as st
import requests
import tempfile
import soundfile as sf
from utils.text_to_speech import text_to_speech
from streamlit_mic_recorder import mic_recorder
from pydub import AudioSegment
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import torch
import librosa


HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
HF_CHATBOT_API = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
HF_WHISPER_API = "https://api-inference.huggingface.co/models/openai/whisper-small"


processor = WhisperProcessor.from_pretrained("openai/whisper-small")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-small")


def transcribe_audio_local(audio_path):
    """
    Transcribe an audio file locally.

    Parameters
    ----------
    audio_path : str
        Path to the audio file to be transcribed.

    Returns
    -------
    str
        The transcribed text or an error message if the transcription fails.
    """
    if not os.path.exists(audio_path) or os.path.getsize(audio_path) == 0:
        return "Error: Audio file is empty or not saved properly."

    try:
        audio_data, samplerate = librosa.load(audio_path, sr=16000) 
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
            resampled_path = temp_wav.name

        inputs = processor(audio_data, sampling_rate=samplerate, return_tensors="pt")
        input_features = inputs.input_features
    except Exception as e:
        return f"Error: Unable to process audio file. {str(e)}"

    try:
        predicted_ids = model.generate(input_features)
        transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
        return transcription[0]
    except Exception as e:
        return f"Error: Unable to transcribe audio. {str(e)}"

def generate_network_response(user_text):
    """
    Generates a response to a user's question related to networking and IT infrastructure.

    Args:
        user_text (str): The user's question or query.

    Returns:
        str: A concise and clear answer to the user's question.
    """
    system_prompt = """
    You are an AI chatbot specialized in networking and IT infrastructure.
    You can answer questions about:
    - Network troubleshooting
    - Packet loss, latency, and bandwidth issues
    - Modems, routers, switches, and firewalls
    - VPNs, DDoS attacks, and network security
    - Cloud networking and data centers
    - IP addressing, DNS, and connectivity problems
    
    If the question is not related to networking, politely respond with:
    "I'm here to help with networking topics. Please ask about network-related issues."
    
    Answer concisely and clearly. It should be properly formatted. Do not repeat the user’s question. Avoid starting responses with "User: ...".
    """

    full_prompt = system_prompt + f"\nQuestion: {user_text}\n\nResponse:"
    
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}
    payload = {"inputs": full_prompt, "parameters": {"max_new_tokens": 500, "temperature": 0.7}}

    response = requests.post(HF_CHATBOT_API, headers=headers, json=payload)

    if response.status_code == 200:
        generated_text = response.json()[0]['generated_text']
        return generated_text.replace(system_prompt, "").strip() 
    else:
        return "Error: Unable to generate response from API."

def display_chatbot():
    """
    Displays a Streamlit app for AI Network Chatbot (NetBot) with text-to-text and voice-to-text modes.

    Text-to-Text Mode:
    - User types a question or query related to networking and IT infrastructure.
    - NetBot responds with a concise and clear answer.

    Voice-to-Text Mode:
    - User records a voice message or uploads a voice file (WAV/MP3).
    - NetBot transcribes the audio and responds with a concise and clear answer.
    - The AI response is also converted to speech using a text-to-speech API and played back.

    NetBot is powered by the Mistral-7B-Instruct-v0.2 model from Hugging Face.
    """
    st.subheader("NetBot: Your AI Network Chatbot")

    chat_mode = st.radio("Select Mode:", ["Text-to-Text", "Voice-to-Text"], horizontal=True)

    if chat_mode == "Text-to-Text":
        user_text = st.text_input("Ask about networking:")

        if st.button("Send Query"):
            response_text = generate_network_response(user_text)
            st.write(response_text)

    elif chat_mode == "Voice-to-Text":
        st.write("Use the microphone.")

        audio_bytes = mic_recorder(start_prompt="🎙️ Click to Record", stop_prompt="🛑 Stop Recording", key="mic")

        temp_path = None

        if audio_bytes:
            if isinstance(audio_bytes, dict) and "bytes" in audio_bytes:
                audio_bytes = audio_bytes["bytes"]

            temp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
            with open(temp_path, "wb") as f:
                f.write(audio_bytes)
        if temp_path:
            transcription = transcribe_audio_local(temp_path)

            if "Error" in transcription:
                st.error(transcription)
            else:
                st.write("Transcribed Text:", transcription)

                response_text = generate_network_response(transcription)
                st.write(response_text)