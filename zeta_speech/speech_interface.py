import speech_recognition as sr
from gtts import gTTS
import os
import tempfile
import pygame
import time
import logging
from threading import Thread
from typing import Optional, Callable

class SpeechInterface:
    """Speech interface module that handles STT and TTS functionality."""
    
    def __init__(self, language="en", timeout=5):
        """
        Initialize the speech interface.
        
        Args:
            language: The language code (default: 'en' for English)
            timeout: Timeout for speech recognition in seconds
        """
        self.recognizer = sr.Recognizer()
        self.language = language
        self.timeout = timeout
        self.logger = self._setup_logger()
        
        # Initialize pygame for audio playback
        pygame.mixer.init()
        
    def _setup_logger(self):
        """Set up logger for the speech interface."""
        logger = logging.getLogger('SpeechInterface')
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger
    
    def listen(self, callback: Optional[Callable] = None) -> str:
        """
        Listen for speech input and convert it to text.
        
        Args:
            callback: Optional callback function to call with the transcribed text
            
        Returns:
            Transcribed text
        """
        text = ""
        
        with sr.Microphone() as source:
            self.logger.info("Adjusting for ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            self.logger.info("Listening...")
            
            try:
                audio = self.recognizer.listen(source, timeout=self.timeout)
                self.logger.info("Processing speech...")
                text = self.recognizer.recognize_google(audio, language=self.language)
                self.logger.info(f"Transcribed: {text}")
                
                if callback:
                    callback(text)
                
            except sr.WaitTimeoutError:
                self.logger.warning("No speech detected within timeout period")
            except sr.UnknownValueError:
                self.logger.warning("Could not understand audio")
            except sr.RequestError as e:
                self.logger.error(f"Could not request results; {e}")
            except Exception as e:
                self.logger.error(f"Error during speech recognition: {e}")
                
        return text
    
    def speak(self, text: str, blocking: bool = False) -> None:
        """
        Convert text to speech and play it.
        
        Args:
            text: Text to convert to speech
            blocking: Whether to block until audio playback is complete
        """
        if not text:
            self.logger.warning("Empty text provided for TTS")
            return
            
        def _speak_thread():
            try:
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
                temp_filename = temp_file.name
                temp_file.close()
                
                tts = gTTS(text=text, lang=self.language, slow=False)
                tts.save(temp_filename)
                
                pygame.mixer.music.load(temp_filename)
                pygame.mixer.music.play()
                
                # Wait for playback to finish if blocking is True
                if blocking:
                    while pygame.mixer.music.get_busy():
                        pygame.time.Clock().tick(10)
                
                # Clean up the temp file after a delay to ensure it's not deleted during playback
                time.sleep(0.5)  # Short delay to ensure playback has started
                try:
                    os.unlink(temp_filename)
                except Exception as e:
                    self.logger.warning(f"Failed to delete temporary file: {e}")
                    
            except Exception as e:
                self.logger.error(f"Error during text-to-speech: {e}")
        
        if blocking:
            _speak_thread()
        else:
            Thread(target=_speak_thread).start()
            
    def conversation_loop(self, process_input_func: Callable[[str], str]) -> None:
        """
        Run a continuous conversation loop.
        
        Args:
            process_input_func: Function that takes user input text and returns response text
        """
        self.speak("Hello! I'm your financial advisor. How can I help you today?", blocking=True)
        
        while True:
            user_input = self.listen()
            
            if not user_input:
                self.speak("I didn't catch that. Could you please try again?")
                continue
                
            if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
                self.speak("Thank you for using our financial advisory service. Goodbye!")
                break
                
            response = process_input_func(user_input)
            self.speak(response)