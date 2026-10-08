# Repository Guidelines

## Project Structure & Module Organization
- `zephyr_bot.py`: main loop orchestrating vision → comment → post.
- `vision_summarizer.py`: calls local Qwen‑VL bridge (`/v1/chat/completions`).
- `llm_providers.py`, `llm_router.py`: provider/model routing (Gemini, Mistral, Ollama).
- `commentary_engine.py`, `anti_flood.py`: comment generation and rate limiting.
- `twitch_client.py`, `youtube_client.py`: platform stubs/clients.
- `qwen_vl_server.py`: FastAPI bridge for local VLM.
- `screenshots/`: input frames consumed by the bot (keep fresh).
- `tests/`: pytest tests; config via `.env`.

## Build, Test, and Development Commands
- Create venv: `python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt`.
- Run bot: `./start-zephyr.sh foreground` or `python zephyr_bot.py`.
- Start Qwen‑VL server: `uvicorn qwen_vl_server:app --host 0.0.0.0 --port 8010`.
- Healthcheck (env, screenshots, connectivity): `python healthcheck.py`.
- Self‑test chain (LLM + sample vision/comment): `python selftest.py`.
- Vision probe: `python vision_summarizer.py`.
- Run tests: `pytest -q`.

## Coding Style & Naming Conventions
- Python 3.10+, PEP 8, 4‑space indentation; keep imports minimal.
- Names: files/modules `snake_case.py`; classes `PascalCase`; funcs/vars `snake_case`.
- Logging: use `logging` with repo format; avoid `print` outside CLI tools.
- Formatting/linting (if installed): `black` and `ruff`.

## Testing Guidelines
- Framework: pytest. Place tests in `tests/` as `test_*.py`.
- Focus on routing, rate limiting, and summarization. No strict coverage target; aim for meaningful coverage.
- Run locally with `pytest -q`. Quick checks: `python selftest.py`, `python healthcheck.py`.

## Commit & Pull Request Guidelines
- Commits: imperative, concise subject (≤72 chars), focused scope.
  - Example: `feat(vision): add base64 image option`.
- PRs include: summary, motivation, risk/rollback, linked issue, config/env changes (update `.env.example`), and runtime evidence (bot output, healthcheck logs) plus local run steps.

## Security & Configuration Tips
- Never commit secrets. Use `.env`; document keys in `.env.example`.
- Key env vars: `AI_ORDER`, `AI_MODE`, provider keys, `SCREENSHOT_FILE`, `QWEN_BASE`, `QWEN_VISION_MODEL`.
- Validate before running: `python healthcheck.py`. Keep `screenshots/` fresh.

