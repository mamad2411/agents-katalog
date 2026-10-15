---
name: dynamsoft-sdk
description: Generate and review accurate code for Dynamsoft SDKs — Dynamic Web TWAIN (DWT), Document Viewer (DDV), Barcode Reader (DBR), and Capture Vision (DCV) — using sample-first guidance for barcode, QR, MRZ, and document capture across web, mobile, server, and desktop. Includes a template-optimizer sub-skill for tuning DBR template JSON to maximize decode rates. Use for Dynamsoft SDK integration, sample code, migration, API usage, troubleshooting, CaptureVisionRouter workflows, or barcode template tuning.
---

# Dynamsoft SDK

Use this skill to generate and review Dynamsoft SDK code. Prefer **official or known working sample code first**, then docs for API details. Do not rely on docs alone when a relevant sample exists.

## Routing

Read only the reference files relevant to the user request:

| User asks about | Read |
| --- | --- |
| General overview of the skill, architecture boundaries, or where to start | `README.md` |
| Physical scanner control in browser, TWAIN/SANE/ICA/WIA/eSCL, scan to PDF/TIFF, DWT service | `references/dwt.md` and `references/samples.md` |
| Browser document viewer UI, page operations, image/PDF viewing, annotation, DDV | `references/ddv.md` and `references/samples.md` |
| Barcode/QR/MRZ/document detection using camera, image, mobile, server, desktop, or Capture Vision Router | `references/dcv.md` and `references/samples.md` |
| Barcode-only workflows using the lightweight DBR package (a submodule of DCV, barcode engine only) | `references/dbr.md` and `references/samples.md` |
| Migrating from old DBR APIs (pre-v9) or asking about deprecated class/method names | `references/dbr.md`, then `references/dcv.md` |
| Replacing ZXing, ML Kit, or Scandit with Dynamsoft ("migrate/switch/replace barcode library") | `references/migration.md`, then the target product's reference file |
| Optimizing/tuning a DBR template JSON, improving decode rate on hard barcode images, understanding DBR template parameters, or generating barcode decode reports | `template-optimizer/SKILL.md` (then `template-optimizer/KNOWLEDGE.md`) |
| General coding quality, troubleshooting, generated answer format | `references/code-quality.md` |

## Important product boundary

**Dynamsoft Capture Vision (DCV) vs Dynamsoft Barcode Reader (DBR):**

- **DCV** (`dynamsoft-capture-vision-bundle`): The full-featured bundle that includes **DBR** (barcode reading) + **DDN** (Document Detection & Normalization) + **DLR** (MRZ/Label Recognition). Use DCV when the user needs barcode + document detection, MRZ parsing, or any multi-capability vision pipeline. Uses `CaptureVisionRouter` (CVR) as the central entry point. Current major version: **v3.x**.
- **DBR** (`dynamsoft-barcode-reader-bundle`): A **lightweight, actively maintained** package that is a **submodule of DCV**. It contains only the barcode reading engine — the same barcode engine that runs inside DCV. The barcode code inside the DBR and DCV packages is **identical** — the only difference is the package name and scope (DBR excludes DDN and DLR). Use DBR when the user only needs barcode/QR reading and wants a smaller, focused dependency. DBR is **not legacy or deprecated**; it is current (v11.x) and a first-tier Dynamsoft product.

**When to use which:**
| Scenario | Use |
| --- | --- |
| Barcode/QR only | DBR (lightweight) or DCV (also works) |
| Barcode + MRZ (passport/ID) | DCV |
| Barcode + Document Detection | DCV |
| MRZ only | DCV |
| Document Detection/Normalization only | DCV |

