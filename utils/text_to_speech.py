import os
import requests
import tempfile

HF_TTS_API = "https://api-inference.huggingface.co/models/facebook/wav2vec2-large-960h"

def text_to_speech(text):
    """
    Converts input text to speech using a Hugging Face API and saves the output as a WAV file.

    Args:
        text (str): The input text to be converted to speech.

    Returns:
        str or None: The file path to the generated WAV file if successful, otherwise None.
    """

    headers = {"Authorization": f"Bearer {os.getenv('HUGGINGFACEHUB_API_TOKEN')}"}
    payload = {"inputs": text}

    response = requests.post(HF_TTS_API, headers=headers, json=payload)

    if response.status_code == 200:
        tts_output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
        with open(tts_output_path, "wb") as f:
            f.write(response.content)
        return tts_output_path
    else:
        return None
