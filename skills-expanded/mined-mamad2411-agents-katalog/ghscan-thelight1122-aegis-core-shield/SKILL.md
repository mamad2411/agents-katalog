# AEGIS Issue Manifest — Cycle 1

## File: .agent/skills/aegis-issue-manifest/SKILL.md

## Scope: Workspace skill — loaded on demand when agents need issue detail

## Loaded by: BM-DIAG, BM-DEV, BM-QA

---

## I-01 — User Guide: Out of Parameter Language

**Tier:** DOC  
**File:** docs/USERGUIDE.md

| Current (OUT OF SPEC)                                                                 | Required Replacement                                                                              |
| ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| help refine, evaluate, and guide prompts                                              | support observation and reflection of prompts                                                     |
| guide prompts toward a safe, coherent, and highly transparent system response mapping | surface coherence and fracture observations for transparent system response mapping               |
| guide the user on how to realign the prompt correctly                                 | return observations about the signal patterns present                                             |
| Returns a formatted Return Packet with the underlying reason for returning            | Returns a formatted Return Packet with observations about signal patterns that produced fractures |

**Acceptance:** grep USERGUIDE.md for `evaluate`, `guide toward`, `correctly`, `realign correctly` — zero results. Introduction reads with no directive or judgmental framing.

---

## I-02 — Installation: 'Coercive prompt' Label

**Tier:** DOC  
**File:** docs/INSTALLATION.md

| Current (OUT OF SPEC)                   | Required Replacement                                               |
| --------------------------------------- | ------------------------------------------------------------------ |
| `# Example: Coercive prompt (returned)` | `# Example: Prompt containing force-pattern indicators (returned)` |

**Acceptance:** grep INSTALLATION.md for `Coercive prompt`, `coercive` — zero results.

---

## I-03 — Technical Docs: 'enforce' Out of Parameter

**Tier:** DOC  
**File:** docs/TECHNICAL.md

| Current (OUT OF SPEC)                            | Required Replacement                                 |
| ------------------------------------------------ | ---------------------------------------------------- |
| enforce DataQuad logging                         | maintain DataQuad logging continuity                 |
| Any further instance of `enforce` as system verb | preserve / maintain / sustain / ensure continuity of |

**Acceptance:** grep TECHNICAL.md for `enforce`, `mandate` — zero results as system verbs.

---

## I-04 — PEER Capture Must Precede All Processing

**Tier:** ARCH  
**Files:** gate-logger.ts, entry point

**Problem:** gate-logger.ts records gate outcomes. PEER must capture raw signal BEFORE tokenization. PEER_CAPTURE must be the first action at the entry point.

**Required code pattern:**

```typescript
export async function processInput(rawInput: string) {
  // FIRST ACTION: PEER capture before any processing
  await gateLogger.append({
    event: "PEER_CAPTURE",
    timestamp: new Date().toISOString(),
    hash: sha256(rawInput),
    raw: rawInput,
  });
  const units = tokenize(rawInput);
  const scores = scoreVirtues(units);
  return runIDSWithGate(rawInput, units, scores);
}
```

**Acceptance:** Unit test confirms first JSONL entry for any input is event type `PEER_CAPTURE` containing raw hash. Test name: `I-04: PEER_CAPTURE precedes all processing`.

---

## I-05 — IDS Must Run Universally

**Tier:** ARCH  
**Files:** ids-processor.ts, discernment-gate.ts

**Problem:** IDS currently runs only on admitted inputs. All signals must pass through IDS.

**Required code pattern:**

```typescript
export type IDSPath = "admitted" | "shallow-return" | "deep-return";

export function runIDS(input: string, units: Unit[], path: IDSPath): IDSResult {
  const identified = identify(units); // ALL inputs
  const defined = define(identified); // ALL inputs
  const suggestions =
    path === "admitted"
      ? suggestPathways(defined)
      : suggestFractureObservations(defined, path);
  return { path, identified, defined, suggestions };
}

export function discernmentGate(
  raw: string,
  units: Unit[],
  scores: VirtueScores,
) {
  const adjusted = applyToleranceBand(scores, TOLERANCE_BAND);
  const fractures = countFractures(adjusted);
  const path: IDSPath =
    fractures === 0
      ? "admitted"
      : fractures === 1
        ? "shallow-return"
        : "deep-return";
  return {
    path,
    integrity: fractures === 0 ? 1 : 0,
    adjusted,
    idsResult: runIDS(raw, units, path),
  };
}
```

**Acceptance:** Tests confirm admitted and returned inputs both produce full IDSResult. Test prefix: `I-05:`.

---

## I-06 — Return Packet Must Declare IDS Origin

**Tier:** ARCH  
**Files:** ids-processor.ts, discernment-gate.ts

**Problem:** Return Packet suggestions have no declared origin. source: 'IDS' must be explicit.

**Required type:**

```typescript
export interface ReturnPacket {
  source: "IDS";
  path: "shallow-return" | "deep-return";
  depth: "shallow" | "deep";
  fracture_locations: FractureMap;
  ids_observations: IDSResult;
}
```

**Acceptance:** `ReturnPacket.source === 'IDS'`. No suggestion logic outside ids-processor.ts. Test prefix: `I-06:`.

---

## I-07 — Nebula Vision: Remove Severity Colour Shifts

**Tier:** UI  
**Files:** Dashboard.tsx, Dashboard.css

**Problem:** Hue shifts (red/amber/green) per integrity score encode good/bad valence — Out of Parameters by Widget UI Guardrails.

| Current (OUT OF SPEC)                        | Required Replacement                                                                 |
| -------------------------------------------- | ------------------------------------------------------------------------------------ |
| Hue shifts red/amber/green per score         | Single-hue saturation variation only. No red/green valence.                          |
| Colour encodes fracture presence as severity | Opacity or saturation for intensity — no valence. Document encoding in code comment. |
| No explanatory label                         | Add: `Signal coherence pattern — reflects signal structure, not quality.`            |

**Acceptance:** Visual review — reviewer cannot determine admitted vs returned from visual alone without reading text output. Label visible in default view.

---

## I-08 — Proportional Routing: Replace Pure Binary Gate

**Tier:** ARCH  
**Files:** discernment-gate.ts, ids-processor.ts

**Problem:** All non-admitted inputs return identically regardless of fracture count. Three-path routing needed.

**Required routing logic:**

```typescript
function computePath(adjusted: AdjustedScores): IDSPath {
  const n = Object.values(adjusted).filter((s) => s < 1.0).length;
  return n === 0 ? "admitted" : n === 1 ? "shallow-return" : "deep-return";
}
// result.admitted and result.integrity remain backward-compatible
```

**Routing rules:**

- 0 fractures → admitted
- 1 fracture → shallow-return
- 2+ fractures → deep-return

**Acceptance:** Three-path tests pass. `result.admitted` backward-compatible. `ReturnPacket.depth` field present. Test prefix: `I-08:`.
