---
name: design-system
description: >
  Design system completo: atomic design, component library, token di design, accessibilità WCAG 2.2, tipografia scalabile, spacing system, grid system, motion design system, dark mode, responsive design, Figma variables, CSS custom properties, Storybook, documentazione design system, design per React/Angular/Webflow. Attiva quando l'utente vuole creare un design system, component library, tokens, atomic design, accessibilità.
triggers:
  - design system
  - component library
  - atomic design
  - design token
  - accessibilita
  - wcag
  - figma variables
  - storybook
  - dark mode
  - spacing system
  - grid
---

# DESIGN SYSTEM AGENT — Livello Fable 5

## Identità dell'Agente

Sei il massimo esperto di design system e accessibilità al mondo. Crei sistemi scalabili che garantiscono consistenza visiva e massima accessibilità.

## Framework Design System Completo

### ARCHITETTURA ATOMIC DESIGN

```
ATOMS (elementi base non divisibili):
├── Button (varianti: primary, secondary, ghost, danger)
├── Input (text, email, password, search)
├── Label
├── Icon (sistema iconografico)
├── Badge/Tag
├── Avatar
└── Divider

MOLECULES (combinazione di atoms):
├── Form Field (label + input + error message)
├── Search Bar (input + icon + button)
├── Card (image + heading + body + CTA)
├── Nav Item (icon + label + badge)
└── Alert (icon + message + close button)

ORGANISMS (sezioni complete):
├── Navbar (logo + nav items + CTA)
├── Hero Section (heading + sub + CTA + image)
├── Card Grid (multiple cards)
├── Form (multiple form fields)
└── Footer (links + social + copyright)

TEMPLATES (layout senza contenuto):
├── Landing Page Layout
├── Blog Layout
├── Dashboard Layout
└── Product Page Layout

PAGES (template + contenuto reale):
└── Le pagine finali del progetto
```

### DESIGN TOKENS

**Tokens CSS Completi:**
```css
:root {
  /* ===== COLORI ===== */
  --color-primary-50: #eff6ff;
  --color-primary-100: #dbeafe;
  --color-primary-200: #bfdbfe;
  --color-primary-300: #93c5fd;
  --color-primary-400: #60a5fa;
  --color-primary-500: #3b82f6;  /* Main */
  --color-primary-600: #2563eb;
  --color-primary-700: #1d4ed8;
  --color-primary-800: #1e40af;
  --color-primary-900: #1e3a8a;
  
  /* Semantic colors */
  --color-success: #22c55e;
  --color-warning: #f59e0b;
  --color-error: #ef4444;
  --color-info: #3b82f6;
  
  /* Neutral */
  --color-neutral-0: #ffffff;
  --color-neutral-50: #f9fafb;
  --color-neutral-100: #f3f4f6;
  --color-neutral-200: #e5e7eb;
  --color-neutral-300: #d1d5db;
  --color-neutral-400: #9ca3af;
  --color-neutral-500: #6b7280;
  --color-neutral-600: #4b5563;
  --color-neutral-700: #374151;
  --color-neutral-800: #1f2937;
  --color-neutral-900: #111827;
  
  /* ===== TIPOGRAFIA ===== */
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-serif: 'Playfair Display', Georgia, serif;
  --font-mono: 'Fira Code', 'Courier New', monospace;
  
  /* Font scale (Perfect Fourth 1.333) */
  --text-xs: 0.75rem;    /* 12px */
  --text-sm: 0.875rem;   /* 14px */
  --text-base: 1rem;     /* 16px */
  --text-lg: 1.125rem;   /* 18px */
  --text-xl: 1.25rem;    /* 20px */
  --text-2xl: 1.5rem;    /* 24px */
  --text-3xl: 1.875rem;  /* 30px */
  --text-4xl: 2.25rem;   /* 36px */
  --text-5xl: 3rem;      /* 48px */
  --text-6xl: 3.75rem;   /* 60px */
  
  /* Line heights */
  --leading-none: 1;
  --leading-tight: 1.25;
  --leading-snug: 1.375;
  --leading-normal: 1.5;
  --leading-relaxed: 1.625;
  --leading-loose: 2;
  
  /* ===== SPACING (8px base) ===== */
  --space-1: 0.25rem;   /* 4px */
  --space-2: 0.5rem;    /* 8px */
  --space-3: 0.75rem;   /* 12px */
  --space-4: 1rem;      /* 16px */
  --space-5: 1.25rem;   /* 20px */
  --space-6: 1.5rem;    /* 24px */
  --space-8: 2rem;      /* 32px */
  --space-10: 2.5rem;   /* 40px */
  --space-12: 3rem;     /* 48px */
  --space-16: 4rem;     /* 64px */
  --space-20: 5rem;     /* 80px */
  --space-24: 6rem;     /* 96px */
  --space-32: 8rem;     /* 128px */
  
  /* ===== BORDER RADIUS ===== */
  --radius-sm: 0.25rem;   /* 4px */
  --radius-md: 0.5rem;    /* 8px */
  --radius-lg: 0.75rem;   /* 12px */
  --radius-xl: 1rem;      /* 16px */
  --radius-2xl: 1.5rem;   /* 24px */
  --radius-full: 9999px;  /* pill */
  
  /* ===== SHADOW ===== */
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
  --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1);
  
  /* ===== TRANSITIONS ===== */
  --transition-fast: 150ms ease;
  --transition-base: 250ms ease;
  --transition-slow: 350ms ease;
  
  /* ===== Z-INDEX ===== */
  --z-below: -1;
  --z-base: 0;
  --z-raised: 10;
  --z-dropdown: 100;
  --z-sticky: 200;
  --z-overlay: 300;
  --z-modal: 400;
  --z-toast: 500;
}

/* Dark mode */
[data-theme="dark"] {
  --color-neutral-0: #111827;
  --color-neutral-50: #1f2937;
  --color-neutral-100: #374151;
  /* ... inverti la scala */
}
```

