# FileConverter — AI Context Document

> **Last updated:** 2026-09-04
> **Version:** v2.0.1
> **Language:** Python 3.12+
> **Framework:** PySide6 (Qt 6)
> **Platform:** Windows (primary), macOS (partial support)

## 1. Project summary

FileConverter is a desktop application that combines common file-conversion tasks
in one interface. Users add files through drag and drop or a file picker. The
application detects the input type and presents only compatible operations.

| Source | Target | Engine | Main dependency |
|---|---|---|---|
| Image | PDF | `core/image_to_pdf.py` | Pillow |
| Image | JPG/PNG/WEBP | `core/image_convert.py` | Pillow |
| Word (`.doc`, `.docx`) | PDF | `core/word_to_pdf.py` | docx2pdf + Microsoft Word |
| Multiple PDFs | One PDF | `core/pdf_merge.py` | pypdf |
| PDF | Separate PDFs | `core/pdf_split.py` | pypdf |
| PDF | PNG/JPG | `core/pdf_to_image.py` | PyMuPDF |
| PDF | DOCX | `core/pdf_to_word.py` | pdf2docx |

## 2. Repository map

```text
FileConverter/
├── main.py                    Application entry point and global QSS theme
├── app_info.py                Shared name, version, license, and source metadata
├── build.py                   PyInstaller build workflow
├── package_release.py         Portable ZIP and SHA-256 generator
├── installer.iss              Inno Setup configuration
├── requirements.txt           Pinned runtime dependencies
├── requirements-build.txt     Pinned build dependencies
├── README.md                  Setup, usage, testing, and release guide
├── LICENSE                    GNU AGPLv3 license
├── THIRD_PARTY_NOTICES.md     Dependency license summary
├── PRIVACY.md                 Local-processing privacy notice
├── CHANGELOG.md               Release history
├── TODO.md                    Roadmap and project status
├── assets/                    PNG and Windows ICO assets
├── core/                      UI-independent conversion logic
├── ui/                        PySide6 user interface
└── tests/                     unittest unit and regression tests
```

## 3. Architecture

`main.py` creates the `QApplication`, applies the global dark theme, and opens
`MainWindow`. `MainWindow` owns one `SmartPanel`, which manages a three-scene flow:

```text
SCENE_EMPTY → SCENE_ACTIONS → SCENE_PROGRESS
     ↑                              │
     └──────────── New operation ───┘
```

The data flow is:

```text
DropZone/File dialog
  → SmartPanel._queue_paths()
  → optional PathScanWorker
  → file_detector.detect_type()
  → matching action page
  → ConversionWorker
  → ProgressWidget
```

All expensive conversion and directory-scanning work must run outside the UI
thread. UI updates must be delivered through Qt signals and slots.

## 4. Core contracts

Conversion functions follow this shape:

```python
def convert_xxx(
    ...,
    progress_callback: Callable[[int], None] | None = None,
    status_callback: Callable[[str], None] | None = None,
    cancel_check: Callable[[], bool] | None = None,
) -> str:
    ...
```

- Return the output file or directory path on success.
- Raise an exception on failure; never fail silently.
- Raise `CancelledException` when `cancel_check()` returns `True`.
- Use atomic output writes when producing a single file.
- Remove outputs created by the current run when a batch fails or is cancelled.
- Never overwrite source files or pre-existing outputs without explicit user intent.
- Keep heavy optional dependencies as lazy imports inside conversion functions.

### File detection

`core/file_detector.py` returns one of `image`, `word`, `pdf`, `mixed`, or
`unsupported`. Folder expansion is recursive, deterministic, filtered to supported
extensions, case-insensitively deduplicated, and cancellable.

### Output behavior

| Operation | Output behavior |
|---|---|
| Image to PDF | User-selected folder, collision-free `converted_images.pdf` |
| Image format | User-selected folder, collision-free source-based names |
| Word to PDF | One collision-free PDF per Word document |
| PDF merge | User-selected PDF path |
| PDF split | Unique `split_output` directory |
| PDF to image | Unique `pdf_pages` directory |
| PDF to Word | Collision-free DOCX in a user-selected folder |

