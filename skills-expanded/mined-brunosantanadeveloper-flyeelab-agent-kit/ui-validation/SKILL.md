---
name: ui-validation
description: Automated UI anti-pattern validation. Detects emojis as icons, missing cursor-pointer, contrast issues, and Design System violations. Use after implementing UI components and before marking styling complete.
allowed-tools: Read, Glob, Grep, Bash
---

# UI Validation Skill

> **Purpose:** Automated detection of common UI anti-patterns that make interfaces look unprofessional.
> **When to Use:** After implementing UI components, before marking Phase complete.

---

## 🔴 Anti-Patterns Detected

| Anti-Pattern | Why It's Bad | Detection |
|--------------|--------------|-----------|
| **Emojis as icons** | Unprofessional, inconsistent sizing | Grep for common emojis |
| **Missing cursor-pointer** | Users don't know element is clickable | Check Links/Buttons |
| **Hardcoded colors** | Breaks Design System | Grep for hex codes |
| **Layout-shifting hovers** | Poor UX, janky feel | Check for scale transforms |
| **Missing transitions** | Abrupt state changes | Check for transition classes |
| **Wrong @theme syntax** | Tailwind classes won't work | Check globals.css |

---

## ⚠️ Tailwind v4 @theme Validation

> [!CAUTION]
> **CRÍTICO:** Se cores/classes Tailwind não funcionam, verificar `globals.css`.

### Sintaxe Correta (Tailwind v4)

```css
/* ✅ CORRETO - Valores diretos dentro de @theme */
@theme {
  --color-primary: #C6F135;
  --color-bg-dark: #0F0F0F;
  --font-sans: 'Plus Jakarta Sans', sans-serif;
}
```

### Sintaxe Incorreta

```css
/* ❌ ERRADO - Não usar :root + @theme inline com var() */
:root {
  --color-primary: #C6F135;
}
@theme inline {
  --color-primary: var(--color-primary);  /* NÃO FUNCIONA */
}
```

### Verificação Manual

```powershell
# Verificar se globals.css usa @theme corretamente
Select-String -Path "src/app/globals.css" -Pattern "@theme inline"
# Se encontrar "@theme inline" → CORRIGIR para "@theme {}"
```

## 🛠️ Usage

### Option 1: Run Script (Recommended)

```bash
python .agent/skills/ui-validation/scripts/ui_antipattern_check.py <project_path>
```

**Example:**
```bash
python .agent/skills/ui-validation/scripts/ui_antipattern_check.py .
```

### Option 2: Manual Commands (PowerShell)

```powershell
# 1. Emojis as icons (PROIBIDO)
Get-ChildItem -Path "src" -Recurse -Include "*.tsx","*.jsx" | Select-String -Pattern "[🔍⚡📊🎨🚀⚙️✨💡🔧📈📌🎯🏆💎🔥⭐🌟✅❌➡️⬅️🔴🟢🟡📁📂💻🖥️📱]"

# 2. Links sem cursor-pointer
Get-ChildItem -Path "src" -Recurse -Include "*.tsx","*.jsx" | Select-String -Pattern "<Link[^>]+>" | Where-Object { $_ -notmatch "cursor-pointer" -and $_ -notmatch "cursor:" }

# 3. Buttons sem cursor-pointer
Get-ChildItem -Path "src" -Recurse -Include "*.tsx","*.jsx" | Select-String -Pattern "<button[^>]+>" | Where-Object { $_ -notmatch "cursor-pointer" }

# 4. Hardcoded hex colors (should use CSS variables)
Get-ChildItem -Path "src" -Recurse -Include "*.tsx","*.jsx" | Select-String -Pattern '#[0-9A-Fa-f]{6}' | Where-Object { $_ -notmatch "shadow" }
```

---

## 📋 Validation Checklist

### Visual Quality
- [ ] **No emojis as icons** - Use SVG (Heroicons, Lucide, Simple Icons)
- [ ] **Consistent icon set** - Don't mix icon libraries
- [ ] **Theme colors only** - No hardcoded hex values in components

### Interaction
- [ ] **cursor-pointer on clickables** - Links, buttons, cards with onClick
- [ ] **Hover feedback** - Visual change on interactive elements
- [ ] **Smooth transitions** - 150-300ms on state changes
- [ ] **Focus states visible** - For keyboard navigation

### Layout
- [ ] **No layout-shifting hovers** - Avoid scale transforms that move content
- [ ] **Responsive** - 375px, 768px, 1024px, 1440px breakpoints
- [ ] **No horizontal scroll** - On any device width

---

## 🔧 Fixing Violations

### Emoji → SVG Icon

```tsx
// ❌ WRONG
<div className="icon">🔍</div>

// ✅ CORRECT
import { MagnifyingGlassIcon } from "@heroicons/react/24/outline";
<MagnifyingGlassIcon className="w-6 h-6" />

// Alternative: Lucide
import { Search } from "lucide-react";
<Search className="w-6 h-6" />
```

### Missing cursor-pointer

```tsx
// ❌ WRONG
<Link href="/about">About</Link>

// ✅ CORRECT
<Link href="/about" className="cursor-pointer hover:text-primary transition-colors">
  About
</Link>
```

### Hardcoded Colors

```tsx
// ❌ WRONG
<div className="bg-[#C6F135]">...</div>

// ✅ CORRECT (using CSS variables via Tailwind)
<div className="bg-primary">...</div>
```

---

## 🔗 Workflow Integration

This skill is called by:

| Workflow | Phase | Trigger |
|----------|-------|---------|
| `/new-project` | Phase 5.3 Gate | Before marking UI Styling complete |
| `/new-task` | Fase 3.7 Gate | If feature has UI changes |
| `/legacy-project` | Phase 5.5 Gate | Before proceeding to tests |
| `/ui-ux-pro-max` | Final Validation | Pre-Delivery Checklist |

### How Workflows Should Call This Skill

```markdown
> [!CAUTION]
> **ANTES DE MARCAR COMPLETO:** Execute validação de UI.
> Skill: `ui-validation` → `python .agent/skills/ui-validation/scripts/ui_antipattern_check.py .`
```

---

## Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `scripts/ui_antipattern_check.py` | Full UI validation | `python scripts/ui_antipattern_check.py <path>` |

---

## Related Skills

| Skill | Relationship |
|-------|--------------|
| `frontend-design` | Design principles (use BEFORE coding) |
| `web-design-guidelines` | Accessibility audit (use AFTER this) |
| `lint-and-validate` | Code quality (separate concern) |
