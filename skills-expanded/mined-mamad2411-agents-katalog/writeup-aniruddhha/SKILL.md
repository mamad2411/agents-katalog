<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-aniruddhha
description: CTF writeups and security challenges by aniruddhha.
---

# Writeups by aniruddhha

Source repository: `/repos/aniruddhha`

## Repository Index

- dirust/LICENCE.md
- dirust/README.md

## Writeup Content


### File: dirust/README.md

# Dirust — Fast, Async Directory Brute-Forcer in Rust

**Dirust** is a high-performance web content discovery tool (a.k.a. “directory buster”) written in Rust. It targets hidden files and directories by probing endpoints from a wordlist with optional extensions, using efficient async I/O and clean, explicit code.

**Use cases:** web directory brute forcing, content discovery, red team/pentest recon, CI-friendly site checks, and rapid HTTP enumeration.

---

## Highlights

- **Async & fast** — Tokio runtime + Reqwest client; bounded concurrency for stable throughput.
- **HEAD with safe fallback** — Tries `HEAD` first for speed, falls back to `GET` on `405`.
- **Extensions fan-out** — `--exts php,html,txt` turns `admin` into `admin.php`, `admin.html`, `admin.txt`, etc.
- **Actionable output** — Prints status code, content length (if available), and redirect `Location` targets.
- **Cross-platform** — Linux (incl. Kali), macOS, Windows, and Raspberry Pi (aarch64/armv7).
- **No root needed** — Pure user-space HTTP(S).
- **Readable codebase** — Clear modules, explicit error handling (no `anyhow`), easy to extend.

---

## Quick Start

```bash
# 1) Build
cargo build --release

# 2) Run against a target
./target/release/dirust https://example.com/ -w /path/to/wordlist.txt

# Add extensions and increase concurrency
./target/release/dirust https://example.com/app/ -w words.txt --exts php,html,txt -c 100

# Force GET (some servers block or alter HEAD)
./target/release/dirust https://example.com/ -w words.txt --get

# Set a custom timeout (seconds)
./target/release/dirust https://example.com/ -w words.txt --timeout 20
```

Show help any time:

```bash
./target/release/dirust --help
```

---

## Local Demo (localhost)

Spin up a tiny site locally and point Dirust at it:

```bash
# Create a few files
mkdir -p /tmp/dirust-site/{admin,secret,api}
printf "admin home"  > /tmp/dirust-site/admin/index.html
printf "top secret"  > /tmp/dirust-site/secret/flag.txt
printf "ok"          > /tmp/dirust-site/api/status
printf "read me"     > /tmp/dirust-site/readme.txt

# Start a simple HTTP server (port 8000)
python3 -m http.server 8000 --directory /tmp/dirust-site

# Minimal wordlist
cat > /tmp/words.txt <<'EOF'
admin
admin/
secret
secret/
api
api/
status
readme
readme.txt
flag.txt
EOF

# Run Dirust
./target/release/dirust http://127.0.0.1:8000/ -w /tmp/words.txt --exts html,txt -c 50
```

---

## Features in Detail

- **Directory & file discovery:** Reads a wordlist and probes each path relative to the base URL.
- **Extensions expansion:** Applies a comma-separated list of extensions to each word (normalized to `.ext`).
- **Concurrency control:** A semaphore ensures at most `--concurrency N` requests are in flight.
- **Robust HTTP logic:**
  - **Method:** `HEAD` by default; automatic GET retry on `405 Method Not Allowed`, or always `GET` with `--get`.
  - **Redirect awareness:** Prints `→ Location` when present (e.g., `301/302`).
  - **Interesting status filter:** Prints common “exists/protected” signals (`200/301/302/401/403`).
- **Clear output format:**
  ```
  [<unix_ts>] <status> len=<content_length_or_->_>  <url> [-> <location_if_any>]
  ```

---

## Installation

**Requirements:** recent Rust toolchain (`rustup update` recommended).

```bash
git clone <your-repo-url> dirust
cd dirust
cargo build --release
```

