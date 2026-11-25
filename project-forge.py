#!/usr/bin/env python3
"""project-forge — scaffold project LENGKAP + skill otomatis + gate verifikasi.

Tujuan: AI tidak perlu ditegur soal struktur. Sekali `new`, semua yang profesional
sudah ada (CI, test, lint, ADR, security, checklist, diagram) DAN skill proyek yang
hemat token (progressive disclosure) sudah ditulis untuk AI berikutnya.

  project-forge new <dir> --name "X" --desc "..." --type web|api|cli|lib|data
                          [--stack ts|py] [--install] [--git]
  project-forge new <dir> --framework fastapi|django|next|gin|axum|...
                          # delegasi CLI resmi: 94 framework + 38 server/infra/security
                          # (nginx, compose, k8s, helm, terraform, postgres, harden-ssh...)
  project-forge adopt <dir> [--name X]   # proyek yang sudah ada: deteksi stack/framework + skill/TODO/AGENTS
  project-forge verify <dir> [--json]      # gate: struktur, lint, types, test, build, security
  project-forge status <dir>               # 3 baris: gate mana yang belum, perintah berikutnya
  project-forge skill <dir>                # tulis ulang skill proyek (hemat token)
  project-forge diagram <dir>              # mermaid workflow
  project-forge gates <dir>                # daftar gate + status
  project-forge stacks                     # 33 stack bahasa
  project-forge frameworks [kata]          # 94 framework/library + 38 server/infra/security
                                           # contoh: --framework nginx|compose|k8s|helm|terraform|
                                           #         postgres|prometheus|harden-ssh|gitleaks-config

Prinsip:
- 0 token saat idle: ini CLI, bukan MCP.
- Skill proyek <= 40 baris; detail ditaruh di TODO.md/README/ADR (dibaca hanya bila perlu).
- `verify` = satu-satunya sumber kebenaran "selesai".
"""
import json
import os
import re
import shutil
import subprocess
import sys
import time
import tempfile

HOME = os.path.expanduser("~")
AG = os.path.join(HOME, ".agents")
sys.path.insert(0, AG)
import project_stacks as PS  # noqa: E402  (definisi stack semua bahasa)
import framework_catalog as FC  # noqa: E402  (katalog framework/library)
import server_catalog as SC  # noqa: E402  (server, container, k8s, iac, data, observability, security)
YEAR = time.strftime("%Y")

# 6 kombinasi punya template detail (teruji end-to-end); sisanya lewat mesin generik
DETAILED = {("web", "ts"), ("api", "py"), ("api", "ts"), ("cli", "py"), ("lib", "ts"),
            ("data", "py")}
_BY_TYPE = PS.stacks_by_type()
TYPES = set(_BY_TYPE) | {"web", "api", "cli", "lib", "data"}
STACKS = {t: sorted(set(v) | {"ts"} if t == "web" else set(v) | {"py"} if t == "data" else set(v))
          for t, v in _BY_TYPE.items()}
for _t in ("web", "api", "cli", "lib", "data"):
    STACKS.setdefault(_t, [])
STACKS["web"] = sorted(set(STACKS["web"]) | {"ts"})
STACKS["api"] = sorted(set(STACKS["api"]) | {"py", "ts"})
STACKS["cli"] = sorted(set(STACKS["cli"]) | {"py"})
STACKS["lib"] = sorted(set(STACKS["lib"]) | {"ts"})
STACKS["data"] = sorted(set(STACKS["data"]) | {"py"})

MERMAID = """```mermaid
flowchart TD
    A[bootstrap: struktur + docs] --> B[setup: deps + .env]
    B --> C[fitur / kode]
    C --> D[test unit + e2e]
    D --> E[lint + typecheck]
    E --> F[build]
    F --> G[security scan]
    G --> H[CI hijau + verify exit 0]
    H --> I[rilis / deploy]
```"""


# ── util ────────────────────────────────────────────────────────────────────
def w(path, content, mode=None):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    if mode:
        os.chmod(path, mode)


def sub(text, **kw):
    for k, v in kw.items():
        text = text.replace(f"__{k.upper()}__", str(v))
    return text


def sh(cmd, cwd=None, timeout=1800):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                          timeout=timeout, shell=isinstance(cmd, str))


def slugify(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") or "project"


def is_py_dir(d):
    return os.path.exists(os.path.join(d, "pyproject.toml"))


# ── template: berkas umum ──────────────────────────────────────────────────
README = """# __NAME__

__DESC__

## Quickstart
```bash
make setup     # pasang dependency
make dev       # jalankan saat mengembangkan
make verify    # gate lengkap (wajib sebelum bilang "selesai")
```

## Struktur
```
__NAME__/
__TREE__
```

## Perintah
| Perintah | Fungsi |
|---|---|
| `make setup` | pasang dependency |
| `make dev` | mode pengembangan |
| `make test` | unit test |
| `make lint` | lint + format check |
| `make build` | build produksi |
| `make verify` | semua gate (struktur→security) |

## Alur kerja
Lihat `TODO.md` (checklist + diagram) dan `docs/adr/` untuk keputusan arsitektur.
Aturan untuk AI/agent ada di `AGENTS.md` dan `.opencode/skills/__SLUG__/SKILL.md`.

## Lisensi
MIT — lihat `LICENSE`.
"""

AGENTS = """# AGENTS.md — __NAME__

Baca ini dulu, jangan menebak struktur.

1. Status kerja: `project-forge status .` (3 baris, 0 token besar).
2. Checklist manusia: `TODO.md` — kerjakan dari fase teratas yang belum dicentang.
3. Sebelum bilang selesai: `project-forge verify .` **harus exit 0**.
4. Skill proyek (ringkas): `.opencode/skills/__SLUG__/SKILL.md`.
5. Keputusan arsitektur: `docs/adr/`. Jangan ubah struktur tanpa ADR baru.

Konvensi: commit kecil, pesan `feat|fix|chore|docs: ...`, jangan commit `.env`.
"""

TODO = """# TODO — __NAME__

__MERMAID__

## Fase 1 — Fondasi
- [ ] `make setup` sukses tanpa error
- [ ] `.env` dibuat dari `.env.example` (jangan commit)
- [ ] `git init` + commit pertama
- [ ] `CHANGELOG.md` diisi entri awal
- [ ] `SECURITY.md` diisi kontak pelaporan

## Fase 2 — Fitur inti
- [ ] Tulis 1 fitur nyata (bukan placeholder) di sumber utama
- [ ] Unit test untuk fitur itu
- [ ] `make lint` bersih
__TYPED_TODO__
## Fase 3 — Siap rilis
- [ ] `make build` menghasilkan artefak
- [ ] CI hijau (`.github/workflows/ci.yml`)
- [ ] `project-forge verify .` exit 0
- [ ] README: quickstart sudah dicoba dari nol
"""

TYPED_TODO_PY = """- [ ] `mypy src` bersih
- [ ] `pytest -q` hijau
"""
TYPED_TODO_TS = """- [ ] `npm run typecheck` bersih
- [ ] `npm test` hijau
"""
TYPED_TODO_WEB = """- [ ] `npx playwright test` hijau (e2e)
- [ ] aksesibilitas: kontras & label form dicek
"""

GITIGNORE_TS = """node_modules/
dist/
build/
coverage/
playwright-report/
test-results/
.env
.env.*
!.env.example
.DS_Store
*.log
"""
GITIGNORE_PY = """__pycache__/
*.py[cod]
.venv/
venv/
dist/
build/
*.egg-info/
.pytest_cache/
.mypy_cache/
.ruff_cache/
.coverage
htmlcov/
.env
.env.*
!.env.example
.DS_Store
*.log
data/processed/*
!data/processed/.gitkeep
"""

EDITORCONFIG = """root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
indent_style = space
indent_size = 2

[*.py]
indent_size = 4

[Makefile]
indent_style = tab
"""

ENV_EXAMPLE = """# __NAME__ — salin ke .env lalu isi
APP_ENV=development
LOG_LEVEL=info
# PORT=3000
# DATABASE_URL=
# API_KEY=
"""

SECURITY = """# Security Policy

## Melaporkan celah
Email: security@example.com (ganti sebelum rilis)

## Cakupan
Versi yang didukung: rilis terakhir.
Jangan buka issue publik untuk celah keamanan.
"""

CONTRIBUTING = """# Berkontribusi

1. Fork & branch: `feat/singkat-jelas`
2. `make setup` lalu `make test`
3. `make verify` harus exit 0
4. Commit: `feat: ...`, `fix: ...`, `docs: ...`
5. PR: jelaskan masalah, solusi, dan cara uji
"""

CHANGELOG = """# Changelog

Format: [Keep a Changelog](https://keepachangelog.com/), versi: SemVer.

## [Unreleased]
### Added
- Struktur awal proyek (scaffold project-forge)
"""

LICENSE = """MIT License

Copyright (c) __YEAR__ __NAME__

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

ADR1 = """# ADR 0001 — Arsitektur awal

Tanggal: __YEAR__
Status: Accepted

## Konteks
Proyek baru, butuh struktur yang bisa diuji, di-lint, dan dirilis tanpa utang awal.

## Keputusan
- Struktur `src/` + `tests/` terpisah
- Konfigurasi eksplisit (lint, typecheck, test) di repo, bukan global
- CI menjalankan gate yang sama dengan `make verify`

## Konsekuensi
- Onboarding butuh `make setup` sekali
- Semua perubahan struktur wajib ADR baru
"""

PRE_COMMIT_TS = """repos:
  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v3.1.0
    hooks: [{id: prettier, types_or: [ts, tsx, json, css, md]}]
  - repo: local
    hooks:
      - id: lint
        name: lint
        entry: npm run lint
        language: system
        pass_filenames: false
"""

PRE_COMMIT_PY = """repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.9
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  - repo: local
    hooks:
      - id: mypy
        name: mypy
        entry: mypy src
        language: system
        pass_filenames: false
"""


def skill_md(name, slug, desc, typ, stack, gates):
    return f"""---
name: {slug}
description: Workflow proyek {name} ({typ}/{stack}). Pakai SEBELUM mengubah kode, menambah file, atau menjawab "selesai".
---

# {name}

{desc}

## Mulai (2 perintah)
- `project-forge status .` → gate yang belum lulus
- `make dev` (atau `make test` bila hanya mengubah logika)

## Aturan keras
- Jangan tambah dependency tanpa alasan + catat di `CHANGELOG.md`.
- Jangan ubah struktur folder tanpa ADR baru di `docs/adr/`.
- Jangan sentuh `.env` nyata; pakai `.env.example`.
- "Selesai" hanya jika `project-forge verify .` exit 0.

## Gate
{", ".join(gates)}

## Peta detail (baca hanya bila perlu)
- `TODO.md` → checklist + diagram fase
- `README.md` → quickstart + perintah
- `docs/adr/0001-*.md` → keputusan arsitektur
- `.github/workflows/ci.yml` → CI
"""


# ── template: web (ts) ─────────────────────────────────────────────────────
WEB = {
    "package.json": """{
  "name": "__PKG__",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "preview": "vite preview",
    "test": "vitest run",
    "test:watch": "vitest",
    "test:e2e": "playwright test",
    "lint": "eslint . --max-warnings=0",
    "typecheck": "tsc --noEmit",
    "fmt": "prettier --write ."
  },
  "dependencies": { "react": "^18.3.1", "react-dom": "^18.3.1" },
  "devDependencies": {
    "@playwright/test": "^1.47.0",
    "@testing-library/jest-dom": "^6.5.0",
    "@testing-library/react": "^16.0.1",
    "@types/react": "^18.3.5",
    "@types/react-dom": "^18.3.0",
    "@vitejs/plugin-react": "^4.3.1",
    "eslint": "^9.10.0",
    "eslint-plugin-react-hooks": "^5.1.0",
    "jsdom": "^25.0.0",
    "prettier": "^3.3.3",
    "typescript": "^5.6.2",
    "typescript-eslint": "^8.5.0",
    "vite": "^5.4.3",
    "vitest": "^2.1.1"
  }
}
""",
    "tsconfig.json": """{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "moduleResolution": "bundler",
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "skipLibCheck": true,
    "isolatedModules": true,
    "noEmit": true,
    "types": ["vitest/globals", "@testing-library/jest-dom"]
  },
  "include": ["src", "tests", "vite.config.ts", "playwright.config.ts"]
}
""",
    "vite.config.ts": """import { defineConfig } from "vite"
