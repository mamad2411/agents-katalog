# Is7z AI Agent Guide

## Overview

This is a fork of 7-Zip (upstream: `jrsoftware/7zip`) with modifications for Inno Setup (`jrsoftware/is7z`). It produces three DLLs used by Inno Setup:
- **7z.dll** (via `Format7zFInno`) — compact 7z.dll with a reduced set of archive formats
- **7zxa.dll** (via `Format7zExtract`) — extract-only, 7z format only
- **7zxr.dll** (via `Format7zExtractR`) — extract-only, 7z format only, no crypto

The Inno Setup-specific code lives in `CPP/7zip/Bundles/Format7zFInno/`. Everything else is upstream 7-Zip source.

## Build

Requires Visual Studio 2022 with C++ tools (and C++ Clang for Arm64). Uses `nmake` via `vcvarsall.bat`.

Two settings files (not checked in) are needed:
- `compilesettings.bat` — sets `VSBUILDROOT` to VS build tools path
- `buildsettings.bat` — sets `ISSRCROOT` to the Inno Setup source root

**Compile a single architecture:**
```
compile.bat x86|x64|arm64 [noclean]
```

**Build x86+x64 and copy DLLs to issrc:**
```
build.bat [noclean] [nosynch]
```

The `noclean` flag skips `nmake clean` before building. The `nosynch` flag skips synching to the issrc Projects\Bin folder.

## Architecture

The three Inno Setup bundles are defined by their makefiles in `CPP/7zip/Bundles/`:

- `Format7zFInno/` — the main Inno Setup 7z.dll. `Arc.mak` defines which archive formats and codecs are included. This is a subset of the full `Format7zF/Arc.mak`.
- `Format7zExtract/` — 7zxa.dll, extract-only for 7z archives. Built with `Z7_EXTRACT_ONLY`.
- `Format7zExtractR/` — 7zxr.dll, same as above but also `Z7_NO_CRYPTO`.

The shared build system is in `CPP/7zip/7zip.mak`. Architecture-specific assembly/optimization is pulled in via `.mak` includes (e.g., `Aes.mak`, `Crc.mak`, `LzmaDec.mak`).

The C source in `C/` provides core compression algorithms (LZMA, LZMA2, Ppmd, AES, etc.). The C++ source in `CPP/` provides the archive handlers, UI, and codec framework.

## Inno Setup-specific changes

See the `README.md` file for a list of modifications.

## Updating from upstream

Upstream releases are imported as zip archives. After merging, verify that `Format7zFInno/Arc.mak` still has the correct subset of formats — new formats added upstream to `Format7zF/Arc.mak` should be evaluated for inclusion.
