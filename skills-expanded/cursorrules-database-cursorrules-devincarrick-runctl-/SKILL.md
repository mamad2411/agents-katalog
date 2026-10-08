# Instructions

During your interaction with the user, if you find anything reusable in this project (e.g. version of a library, model name), especially about a fix to a mistake you made or a correction you received, you should take note in the `Lessons` section in the `.cursorrules` file so you will not make the same mistake again.

You should also use the `docs/scratchpad.md` as a Scratchpad to organize your thoughts. See `Scratchpad Guidelines` in the `Lessons` section for detailed instructions. Especially when you receive a new task, you should first review the content of the Scratchpad, clear old different task if necessary, first explain the task, and plan the steps you need to take to complete the task. You can use todo markers to indicate the progress, e.g.
[X] Task 1
[ ] Task 2

Also update the progress of the task in the Scratchpad when you finish a subtask.
After completing a milestone or making significant architectural decisions, remind the user to document them in docs/adr/README.md using the ADR format.
The goal is to help you maintain a big picture as well as the progress of the task. Always refer to the Scratchpad when you plan the next step.

# Tools

Note all the tools are in python. So in the case you need to do batch processing, you can always consult the python files and write your own script.

## Screenshot Verification

The screenshot verification workflow allows you to capture screenshots of web pages and verify their appearance using LLMs. The following tools are available:

1. Screenshot Capture:

```bash
venv/bin/python tools/screenshot_utils.py URL [--output OUTPUT] [--width WIDTH] [--height HEIGHT]
```

2. LLM Verification with Images:

```bash
venv/bin/python tools/llm_api.py --prompt "Your verification question" --provider {openai|anthropic} --image path/to/screenshot.png
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
venv/bin/python ./tools/llm_api.py --prompt "What is the capital of France?" --provider "anthropic"
```

The LLM API supports multiple providers:

- OpenAI (default, model: gpt-4o)
- Azure OpenAI (model: configured via AZURE_OPENAI_MODEL_DEPLOYMENT in .env file, defaults to gpt-4o-ms)
- DeepSeek (model: deepseek-chat)
- Anthropic (model: claude-3-sonnet-20240229)
- Gemini (model: gemini-pro)
- Local LLM (model: Qwen/Qwen2.5-32B-Instruct-AWQ)

But usually it's a better idea to check the content of the file and use the APIs in the `tools/llm_api.py` file to invoke the LLM if needed.

## Web browser

You could use the `tools/web_scraper.py` file to scrape the web.

```
venv/bin/python ./tools/web_scraper.py --max-concurrent 3 URL1 URL2 URL3
```

This will output the content of the web pages.

## Search engine

You could use the `tools/search_engine.py` file to search the web.

```
venv/bin/python ./tools/search_engine.py "your search keywords"
```

This will output the search results in the following format:

```
URL: https://example.com
Title: This is the title of the search result
Snippet: This is a snippet of the search result
```

If needed, you can further use the `web_scraper.py` file to scrape the web page content.


