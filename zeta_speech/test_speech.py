from speech_interface import SpeechInterface

def main():
    """Simple test for the speech interface."""
    print("Testing Speech Interface")
    
    # Initialize the speech interface
    speech = SpeechInterface()
    
    # Test TTS
    print("Testing text-to-speech...")
    speech.speak("This is a test of the text to speech functionality.", blocking=True)
    
    # Test STT
    print("Testing speech-to-text...")
    print("Please say something when prompted...")
    speech.speak("Please say something now.", blocking=True)
    
    text = speech.listen()
    print(f"Recognized: '{text}'")
    
    if text:
        print("Testing response...")
        speech.speak(f"You said: {text}", blocking=True)
    
    print("Test complete.")

if __name__ == "__main__":
    main()