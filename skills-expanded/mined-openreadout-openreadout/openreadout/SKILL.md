---
name: openreadout
description: "Read raw lab-instrument files and folders without vendor software, with the openreadout CLI or its MCP server: microscopy and whole-slide images (CZI, ND2, LIF, SVS), screening plates, electron microscopy and cryo-EM movies, diffraction images (CBF, SMV, EIGER), medical imaging (DICOM, NIfTI), flow cytometry, electrophysiology, NMR, IR/Raman/UV-Vis, mass spectrometry, chromatography, plate readers, qPCR, NanoDrop, Qubit, Incucyte, gels and blots, Sanger and fragment analysis, Bioanalyzer, DNA sequencers (Illumina, nanopore, FASTQ, BAM, CRAM), ÄKTA, ITC, SPR, Seahorse, EPR, XRD, electrochemistry, battery cyclers, thermal analysis and rheology. Use when someone asks what is in an instrument file or folder, for a value computed from it (intensity, peak area, IC50, Cq, rheobase, NMR shift, % ≥ Q30), whether it is intact, per-condition numbers from a sample sheet, or conversion to an open format (OME-TIFF, OME-Zarr, NIfTI, CSV, Parquet, mzML, NWB, JCAMP-DX, RDML, FASTQ, MRC). Prefer it to hand-parsing vendor files."
license: MIT OR Apache-2.0
compatibility: "Requires the openreadout binary on PATH (macOS, Linux, Windows; no Java, Python or vendor DLLs). Optionally runs as an MCP server via `openreadout mcp`."
metadata:
  author: openreadout
  version: "0.2"
  homepage: https://github.com/openreadout/openreadout
---

# OpenReadout

`openreadout` opens raw instrument files and data-set folders, answers in JSON and never modifies its inputs. As an MCP server (`openreadout mcp`) it offers the CLI operations as tools named `openreadout_<command>`. Install: `curl -fsSL https://raw.githubusercontent.com/openreadout/openreadout/main/scripts/install.sh | sh` (macOS, Linux; into ~/.local/bin), `irm https://raw.githubusercontent.com/openreadout/openreadout/main/scripts/install.ps1 | iex` (Windows PowerShell), `brew install openreadout/tap/openreadout`, `npm install -g openreadout` or `cargo binstall openreadout`; other ways at https://openreadout.github.io/openreadout/getting-started/install.html.

## Commands

