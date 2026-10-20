# TailorTex

Tailors a LaTeX resume to a job description and compiles it to PDF via `pdflatex`. Supports two modes: a Chrome side-panel extension backed by a FastAPI server (recommended), and a legacy CLI. The backend uses a Strategy + Registry provider pattern so Gemini and Claude Code run as interchangeable generation methods with separate job queues.

## Commands

```bash
# Backend
cd backend && uvicorn api.server:app --port 8001 --reload

# Tests
cd backend && pytest

# CLI (legacy, Gemini only)
cd local && python main.py --name TargetCompany

# CLI via Claude Code slash command
claude -p "/tailor-resume TargetCompany"

# Compile a .tex file locally (resume or cover letter)
python local/compile.py --tex path/to/file.tex --prefix Google
python local/compile.py --tex output/Google_CoverLetter.tex --prefix Google --type cover_letter
```

## Directory Structure

```
TailorTex/
├── CLAUDE.md                          # this file
├── README.md                          # human-facing setup guide
├── Makefile                           # shorthand commands (make serve-api, make dev, etc.)
├── requirements.txt                   # Python dependencies
├── job_description.txt                # JD read by CLI and slash commands
│
├── backend/
│   ├── api/
│   │   ├── server.py                  # FastAPI app — all endpoints, job queue, worker threads
│   │   └── schemas.py                 # Pydantic request/response models
│   └── core/
│       ├── prompt_pipeline.py         # preamble split, prompt file loading, LaTeX post-processing
│       ├── compiler.py                # find_pdflatex() + compile_latex() — used by all providers
│       ├── tex_parser.py              # parse .tex → structured dict; format_resume_for_eval()
│       ├── profile.py                 # personal config: MY_NAME, MY_EMAIL, MY_PHONE, LOCATION_ADDRESS_MAP (gitignored)
│       └── profile.py.template        # committed placeholder — copy → profile.py and fill in
│       └── providers/
│           ├── __init__.py            # registry: get_provider(id), registered_provider_ids()
│           ├── base.py                # ResumeProvider ABC, GenerationRequest, GenerationResult
│           ├── registry.py            # ModelConfig dataclass + GEMINI_MODEL_CHAIN list
│           ├── gemini.py              # GeminiProvider — waterfall fallback across model chain
│           └── claude_cli.py          # ClaudeCliProvider — subprocess via claude -p /tailor-resume
│
├── backend/tests/
│   ├── conftest.py                    # shared fixtures: TestClient, mock_api_calls auto-mock
│   ├── test_server.py                 # all API endpoints + edge cases
│   ├── test_providers.py              # 31 tests — GeminiProvider, ClaudeCliProvider, registry
│   ├── test_compiler.py               # 7 tests  — find_pdflatex(), compile_latex()
│   ├── test_tex_parser.py             # 35 tests  — parse_resume_tex, clean_latex, format_resume_for_eval
│   └── test_prompt_pipeline.py        # 32 tests  — build_prompts, postprocess_latex, validate_latex
│
├── frontend/
│   ├── extension/
│   │   ├── manifest.json              # Chrome MV3 manifest
│   │   ├── background.js              # opens side panel on toolbar click
│   │   ├── popup.html                 # side panel markup
│   │   ├── popup.js                   # all extension logic: queue, SSE, output browser, retry
│   │   └── popup.css                  # dark theme styles
│   └── src/                           # React/Vite frontend (make serve-ui) — separate from extension
│
├── local/
│   ├── main.py                        # CLI entry point (Gemini, argparse)
│   ├── compile.py                     # standalone script: compile a .tex file to PDF (--type resume|cover_letter)
│   └── backup.py                      # copy output/ to BACKUP_LOCATION with date-stamped names
│
├── prompts/
│   ├── system_prompt.txt              # core AI generation rules (optimizer may edit this)
│   ├── user_constraints.txt           # per-run hard rules (never modified by optimizer)
│   ├── additional_projects.txt        # project bank the AI can swap in
│   ├── experience_bank.txt            # experience bank the AI can draw from (optional, opt-in)
│   ├── evaluator_prompt.txt           # scoring rubric for /judge-resume
│   ├── optimizer_prompt.txt           # decision rules for /optimize-prompt
│   ├── prompt_summary.txt             # compressed rule reference for the evaluator
│   ├── daily_feedback.json            # evaluation results; cleared by /optimize-prompt
│   └── change_tracker.json            # scoring ledger and rule history
│
├── cover_letters/                     # cover letter LaTeX templates (cover_letter.tex is the default)
├── resumes/                           # source .tex files; all files listed by /resumes endpoint
├── output/                            # generated .tex/.pdf (gitignored)
│   ├── extras/                        # plain-text eval files written by ClaudeCliProvider
│   └── job_details/                   # generation inputs stored per company for Retry
├── examples/                          # sample resume template and prompt files to copy from
│
└── docs/
    ├── DESIGN.md                      # architecture, data models, decisions, alternatives
    ├── tasks/TASKS.md                 # task checklist — updated after each sub-task
    └── features/                      # one LLD file per feature (implementation + tests)
        ├── job-queue-and-api.md
        ├── provider-system.md
        ├── prompt-pipeline.md
        ├── latex-compiler.md
        ├── tex-parser.md
        ├── chrome-extension.md
        ├── slash-commands.md
        ├── feedback-loop.md
        ├── experience-bank.md
        ├── retry-on-error.md
        ├── recompile-improvements.md
        └── cl-generation-no-timeout.md
```

