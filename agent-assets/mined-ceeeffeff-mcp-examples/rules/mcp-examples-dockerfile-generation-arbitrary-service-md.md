---
description: This plan generates a Dockerfile for a Python service by leveraging
  package management files(e.g., pyproject.toml, uv.lock), identifying entry points
  (e.g., main.py), and incorporating documentation (e.g.,README.md).
  It uses a multi-stage build to install dependencies efficiently, ensures the service
  runs as intended, and handles edge cases like missing lockfiles or custom entry points
  Use this plan when the service directory contains Python source files, package
  management files, and documentation, and when the goal is to containerize the
  service with minimal assumptions about its structure.
alwaysApply: false
---
# Dockerfile Generation Plan for Arbitrary Service Directory

## 1. **Identify Key Files in the Service Directory**
   - **Package Management Files**:  
     Look for files like `pyproject.toml`, `uv.lock`, `requirements.txt`, or `Pipfile`. These define dependencies.  
     *If none found*, check for a `setup.py` or `package.json` (for Node.js, though this is Python-focused).  
     **Note**: Use the `Memory` tool to recall common package file patterns if unsure.

   - **Entry Point**:  
     Locate the main Python file (e.g., `main.py`, `app.py`, or `service.py`).  
     If in a subdirectory, note the path (e.g., `src/main.py`).  
     *Check documentation files* (see step 2) for clues about the entry point.

   - **Documentation Files**:  
     Search for `.md` files like `README.md`, `STARTUP.md`, or `DEPLOY.md`. These often contain build instructions or entry point details.

   - **Ignored Files/Directories**:  
     Exclude:  
     - `.venv/`, `node_modules/`, `package-lock.json`, `*.lock`  
     - Other build artifacts (e.g., `dist/`, `build/`)  
     *Use the `Memory` tool to store these patterns for future reference.*

---

## 2. **Structure the Dockerfile Using the Template**
   - **Base Image**:  
     Use a Python image with `uv` pre-installed (e.g., `ghcr.io/astral-sh/uv:python3.x-bookworm-slim`).  
     *Adjust the Python version to match `.python-version` if present.*

   - **Multi-Stage Build for Dependencies**:  
     ```Dockerfile
     # Builder stage: Install dependencies
     FROM ghcr.io/astral-sh/uv:python3.x-bookworm-slim as builder
     WORKDIR /app
     COPY uv.lock pyproject.toml ./
     RUN --mount=type=cache,target=/root/.cache/uv \
         uv sync --locked --no-install-project --no-dev
     ```

   - **Copy Source Code and Install**:  
     ```Dockerfile
     # App stage: Copy source and install
     FROM ghcr.io/astral-sh/uv:python3.x-bookworm-slim
     WORKDIR /app
     COPY . /app
     RUN --mount=type=cache,target=/root/.cache/uv \
         uv sync --locked --no-dev
     ```

   - **Set Entry Point and CMD**:  
     - Use the identified entry point (e.g., `python /app/main.py`).  
     - If the service uses a framework (e.g., FastAPI), set `CMD` accordingly (e.g., `uv run main:app`).  
     - *Refer to documentation files* for specific commands.

---

## 3. **Handle Edge Cases**
   - **No `uv.lock` or `pyproject.toml`**:  
     If dependencies are managed via `requirements.txt`, modify the `RUN` command:  
     ```Dockerfile
     RUN pip install -r requirements.txt
     ```
     *Use the `taskmaster-ai` tool to break this into smaller steps if needed.*

   - **Custom Entry Point**:  
     If the service uses a non-standard entry point (e.g., a script or CLI tool), consult the `README.md` or `STARTUP.md` for instructions.

   - **Documentation-Driven Setup**:  
     If documentation files detail the build process, prioritize their guidance over assumptions.

---

## 4. **Validate and Test**
   - **Build the Dockerfile**:  
     Run `docker build -t service-name .` to ensure it builds without errors.  
   - **Test the Service**:  
     Run `docker run service-name` to verify it executes the service as expected.  
   - **Check for Ignored Files**:  
     Ensure excluded directories (e.g., `.venv/`) are not copied into the image.

---

## 5. **Store Knowledge for Future Use**
   - **Update Memory**:  
     Use the `Memory` tool to store patterns for:  
     - Common package files (e.g., `requirements.txt`, `Pipfile`)  
     - Standard entry points (e.g., `main.py`, `app.py`)  
     - Ignored file patterns for future projects.  
   - **Document the Plan**:  
     Save this plan in a `rules/` directory as a reusable template for similar projects.

---

## 6. **When to Ask for Help**
   - If the service uses an unknown package manager (e.g., `poetry`, `pipenv`).  
   - If documentation files are ambiguous or missing critical info.  
   - If the entry point is unclear (e.g., multiple `main.py` files exist).  
   - Use the `taskmaster-ai` tool to split complex tasks into smaller, manageable steps.  
