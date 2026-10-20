# Multi-Language Development Skill

Workflows für Rust, Python, TypeScript, Bun, Tauri, Turbopack, CMake.

## Rust

### Projekt-Setup
```bash
cargo new myapp --bin
cd myapp && cargo add serde tokio reqwest anyhow
cargo build --release
cargo test -- --nocapture
cargo clippy -- -D warnings
cargo fmt --check
```

### Cargo.toml
```toml
[package]
name = "myapp"
version = "0.1.0"
edition = "2021"

[dependencies]
tokio = { version = "1", features = ["full"] }
serde = { version = "1", features = ["derive"] }
reqwest = { version = "0.12", features = ["json"] }
anyhow = "1"
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter"] }

[profile.release]
opt-level = 3
lto = true
codegen-units = 1
```

## Python

### Modern Python Project
```bash
uv init myapp
uv add httpx fastapi uvicorn pydantic
uv run python -m myapp
uv sync  # lockfile
```

### pyproject.toml
```toml
[project]
name = "myapp"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "httpx>=0.28",
    "fastapi>=0.115",
    "uvicorn[standard]",
]

[tool.ruff]
line-length = 120
target-version = "py312"
[tool.ruff.lint]
select = ["E", "F", "I", "N", "W"]
[tool.mypy]
strict = true
```

## TypeScript / Bun

### Bun Projekt
```bash
bun init -y
bun add hono zod
bun add -d @types/bun
bun run src/index.ts
bun test
bun build --target bun --outdir ./dist ./src/index.ts
```

### package.json
```json
{
  "compilerOptions": {
    "target": "ESNext",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "outDir": "./dist"
  }
}
```

## Tauri (Rust + Frontend)

### Setup
```bash
npm create tauri-app@latest -- --template react-ts
cd myapp
npm install
cargo tauri dev    # development
cargo tauri build  # production
```

### Tauri Config
```json
{
  "build": {
    "beforeBuildCommand": "npm run build",
    "frontendDist": "../dist",
    "devUrl": "http://localhost:5173"
  },
  "bundle": {
    "active": true,
    "identifier": "com.zen.myapp",
    "icon": ["icons/icon.png"]
  },
  "app": {
    "windows": [{"title": "MyApp", "width": 1024, "height": 768}],
    "security": {
      "csp": "default-src 'self'; script-src 'self'"
    }
  }
}
```

## Turbopack

### Setup
```bash
npx create-turbo@latest
cd myapp
npm run dev  # turbopack based
npm run build
```

## CMake

### Basic CMakeLists.txt
```cmake
cmake_minimum_required(VERSION 3.28)
project(myapp VERSION 0.1.0 LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
add_executable(myapp src/main.cpp src/utils.cpp)
target_include_directories(myapp PRIVATE include)
target_link_libraries(myapp PRIVATE fmt fmt::fmt)
```

### Cross-Compilation
```bash
cmake -B build -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_TOOLCHAIN_FILE=/toolchains/aarch64-linux-gnu.cmake
cmake --build build -j$(nproc)
```