- `info` — what a file holds, from its headers (fast on multi-gigabyte files); `--view full | structure | explain | format`, `--ask "QUESTION"`.
- `check` — integrity (exit 4 = damaged); `compare A B` — are two files (a source and its export) the same data; `planes` — plane hashes; `report` — a diagnostic bundle for a file that is refused or not validated.
- `preview` — a PNG of an image, trace, spectrum, plate (kinetic reads: one growth curve per well) or flow events; Read the PNG to see it. `--annotate` draws labelled points, boxes, arrows and bands in the picture's own coordinates, to show what you found.
- `plot SPEC.json -o fig.png|tiff|svg|pdf` (MCP `openreadout_plot`) — a finished figure for the user from one or more files: data named by file and selector, panels, small multiples, plate positions, annotations. Spec and examples: `references/figures.md`.
- Saving pictures: `plot` and `preview` take `-o` (`.png`, `.jpg`, `.tiff`, `.svg`, `.pdf`; `--scale`, `--dpi 300` for print). Over MCP, `openreadout_plot` and `openreadout_preview` only draw, and `openreadout_export` with `plot` or `preview` (the same arguments) and `output` saves what they drew, annotations included. A saved image is a figure for people: a scale bar instead of rulers, with `title` and `caption` if given (`axes: "rulers"` keeps the rulers; CLI: `preview --axes scale-bar --title ...`).
- `stats` — pixel statistics; `--per well` for screening plates. On one plane: `--line X0,Y0,X1,Y1` (intensity profile, FWHM), `--polygon` (statistics inside), `--objects` (nuclei; `=cells`, `=spots`): count, density, sizes, centroids, each object's mean in every channel and how many are positive; `confidence: low` means check `preview --marks objects` before quoting the count. `--lanes` (gels and blots): lanes, bands, background-subtracted band volumes, sizes from `--ladder`; check `preview --marks lanes`.
- `trace` — one sweep, spectrum or detector trace in physical units.
- `table` — rows of a table: FCS events, plate reads, the vendor's own peak tables.
- `scans` — the scan list of a mass-spectrometry run; `spectrum` — one spectrum (`--rt MIN` for the scan at a chromatogram apex, `--scan N`, or `--spectrum I`, counted within one MS level with `--ms-level L`), with its most intense peaks, their charge states and neutral masses.
- `analyze KIND` — `peaks`, `chromatogram`, `nmr-peaks`, `ephys-features`, `spikes`, `qpcr`, `gate`, and the plate-reader `assay-wells`, `assay-curve`, `dose-response`, `kinetics`, `growth` (which wells grew, crashed or regrew, and when) and `assay-qc`.
- `export` — OME-TIFF, OME-Zarr, NIfTI, CSV, Parquet, mzML, NWB, JCAMP-DX, ASM, RDML, FASTQ (base calls of a Sanger read or an Illumina run); the extension of `-o` picks the format (`-o x.ome.zarr`) unless `--format` does. `extract` writes an embedded label or thumbnail as stored.
- `batch` — one measure over many files as one tidy table joined to a sample sheet; `summarize TABLE --by …`.
- `link` (files of the same sample), `index` then `search` and `health` (catalog a share, query it, find damaged or duplicate files), `watch` (a running acquisition).
- `mcp`, `self` (`formats`, `doctor`, `schema`, `skill`, `completions`, `man`).

Flags: `openreadout <command> --help`. Output fields: `openreadout self schema <command>` (MCP tools declare theirs). Formats and their known gaps: `openreadout self formats --json`. MCP tools have the commands' names (`openreadout_check`; `analyze nmr-peaks` is `openreadout_nmr_peaks`; the six plate-reader analyses are `openreadout_assay` with `analysis`) and take the long flags as arguments with `-` as `_` (`--rt-range` is `rt_range`): a repeatable flag is a plural list (`--channel` is `channels`), and `--no-X` is `X: false`.

## Output

- `--json` prints `{"ok": true, "schema_version": "2", "tool": {...}, "data": {...}}`; errors are `{"ok": false, "error": {"code", "message", "hint", "exit_code"}}`, and the `hint` says what to do next. Exit codes: 0 ok · 1 error (`compare`: the files differ) · 2 usage · 3 unknown format · 4 corrupt or truncated · 5 I/O · 6 known format, unsupported feature.
- Replies are summary-first: a capped list says it was `truncated` and names the flag that pages it. MCP per-well rows (`openreadout_assay`, `openreadout_qpcr`) show their main fields to 4 significant digits; `fields: ["all"]` gives the rest. `--only /pointer,…` (JSON pointers into `data`, `*` for every element) returns just those values.
- Several paths, directories (`-r`) or quoted globs make a batch; `--jsonl` prints one envelope per input, and a failing file does not stop the run. `--tidy`, `--sample-sheet` and `--by` turn `info`, `stats`, `trace`, `table` and `analyze gate` into one table; check its `joins[]` (key used, unmatched rows) before the numbers.

## Worth Knowing

