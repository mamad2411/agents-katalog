---
description: This rule should be used when creating a Dockerfile for a Python
  service that relies on uv (uvicorn) for dependency management and runtime,
  with a customizable entry point/command. It’s ideal for applications where
  the default CMD in the template (e.g., FastAPI) doesn’t match the service’s
  requirements, allowing dynamic adaptation to frameworks or custom execution logic.
alwaysApply: false
---
Parameters:
- CMD_COMMAND: Command to run the service (e.g., ["fastapi", "dev", "src/main.py"], ["myapp", "run"])

Template:
```Dockerfile
# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim
# Install the project into `/app`
WORKDIR /app
# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1
# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy
# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
--mount=type=bind,source=uv.lock,target=uv.lock \
--mount=type=bind,source=pyproject.toml,target=pyproject.toml \
uv sync --locked --no-install-project --no-dev
# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
uv sync --locked --no-dev
# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"
# Reset the entrypoint, don't invoke `uv`
ENTRYPOINT []
# Run the service by default
CMD {{ CMD_COMMAND }}
```
