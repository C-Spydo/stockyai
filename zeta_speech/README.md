# Financial Advisor Speech Interface

This module adds speech-to-text and text-to-speech capabilities to the financial advisor LLM RAG system.

## Setup

1. Install dependencies:
   ```
   pipenv install
   ```
   
2. Activate the virtual environment:
   ```
   pipenv shell
   ```

## Testing

Run the basic test script:
```
python test_speech.py
```

Run the demo integration:
```
python demo_integration.py
```

## Known Issues

- PyAudio installation may require additional system dependencies
- Speech recognition requires an internet connection for Google's API
- Microphone permissions may need to be granted to your terminal/IDE

## Integration Notes

This module provides a clean interface for speech capabilities that can be integrated with the main RAG system.