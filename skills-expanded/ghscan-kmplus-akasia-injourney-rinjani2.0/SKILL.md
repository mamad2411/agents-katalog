# Design Input Pack (DIP): output guide for AI prototyping

**Purpose:** Define the **artifact you produce**—a single Markdown **Design Input Pack**—so tools like **Google Stitch** can run design iterations from **requirements-aligned** context. Visual language (colors, layout, components) stays with the prototyping tool; this guide does **not** prescribe how your Notion workspace or databases are organized.

**Audience:** Anyone assembling exports from existing docs (Notion, Confluence, wikis) plus optional repo-local data.

**How to use:** Keep this file in the repo or import it into Notion as a **reference page**. When you export a DIP, follow the **section order** and **scope rules** below.

---

## 1. Philosophy: split of responsibilities


| Layer                     | Typical source                                                            | In the DIP                                                                                  |
| ------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| **Product truth**         | Notion (or other) + optional engineering artifacts                        | Intent, personas, processes, user stories, acceptance criteria, terminology, open questions |
| **Structural data truth** | Legacy DB design export + **IDE-maintained** schema/samples (recommended) | Pack Section 3 (domain model), Pack Section 4 (reference dataset)                           |
| **Visual & layout**       | AI prototyping tool                                                       | Chosen by the tool, bounded by stories, states, and sample data                             |


**Why sample data matters:** Without aligned example rows, generators fall back to generic placeholders. Pack Sections 3 and 4 should be **internally consistent** (IDs and foreign keys match).

**Anti-hallucination rule:** In **Pack Section 0** (the instruction block), tell the tool not to invent KPIs, uptime stats, or metrics you did not supply. Use `[TBD]` where unknown.

---

## 2. What a complete DIP contains (skill outcomes)

A good pack lets a prototype **start strong**—not only pretty, but **credible** relative to your business:

1. Clear product intent and MVP / non-goals.
2. Personas and **access** (who can see or do what), even informally.
3. **Semantic domain model** (entities, fields, enums, relationships)—no SQL required.
4. **Reference dataset**: small, realistic, cross-referenced rows.
5. Business processes / flows (steps, branches, exceptions).
6. User stories with acceptance criteria, ordered for the slice you are designing.
7. Optional: conceptual **screen / flow coverage map** (which stories land on which screens)—not wireframes.
8. Terminology + **open questions**.

---

## 3. How big should one document be? (scope)

**Rule of thumb:** One DIP = **one coherent design slice**, not the entire product.

Use boundaries such as:

- **One primary journey** end-to-end (e.g. employee drafts and submits an IDP in one cycle), or  
- **One actor + one goal** across a few screens (e.g. manager approves pending IDPs), or  
- **One epic** that you would ship and test together.

**When one “module” is too large for a single DIP**

A product **module** (e.g. Rinjani **Development Plan** / IDP: employee dashboard, editor, catalog, gap analysis, manager team view, admin HQ) often spans **many routes and personas**. That is **too much context for one paste**: models, stories, and samples balloon; tools lose focus and contradict edge cases.

**Practical split for a large module** (example pattern):


| DIP title (example)                | Rough scope                                                                                   |
| ---------------------------------- | --------------------------------------------------------------------------------------------- |
| IDP — employee draft & submit      | Stories for editor, validation, submit; dataset for one employee, one cycle, a few activities |
| IDP — manager review & approve     | Team list, review screen, approval states; sample team rows                                   |
| IDP — course catalog & add to plan | Catalog browse, add/remove from draft; sample courses                                         |
| IDP — admin cycle configuration    | Cycles, deadlines (if prototyping admin separately)                                           |


**Heuristics**

- If you are pasting into a tool with a **context limit**, aim for **roughly ~5–15 user stories** per DIP (flexible: fewer if stories are heavy, more if tiny).  
- If **Pack Sections 3 and 4** exceed **~1–2 screens of dense Markdown**, consider moving **full** fixtures to the repo and in the DIP keep a **trimmed** dataset plus a one-line **pointer** (see **Optional: pointer to repo fixtures** in this guide).  
- Prefer **multiple focused DIPs** over one “whole module” dump; you can reuse the same Pack Sections 3 and 4 across related DIPs when the model is identical.

