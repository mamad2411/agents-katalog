# Jak zorganizować reguły (.cursor/rules), żeby agent pracował wydajniej

Reguły w Cursor to pliki **`.mdc`** w katalogu **`.cursor/rules/`**. Dzięki nim agent ma stały kontekst bez powtarzania tych samych zasad w chacie.

---

## 1. Gdzie i w jakim formacie

- **Lokalizacja:** `.cursor/rules/`
- **Format plików:** `.mdc` (Markdown z YAML frontmatter na górze)
- **Jedna reguła = jeden plik**, jeden główny temat (krótko, konkretnie, najlepiej &lt; 50 linii).

---

## 2. Frontmatter (obowiązkowy nagłówek)

Każdy plik `.mdc` musi zaczynać się od bloku YAML:

```yaml
---
description: Krótki opis, co ta reguła robi (widać w rule pickerze)
globs: "**/*.html"        # opcjonalnie – kiedy reguła ma działać (np. tylko index.html)
alwaysApply: false        # true = reguła zawsze aktywna w każdej sesji
---
```

- **`alwaysApply: true`** – używaj dla zasad ogólnych (styl kodu, commity, spec.md, checklisty), które mają obowiązywać przy każdej zmianie.
- **`globs`** – używaj, gdy reguła dotyczy tylko konkretnych plików (np. `index.html`, `**/sw.js`, `**/*.js`). Dzięki temu agent ładuje ją tylko przy pracy z tymi plikami.

---

## 3. Propozycja struktury dla tego repo (beskider)

| Plik | Opis | alwaysApply | globs (jeśli nie always) |
|------|------|-------------|---------------------------|
| `project-overview.mdc` | Struktura projektu, kto co robi (index.html, app.js, sw, assets, spec.md), gdzie ikony/Font Awesome | `true` | — |
| `content-and-spec.mdc` | Zasady aktualizacji spec.md (§6, §7), nowe sekcje, nowe linki w nav, planowanie zmiany (checklist) | `true` | — |
| `styling-and-assets.mdc` | Tailwind, 8px grid, nazewnictwo plików (lowercase, hyphens), brak HDR, pobieranie zasobów z URL | `true` | — |
| `index-html.mdc` | Markup: section, section__head, rules-grid, rule-card; gdzie style (@layer) | `false` | `**/index.html` |
| `pwa-and-sw.mdc` | Kiedy bump CACHE_VERSION, ASSETS, manifest, CSP | `false` | `**/sw.js`, `**/manifest.json` |
| `testing-and-qa.mdc` | TESTING.md, debug:nav, manual checks, co testować po zmianach | `false` | (można alwaysApply: true jeśli chcesz, żeby agent zawsze pamiętał o testach) |

**Dlaczego tak:**  
- **Zawsze w kontekście** są tylko 2–3 reguły (overview + content/spec + styling), więc agent nie jest przeciążony, ale ma podstawy.  
- **Reszta** ładuje się przy otwieraniu/edycji konkretnych plików (np. index.html, sw.js), więc jest precyzyjna i wydajna.

---

## 4. Dobre praktyki (żeby agent faktycznie z tego korzystał)

- **Krótko:** mało tekstu, bullet points, konkretne przykłady (np. „dobrze: …”, „źle: …”).
- **Jedna odpowiedzialność na plik:** np. osobno „spec.md i IA”, osobno „PWA i sw.js”.
- **Konkretne przykłady:** zamiast „aktualizuj spec” → „dla nowej sekcji: dopisać w spec.md §6 (Struktura informacji) i ewentualnie §7 (Nawigacja)”.
- **Akcje, nie teoria:** formułuj jak checklisty / instrukcje („Zrób X”, „Przy nowej sekcji: 1. … 2. …”).

---

## 5. Krok po kroku – jak to wdrożyć

1. **Utwórz katalog:**  
   `mkdir -p .cursor/rules`

2. **Skopiuj z AGENTS.md do reguł:**  
   Weź fragmenty z `AGENTS.md` i rozbij je na pliki `.mdc` według tabeli powyżej. W frontmatter ustaw `description` i `alwaysApply` / `globs`.

3. **Nie duplikuj całego AGENTS.md:**  
   W regułach trzymaj skondensowane, „agentowe” wersje (co ma zrobić, w jakiej kolejności); pełną dokumentację możesz zostawić w AGENTS.md i w regułach dać odwołanie: „szczegóły w AGENTS.md”.

4. **Testuj:**  
   Otwórz `index.html`, poproś agenta o zmianę w sekcji – sprawdź, czy stosuje konwencje z reguł. To zweryfikuje, czy `globs` i opisy działają.

---

## 6. Przykład minimalnej reguły (always apply)

**Plik:** `.cursor/rules/content-and-spec.mdc`

```markdown
---
description: Aktualizacja spec.md i planowanie zmiany treści/UI
alwaysApply: true
---

# Treść i spec

- Każda zmiana UI, treści lub zasobów → aktualizacja **spec.md**.
- Nowa sekcja lub nowy link w nav → **spec.md §6 (Struktura informacji)** oraz w razie potrzeby §7 (Nawigacja).

## Przy nowej sekcji / nowym bloku treści
1. Zaktualizować spec.md (§6, ewentualnie nowy podrozdział).
2. W index.html: markup z istniejących komponentów (section, section__head, rules-grid / rule-card).
3. Dodać link w nav.
4. sw.js: tylko gdy dodane/usunięte pliki w ASSETS; ewentualnie bump data-build.
```

---

Dzięki takiej strukturze agent ma zawsze pod ręką overview + content/spec + styling, a przy edycji `index.html` czy `sw.js` dostaje dodatkowo reguły dopasowane do tych plików – co zwiększa wydajność i spójność zmian.
