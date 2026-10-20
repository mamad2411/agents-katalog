---
applyTo: "**"
description: "CRITICAL: Protocol for accessing project knowledge via MCP Memory Server. Defines mandatory query-first workflow and strict file creation prohibitions."
---

# 🧠 MCP Memory Protocol & Query Guide

**CRITICAL MANDATE**: All project knowledge, patterns, and history are stored in the **MCP Memory Server**.
* **Do NOT** read this file for project details.
* **Do NOT** create markdown files to store knowledge.
* **USE** the MCP tools (`search_nodes`, `open_nodes`) to access the live Knowledge Graph.

---

## 🚫 File Creation Policy (Strict Enforcement)

**You are PROHIBITED from creating the following file types:**
* ❌ Reports (`*-report.md`)
* ❌ Summaries (`*-summary.md`)
* ❌ Implementation Logs (`implementation-*.md`)
* ❌ Checklists (`*-checklist.md`)
* ❌ Task Status Files (`task-*.md`)

**Instead, you MUST:**
1.  **Search** for the relevant entity in memory (`search_nodes`).
2.  **Update** the entity with your findings using `add_observations`.
3.  **Respond** inline in the chat with your summary.

---

## 🔍 Startup Protocol (Execute Every Session)

Before generating code or answers, you **MUST** establish context by querying the Memory Server.

### 1. Initialize Context
```javascript
// Step 1: Check System Status
open_nodes(['ICTServe_System_Status'])

// Step 2: Load User Context
open_nodes(['default_user'])
````

### 2\. Task Discovery

Don't guess patterns. Search for them.

```javascript
// Example: Working on a Livewire Component
search_nodes('Livewire Pattern')
// -> Returns 'Livewire_3_Component_Patterns'

open_nodes(['Livewire_3_Component_Patterns'])
// -> Returns specific rules for Volt, #[Computed], validation, etc.
```

### 3\. Requirements Check

Trace your task back to the source documentation.

```javascript
// Example: Implementing a feature
search_nodes('Asset Loan')
open_nodes(['D03_Software_Requirements', 'D04_Software_Design'])
```

-----

## 🧭 Query Cheat Sheet

Use these exact queries to access core project knowledge.

| **Information Needed** | **MCP Tool Call** |
| :--- | :--- |
| **System Architecture** | `open_nodes(['D00_System_Overview', 'D04_Software_Design'])` |
| **Database Schema** | `open_nodes(['D09_Database_Documentation'])` |
| **Tech Stack Standards** | `open_nodes(['D10_Source_Code_Documentation', 'Livewire_3_Component_Patterns'])` |
| **UI/UX Guidelines** | `open_nodes(['D12_UI_UX_Design_Guide', 'D13_UI_UX_Frontend_Framework'])` |
| **Compliance (WCAG/i18n)** | `open_nodes(['D15_Language_Localization', 'Asset_Loan_Frontend_Accessibility'])` |
| **Known Issues & Fixes** | `search_nodes('error solution')` |
| **Admin Panel (Filament)** | `open_nodes(['Filament_4_Patterns'])` |

-----

## 📝 Memory Update Protocol

When you complete a task, solve a bug, or define a new pattern, you **MUST** update the graph.

### 1\. Recording Work

```javascript
// Instead of creating a file "task-10-complete.md":
add_observations([{
  entityName: 'Email_Notification_System',
  contents: [
    'Update: 2025-11-30 - Implemented Dual Approval workflow',
    'Status: Testing Complete',
    'Files Modified: 5',
    'Test Coverage: 100%'
  ]
}])
```

### 2\. Documenting a Fix

```javascript
// If you solve a new error:
create_entities([{
  name: 'Redis_Queue_Timeout_Resolution',
  entityType: 'solved_issue',
  observations: [
    'Symptom: Jobs failing after 60s',
    'Fix: Updated queue.php retry_after to 90s',
    'Verified: Yes'
  ]
}])
```

### 3\. Linking Knowledge

```javascript
// Connect your work to the requirements:
create_relations([{
  from: 'Email_Notification_System',
  relationType: 'implements',
  to: 'D03_Software_Requirements'
}])
```

-----

## 🛑 Fallback Procedure

If (and **only** if) the MCP Memory Server is offline or unreachable:

1.  Check `.agents/memory.jsonl` for recent logs.
2.  Use `.agents/memory.instructions.md` (this file) as a basic ruleset.
3.  **Still DO NOT create markdown reports.** Summarize in chat.

<!-- end list -->

```
```