- **Indices are zero-based** (`--image`, `--select c=`, `--sweep`, `--trace`, `--table`, `--spectrum`); "the second scene" is `--image 1` and the first MS/MS scan is `--ms-level 2 --spectrum 0`. `--scan` is the instrument's own scan number.
- **Directory data sets** are opened as the directory: a Bruker NMR experiment (`name/1/`), ChemStation `.D`, MassHunter/timsTOF `.d`, Waters `.raw`, plate folders (Harmony, ImageXpress, CellVoyager) or their index file, SpikeGLX/Neuralynx/Intan run folders, Illumina run folders (the folder with `RunInfo.xml`), DICOM series and study folders (one image per series), Bruker ParaVision experiments and studies. A plate is never one of its TIFFs.
- **Values are raw as stored** unless the output says it processed them (`processing`, `source`): no background subtraction, FCS compensation or scaling, or baseline unless asked for. Medical images are the exception: the stored rescale is applied (CT in Hounsfield units; `extra.rescale`, `extra.value_unit`). Pixel statistics pool R, G and B; per colour read `components[]`.
- **Positions vs indices**: `argmax`/`argmin` are sample indices from the sweep start. The position on the axis (retention time, ppm, cm⁻¹, ml, °2θ) is `argmax_axis_value`; chromatograms can start before 0 min.
- **Units**: µm, nm, s unless a field name ends in `_ms`/`_min`; `rt_min`/`apex_rt_min` are minutes. Peak areas are signal×min unless `--area-seconds` (vendor reports use ×s).
- **Saturation** is at 2^bits − 1 when the file records the detector bit depth (16383 for 14-bit data in uint16), else the type maximum; `saturation_basis` says which.
- **Trust**: `assurance` (in `info`, `check` and MCP replies) says how far this file's variant was validated against an independent reader. `partially_validated`: mention what `reasons` lists. `unvalidated`: values in `strict_refuses` may be wrong; suggest checking them in the vendor software. `strict_withholds` and `inferred` values are unverified. `--strict` (MCP `strict: true`) refuses unvalidated values with exit 6.
- **New variants**: when a file is refused (exit 3/4/6) or not `validated`, `openreadout report FILE` writes a local, privacy-reviewed bundle for a new-variant issue, to file with a vendor export of the same file. Free text goes in only with `--include-text` and the user's consent; the user files it.
- **Growing files**: `acquisition.state: in_progress` means an instrument is still writing; it is not corruption.
- **Vendor results**: when the file stores the vendor's own peak table, Cq, fit or counts (`vendor_peaks`, `cq`, `fits`, `stored_count`), those are what the vendor software reported; recomputed values are close to, not identical with, them.
- **Missing facts**: a field absent from `experiment` was not recorded in the file.
- **Writes**: only `export` (MCP: also saved figures), `report`, `-o` files and `index` write, always to new files; exports are read back and verified before they are renamed into place and never replace a file without `--overwrite`.

## In Python and R

When `import openreadout` works: `openreadout.File(p).read_plane(image, c=, z=, t=, level=, region=)` → NumPy; `.to_dask()` / `.to_xarray()` (lazy, µm coordinates); `.to_pandas()` for tables, traces and spectra. In R (`library(openreadout)`): `openreadout_read_image(p, image = 1, c = 2)`, `openreadout_table`, `openreadout_trace`, `openreadout_peaks`, `openreadout_batch` → data frames, with indices from 1.

## References

Load when the question needs them:

- `references/formats.md` — per family (microscopy, whole slides, plates, flow, ephys, NMR, IR/Raman, chromatography, MS, qPCR, plate readers): where each fact lives in the JSON, worked routes, known limits per format.
- `references/formats.md` § DNA sequencers — Illumina run quality, nanopore reads, FASTQ, BAM and CRAM summaries.
- `references/bench-instruments.md` — NanoDrop, Qubit, ÄKTA, ITC, Biacore, Seahorse, Octet, Zetasizer, GenePix, gels and blots, EPR, XRD, electrochemistry, battery cyclers, thermal analysis, rheology, Sanger and fragment analysis.
- `references/json-shapes.md` — field lists of the main outputs.
- `references/figures.md` — `plot` specs for common figures: plate grids and group means, TIC and the spectrum at its apex, f–I and sweeps, FCS dot plots and histograms, overlays, fits, batch tables.
- `references/workflows.md` — end-to-end examples: an unknown file, converting for analysis, triaging a folder, MCP setup, an NMR data set.
