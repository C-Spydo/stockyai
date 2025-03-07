import sys
import os
import json
from typing import Dict, Any

# Import your speech interface
from speech_interface import SpeechInterface

# This is a stub for the LLM RAG system - you'll need to integrate with the actual system
class FinancialAdvisorRAG:
    """Mock class to represent the existing RAG system."""
    
    def __init__(self, config_path=None):
        """Initialize with optional configuration."""
        self.config = {}
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                self.config = json.load(f)
    
    def process_query(self, query: str) -> str:
        """
        Process a user query and return a response.
        This is a stub - would actually connect to the RAG system.
        """
        # In a real implementation, this would call the actual RAG system
        # For demo purposes, we just return a mock response
        if "stock" in query.lower():
            return "Based on current market conditions, I recommend diversifying your portfolio with a mix of growth and value stocks."
        elif "budget" in query.lower():
            return "Creating a budget involves tracking your income and expenses. Start by categorizing your spending and setting realistic financial goals."
        elif "invest" in query.lower():
            return "For long-term investments, consider a mix of stocks, bonds, and ETFs based on your risk tolerance and time horizon."
        else:
            return "I'm your financial advisor assistant. You can ask me about investments, budgeting, retirement planning, or other financial topics."


def main():
    """Main function to run the demo."""
    print("Initializing Financial Advisor with Speech Interface...")
    
    # Initialize the speech interface
    speech_interface = SpeechInterface(language="en", timeout=5)
    
    # Initialize the RAG system
    # In a real integration, you would use the actual system's initialization
    config_path = "config.json" if len(sys.argv) > 1 else None
    rag_system = FinancialAdvisorRAG(config_path)
    
    # Define the callback function that will process user input
    def process_user_input(text: str) -> str:
        print(f"Processing: '{text}'")
        response = rag_system.process_query(text)
        print(f"Response: '{response}'")
        return response
    
    # Start the conversation loop
    print("Starting conversation. Say 'exit' or 'quit' to end.")
    speech_interface.conversation_loop(process_user_input)
    
    print("Conversation ended.")


if __name__ == "__main__":
    main()