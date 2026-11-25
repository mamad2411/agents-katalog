---
name: browser-media-wasm
description: Engineer leak-free browser media, Canvas/OffscreenCanvas, WebAudio, PDF, QR, and WebAssembly pipelines using Web Worker offloading, magic-byte validation, and deterministic ObjectURL cleanup.
---

# Browser Media, Canvas & WebAssembly Offloading (`/browser-media-wasm`)

> **Role**: Principal Browser Media & Wasm Pipeline Engineer  
> **Philosophy**: *Never freeze the UI thread. Revoke every ObjectURL you allocate. Terminate idle Workers. Validate magic bytes, not file extensions. Keep user media 100% on-device.*

Distilled from offline browser media tooling (`domodomo`), this skill governs high-throughput photo, video, audio, PDF, QR, and WebAssembly pipelines.

---

## 1. Quick Navigation & References

| Resource | Purpose |
| :--- | :--- |
| [references/canvas-worker-and-objecturl-lifecycle.md](references/canvas-worker-and-objecturl-lifecycle.md) | `URL.revokeObjectURL` pairing, Web Worker + `OffscreenCanvas` transferables, WebAudio cleanup, magic-byte checks, WASM caching. |
| [scripts/verify_media_wasm_hygiene.py](scripts/verify_media_wasm_hygiene.py) | CLI auditor flagging unrevoked `createObjectURL`, missing `worker.terminate()`, and unbounded media loops. |

---

## 2. Core Browser Media Invariants

| Resource | Hazard | Mandatory Guardrail |
| :--- | :--- | :--- |
| **Object URLs** | `URL.createObjectURL(blob)` leaks RAM across conversions | Always pair with `URL.revokeObjectURL(url)` in `try/finally` or React unmount cleanup. |
| **Main Thread** | Pixel loops, PDF parsing, or FFmpeg.wasm lock UI rendering | Offload via `Worker` + `OffscreenCanvas` + transferable `ArrayBuffer` (`postMessage(buf, [buf])`). |
| **Workers & Audio** | Orphaned workers & active `AudioContext` drain battery | Call `worker.terminate()`, `audioCtx.close()`, and `AbortController.abort()` on cancel/unmount. |
| **Untrusted Files** | Renamed `.exe` or 8000x8000 image bomb causes tab OOM | Inspect binary magic bytes (`PNG`/`JPEG`/`PDF`/`RIFF`), cap dimensions/bytes, downscale previews first. |
| **Privacy Boundary** | Hidden remote upload of user media for local tools | Keep bytes strictly client-side; zero silent network egress or analytics beacons. |

---

## 3. Leak-Free ObjectURL & Worker Pattern

```typescript
export async function processImageInWorker(file: File, signal: AbortSignal): Promise<Blob> {
  if (file.size > 50 * 1024 * 1024) throw new Error("FILE_TOO_LARGE");
  const worker = new Worker(new URL("./media.worker.ts", import.meta.url), { type: "module" });

  return new Promise<Blob>((resolve, reject) => {
    const onAbort = () => {
      worker.terminate();
      reject(new DOMException("Cancelled", "AbortError"));
    };
    signal.addEventListener("abort", onAbort, { once: true });

    worker.onmessage = (ev: MessageEvent<{ blob?: Blob; error?: string }>) => {
      signal.removeEventListener("abort", onAbort);
      worker.terminate();
      if (ev.data.error || !ev.data.blob) reject(new Error(ev.data.error ?? "MEDIA_FAILED"));
      else resolve(ev.data.blob);
    };
    worker.onerror = (err) => {
      signal.removeEventListener("abort", onAbort);
      worker.terminate();
      reject(err);
    };

    worker.postMessage({ file });
  });
}
```

---

## 4. Automated Browser Media Hygiene Auditor

```bash
python3 skills/browser-media-wasm/scripts/verify_media_wasm_hygiene.py --path . --strict
```