---

## 4. Where schema and samples live (Notion vs IDE)

Your workflow can stay **light in Notion** for slow or heavy data work:


| Concern                                            | Suggested owner                                                                 | Role in the DIP                                                                                                                        |
| -------------------------------------------------- | ------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| Business process, user stories, personas, glossary | Notion (or existing wiki)                                                       | Pack Sections 1, 2, 5, 6, 8, 9                                                                                                         |
| **Legacy / authoritative database structure**      | Export from your design tool (ERD, DDL, modeling doc) or existing technical doc | Paste or summarize into **Pack Section 3** (semantic bullets). Keep one source of truth outside Notion if that is already established. |
| **New tables, extended schema, seed rows**         | **IDE (e.g. Cursor)** — types, JSON fixtures, migrations                        | Author and iterate quickly; then **copy a stable snapshot** into Pack Sections 3 and 4 for Stitch, or reference a repo path            |


**DIP assembly:** Treat Notion as the place you **narrate** requirements; treat the repo as the place you **shape** structure and sample data. The exported Markdown file **merges** both for the prototyping tool.

---

## 5. Export artifact: Design Input Pack (DIP)

**Format:** Markdown (export from Notion, or compose in the IDE).

**Fixed section order** (keep this order for predictable parsing and model alignment). **Pack Section N** means the Nth block inside the exported DIP (0 = instructions, 1 = product intent, …).

1. **Pack Section 0** — Instruction to prototyping tool
2. **Pack Section 1** — Product intent
3. **Pack Section 2** — Personas & access
4. **Pack Section 3** — Domain model (semantic)
5. **Pack Section 4** — Reference dataset
6. **Pack Section 5** — Business processes & flows
7. **Pack Section 6** — User stories (ordered)
8. **Pack Section 7** — Screen / flow coverage map (optional)
9. **Pack Section 8** — Content & terminology
10. **Pack Section 9** — Open questions

### Pack Section 0 — Template (copy into every export)

```markdown
## 0. Instruction to prototyping tool

- Generate UI structure, components, and visual style using your best judgment and integrated design-system context.
- You MUST reflect the user stories, personas, domain entities, states, and acceptance criteria in this document.
- Use ONLY the reference dataset supplied below for realistic content; align labels and relationships to the domain model.
- Do not invent business metrics, KPIs, uptime/performance statistics, or fabricated company names not present in the sample data.
- Where information is missing, use the literal placeholder `[TBD]` instead of guessing.
```

### Empty DIP scaffold

```markdown
# Design Input Pack: [Product name] — [Slice name: journey / actor / epic]
**Version:** [x.y]  **Date:** [ISO date]  **Owner:** [name/role]

## 0. Instruction to prototyping tool
[paste Pack Section 0 template]

## 1. Product intent
- Problem:
- Target outcome:
- MVP scope:
- Non-goals:

## 2. Personas & access
| Persona | Goals | Can | Cannot |
|--------|--------|-----|--------|
| | | | |

## 3. Domain model (semantic)
- **EntityName:** fields, types, enums, relationships (short bullets)
- (Optional one line: **Schema source:** legacy export dated … / repo path …)

## 4. Reference dataset
(Tables or lists; every ID and foreign key must match Pack Section 3.)

## 5. Business processes & flows
### [Process name]
1. …
- Variations: …

## 6. User stories
### [US-xxx] — [title]
- Story: As a … I want … So that …
- Acceptance criteria:
  - …
- Touches: [entities]
- States: …

## 7. Screen / flow coverage map (optional)
- **[Conceptual screen]:** [story IDs]

## 8. Content & terminology
- Preferred terms:
- Forbidden / deprecated terms:
- Locale / formatting notes:

## 9. Open questions
- …
```

---

## 6. Optional: pointer to repo fixtures

If Pack Section 4 would be huge, keep the **full** dataset in the repo (e.g. `idpData.ts`, JSON seeds) and in the DIP add:

```markdown
## 4. Reference dataset

**Authoritative fixtures:** `packages/talent/src/data/idpData.ts` (commit SHA or date: …).

**Subset for this slice (paste the rows Stitch must render):**
- …
```

