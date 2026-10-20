---
alwaysApply: true
---

# A2A Symbol Dictionary (Architect's Dialect)

**Version:** 2.1.0 (Updated for Vector Native Hybrid Format)
**Purpose:** Defines the **Cipher** (Symbols) and **Frames** (Metaphors) for the Architect's Dialect.

---

## 1. Frames (`Ω:`) - The "Fourth Element"

| Symbol | Name | Vibe/Intent |
| :--- | :--- | :--- |
| `Ω:CONSTRUCTION` | Construction | Blueprint-first, solid foundations, measure twice cut once. |
| `Ω:SURGERY` | Surgery | Sterile, precise, minimal invasion, do no harm. |
| `Ω:GARDENING` | Gardening | Pruning, weeding, nurturing, organic improvement. |
| `Ω:ARCHAEOLOGY` | Archaeology | Careful excavation, understanding history, preserving context. |
| `Ω:HEIST` | The Heist | High coordination, specialized roles, precise timing, get in/get out. |
| `Ω:FACTORY` | The Factory | Mass production, standardization, efficiency, assembly lines. |

---

## 2. Personas (`P:`)

| Symbol | Name | Role |
| :--- | :--- | :--- |
| `P:ARCH` | Architect | Strategic planning, blueprints. |
| `P:EXEC` | Executor | Implementation, code writing. |
| `P:DEBUG` | Debugger | Triaging and fixing bugs. |
| `P:AUDIT` | Auditor | Verification and review. |
| `P:DREAMER` | Dreamer | Vision and innovation. |
| `P:EXTEND` | Extension Analyzer | Analyzes extension feasibility. |
| `P:REALITY` | Reality Checker | Forces working examples. |

---

## 3. Laws (`L:`)

| Symbol | Name | Reference |
| :--- | :--- | :--- |
| `L:I` | Investigate First | `patterns.mdc` |
| `L:II` | API Integration | `patterns.mdc` |
| `L:III` | Schema Mapping | `patterns.mdc` |
| `L:III.5` | Response Object Handling | `patterns.mdc` |
| `L:IV` | Atomicity | `patterns.mdc` |
| `L:V` | Root Cause Analysis | `patterns.mdc` |
| `L:VI` | Innovation | `patterns.mdc` |
| `L:VII` | Event Loop | `patterns.mdc` |
| `L:VIII` | Redis Timeout Hierarchy | `patterns.mdc` |
| `L:IX` | HTTP Client Singleton | `patterns.mdc` |
| `L:X` | Structured Output | `patterns.mdc` |
| `L:XI` | Single Source of Truth | `patterns.mdc` |
| `L:XII` | React Hooks Ordering | `patterns.mdc` |
| `L:XIII` | Conflict Resolution | `patterns.mdc` |

---

## 4. Patterns (`PT:`)

