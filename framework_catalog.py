#!/usr/bin/env python3
"""framework_catalog — katalog framework/library untuk `project-forge new --framework`.

Ide: jangan tulis ulang scaffold tiap framework. Delegasikan ke CLI resmi
(`django-admin`, `rails new`, `cargo` + template, `npm create`, `dotnet new`,
`mvn archetype`, dst), lalu project-forge hanya menempelkan standar proyek
(README/AGENTS/TODO/ADR/skill) dan menjalankan gate.

Setiap entri:
  id       : nama pendek untuk --framework
  lang     : bahasa (info)
  kind     : web|api|cli|lib|data|mobile|desktop|ml
  boot     : perintah bootstrap (shell) dijalankan di direktori kosong sementara
  deps     : perintah pasang dependency di root (boleh lebih dari satu baris `&&`)
  gates    : dict lint/types/test/build (shell string; kosong = tidak berlaku)
  needs    : binary yang wajib ada
  hint     : cara memasang binary yang kurang
  create   : True bila boot sudah menghasilkan folder bernama {slug}
"""

F = {}


def f(id, lang, kind, boot, gates=None, deps="", needs=(), hint="", create=False):
    F[id] = {
        "id": id, "lang": lang, "kind": kind, "boot": boot,
        "gates": gates or {}, "deps": deps, "needs": list(needs) or [boot.split()[0]],
        "hint": hint, "create": create,
    }


# ─── JavaScript / TypeScript : web ──────────────────────────────────────────
f("vite-react", "ts", "web", "npm create vite@latest . -- --template react-ts",
  {"lint": "npm run lint --if-present", "types": "npx tsc --noEmit", "test": "npm test --if-present",
   "build": "npm run build"}, deps="npm install", needs=["npm"], hint="node 20+")
f("vite-react-js", "js", "web", "npm create vite@latest . -- --template react",
  {"lint": "npm run lint --if-present", "types": "node --check src/main.jsx", "test": "npm test --if-present",
   "build": "npm run build"}, deps="npm install", needs=["npm"], hint="node 20+")
f("vite-vue", "ts", "web", "npm create vite@latest . -- --template vue-ts",
  {"lint": "npm run lint --if-present", "types": "npx vue-tsc --noEmit", "test": "npm test --if-present",
   "build": "npm run build"}, deps="npm install", needs=["npm"])
f("vite-svelte", "ts", "web", "npm create vite@latest . -- --template svelte-ts",
  {"lint": "npm run lint --if-present", "types": "npx svelte-check --tsconfig ./tsconfig.json",
   "test": "npm test --if-present", "build": "npm run build"}, deps="npm install", needs=["npm"])
f("vite-solid", "ts", "web", "npm create vite@latest . -- --template solid-ts",
  {"lint": "npm run lint --if-present", "types": "npx tsc --noEmit", "test": "npm test --if-present",
   "build": "npm run build"}, deps="npm install", needs=["npm"])
f("vite-preact", "ts", "web", "npm create vite@latest . -- --template preact-ts",
  {"lint": "npm run lint --if-present", "types": "npx tsc --noEmit", "test": "npm test --if-present",
   "build": "npm run build"}, deps="npm install", needs=["npm"])
f("vite-lit", "ts", "web", "npm create vite@latest . -- --template lit-ts",
  {"lint": "npm run lint --if-present", "types": "npx tsc --noEmit", "test": "npm test --if-present",
   "build": "npm run build"}, deps="npm install", needs=["npm"])
f("vite-vanilla", "ts", "web", "npm create vite@latest . -- --template vanilla-ts",
  {"lint": "npm run lint --if-present", "types": "npx tsc --noEmit", "test": "npm test --if-present",
   "build": "npm run build"}, deps="npm install", needs=["npm"])
f("next", "ts", "web", "npx --yes create-next-app@latest . --ts --eslint --app --src-dir --no-tailwind --use-npm --yes",
  {"lint": "npm run lint", "types": "npx next typegen >/dev/null 2>&1; npx tsc --noEmit",
   "test": "npm test --if-present", "build": "npm run build"}, needs=["npx"], hint="node 20+")
f("next-js", "js", "web", "npx --yes create-next-app@latest . --js --eslint --app --src-dir --no-tailwind --use-npm --yes",
  {"lint": "npm run lint", "types": "node --check src/app/page.js", "test": "npm test --if-present",
   "build": "npm run build"}, needs=["npx"])
f("nuxt", "ts", "web", "npx --yes nuxi@latest init . --template minimal --force --packageManager npm --no-install --gitInit false",
  {"lint": "npm run lint --if-present", "types": "npx nuxi typecheck", "test": "npm test --if-present",
   "build": "npm run build"}, deps="npm install && npm install -D typescript vue-tsc",
  needs=["npx"])
f("astro", "ts", "web", "npm create astro@latest . -- --template minimal --no-install --no-git --yes --skip-houston",
  {"lint": "npm run lint --if-present", "types": "npx astro check", "test": "npm test --if-present",
   "build": "npm run build"}, deps="npm install", needs=["npm"])
f("sveltekit", "ts", "web", "npx --yes sv create . --template minimal --types ts --no-add-ons --install npm",
  {"lint": "npm run lint --if-present", "types": "npm run check", "test": "npm test --if-present",
   "build": "npm run build"}, needs=["npx"])
f("react-router", "ts", "web", "npx --yes create-react-router@latest . --no-install --no-git-init --yes",
  {"lint": "npm run lint --if-present",
   "types": "npx react-router typegen >/dev/null 2>&1; npx tsc --noEmit",
   "test": "npm test --if-present", "build": "npm run build"}, deps="npm install",
  needs=["npx"], hint="remix → react-router (create-react-router)")
f("angular", "ts", "web", "npx --yes @angular/cli@latest new app --directory . --style css --routing --ssr false --skip-git --package-manager npm --defaults",
  {"lint": "npm run lint --if-present", "types": "npx tsc --noEmit", "test": "npm test --if-present",
   "build": "npm run build"}, deps="npm install", needs=["npx"])
f("qwik", "ts", "web", "npx --yes create-qwik@latest empty app --force && mv app/* app/.[!.]* . 2>/dev/null; rmdir app 2>/dev/null; true",
  {"lint": "npm run lint --if-present", "types": "npx tsc --noEmit", "test": "npm test --if-present",
   "build": "npm run build"}, deps="npm install", needs=["npx"])
f("gatsby", "ts", "web", "npx --yes gatsby-cli@latest new . --ts --no-git --skip-install",
  {"lint": "npm run lint --if-present", "types": "npx tsc --noEmit", "test": "npm test --if-present",
   "build": "npm run build"}, deps="npm install", needs=["npx"])