PDF to Word is intentionally non-cancellable once the third-party conversion call
begins because interrupting it cannot be guaranteed to leave resources consistent.

## 5. User interface

`ui/panels/smart_panel.py` is the main flow controller. It owns file selection,
type detection, action pages, output dialogs, worker connections, and result handling.

The action stack contains:

| Index | Input state | Actions |
|---:|---|---|
| 0 | Images | Create PDF; convert image format |
| 1 | Word documents | Convert to PDF |
| 2 | One PDF | Split; render images; convert to Word |
| 3 | Multiple PDFs | Merge |
| 4 | Mixed types | Guidance message |
| 5 | Unsupported input | Error message |

`ui/drop_zone.py` accepts local files and directories. Filtering and recursive
folder expansion belong to `file_detector` and `SmartPanel`, not the drop widget.

`ui/progress_widget.py` displays running, success, error, and cancelled states. It
also exposes cancel, show-output, and new-operation controls.

## 6. Development rules

- Write all user-facing UI, dialog, status, and error text in clear international English.
- Write all comments, docstrings, documentation, build output, and installer text in English.
- Use `pathlib.Path` for filesystem paths.
- Use Python 3.12+ type annotations and `X | None` union syntax.
- Use `frozenset` for extension collections.
- Keep conversion dependencies lazy-loaded where practical.
- Keep platform-specific behavior explicit and provide actionable errors.
- Do not access UI widgets directly from worker threads.
- Clean up finished workers with `deleteLater()`.
- Preserve the existing dark visual system and use unique `objectName` values for QSS hooks.
- Make child widgets transparent when parent-card styling could cascade unexpectedly.
- Add or update regression tests whenever user-visible behavior changes.

## 7. Adding a conversion engine

1. Add a focused module under `core/`.
2. Follow the callback, cancellation, exception, and output-safety contracts above.
3. Add supported extensions to `core/file_detector.py` if needed.
4. Add an action page and launcher in `SmartPanel`.
5. Update file-dialog filters and documentation.
6. Add unit tests for success, validation, failure cleanup, and cancellation.
7. Run the full test suite and a representative real conversion.

## 8. Dependencies and licensing

Runtime dependencies are pinned in `requirements.txt`; build dependencies are pinned
in `requirements-build.txt`. Microsoft Word is a system dependency for Word to PDF.

The project is licensed under `AGPL-3.0-only`, in part because PyMuPDF is used under
its AGPL option. Preserve `LICENSE`, `PRIVACY.md`, `THIRD_PARTY_NOTICES.md`, and the
in-app About notice in distributed packages. Review new direct and transitive
dependencies before every public release.

## 9. Build and release

```powershell
python -m pip install -r requirements-build.txt
python build.py
# Compile installer.iss with Inno Setup 6
python package_release.py
```

`build.py` removes only the project-local `build/` and `dist/` directories before
building. It uses the active Python interpreter to run PyInstaller and creates
`dist/FileConverter.exe`.

`installer.iss` creates a per-user English Windows installer in `dist/` and includes
the project license, privacy notice, changelog, and third-party notices.

`package_release.py` creates the versioned portable ZIP and `SHA256SUMS.txt`.

## 10. Known limitations and technical debt

- Encrypted PDFs are unsupported.
- PDF to Word does not perform OCR and may approximate complex layouts.
- Multi-frame TIFF and animated WEBP handling is not yet explicit.
- Large image batches may consume substantial memory.
- Structured logging is not implemented.
- `SmartPanel` should eventually be split into smaller components.
- CI test/build verification is not implemented.
- Public binaries are not yet signed with a trusted Windows code-signing certificate.

## 11. Commands

```powershell
# Install runtime dependencies
python -m pip install -r requirements.txt

# Start the application
python main.py

# Run all tests
python -m unittest discover -s tests -v

# Install build dependencies and build the standalone executable
python -m pip install -r requirements-build.txt
python build.py
```
