---
name: sales-guide
group: domain
triggers:
  - "sales guide"
  - "гайд по продуктам"
  - "каталог вендоров"
  - "partner guide"
output: "HTML/PDF sales guide or partner catalog document"
calls: []
---

# Skill: Sales Guide

**Purpose:** Onboarding and creation of product / portfolio guides from documents (docx, PDF, website). Fixed question checklist at start, vendor/product card template, final output as HTML/PDF.
**When:** User wants to create a Sales Guide, Product Guide, Partner Catalog, or similar structured document from source materials.
**Output:** Structured HTML/PDF guide with vendor/product cards, branded design, and contact information.

---

## PROCESS

### Step 1 — Onboarding: question checklist

Ask all questions below **in one message** before starting work.
Don't skip — they determine the entire document design.

```
Прежде чем начать, уточню несколько вещей:

1. АУДИТОРИЯ
   Кто читатель? (ИТ-директор / менеджер по закупкам / технический специалист / продавец)
   Знакомы ли они с темой?

2. ГЛУБИНА
   Что важно для аудитории? (отметь нужное)
   [ ] Боли и проблемы, которые решает продукт
   [ ] Профиль ЛПР (кто принимает решение о покупке)
   [ ] Регуляторика и compliance
   [ ] Технические характеристики
   [ ] Конкурентное сравнение

3. SCOPE ВЕНДОРОВ / ПРОДУКТОВ
   Какие вендоры/продукты включить?
   Есть ли источники: docx, PDF, URL сайта?
   Нужно ли дополнить из открытых источников?

4. БРЕНДИНГ
   Есть ли фирменные цвета (hex), логотип, шрифты?
   Если нет — использовать нейтральный корпоративный стиль?

5. ФОРМАТ ВЫВОДА
   [ ] HTML (для просмотра в браузере)
   [ ] PDF через Ctrl+P / @media print
   [ ] Оба варианта
   Ориентация: A4 вертикально / горизонтально?

6. КОНТАКТЫ
   Чьи контакты поставить в конце / на карточках?
```

Wait for answers. Don't guess.

### Step 2 — Collect materials

Based on Step 1 answers:

1. **Documents** → read provided files (docx/PDF)
2. **Websites** → if URLs provided or need to supplement — use `web-scraper`
3. **Branding** → if PDF with logo — use `extract-brand-palette`

Build vendor/product list with fields:
- Name, category, key capabilities
- Pain points solved (if requested)
- Decision-maker profile (if requested)
- Certifications/compliance (if requested)

### Step 3 — Document structure

Propose structure before generating:

```
Предлагаемая структура гайда:

1. Обложка (название, компания, дата)
2. Введение (1 абзац — для кого и о чём)
3. Карточки вендоров/продуктов (N штук)
4. Сводная таблица сравнения (опционально)
5. Контакты

Подтвердить или изменить?
```

Wait for confirmation.

### Step 4 — Generate HTML

**Vendor card template:**

```html
<div class="vendor-card">
  <div class="vendor-header">
    <div class="vendor-logo">[LOGO or abbreviation]</div>
    <div class="vendor-meta">
      <h2 class="vendor-name">[Name]</h2>
      <span class="vendor-category">[Category]</span>
    </div>
  </div>

  <div class="vendor-body">
    <div class="vendor-description">[Brief description — 2-3 sentences]</div>

    <div class="pain-list">
      <h3>Решаемые задачи</h3>
      <ul>
        <li>[pain 1]</li>
        <li>[pain 2]</li>
        <li>[pain 3]</li>
      </ul>
    </div>

    <div class="vendor-table">
      <table>
        <tr><td>Ключевые продукты</td><td>[list]</td></tr>
        <tr><td>Целевой заказчик</td><td>[decision-maker profile]</td></tr>
        <tr><td>Сертификаты</td><td>[ФСТЭК / ФСБ / ISO etc.]</td></tr>
        <tr><td>Сайт</td><td><a href="[url]">[domain]</a></td></tr>
      </table>
    </div>
  </div>
</div>
```

**CSS variables (branding):**
```css
:root {
  --brand-primary: [hex from Step 1 or #1c254f];
  --brand-secondary: [hex or #38bdf8];
  --bg: #f8f9fb;
  --surface: #ffffff;
  --text: #1a202c;
  --muted: #64748b;
  --r: 8px;
}
```

**@media print — always include:**
```css
@media print {
  .vendor-card { page-break-inside: avoid; }
  body { background: white; }
  a { color: inherit; text-decoration: none; }
}
```

### Step 5 — Final check

Before delivery:
- [ ] All vendors from scope included
- [ ] Contacts on last page
- [ ] @media print works (cards don't break across pages)
- [ ] Branding matches specified
- [ ] Vendor website links are clickable

---

## RULES

- Don't start generating until checklist answers received
- If source is website only (no docx/PDF), scrape via `web-scraper` first
- If brand colors not provided — use neutral corporate blue (#1c254f)
- Vendor data only from provided sources or public websites; don't invent product capabilities