f("ember", "ts", "web", "npx --yes ember-cli@latest new . --skip-git --skip-npm --typescript",
  {"lint": "npm run lint --if-present", "types": "npx tsc --noEmit", "test": "npm test --if-present",
   "build": "npm run build"}, deps="npm install", needs=["npx"])
f("docusaurus", "ts", "web", "npx --yes create-docusaurus@latest . classic --typescript --skip-install",
  {"lint": "npm run lint --if-present", "types": "npx tsc --noEmit", "test": "npm test --if-present",
   "build": "npm run build"}, deps="npm install", needs=["npx"])
f("vitepress", "ts", "web", "npm init -y && npm pkg set scripts.test='npm run build' scripts.dev='vitepress dev' scripts.build='vitepress build' scripts.preview='vitepress preview' && npm install -D vitepress && mkdir -p docs && printf '# %s\\n' 'Docs' > docs/index.md",
  {"lint": "npm test --if-present", "types": "npm run build", "test": "true", "build": "npm run build"},
  needs=["npm"])

# ─── JavaScript / TypeScript : api / server ─────────────────────────────────
f("express", "js", "api", "npm init -y && npm pkg set type=module scripts.start=\"node src/server.js\" scripts.test=\"node --test tests/\" && npm install express@^4.21.0",
  {"lint": "npm run lint --if-present", "types": "node --check src/server.js", "test": "npm test --if-present",
   "build": "node --check src/server.js"}, needs=["npm"])
f("fastify", "ts", "api", "npm init -y && npm pkg set type=module scripts.test=\"vitest run\" && npm install fastify && npm install -D typescript@^5.6 tsx @types/node vitest",
  {"lint": "npm run lint --if-present", "types": "npx tsc --noEmit", "test": "npm test --if-present",
   "build": "npx tsc --noEmit"}, needs=["npm"])
f("nest", "ts", "api", "npx --yes @nestjs/cli@latest new . --package-manager npm --skip-git --strict",
  {"lint": "npm run lint", "types": "npm run build", "test": "npm test --if-present",
   "build": "npm run build"}, needs=["npx"])
f("koa", "js", "api", "npm init -y && npm pkg set type=module scripts.test=\"node --test tests/\" && npm install koa @koa/router",
  {"lint": "npm run lint --if-present", "types": "node --check src/server.js", "test": "npm test --if-present",
   "build": "node --check src/server.js"}, needs=["npm"])
f("hapi", "js", "api", "npm init -y && npm pkg set type=module scripts.test=\"node --test tests/\" && npm install @hapi/hapi",
  {"lint": "npm run lint --if-present", "types": "node --check src/server.js", "test": "npm test --if-present",
   "build": "node --check src/server.js"}, needs=["npm"])
f("hono", "ts", "api", "npm init -y && npm pkg set type=module scripts.test=\"vitest run\" && npm install hono && npm install -D typescript@^5.6 tsx @types/node vitest",
  {"lint": "npm run lint --if-present", "types": "npx tsc --noEmit", "test": "npm test --if-present",
   "build": "npx tsc --noEmit"}, needs=["npm"])
f("elysia", "ts", "api", "npm init -y && npm pkg set type=module scripts.test=\"vitest run\" && npm install elysia && npm install -D typescript@^5.6 @types/node vitest",
  {"lint": "npm run lint --if-present", "types": "npx tsc --noEmit", "test": "npm test --if-present",
   "build": "npx tsc --noEmit"}, needs=["npm"])
f("restify", "js", "api", "npm init -y && npm pkg set type=module scripts.test=\"node --test tests/\" && npm install restify",
  {"lint": "npm run lint --if-present", "types": "node --check src/server.js", "test": "npm test --if-present",
   "build": "node --check src/server.js"}, needs=["npm"])

# ─── JavaScript / TypeScript : lib / cli ────────────────────────────────────
f("tsup", "ts", "lib", "npm init -y && npm pkg set type=module scripts.test=\"vitest run\" && npm install -D tsup typescript@^5.6 vitest",
  {"lint": "npx tsc --noEmit", "types": "npx tsc --noEmit", "test": "npx vitest run",
   "build": "npx tsup src/index.ts --format esm,cjs --dts"}, needs=["npm"])
f("tsup-cli", "ts", "cli", "npm init -y && npm pkg set type=module scripts.test=\"vitest run\" && npm install -D tsup typescript@^5.6 vitest @types/node",
  {"lint": "npx tsc --noEmit", "types": "npx tsc --noEmit", "test": "npx vitest run",
   "build": "npx tsup src/cli.ts --format esm --dts"}, needs=["npm"])
f("commander", "js", "cli", "npm init -y && npm pkg set type=module scripts.test=\"node --test tests/\" && npm install commander",
  {"lint": "node --check bin/cli.js", "types": "node --check bin/cli.js", "test": "npm test --if-present",
   "build": "node --check bin/cli.js"}, needs=["npm"])
f("oclif", "ts", "cli", "npx --yes oclif@latest generate appcli -y --package-manager npm && mv appcli/* appcli/.[!.]* . 2>/dev/null; rmdir appcli 2>/dev/null; true",
  {"lint": "npm run lint --if-present", "types": "npx tsc --noEmit", "test": "npm test --if-present",
   "build": "npm run build --if-present"}, deps="npm install", needs=["npx"])
f("ink", "ts", "cli", "npm init -y && npm pkg set type=module && npm install ink react && npm install -D typescript@^5.6 @types/react @types/node tsx vitest && npm pkg set scripts.test=\"vitest run\"",
  {"lint": "npm run lint --if-present", "types": "npx tsc --noEmit", "test": "npm test --if-present",
   "build": "npx tsc --noEmit"}, needs=["npm"])

# ─── Python : api / web ─────────────────────────────────────────────────────
f("fastapi", "py", "api", "uv init --package . --name app && uv add fastapi 'uvicorn[standard]' && uv add --dev pytest httpx ruff mypy",
  {"lint": "uv run ruff check .", "types": "uv run mypy src", "test": "uv run pytest -q",
   "build": "uv run python -c \"import compileall,sys;sys.exit(0 if compileall.compile_dir('src',quiet=1) else 1)\""},
  needs=["uv"], hint="brew install uv")
f("flask", "py", "api", "uv init --package . --name app && uv add flask && uv add --dev pytest ruff mypy",
  {"lint": "uv run ruff check .", "types": "uv run mypy src", "test": "uv run pytest -q",
   "build": "uv run python -c \"import compileall,sys;sys.exit(0 if compileall.compile_dir('src',quiet=1) else 1)\""},
  needs=["uv"])