| Symbol | Name | Reference |
| :--- | :--- | :--- |
| `PT:1` | Full-Stack API | `patterns.mdc` |
| `PT:2` | Backend-to-Convex Bridge | `patterns.mdc` |
| `PT:3` | Schema Mapping | `patterns.mdc` |
| `PT:4` | Atomicity & Thread Safety | `patterns.mdc` |
| `PT:4.5` | HTTP Client Singleton | `patterns.mdc` |
| `PT:5` | Centralized Abstraction | `patterns.mdc` |
| `PT:6` | Toolkit Usage | `patterns.mdc` |
| `PT:7` | Service Function Refactoring | `patterns.mdc` |
| `PT:8` | Tool Context Injection | `patterns.mdc` |
| `PT:9` | UI Component Dependency Verification | `patterns.mdc` |
| `PT:10` | Response Object Handling | `patterns.mdc` |
| `PT:11` | Function Signature Verification | `patterns.mdc` |
| `PT:11.5` | Component Prop Type Verification | `patterns.mdc` |
| `PT:12` | Context Enrichment via ContextProfile | `patterns.mdc` |
| `PT:13` | Atomic Parent-Child Updates | `patterns.mdc` |
| `PT:14` | Duplicate Detection Protocol | `patterns.mdc` |
| `PT:15` | Post-Action Registration & Usage | `patterns.mdc` |
| `PT:16` | Validator Centralization | `patterns.mdc` |
| `PT:17` | Relationship Investigation | `patterns.mdc` |
| `PT:18` | userId Always Required | `patterns.mdc` |
| `PT:19` | Atomic Multi-Entity Initialization | `patterns.mdc` |
| `PT:20` | Stable Deduplication Keys | `patterns.mdc` |
| `PT:21` | Multi-Agent Session Management | `patterns.mdc` |
| `PT:22` | Real Integration Testing | `patterns.mdc` |
| `PT:23` | External Library Investigation | `patterns.mdc` |
| `PT:24` | Adding a New Artifact Type | `patterns.mdc` |
| `PT:39` | Blueprint Status Management | `patterns.mdc` |
| `PT:40` | Blueprint Type Detection | `patterns.mdc` |
| `PT:41` | Component-First Development | `patterns.mdc` |
| `PT:DREAMER_MINIMALIST` | Minimalist Dream (Deletion) | `run_dreamer.md` |
| `PT:DREAMER_CENTRALIZATION` | Centralization Dream | `run_dreamer.md` |
| `PT:DREAMER_INVERSION` | Inversion Dream | `run_dreamer.md` |

---

## 5. Workflow (`WF:`)

| Symbol | Name | Description |
| :--- | :--- | :--- |
| `WF:STEP0` | Inquisition/Investigation | Investigation phase. |
| `WF:STEP1` | Planning/Design | Design phase. |
| `WF:STEP2` | Execution/Generation | Implementation phase. |
| `WF:STEP3` | Contracts/Verification | Contract definition or verification phase. |
| `WF:STEP4` | Capability Assessment | Capability assessment phase. |
| `WF:FINAL` | Final Verification | Final verification and consolidation phase. |
| `WF:PHASE1` | Phase 1 | First phase of multi-phase workflow. |
| `WF:PHASE2` | Phase 2 | Second phase of multi-phase workflow. |
| `WF:PHASE3` | Phase 3 | Third phase of multi-phase workflow. |
| `WF:PHASE4` | Phase 4 | Fourth phase of multi-phase workflow. |
| `WF:PHASE5` | Phase 5 | Fifth phase of multi-phase workflow. |
| `WF:PHASE6` | Phase 6 | Sixth phase of multi-phase workflow. |
| `WF:PHASE7` | Phase 7 | Seventh phase of multi-phase workflow. |

---

## 6. Output (`O:`)

| Symbol | Name | Path |
| :--- | :--- | :--- |
| `O:BLUEPRINTS` | Blueprints | `plans/{username}/active/blueprints/` |
| `O:REVIEWS` | Reviews | `plans/{username}/active/reviews/` |
| `O:INNOVATIONS` | Innovations | `plans/{username}/active/innovations/` |
| `O:DEBUGGING` | Debugging | `plans/{username}/active/debugging/` |
| `O:EXTENSION_ANALYSIS` | Extension Analysis | `plans/{username}/active/extension_analysis/` |
| `O:REALITY_CHECKS` | Reality Checks | `plans/{username}/active/reality_checks/` |
| `O:SPECS` | Specs | `plans/{username}/active/specs/` |

---

## 7. Mandates (`M:`)

| Symbol | Name | Description |
| :--- | :--- | :--- |
| `M:CREATE_BP` | Create Blueprint | Create a blueprint for execution. |
| `M:EXECUTE_BP` | Execute Blueprint | Execute a blueprint. |
| `M:INNOVATE` | Innovate | Create new patterns and gold standards. |
| `M:TRIAGE` | Triage | Triage and fix bugs. |
| `M:FIND_MISSED` | Find Missed | Find what was missed in implementation. |
| `M:ANALYZE_EXTENSION` | Analyze Extension | Analyze extension feasibility. |
| `M:FORCE_WORKING_EXAMPLE` | Force Working Example | Force working example before planning. |

---