import react from "@vitejs/plugin-react"

export default defineConfig({
  plugins: [react()],
  test: {
    environment: "jsdom",
    setupFiles: ["./tests/setup.ts"],
    globals: true,
    include: ["tests/**/*.test.{ts,tsx}"],
    exclude: ["e2e/**", "node_modules/**", "dist/**"],
  },
})
""",
    "index.html": """<!doctype html>
<html lang="id">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>__NAME__</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
""",
    "src/main.tsx": """import { StrictMode } from "react"
import { createRoot } from "react-dom/client"
import App from "./App"
import "./index.css"

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
""",
    "src/App.tsx": """export default function App() {
  return (
    <main style={{ fontFamily: "system-ui", padding: 48, lineHeight: 1.5 }}>
      <h1>__NAME__</h1>
      <p>__DESC__</p>
      <p>
        Mulai dari <code>src/App.tsx</code>. Checklist ada di <code>TODO.md</code>.
      </p>
    </main>
  )
}
""",
    "src/index.css": """:root {
  color-scheme: light dark;
  --bg: #0b1020;
  --fg: #e2e8f0;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--fg);
  font-family: system-ui, -apple-system, sans-serif;
}
""",
    "tests/setup.ts": """import "@testing-library/jest-dom/vitest"
""",
    "tests/app.test.tsx": """import { render, screen } from "@testing-library/react"
import App from "../src/App"

test("judul proyek tampil", () => {
  render(<App />)
  expect(screen.getByRole("heading", { level: 1 })).toHaveTextContent("__NAME__")
})
""",
    "playwright.config.ts": """import { defineConfig } from "@playwright/test"

export default defineConfig({
  testDir: "./e2e",
  use: { baseURL: "http://localhost:5173" },
  webServer: { command: "npm run dev", url: "http://localhost:5173", reuseExistingServer: true },
})
""",
    "eslint.config.js": """import js from "@eslint/js"
import tseslint from "typescript-eslint"
import reactHooks from "eslint-plugin-react-hooks"

export default tseslint.config(
  { ignores: ["dist", "node_modules", "playwright-report"] },
  js.configs.recommended,
  ...tseslint.configs.recommended,
  { plugins: { "react-hooks": reactHooks }, rules: { ...reactHooks.configs.recommended.rules } },
)
""",
    ".prettierrc": """{ "semi": false, "printWidth": 100, "singleQuote": false }
""",
    "e2e/smoke.spec.ts": """import { test, expect } from "@playwright/test"

test("halaman utama terbuka", async ({ page }) => {
  await page.goto("/")
  await expect(page.getByRole("heading", { level: 1 })).toBeVisible()
})
""",
    "Dockerfile": """FROM node:22-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
""",
}

# ── template: api (py) ─────────────────────────────────────────────────────
API_PY = {
    "pyproject.toml": """[project]
name = "__PKG__"
version = "0.1.0"
description = "__DESC__"
requires-python = ">=3.11"
dependencies = ["fastapi>=0.115", "uvicorn[standard]>=0.30", "pydantic-settings>=2.4"]