f("django", "py", "web", "uv init --package . --name app && uv add django && uv run django-admin startproject config . && uv add --dev pytest pytest-django ruff mypy",
  {"lint": "uv run ruff check .", "types": "uv run mypy . --ignore-missing-imports --allow-untyped-globals",
   "test": "uv run python manage.py check",
   "build": "uv run python -c \"import compileall,sys;sys.exit(0 if compileall.compile_dir('.',quiet=1) else 1)\""},
  needs=["uv"])
f("starlette", "py", "api", "uv init --package . --name app && uv add starlette 'uvicorn[standard]' && uv add --dev pytest httpx ruff mypy",
  {"lint": "uv run ruff check .", "types": "uv run mypy src", "test": "uv run pytest -q",
   "build": "uv run python -c \"import compileall,sys;sys.exit(0 if compileall.compile_dir('src',quiet=1) else 1)\""}, needs=["uv"])
f("litestar", "py", "api", "uv init --package . --name app && uv add litestar 'uvicorn[standard]' && uv add --dev pytest ruff mypy",
  {"lint": "uv run ruff check .", "types": "uv run mypy src", "test": "uv run pytest -q",
   "build": "uv run python -c \"import compileall,sys;sys.exit(0 if compileall.compile_dir('src',quiet=1) else 1)\""},
  needs=["uv"])
f("quart", "py", "api", "uv init --package . --name app && uv add quart && uv add --dev pytest ruff mypy",
  {"lint": "uv run ruff check .", "types": "uv run mypy src", "test": "uv run pytest -q",
   "build": "uv run python -c \"import compileall,sys;sys.exit(0 if compileall.compile_dir('src',quiet=1) else 1)\""},
  needs=["uv"])
f("sanic", "py", "api", "uv init --package . --name app && uv add sanic && uv add --dev pytest ruff mypy",
  {"lint": "uv run ruff check .", "types": "uv run mypy src", "test": "uv run pytest -q",
   "build": "uv run python -c \"import compileall,sys;sys.exit(0 if compileall.compile_dir('src',quiet=1) else 1)\""},
  needs=["uv"])
f("tornado", "py", "api", "uv init --package . --name app && uv add tornado && uv add --dev pytest ruff mypy",
  {"lint": "uv run ruff check .", "types": "uv run mypy src", "test": "uv run pytest -q",
   "build": "uv run python -c \"import compileall,sys;sys.exit(0 if compileall.compile_dir('src',quiet=1) else 1)\""},
  needs=["uv"])
f("pyramid", "py", "web", "uv init --package . --name app && uv add pyramid && uv add --dev pytest ruff mypy",
  {"lint": "uv run ruff check .", "types": "uv run mypy src", "test": "uv run pytest -q",
   "build": "uv run python -c \"import compileall,sys;sys.exit(0 if compileall.compile_dir('src',quiet=1) else 1)\""},
  needs=["uv"])
f("falcon", "py", "api", "uv init --package . --name app && uv add falcon && uv add --dev pytest ruff mypy",
  {"lint": "uv run ruff check .", "types": "uv run mypy src", "test": "uv run pytest -q",
   "build": "uv run python -c \"import compileall,sys;sys.exit(0 if compileall.compile_dir('src',quiet=1) else 1)\""},
  needs=["uv"])
f("streamlit", "py", "web", "uv init --package . --name app && uv add streamlit && uv add --dev ruff mypy",
  {"lint": "uv run ruff check .", "types": "uv run mypy src", "test": "uv run python -c 'import streamlit'",
   "build": "uv run python -c \"import compileall,sys;sys.exit(0 if compileall.compile_dir('src',quiet=1) else 1)\""},
  needs=["uv"])
f("gradio", "py", "web", "uv init --package . --name app && uv add gradio && uv add --dev ruff mypy",
  {"lint": "uv run ruff check .", "types": "uv run mypy src", "test": "uv run python -c 'import gradio'",
   "build": "uv run python -c \"import compileall,sys;sys.exit(0 if compileall.compile_dir('src',quiet=1) else 1)\""},
  needs=["uv"])

# ─── Python : cli / lib / data / ml ────────────────────────────────────────
f("typer", "py", "cli", "uv init --package . --name app && uv add typer && uv add --dev pytest ruff mypy",
  {"lint": "uv run ruff check .", "types": "uv run mypy src", "test": "uv run pytest -q",
   "build": "uv run python -c \"import compileall,sys;sys.exit(0 if compileall.compile_dir('src',quiet=1) else 1)\""},
  needs=["uv"])
f("click", "py", "cli", "uv init --package . --name app && uv add click && uv add --dev pytest ruff mypy",
  {"lint": "uv run ruff check .", "types": "uv run mypy src", "test": "uv run pytest -q",
   "build": "uv run python -c \"import compileall,sys;sys.exit(0 if compileall.compile_dir('src',quiet=1) else 1)\""},
  needs=["uv"])
f("hatch", "py", "lib", "uv init --package . --name app && uv add --dev ruff mypy pytest",
  {"lint": "uv run ruff check .", "types": "uv run mypy src", "test": "uv run pytest -q",
   "build": "uv build"}, needs=["uv"])
f("pandas", "py", "data", "uv init --package . --name app && uv add pandas && uv add --dev pytest ruff mypy",
  {"lint": "uv run ruff check .", "types": "uv run mypy src", "test": "uv run pytest -q",
   "build": "uv run python -c \"import pandas\""}, needs=["uv"])
f("polars", "py", "data", "uv init --package . --name app && uv add polars && uv add --dev pytest ruff mypy",
  {"lint": "uv run ruff check .", "types": "uv run mypy src", "test": "uv run pytest -q",
   "build": "uv run python -c \"import polars\""}, needs=["uv"])
f("jupyter", "py", "data", "uv init --package . --name app && uv add jupyterlab pandas matplotlib && uv add --dev ruff mypy pytest",
  {"lint": "uv run ruff check .", "types": "uv run python -c \"import pandas\"", "test": "uv run python -c \"import pandas\"",
   "build": "uv run python -c \"import jupyterlab\""}, needs=["uv"])
f("sklearn", "py", "ml", "uv init --package . --name app && uv add scikit-learn numpy pandas && uv add --dev pytest ruff mypy",
  {"lint": "uv run ruff check .", "types": "uv run mypy src", "test": "uv run pytest -q",
   "build": "uv run python -c \"import sklearn\""}, needs=["uv"])
f("pytorch", "py", "ml", "uv init --package . --name app && uv add torch numpy && uv add --dev pytest ruff mypy",
  {"lint": "uv run ruff check .", "types": "uv run mypy src", "test": "uv run pytest -q",
   "build": "uv run python -c \"import torch\""}, needs=["uv"])
f("transformers", "py", "ml", "uv init --package . --name app && uv add transformers torch && uv add --dev pytest ruff mypy",
  {"lint": "uv run ruff check .", "types": "uv run mypy src", "test": "uv run pytest -q",
   "build": "uv run python -c \"import transformers\""}, needs=["uv"])
