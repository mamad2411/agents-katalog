---
name: bootstrap-mobile
description: Mobile-first Bootstrap 5 UI development targeting iPhone 15 (Safari). Use when building templates, layouts, components, or any HTML/CSS/JS UI for this project. Ensures touch-friendly, performant interfaces.
---

# Bootstrap Mobile — решения этого проекта

Шаблоны уже написаны — смотри `templates/`. Этот скилл про неочевидные правила, которые нельзя угадать.

---

## Цель: iPhone 15, Safari

- Логический viewport: 393×852pt
- Минимальная ширина приложения: 390px
- Браузер: Safari (WebKit) — не Chrome

---

## Touch targets: 44×44pt минимум (Apple HIG)

```css
/* static/css/main.css */
.btn, .form-check-input, .list-group-item-action {
    min-height: 44px;
    min-width: 44px;
}
.form-check-input {
    width: 1.5em;
    height: 1.5em;  /* Bootstrap default слишком мал для пальца */
}
```

Если элемент меньше 44pt — пользователь будет промахиваться.

---

## Safari gotchas

| Проблема | Решение |
|----------|---------|
| `input[type=number]` показывает не ту клавиатуру | Добавь `inputmode="decimal"` для дробных значений |
| `position: fixed` прыгает при открытии клавиатуры | Держи header минимальным, не используй высокие fixed элементы |
| `vh` единицы не учитывают адресную строку | Используй `dvh` или `window.innerHeight` |
| `overscroll-behavior` не работает полностью | Тестируй скролл вручную на реальном устройстве |

---

## Запрещено

- **`user-scalable=no`** в viewport — ломает доступность и нарушает Apple HIG
- **`vh` для полной высоты** — используй `dvh`
- **Хардкодить `px`** для размеров — Bootstrap spacing (`p-3`, `mt-2`) или `rem`
- **Привязывать обработчики к `hover`** — на мобиле hover нет

---

## data-атрибуты (конвенция проекта)

```html
data-purchase-id="42"     <!-- ссылка на Purchase.pk -->
data-category-id="7"      <!-- ссылка на Category.pk -->
```

ID передаются только через `data-*`. Никогда не парсить из текста или href.

---

## Структура шапки (fixed-top)

Шапка фиксирована. После неё обязателен спейсер, иначе контент прячется под header:

```html
<header class="navbar fixed-top ...">...</header>
<div style="height: 60px;"></div>  <!-- компенсация fixed header -->
```
