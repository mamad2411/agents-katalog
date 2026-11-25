---
name: golang-coding
description: Scaffolds a Go project with multi-architecture build scripts and a universal entry-point loader. Use when bootstrapping a new Go CLI tool or service, setting up a Go project structure, or creating cross-platform Go binaries.
---

# Golang Project Scaffolder

Uses `bin/` as the standard directory for compiled binaries.

Replace `{{APP_NAME}}` with the actual project name (e.g. `mytool`) in every file below.

## Scaffold Templates

### .gitignore

Prevents binaries and OS-specific files from being committed.

```text
/bin/
/dist/
*.exe
*.exe~
*.dll
*.so
*.dylib
*.test
*.out
```

### scripts/build.sh

This script builds the project for common OS/Architecture pairs.

```bash
#!/bin/bash
# scripts/build.sh
APP_NAME="{{APP_NAME}}"
PLATFORMS=("darwin/amd64" "darwin/arm64" "linux/amd64" "linux/arm64" "windows/amd64")

mkdir -p bin

for PLATFORM in "${PLATFORMS[@]}"; do
    OS=$(echo $PLATFORM | cut -d'/' -f1)
    ARCH=$(echo $PLATFORM | cut -d'/' -f2)
    OUTPUT="bin/${APP_NAME}-${OS}-${ARCH}"

    if [ "$OS" = "windows" ]; then
        OUTPUT="${OUTPUT}.exe"
    fi

    echo "Building for $OS/$ARCH..."
    GOOS=$OS GOARCH=$ARCH go build -o "$OUTPUT" .
done

find bin/ -not -name "*.exe" -exec chmod +x {} +
```

### {{APP_NAME}} (Universal Loader)

An extensionless script at the project root that detects the host environment and runs the matching binary.

```bash
#!/bin/bash
# {{APP_NAME}}
APP_NAME="{{APP_NAME}}"

# Detect OS and Normalize
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
case "$OS" in
    darwin*)  OS="darwin" ;;
    linux*)   OS="linux" ;;
    msys*|cygwin*|mingw*) OS="windows" ;;
esac

# Detect Architecture and Normalize
ARCH=$(uname -m)
case "$ARCH" in
    x86_64) ARCH="amd64" ;;
    aarch64|arm64) ARCH="arm64" ;;
    i386|i686) ARCH="386" ;;
esac

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BINARY="${SCRIPT_DIR}/bin/${APP_NAME}-${OS}-${ARCH}"
if [ "$OS" = "windows" ]; then
    BINARY="${BINARY}.exe"
fi

if [ -f "$BINARY" ]; then
    exec "$BINARY" "$@"
else
    echo "Error: No binary found for $OS-$ARCH ($BINARY)."
    echo "Run './scripts/build.sh' to generate binaries."
    exit 1
fi
```

## Usage

1. Replace `{{APP_NAME}}` with the project name in both `scripts/build.sh` and the loader script.
2. Run `chmod +x scripts/build.sh {{APP_NAME}}`.
3. Run `./scripts/build.sh` to produce binaries in `bin/`.
4. Run `./{{APP_NAME}}` — the loader selects the correct binary automatically.