## Where to Look for a Task

Each feature file in `docs/features/` covers implementation details and the full test table for one area:

| Feature file | Use it when working on |
|---|---|
| `job-queue-and-api.md` | Any API endpoint, job lifecycle, queue/worker architecture, SSE streaming, company fallback path |
| `provider-system.md` | Adding or changing an AI provider, the provider registry, `GenerationRequest`/`GenerationResult`, Gemini model chain |
| `prompt-pipeline.md` | Prompt assembly (`build_prompts`), preamble splitting, LaTeX post-processing (`postprocess_latex`, `validate_latex`) |
| `latex-compiler.md` | `pdflatex` binary discovery, `compile_latex()`, aux file cleanup, the `/recompile` mtime check |
| `tex-parser.md` | Parsing `.tex` → structured data (`parse_resume_tex`), LaTeX stripping (`clean_latex`), plain-text eval output (`format_resume_for_eval`) |
| `chrome-extension.md` | Extension UI, job card rendering, SSE wiring, output browser, `chrome.storage.local` job state |
| `slash-commands.md` | `/tailor-resume`, `/judge-resume`, `/optimize-prompt` — how each command reads and writes files |
| `feedback-loop.md` | End-to-end flow: generation → evaluation → prompt optimization; `daily_feedback.json` lifecycle |
| `experience-bank.md` | `experience_bank.txt` opt-in flag, `use_experience` in `build_prompts`, `/generate` endpoint, CLI `--experience` flag |
| `retry-on-error.md` | Retry on Error — `GET /job_details/{company}` endpoint, `output/job_details/` file lifecycle, Retry button in extension |
| `cover-letter.md` | Cover letter generation — `_generate_cover_letter()`, new endpoints, extension UI, `profile.py` config |
| `recompile-improvements.md` | Recompile type selection — `type` query param on `POST /recompile`, `#recompile-type-modal`, `openRecompileModal()` JS helper |
| `cl-generation-no-timeout.md` | CL no-timeout polling — `cover_letter_error` flag in `JobStatus`, `_cl_thread()` wrapper, `while (true)` poll loop in `submitGenerateCl` |

## Environment Variables

- `GEMINI_API_KEY` — Google Gemini API key
- `BACKUP_LOCATION` — absolute path to backup folder for `local/backup.py`
- `PDFLATEX_PATH` — (optional) explicit path to `pdflatex` binary

## Key Conventions

- **New providers**: implement `ResumeProvider` ABC; register in `backend/core/providers/__init__.py` — no changes to `server.py`
- **New Google models**: append `ModelConfig` to `GEMINI_MODEL_CHAIN` in `registry.py`
- **Output filenames**: `output/{NAME}_Resume.tex` / `.pdf`
- **`job_id='_'` sentinel**: extension uses this for archived resumes; server falls back to reconstructing paths from `?company=X` query param
- **`conftest.py` auto-mock**: patches `build_prompts`, `get_provider`, and `os.startfile` for all server tests; `compile_latex` is NOT patched there — recompile tests mock it directly on `core.compiler.compile_latex`
- **Feature docs**: `docs/features/<name>.md` describes implementation and lists every test; keep in sync when adding tests

## API Endpoints (quick ref)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/resumes` | List `.tex` files in `resumes/` |
| GET | `/locations` | List supported locations |
| GET | `/cover_letters` | List `.tex` templates in `cover_letters/` |
| GET | `/output/resumes` | List archived resumes in `output/` (both `.tex` + `.pdf` present) |
| GET | `/job_details/{company}` | Stored generation inputs for a company (used by Retry button) |
| POST | `/generate` | Submit a generation job → `{"job_id": "..."}` |
| GET | `/queue` | All in-memory jobs |
| GET | `/status/{job_id}` | SSE stream of log lines + completion event |
| GET | `/status/{job_id}/json` | Snapshot status |
| GET | `/open/{job_id}?company=X` | Open resume PDF with system viewer |
| GET | `/open_cl/{job_id}?company=X` | Open cover letter PDF with system viewer |
| GET | `/download/{job_id}` | Serve PDF as download |
| GET | `/details/{job_id}?company=X` | Parsed experience + projects from `.tex` |
| POST | `/recompile/{job_id}?company=X&type=resume\|cover_letter` | Recompile `.tex` → PDF; `type` defaults to `resume` |
| POST | `/generate_cl/{job_id}?company=X` | Standalone cover letter generation (reads `job_details/`) |
| DELETE | `/files/{job_id}?company=X` | Delete `.tex`, `.pdf`, cover letter files, extras, and `job_details` |
