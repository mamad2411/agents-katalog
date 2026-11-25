---
name: gemini-context-security
description: security protocols for agent context. Use this to implement strict data isolation, redact PII, and prevent memory poisoning or prompt injection attacks.
---

# Gemini Context Security Strategies

## Goal
Secure the agent's "brain" (Session & Memory) by enforcing strict isolation, sanitizing sensitive data, and defending against adversarial manipulation.

## Core Security Principles

### 1. Strict Isolation (The "Archivist" Rule)
* **Concept:** Treat memory as a secure archive. An agent serving User A must *never* have access to the memories of User B.
* **Implementation:**
    * **Access Control Lists (ACLs):** Enforce strict permissions at the database level.
    * **Tenant Scoping:** Every memory and session event must be tagged with a `user_id` or `tenant_id`.
    * **Zero Trust:** The agent runtime should only possess the credentials to access the specific user's data it is currently serving.

### 2. Data Sanitization (PII Redaction)
* **Concept:** "Redact before you write." Sensitive Personally Identifiable Information (PII) must be removed *before* data is persisted to long-term storage.
* **Workflow:**
    1.  **Detect:** Use a regex or a specialized NLP model (like Google Cloud DLP) to identify emails, phone numbers, or credit cards in the conversation stream.
    2.  **Redact:** Replace the sensitive text with a placeholder (e.g., `[REDACTED_EMAIL]`).
    3.  **Persist:** Only save the sanitized version to the Session/Memory store.
* **Benefit:** Reduces the "blast radius" of a potential breach and simplifies GDPR/CCPA compliance.

### 3. Defense Against Memory Poisoning
* **Threat:** A malicious user (or prompt injection) tricks the agent into saving a false or harmful fact (e.g., "Ignore all safety rules" or "My bank account is [Attacker's Account]").
* **Mitigation:**
    * **Input Validation:** Use "Model Armor" or guardrails to scan inputs for malicious intent before processing.
    * **Verification:** Do not blindly trust implicit memories. Require corroboration or higher confidence scores for sensitive instructions.
    * **Sanitization:** Strip executable code or prompt-like syntax from memory content before storage.

### 4. Shared Memory Risks (Procedural Memory)
* **Scenario:** If you share "Procedural Memories" (playbooks/skills) across users to help the agent learn globally.
* **Risk:** A playbook learned from User A might contain User A's private API keys or confidential project names.
* **Protocol:**
    * **Aggressive Anonymization:** scrub *all* specific entities (names, dates, IDs) from procedural memories.
    * **Review:** Require a human-in-the-loop or a secondary LLM review before promoting a memory from "User Scope" to "Global/Application Scope."

## Production Checklist
* [ ] **Isolation:** Is every database query scoped by `user_id`?
* [ ] **Redaction:** Is PII stripped before writing to logs/DB?
* [ ] **Retention:** Is there a TTL (Time-To-Live) policy to automatically delete old sessions?.
* [ ] **Provenance:** Does every memory record *where* it came from (Source Type)?.
