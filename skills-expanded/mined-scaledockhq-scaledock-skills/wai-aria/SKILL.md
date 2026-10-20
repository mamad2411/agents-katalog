---
name: wai-aria
description: >-
  WAI-ARIA 1.2 roles, states, properties and accessible names for web widgets,
  with APG keyboard and focus patterns. Builds and reviews accessible custom
  components: native HTML first per ARIA in HTML, non-abstract roles with
  their required owned elements, context roles and required states, accessible
  names and descriptions per AccName, and focus management for modal dialog,
  menu button, menu and menubar, combobox, listbox, tabs, disclosure, grid,
  tree view and live regions (alert, status, aria-live). Use when adding role
  or aria-* attributes, fixing a missing or wrong accessible name, using
  aria-labelledby, aria-describedby, aria-hidden, aria-expanded,
  aria-controls, aria-activedescendant, aria-modal or a roving tabindex, or
  auditing ARIA misuse. Targets WAI-ARIA 1.2, AccName 1.1 and ARIA in HTML;
  builds on the AccName 1.2 preview, reserves names from the WAI-ARIA 1.3
  preview, and upgrades from WAI-ARIA 1.1 and WAI-ARIA 1.0. Also Graphics ARIA
  1.0 and DPUB-ARIA 1.1. Also SVG-AAM and DPub-AAM 1.0.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.2.0"
  kind: standard
---

# WAI-ARIA