Stitch and similar tools usually work best when **at least** the rows needed for the screens in scope are **inline** in the Markdown; the pointer is for humans and for staying in sync with engineering.

---

## 7. Sample Design Input Pack (filled example)

Fictional domain; use as a **quality bar** for density and consistency—not as Rinjani IDP content.

```markdown
# Design Input Pack: Northwind Field Ops — Work order completion
**Version:** 0.2  **Date:** 2026-04-07  **Owner:** Ops PM

## 0. Instruction to prototyping tool

- Generate layout, components, and visual style freely; prioritize clarity and professional defaults.
- Honor all user stories, personas, domain entities, and acceptance criteria below.
- Use only the sample records in Section 4 (Reference dataset); do not invent SLA percentages, performance numbers, or extra companies.
- Use `[TBD]` where information is unspecified.

## 1. Product intent

Technicians complete assigned work orders in the field; dispatchers monitor status. MVP covers the technician journey from list → detail → start → complete (with notes/photos). No billing, inventory, or offline mode in MVP.

**Non-goals:** Multi-language, admin configuration UI, completing work on behalf of another technician.

## 2. Personas & access

| Persona | Goals | Can | Cannot |
|--------|--------|-----|--------|
| Technician (primary, mobile) | Finish jobs quickly; document proof | View own assigned WOs; set InProgress/Completed/Blocked; add notes and photos | See other technicians’ queues or unassigned WOs |
| Dispatcher (secondary, web) | Monitor workload | View all WOs and assignment; reassign | Complete jobs for technicians in MVP |

## 3. Domain model (semantic)

- **WorkOrder:** `id`, `code`, `title`, `status` ∈ {Draft, Assigned, InProgress, Completed, Blocked}, `priority` ∈ {P1, P2, P3}, `siteId`, `assignedTechId`, `scheduledStart`, `scheduledEnd`, `createdAt`
- **Site:** `id`, `name`, `addressLine`, `city`, `regionCode`
- **Technician:** `id`, `displayName`, `employeeCode`
- **WorkNote:** `id`, `workOrderId`, `authorId`, `body`, `createdAt`, `hasPhoto` (bool)

**Relationships:** WorkOrder → Site (many-to-one); WorkOrder → Technician (assigned); WorkOrder → WorkNote (one-to-one).

## 4. Reference dataset

**Technician**

- `T-901` — displayName: Ana Russo, employeeCode: AR-901

**Site**

- `S-100` — name: Rinjani Depot, addressLine: Jl. Example 12, city: Mataram, regionCode: NB

**WorkOrder**

- `WO-240407-01` — code: WO-240407-01, title: Replace pump seal, status: Assigned, priority: P2, siteId: S-100, assignedTechId: T-901, scheduledStart: 2026-04-08T08:00+08:00, scheduledEnd: 2026-04-08T12:00+08:00, createdAt: 2026-04-07T09:00+08:00

**WorkNote**

- `N-5001` — workOrderId: WO-240407-01, authorId: T-901, body: Customer reports intermittent leak, createdAt: 2026-04-07T16:10+08:00, hasPhoto: false

## 5. Business processes & flows

### Complete assigned work order (technician)

1. Technician opens list of work orders where `assignedTechId` = self and `status` ∈ {Assigned, InProgress}.
2. Opens detail for one work order; sees site, schedule, existing notes.
3. Taps **Start work** → `status` = InProgress (timestamp recorded).
4. To complete: adds at least one note; optional photo → **Complete** → `status` = Completed.
5. If cannot proceed: **Blocked** → `status` = Blocked with required note.

**Exception:** Completion requires at least one note when no photo is attached (show inline validation; message text can be drafted by the tool).

## 6. User stories

**US-101 — Assigned list**

- **Story:** As a technician, I want to see my assigned and in-progress work orders for today so I can plan my route.
- **Acceptance criteria:**
  - List only WOs for current technician with status Assigned or InProgress.
  - Row shows code, title, site name, time window, priority.
- **Touches:** WorkOrder (read), Site (read)

**US-102 — Start work**

- **Story:** As a technician, I want to open a work order and start work so dispatch sees live status.
- **Acceptance criteria:**
  - Detail shows attributes from Section 3 (Domain model) for one WO.
  - Start sets status InProgress; Blocked requires a note.
- **Touches:** WorkOrder (write status), WorkNote (read)

**US-103 — Complete with evidence**

- **Story:** As a technician, I want to complete a work order with a note and optional photo so the job is closed audibly.
- **Acceptance criteria:**
  - Complete requires a note; photo optional.
  - After complete, show clear success state tied to WO-240407-01.
- **Touches:** WorkOrder (write), WorkNote (create)

## 7. Screen / flow coverage map

- **Today’s jobs** → US-101  
- **Work order detail** → US-102, US-103  

## 8. Content & terminology

Use **work order** (not “ticket”). Show **city + site name** to users; `regionCode` is internal.

## 9. Open questions

- Max photos per note? (assume 3 for prototype.)  
- Display time zone: fixed Asia/Makassar vs device local?  
```