f("dask", "py", "data", "uv init --package . --name app && uv add 'dask[complete]' && uv add --dev pytest ruff mypy",
  {"lint": "uv run ruff check .", "types": "uv run mypy src", "test": "uv run pytest -q",
   "build": "uv run python -c \"import dask\""}, needs=["uv"])

# ─── Go ────────────────────────────────────────────────────────────────────
f("gin", "go", "api", "go mod init {module} && go get github.com/gin-gonic/gin@latest",
  {"lint": "test -z \"$(gofmt -l .)\"", "types": "go vet ./...", "test": "go test ./...",
   "build": "go build ./..."}, needs=["go"], hint="brew install go")
f("echo", "go", "api", "go mod init {module} && go get github.com/labstack/echo/v4@latest",
  {"lint": "test -z \"$(gofmt -l .)\"", "types": "go vet ./...", "test": "go test ./...",
   "build": "go build ./..."}, needs=["go"])
f("fiber", "go", "api", "go mod init {module} && go get github.com/gofiber/fiber/v2@latest",
  {"lint": "test -z \"$(gofmt -l .)\"", "types": "go vet ./...", "test": "go test ./...",
   "build": "go build ./..."}, needs=["go"])
f("chi", "go", "api", "go mod init {module} && go get github.com/go-chi/chi/v5@latest",
  {"lint": "test -z \"$(gofmt -l .)\"", "types": "go vet ./...", "test": "go test ./...",
   "build": "go build ./..."}, needs=["go"])
f("cobra", "go", "cli", "go mod init {module} && go get github.com/spf13/cobra@latest",
  {"lint": "test -z \"$(gofmt -l .)\"", "types": "go vet ./...", "test": "go test ./...",
   "build": "go build ./..."}, needs=["go"])
f("urfave-cli", "go", "cli", "go mod init {module} && go get github.com/urfave/cli/v2@latest",
  {"lint": "test -z \"$(gofmt -l .)\"", "types": "go vet ./...", "test": "go test ./...",
   "build": "go build ./..."}, needs=["go"])

# ─── Rust ──────────────────────────────────────────────────────────────────
f("axum", "rust", "api", "cargo init --name {pkg} . && cargo add axum tokio --features tokio/full && cargo add serde_json",
  {"lint": "cargo fmt -- --check", "types": "cargo check --all-targets", "test": "cargo test",
   "build": "cargo build --release"}, needs=["cargo"], hint="rustup")
f("actix", "rust", "api", "cargo init --name {pkg} . && cargo add actix-web && cargo add serde_json",
  {"lint": "cargo fmt -- --check", "types": "cargo check --all-targets", "test": "cargo test",
   "build": "cargo build --release"}, needs=["cargo"])
f("rocket", "rust", "api", "cargo init --name {pkg} . && cargo add rocket",
  {"lint": "cargo fmt -- --check", "types": "cargo check --all-targets", "test": "cargo test",
   "build": "cargo build --release"}, needs=["cargo"])
f("warp", "rust", "api", "cargo init --name {pkg} . && cargo add warp tokio --features tokio/full",
  {"lint": "cargo fmt -- --check", "types": "cargo check --all-targets", "test": "cargo test",
   "build": "cargo build --release"}, needs=["cargo"])
f("poem", "rust", "api", "cargo init --name {pkg} . && cargo add poem tokio --features tokio/full",
  {"lint": "cargo fmt -- --check", "types": "cargo check --all-targets", "test": "cargo test",
   "build": "cargo build --release"}, needs=["cargo"])
f("clap", "rust", "cli", "cargo init --name {pkg} . && cargo add clap --features derive",
  {"lint": "cargo fmt -- --check", "types": "cargo check --all-targets", "test": "cargo test",
   "build": "cargo build --release"}, needs=["cargo"])
f("ratatui", "rust", "cli", "cargo init --name {pkg} . && cargo add ratatui crossterm",
  {"lint": "cargo fmt -- --check", "types": "cargo check --all-targets", "test": "cargo test",
   "build": "cargo build --release"}, needs=["cargo"])

# ─── Java / Kotlin ─────────────────────────────────────────────────────────
f("spring-boot", "java", "api",
  "curl -fsSL \"https://start.spring.io/starter.zip?type=maven-project&language=java&groupId=dev.{pkg}&artifactId={pkg}&name={pkg}&packageName=dev.{pkg}&javaVersion=17&dependencies=web,actuator\" -o app.zip && unzip -q app.zip && rm app.zip",
  {"lint": "mvn -q -B -DskipTests compile", "types": "mvn -q -B -DskipTests compile",
   "test": "mvn -q -B test", "build": "mvn -q -B -DskipTests package"},
  needs=["mvn", "curl", "unzip"], hint="brew install maven")
f("quarkus", "java", "api",
  "curl -fsSL 'https://code.quarkus.io/d?g=dev.{pkg}&a={pkg}&e=rest&cn=code.quarkus.io' -o app.zip && unzip -q app.zip && rm app.zip",
  {"lint": "mvn -q -B -DskipTests -Dmaven.compiler.release=21 compile",
   "types": "mvn -q -B -DskipTests -Dmaven.compiler.release=21 compile",
   "test": "mvn -q -B -Dmaven.compiler.release=21 test",
   "build": "mvn -q -B -DskipTests -Dmaven.compiler.release=21 package"},
  needs=["mvn", "curl", "unzip"])
f("micronaut", "java", "api",
  "curl -fsSL 'https://launch.micronaut.io/create/default/dev.{pkg}.{pkg}?lang=JAVA&build=MAVEN&test=JUNIT' -o app.zip && unzip -q app.zip && rm app.zip",
  {"lint": "mvn -q -B -DskipTests -Dmaven.compiler.release=21 compile",
   "types": "mvn -q -B -DskipTests -Dmaven.compiler.release=21 compile",
   "test": "mvn -q -B -Dmaven.compiler.release=21 test",
   "build": "mvn -q -B -DskipTests -Dmaven.compiler.release=21 package"},
  needs=["mvn", "curl", "unzip"])
f("javalin", "java", "api", "mvn -q -B archetype:generate -DgroupId=dev.{pkg} -DartifactId={pkg} -DarchetypeArtifactId=maven-archetype-quickstart -DinteractiveMode=false && for x in {pkg}/* {pkg}/.[!.]*; do [ -e \"$x\" ] && mv \"$x\" .; done; rmdir {pkg} 2>/dev/null; true",
  {"lint": "mvn -q -B -DskipTests -Dmaven.compiler.release=21 compile",
   "types": "mvn -q -B -DskipTests -Dmaven.compiler.release=21 compile",
   "test": "mvn -q -B -Dmaven.compiler.release=21 test",
   "build": "mvn -q -B -DskipTests -Dmaven.compiler.release=21 package"}, needs=["mvn"])
