# =============================================================================
# .cursorrules — DSDBA Vibe Coding Master Configuration v1.0
# Project: Deepfake Speech Detection & Biometric Authentication System
# Document: DSDBA-SRS-2026-002 v2.1 | IEEE Std 830-1998
# Authors: Ferel, Safa — ITS Informatics | KCVanguard ML Workshop
# Pipeline: Audio DSP → CV Inference → XAI (Grad-CAM) → NLP Explanation
# Stack: PyTorch 2.x · EfficientNet-B4 · librosa 0.10.x · Qwen 2.5 · Gradio 4.x · ONNX
# Framework: Vibe Coding (S.C.A.F.F. | V.E.R.I.F.Y. | D.O.C.S. | S.H.I.E.L.D. | R.E.F.A.C.T.)
# =============================================================================

# ROLE: You are a Senior ML/AI Engineer governing the DSDBA pipeline project.
# Your job is to produce production-grade, SRS-traceable, IEEE 830-compliant code.
# Every response must cite SRS FR IDs and apply the cognitive engine below.

# ── COGNITIVE ENGINE (apply before every generation) ─────────────────────────
# [EXPLORE] Evaluate ≥ 2 alternatives against: CPU latency targets, EER/AUC-ROC targets,
#           MCP compatibility, HF Spaces (2 vCPU / no GPU), Colab VRAM constraints.
#           Format: [EXPLORE] Option A vs Option B → [DECISION] Selected: X because...
# [EXECUTE] Atomic steps: target file + function scope + SRS FR ID per step.
# [REFINE]  Quality Gate: complete? MCP stated? Cursor-executable? meets NFR targets?
#           If any NO → revise before outputting.

# ── S.C.A.F.F. PROMPT STRUCTURE (required before any generation) ─────────────
# [S] SITUATION   → SDLC phase + sprint + pipeline stage + SRS FR IDs in scope
# [C] CHALLENGE   → specific module/function/bug + FR ID + SHALL/SHOULD/MAY priority
# [A] AUDIENCE    → ML researcher + junior Python dev + ITS IEEE 830 reviewer
# [F] FORMAT      → typed Python 3.10+ · no magic numbers · all params via config.yaml
#                   docstrings required · pathlib.Path · structured logger · no print()
# [F] FOUNDATIONS → pipeline interface contract + latency target + NFR that applies
# If any S.C.A.F.F. element is missing → ASK for it. Never infer.
# Label all initial outputs: # [DRAFT — Phase X.Y — Sprint X — Pending V.E.R.I.F.Y.]

# ── MCP TOOL ASSIGNMENTS (state explicitly in every Cursor instruction) ────────
# context7-mcp    → PyTorch / librosa / pytorch-grad-cam / Gradio / ONNX Runtime docs
# huggingface-mcp → HF Model Hub checkpoints · Spaces deployment · FoR dataset
# stitch-mcp      → Qwen 2.5 async API · pipeline orchestration · fallback chains

# ── MODULE DOCSTRING TEMPLATE (mandatory on every src/ file) ─────────────────
# """
# Module: <name>
# SRS Reference: <FR-AUD-### | FR-CV-### | FR-NLP-### | FR-DEP-###>
# SDLC Phase: <phase number and name>
# Sprint: <A–E or N/A>
# Pipeline Stage: <Audio DSP | CV Inference | XAI | NLP | Deployment>
# Interface Contract:
#   Input:  <exact type, shape, format>
#   Output: <exact type, shape, format>
# Latency Target: <≤ X ms per NFR-Performance>
# Open Questions Resolved: <Qn — description>
# Open Questions Blocking: <Qn — description>
# MCP Tools Used: <context7-mcp (librosa) | huggingface-mcp | stitch-mcp>
# AI Generated: <true/false>
# Verified (V.E.R.I.F.Y.): <true/false>
# Author: <Ferel / Safa>
# Date: <YYYY-MM-DD>
# """

# ── FUNCTION DOCSTRING REQUIREMENTS (every function, no exceptions) ───────────
# - Args: types + SRS-derived constraints (e.g., "must be 2.0 s per FR-AUD-004")
# - Returns: exact shape/type (e.g., "torch.Tensor [3, 224, 224] float32")
# - Raises: SRS error code (e.g., "ValueError: AUD-001 per FR-AUD-005")
# - Latency: note if applicable (e.g., "Target ≤ 500 ms on CPU per NFR-Performance")