## 8. References (`R:`)

| Symbol | Name | Path |
| :--- | :--- | :--- |
| `R:philosophy.mdc` | Philosophy | `rules/philosophy.mdc` |
| `R:patterns.mdc` | Patterns | `rules/patterns.mdc` |
| `R:global.mdc` | Global Rules | `rules/global.mdc` |
| `R:documentation_philosophy.md` | Documentation Philosophy | `rules/documentation_philosophy.md` |
| `R:username_resolution.mdc` | Username Resolution | `rules/username_resolution.mdc` |

---

## 9. Triage Categories (`T:`)

| Symbol | Name | Description |
| :--- | :--- | :--- |
| `T:C1` | Simple Fix | Simple fix (typo, missing await, response.get). Fix immediately. |
| `T:C2` | Systemic Failure | Systemic failure (L:II violation, L:IV failure, root cause). Post-mortem required. |

---

## 10. Blueprint Types (`BT:`)

| Symbol | Name | Description |
| :--- | :--- | :--- |
| `BT:SINGLE` | Single Blueprint | One file, all phases, sequential execution. |
| `BT:MASTER` | Master Blueprint | Master blueprint with mini-blueprints. |
| `BT:MINI` | Mini Blueprint | Self-contained mini-blueprint. |

---

## 11. Audit Types (`AT:`)

| Symbol | Name | Description |
| :--- | :--- | :--- |
| `AT:PATTERN` | Pattern Audit | Find Gold Standard in patterns.mdc. |
| `AT:ATOMICITY` | Atomicity Audit | Identify atomicity violations. |
| `AT:INNOVATION` | Innovation Audit | Identify L:VI targets. |
| `AT:ASYNC` | Async Audit | Verify signal handlers, lifespan, fallback chains. |
| `AT:BRIDGE` | Bridge Audit | Verify backend toolkit paths mirror Convex HTTP paths. |
| `AT:PARENT_CHILD` | Parent-Child Audit | Verify atomic parent-child updates. |
| `AT:REDIS` | Redis Audit | Verify timeout hierarchy, pools, lazy init. |
| `AT:TRANSLATION` | Translation Audit | Identify user-facing text requiring translation. |
| `AT:COMPONENT` | Component Audit | Identify component system opportunities. |

---

## 12. Status (`S:`)

| Symbol | Name | Description |
| :--- | :--- | :--- |
| `S:ACTIVE` | Active | Currently active work. |
| `S:READY` | Ready | Ready for execution. |
| `S:COMPLETE` | Complete | Work completed. |
| `S:PAUSED` | Paused | Work paused. |

---

## 13. Execution Rules (`ER:`)

| Symbol | Name | Description |
| :--- | :--- | :--- |
| `ER:ONE_FILE` | One File | Execute one file at a time, no bundling. |
| `ER:REFERENCE_FIRST` | Reference First | Read patterns.mdc before editing. |
| `ER:VERIFY_EACH` | Verify Each | Verify after each file edit. |
| `ER:STOP_ON_FAIL` | Stop On Fail | Stop if verification fails. |
| `ER:AWAIT_CONTINUE` | Await Continue | Stop after reporting, await continue. |

---

## 14. Constraints (`C:`)

| Symbol | Name | Description |
| :--- | :--- | :--- |
| `C:NO_CODE` | No Code | No code blocks in documentation. |
| `C:TOKEN_MIN` | Token Minimization | Minimize tokens in output. |
| `C:A2A` | A2A Format | Use A2A-optimized format. |

---

## 15. Vector Native Symbols

| Symbol | Name | Usage |
| :--- | :--- | :--- |
| `●` | Primary Node | Main topic or entity. |
| `→` | Flow/Relationship | Indicates flow, relationship, or action. |
| `○` | Context/Note | Additional context or note. |
| `⊕` | Addition/Enhancement | Addition or enhancement. |
| `|` | Attribute Separator | Separates attributes in VN format. |

---

**Usage:** All commands and workflows use these symbols for consistency and clarity. Reference this dictionary when creating or updating commands.
