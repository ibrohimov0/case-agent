import sounddevice as sd
import os
import whisper
import numpy as np
import tempfile
import soundfile as sf

WHISPER_MODEL  = "tiny"       # tiny = fast enough for wake word on CPU
SAMPLE_RATE    = 16000    
CHUNK_SECONDS = 3
WAKE_PHRASES = ["hey computer","hey case"]

BANNER = r"""
  ██████╗ █████╗ ███████╗███████╗
 ██╔════╝██╔══██╗██╔════╝██╔════╝
 ██║     ███████║███████╗█████╗  
 ██║     ██╔══██║╚════██║██╔══╝  
 ╚██████╗██║  ██║███████║███████╗
  ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝
"""
def on_wake():
    """Called when wake phrase is detected."""
    os.system("clear")
    print("\033[36m" + BANNER + "\033[0m")
    print("\033[90m─────────────────────────────────────\033[0m")
    print("\033[1m  Hey. I'm Case. I'm listening.\033[0m")
    print("\033[90m─────────────────────────────────────\033[0m")
    print()
    print("  \033[33m▸\033[0m Say something, or press Ctrl+C to go back.")
    print()
 
 
def record_chunk():
    """Record CHUNK_SECONDS of audio and return as numpy array."""
    audio = sd.rec(
        int(CHUNK_SECONDS * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32",
    )
    sd.wait()
    return audio.flatten()
 
def transcribe(model, audio: np.ndarray) -> str:
    """Save audio to a temp wav file and transcribe with Whisper."""
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        tmp_path = f.name
        sf.write(tmp_path, audio, SAMPLE_RATE)
    try:
        result = model.transcribe(tmp_path, language="en", fp16=False)
        return result["text"].lower().strip()
    finally:
        os.unlink(tmp_path)

def listen():
    print("\033[90m[Case]\033[0m Loading Whisper model...")
    model = whisper.load_model(WHISPER_MODEL)
    print(f"\033[32m[Case]\033[0m Listening for \033[1m\"Hey Case\"\033[0m ...")
    print(f"\033[90m       (checking every {CHUNK_SECONDS}s — Ctrl+C to quit)\033[0m")
    print()
    
    while True:
        audio = record_chunk()
        text = transcribe(model, audio)
        if text:
            print(f"\033[90m  heard: {text}\033[0m")
        if any(phrase in text for phrase in WAKE_PHRASES):
            on_wake()
            print("\033[90m[Case]\033[0m Back to listening...\n")
 
 
if __name__ == "__main__":
    try:
        listen()
    except KeyboardInterrupt:
        print("\n\033[90m[Case]\033[0m Goodbye.\n")
 