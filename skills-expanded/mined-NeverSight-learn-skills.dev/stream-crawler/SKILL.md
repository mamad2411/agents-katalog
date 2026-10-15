---
name: stream-crawler
description: Use Playwright to capture URLs that are easily missed by normal fetching, such as infinite scroll, lazy loading, virtual lists, and SPA listings. Use this when you want to save URL content and page-streaming is insufficient.
---

This skill is designed to execute dynamic page fetching following a set procedure. When a target URL is received, first check the execution environment, perform setup if necessary, and then run the existing script. After fetching, check the generated files in the specified output directory (e.g., `<output_directory>`), and concisely report to the user how much was captured, and what happened if there were failures or missing data.

## When to Use

- When capturing dynamic pages is necessary
- When you want to save the contents of list pages or SPAs

## Execution Environment

**Note:** All paths and operations described in this document assume that your current working directory is the skill directory (the directory containing this `SKILL.md` file), denoted as `<skill_directory>`.

For the first time, prepare Python and Playwright.

```bash
cd <skill_directory>
python3 --version
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

Afterwards, activate the virtual environment to execute.

```bash
cd <skill_directory>
source .venv/bin/activate
```

## Execution Procedure

Normal fetch:

```bash
python scripts/stream_crawler.py \
  --url "https://example.com/list" \
  --session-dir "<output_directory>/example"
```

Outputs to check:

- `<output_directory>/example/curl.html`
- `<output_directory>/example/page_type.json`
- `<output_directory>/example/pages/page_000N.json`
- `<output_directory>/example/logs/crawler.log`


## How to Read the Outputs

### `page_type.json`

- Concisely summarizes the page type determination of the target URL.
- Look here first when you want a rough overview of the entire page.
- Refer to [`references/json-format.md`](references/json-format.md) for detailed JSON items.

### `curl.html`

- Initial HTML fetched with `curl`.
- Use this when you want to check how much content was included before JavaScript execution.

### `page_000N.json`

- Summary information of each snapshot.
- Use this to get a rough overview of the whole process, track at what point content increased, and find the next file to look at.
- Refer to [`references/json-format.md`](references/json-format.md) for detailed JSON items.

### `page_000N.html`

- The HTML of the main content at that time.
- Use this when you want to extract information using XPath or CSS selectors based on the HTML structure.

### `page_000N.txt`

- The full text of the body at that time.
- Use this for text search, keyword checking, or when you want to quickly read through the entire text.

### `crawler.log`

- Logs of the scrolls executed and termination reasons.
- Use this when you want to check where growth occurred, where it stopped, or the reason for a fetch failure.


## Rules

- Prioritize using the script.
- Do not supplement content that could not be fetched.
- Report errors as failures.
- Guide to related documents if an explanation of the implementation specifications is needed.

## References

- [`README.md`](README.md)
- [`docs/spec.md`](docs/spec.md)
- [`references/json-format.md`](references/json-format.md)