[dependency-groups]
dev = ["ruff>=0.6", "mypy>=1.11", "pytest>=8.3", "httpx>=0.27"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/__PKG__"]

[tool.ruff]
line-length = 100
src = ["src", "tests"]

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP", "SIM"]

[tool.mypy]
python_version = "3.11"
strict = true
files = ["src"]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
""",
    "src/__PKG__/__init__.py": '''"""__NAME__ — __DESC__"""

__version__ = "0.1.0"
''',
    "src/__PKG__/config.py": """from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "development"
    log_level: str = "info"


settings = Settings()
""",
    "src/__PKG__/main.py": '''from fastapi import FastAPI
from pydantic import BaseModel

from .config import settings

app = FastAPI(title="__NAME__", version="0.1.0")


class Item(BaseModel):
    id: int
    name: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "env": settings.app_env}


@app.get("/api/items")
def list_items() -> list[Item]:
    return [Item(id=1, name="contoh")]
''',
    "tests/test_health.py": '''from fastapi.testclient import TestClient

from __PKG__.main import app

client = TestClient(app)


def test_health_ok() -> None:
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_items_bukan_kosong() -> None:
    r = client.get("/api/items")
    assert r.status_code == 200
    assert len(r.json()) >= 1
''',
    "Dockerfile": """FROM python:3.12-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
COPY pyproject.toml ./
RUN uv sync --no-dev
COPY src ./src
EXPOSE 8000
CMD ["uv", "run", "uvicorn", "__PKG__.main:app", "--host", "0.0.0.0", "--port", "8000"]
""",
    "docker-compose.yml": """services:
  api:
    build: .
    ports: ["8000:8000"]
    env_file: [.env]
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request;urllib.request.urlopen('http://localhost:8000/health')"]
      interval: 30s
      timeout: 5s
      retries: 3
""",
    ".dockerignore": """.git
.venv
__pycache__
*.pyc
.pytest_cache
.env
""",
}

# ── template: api (ts) ─────────────────────────────────────────────────────
API_TS = {
    "package.json": """{
  "name": "__PKG__",
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "tsx watch src/server.ts",
    "build": "tsc -p tsconfig.build.json",
    "start": "node dist/server.js",
    "test": "vitest run",
    "lint": "eslint . --max-warnings=0",
    "typecheck": "tsc --noEmit",
    "fmt": "prettier --write ."
  },
  "dependencies": { "fastify": "^4.28.1" },
  "devDependencies": {
    "@types/node": "^22.5.0",
    "eslint": "^9.10.0",
    "prettier": "^3.3.3",
    "tsx": "^4.19.0",
    "typescript": "^5.6.2",
    "typescript-eslint": "^8.5.0",
    "vitest": "^2.1.1"
  }
}
""",
    "tsconfig.json": """{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "noEmit": true,
    "skipLibCheck": true,
    "types": ["node", "vitest/globals"]
  },
  "include": ["src", "tests", "vitest.config.ts"]
}
""",
    "tsconfig.build.json": """{
  "extends": "./tsconfig.json",
  "compilerOptions": { "noEmit": false, "outDir": "dist", "rootDir": "src", "declaration": true },
  "include": ["src"],
  "exclude": ["tests", "dist"]
}
""",
    "vitest.config.ts": """import { defineConfig } from "vitest/config"

export default defineConfig({
  test: { include: ["tests/**/*.test.ts"], exclude: ["dist/**", "node_modules/**"] },
})
""",
    "src/app.ts": """import Fastify from "fastify"

export function buildApp() {
  const app = Fastify({ logger: true })

  app.get("/health", async () => ({ status: "ok", env: process.env.APP_ENV ?? "development" }))

  app.get("/api/items", async () => [{ id: 1, name: "contoh" }])

  return app
}
""",
    "src/server.ts": """import { buildApp } from "./app.js"

const port = Number(process.env.PORT ?? 3000)
buildApp()
  .listen({ port, host: "0.0.0.0" })
  .catch((err) => {
    console.error(err)
    process.exit(1)
  })
""",
    "tests/health.test.ts": """import { describe, expect, it } from "vitest"
import { buildApp } from "../src/app.js"

describe("api", () => {
  it("health ok", async () => {
    const app = buildApp()
    const res = await app.inject({ method: "GET", url: "/health" })
    expect(res.statusCode).toBe(200)
    expect(res.json()).toMatchObject({ status: "ok" })
  })
})
""",
    "eslint.config.js": """import js from "@eslint/js"
import tseslint from "typescript-eslint"

export default tseslint.config({ ignores: ["dist"] }, js.configs.recommended,
  ...tseslint.configs.recommended)
""",
    ".prettierrc": """{ "semi": false, "printWidth": 100 }
""",
    "Dockerfile": """FROM node:22-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:22-alpine
WORKDIR /app
ENV NODE_ENV=production
COPY --from=build /app/package*.json ./
RUN npm ci --omit=dev
COPY --from=build /app/dist ./dist
EXPOSE 3000
CMD ["node", "dist/server.js"]
""",
}

# ── template: cli (py) ─────────────────────────────────────────────────────
CLI_PY = {
    "pyproject.toml": """[project]
name = "__PKG__"
version = "0.1.0"
description = "__DESC__"
requires-python = ">=3.11"
dependencies = []

[project.scripts]
__SLUG__ = "__PKG__.cli:main"

[dependency-groups]
dev = ["ruff>=0.6", "mypy>=1.11", "pytest>=8.3"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/__PKG__"]

[tool.ruff]
line-length = 100
src = ["src", "tests"]

[tool.mypy]
python_version = "3.11"
strict = true
files = ["src"]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
""",
    "src/__PKG__/__init__.py": '''"""__NAME__ — __DESC__"""

__version__ = "0.1.0"
''',
    "src/__PKG__/cli.py": '''import argparse
import sys

from . import __version__


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="__PKG__", description="__DESC__")
    p.add_argument("--version", action="version", version=f"__PKG__ {__version__}")
    p.add_argument("name", nargs="?", default="dunia", help="siapa yang disapa")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    print(f"Halo, {args.name}!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
''',
    "tests/test_cli.py": '''from __PKG__.cli import main


def test_main_default(capsys) -> None:  # type: ignore[no-untyped-def]
    assert main([]) == 0
    assert "Halo, dunia!" in capsys.readouterr().out


def test_main_arg(capsys) -> None:  # type: ignore[no-untyped-def]
    assert main(["mamat"]) == 0
    assert "mamat" in capsys.readouterr().out
''',
}

# ── template: lib (ts) ─────────────────────────────────────────────────────
LIB_TS = {
    "package.json": """{
  "name": "__PKG__",
  "version": "0.1.0",
  "type": "module",
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "files": ["dist"],
  "exports": { ".": { "types": "./dist/index.d.ts", "import": "./dist/index.js" } },
  "scripts": {
    "build": "tsup",
    "test": "vitest run",
    "lint": "eslint . --max-warnings=0",
    "typecheck": "tsc --noEmit",
    "fmt": "prettier --write ."
  },
  "devDependencies": {
    "@types/node": "^22.5.0",
    "eslint": "^9.10.0",
    "prettier": "^3.3.3",
    "tsup": "^8.2.4",
    "typescript": "^5.6.2",
    "typescript-eslint": "^8.5.0",
    "vitest": "^2.1.1"
  }
}
""",
    "tsup.config.ts": """import { defineConfig } from "tsup"

export default defineConfig({
  entry: ["src/index.ts"],
  format: ["esm"],
  dts: true,
  clean: true,
  sourcemap: true,
})
""",
    "tsconfig.json": """{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "declaration": true,
    "skipLibCheck": true,
    "types": ["node", "vitest/globals"]
  },
  "include": ["src", "tests"]
}
""",
    "src/index.ts": """/** __NAME__ — __DESC__ */
export function greet(name: string): string {
  return `Halo, ${name}!`
}
""",
    "tests/index.test.ts": """import { describe, expect, it } from "vitest"
import { greet } from "../src/index"

describe("greet", () => {
  it("menyapa", () => {
    expect(greet("mamat")).toBe("Halo, mamat!")
  })
})
""",
    "eslint.config.js": """import js from "@eslint/js"
import tseslint from "typescript-eslint"

export default tseslint.config({ ignores: ["dist"] }, js.configs.recommended,
  ...tseslint.configs.recommended)
""",
    ".prettierrc": """{ "semi": false, "printWidth": 100 }
""",
}

# ── template: data (py) ────────────────────────────────────────────────────
DATA_PY = {
    "pyproject.toml": """[project]
name = "__PKG__"
version = "0.1.0"
description = "__DESC__"
requires-python = ">=3.11"
dependencies = ["polars>=1.6", "pyarrow>=17.0"]