---

## 8. Optional: short cover paragraph for Stitch (paste above the DIP)

> Design a prototype for the flow described in the specification below. You may choose typography, color, spacing, and components. The UI must satisfy every user story and acceptance criterion; use only the entities and sample values provided. Do not invent statistics, KPIs, or company names beyond the sample data.

---

## 9. Iteration loop

1. **Export** one DIP per slice (see **Section 3 of this guide**, document scope).
2. **Generate** in Stitch; note contradictions with AC, invented data, or missing states.
3. **Fix upstream:** tighter stories, more explicit states, richer Pack Section 4—or adjust IDE fixtures then refresh Pack Section 4.
4. **Revise Pack Section 0** when you see repeated tool failures (e.g. fake metrics).
5. **Version** the DIP header when domain or stories change.

---

## 10. Relationship to `.stitch` / design-system files (optional)

A repo-local `.stitch/DESIGN.md` (if you use one) is a **visual** supplement you can paste alongside a DIP. It does not replace Pack Sections 1 through 6 for **requirements and data**.

---

## 11. Resources


| Resource                            | URL                                                                                                        | Why                                                   |
| ----------------------------------- | ---------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| Google Stitch — Effective prompting | [https://stitch.withgoogle.com/docs/learn/prompting/](https://stitch.withgoogle.com/docs/learn/prompting/) | Structure and clarity even when visuals are delegated |
| INVEST (user stories)               | [https://www.agilealliance.org/glossary/invest/](https://www.agilealliance.org/glossary/invest/)           | Keeps slices small and testable                       |
| Jobs to be Done (overview)          | [https://www.intercom.com/blog/jobs-to-be-done/](https://www.intercom.com/blog/jobs-to-be-done/)           | Optional framing for intent / personas                |


---

## 12. Export drop zone in this repository

Exported DIPs and related Markdown for **performance**, **talent**, and **portal** live under:

`docs/design-input-packs/`


| Path                                      | Product line                  | Typical code           |
| ----------------------------------------- | ----------------------------- | ---------------------- |
| `design-input-packs/performance/exports/` | Engineering performance       | `packages/performance` |
| `design-input-packs/talent/exports/`      | Talent (IDP, journeys, admin) | `packages/talent`      |
| `design-input-packs/portal/exports/`      | Portal shell / entry          | `packages/portal`      |


**Authoring expectations:** Use the shared template `docs/design-input-packs/dip-TEMPLATE.md`; save filled packs as `dip-<slice>-v0.1.md` (or similar) in the correct `exports/` folder. Full instructions for humans and for Cursor sessions are in `[design-input-packs/README.md](design-input-packs/README.md)`.

**Design iterations:** The assistant only has the context you attach. **@ mention** the active DIP file path (and optional fixture paths) when you ask for Stitch prompts, UI work, or implementation aligned to a slice.

---

## 13. Changelog


| Date       | Change                                                                                                                        |
| ---------- | ----------------------------------------------------------------------------------------------------------------------------- |
| 2026-04-07 | Initial skill guide added to `docs/`                                                                                          |
| 2026-04-07 | Refocus on DIP outputs, scope/sizing, Notion vs IDE for schema/samples; removed Notion IA and database property prescriptions |
| 2026-04-07 | Renamed pack parts to “Pack Section N” and plain English (no section-sign shorthand)                                          |
| 2026-04-07 | Added `docs/design-input-packs/` drop zone and cross-reference (Section 12)                                                   |