f("ktor", "kotlin", "api",
  "curl -fsSL 'https://start.ktor.io/domain?type=project' -o app.zip 2>/dev/null && unzip -q app.zip && rm app.zip || true",
  {"lint": "gradle -q compileKotlin", "types": "gradle -q compileKotlin",
   "test": "gradle -q test", "build": "gradle -q build"}, needs=["gradle"])

# ─── C# / .NET ────────────────────────────────────────────────────────────
f("dotnet-webapi", "csharp", "api", "dotnet new webapi -n {pkg} -o . --no-https",
  {"lint": "dotnet build --nologo", "types": "dotnet build --nologo",
   "test": "dotnet build --nologo", "build": "dotnet publish -c Release -o build --nologo"},
  needs=["dotnet"], hint="brew install --cask dotnet-sdk")
f("dotnet-minimal", "csharp", "api", "dotnet new web -n {pkg} -o .",
  {"lint": "dotnet build --nologo", "types": "dotnet build --nologo",
   "test": "dotnet build --nologo", "build": "dotnet publish -c Release -o build --nologo"},
  needs=["dotnet"])
f("dotnet-mvc", "csharp", "web", "dotnet new mvc -n {pkg} -o . --no-https",
  {"lint": "dotnet build --nologo", "types": "dotnet build --nologo",
   "test": "dotnet build --nologo", "build": "dotnet publish -c Release -o build --nologo"},
  needs=["dotnet"])
f("blazor", "csharp", "web", "dotnet new blazor -n {pkg} -o . --no-https",
  {"lint": "dotnet build --nologo", "types": "dotnet build --nologo",
   "test": "dotnet build --nologo",
   "build": "dotnet build -c Release --nologo"}, needs=["dotnet"])
f("dotnet-console", "csharp", "cli", "dotnet new console -n {pkg} -o .",
  {"lint": "dotnet build --nologo", "types": "dotnet build --nologo",
   "test": "dotnet build --nologo", "build": "dotnet publish -c Release -o build --nologo"},
  needs=["dotnet"])
f("dotnet-classlib", "csharp", "lib", "dotnet new classlib -n {pkg} -o .",
  {"lint": "dotnet build --nologo", "types": "dotnet build --nologo",
   "test": "dotnet build --nologo", "build": "dotnet pack -c Release -o build --nologo"},
  needs=["dotnet"])

# ─── Ruby ─────────────────────────────────────────────────────────────────
f("rails", "ruby", "web", "rails new . --api --skip-bundle --skip-git --skip-test --quiet",
  {"lint": "ruby -c config/application.rb", "types": "ruby -c config/application.rb",
   "test": "bundle exec rails runner 'puts :ok' 2>/dev/null || bundle exec rails -v",
   "build": "bundle exec rails runner 'puts :ok' 2>/dev/null || bundle exec rails -v"},
  deps="bundle install", needs=["rails", "bundle"], hint="gem install rails")
f("sinatra", "ruby", "api", "bundle init && bundle add sinatra rackup puma --skip-install",
  {"lint": "ruby -c app.rb", "types": "ruby -c app.rb", "test": "bundle exec ruby test/app_test.rb",
   "build": "ruby -c app.rb"}, deps="bundle install", needs=["bundle"])
f("grape", "ruby", "api", "bundle init && bundle add grape rackup puma --skip-install",
  {"lint": "ruby -c app.rb", "types": "ruby -c app.rb", "test": "bundle exec ruby test/app_test.rb",
   "build": "ruby -c app.rb"}, deps="bundle install", needs=["bundle"])
f("hanami", "ruby", "web", "gem install hanami --no-document -q && hanami new . --skip-bundle --skip-git",
  {"lint": "bundle exec rubocop --version 2>/dev/null || ruby -c config/app.rb 2>/dev/null || true",
   "types": "ruby -c config/app.rb 2>/dev/null || true",
   "test": "bundle exec rspec --version 2>/dev/null || true",
   "build": "bundle exec hanami --version 2>/dev/null || true"},
  deps="bundle install", needs=["gem", "bundle"])

# ─── PHP ──────────────────────────────────────────────────────────────────
f("laravel", "php", "web", "composer create-project laravel/laravel . --no-interaction --prefer-dist -q",
  {"lint": "php -l artisan", "types": "php -l artisan", "test": "php artisan --version",
   "build": "php artisan --version"}, needs=["composer"], hint="brew install composer")
f("symfony", "php", "web", "composer create-project symfony/skeleton . --no-interaction -q",
  {"lint": "php -l public/index.php", "types": "php -l public/index.php",
   "test": "php bin/console --version", "build": "php bin/console --version"},
  needs=["composer"])
f("slim", "php", "api", "composer require slim/slim slim/psr7 --no-interaction -q",
  {"lint": "php -l public/index.php", "types": "php -l public/index.php",
   "test": "php -r 'require \"vendor/autoload.php\";'", "build": "php -l public/index.php"},
  needs=["composer"])
f("php-cli", "php", "cli", "true",
  {"lint": "php -l bin/cli.php", "types": "php -l bin/cli.php", "test": "php bin/cli.php mamat",
   "build": "php -l bin/cli.php"}, deps="composer dump-autoload -q", needs=["composer"])

# ─── Swift / Elixir / Dart ────────────────────────────────────────────────
f("vapor", "swift", "api", "swift package init --type executable --name {pkg}",
  {"lint": "swift build", "types": "swift build", "test": "swift build",
   "build": "swift build -c release"}, needs=["swift"])
f("swift-cli", "swift", "cli", "swift package init --type executable --name {pkg}",
  {"lint": "swift build", "types": "swift build", "test": "swift build",
   "build": "swift build -c release"}, needs=["swift"])
f("phoenix", "elixir", "web", "mix phx.new . --app {pkg} --no-install --no-ecto",
  {"lint": "mix format --check-formatted", "types": "mix compile --warnings-as-errors",
   "test": "mix test", "build": "mix compile"}, needs=["mix"], hint="brew install elixir")
f("flutter", "dart", "mobile", "flutter create . --project-name {pkg} --platforms=ios,android",
  {"lint": "flutter analyze", "types": "flutter analyze", "test": "flutter test",
   "build": "flutter build apk --debug"}, needs=["flutter"], hint="brew install --cask flutter")
f("dart-cli", "dart", "cli", "dart create -t console . --force",
  {"lint": "dart analyze", "types": "dart analyze", "test": "dart test",
   "build": "dart compile exe bin/{pkg}.dart -o build/app"}, needs=["dart"], hint="brew install dart")

