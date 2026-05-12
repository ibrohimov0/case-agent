import sounddevice as sd
import queue
import json
import subprocess
import sys
import os
from vosk import Model, KaldiRecognizer

MODEL_PATH = "./vosk-model-small-en-us-0.15"
SAMPLE_RATE = 16000
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
    # Clear screen and show Case UI in the SAME terminal
    os.system("clear")
    print("\033[36m" + BANNER + "\033[0m")
    print("\033[90m─────────────────────────────────────\033[0m")
    print("\033[1m  Hey. I'm Case. I'm listening.\033[0m")
    print("\033[90m─────────────────────────────────────\033[0m")
    print()
    print("  \033[33m▸\033[0m Say something, or press Ctrl+C to go back.")
    print()
 
 
def check_model():
    if not os.path.exists(MODEL_PATH):
        print(f"\033[31m[ERROR]\033[0m Model not found at: {MODEL_PATH}")
        print()
        print("Download a model first:")
        print("  wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip")
        print("  unzip vosk-model-small-en-us-0.15.zip")
        print()
        sys.exit(1)
 
 
def listen():
    check_model()
 
    print("\033[90m[Case]\033[0m Loading model...")
    model = Model(MODEL_PATH)
    rec = KaldiRecognizer(model, SAMPLE_RATE)
    audio_queue = queue.Queue()
 
    def audio_callback(indata, frames, time, status):
        if status:
            print(f"\033[33m[warn]\033[0m {status}")
        audio_queue.put(bytes(indata))
 
    print("\033[32m[Case]\033[0m Listening for \033[1m\"Hey Case\"\033[0m ...")
    print("\033[90m       (Ctrl+C to quit)\033[0m")
    print()
 
    with sd.RawInputStream(
        samplerate=SAMPLE_RATE,
        blocksize=8000,
        dtype="int16",
        channels=1,
        callback=audio_callback,
    ):
        while True:
            data = audio_queue.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "").lower()
 
                if text:
                    print(f"\033[90m  heard: {text}\033[0m")
 
                if any(phrase in text for phrase in WAKE_PHRASES):
                    on_wake()
 
                    # After greeting, return to listening state
                    print("\033[90m[Case]\033[0m Back to listening...\n")
 
 
if __name__ == "__main__":
    try:
        listen()
    except KeyboardInterrupt:
        print("\n\033[90m[Case]\033[0m Goodbye.\n")
 