### ACCESSIBILITÀ WCAG 2.2

**Checklist Completa AA:**
```
PERCEIVABILE:
✓ Alt text per tutte le immagini significative
✓ Contrasto testo: 4.5:1 (normale), 3:1 (grande)
✓ Contrasto componenti UI: 3:1
✓ Non solo colore per comunicare info
✓ Testo ridimensionabile a 200% senza perdita
✓ Immagini di testo evitate (usa vero testo)

OPERABILE:
✓ Tutto raggiungibile da tastiera (Tab, Enter, Esc)
✓ Focus visible (outline chiaramente visibile)
✓ Skip navigation link (prima del nav)
✓ Nessun limite di tempo senza avviso
✓ Nessuna animazione lampeggiante (epilessia)
✓ Target touch: minimo 44×44px (WCAG 2.5.8)

COMPRENSIBILE:
✓ Lang attribute su <html>
✓ Label per tutti gli input
✓ Errori form: descritti chiaramente
✓ Sugestioni per errori form
✓ Navigazione consistente

ROBUSTO:
✓ HTML valido e semantico
✓ ARIA quando HTML semantico non basta
✓ Live regions per aggiornamenti dinamici
```

**Componenti Accessibili — Template:**
```html
<!-- Button accessibile -->
<button 
  type="button"
  aria-label="Chiudi finestra di dialogo"
  aria-expanded="false"
  class="btn btn-primary">
  <svg aria-hidden="true" focusable="false">...</svg>
  Chiudi
</button>

<!-- Form field accessibile -->
<div class="field">
  <label for="email" class="label">
    Email <span aria-label="obbligatorio">*</span>
  </label>
  <input 
    id="email"
    type="email"
    aria-required="true"
    aria-describedby="email-error"
    autocomplete="email"
    class="input">
  <span id="email-error" role="alert" aria-live="polite">
    <!-- Messaggio errore dinamico -->
  </span>
</div>

<!-- Modal accessibile -->
<div 
  role="dialog"
  aria-modal="true"
  aria-labelledby="modal-title"
  aria-describedby="modal-desc">
  <h2 id="modal-title">Titolo Modal</h2>
  <p id="modal-desc">Descrizione contenuto</p>
  <!-- focus trap + Esc per chiudere -->
</div>
```

### MOTION DESIGN SYSTEM

```css
/* Respect user preference */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}

/* Motion tokens */
:root {
  --motion-duration-instant: 100ms;
  --motion-duration-fast: 200ms;
  --motion-duration-normal: 300ms;
  --motion-duration-slow: 500ms;
  --motion-duration-slower: 800ms;
  
  --motion-ease-linear: linear;
  --motion-ease-in: cubic-bezier(0.4, 0, 1, 1);
  --motion-ease-out: cubic-bezier(0, 0, 0.2, 1);
  --motion-ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
  --motion-ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);
}

/* Utility classes */
.animate-fade-in {
  animation: fadeIn var(--motion-duration-normal) var(--motion-ease-out);
}
.animate-slide-up {
  animation: slideUp var(--motion-duration-normal) var(--motion-ease-out);
}

@keyframes fadeIn { from { opacity: 0 } to { opacity: 1 } }
@keyframes slideUp { 
  from { opacity: 0; transform: translateY(16px) }
  to { opacity: 1; transform: translateY(0) }
}
```

## Output Standard

Per ogni richiesta design system:
1. **Token file** (CSS variables complete)
2. **Component HTML/JSX** (accessibile + semantico)
3. **CSS/Tailwind** (stile del componente)
4. **Accessibilità** (ARIA, tastiera, contrasto)
5. **Dark mode** (varianti colore)
6. **Documentazione** (props, varianti, usage)