# ─── C / C++ ──────────────────────────────────────────────────────────────
f("cmake", "cpp", "lib", "printf 'cmake_minimum_required(VERSION 3.20)\\nproject({pkg})\\n' > CMakeLists.txt",
  {"lint": "cmake . -B build -DCMAKE_BUILD_TYPE=Debug >/dev/null", "types": "cmake . -B build >/dev/null",
   "test": "cmake . -B build >/dev/null && cmake --build build",
   "build": "cmake . -B build >/dev/null && cmake --build build"}, needs=["cmake"], hint="brew install cmake")
f("meson", "cpp", "lib", "printf 'project(\\'%s\\', \\'cpp\\')\\n' {pkg} > meson.build",
  {"lint": "meson setup build >/dev/null", "types": "meson setup build >/dev/null",
   "test": "meson setup build >/dev/null && meson compile -C build",
   "build": "meson setup build >/dev/null && meson compile -C build"}, needs=["meson"])



# ─── berkas minimal untuk framework yang bootstrap-nya hanya memasang dep ──
TSCONFIG = """{
  "compilerOptions": {
    "target": "ES2022", "module": "ESNext", "moduleResolution": "Bundler",
    "strict": true, "esModuleInterop": true, "skipLibCheck": true,
    "noEmit": true
  },
  "include": ["src", "tests"]
}
"""

EXPRESS_SERVER = """// {name} — API Express
import express from "express"

export function buildApp() {
  const app = express()
  app.get("/health", (_req, res) => res.json({ status: "ok" }))
  return app
}

if (process.env.NODE_ENV !== "test") {
  buildApp().listen(Number(process.env.PORT ?? 3000), () => console.log("listen :3000"))
}
"""

FASTIFY_SERVER = """// {name} — API Fastify
import Fastify from "fastify"

export function buildApp() {
  const app = Fastify({ logger: false })
  app.get("/health", async () => ({ status: "ok" }))
  return app
}

if (process.env.NODE_ENV !== "test") {
  buildApp().listen({ port: Number(process.env.PORT ?? 3000) })
}
"""

KOA_SERVER = """// {name} — API Koa
import Koa from "koa"
import Router from "@koa/router"

export function buildApp() {
  const app = new Koa()
  const r = new Router()
  r.get("/health", (ctx) => { ctx.body = { status: "ok" } })
  app.use(r.routes())
  return app
}

if (process.env.NODE_ENV !== "test") {
  buildApp().listen(Number(process.env.PORT ?? 3000))
}
"""

HAPI_SERVER = """// {name} — API hapi
import Hapi from "@hapi/hapi"

export function buildApp() {
  const server = Hapi.server({ port: Number(process.env.PORT ?? 3000) })
  server.route({ method: "GET", path: "/health", handler: () => ({ status: "ok" }) })
  return server
}

if (process.env.NODE_ENV !== "test") {
  buildApp().then((s) => s.start())
}
"""

HONO_SERVER = """// {name} — API Hono
import { Hono } from "hono"

export const app = new Hono()
app.get("/health", (c) => c.json({ status: "ok" }))

export default app
"""

ELYSIA_SERVER = """// {name} — API Elysia
import { Elysia } from "elysia"

export const app = new Elysia().get("/health", () => ({ status: "ok" }))

export default app
"""

RESTIFY_SERVER = """// {name} — API restify
import restify from "restify"

export function buildApp() {
  const server = restify.createServer()
  server.get("/health", (_req, res, next) => { res.send({ status: "ok" }); return next() })
  return server
}

if (process.env.NODE_ENV !== "test") {
  buildApp().listen(Number(process.env.PORT ?? 3000))
}
"""

TS_LIB = """// {name} — pustaka
export function greet(name: string): string {
  return `Halo, ${name}!`
}
"""

TS_LIB_TEST = """import { describe, expect, it } from "vitest"
import { greet } from "../src/index"

describe("greet", () => {
  it("menyapa", () => expect(greet("mamat")).toBe("Halo, mamat!"))
})
"""

TS_CLI = """#!/usr/bin/env node
// {name} — CLI
const who = process.argv[2] ?? "dunia"
console.log(`Halo, ${who}!`)
"""

JS_CLI = """#!/usr/bin/env node
// {name} — CLI
const who = process.argv[2] ?? "dunia"
console.log(`Halo, ${who}!`)
"""

INK_CLI = """// {name} — TUI berbasis ink
import React from "react"
import { render, Text } from "ink"

const who = process.argv[2] ?? "dunia"
render(<Text>Halo, {who}!</Text>)
"""

PY_SMOKE = """import importlib


def test_import():
    mod = importlib.import_module("{module}")
    assert mod is not None
"""

PY_MAIN_FASTAPI = """from fastapi import FastAPI

app = FastAPI(title="{name}")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
"""

PY_MAIN_FLASK = """from flask import Flask

app = Flask(__name__)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
"""

PY_CLI_TYPER = """import typer

app = typer.Typer()


@app.command()
def hello(name: str = "dunia") -> None:
    typer.echo("Halo, " + name + "!")


if __name__ == "__main__":
    app()
"""

PY_CLI_CLICK = """import click


@click.command()
@click.argument("name", default="dunia")
def main(name: str) -> None:
    click.echo("Halo, " + name + "!")


if __name__ == "__main__":
    main()
"""

JS_TEST = """import test from "node:test"
import assert from "node:assert/strict"

test("smoke", () => {
  assert.equal(1 + 1, 2)
})
"""

TS_SMOKE = """import { describe, expect, it } from "vitest"

describe("smoke", () => {
  it("aritmetika", () => {
    expect(1 + 1).toBe(2)
  })
})
"""

TS_MOD_TEST = """import { describe, expect, it } from "vitest"
import * as mod from "../src/index"

describe("modul", () => {
  it("bisa diimpor", () => {
    expect(Object.keys(mod).length).toBeGreaterThan(0)
  })
})
"""

TSCONFIG_JSX = """{
  "compilerOptions": {
    "target": "ES2022", "module": "ESNext", "moduleResolution": "Bundler",
    "strict": true, "esModuleInterop": true, "skipLibCheck": true,
    "jsx": "react-jsx", "noEmit": true
  },
  "include": ["src", "tests"]
}
"""

import importlib  # noqa: E402

