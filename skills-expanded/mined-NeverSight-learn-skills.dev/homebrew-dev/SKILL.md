---
name: homebrew-dev
description: Package and distribute macOS apps, fonts, CLI tools, and arbitrary files using Homebrew formulas and casks. Use this skill whenever the user wants to create a Homebrew formula or cask, set up a personal tap, package a macOS .app bundle, distribute fonts or pre-built binaries via brew, use `brew create`, bump a formula or cask to a new version, submit a package to homebrew-core or homebrew-cask, or publish anything with Homebrew — even if they just ask how to "make something installable with brew", "share my app through Homebrew", "update my formula", or "get my package into Homebrew".
allowed-tools:
  - Bash(brew:*)
  - Bash(shasum:*)
  - Bash(git:*)
  - Bash(gh:*)
---

# Homebrew Packaging Skill

You are an expert at packaging software with Homebrew — both formulas (source builds and pre-built binaries) and casks (macOS apps, fonts, arbitrary files). You help users create, test, and distribute packages through personal taps on GitHub.

## Deciding: Formula vs. Cask

| Scenario | Use |
|----------|-----|
| CLI tool with source code (C, Go, Rust, etc.) | Formula |
| Pre-built binary tarball for a CLI tool | Formula (no build step) |
| macOS `.app` bundle | Cask |
| Font files (`.ttf`, `.otf`) | Cask |
| PKG installer | Cask |
| Arbitrary file placement (e.g. completions, configs) | Cask with `artifact` |
| App with auto-updater | Cask with `auto_updates true` |
| Both a CLI and a GUI component | Both (linked from cask with `binary`) |

---

## Creating a Formula

### Scaffold
```bash
brew create https://example.com/mytool-1.0.tar.gz
```
This auto-populates `url`, `sha256`, `version`, and opens the editor.

### Key fields
```ruby
class Mytool < Formula
  desc "One-line description (imperative, no trailing period, no 'A' prefix)"
  homepage "https://example.com/mytool"
  url "https://example.com/mytool-1.0.tar.gz"
  sha256 "abc123..."      # from: shasum -a 256 <file>
  license "MIT"
  version "1.0"           # omit if parseable from url

  depends_on "cmake" => :build           # build-time only
  depends_on "openssl@3"                 # runtime
  depends_on "python@3.12" => :optional  # optional runtime
  depends_on :macos => :monterey         # minimum macOS

  def install
    system "./configure", *std_configure_args
    system "make", "install"
  end

  test do
    system "#{bin}/mytool", "--version"
    assert_match "1.0", shell_output("#{bin}/mytool --version")
  end
end
```

### Install directory variables
| Variable | Expands to |
|----------|-----------|
| `bin` | `$(brew --prefix)/bin` |
| `lib` | `$(brew --prefix)/lib` |
| `include` | `$(brew --prefix)/include` |
| `share` | `$(brew --prefix)/share` |
| `etc` | `$(brew --prefix)/etc` |
| `var` | `$(brew --prefix)/var` |
| `libexec` | `$(brew --prefix)/opt/<name>/libexec` |

### Build systems
```ruby
# Autoconf/Make
system "./configure", *std_configure_args
system "make", "install"

# CMake
system "cmake", "-S", ".", "-B", "build", *std_cmake_args
system "cmake", "--build", "build"
system "cmake", "--install", "build"

# Cargo (Rust)
system "cargo", "install", *std_cargo_args

# Go
system "go", "build", *std_go_args, "-o", bin/"mytool", "./cmd/mytool"

# Pre-built binary (no build)
def install
  bin.install "mytool"
  man1.install "mytool.1"
end
```

### Architecture conditionals
```ruby
on_arm do
  url "https://example.com/mytool-1.0-arm64.tar.gz"
  sha256 "arm_sha..."
end

on_intel do
  url "https://example.com/mytool-1.0-x86_64.tar.gz"
  sha256 "intel_sha..."
end
```

---

## Creating a Cask

### Scaffold
```bash
brew create --cask https://example.com/MyApp-1.0.dmg
```

### Artifact types and their uses

| Artifact | Use case | Installs to |
|----------|----------|-------------|
| `app "MyApp.app"` | macOS `.app` bundles | `/Applications` |
| `font "MyFont.ttf"` | Font files | `~/Library/Fonts/` |
| `binary "mytool"` | Pre-built CLI tool from archive | `$(brew --prefix)/bin/` |
| `artifact "myfile", target: "~/.config/myfile"` | Arbitrary file placement | Custom path |
| `pkg "MyApp.pkg"` | PKG installer | System (requires `uninstall`) |
| `suite "MyApp.app"` | Multi-app suites | `/Applications` |

### Minimal cask (DMG with app)
```ruby
cask "myapp" do
  version "1.0"
  sha256 "abc123..."

  url "https://example.com/MyApp-#{version}.dmg"
  name "MyApp"
  desc "Does something useful"
  homepage "https://example.com/myapp"

  app "MyApp.app"

  zap trash: [
    "~/Library/Application Support/MyApp",
    "~/Library/Preferences/com.example.myapp.plist",
  ]
end
```

### Font cask
```ruby
cask "font-my-font" do
  version "2.0"
  sha256 "abc123..."

  url "https://example.com/MyFont-#{version}.zip"
  name "My Font"
  desc "A beautiful typeface"
  homepage "https://example.com/myfont"

  font "MyFont-Regular.ttf"
  font "MyFont-Bold.ttf"
  font "MyFont-Italic.ttf"
end
```

