---
name: sky-web-components
description: >-
  Web Components ve framework'süz bileşenler: Custom Elements yaşam döngüsü, Shadow DOM ve stil
  kapsülleme (::part, CSS değişkenleri, slot'lar), Lit ile reaktif bileşenler, form ile
  bütünleşme (ElementInternals, form-associated), erişilebilirlik, olaylar, SSR (Declarative
  Shadow DOM), React/Vue içinde kullanım, gömülebilir widget dağıtımı (tek script) ve tasarım
  sistemi paylaşımı. "Her siteye gömülebilir widget", "framework bağımsız bileşen" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Web Components

## Ne zaman?

✓ **Gömülebilir widget** (randevu butonu, sohbet balonu, yorum kutusu — müşterinin her türlü sitesine tek script), birden çok framework'te paylaşılan tasarım sistemi, uzun ömürlü framework bağımsız bileşenler.
✗ Tek framework'lü uygulama içi bileşenler — o framework'ün bileşenleri daha ergonomik.

## Lit ile bileşen

```ts
import { LitElement, html, css } from "lit";
import { customElement, property, state } from "lit/decorators.js";

@customElement("sky-booking-button")
export class SkyBookingButton extends LitElement {
  static styles = css`
    :host { --sky-accent: #2b59ff; display: inline-block; font-family: var(--sky-font, system-ui); }
    button { background: var(--sky-accent); color: white; border: 0; border-radius: 10px; padding: 12px 18px; cursor: pointer; }
    button:focus-visible { outline: 2px solid var(--sky-accent); outline-offset: 2px; }
  `;
  @property({ attribute: "org" }) org = "";
  @state() private open = false;
  render() {
    return html`<button part="button" @click=${() => (this.open = true)} aria-haspopup="dialog">Randevu al</button>
      ${this.open ? html`<sky-booking-dialog org=${this.org} @close=${() => (this.open = false)}></sky-booking-dialog>` : ""}`;
  }
}
```
Müşteri sitesine: `<script type="module" src="https://cdn.site.com/widget.js"></script><sky-booking-button org="acme"></sky-booking-button>`.

## Stil kapsülleme

Shadow DOM dışarının CSS'ini engeller (widget her sitede aynı görünür). Özelleştirme kapıları: **CSS özel özellikleri** (`--sky-accent`), `::part(button)`, `<slot>` ile içerik yerleştirme. Fontlar shadow içine sızmaz — `:host`'ta font ailesi ver veya `@font-face`'i belgeye ekle.

## Formlarla bütünleşme

`static formAssociated = true` + `this.attachInternals()` → özel input'lar native `<form>` gönderimine ve doğrulamasına katılır (`internals.setFormValue`, `setValidity`).

## Erişilebilirlik

Shadow DOM sınırında `aria-labelledby` ID referansları çalışmaz → `ElementInternals` ARIA özellikleri, etiketleri bileşen içinde tut; odak yönetimi (`delegatesFocus: true`); klavye davranışları native öğelerden miras al (içeride gerçek `<button>`).

## Olaylar

`this.dispatchEvent(new CustomEvent("booking-created", { detail: { id }, bubbles: true, composed: true }))` — `composed` shadow sınırını geçer; host sayfa dinler (analitik, yönlendirme).

## SSR ve framework'ler

Declarative Shadow DOM (`<template shadowrootmode="open">`) + `@lit-labs/ssr`; React 19 custom element'leri tam destekler (özellik/olay geçişi), Vue `compilerOptions.isCustomElement`.

## Widget dağıtımı

Tek dosya ES modülü (Vite library mode), küçük boyut (Lit ~5KB), sürümlü CDN yolu (`/v1/widget.js`) + uzun önbellek, iframe yerine Shadow DOM (SEO ve boyutlandırma kolay; tam izolasyon/güvenlik gerekiyorsa iframe), CSP uyumlu (inline script yok), müşteri sitesinin global'lerine dokunmama.