[dependency-groups]
dev = ["ruff>=0.6", "mypy>=1.11", "pytest>=8.3", "pandas>=2.2", "jupyterlab>=4.2"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/__PKG__"]

[tool.ruff]
line-length = 100
src = ["src", "tests"]

[tool.mypy]
python_version = "3.11"
strict = true
files = ["src"]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
""",
    "src/__PKG__/__init__.py": '''"""__NAME__ — __DESC__"""

__version__ = "0.1.0"
''',
    "src/__PKG__/pipeline.py": '''from __future__ import annotations

import polars as pl


def load(path: str) -> pl.DataFrame:
    """Muat data mentah (csv/parquet/json)."""
    if path.endswith(".parquet"):
        return pl.read_parquet(path)
    if path.endswith(".json"):
        return pl.read_json(path)
    return pl.read_csv(path)


def clean(df: pl.DataFrame) -> pl.DataFrame:
    """Buang baris kosong + duplikat, rapikan nama kolom."""
    df = df.drop_nulls()
    return df.unique().rename({c: c.strip().lower().replace(" ", "_") for c in df.columns})
''',
    "tests/test_pipeline.py": '''import polars as pl

from __PKG__.pipeline import clean


def test_clean_hapus_duplikat() -> None:
    df = pl.DataFrame({"a": [1, 1, 2], "b": ["x", "x", "y"]})
    out = clean(df)
    assert out.height == 2
''',
    "Makefile.data": """data:
\t@echo "letakkan data mentah di data/raw/, hasil di data/processed/"
""",
}

# ── Makefile + CI ──────────────────────────────────────────────────────────
MAKEFILE_TS = """SHELL := /bin/bash
.DEFAULT_GOAL := help

setup:
\t@command -v npm >/dev/null || { echo "butuh node/npm"; exit 1; }
\tnpm install
\t@test -f .env || cp .env.example .env

dev:
\tnpm run dev

test:
\tnpm test

lint:
\tnpm run lint

typecheck:
\tnpm run typecheck

build:
\tnpm run build

verify:
\t@project-forge verify .

clean:
\trm -rf node_modules dist coverage

help:
\t@grep -E '^[a-zA-Z_-]+:' Makefile | cut -d: -f1 | grep -v '^help$$' | tr '\\n' ' '; echo
"""

MAKEFILE_PY = """SHELL := /bin/bash
.DEFAULT_GOAL := help
UV := $(shell command -v uv || true)

setup:
\t@if [ -n "$(UV)" ]; then uv sync; else python3 -m venv .venv && .venv/bin/pip install -e ".[dev]"; fi
\t@test -f .env || cp .env.example .env

dev:
\t@if [ -n "$(UV)" ]; then uv run python -m __PKG__; else .venv/bin/python -m __PKG__; fi

test:
\t@if [ -n "$(UV)" ]; then uv run pytest -q; else .venv/bin/pytest -q; fi

lint:
\t@if [ -n "$(UV)" ]; then uv run ruff check . && uv run ruff format --check .; else .venv/bin/ruff check .; fi

typecheck:
\t@if [ -n "$(UV)" ]; then uv run mypy src; else .venv/bin/mypy src; fi

build:
\t@if [ -n "$(UV)" ]; then uv build; else .venv/bin/python -m build; fi

verify:
\t@project-forge verify .

clean:
\trm -rf .venv dist build *.egg-info .pytest_cache .mypy_cache .ruff_cache

help:
\t@grep -E '^[a-zA-Z_-]+:' Makefile | cut -d: -f1 | grep -v '^help$$' | tr '\\n' ' '; echo
"""

CI_TS = """name: ci
on:
  push: { branches: [main] }
  pull_request:
jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 22, cache: npm }
      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck
      - run: npm test
      - run: npm run build
"""

CI_PY = """name: ci
on:
  push: { branches: [main] }
  pull_request:
jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - run: uv sync
      - run: uv run ruff check .
      - run: uv run mypy src
      - run: uv run pytest -q
      - run: uv build
