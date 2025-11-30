
# Agent Coco: Codebase Documentation Generator

This project utilizes a Google Generative AI model to act as 'Agent Coco', an expert Software Architect and Technical Writer. Agent Coco's primary function is to analyze codebases and generate comprehensive documentation, specifically a `README.md` file.

## Features

*   **Automated Documentation:** Generates `README.md` files based on codebase analysis.
*   **Structured Agentic Process:** Follows a strict `EXPLORE -> READ -> WRITE` loop to minimize errors and hallucinations.
*   **Codebase Exploration:** Uses `get_file_structure` to understand the project layout.
*   **Selective File Reading:** Employs `read_file_content` to inspect relevant files, with security measures to prevent access to sensitive information (like `.env` files).
*   **Error Handling & Fallbacks:** Includes fallbacks for the AI model and robust error handling for file operations.
*   **Observability:** Logs agent actions (tool calls) to the console for transparency.

## How to Run

1.  **Clone the repository:**
    ```bash
    git clone [repository-url]
    cd [repository-name]
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Set up API Key:**
    Create a `.env` file in the root directory and add your Google API Key:
    ```
    GOOGLE_API_KEY=your_api_key_here
    ```
4.  **Run the agent:**
    ```bash
    python main.py
    ```
5.  **Interact with Agent Coco:**
    Follow the prompts in your terminal. For example, you can ask it to analyze the current directory and create a `README.md`.

## File Structure

```
./
    .gitignore
    main.py
    README.md
    requirements.txt
    tools.py
```

*   `.gitignore`: Specifies intentionally untracked files that Git should ignore.
*   `main.py`: The main script that initializes the AI agent, configures the API, and runs the interaction loop.
*   `requirements.txt`: Lists the Python dependencies required to run the project.
*   `tools.py`: Contains the Python functions that Agent Coco can call to interact with the file system (get file structure, read files, write documentation).

## Agentic Workflow

Agent Coco operates using a sequential agent pattern enforced by its system instructions:

1.  **EXPLORE:** The agent first uses `get_file_structure` to map out the project directory.
2.  **READ:** Based on the file structure, it intelligently selects key files (like `main.py`, `tools.py`) using `read_file_content` to understand their purpose and content.
3.  **WRITE:** Finally, it synthesizes the gathered information to generate the `README.md` using `write_documentation`.

This structured approach ensures that the agent has a clear understanding of the codebase before generating documentation, leading to more accurate and relevant output.
