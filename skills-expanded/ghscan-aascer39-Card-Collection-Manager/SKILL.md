Use the Meta-Skill in skills/meta-skill.md.

Generate a React frontend GUI for a Tauri + Rust + SQLite card collection system.

---

## Project Context

This is a local desktop application built with:

- Tauri (desktop runtime)
- Rust backend using rusqlite only (NO ORM)
- SQLite database
- React frontend (TypeScript preferred)

The system manages:

- 52 playing cards + optional jokers
- card boxes (type: box)
- collection status (collected / not collected)

---

## Functional Requirements

The frontend MUST support:

### 1. CRUD Operations

- Create card/box entries
- Read and display card list
- Update card state (collected / not collected)
- Delete or reset collection state (via backend)

---

### 2. Batch Operations

- Multi-select cards
- Select all
- Invert selection
- Batch mark collected
- Batch mark uncollected
- Reset all collection state (requires confirmation)

---

### 3. View Modes

Must support two switchable views:

#### A. Suit Group View

Group cards by:

- Spades
- Hearts
- Clubs
- Diamonds
- Boxes

#### B. Collection Status View

Group cards by:

- Collected
- Not Collected

---

### 4. Search System

- Search by name / suit / rank
- Must include debounce (300ms)
- Must support partial match filtering
- Must update UI in real time

---

### 5. UI Interaction Rules

- Click card → toggle selection or collected state
- Shift/Ctrl click → multi-select
- Batch actions must operate on selected cards
- Reset actions require confirmation modal

---

## Technical Constraints

### MUST:

- Use React functional components only
- Use Tauri invoke API for all backend calls
- Use state manager (Zustand preferred)
- Keep UI and backend logic strictly separated
- No direct database access in frontend
- No ORM usage anywhere in frontend/backend
- Must support reusable components

### MUST NOT:

- Do not directly manipulate DOM
- Do not embed SQL logic in frontend
- Do not mix API logic inside UI components

---

## Required Architecture

The frontend should be structured as:

- components/
  - Card
  - CardGrid
  - Toolbar
  - SearchBar
  - ConfirmModal

- store/
  - cardStore (state management)

- services/
  - api.ts (Tauri invoke wrappers)

- pages/
  - main layout page

---

## Data Model (Frontend View)

Card object:
{
id: number,
name: string,
suit: "spade" | "heart" | "club" | "diamond" | "box",
rank: string,
collected: boolean
}

---

## Backend API (Tauri Commands)

Frontend MUST call:

- get_cards
- search_cards
- toggle_collect
- batch_update
- reset_collection

via Tauri invoke only.

---

## Output Requirements

Generate:

- React TypeScript frontend code
- Component-based architecture
- State-managed implementation
- Clean separation of UI and logic
- Production-level structure (not prototype code)
- Production-level structure (not prototype code)
