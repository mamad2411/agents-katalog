---
name: rpa-reuse
description: Find and reuse reviewed saved RPA skills before repeating screen-by-screen CUA or multimodal reasoning for a known GUI task.
---

Use the VAMP RPA Library MCP provider when available.

When deriving a variant or editing a GUI recording, keep paired `# vamp-step: ID` and `# vamp-end: ID` comments around each local block. Use the matching `section` in the step plan and pin reused blocks to the original commit. For existing recordings first preview the comment migration through `rpa_revision(action="annotate")`. [Authoring and review](../vamp-rpa-ui-checks/SKILL.md#mark-editable-steps-in-gui-recordings)

1. Search with `rpa_search` using the user's task keywords. Titles, descriptions, use cases and tags are searchable; source and screenshots are not needed for discovery.
2. Read `rpa_details` for the best candidate. Check backend, recorded guest resolution, declared input names, review state and expected result. A keyword match alone is not enough.
3. Prefer a suitable reviewed RPA over another CUA/OCR/multimodal loop. Supply exactly the declared inputs and the explicit target VM UUID. Do not invent input values or automatically mark an RPA reviewed.
4. With task authorization, call `rpa_run_saved` with `confirmed=true`. This replays statically parsed actions on guest devices, not Python source on the host. Hyper-V desktop replay is unsupported.
5. Read the compact result first. `completed_unverified` means the events were delivered; it does not establish application success. Verify the stated result with the cheapest reliable observation, and only request targeted screenshots/OCR/multimodal inspection when necessary.
6. If no compatible skill exists or verification fails, use CUA to complete the task with normal authorization. Offer to record/register a reusable RPA afterward when helpful.

A user registers a skill through **RPA Library → Create**, or answers the questions in **Create with AI** and reviews the suggested metadata. The user controls its title, description, search tags, input contract and review checkbox. Recorded text may contain private values; never copy it into metadata or an AI request without the user's explicit action.

## Keep repeated runs inexpensive

Run the saved RPA and its outcome checks locally. For normal success, return only status, verification, a bounded error summary when present, and evidence paths; do not load or forward full OCR text, YOLO boxes, base64 images, Robot logs or source into the LLM context. Read a targeted query/page/region only when the result is ambiguous, verification fails, the UI changes or the user requests inspection. Avoid polling unchanged screenshots through the model. Local OCR/YOLO saves model tokens only when observations stay local or compact; it still uses compute, and no percentage saving is established without a comparable measurement. See [the output policy](../../../docs/LOW_TOKEN_AUTOMATION.md).