"""


# ── generator ──────────────────────────────────────────────────────────────
def required_files(typ, stack):
    common = ["README.md", "AGENTS.md", "TODO.md", "Makefile", ".gitignore", ".editorconfig",
              ".env.example", "SECURITY.md", "CONTRIBUTING.md", "CHANGELOG.md", "LICENSE",
              "docs/adr/0001-initial-architecture.md", ".github/workflows/ci.yml",
              ".pre-commit-config.yaml", ".mamat/project.json"]
    extra = {
        ("web", "ts"): ["package.json", "tsconfig.json", "vite.config.ts", "index.html",
                        "src/main.tsx", "src/App.tsx", "tests/app.test.tsx",
                        "playwright.config.ts", "e2e/smoke.spec.ts", "Dockerfile"],
        ("api", "py"): ["pyproject.toml", "src/__PKG__/main.py", "tests/test_health.py",
                        "Dockerfile", "docker-compose.yml"],
        ("api", "ts"): ["package.json", "tsconfig.json", "src/server.ts",
                        "tests/health.test.ts", "Dockerfile"],
        ("cli", "py"): ["pyproject.toml", "src/__PKG__/cli.py", "tests/test_cli.py"],
        ("lib", "ts"): ["package.json", "tsup.config.ts", "src/index.ts", "tests/index.test.ts"],
        ("data", "py"): ["pyproject.toml", "src/__PKG__/pipeline.py", "tests/test_pipeline.py"],
    }[(typ, stack)]
    return common + extra


def gates_for(typ, stack):
    g = ["structure"]
    if stack == "ts":
        g += ["lint", "types", "test", "build"]
    else:
        g += ["lint", "types", "test", "build"]
    g += ["security", "docs"]
    return g


def gen_skill(root, name, desc, typ, stack, slug, gates):
    body = skill_md(name, slug, desc, typ, stack, gates)
    for rel in (f".opencode/skills/{slug}/SKILL.md", f".claude/skills/{slug}/SKILL.md"):
        w(os.path.join(root, rel), body)
    return body


def catalog_get(fid):
    """entri katalog framework atau server/infra/security."""
    return FC.get(fid) or SC.get(fid)


def catalog_search(q):
    seen, out = set(), []
    for e in FC.search(q) + SC.search(q):
        if e["id"] not in seen:
            seen.add(e["id"])
            out.append(e)
    return out


def subst_keys(text, **kw):
    """ganti {key} saja — brace literal (YAML/JSON/awk) tidak disentuh."""
    for k, v in kw.items():
        text = re.sub(r"(?<!\$)\{" + k + r"\}", lambda m, v=str(v): v, text)
    return text


def new_framework(root, name, desc, fid, a):
    """scaffold lewat CLI resmi framework + tempel standar proyek + gate."""
    e = catalog_get(fid)
    if not e:
        sug = ", ".join(x["id"] for x in catalog_search(fid)[:8]) or "lihat `project-forge frameworks`"
        sys.exit(f"framework tidak dikenal: {fid}\n  mirip: {sug}")
    if os.path.isdir(root) and os.listdir(root):
        if "--force" not in a:
            sys.exit(f"folder tidak kosong: {root} (pakai --force bila memang mau menimpa)")
        for entry in os.listdir(root):
            p_ = os.path.join(root, entry)
            shutil.rmtree(p_, ignore_errors=True) if os.path.isdir(p_) else os.remove(p_)

    slug = slugify(name)
    pkg = slug.replace("-", "_")
    subs = dict(name=name, desc=desc, slug=slug, pkg=pkg, year=YEAR)

    missing = [n for n in e["needs"] if not shutil.which(n)]
    if missing:
        print(f"⚠️  butuh: {', '.join(missing)}" + (f" → {e['hint']}" if e.get("hint") else ""))
        print("   scaffold dokumentasi tetap dibuat; gate bahasa akan SKIP.")

    os.makedirs(root, exist_ok=True)
    boot = subst_keys(e["boot"], slug=slug, pkg=pkg, name=name, module=pkg)
    tmp = tempfile.mkdtemp(prefix="pf-fw-")
    print(f"» bootstrap {fid} ...")
    env = dict(os.environ, CI="1", NONINTERACTIVE="1", TERM="dumb")
    r = subprocess.run(boot, cwd=tmp, shell=True, capture_output=True, text=True,
                       timeout=3600, env=env, stdin=subprocess.DEVNULL)
    if r.returncode != 0:
        tail = (r.stdout + r.stderr).strip().splitlines()
        print(f"⚠️  bootstrap keluar {r.returncode}: {tail[-1][:160] if tail else '-'}")
    # pindahkan hasil ke root
    moved = 0
    for entry in os.listdir(tmp):
        shutil.move(os.path.join(tmp, entry), os.path.join(root, entry))
        moved += 1
    shutil.rmtree(tmp, ignore_errors=True)
    # ratakan bila arsip menghasilkan satu folder bersarang
    entries = [x for x in os.listdir(root) if x != ".DS_Store"]
    if len(entries) == 1 and os.path.isdir(os.path.join(root, entries[0])):
        inner = os.path.join(root, entries[0])
        for item in os.listdir(inner):
            shutil.move(os.path.join(inner, item), os.path.join(root, item))
        os.rmdir(inner)
    print(f"   {moved} entri dibuat")

    # venv yang ikut dipindah punya path absolut ke tmp → buat ulang
    if os.path.isdir(os.path.join(root, ".venv")):
        shutil.rmtree(os.path.join(root, ".venv"), ignore_errors=True)
        if shutil.which("uv"):
            subprocess.run(["uv", "sync", "-q"], cwd=root, capture_output=True, timeout=3600)

    # berkas minimal untuk framework yang bootstrap-nya cuma memasang dep
    added = 0
    for rel, content in (e.get("files") or {}).items():
        target = os.path.join(root, rel.replace("{pkg}", pkg))
        if os.path.exists(target):
            continue
        body = subst_keys(content, name=name, pkg=pkg, slug=slug, desc=desc)
        w(target, body)
        added += 1
    if added:
        print(f"   {added} berkas awal ditulis")

    if e["deps"]:
        print("» memasang dependency ...")
        d = subprocess.run(e["deps"], cwd=root, shell=True, capture_output=True, text=True,
                           timeout=5400, env=dict(os.environ, CI="1"), stdin=subprocess.DEVNULL)
        if d.returncode != 0:
            tail = (d.stdout + d.stderr).strip().splitlines()
            print(f"⚠️  deps keluar {d.returncode}: {tail[-1][:160] if tail else '-'}")

    # standar proyek
    subs["tree"] = "\n".join("├── " + x for x in sorted(os.listdir(root))[:12])
    common = {
        "README.md": README, "AGENTS.md": AGENTS, "SECURITY.md": SECURITY,
        "CONTRIBUTING.md": CONTRIBUTING, "CHANGELOG.md": CHANGELOG, "LICENSE": LICENSE,
        "docs/adr/0001-initial-architecture.md": ADR1, ".editorconfig": EDITORCONFIG,
        ".env.example": ENV_EXAMPLE,
    }
    for rel, content in common.items():
        w(os.path.join(root, rel), sub(content, **subs))
    if not os.path.exists(os.path.join(root, ".gitignore")):
        w(os.path.join(root, ".gitignore"),
          PS.GIT.get(e["lang"], ".env\nnode_modules/\n") + ".venv/\nbuild/\ndist/\n")
    if not os.path.exists(os.path.join(root, ".github/workflows/ci.yml")):
        w(os.path.join(root, ".github/workflows/ci.yml"),
          "name: ci\non:\n  push: { branches: [main] }\n  pull_request:\n"
          "jobs:\n  ci:\n    runs-on: ubuntu-latest\n    steps:\n"
          "      - uses: actions/checkout@v4\n"
          "      - run: echo 'jalankan gate: project-forge status .'\n")

    gates = ["structure"] + [g for g in ("lint", "types", "test", "build")
                             if g in e["gates"]] + ["security", "docs"]
    typed_todo = "".join(f"- [ ] `{cmd}` hijau\n" for cmd in e["gates"].values())
    w(os.path.join(root, "TODO.md"),
      sub(TODO, **subs).replace("__MERMAID__", MERMAID)
      .replace("__TYPED_TODO__", typed_todo))

    st = {"name": name, "slug": slug, "type": e["kind"], "stack": fid,
          "framework": fid, "lang": e["lang"], "package": pkg,
          "created": time.strftime("%Y-%m-%dT%H:%M:%S"), "gates": gates,
          "gate_cmds": e["gates"], "schema": 1}
    w(os.path.join(root, ".mamat/project.json"), json.dumps(st, indent=2, ensure_ascii=False))
    gen_skill(root, name, desc, e["kind"], fid, slug, gates)

    if flag(a, "--git") and shutil.which("git"):
        if not os.path.isdir(os.path.join(root, ".git")):
            sh(["git", "init", "-q"], cwd=root)
            sh(["git", "add", "-A"], cwd=root)
            sh(["git", "-c", "user.email=dev@local", "-c", "user.name=dev",
                "commit", "-qm", "chore: scaffold project-forge"], cwd=root)
    print(f"✅ scaffold: {root}")
    print(f"   framework={fid} ({e['lang']}/{e['kind']}) gate={len(gates)} "
          f"skill=.opencode/skills/{slug}/SKILL.md")
    print("   berikutnya: project-forge status .")


def new_generic(root, name, desc, typ, stack, slug, pkg, a):
    gates = PS.gates_for(typ, stack)
    subs = dict(name=name, desc=desc, slug=slug, pkg=pkg, year=YEAR)
    if os.path.isdir(root) and os.listdir(root) and "--force" not in a:
        sys.exit(f"folder tidak kosong: {root} (pakai --force bila memang mau menimpa)")
    req = PS.required(typ, stack, pkg)
    tree = "\n".join("├── " + r for r in sorted(set(req))) + \
        f"\n├── .opencode/skills/{slug}/SKILL.md"
    subs["tree"] = tree
    typed = {"go": "- [ ] `go vet ./...` bersih\n- [ ] `go test ./...` hijau\n",
             "rust": "- [ ] `cargo clippy -- -D warnings` bersih\n- [ ] `cargo test` hijau\n",
             "java": "- [ ] `mvn test` hijau\n", "csharp": "- [ ] `dotnet test` hijau\n",
             "php": "- [ ] `php -l` bersih\n", "ruby": "- [ ] `ruby test/...` hijau\n",
             "swift": "- [ ] `swift test` hijau\n", "lua": "- [ ] `lua tests/test.lua` ok\n",
             "bash": "- [ ] `shellcheck` bersih\n", "c": "- [ ] `make test` hijau\n",
             "cpp": "- [ ] `make test` hijau\n", "js": "- [ ] `npm test` hijau\n",
             "dart": "- [ ] `dart analyze` bersih\n", "elixir": "- [ ] `mix test` hijau\n",
             "zig": "- [ ] `zig build` ok\n", "r": "- [ ] `Rscript tests/test.R` ok\n",
             "julia": "- [ ] `julia test/runtests.jl` ok\n"}.get(stack, "")
    common = {
        "README.md": README, "AGENTS.md": AGENTS, "SECURITY.md": SECURITY,
        "CONTRIBUTING.md": CONTRIBUTING, "CHANGELOG.md": CHANGELOG, "LICENSE": LICENSE,
        "docs/adr/0001-initial-architecture.md": ADR1, ".editorconfig": EDITORCONFIG,
        ".env.example": ENV_EXAMPLE, ".pre-commit-config.yaml": PRE_COMMIT_TS,
        "TODO.md": TODO.replace("__MERMAID__", MERMAID).replace("__TYPED_TODO__", typed),
    }
    for rel, content in common.items():
        w(os.path.join(root, rel), sub(content, **subs))
    st = {"name": name, "slug": slug, "type": typ, "stack": stack, "package": pkg,
          "created": time.strftime("%Y-%m-%dT%H:%M:%S"), "gates": gates, "schema": 1,
          "generic": True}
    PS.generate(root, st, subs)
    w(os.path.join(root, ".mamat/project.json"), json.dumps(st, indent=2, ensure_ascii=False))
    gen_skill(root, name, desc, typ, stack, slug, gates)
    if flag(a, "--git") and shutil.which("git"):
        if not os.path.isdir(os.path.join(root, ".git")):
            sh(["git", "init", "-q"], cwd=root)
            sh(["git", "add", "-A"], cwd=root)
            sh(["git", "-c", "user.email=dev@local", "-c", "user.name=dev",
                "commit", "-qm", "chore: scaffold project-forge"], cwd=root)
    if flag(a, "--install"):
        print("» memasang dependency ...")
        r = sh(["make", "setup"], cwd=root)
        print((r.stdout or r.stderr)[-600:])
    print(f"✅ scaffold: {root}")
    print(f"   tipe={typ}/{stack} paket={pkg} gate={len(gates)} skill=.opencode/skills/{slug}/SKILL.md")
    print("   berikutnya: make setup && project-forge status .")


def cmd_new(a):
    if not a:
        print(__doc__)
        return
    root = os.path.abspath(a[0])
    if "--framework" in a:
        fid = a[a.index("--framework") + 1]
        name = a[a.index("--name") + 1] if "--name" in a else os.path.basename(root)
        desc = a[a.index("--desc") + 1] if "--desc" in a else f"Proyek {name}"
        return new_framework(root, name, desc, fid, a)
    name = a[a.index("--name") + 1] if "--name" in a else os.path.basename(root)
    desc = a[a.index("--desc") + 1] if "--desc" in a else f"Proyek {name}"
    typ = a[a.index("--type") + 1] if "--type" in a else "web"
    stack = a[a.index("--stack") + 1] if "--stack" in a else STACKS[typ][0]
    if typ not in TYPES:
        sys.exit(f"--type harus salah satu: {', '.join(sorted(TYPES))}")
    ok_stack = (typ, stack) in DETAILED or (typ, stack) in PS.SPECS
    if stack not in STACKS.get(typ, []) or not ok_stack:
        sys.exit(f"--stack untuk {typ}: {', '.join(STACKS.get(typ, []))} "
                 f"(lengkap: {', '.join(f'{t}/{s}' for t, s in sorted(PS.SPECS))})")
    slug = slugify(name)
    pkg = slug.replace("-", "_") if stack == "py" else slug
    if (typ, stack) not in DETAILED:
        return new_generic(root, name, desc, typ, stack, slug, pkg, a)
    gates = gates_for(typ, stack)
    subs = dict(name=name, desc=desc, slug=slug, pkg=pkg, year=YEAR)

    if os.path.isdir(root) and os.listdir(root) and "--force" not in a:
        sys.exit(f"folder tidak kosong: {root} (pakai --force bila memang mau menimpa)")

    files = {}
    # common
    files["README.md"] = README
    files["AGENTS.md"] = AGENTS
    files["SECURITY.md"] = SECURITY
    files["CONTRIBUTING.md"] = CONTRIBUTING
    files["CHANGELOG.md"] = CHANGELOG
    files["LICENSE"] = LICENSE
    files["docs/adr/0001-initial-architecture.md"] = ADR1
    files[".editorconfig"] = EDITORCONFIG
    files[".env.example"] = ENV_EXAMPLE
    files[".pre-commit-config.yaml"] = PRE_COMMIT_PY if stack == "py" else PRE_COMMIT_TS
    files[".gitignore"] = GITIGNORE_PY if stack == "py" else GITIGNORE_TS
    files[".github/workflows/ci.yml"] = CI_PY if stack == "py" else CI_TS

    # typed
    tables = {("web", "ts"): WEB, ("api", "py"): API_PY, ("api", "ts"): API_TS,
              ("cli", "py"): CLI_PY, ("lib", "ts"): LIB_TS, ("data", "py"): DATA_PY}
    files.update(tables[(typ, stack)])

    # Makefile: py butuh nama modul
    mk = MAKEFILE_PY.replace("__PKG__", pkg) if stack == "py" else MAKEFILE_TS
    files["Makefile"] = mk

    # susun tree untuk README
    rels = sorted(set(required_files(typ, stack)) | {"Makefile", ".opencode/skills/" + slug + "/SKILL.md"})
    tree = "\n".join("├── " + r for r in rels) + ("\n└── data/" if typ == "data" else "")
    subs["tree"] = tree

    # TODO per tipe
    typed_todo = TYPED_TODO_PY if stack == "py" else TYPED_TODO_TS
    if typ == "web":
        typed_todo += TYPED_TODO_WEB
    files["TODO.md"] = TODO.replace("__MERMAID__", MERMAID).replace("__TYPED_TODO__", typed_todo)

    for rel, content in files.items():
        target = os.path.join(root, rel)
        target = target.replace("__PKG__", pkg) if "__PKG__" in rel else target
        w(target, sub(content, **subs))

    # direktori data
    if typ == "data":
        for d in ("data/raw", "data/processed", "notebooks"):
            os.makedirs(os.path.join(root, d), exist_ok=True)
            w(os.path.join(root, d, ".gitkeep"), "")

    # state + skill
    state = {"name": name, "slug": slug, "type": typ, "stack": stack, "package": pkg,
             "created": time.strftime("%Y-%m-%dT%H:%M:%S"), "gates": gates,
             "schema": 1}
    w(os.path.join(root, ".mamat/project.json"), json.dumps(state, indent=2, ensure_ascii=False))
    gen_skill(root, name, desc, typ, stack, slug, gates)

    if flag(a, "--git") and shutil.which("git"):
        if not os.path.isdir(os.path.join(root, ".git")):
            sh(["git", "init", "-q"], cwd=root)
            sh(["git", "add", "-A"], cwd=root)
            sh(["git", "-c", "user.email=dev@local", "-c", "user.name=dev",
                "commit", "-qm", "chore: scaffold project-forge"], cwd=root)
    if flag(a, "--install"):
        print("» memasang dependency ...")
        r = sh(["make", "setup"], cwd=root)
        print((r.stdout or r.stderr)[-600:])

    print(f"✅ scaffold: {root}")
    print(f"   tipe={typ}/{stack} paket={pkg} gate={len(gates)} skill=.opencode/skills/{slug}/SKILL.md")
    print("   berikutnya: make setup && project-forge status .")


def flag(a, name):
    return name in a


# ── gate / verifikasi ──────────────────────────────────────────────────────
SECRET_PATTERNS = [
    (r"AKIA[0-9A-Z]{16}", "AWS access key"),
    (r"sk-[A-Za-z0-9]{20,}", "OpenAI-style key"),
    (r"ghp_[A-Za-z0-9]{30,}", "GitHub token"),
    (r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----", "private key"),
    (r"(?i)(password|passwd|secret|api[_-]?key)\s*[:=]\s*['\"](?!%env\(|\$\{|<)[^'\"]{8,}['\"]",
     "hardcoded secret"),
]
SKIP_DIRS = {".git", "node_modules", "dist", "build", ".venv", "venv", "__pycache__",
             "coverage", ".pytest_cache", ".mypy_cache", ".ruff_cache", "playwright-report",
             "vendor", "target", "Pods", ".next", ".nuxt", ".svelte-kit", ".dart_tool",
             "_build", "deps", "obj", "bin", ".gradle", "zig-cache", "zig-out"}


def scan_secrets(root):
    hits = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn.endswith((".png", ".jpg", ".jpeg", ".gif", ".pdf", ".woff", ".woff2",
                            ".ico", ".mp4", ".wav", ".zip", ".lock", ".map")):
                continue
            if fn in ("package-lock.json", "uv.lock", "pnpm-lock.yaml", "yarn.lock",
                      "mvnw", "mvnw.cmd", "gradlew", "gradlew.bat"):
                continue
            p = os.path.join(dirpath, fn)
            try:
                if os.path.getsize(p) > 800_000:
                    continue
                txt = open(p, encoding="utf-8", errors="ignore").read()
            except Exception:
                continue
            for pat, label in SECRET_PATTERNS:
                if re.search(pat, txt):
                    hits.append((os.path.relpath(p, root), label))
                    break
    return hits


def read_state(root):
    p = os.path.join(root, ".mamat/project.json")
    try:
        return json.load(open(p))
    except Exception:
        return None


def cmd_frameworks(a):
    """daftar framework/library/server/security yang bisa di-scaffold."""
    if a:
        for e in catalog_search(" ".join(a)):
            print(f"{e['id']:<18} {e['lang']:<7} {e['kind']}")
        return
    kinds = {}
    for e in list(FC.F.values()) + list(SC.F.values()):
        kinds.setdefault(e["kind"], []).append(e["id"])
    for k in sorted(kinds):
        print(f"{k:<12} {' '.join(sorted(kinds[k]))}")
    print(f"\ntotal {len(FC.F) + len(SC.F)} entri "
          f"({len(FC.F)} framework/library + {len(SC.F)} server/infra/security) — --framework <id>")


def cmd_stacks(a):
    """daftar tipe/stack yang tersedia."""
    by = PS.stacks_by_type()
    for t, st in DETAILED:
        by.setdefault(t, [])
        if st not in by[t]:
            by[t].append(st)
    print("template detail:", ", ".join(f"{t}/{s}" for t, s in sorted(DETAILED)))
    print("semua stack:")
    for t in sorted(by):
        print(f"  {t:<5} {' '.join(sorted(by[t]))}")


def cmd_gates(a):
    root = os.path.abspath(a[0] if a else ".")
    st = read_state(root)
    if not st:
        sys.exit("bukan proyek project-forge (tidak ada .mamat/project.json)")
    print("gate:", ", ".join(st.get("gates", [])))


_RUBY_MODERN = None


def ruby_modern():
    """system ruby macOS 2.6 terlalu tua untuk sinatra/rails modern."""
    global _RUBY_MODERN
    if _RUBY_MODERN is None:
        r = sh(["ruby", "-e", "print RUBY_VERSION"])
        out = (r.stdout or "").strip().split(".")
        _RUBY_MODERN = r.returncode == 0 and out and out[0].isdigit() and int(out[0]) >= 3
    return _RUBY_MODERN


def run_gate(root, gate, st):
    typ, stack, pkg = st["type"], st["stack"], st["package"]
    npm = shutil.which("npm")
    uv = shutil.which("uv")
    venv = os.path.join(root, ".venv", "bin")
    node_modules = os.path.isdir(os.path.join(root, "node_modules"))

    generic = bool(st.get("generic")) and (typ, stack) in PS.SPECS
    if gate == "structure" and st.get("framework"):
        req = ["README.md", "AGENTS.md", "TODO.md", "docs/adr/0001-initial-architecture.md",
               f".opencode/skills/{st['slug']}/SKILL.md", ".mamat/project.json"]
        miss = [r for r in req if not os.path.exists(os.path.join(root, r))]
        return (("FAIL" if miss else "PASS"),
                f"hilang: {', '.join(miss)}" if miss else "standar proyek lengkap")
    if gate == "structure":
        miss = []
        req = (["AGENTS.md", "TODO.md", f".opencode/skills/{st['slug']}/SKILL.md"]
               if st.get("adopted") else
               (PS.required(typ, stack, pkg) if generic else required_files(typ, stack)))
        for rel in req:
            rel2 = rel.replace("__PKG__", pkg)
            if not os.path.exists(os.path.join(root, rel2)):
                miss.append(rel2)
        return (("FAIL" if miss else "PASS"),
                f"hilang: {', '.join(miss[:6])}" if miss else "semua berkas wajib ada")

    if gate == "docs":
        probs = []
        rd = os.path.join(root, "README.md")
        if os.path.exists(rd):
            t = open(rd, encoding="utf-8", errors="ignore").read()
            if "## Quickstart" not in t:
                probs.append("README tanpa Quickstart")
        if not os.path.exists(os.path.join(root, f".opencode/skills/{st['slug']}/SKILL.md")):
            probs.append("skill proyek tidak ada")
        td = os.path.join(root, "TODO.md")
        if os.path.exists(td) and "mermaid" not in open(td, encoding="utf-8", errors="ignore").read():
            probs.append("TODO tanpa diagram")
        if not os.path.exists(os.path.join(root, "docs/adr")):
            probs.append("tanpa docs/adr")
        return (("FAIL" if probs else "PASS"),
                "; ".join(probs) if probs else "README+skill+TODO+ADR lengkap")

    if gate == "security":
        hits = scan_secrets(root)
        if hits:
            return ("FAIL", f"{len(hits)} temuan: " + "; ".join(f"{p} ({w})" for p, w in hits[:3]))
        # .env lokal boleh ada, yang dilarang: ter-track git
        gi = os.path.join(root, ".gitignore")
        ignored = os.path.exists(gi) and re.search(r"(?m)^\.env$", open(gi, encoding="utf-8",
                                                                     errors="ignore").read())
        envf = os.path.join(root, ".env")
        if os.path.exists(envf) and not ignored:
            body = open(envf, encoding="utf-8", errors="ignore").read()
            real = any(re.search(pat, body) for pat, _ in SECRET_PATTERNS)
            if real:
                return ("FAIL", ".env ada tapi tidak di-.gitignore")
            return ("PASS", ".env hanya placeholder (tanpa secret nyata)")
        if os.path.isdir(os.path.join(root, ".git")):
            t = sh(["git", "ls-files", "--error-unmatch", ".env"], cwd=root)
            if t.returncode == 0 and t.stdout.strip():
                return ("FAIL", ".env ter-track git — `git rm --cached .env`")
        return ("PASS", "tidak ada pola secret; .env tidak ter-track")

    if st.get("framework"):
        cmds = (st.get("gate_cmds") or {}).get(gate)
        if not cmds:
            return ("PASS", "tidak berlaku")
        if st.get("lang") == "ruby" and not ruby_modern():
            return ("SKIP", "butuh ruby 3.2+ (brew install ruby) — sistem 2.6")
        if str(cmds).startswith("SKIP:"):
            return ("SKIP", str(cmds)[5:].strip())
        first = str(cmds).lstrip("(").split()[0]
        if first in ("uv", "npm", "npx", "pnpm", "yarn", "bun", "cargo", "go", "mvn", "gradle",
                     "dotnet", "composer", "bundle", "ruby", "gem", "swift", "mix", "dart",
                     "flutter", "cmake", "meson", "php", "test", "curl", "unzip", "printf"):
            if not shutil.which(first):
                return ("SKIP", f"toolchain '{first}' tidak ada → {st.get('framework')}")
        r = sh(cmds, cwd=root, timeout=3600)
        if r.returncode == 0:
            return ("PASS", str(cmds)[:80])
        out = (r.stdout or "") + (r.stderr or "")
        if "no such module 'XCTest'" in out:
            return ("SKIP", "XCTest butuh Xcode penuh")
        tail = out.strip().splitlines()
        return ("FAIL", (tail[-1] if tail else "gagal")[:180])

    if generic and gate in ("lint", "types", "test", "build"):
        return PS.gate(typ, stack, root, gate,
                       lambda c: shutil.which(c) is not None, pkg)

    # gate perintah
    if stack == "ts":
        if npm and not node_modules:
            print("   (memasang dependency npm sekali ...)")
            sh([npm, "install", "--silent"], cwd=root, timeout=2400)
            node_modules = os.path.isdir(os.path.join(root, "node_modules"))
        if not (npm and node_modules):
            return ("SKIP", "npm/node_modules belum ada → `make setup`")
        cmds = {
            "lint": ["npm", "run", "lint"],
            "types": ["npm", "run", "typecheck"],
            "test": ["npm", "test"],
            "build": ["npm", "run", "build"],
        }[gate]
        r = sh(cmds, cwd=root, timeout=1800)
        if r.returncode == 0:
            return ("PASS", " ".join(cmds[1:]) + " ok")
        msg = (r.stdout or r.stderr or "").strip().splitlines()
        return ("FAIL", (msg[-1] if msg else "gagal")[:180])

    # python
    pybin = os.path.join(venv, "python") if os.path.isdir(venv) else None
    if uv and not pybin and not os.path.isdir(os.path.join(root, ".venv")):
        print("   (menyiapkan .venv + dependency sekali ...)")
        sh([uv, "sync", "--quiet"], cwd=root, timeout=2400)
        pybin = os.path.join(venv, "python") if os.path.isdir(venv) else None
    if not uv and not pybin:
        return ("SKIP", "butuh uv atau .venv → `make setup`")
    runner = ([uv, "run"] if uv else [pybin])
    cmds = {
        "lint": runner + (["ruff", "check", "."] if uv else ["-m", "ruff", "check", "."]),
        "types": runner + (["mypy", "src"] if uv else ["-m", "mypy", "src"]),
        "test": runner + (["pytest", "-q"] if uv else ["-m", "pytest", "-q"]),
        "build": runner + (["python", "-c", "import compileall,sys;sys.exit(0 if compileall.compile_dir('src',quiet=1) else 1)"]
                           if uv else ["-c", "import compileall,sys;sys.exit(0 if compileall.compile_dir('src',quiet=1) else 1)"]),
    }[gate]
    r = sh(cmds, cwd=root, timeout=1800)
    if r.returncode == 0:
        return ("PASS", "ok")
    msg = (r.stdout or r.stderr or "").strip().splitlines()
    return ("FAIL", (msg[-1] if msg else "gagal")[:180])


ICON = {"PASS": "✅", "FAIL": "❌", "SKIP": "⏭️"}


def detect(root):
    """tebak tipe/stack proyek yang sudah ada."""
    pkg = os.path.join(root, "package.json")
    py = os.path.join(root, "pyproject.toml")
    typ, stack = None, None
    if os.path.exists(pkg):
        stack = "ts"
        t = open(pkg, encoding="utf-8", errors="ignore").read().lower()
        if '"vite"' in t or '"react"' in t or '"next"' in t:
            typ = "web"
        elif '"fastify"' in t or '"express"' in t:
            typ = "api"
        elif '"tsup"' in t or '"main"' in t and '"files"' in t:
            typ = "lib"
        else:
            typ = "lib"
    elif os.path.exists(py):
        stack = "py"
        t = open(py, encoding="utf-8", errors="ignore").read().lower()
        if "fastapi" in t or "flask" in t or "django" in t:
            typ = "api"
        elif "polars" in t or "pandas" in t or "jupyter" in t:
            typ = "data"
        elif "project.scripts" in t or "console_scripts" in t:
            typ = "cli"
        else:
            typ = "lib"
    return typ, stack


FW_MARKERS = {
    "package.json": {
        "next": "next", "nuxt": "nuxt", "@angular/core": "angular", "svelte": "vite-svelte",
        "astro": "astro", "@remix-run/react": "remix", "solid-js": "vite-solid",
        "preact": "vite-preact", "lit": "vite-lit", "@builder.io/qwik": "qwik",
        "vue": "vite-vue", "react": "vite-react", "gatsby": "gatsby", "ember-source": "ember",
        "@nestjs/core": "nest", "fastify": "fastify", "express": "express", "koa": "koa",
        "@hapi/hapi": "hapi", "restify": "restify", "hono": "hono", "elysia": "elysia",
        "tsup": "tsup", "commander": "commander", "ink": "ink",
    },
    "pyproject.toml": {
        "fastapi": "fastapi", "django": "django", "flask": "flask", "litestar": "litestar",
        "starlette": "starlette", "quart": "quart", "sanic": "sanic", "tornado": "tornado",
        "pyramid": "pyramid", "falcon": "falcon", "streamlit": "streamlit",
        "gradio": "gradio", "typer": "typer", "click": "click", "polars": "polars",
        "pandas": "pandas", "scikit-learn": "sklearn", "torch": "pytorch",
        "transformers": "transformers", "dask": "dask", "jupyterlab": "jupyter",
    },
    "go.mod": {
        "gin-gonic/gin": "gin", "labstack/echo": "echo", "gofiber/fiber": "fiber",
        "go-chi/chi": "chi", "spf13/cobra": "cobra", "urfave/cli": "urfave-cli",
    },
    "Cargo.toml": {
        "axum": "axum", "actix-web": "actix", "rocket": "rocket", "warp": "warp",
        "poem": "poem", "clap": "clap", "ratatui": "ratatui",
    },
    "composer.json": {"laravel/framework": "laravel", "symfony/framework-bundle": "symfony",
                      "slim/slim": "slim"},
    "Gemfile": {"rails": "rails", "sinatra": "sinatra", "grape": "grape", "hanami": "hanami"},
    "mix.exs": {"phoenix": "phoenix"},
    "pubspec.yaml": {"flutter": "flutter"},
}


def detect_framework(root):
    """tebak framework dari dependency yang sudah ada di proyek."""
    for rel, marks in FW_MARKERS.items():
        path = os.path.join(root, rel)
        if not os.path.exists(path):
            continue
        try:
            body = open(path, encoding="utf-8", errors="ignore").read().lower()
        except Exception:
            continue
        for needle, fid in marks.items():
            if needle.lower() in body:
                return fid
    for f in os.listdir(root):
        if f.endswith(".csproj"):
            body = open(os.path.join(root, f), encoding="utf-8", errors="ignore").read().lower()
            if "microsoft.net.sdk.web" in body:
                return "dotnet-webapi"
            return "dotnet-classlib"
    return None


def cmd_adopt(a):
    root = os.path.abspath(a[0] if a else ".")
    name = a[a.index("--name") + 1] if "--name" in a else os.path.basename(root)
    typ, stack = detect(root)
    if not typ:
        sys.exit("tidak terdeteksi package.json/pyproject.toml — pakai `new` untuk proyek baru")
    slug = slugify(name)
    pkg = slug.replace("-", "_") if stack == "py" else slug
    gates = gates_for(typ, stack)
    fw = detect_framework(root)
    e = FC.get(fw) if fw else None
    if e:
        gates = ["structure"] + [g for g in ("lint", "types", "test", "build")
                                 if g in e["gates"]] + ["security", "docs"]
    subs = dict(name=name, desc=f"Proyek {name} (diadopsi)", slug=slug, pkg=pkg, year=YEAR,
                tree="(lihat isi repo)")
    added = []

    def add_if_missing(rel, content):
        target = os.path.join(root, rel)
        if os.path.exists(target):
            return
        w(target, sub(content, **subs))
        added.append(rel)

    add_if_missing("AGENTS.md", AGENTS)
    add_if_missing("TODO.md", TODO.replace("__MERMAID__", MERMAID)
                   .replace("__TYPED_TODO__", TYPED_TODO_PY if stack == "py" else TYPED_TODO_TS))
    add_if_missing("docs/adr/0001-initial-architecture.md", ADR1)
    add_if_missing("SECURITY.md", SECURITY)
    add_if_missing(".editorconfig", EDITORCONFIG)
    state = {"name": name, "slug": slug, "type": typ, "stack": stack, "package": pkg,
             "created": time.strftime("%Y-%m-%dT%H:%M:%S"), "gates": gates, "schema": 1,
             "adopted": True}
    if e:
        state.update({"framework": fw, "lang": e["lang"], "gate_cmds": e["gates"]})
    w(os.path.join(root, ".mamat/project.json"), json.dumps(state, indent=2, ensure_ascii=False))
    gen_skill(root, name, f"Proyek {name}", typ, stack, slug, gates)
    print(f"✅ adopsi: {root} → {typ}/{stack}"
          + (f" · framework={fw}" if e else "") + f" · gate={len(gates)}")
    if added:
        print("   ditambah:", ", ".join(added))
    print("   berikutnya: project-forge status .")


def cmd_verify(a):
    root = os.path.abspath(a[0] if a and not a[0].startswith("--") else ".")
    st = read_state(root)
    if not st:
        sys.exit("bukan proyek project-forge (tidak ada .mamat/project.json)")
    results = []
    for gate in st.get("gates", []):
        status, note = run_gate(root, gate, st)
        results.append({"gate": gate, "status": status, "note": note})
        print(f"{ICON[status]} {gate:<10} {note}", flush=True)
    fails = [r for r in results if r["status"] == "FAIL"]
    skips = [r for r in results if r["status"] == "SKIP"]
    out = {"project": st.get("name"), "root": root, "pass": len(results) - len(fails) - len(skips),
           "fail": len(fails), "skip": len(skips), "gates": results,
           "ok": not fails}
    if flag(a, "--json"):
        print(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"\n{len(results) - len(fails) - len(skips)} pass · {len(fails)} fail · {len(skips)} skip "
          f"→ {'SIAP' if not fails else 'BELUM SIAP'}")
    sys.exit(0 if not fails else 1)


def cmd_status(a):
    root = os.path.abspath(a[0] if a else ".")
    st = read_state(root)
    if not st:
        sys.exit("bukan proyek project-forge")
    pending = []
    for gate in st.get("gates", []):
        status, note = run_gate(root, gate, st)
        if status != "PASS":
            pending.append((gate, status, note))
    print(f"{st['name']} · {st['type']}/{st['stack']} · {len(st.get('gates', []))} gate")
    if not pending:
        print("semua gate PASS — boleh lanjut rilis")
        return
    for gate, status, note in pending[:4]:
        print(f"{ICON[status]} {gate}: {note}")
    if st.get("framework"):
        nxt = {"structure": "lengkapi berkas wajib", "docs": "update README/TODO/skill",
               "security": "hapus secret dari kode"}
        for g in ("lint", "types", "test", "build"):
            nxt[g] = str((st.get("gate_cmds") or {}).get(g, "project-forge verify ."))
    else:
        nxt = {"structure": "lengkapi berkas wajib", "docs": "update README/TODO/skill",
               "security": "hapus secret dari kode", "lint": "make lint",
               "types": "make typecheck", "test": "make test", "build": "make build"}
    first_fail = next((g for g, stt, _ in pending if stt == "FAIL"), None)
    if first_fail:
        print("berikutnya:", nxt.get(first_fail, "perbaiki gate pertama"))
    else:
        print("semua gate sisanya SKIP (toolchain belum ada) — tidak ada yang gagal")


def cmd_skill(a):
    root = os.path.abspath(a[0] if a else ".")
    st = read_state(root)
    if not st:
        sys.exit("bukan proyek project-forge")
    gen_skill(root, st["name"], "", st["type"], st["stack"], st["slug"], st.get("gates", []))
    p = os.path.join(root, f".opencode/skills/{st['slug']}/SKILL.md")
    print("skill:", p, f"({len(open(p).read().splitlines())} baris)")


def cmd_diagram(a):
    print(MERMAID)


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        return
    cmd, rest = a[0], a[1:]
    table = {"new": cmd_new, "adopt": cmd_adopt, "verify": cmd_verify, "status": cmd_status,
             "skill": cmd_skill, "diagram": cmd_diagram, "gates": cmd_gates,
             "stacks": cmd_stacks, "frameworks": cmd_frameworks, "search": cmd_frameworks}
    fn = table.get(cmd)
    if not fn:
        sys.exit(f"perintah tidak dikenal: {cmd}\n\n{__doc__}")
    fn(rest)


if __name__ == "__main__":
    main()
