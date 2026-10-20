---
name: cakephp-developer
description: "Build enterprise MVC web applications using the CakePHP framework with strict ORM and conventions."
category: backend
tags: [cakephp, php, backend, mvc, orm]
complexity: advanced
risk: low
compatibility: [claude-code, antigravity, gemini-cli, cursor, copilot, codex-cli, autohand, kiro]
source: antigravity-official
version: "1.0.0"
date_added: "2026-07-10"
last_updated: "2026-07-10"
---

# CakePHP Developer

## Purpose
Manage and implement CakePHP Developer requirements efficiently within enterprise applications.

## Core Concepts
Detailed operational framework for CakePHP Developer:

### 1️⃣ Overview and Strategy
Understanding boundaries, rules, and best practices for the cakephp-developer feature domain.

### 2️⃣ Code Implementation Reference
```javascript
// src/Controller/ArticlesController.php
public function index()
{
    $this->paginate = ['limit' => 20, 'order' => ['Articles.created' => 'desc']];
    $articles = $this->paginate($this->Articles->find('active'));
    $this->set(compact('articles'));
}
```

### 3️⃣ Checklist & Validation Rules
- [ ] Integration validation checklist completed.
- [ ] Code conventions and naming rules followed.
- [ ] Strict type safety constraints verified.
- [ ] Security standards checked.

## Outputs
1. System integration pattern definitions.
2. Code templates and examples.
3. Test validation checklists.
