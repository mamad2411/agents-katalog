- Make it the most efficient possible
- then .env already contains the HF_TOKEN variable
- implement good error handling and debugging practices
- add clear docstrings and meaningful easy to understand comments.
- a detailled, live, debugging level logging shall be in the run.log, console.log, container.log and only a minimal info level logging with one tqdm progress bar shall be seen in the cli output

- Reproducible environments
  - Dockerfile + docker-compose for consistent runs; CPU/GPU modes toggled.
  - `requirements.txt` + local `.venv` for dev parity.
  - Pinned core libs (Transformers/TRL/PEFT/Torch) for deterministic behavior.
  - execute inside the running container interactively by using docker exec -it <container> bash -lc "<python command>" where `-it` attaches our terminal to the container process’s STDOUT/STDERR, so logs and tracebacks stream directly to our PowerShell window in real time.

- Configuration and 12‑factor principles
  - Central `config.yaml` with all tunables 
  - CLI overrides via Typer and `KEY=VALUE`.
  - .env (`HF_TOKEN`) injected through environment variables.

- Modular, testable codebase
  - `src/` OOP layout.
  - Pytest coverage for orchestration utilities; green tests before running heavy stages.

- Observability and logging
  - Rich logging to console + rotating file logs per run directory.
  - Auto-incremented run folders (`log_vXX_...`) with `latest.txt` pointer.

- Serving and inference
  - container wired with port 1001 and served model name.
  - Healthcheck + simple client for smoke tests.
  - Configurable model mount (UNC path) for portability across machines.

- Portability and infra pragmatics
  - UNC mount handling for shared model storage.
  - GPU-first design with CPU fallback for validation.
  - Clear README with “quick start,” troubleshooting, and next steps (CI/CD, dvc.yaml).