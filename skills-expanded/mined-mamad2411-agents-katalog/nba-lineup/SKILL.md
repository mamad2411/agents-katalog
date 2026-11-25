# Instructions

During your interaction with the user, if you find anything reusable in this project (e.g. version of a library, model name), especially about a fix to a mistake you made or a correction you received, you should take note in the `Lessons` section in the `.cursorrules` file so you will not make the same mistake again. 

You should also use the `.cursorrules` file as a Scratchpad to organize your thoughts. Especially when you receive a new task, you should first review the content of the Scratchpad, clear old different task if necessary, first explain the task, and plan the steps you need to take to complete the task. You can use todo markers to indicate the progress, e.g.
[X] Task 1
[ ] Task 2

Also update the progress of the task in the Scratchpad when you finish a subtask.
Especially when you finished a milestone, it will help to improve your depth of task accomplishment to use the Scratchpad to reflect and plan.
The goal is to help you maintain a big picture as well as the progress of the task. Always refer to the Scratchpad when you plan the next step.

# Tools

Note all the tools are in python3. So in the case you need to do batch processing, you can always consult the python files and write your own script.

## Screenshot Verification

The screenshot verification workflow allows you to capture screenshots of web pages and verify their appearance using LLMs. The following tools are available:

1. Screenshot Capture:
```bash
venv/bin/python3 tools/screenshot_utils.py URL [--output OUTPUT] [--width WIDTH] [--height HEIGHT]
```

2. LLM Verification with Images:
```bash
venv/bin/python3 tools/llm_api.py --prompt "Your verification question" --provider {openai|anthropic} --image path/to/screenshot.png
```

Example workflow:
```python
from screenshot_utils import take_screenshot_sync
from llm_api import query_llm

# Take a screenshot

screenshot_path = take_screenshot_sync('https://example.com', 'screenshot.png')

# Verify with LLM

response = query_llm(
    "What is the background color and title of this webpage?",
    provider="openai",  # or "anthropic"
    image_path=screenshot_path
)
print(response)
```

## LLM

You always have an LLM at your side to help you with the task. For simple tasks, you could invoke the LLM by running the following command:
```
venv/bin/python3 ./tools/llm_api.py --prompt "What is the capital of France?" --provider "anthropic"
```

The LLM API supports multiple providers:
- OpenAI (default, model: gpt-4o)
- Azure OpenAI (model: configured via AZURE_OPENAI_MODEL_DEPLOYMENT in .env file, defaults to gpt-4o-ms)
- DeepSeek (model: deepseek-chat)
- Anthropic (model: claude-3-sonnet-20240229)
- Gemini (model: gemini-pro)
- Ollama (local, default model: mistral, configurable via OLLAMA_MODEL in .env)
- LM Studio (local, model configured in LM Studio UI, accessed via REST API)

For local LLM providers:
- Ollama: Ensure Ollama is running locally (http://localhost:11434)
- LM Studio: Start LM Studio and enable the local server (http://localhost:1234)

But usually it's a better idea to check the content of the file and use the APIs in the `tools/llm_api.py` file to invoke the LLM if needed.

## Web browser

You could use the `tools/web_scraper.py` file to scrape the web.
```bash
venv/bin/python3 ./tools/web_scraper.py --max-concurrent 3 URL1 URL2 URL3
```
This will output the content of the web pages.

## Search engine

You could use the `tools/search_engine.py` file to search the web.
```bash
venv/bin/python3 ./tools/search_engine.py "your search keywords"
```
This will output the search results in the following format:
```
URL: https://example.com
Title: This is the title of the search result
Snippet: This is a snippet of the search result
```
If needed, you can further use the `web_scraper.py` file to scrape the web page content.

# Lessons

## User Specified Lessons

- You have a python3 venv in ./venv. Use it.
- Include info useful for debugging in the program output.
- Read the file before you try to edit it.
- Due to Cursor's limit, when you use `git` and `gh` and need to submit a multiline commit message, first write the message in a file, and then use `git commit -F <filename>` or similar command to commit. And then remove the file. Include "[Cursor] " in the commit message and PR title.

## Cursor learned

- For search results, ensure proper handling of different character encodings (UTF-8) for international queries
- Add debug information to stderr while keeping the main output clean in stdout for better pipeline integration
- When using seaborn styles in matplotlib, use 'seaborn-v0_8' instead of 'seaborn' as the style name due to recent seaborn version changes
- Use 'gpt-4o' as the model name for OpenAI's GPT-4 with vision capabilities
- When searching for recent news, use the current year (2025) instead of previous years, or simply use the "recent" keyword to get the latest information
- When using VS Code with NixOS on WSL, explicitly set the git.path in settings.json to help VS Code source control find the git executable
- For VS Code to detect git repositories in NixOS-WSL, create a flake.nix with a devshell that includes git and use `nix develop` in the terminal profiles
- For NBA lineup prediction, use scikit-learn, pandas, and numpy as core libraries with proper model evaluation techniques
- In NixOS/WSL environments, use nix-shell with specific Python packages instead of pip/venv for consistent package management. When running Python scripts, use `nix-shell -p "python3.withPackages(ps: with ps; [package1 package2])" --run "python script.py"` to ensure all dependencies are available.

# Scratchpad

## Current Task: NBA Lineup Prediction Project

Task: Develop a machine learning model to predict the optimal fifth player for a home team in NBA games.

Plan:
[X] Explore dataset structure to understand available data
[X] Create project structure and organize code
[X] Develop data processing modules
[X] Create feature engineering and model components
[X] Implement visualization tools
[X] Create main script to tie everything together
[X] Create Jupyter notebook for data exploration
[X] Set up run script for model training and evaluation
[X] Fix environment issues to run the model
[ ] Run model on small sample to verify functionality
[ ] Fine-tune model parameters
[ ] Run model on full dataset
[ ] Analyze results

Current Issues:
1. Nix environment setup issues:
   - File path resolution error in temporary directory
   - NumPy import error due to source directory conflict
   - Virtual environment activation issues

Next Steps:
1. Fix the Nix environment setup:
   - Update the flake.nix to properly handle file paths
   - Fix the virtual environment setup
   - Resolve NumPy import issues
2. Test the model with a small dataset
3. Fine-tune model parameters if needed
4. Run the full dataset analysis

Progress:
- We've identified the core issues with the Nix environment setup
- We need to modify the flake.nix to properly handle file paths and dependencies
- We'll need to ensure proper virtual environment setup and package installation