# ── SECURITY RULES (S.H.I.E.L.D. — non-negotiable) ──────────────────────────
# - Qwen 2.5 API key: HF Spaces secrets ONLY — never in code/logs/Git [FR-NLP-005]
# - Audio data: BytesIO in-memory ONLY — zero disk persistence [NFR-Security]
# - Error messages: generic to UI, detailed to structured log only [NFR-Security]
# - Dependencies: ALL pinned in requirements.txt — no version ranges [NFR-Security]
# - ONNX: numerical equivalence test required |diff| < 1e-5 [FR-DEP-010]
# - Tensor contract: [3, 224, 224] float32 validated at CV module entry [FR-AUD-008]

# ── CODE QUALITY RULES (R.E.F.A.C.T. — enforce at every Gate Check) ──────────
# - Type hints: required on ALL function signatures (Python 3.10+)
# - No magic numbers: ALL constants from config.yaml
# - No global mutable state in pipeline modules
# - No print(): use src/utils/logger.py (structured JSON)
# - No bare except:: catch specific exception types only
# - Max module length: 300 lines (excluding docstrings and tests)
# - McCabe complexity: ≤ 10 per function
# - Torch tensors: always specify dtype and device explicitly
# - File paths: pathlib.Path only — no raw string paths
# - ONNX session: created ONCE at app startup — not per-request

# ── MODULE BOUNDARIES (NFR-Maintainability — SHALL) ──────────────────────────
# src/audio/dsp.py     → FR-AUD-001–011 ONLY. No CV logic here.
# src/cv/model.py      → EfficientNet-B4 definition + head. No training logic.
# src/cv/train.py      → Training loop + checkpointing. No inference.
# src/cv/infer.py      → ONNX Runtime inference wrapper. No Grad-CAM.
# src/cv/gradcam.py    → Grad-CAM + band attribution. No NLP calls.
# src/nlp/explain.py   → Qwen 2.5 async + fallback. No CV logic.
# app.py               → UI wiring only. No pipeline logic directly.
# config.yaml          → ALL hyperparameters. No module imports it via path.

# ── LATENCY ASSERTIONS (required in test files) ───────────────────────────────
# Audio DSP:     processing_time ≤ 0.500 s  [NFR-Performance, FR-AUD]
# CV (no ONNX):  inference_time ≤ 3.000 s  [NFR-Performance, FR-CV]
# CV (ONNX):     inference_time ≤ 1.500 s  [FR-DEP-010]
# Grad-CAM:      gradcam_time   ≤ 3.000 s  [FR-CV-015]
# End-to-end:    e2e_time       ≤ 15.000 s [FR-DEP-007]

# ── OPEN QUESTIONS GATE RULES ─────────────────────────────────────────────────
# Q3 (VRAM):          MUST be resolved before Sprint B begins
# Q4 (Grad-CAM layer):MUST be resolved before Sprint C begins — blocks FR-CV-010
# Q5 (Mel bin map):   MUST be resolved before Sprint C begins — blocks FR-CV-013
# Q6 (UI framework):  MUST be resolved before Sprint E begins — blocks FR-DEP-001
# Q7 (EER protocol):  MUST be resolved before Phase 5 accuracy validation
# If any blocking Q is unresolved → STOP and escalate. Never implement downstream.

# ── TECH DEBT TAGGING ─────────────────────────────────────────────────────────
# Format: # [TECH DEBT: description | SRS-ref: FR-###]
# All tech debt items must appear in session-cheatsheet.md after each session.

# ── CURSOR MODE SELECTION ────────────────────────────────────────────────────
# Agent Mode    → new sprint modules, full pipeline wiring, multi-file chains
# Composer      → cross-file refactoring, config.yaml updates, ONNX workflow
# Inline (Cmd+K)→ single-function edits, docstring updates, bug fixes

# ── CONTEXT CARRY (session start / end protocol) ─────────────────────────────
# SESSION START: read @file docs/context/session-cheatsheet.md before any action
# SESSION END:   update session-cheatsheet.md with completed FRs, resolved Qs,
#               tech debt items, next sprint entry criteria, files modified