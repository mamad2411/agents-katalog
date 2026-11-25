---
name: create-roadmap
description: Generates a battle-tested, phased master roadmap (progress.md) from any app idea or feature spec. Breaks development into foundational infrastructure, modular features, settings, monetization, security, polish, and store publishing, modeled after production systems like Floatkit.
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: project-planning
---

# 🗺️ Create Roadmap (`progress.md`)

## What I Do
1. **Analyze App Ideas & Specs**: Takes a user's raw app concept, feature list, or architecture brief and dissects it into an execution-ready master roadmap.
2. **Generate `progress.md`**: Builds a comprehensive, phased tracking file (`progress.md`) featuring granular checklists, UI/UX tasks, data models, edge cases, settings, monetization, and store publishing.
3. **Enforce Complete App Lifecycles**: Ensures critical non-feature phases are never overlooked (theming/settings, legal/privacy, monetization gating, app security/obfuscation, splash/onboarding, and store deployment).
4. **Establish Long-Term Evolution**: Structures the document with post-launch update sprints (`## Updates`), future backlogs (`## Future Plans`), and immediate punchlists (`## Next To-Do`).

---

## When to Use Me
- Right after the user describes a new app concept, feature set, or pitch.
- When starting Phase 1 of a new project after running `project-scaffold`.
- When an existing project needs a comprehensive, professional master roadmap.
- When the user asks: *"create progress.md"*, *"plan out the app phases"*, *"break down this app idea into a roadmap"*, or *"make a roadmap like Floatkit"*.

---

## 🏛️ The Floatkit Roadmap Architecture

A production-grade app is never just a list of features. It spans a **15-Phase Progressive Lifecycle**:

```
┌─────────────────────────────────────────────────────────────┐
│                 APP LIFECYCLE PROGRESSION                   │
├─────────────────────────────────────────────────────────────┤
│ 🔌 Phase 1: Core Foundation & Runtime Infrastructure        │
│ 🗄️ Phase 2: Data Architecture, Storage & State Flow         │
│ 🎨 Phase 3: Shell Layout, Design Tokens & Base Navigation   │
│ 📦 Phases 4–N: Modular Core Features (One phase per module) │
│ 📱 Phase N+1: Companion Dashboard / Home Interface          │
│ ⚙️ Phase N+2: Settings, Customization & Data Management     │
│ ℹ️ Phase N+3: About, Support, FAQs & Developer Contact      │
│ 🛡️ Phase N+4: Legal, Compliance, Privacy & Disclosures      │
│ ⭐ Phase N+5: Monetization, Paywall & Feature Gating        │
│ 🔐 Phase N+6: Security, Integrity, Obfuscation & Hardening  │
│ ❇️ Phase N+7: Branding, App Icon, Splash & Onboarding       │
│ 🚀 Phase N+8: Production Polish, Testing & Store Publishing  │
│ ─────────────────────────────────────────────────────────── │
│ 🔄 Updates: Post-Launch Feature Updates (v1.1, v1.2, ...)   │
│ 🔮 Future Plans: Ideation Backlog                           │
│ 🛠️ Next To-Do: Active Bugfixes & Immediate Punchlist        │
└─────────────────────────────────────────────────────────────┘
```

---

## ⚙️ Execution Steps for the Agent

When this skill is invoked:

### Step 1: Dissect the App Concept
Extract and categorize the user's requirements into:
1. **Target Platform & Runtime**: (Android, iOS, Web/React, Desktop/Electron, CLI)
2. **Core Capabilities / Modules**: What are the 3–5 distinct tools or feature panels?
3. **Data & Persistence**: Local DB (Room, SQLite, IndexedDB), sync, or files?
4. **Monetization Model**: Free only, freemium with limits, monthly/lifetime subscription, or one-time purchase?
5. **Hardware / OS Integrations**: Permissions (overlays, notifications, camera, microphone, storage, network)?

### Step 2: Generate `progress.md`
Generate `progress.md` in the project root using the standard blueprint below. Tailor each phase directly to the app's domain and features while preserving the granular sub-item pattern:
- Every feature module MUST have: `UI/Layout`, `Data & Logic`, `Input limits / Validation`, `User Feedback (Haptics/Toast/Snackbars)`, `Empty States`, and `Helper Tips`.
- If freemium, explicitly state free vs. pro limitations in the feature checklist.

### Step 3: Present and Sync
1. Inform the user that `progress.md` has been created.
2. Provide a high-level summary of the phases.
3. Update `AGENT_SYNC.md` to reference Phase 1 of `progress.md` as the active phase.