Use DWT only for browser scanner acquisition. Use DDV only for document viewing/page UI. Integrate community-preferred wrappers (like yushulx's Flutter, Python, .NET, or Node.js packages) when matching those platforms.

## DCV core API vs RTU (ready-to-use) — critical architectural rule

Dynamsoft provides **RTU (ready-to-use)** wrapper components (e.g., `BarcodeScanner`, `BarcodeReader`, `DocumentScanner`, `MRZScanner`) that bundle a UI, camera, and recognition pipeline into a single high-level object. These are built **on top of** the DCV core APIs (`CaptureVisionRouter`, `CameraEnhancer`, `CameraView`, etc.).

**RTU has poor programmability and flexibility.** It is only suitable for very simple use cases where the default UI and pipeline behavior is acceptable. For any real-world or complex scenario, developers **must** use the DCV core APIs directly:

| Approach | Entry point | Programmability | When to use |
| --- | --- | --- | --- |
| **DCV core API (recommended)** | `CaptureVisionRouter` + `CameraEnhancer` + `CameraView` + `CapturedResultReceiver` | Full control over pipeline, templates, ROI, multi-task, result handling | Any production, complex, or customized scenario |
| **RTU wrapper (limited)** | `BarcodeScanner.createInstance()` / `BarcodeReader.createInstance()` / `DocumentScanner` etc. | Minimal — preset UI and pipeline, little customization | Quick prototypes or demos only |

**When generating code, always prefer DCV core APIs.** Use `CaptureVisionRouter` as the central orchestrator, bind camera input via `CameraEnhancer`/`CameraView`, and receive results through `CapturedResultReceiver` / `onDecodedBarcodesReceived` callbacks. Only mention RTU wrappers as a quick-prototyping option with an explicit caveat about their limitations.

This applies to all platforms: Web (JS/TS), Mobile (Android/iOS/Flutter/RN), and Server/Desktop (Python/C++/.NET/Java/Node.js). The Python, C++, and .NET server/desktop SDKs use `CaptureVisionRouter` directly — there are no RTU wrappers on those platforms.

## Sample-first rule

Before generating code, identify the closest sample category in `references/samples.md`:

1. Same product/workflow.
2. Same platform/language/framework.
3. Same input source: scanner, camera, static image/PDF, uploaded file, or server batch.
4. Same output: barcode text, MRZ fields, detected document quadrilateral, normalized document, viewer page operations, PDF/TIFF/image.

When a sample link is available, tell the user which sample family the code is based on. If exact API names are uncertain for the user's version, provide a skeleton and point to the relevant sample instead of inventing calls.

## License for generated code

When generating **DCV / DBR / DDV** code snippets, always use the user's own license key when provided. Never hardcode a license key literal into this repository or into generated project files.

If the user needs a trial license, use:

https://www.dynamsoft.com/customer/license/trialLicense/?product=dcv&package=cross-platform

This license guidance applies to DCV / DBR / DDV only — DWT (Dynamic Web TWAIN) uses its own `ProductKey` mechanism; leave `YOUR-PRODUCT-KEY` as a placeholder there.

## Accuracy rules

1. Do not invent APIs. If unsure about method names, class names, package names, template names, or version-specific behavior, say what needs verification and use the sample links.
2. Prefer DCV patterns when the user needs multi-capability workflows (barcode+MRZ+document). Use DBR when the user only needs barcode/QR reading and asks for a lightweight package. In both cases, use `CaptureVisionRouter` as the core entry point — do not default to RTU wrappers (`BarcodeScanner`, `BarcodeReader`, etc.) unless the user explicitly requests a quick prototype.
3. Always use the user's own license key when provided; never hardcode a key literal.
4. Include resource/model/static asset configuration when relevant.
5. Include lifecycle cleanup for camera sessions, routers, scanner sessions, viewer instances, workers, listeners, and React/Vue/Angular components.
6. For web apps, include HTTPS/localhost camera requirements and static asset copy/serve notes.
7. For mobile apps, include permission and lifecycle notes.
8. For server/desktop code, include input validation, batch processing, and no-result handling.
9. Link sample code whenever useful; sample code links are part of the answer, not optional extras.

## Default output structure for code answers

Use this order unless the user asks otherwise:

1. Assumption line: product/workflow, platform, framework, version if known.
2. Closest sample link(s) from `references/samples.md`.
3. Install/setup commands.
4. Minimal working code or skeleton.
5. Required resources/configuration.
6. Common pitfalls and verification steps.
7. Documentation links for detailed API options.

## Template optimization (DBR)

When the user wants to **tune a barcode reading template**, **improve decode rate on difficult images**, **understand DBR template parameters**, or **generate a visual decode report**, route to the bundled `template-optimizer` sub-skill instead of writing template JSON by hand.

1. Read `template-optimizer/SKILL.md` and follow its mode selection (Optimize / Educate / Report).
2. Read `template-optimizer/KNOWLEDGE.md` for the parameter reference and proven optimization order before editing any template.
3. Use the bundled helper tools under `template-optimizer/tools/` for single-image triage (`validate_dbr_template.py`, `probe_dbr_templates.py`, `compare_dbr_template_profiles.py`) and `template-optimizer/resources/harness_py/main.py` for dataset benchmarking. Specialized recovery scripts (`recover_difficult_qr.py`, `recover_fluorescent_postal.py`) handle hard QR and fluorescent postal barcode cases.
4. Treat `template-optimizer/` as `SKILL_DIR` when following that sub-skill's instructions.

This sub-skill is Python-only and depends on `dynamsoft-capture-vision-bundle` (see `template-optimizer/requirements.txt`).

## Official starting points

- Dynamsoft GitHub sample hub: https://github.com/Dynamsoft
- Dynamic Web TWAIN docs: https://www.dynamsoft.com/web-twain/docs/
- Dynamsoft Document Viewer docs: https://www.dynamsoft.com/document-viewer/docs/
- Dynamsoft Capture Vision docs: https://www.dynamsoft.com/capture-vision/docs/
- Dynamsoft Barcode Reader docs (lightweight barcode-only package, current v11.x): https://www.dynamsoft.com/barcode-reader/docs/