Accessible Rich Internet Applications (WAI-ARIA), published by the W3C, defines the roles, states and properties that expose custom user interface components to assistive technologies. With its companions AccName (how names and descriptions are computed) and ARIA in HTML (which ARIA each HTML element allows), and the ARIA Authoring Practices Guide (APG) for keyboard behaviour, this skill produces or reviews markup and scripts for accessible widgets.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources), with the section it cites. WAI-ARIA rules cite WAI-ARIA 1.2 sections unless marked otherwise; APG rules cite the page and heading. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: component author (building a widget), reviewer or auditor, or conformance checker author. User agent and assistive technology implementers are out of scope.
- Host language: HTML (the default; ARIA in HTML applies), SVG or another host.
- Component: which widget or pattern, for example modal dialog, menu button, combobox, tabs, grid or a live region, and whether a native HTML element already does the job.
- Target version: WAI-ARIA 1.2 (current, the default). WAI-ARIA 1.1 and WAI-ARIA 1.0 are legacy: read them and upgrade from them, never author them. WAI-ARIA 1.3 is a preview (posture: name): reserve its names, never ship its new roles or attributes as the only carrier of meaning. AccName 1.1 is the current AccName Recommendation; AccName 1.2 is a preview (posture: build) that WAI-ARIA 1.2 cites normatively, so predict names with it and test what it adds. ARIA in HTML is current. Graphics ARIA 1.0 and DPUB-ARIA 1.1 are each the current line of their family. SVG-AAM is current with posture track. DPub-AAM 1.0 is current. See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill or when a rule looks out of date, re-read every URL in [Sources](#sources) first, check the W3C TR pages for WAI-ARIA, AccName and ARIA in HTML for a newer maturity level, and update the pins.

## Invariants

1. **Native HTML first.** When a host-language feature with the same semantics exists, authors SHOULD use it rather than repurpose another element with ARIA (§8.5; Using ARIA §2.1).
2. **No abstract roles.** Authors MUST NOT use `command`, `composite`, `input`, `landmark`, `range`, `roletype`, `section`, `sectionhead`, `select`, `structure`, `widget` or `window` (§5.2.1, §5.3.1).
3. **One meaningful role token.** The first non-abstract token wins and an unknown token is ignored (§4.1, §9.1); write role tokens in lowercase (ARIA in HTML §4.4).
4. **Required states are set.** Authors MUST provide a non-empty value for each required state or property, for example `aria-checked` on `checkbox` and `aria-level` on `heading` (§5.2.2).
5. **Structure is complete.** A role with required owned elements owns at least one of them, a role with a required context role is contained in or owned by it, and authors MUST set `aria-busy="true"` while required children are still loading (§5.2.6, §5.2.7).
6. **Attributes fit the role.** Authors MUST only use non-global states and properties on roles that support them, and MUST NOT use prohibited ones (§8.6, §5.2.5).
7. **Names follow the role.** Name-required roles get an accessible name; authors MUST NOT put `aria-label` or `aria-labelledby` on name-prohibited roles such as `generic`, `paragraph` or `code` (§5.2.8, §5.2.8.4, §5.2.8.6; ARIA in HTML §4.1).
8. **No conflict with HTML.** Authors MUST NOT use ARIA in a way that conflicts with the ARIA in HTML element and attribute tables, and SHOULD NOT set an aria-\* attribute next to its native equivalent, because the native one wins (ARIA in HTML §1, §4, §4.2; §8.5).
9. **Hidden means equivalent.** Authors using `aria-hidden="true"` on visible content MUST expose equivalent meaning and function (§6.7 aria-hidden); never on focusable elements or `body` (ARIA in HTML §4, §4.2).
10. **Composites manage focus.** Authors MUST manage focus in `grid`, `listbox`, `menu`, `menubar`, `radiogroup`, `tree`, `treegrid` and `tablist` (§4.3.1), and every interactive ARIA control is keyboard operable (Using ARIA §2.3).
11. **Active descendants are owned.** `aria-activedescendant` MUST refer to an owned element, or for a combobox, textbox or searchbox to an element owned by the element it controls (§6.7 aria-activedescendant).
12. **One owner.** Authors MUST NOT list an element in more than one `aria-owns` (§6.7 aria-owns).
13. **Modals are self-contained.** With a modal displayed, authors MUST ensure the interface can be controlled using only its descendants (§6.7 aria-modal), and MUST name every `dialog` (§5.4 dialog).
14. **The combobox follows 1.2.** Authors MUST set `aria-expanded` and `aria-controls` on the combobox, give the popup role `listbox`, `tree`, `grid` or `dialog`, set `aria-haspopup` when it is not a listbox, and set `aria-autocomplete` when the input autocompletes (§5.4 combobox).
15. **Errors are pertinent.** Authors MUST use `aria-errormessage` with `aria-invalid`, and MUST show the message only while it is pertinent (§6.7 aria-errormessage).
16. **Regions are labelled.** Authors MUST give each `region` a brief label (§5.4 region).

## Workflow

1. **Pick the version.** Author against WAI-ARIA 1.2 and ARIA in HTML, predict names with AccName 1.2, and record any WAI-ARIA 1.3 names you reserve.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and no legacy markup or 1.3-only role or attribute is being shipped.
2. **Decide native or ARIA.** Look for an HTML element or attribute that already does the job; otherwise check which roles the base element allows.
   -> [`references/aria-in-html.md`](references/aria-in-html.md)
   ✓ Every explicit role is allowed on its element by the ARIA in HTML table, and none repeats the implicit role.
3. **Assign roles and structure.** Pick concrete roles, then add their required owned elements, context roles and required states.
   -> [`references/roles-states-properties.md`](references/roles-states-properties.md)
   ✓ No abstract role, no missing required child or parent, no missing required state.
4. **Name and describe.** Give every name-required element a name from visible text where possible, and leave name-prohibited elements unnamed.
   -> [`references/accessible-names.md`](references/accessible-names.md)
   ✓ The computed name of each control matches the intended name in each target browser's accessibility tree.
5. **Wire states and relationships.** Keep `aria-expanded`, `aria-selected`, `aria-checked`, `aria-controls` and `aria-activedescendant` in sync with the UI on every change, from keyboard and pointer.
   -> [`references/roles-states-properties.md`](references/roles-states-properties.md)
   ✓ Every state change in the UI is reflected in the attributes, and every ID reference resolves.
6. **Implement keyboard and focus.** Follow the APG pattern for the widget: tab stops, arrow keys, Escape, initial focus and focus return.
   -> [`references/apg-patterns.md`](references/apg-patterns.md)
   ✓ The widget is fully operable from the keyboard, focus is always visible, and focus never falls back to `body`.
7. **Announce changes.** Use `alert`, `status` or `aria-live` for updates that happen away from focus, at the lowest politeness that works.
   -> [`references/apg-patterns.md`](references/apg-patterns.md#alerts-and-live-regions)
   ✓ Each dynamic message is announced once, without moving focus, and nothing uses `assertive` without need.
8. **Upgrade** (only when asked). Follow the upgrade section for each step from the source line to WAI-ARIA 1.2.
   -> [`references/versions.md`](references/versions.md)
   ✓ The upgraded component passes the Verify list below, and users get the same names, roles, states and keys as before.

## Verify before done

- [ ] No abstract role, and no role on an element whose ARIA in HTML row says "No role" (§5.2.1; ARIA in HTML §4).
- [ ] Every required owned element, context role and required state is present (§5.2.2, §5.2.6, §5.2.7).
- [ ] No `aria-label` or `aria-labelledby` on a name-prohibited role, and every name-required role has a non-empty name (§5.2.8).
- [ ] No aria-\* attribute duplicates a native HTML attribute on the same element (ARIA in HTML §4.2).
- [ ] No `aria-hidden="true"` or `role="presentation"` on a focusable element, and no `aria-hidden="true"` on an ancestor of a visible interactive element (ARIA in HTML §4.2; Using ARIA §2.4).
- [ ] Each composite has one tab stop, and arrow keys move focus as the APG pattern describes (§4.3.1; APG Developing a Keyboard Interface).
- [ ] Every `aria-activedescendant`, `aria-controls`, `aria-labelledby` and `aria-describedby` ID resolves to the right element (§8.6.1).
- [ ] Modal dialogs trap Tab, close on Escape, and return focus to the invoking element (APG Dialog (Modal) Pattern).
- [ ] No deprecated feature (`aria-grabbed`, `aria-dropeffect`, `directory`) in new content (§3.5; ARIA in HTML §4.3).
- [ ] Nothing from WAI-ARIA 1.3 is the only carrier of meaning (posture: name).

## Reference index

- **`references/versions.md`**: every WAI-ARIA, AccName and ARIA in HTML line with its status, what each changed, upgrade steps from 1.1 and 1.0, and the 1.3 and AccName 1.2 previews. Load for steps 1 and 8.
- **`references/aria-in-html.md`**: the rules of ARIA use, ARIA in HTML author requirements, allowed roles for common elements, HTML attribute parity, deprecated features and case. Load for step 2.
- **`references/roles-states-properties.md`**: role categories, abstract roles, required owned elements and context roles, required and global states, hiding and presentational roles, relationship and live region attributes, deprecated features, common mistakes. Load for steps 3 and 5.
- **`references/accessible-names.md`**: name from author, contents or prohibited, the AccName computation steps, the description computation, authoring rules and debugging. Load for step 4.
- **`references/apg-patterns.md`**: focus fundamentals (roving tabindex, `aria-activedescendant`, disabled items) and the dialog, menu button, menu and menubar, combobox, listbox, tabs, disclosure, grid, tree view and alert patterns. Load for steps 6 and 7.

## Related skills

- `wcag`, for the WCAG success criteria that ARIA markup helps meet: `npx skills add ScaleDockHQ/scaledock-skills --skill wcag`

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Accessible Rich Internet Applications (WAI-ARIA) 1.2](https://www.w3.org/TR/wai-aria-1.2/): W3C Recommendation, 2023-06-06, checked 2026-10-05.
- [Accessible Rich Internet Applications (WAI-ARIA) 1.1](https://www.w3.org/TR/wai-aria-1.1/): W3C Recommendation, 2017-12-14, checked 2026-10-05.
- [Accessible Rich Internet Applications (WAI-ARIA) 1.0](https://www.w3.org/TR/wai-aria-1.0/): W3C Recommendation, 2014-03-20, checked 2026-10-05.
- [WAI-ARIA 1.0 Roles](https://www.w3.org/TR/wai-aria-1.0/roles): W3C Recommendation, 2014-03-20, checked 2026-10-05.
- [Accessible Rich Internet Applications (WAI-ARIA) 1.3](https://www.w3.org/TR/wai-aria-1.3/): W3C Working Draft, 2026-06-04, checked 2026-10-05. Draft posture: name.
- [WAI-ARIA editor's draft](https://w3c.github.io/aria/): W3C Editor's Draft, 2026-10-02, same roles and attributes as the 1.3 Working Draft, checked 2026-10-05. Draft posture: name.
- [Accessible Name and Description Computation 1.2](https://www.w3.org/TR/accname-1.2/): W3C Working Draft, 2026-10-02, checked 2026-10-05. Draft posture: build.
- [Accessible Name and Description Computation 1.1](https://www.w3.org/TR/accname-1.1/): W3C Recommendation, 2018-12-18, checked 2026-10-05.
- [ARIA in HTML](https://www.w3.org/TR/html-aria/): W3C Recommendation, 2026-08-11, checked 2026-10-05.
- [Using ARIA](https://www.w3.org/TR/using-aria/): W3C Discontinued Draft, 2026-02-24, informative, checked 2026-10-05.
- [ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/): W3C WAI resource, published site as read 2026-10-05 (w3c/aria-practices main at 0f765e4, 2026-09-30), checked 2026-10-05.
- [APG Patterns](https://www.w3.org/WAI/ARIA/apg/patterns/): W3C WAI resource, as read 2026-10-05, checked 2026-10-05.
- [APG Dialog (Modal) Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/): W3C WAI resource, as read 2026-10-05, checked 2026-10-05.
- [APG Alert Dialog Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/alertdialog/): W3C WAI resource, as read 2026-10-05, checked 2026-10-05.
- [APG Menu Button Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/menu-button/): W3C WAI resource, as read 2026-10-05, checked 2026-10-05.
- [APG Menu and Menubar Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/menubar/): W3C WAI resource, as read 2026-10-05, checked 2026-10-05.
- [APG Combobox Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/combobox/): W3C WAI resource, as read 2026-10-05, checked 2026-10-05.
- [APG Listbox Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/listbox/): W3C WAI resource, as read 2026-10-05, checked 2026-10-05.
- [APG Tabs Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/tabs/): W3C WAI resource, as read 2026-10-05, checked 2026-10-05.
- [APG Disclosure (Show/Hide) Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/): W3C WAI resource, as read 2026-10-05, checked 2026-10-05.
- [APG Grid Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/grid/): W3C WAI resource, as read 2026-10-05, checked 2026-10-05.
- [APG Tree View Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/treeview/): W3C WAI resource, as read 2026-10-05, checked 2026-10-05.
- [APG Alert Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/alert/): W3C WAI resource, as read 2026-10-05, checked 2026-10-05.
- [APG Developing a Keyboard Interface](https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/): W3C WAI resource, as read 2026-10-05, checked 2026-10-05.
- [APG Providing Accessible Names and Descriptions](https://www.w3.org/WAI/ARIA/apg/practices/names-and-descriptions/): W3C WAI resource, as read 2026-10-05, checked 2026-10-05.
- [WAI-ARIA Graphics Module](https://www.w3.org/TR/graphics-aria-1.0/): W3C Recommendation, 2 October 2018 (REC-graphics-aria-1.0-20181002), checked 2026-10-06.
- [Digital Publishing WAI-ARIA Module 1.1](https://www.w3.org/TR/dpub-aria-1.1/): W3C Recommendation, 12 June 2025 (REC-dpub-aria-1.1-20250612), checked 2026-10-06.
- [Core Accessibility API Mappings 1.2](https://www.w3.org/TR/core-aam-1.2/): W3C Candidate Recommendation Draft, 23 September 2026 (CRD-core-aam-1.2-20260923), checked 2026-10-06.
- [HTML Accessibility API Mappings 1.0](https://www.w3.org/TR/html-aam-1.0/): W3C Working Draft, 5 October 2026 (WD-html-aam-1.0-20261005), checked 2026-10-06.
- [SVG Accessibility API Mappings](https://www.w3.org/TR/svg-aam-1.0/): W3C Working Draft, 24 September 2026 (WD-svg-aam-1.0-20260924), checked 2026-10-06.
- [Digital Publishing Accessibility API Mappings](https://www.w3.org/TR/dpub-aam-1.0/): W3C Recommendation, 14 December 2017 (REC-dpub-aam-1.0-20171214), checked 2026-10-06.