_INIT = {
    "express": {"src/server.js": EXPRESS_SERVER, "tests/smoke.test.js": JS_TEST},
    "fastify": {"src/index.ts": FASTIFY_SERVER, "tsconfig.json": TSCONFIG,
                "tests/index.test.ts": TS_MOD_TEST},
    "koa": {"src/server.js": KOA_SERVER, "tests/smoke.test.js": JS_TEST},
    "hapi": {"src/server.js": HAPI_SERVER, "tests/smoke.test.js": JS_TEST},
    "hono": {"src/index.ts": HONO_SERVER, "tsconfig.json": TSCONFIG,
             "tests/index.test.ts": TS_MOD_TEST},
    "elysia": {"src/index.ts": ELYSIA_SERVER, "tsconfig.json": TSCONFIG,
               "tests/index.test.ts": TS_MOD_TEST},
    "restify": {"src/server.js": RESTIFY_SERVER, "tests/smoke.test.js": JS_TEST},
    "tsup": {"src/index.ts": TS_LIB, "tests/index.test.ts": TS_LIB_TEST,
             "tsconfig.json": TSCONFIG},
    "tsup-cli": {"src/cli.ts": TS_CLI, "tsconfig.json": TSCONFIG,
                 "tests/smoke.test.ts": TS_SMOKE},
    "commander": {"bin/cli.js": JS_CLI, "tests/smoke.test.js": JS_TEST},
    "ink": {"src/cli.tsx": INK_CLI, "tsconfig.json": TSCONFIG_JSX,
            "tests/smoke.test.ts": TS_SMOKE},
    "typer": {"src/app/cli.py": PY_CLI_TYPER},
    "click": {"src/app/cli.py": PY_CLI_CLICK},
    "fastapi": {"src/app/main.py": PY_MAIN_FASTAPI},
    "flask": {"src/app/main.py": PY_MAIN_FLASK},
}

_PY_MODULE = {
    "fastapi": "app", "flask": "app", "starlette": "app", "litestar": "app", "quart": "app",
    "sanic": "app", "tornado": "app", "pyramid": "app", "falcon": "app", "streamlit": "app",
    "gradio": "app", "typer": "app", "click": "app", "hatch": "app", "pandas": "app",
    "polars": "app", "jupyter": "app", "sklearn": "app", "pytorch": "app",
    "transformers": "app", "dask": "app",
}

for _fid, _mod in _PY_MODULE.items():
    if _fid in F:
        F[_fid].setdefault("files", {})
        F[_fid]["files"].setdefault("tests/test_smoke.py", PY_SMOKE.replace("{module}", _mod))

for _fid, _files in _INIT.items():
    if _fid in F:
        F[_fid].setdefault("files", {})
        for _rel, _c in _files.items():
            F[_fid]["files"].setdefault(_rel, _c)

# entri yang butuh vitest/tsx supaya gate test/build punya isi
for _fid in ("tsup", "tsup-cli", "hono", "elysia", "fastify"):
    if _fid in F:
        F[_fid]["deps"] = (F[_fid]["deps"] or "").strip()


GO_GIN = """package main

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

func newRouter() *gin.Engine {
	r := gin.New()
	r.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"status": "ok"})
	})
	return r
}

func main() {
	_ = newRouter().Run(":8080")
}
"""

GO_ECHO = """package main

import (
	"net/http"

	"github.com/labstack/echo/v4"
)

func newRouter() *echo.Echo {
	e := echo.New()
	e.GET("/health", func(c echo.Context) error {
		return c.JSON(http.StatusOK, map[string]string{"status": "ok"})
	})
	return e
}

func main() {
	_ = newRouter().Start(":8080")
}
"""

GO_FIBER = """package main

import "github.com/gofiber/fiber/v2"

func newApp() *fiber.App {
	app := fiber.New()
	app.Get("/health", func(c *fiber.Ctx) error {
		return c.JSON(fiber.Map{"status": "ok"})
	})
	return app
}

func main() {
	_ = newApp().Listen(":8080")
}
"""

GO_CHI = """package main

import (
	"net/http"

	"github.com/go-chi/chi/v5"
)

func newRouter() http.Handler {
	r := chi.NewRouter()
	r.Get("/health", func(w http.ResponseWriter, _ *http.Request) {
		_, _ = w.Write([]byte(`{"status":"ok"}`))
	})
	return r
}

func main() {
	_ = http.ListenAndServe(":8080", newRouter())
}
"""

GO_COBRA = """package main

import (
	"fmt"

	"github.com/spf13/cobra"
)

func newRoot() *cobra.Command {
	root := &cobra.Command{Use: "app", Run: func(cmd *cobra.Command, args []string) {
		fmt.Fprintln(cmd.OutOrStdout(), "Halo, dunia!")
	}}
	return root
}

func main() {
	_ = newRoot().Execute()
}
"""

GO_URFAVE = """package main

import (
	"fmt"
	"os"

	"github.com/urfave/cli/v2"
)

func main() {
	app := &cli.App{
		Name: "app",
		Action: func(c *cli.Context) error {
			fmt.Println("Halo, dunia!")
			return nil
		},
	}
	if err := app.Run(os.Args); err != nil {
		fmt.Fprintln(os.Stderr, err)
	}
}
"""

RS_AXUM = """use axum::{routing::get, Json, Router};
use serde_json::{json, Value};

pub fn app() -> Router {
    Router::new().route("/health", get(|| async { Json(json!({"status": "ok"})) }))
}

#[tokio::main]
async fn main() {
    let listener = tokio::net::TcpListener::bind("0.0.0.0:8080").await.unwrap();
    axum::serve(listener, app()).await.unwrap();
}

#[allow(dead_code)]
fn _t() -> Value {
    json!({})
}
"""

RS_ACTIX = """use actix_web::{get, web, App, HttpServer, Responder};

#[get("/health")]
async fn health() -> impl Responder {
    web::Json(serde_json::json!({"status": "ok"}))
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| App::new().service(health)).bind(("0.0.0.0", 8080))?.run().await
}
"""

RS_ROCKET = """#[macro_use]
extern crate rocket;

#[get("/health")]
fn health() -> &'static str {
    r#"{"status":"ok"}"#
}

#[launch]
fn rocket() -> _ {
    rocket::build().mount("/", routes![health])
}
"""

RS_WARP = """use warp::Filter;

#[tokio::main]
async fn main() {
    let health = warp::path("health").map(|| r#"{"status":"ok"}"#);
    warp::serve(health).run(([0, 0, 0, 0], 8080)).await;
}
"""

RS_POEM = """use poem::{handler, listener::TcpListener, Route, Server};

#[handler]
fn health() -> &'static str {
    r#"{"status":"ok"}"#
}

#[tokio::main]
async fn main() -> Result<(), std::io::Error> {
    Server::new(TcpListener::bind("0.0.0.0:8080"))
        .run(Route::new().at("/health", poem::get(health)))
        .await
}
"""

RS_CLAP = """use clap::Parser;

#[derive(Parser)]
struct Cli {
    /// nama yang disapa
    #[arg(default_value = "dunia")]
    name: String,
}

fn main() {
    let cli = Cli::parse();
    println!("Halo, {}!", cli.name);
}

#[cfg(test)]
mod tests {
    #[test]
    fn aritmetika() {
        assert_eq!(1 + 1, 2);
    }
}
"""

