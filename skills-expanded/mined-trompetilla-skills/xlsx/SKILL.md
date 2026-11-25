---
name: XLSX
description: Read and generate Excel files with correct types, dates, and cross-platform compatibility.
metadata: {"clawdbot":{"emoji":"📗","os":["linux","darwin","win32"]}}
---

## Dates

- Excel dates are serial numbers—days since 1900-01-01 (Windows) or 1904-01-01 (Mac legacy)
- 1900 leap year bug: Excel incorrectly treats 1900 as leap year—serial 60 is Feb 29, 1900 (invalid)
- Date vs number ambiguous without cell format—always check number format code, not just value
- Times are fractional days: 0.5 = 12:00 noon; 0.25 = 06:00

## Numbers

- 15-digit precision limit—larger numbers silently truncate; use text format for IDs, phone numbers
- Leading zeros stripped from numbers—format as text or use custom format `00000`
- Scientific notation triggers automatically—`1E10` becomes number; quote if literal text
- Currency/percentage stored as numbers—formatting is display-only, raw value differs

## Text & Encoding

- Shared strings table stores unique text once—large files reuse indices; libraries handle this
- 32,767 character limit per cell
- Newlines in cells: `\n` works but cell needs wrap text format to display
- Unicode fully supported in XLSX—but legacy XLS has codepage issues

## Structure

- Row limit: 1,048,576; column limit: 16,384 (XFD)—XLS limit is 65,536 × 256
- Merged cells: only top-left cell holds value—reading others returns empty
- Hidden rows/columns still contain data—don't assume hidden means excluded
- Sheet names max 31 chars; forbidden: `\ / ? * [ ]`

## Formulas

- Cell may contain formula and cached result—some readers return formula, others cached value
- Formulas recalculate on open—cached values may be stale; force recalc or read formula
- Array formulas (CSE/dynamic) have different behavior across Excel versions
- External references `[Book.xlsx]Sheet!A1` break when file moves

## Cross-Platform

- Windows vs Mac Excel: date system (1900 vs 1904) can differ—check workbook setting
- LibreOffice/Google Sheets: some Excel features unsupported—test roundtrip
- XLSM contains macros (security risk); XLSB is binary (faster, less compatible)
- Password protection is trivial to break—not real security; encrypt file externally

## Common Library Issues

- Empty rows at end: some writers pad to fixed size—trim when reading
- Type inference on read: numbers-as-text stay text; explicit conversion needed
- Memory: loading large files fully into RAM—use streaming reader for big files
- Column letters vs indices: A=0 or A=1 varies by library—verify convention