### Arbitrary file placement
```ruby
cask "mycli" do
  version "1.0"
  sha256 "abc123..."

  url "https://example.com/mycli-#{version}.zip"
  name "MyCLI"
  desc "A command-line tool"
  homepage "https://example.com/mycli"

  binary "mycli"
  artifact "mycli.zsh-completion", target: "#{HOMEBREW_PREFIX}/share/zsh/site-functions/_mycli"
  artifact "mycli.fish", target: "#{HOMEBREW_PREFIX}/share/fish/vendor_completions.d/mycli.fish"
end
```

### PKG installer
```ruby
cask "myapp" do
  version "1.0"
  sha256 "abc123..."

  url "https://example.com/MyApp-#{version}.pkg"
  name "MyApp"
  desc "Does something useful"
  homepage "https://example.com/myapp"

  pkg "MyApp.pkg"

  uninstall pkgutil: "com.example.myapp"

  zap trash: [
    "~/Library/Application Support/MyApp",
    "~/Library/Preferences/com.example.myapp.plist",
  ]
end
```

### Architecture-conditional cask
```ruby
cask "myapp" do
  version "1.0"

  on_arm do
    url "https://example.com/MyApp-#{version}-arm64.dmg"
    sha256 "arm_sha..."
  end

  on_intel do
    url "https://example.com/MyApp-#{version}-x86_64.dmg"
    sha256 "intel_sha..."
  end

  name "MyApp"
  desc "Does something useful"
  homepage "https://example.com/myapp"

  app "MyApp.app"
end
```

### Rolling release (no stable version)
```ruby
cask "myapp" do
  version :latest
  sha256 :no_check

  url "https://example.com/MyApp-latest.dmg"
  name "MyApp"
  desc "Does something useful"
  homepage "https://example.com/myapp"

  auto_updates true   # app has built-in updater
  app "MyApp.app"
end
```

---

## Bumping a Version

When a new release is out, update three things:

**Formula:**
```ruby
url "https://example.com/mytool-1.1.tar.gz"   # new URL
sha256 "newsha256..."                           # recompute (see below)
version "1.1"                                   # if not parseable from url
```

**Cask:** same fields, but also verify `#{version}` interpolation in `url` still produces the correct download URL with the new version string.

**Get the new checksum:**
```bash
# Option A: download and compute locally
shasum -a 256 mytool-1.1.tar.gz

# Option B: let brew fetch it
brew fetch --force --build-from-source ./Formula/mytool.rb
```

**Then verify:**
```bash
brew audit mytool
brew test mytool
```

**Faster alternative — let brew do it all:**
```bash
brew bump-formula-pr mytool --version 1.1 --url https://example.com/mytool-1.1.tar.gz
brew bump-cask-pr myapp --version 1.1
```
These commands fetch the new tarball, compute the sha256, update the formula/cask, and open a pull request — all in one step. Recommended when submitting bumps to homebrew-core or homebrew-cask.

---

## Submitting to Homebrew Core / Cask

To get your package into the official `homebrew/core` or `homebrew/cask` taps (so users can `brew install` without adding your tap), you need to open a PR against the upstream repo.

Eligibility requirements, the fork/PR workflow, audit flags, commit conventions, and common rejection reasons are covered in full at:

`references/homebrew-core-submission.md`

---

## Setting up a Personal Tap

### 1. Create the GitHub repo
Name it `homebrew-<tapname>` (e.g. `homebrew-tools`).

### 2. Directory structure
```
homebrew-tools/
├── Formula/
│   └── mytool.rb
└── Casks/
    └── myapp.rb
```

### 3. Tap and install
```bash
brew tap username/tools                      # taps github.com/username/homebrew-tools
brew install username/tools/mytool
brew install --cask username/tools/myapp
```

### 4. Test before publishing
```bash
brew install --build-from-source ./Formula/mytool.rb
brew install --cask ./Casks/myapp.rb
```

---

## Development Commands

```bash
# Create scaffolds
brew create https://example.com/tool-1.0.tar.gz
brew create --cask https://example.com/App-1.0.dmg

# Edit formula/cask
brew edit mytool
brew edit --cask myapp

# Install for testing
brew install --build-from-source ./Formula/mytool.rb
brew install --cask ./Casks/myapp.rb

# Run tests
brew test mytool
brew test --cask myapp

# Audit (validate before publishing)
brew audit --new mytool
brew audit --new --cask myapp

# Uninstall / reinstall cycle
brew uninstall mytool && brew install --build-from-source ./Formula/mytool.rb

# Style check
brew style ./Formula/mytool.rb
brew style --cask ./Casks/myapp.rb

# Fetch without installing (verify download)
brew fetch mytool
brew fetch --cask myapp
```

---

## Checksum Workflow

```bash
# Compute SHA-256 for a local file
shasum -a 256 myapp-1.0.dmg

# Or let brew fetch and show it
brew fetch --force --build-from-source ./Formula/mytool.rb
```

`brew create` auto-populates `sha256` if it can download the file during scaffold creation.

---

## Validation

Run before publishing to a tap:
```bash
brew audit --new mytool          # stricter checks for new packages
brew audit --new --cask myapp
brew style ./Formula/mytool.rb   # RuboCop style check
```

**Common audit issues:**
- `desc` must not start with "A" or "The", must not end with a period
- `homepage` must use HTTPS
- `license` required for formulas (use SPDX identifiers: `"MIT"`, `"Apache-2.0"`, etc.)
- `url` must be stable, versioned, and use HTTPS
- `sha256` must match the download exactly
- Test block required for formulas

---

## References

- Formula patterns & annotated examples: `references/formula-cookbook.md`
- Cask patterns & annotated examples: `references/cask-cookbook.md`
- Submitting to homebrew-core / homebrew-cask: `references/homebrew-core-submission.md`
- Official docs: https://docs.brew.sh/Formula-Cookbook
- Cask docs: https://docs.brew.sh/Cask-Cookbook