Binary output:
- Linux/macOS: `./target/release/dirust`
- Windows: `.	arget
elease\dirust.exe`

Raspberry Pi:
- Build on the Pi directly (recommended), or cross-compile using the appropriate target (`aarch64-unknown-linux-gnu` or `armv7-unknown-linux-gnueabihf`) and system linker.

---

## CLI Summary

```
Usage: dirust [OPTIONS] <BASE>

Arguments:
  <BASE>  Base URL (e.g., https://example.com/ or https://example.com/app/)

Options:
  -w, --wordlist <WORDLIST>         Path to wordlist file (required)
  -c, --concurrency <N>             Requests in flight [default: 50]
      --get                         Use GET instead of HEAD
      --timeout <SECS>              Per-request timeout [default: 10]
      --exts <E1,E2,...>            Extra extensions (e.g., php,html,txt)
  -h, --help                        Print help
  -V, --version                     Print version
```

---

## Architecture

The project is organized into small, focused modules for clarity and maintainability:

```
src/
  main.rs         # entry point: parse args, build client, run scan
  args.rs         # clap-based CLI definition and helpers
  error.rs        # explicit DirustError enum and conversions
  url.rs          # base URL validation/normalization
  scanner/
    mod.rs        # orchestration: concurrency, task spawning, printing
    wordlist.rs   # file I/O: load and filter wordlist
    targets.rs    # build full URLs from base + words + extensions
    http.rs       # single-request probe; summarize status/headers
    util.rs       # timestamp and status filter helpers
```

Design choices:
- **Explicit error handling:** `DirustError` (no `anyhow`), clear `Result` returns, and full `match` statements for readability.
- **No auto-redirect:** we want to **see** redirect responses and their `Location` targets.
- **Stable concurrency:** acquire semaphore permits **before** spawning tasks to hard-cap active work.
- **Separation of concerns:** wordlist reading, target generation, HTTP probe, and printing are isolated modules.

---

## Performance Tips

- Tune `--concurrency` based on network conditions and target behavior. Watch for server rate-limits and adjust.
- `HEAD` is usually faster; if a server misbehaves on HEAD, use `--get`.
- Increase `--timeout` when probing slow or distant hosts; decrease it for aggressive scans on fast LANs.
- Reuse a single process and a single HTTP client (Dirust does this by design) to benefit from connection pooling.

---

## Roadmap

Planned enhancements (kept intentionally focused and practical):

- `--delay-ms` and retries with jitter (gentler on fragile hosts)
- `--output <file>` (text/JSON) and consistent structured logs
- `--proxy`, `--header`, `--user-agent`, `--cookie`
- Smart 404 detection (baseline + size tolerance) as an optional module
- Depth-limited recursion (`--max-depth`) for directory trees
- VHost mode (brute Host header) as a sibling tool

---

## Compatibility

- **OS:** Linux (incl. Kali), macOS, Windows, Raspberry Pi
- **Network:** HTTP/HTTPS, no root privileges required
- **TLS:** Uses rustls; for custom corporate CAs, consider building with native roots (`rustls-tls-native-roots` feature in Reqwest)

---

## Security & Legal

Only scan systems you **own** or have explicit permission to test. Unauthorized scanning can be illegal and unethical. Use Dirust responsibly and comply with local laws and the target’s terms of service.

---

## Contributing

Contributions are welcome. Please keep changes:
- Explicit and easy to read (prefer full `match` over terse shortcuts)
- Modular (one concern per file/module)
- Well-explained in commit messages

Open a PR with a clear description and example commands. Bug reports with repro steps are great.

---

## License

MIT License — [See LICENSE](./LICENCE.md)

---

## Keywords

`web discovery`, `directory brute force`, `dirb alternative`, `gobuster alternative`, `pentest`, `red team`, `content discovery`, `http enumeration`, `rust`, `async`, `tokio`, `reqwest`



### File: dirust/LICENCE.md

MIT License

Copyright (c) 2025 Aniruddha Kudalkar

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

