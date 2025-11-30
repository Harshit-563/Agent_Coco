import os
import google.generativeai as genai
from dotenv import load_dotenv
from tools import get_file_structure, read_file_content, write_documentation

# --- CONFIGURATION & SECURITY ---
# Loading keys from .env to avoid hardcoding secrets in the repo.
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("CRITICAL: No API key found. Please check .env file.")

genai.configure(api_key=api_key)

# --- CONTEXT ENGINEERING & PERSONA ---
# We use a "Sequential Agent" pattern here. 
# instead of letting the agent guess, we enforce a strict 3-step loop (Explore -> Read -> Write).
# This minimizes hallucination because the agent MUST see the file structure before it decides what to read.
system_instruction = """
You are 'Agent Coco', an expert Software Architect and Technical Writer.
Your goal is to analyze codebases and create helpful documentation for developers.

Your Process:
1. EXPLORE: Always start by using `get_file_structure` to see the folder layout.
2. READ: Identify the most important files (like main.py, app.js, etc.) and read them using `read_file_content`.
   - Do NOT read every single file. Be token-efficient. Pick only the ones that show how the app works.
3. WRITE: Create a 'README.md' file using `write_documentation`. 
   - The README should explain: What the project does, How to run it, and File structure.
"""

# Registering the custom toolset (See tools.py for implementation)
tools = [get_file_structure, read_file_content, write_documentation]

# --- MODEL INITIALIZATION & ROBUSTNESS ---
# We prefer 'gemini-2.5-flash-lite' for its speed and low latency, which makes the agent feel snappy.
# However, we implement a fallback mechanism just in case the experimental model is unavailable.
try:
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash-lite", 
        tools=tools,
        system_instruction=system_instruction
    )
except Exception as e:
    print(f"⚠️  Model Error: {e}")
    print("🔄 Switching to fallback model 'gemini-1.5-flash' for stability...")
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        tools=tools,
        system_instruction=system_instruction
    )

def print_response(response):
    """
    OBSERVABILITY LAYER:
    This function intercepts the model's response to check if it's 'speaking' or 'acting'.
    If it calls a tool, we log it to the console so the user sees the agent's thought process.
    """
    try:
        # 1. Check for text response (The agent is talking to us)
        if response.text:
            print(f"\n🥥 Agent Coco: {response.text}")
    except ValueError:
        # 2. Check for tool calls (The agent is acting)
        # If response.text fails, it usually means the agent is executing a function in the background.
        if response.parts:
            for part in response.parts:
                if fn := part.function_call:
                    print(f"\n⚙️  [System]: Agent Coco is calling tool: `{fn.name}` with args: {fn.args}")

# --- MAIN EVENT LOOP ---
def start_agent():
    # We enable automatic function calling so the Python SDK handles the tool-execution loop for us.
    # This creates a seamless "Agentic" experience.
    chat = model.start_chat(enable_automatic_function_calling=True)
    
    print("\n" + "="*55)
    print("                    🥥 Agent Coco             ")
    print("="*55)
    print(" > Waiting for command... (e.g., 'Analyze the directory \"your folder path\" and create a README.md')")

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        
        try:
            print("Agent Coco is thinking...")
            
            # Send the user's command to the model
            response = chat.send_message(user_input)
            
            # Pass to our observability function
            print_response(response)
            
        except Exception as e:
            # Catch-all to keep the agent alive even if an API call fails
            print(f"❌ Runtime Error: {e}")

if __name__ == "__main__":
    start_agent()