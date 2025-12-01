import os

# DAY 2 CONCEPT: AGENT TOOLS
# These functions define the "Action Space" for the agent.
# By exposing these to the LLM, we transform it from a chatbot into an agent
# capable of interacting with the local operating system.
# # Debug note: Changed 'root_path' -> 'path'. 
# Gemini kept throwing MALFORMED_FUNCTION_CALL errors because it guessed 'path' by default.
def get_file_structure(path: str = ".") -> str:
    """
    Scans the given folder path and returns a string representation of the file tree.
    Use this to understand the project structure.
    
    Args:
        path: The directory to scan (use "." for current directory).
    """
    tree_str = ""
    start_path = path
    
    # Skip hidden files and venv to keep the context window small. 
    # We don't need to read git internals or library files.
    IGNORE_PATTERNS = {'.git', '__pycache__', 'node_modules', '.DS_Store', 'venv', '.idea', '.env', '.vscode'}

    try:
        for root, dirs, files in os.walk(start_path):
            dirs[:] = [d for d in dirs if d not in IGNORE_PATTERNS]
            
            level = root.replace(start_path, '').count(os.sep)
            indent = ' ' * 4 * (level)
            tree_str += f"{indent}{os.path.basename(root)}/\n"
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                if f not in IGNORE_PATTERNS and not f.endswith('.pyc'):
                    tree_str += f"{subindent}{f}\n"
        
        if not tree_str:
            return "Directory is empty or path is invalid."
        return tree_str
    except Exception as e:
        return f"Error scanning directory: {str(e)}"

def read_file_content(path: str) -> str:
    """
    Reads the text content of a specific code file.
    
    Args:
        path: The relative path to the file (e.g., 'src/main.py').
    """
    try:
        # Security guardrail: Stop the agent from accidentally reading my .env file or secrets.
        if ".env" in path or "password" in path.lower():
            return "SECURITY ALERT: Access to sensitive configuration files is restricted."

        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
            # Adding line numbers helps the agent reference specific lines in the docs later.
            numbered_content = "\n".join([f"{i+1}: {line}" for i, line in enumerate(lines)])
            return f"--- START OF FILE: {path} ---\n{numbered_content}\n--- END OF FILE ---"
    except Exception as e:
        return f"Error reading file {path}: {str(e)}"

def write_documentation(filename: str, content: str) -> str:
    """
    Writes text to a file. Use this to save the README.md.
    
    Args:
        filename: The output filename (e.g. 'README.md').
        content: The full markdown text to save.
    """
    try:
        # Fix: ensure the folder exists before writing, otherwise it crashes on nested paths like 'docs/README.md'.
        if os.path.dirname(filename):
            os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote documentation to {filename}"
    except Exception as e:
        return f"Failed to write file: {str(e)}"