---

## 📋 The Master `progress.md` Template

```markdown
# [App Name] Master Roadmap

## 📌 High-Level Phase Overview
- [ ] **Phase 1: Core Foundation & Runtime Infrastructure**
- [ ] **Phase 2: Data Architecture, Storage & State Flow**
- [ ] **Phase 3: Shell Layout, Design Tokens & Base Navigation**
- [ ] **Phase 4: [Core Feature 1 Name]**
- [ ] **Phase 5: [Core Feature 2 Name]**
- [ ] **Phase 6: [Core Feature 3 Name]**
- [ ] **Phase 7: Main Dashboard & Companion Interface**
- [ ] **Phase 8: Settings, Customization & Preferences**
- [ ] **Phase 9: About, Help & Support Section**
- [ ] **Phase 10: Legal, Compliance & Privacy**
- [ ] **Phase 11: Monetization, Paywall & Feature Gating**
- [ ] **Phase 12: Security, Integrity & Hardening**
- [ ] **Phase 13: Branding, App Icon, Splash & Onboarding**
- [ ] **Phase 14: Quality Assurance, Testing & Store Publishing**

---

## 🔌 Phase 1: Core Foundation & Runtime Infrastructure
- [ ] Project initialization & build configuration
- [ ] Runtime permissions & system contracts setup
- [ ] Background service / lifecycle controller setup
- [ ] Base crash handling & process termination recovery
- [ ] Safe fallback for missing system capabilities

## 🗄️ Phase 2: Data Architecture, Storage & State Flow
- [ ] Local database schemas & tables / entities
- [ ] Key-value preferences store (DataStore / LocalStorage)
- [ ] Repository interfaces & state publishers (Flow / Signals)
- [ ] Safe schema migrations & initial prepopulated data
- [ ] Threading & IO dispatcher safety

## 🎨 Phase 3: Shell Layout, Design Tokens & Base Navigation
- [ ] Design system tokens (strict 8-point rhythm, color palette, typography ramp)
- [ ] Navigation routing & backstack handler
- [ ] Base shell / scaffold (bars, docked containers, drawer or bottom nav)
- [ ] Motion & transition specs (slide, fade, scale curves)
- [ ] Adaptive layouts (mobile, tablet, split-screen)

## 📦 Phase 4: [Feature 1 Name - e.g., Task Manager]
- [ ] **UI Layout:**
  - [ ] Card / list container with clean spacing
  - [ ] Action buttons (Add, Edit, Delete, Complete)
  - [ ] Order indicator & sort options
- [ ] **Logic & Operations:**
  - [ ] Input field with character length validation
  - [ ] Reordering / drag-and-drop mechanics
  - [ ] Completion toggle with visual feedback
- [ ] **User Experience Polish:**
  - [ ] Subtle haptic / audio feedback on key actions
  - [ ] Empty state with instructive illustration & CTA
  - [ ] Tooltip / tip card for first-time use
  - [ ] Swipe-to-dismiss gesture handling

## 📦 Phase 5: [Feature 2 Name - e.g., Quick Notes]
- [ ] **UI Layout:**
  - [ ] Title & content typography hierarchy
  - [ ] Context menu / 3-dot overflow actions
  - [ ] Pin / favorite badge
- [ ] **Logic & Operations:**
  - [ ] Create, edit, search, and delete notes
  - [ ] Auto-save on idle / blur
  - [ ] Share / export to external apps
  - [ ] Clipboard copy action
- [ ] **User Experience Polish:**
  - [ ] Input limit warnings
  - [ ] Visual distinction for pinned items
  - [ ] Soft deletion / undo snackbar

## 📦 Phase 6: [Feature 3 Name - e.g., Clipboard / Search]
- [ ] **UI Layout:**
  - [ ] Search input bar (single-line, non-expanding, clear button)
  - [ ] Filter chips / tab selector
  - [ ] Results list with high-contrast text snippets
- [ ] **Logic & Operations:**
  - [ ] Debounced real-time query filtering
  - [ ] Category grouping
  - [ ] Auto-expiry / purge options
- [ ] **User Experience Polish:**
  - [ ] Zero-results state with suggestions
  - [ ] Keyboard focus & accessibility handling
  - [ ] Haptic feedback on selection

## 📱 Phase 7: Main Dashboard & Companion Interface
- [ ] **Hero Section:**
  - [ ] Master service / app toggle switch
  - [ ] Current system status badge (Active, Inactive, Blocked)
- [ ] **Diagnostics & Permissions Card:**
  - [ ] Permission status checklist with tap-to-grant prompts
  - [ ] System capability verification (Battery optimization whitelist, overlay)
- [ ] **Quick Stats & Activity Overview:**
  - [ ] Item counts (e.g., total notes, completed tasks)
  - [ ] Recent activity timestamps
- [ ] Smooth scrolling & collapsing header animation

## ⚙️ Phase 8: Settings, Customization & Preferences
- [ ] **Appearance:**
  - [ ] Theme selection (Light / Dark / System Default)
  - [ ] Accent color or font size scaling
- [ ] **Behavioral Preferences:**
  - [ ] Position anchor & dock alignment
  - [ ] Idle opacity / auto-collapse delay
  - [ ] Haptic feedback toggle
  - [ ] Notification toggles
- [ ] **Data Management:**
  - [ ] Export / backup data to file
  - [ ] Restore / import data from file
  - [ ] "Clear All Data" with destructive confirmation dialog

## ℹ️ Phase 9: About, Help & Support Section
- [ ] **Help & Guides:**
  - [ ] Frequently Asked Questions (FAQ) accordion
  - [ ] Quick-start walkthrough / manual
- [ ] **Feedback & Contact:**
  - [ ] In-app feedback board or contact support action
  - [ ] Error report generator (non-PII hardware metadata)
- [ ] **App Info:**
  - [ ] Version code & build number display
  - [ ] Changelog viewer
  - [ ] Rate App (Play Store / App Store deep-link)
  - [ ] Developer / company credits

## 🛡️ Phase 10: Legal, Compliance & Privacy
- [ ] Structured In-App Privacy Policy screen
- [ ] Structured In-App Terms of Service screen
- [ ] Third-party SDK disclosure list
- [ ] Data safety compliance declaration
- [ ] Offline-first / zero-telemetry guarantee text

## ⭐ Phase 11: Monetization, Paywall & Feature Gating
- [ ] **Freemium Limits Definition:**
  - [ ] Free tier constraints (e.g., max 10 tasks, max 5 bookmarks)
  - [ ] Premium-only feature locks
  - [ ] Soft limit warnings & upgrade triggers
- [ ] **Paywall UI & Experience:**
  - [ ] Benefit comparison card (Free vs. PRO)
  - [ ] Pricing options (Monthly, Lifetime, Launch Discount)
  - [ ] Terms & auto-renewal fine print
- [ ] **Billing Integration:**
  - [ ] Store billing library integration (Play Billing / StoreKit / Stripe)
  - [ ] Secure purchase verification & receipt validation
  - [ ] Restore purchases functionality

## 🔐 Phase 12: Security, Integrity & Hardening
- [ ] Code obfuscation & resource shrinking (ProGuard / R8 / Terser)
- [ ] Secure storage for sensitive preferences / tokens
- [ ] Tapjacking protection (filter touches when obscured)
- [ ] Strict input sanitization & boundary validation
- [ ] Zero secrets audit (verify no keys in source code)

## ❇️ Phase 13: Branding, App Icon, Splash & Onboarding
- [ ] Vector adaptive app icons & favicons
- [ ] Animated splash screen / cold-start window
- [ ] Multi-slide onboarding walkthrough
- [ ] Feature discovery highlight on first launch

## 🚀 Phase 14: Quality Assurance, Testing & Store Publishing
- [ ] Full lint, static analysis & unit test suite pass
- [ ] Memory leak & battery consumption audit
- [ ] Store assets (icons, screenshots, feature graphics)
- [ ] Store listing copy (`PLAY_STORE_DESCRIPTION.txt` or store copy)
- [ ] Internal / closed testing rollout
- [ ] Production build signing & release upload

---

# 🔄 Post-Launch Updates Backlog

## Phase: Update 1 (Quick Wins & Polish)
- [ ] User feedback refinements
- [ ] Additional quick presets & shortcuts

## Phase: Update 2 (Advanced Capabilities)
- [ ] Extended format support
- [ ] Additional customization settings

---

# 🔮 Future Plans & Ideas
- [ ] Cloud backup integration (Google Drive / iCloud)
- [ ] Home screen widget support
- [ ] AI-powered local assistant / summary

---

# 🛠️ Next To-Do (Active Fixes & Punchlist)
- [ ] Step 1 of Phase 1
```
