---
name: render-transactional-emails
description: Use when sending a templated transactional email (or generating a templated PDF/document) — rendering from a named template + data through one shared render service, with per-locale template files, CSS inlining, returning subject/html/text, then dispatching via the notification facade (not inline). Covers reusing the same render for HTML→PDF. NestJS/TS reference, framework-flexible.
metadata:
  author: Ken Nguyễn <ntnpro@gmail.com>
---

# Render transactional emails (and documents)

Producing transactional content — order receipts, OTPs, invites, notices, PDFs — from templates rather
than hand-built strings. Examples NestJS/TS (an `email-templates`/EJS + CSS-inliner stack), neutral
domain. principle → **▸ Example** → **▸ Other stacks**. Sending lives behind the notification facade in
`integrate-external-services` §1; this skill is how the *content* is produced.

## Core principle
**Never concatenate email HTML in a handler.** Render from a **versioned template + a typed data
context** through one shared service — localized and CSS-inlined — and return a `{ subject, html, text }`
the transport sends. Templates hold markup; code holds logic.

## 1. One render service over a template engine
Wrap the template lib (EJS / Handlebars / …) + a CSS inliner (so styles survive email clients) in a
single `render(templateName, context)`; resolve the file by **name + locale convention**; configure the
template root via DI, not hard-coded paths.
```ts
@Injectable() export class TemplateService {
  private email = new Email({
    views: { root, options: { extension: 'ejs' } },
    getPath: (file, template, ctx) => path.join(dir, template, `${file}.${ctx.language ?? 'en'}`), // <template>/<file>.<lang>
    juiceResources: { /* inline CSS */ },
  });
  render(name: string, ctx: { language?: string; data: unknown }) {
    return this.email.renderAll(name, ctx.data);   // → { subject, html, text }
  }
}
```

## 2. Templates are data-driven + localized
- Pass a **typed context** `{ language, data }`; one **folder per template** with **per-locale files**
  (`welcome/subject.en.ejs`, `welcome/html.en.ejs`, …). Adding a language = adding files, no code change.
- **Keep logic out of templates** — format dates/money/decimals in code (a date/decimal lib, see
  `write-service-code` §5) and pass display-ready values in; the template only interpolates.

## 3. Render → dispatch via the facade (separate concerns)
The use-case **renders, then hands off to the notification `send()` facade** — don't call the email
provider inline. Render (content) and transport (channel/vendor) are different responsibilities.
```ts
const { subject, html } = await this.templates.render('membership-invite', { language, data: { name, link } });
await this.notifier.sendEmail({ to, subject, html });   // facade picks the provider — integrate-external-services §1
```
Mask PII before any logging (`write-service-code` §7); don't log full rendered bodies (they hold names/OTPs).

## 4. PDFs reuse the same render
A document (invoice, policy, form) is the **same template render** → then convert the HTML to PDF
(headless browser / a render lambda) and store it (e.g. object storage), returning a URL/ref. Same
template discipline; the HTML→PDF conversion is the only extra step.
```ts
const { html } = await this.templates.render('policy-doc', { language, data });
const pdf = await this.htmlToPdf.convert(html);     // headless/lambda
await this.storage.put(`${id}.pdf`, pdf);           // store + reference
```
▸ *Other stacks:* any engine (Jinja2 / Thymeleaf / Razor / Liquid) + an email lib + an inliner; HTML→PDF
via wkhtmltopdf / Puppeteer / a service. Principle: template + data → localized content, CSS-inlined,
produced once and reused for email or PDF, separate from sending.

## Verification
- Email content comes from a **named template + typed context** via one service — no string-built HTML in handlers.
- Templates are **per-locale files** under a per-template folder; formatting is done in code, not the template.
- The use-case **renders then dispatches via the facade** — the provider isn't called inline; bodies/PII aren't logged.
- PDFs **reuse the same render** then convert + store.

## Related
- `integrate-external-services` §1 — the notification `send()` facade (email/SMS/push) that transports the rendered content.
- `write-service-code` §5 (format money/dates in code), §7 (mask PII, don't log bodies).
- `structure-a-shared-backend-lib` — the render service is a good shared-lib primitive · `handle-files-frontend` (the FE side of file/PDF download).