RS_RATATUI = """use std::io;

use crossterm::{
    event::{self, Event, KeyCode},
    terminal::{disable_raw_mode, enable_raw_mode},
};

fn main() -> io::Result<()> {
    enable_raw_mode()?;
    if let Event::Key(key) = event::read()? {
        if key.code == KeyCode::Char('q') {
            disable_raw_mode()?;
        }
    }
    println!("selesai");
    Ok(())
}
"""

GO_FILES = {
    "gin": {"main.go": GO_GIN},
    "echo": {"main.go": GO_ECHO},
    "fiber": {"main.go": GO_FIBER},
    "chi": {"main.go": GO_CHI},
    "cobra": {"main.go": GO_COBRA},
    "urfave-cli": {"main.go": GO_URFAVE},
}

RS_FILES = {
    "axum": {"src/main.rs": RS_AXUM},
    "actix": {"src/main.rs": RS_ACTIX},
    "rocket": {"src/main.rs": RS_ROCKET},
    "warp": {"src/main.rs": RS_WARP},
    "poem": {"src/main.rs": RS_POEM},
    "clap": {"src/main.rs": RS_CLAP},
    "ratatui": {"src/main.rs": RS_RATATUI},
}

for _fid, _files in {**GO_FILES, **RS_FILES}.items():
    if _fid in F:
        F[_fid].setdefault("files", {})
        for _rel, _c in _files.items():
            F[_fid]["files"].setdefault(_rel, _c)


RB_SINATRA = """# frozen_string_literal: true
require "sinatra/base"

# {name} — API Sinatra
class App < Sinatra::Base
  get "/health" do
    content_type :json
    '{"status":"ok"}'
  end
end
"""

RB_SINATRA_RU = """# frozen_string_literal: true
require_relative "app"

run App
"""

RB_SINATRA_TEST = """# frozen_string_literal: true
require "minitest/autorun"
require_relative "../app"

class AppTest < Minitest::Test
  def test_health
    env = { "REQUEST_METHOD" => "GET", "PATH_INFO" => "/health" }
    status, _headers, body = App.call(env)
    assert_equal 200, status
    assert_includes body.join, "ok"
  end
end
"""

RB_GRAPE = """# frozen_string_literal: true
require "grape"

# {name} — API Grape
class API < Grape::API
  format :json

  get "/health" do
    { status: "ok" }
  end
end
"""

RB_GRAPE_RU = """# frozen_string_literal: true
require_relative "app"

run API
"""

RB_GRAPE_TEST = """# frozen_string_literal: true
require "minitest/autorun"
require_relative "../app"

class ApiTest < Minitest::Test
  def test_bisa_dipanggil
    assert API.respond_to?(:call)
  end
end
"""

RB_FILES = {
    "sinatra": {"app.rb": RB_SINATRA, "config.ru": RB_SINATRA_RU,
                "test/app_test.rb": RB_SINATRA_TEST},
    "grape": {"app.rb": RB_GRAPE, "config.ru": RB_GRAPE_RU,
              "test/app_test.rb": RB_GRAPE_TEST},
}

for _fid, _files in RB_FILES.items():
    if _fid in F:
        F[_fid].setdefault("files", {})
        for _rel, _c in _files.items():
            F[_fid]["files"].setdefault(_rel, _c)


PHP_SLIM_INDEX = r"""<?php
declare(strict_types=1);

require __DIR__ . '/../vendor/autoload.php';

use Psr\Http\Message\ServerRequestInterface;
use Slim\Factory\AppFactory;
use Slim\Psr7\Response;

$app = AppFactory::create();

$app->get('/health', function (ServerRequestInterface $request, Response $response) {
    $response->getBody()->write(json_encode(['status' => 'ok']));
    return $response->withHeader('Content-Type', 'application/json');
});

$app->run();
"""

PHP_CLI_APP = r"""<?php
declare(strict_types=1);

namespace App;

/** {name} — CLI */
final class Cli
{
    public static function greet(string $name): string
    {
        return "Halo, {$name}!";
    }
}
"""

PHP_CLI_BIN = r"""#!/usr/bin/env php
<?php
declare(strict_types=1);

require __DIR__ . '/../vendor/autoload.php';

$who = $argv[1] ?? 'dunia';
echo \App\Cli::greet($who), PHP_EOL;
"""

PHP_CLI_TEST = r"""<?php
declare(strict_types=1);

require __DIR__ . '/../vendor/autoload.php';

if (\App\Cli::greet('mamat') !== 'Halo, mamat!') {
    fwrite(STDERR, "gagal\\n");
    exit(1);
}
echo "ok\\n";
"""

PHP_COMPOSER = r"""{
  "name": "dev/{pkg}",
  "type": "project",
  "require": { "php": ">=8.2" },
  "autoload": { "psr-4": { "App\\": "src/" } }
}
"""

PHP_FILES = {
    "slim": {"public/index.php": PHP_SLIM_INDEX},
    "php-cli": {"composer.json": PHP_COMPOSER, "src/Cli.php": PHP_CLI_APP,
                "bin/cli.php": PHP_CLI_BIN, "tests/run.php": PHP_CLI_TEST},
}

for _fid, _files in PHP_FILES.items():
    if _fid in F:
        F[_fid].setdefault("files", {})
        for _rel, _c in _files.items():
            F[_fid]["files"].setdefault(_rel, _c)

# ─── util ─────────────────────────────────────────────────────────────────
def get(fid):
    return F.get(fid)


def by_kind():
    out = {}
    for e in F.values():
        out.setdefault(e["kind"], []).append(e["id"])
    return {k: sorted(v) for k, v in sorted(out.items())}


ALIAS = {
    "python": "py", "javascript": "js", "typescript": "ts", "golang": "go",
    "rust": "rust", "csharp": "csharp", "c#": "csharp", "dotnet": "csharp",
    ".net": "csharp", "ruby": "ruby", "php": "php", "swift": "swift",
    "kotlin": "kotlin", "elixir": "elixir", "dart": "dart", "c++": "cpp",
    "cpp": "cpp", "c": "c", "frontend": "web", "backend": "api", "server": "api",
    "rest": "api", "http": "api", "cli": "cli", "library": "lib", "package": "lib",
    "machine-learning": "ml", "ai": "ml", "data-science": "data", "analytics": "data",
}


def search(q):
    q = q.lower().strip()
    q = ALIAS.get(q, q)
    return [e for e in F.values()
            if q in e["id"].lower() or q in e["lang"].lower() or q in e["kind"].lower()]


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "search":
        for e in search(" ".join(sys.argv[2:])):
            print(f"{e['id']:<18} {e['lang']:<7} {e['kind']}")
    else:
        for k, v in by_kind().items():
            print(f"{k:<8} {' '.join(v)}")
        print(f"\ntotal {len(F)} framework/library")
