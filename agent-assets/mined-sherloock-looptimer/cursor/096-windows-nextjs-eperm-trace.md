---
description: "Windows: fix Next.js EPERM on .next/trace (Defender Controlled folder access)"
globs: "**/*"
---

## Symptom
- `Error: EPERM: operation not permitted, open '<project>\\.next\\trace'` during `next dev`.

## Fix checklist (Windows)
- Stop all Next/Node dev servers that may lock `.next` or ports (3000/3001).
- Delete the `.next` directory, then restart `npm run dev`.

## Windows Security note
- Defender “Exclusions” are not enough if **Controlled folder access** is enabled.
- If Controlled folder access is enabled, allow:
  - `C:\\Program Files\\nodejs\\node.exe`
  - (optional) `C:\\Program Files\\cursor\\resources\\app\\resources\\helpers\\node.exe`
  - (optional) the project folder (e.g. `F:\\Fejlesztes\\projects\\my\\timer`)
