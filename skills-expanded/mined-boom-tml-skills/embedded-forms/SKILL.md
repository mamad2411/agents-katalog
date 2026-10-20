---
name: embedded-forms
description: Use when the user wants to build, publish, embed or share a form through Boom that sits inside their own page (or on a Boom-hosted link) — a scored test with results ("test de estrés"), a webinar sign-up, a lead form, a Typeform replacement — read its responses, or build a journey on its event. Triggers on "embedded form", "formulario", "form on my landing", "Typeform", "test", "quiz with a result", "webinar registration", "hosted form link", "form responses", "<slug>_submitted".
---

# Embedded forms

An embedded form is a form placed **inside** a page on the customer's website — or on its own Boom-hosted link — built from steps of typed questions, optionally scored, ending on a result. Each response becomes a **lead** in Boom's CDP, a **response** in the form, and one **event** named after the form (e.g. `test_estres_submitted`) that a journey can start from. Pop-ups (the modal with games) are a different kind: see the `lead-capture` skill.

Embedded forms are part of the Lead Capture add-on and have their own switch. Every tool answers `lead_capture_forms_unavailable` until Boom turns them on for the organization.

## Tools used

| Tool | Purpose | Scope |
|---|---|---|
| `lead_capture_embedded_forms_list` | Every form with status, published version and whether the draft has unpublished changes | read |
| `lead_capture_embedded_forms_get` | One form: its editable `draft`, the `embedTag` + `installTag`, and `publishIssues` | read |
| `lead_capture_embedded_forms_create` | Create a form, PAUSED and unpublished, optionally from a full `draft` | write |
| `lead_capture_embedded_forms_update` | Patch the `draft`, replace `allowedOrigins`, set `status` ACTIVE or PAUSED | write |
| `lead_capture_embedded_forms_publish` | Freeze the draft as the next version visitors get; returns the journeys and segments affected | write |
| `lead_capture_form_responses_list` | The responses, newest first: contact, answers by key, score, result, hidden values | read |

Creating, editing and publishing need the **Owner** or **Admin** role. Reading responses also needs access to customer data (People).

## Draft → publish → active

You always edit a **draft**; visitors only ever get a **published version**. The order is:

1. `create` (or `get` an existing one) → edit the draft with `update`.
2. `get` again and show the user `publishIssues` — empty means it can be published.
3. `publish`. If it returns `impact`, tell the user which journeys or segments still read a question, answer or result this version stops producing.
4. `update` with `status: "ACTIVE"` (needs a published version and at least one allowed site).

Pages already open keep working for an hour after a publish. Visitors get a new version within about five minutes.

## Read before you write

`get` first, then send **only what changes** in `draft`:

- Objects merge key by key; **lists replace whole** (`steps`, `fields`, `options`, `endings`, `hidden`, `constants`) — send the full list.
- Unknown fields are refused with their path.
- Text is `{ "en": "…", "es": "…", "pt": "…" }`. A form is written in one language, `language.default` (`en`, `es` or `pt`; set it on create, e.g. `es` for a Spanish form): the required copy must be filled in that language. Visitors whose browser language is fully written see it; everyone else sees the form's own language, never a mix. `language.fixed: true` shows the default language to everyone.

## The draft

| Part | Keys |
|---|---|
| Identity | `slug` (snake_case; names the event `<slug>_submitted` and the person attributes `<slug>_<key>`), optional `eventName` — both **frozen at the first publish** |
| Questions | `steps[]` (`id`, `title`, `fieldIds`) and `fields[]`: `id`, `key` (snake_case, frozen once published), `type` (`short_text`, `long_text`, `email`, `phone`, `number`, `single_choice`, `multi_choice`, `dropdown`, `scale`, `statement`), `label`, `help`, `placeholder`, `required`, `sensitive`, `options[]` (`id`, `value` — what is stored, frozen — `label`, `score`), `scale` (`min`, `max`, labels), `scored`, `mapsTo` (`email`, `phone`, `firstName`, `lastName`), `saveToProfile`, `profileKey` |
| Results | `scoring.enabled`, `endings[]` (`id`, `key` — the stored result — `title`, `body`, `buttonLabel`/`buttonUrl`, `redirectUrl`, `scoreMin`/`scoreMax`). Exactly one ending has no range: it shows when no range matches. Ranges may not overlap |
| Extra data | `hidden[]` (`key`, `from`: `query` or `data`) — carried from the page's address or the container's `data-*`; `utm_*` are kept automatically. `constants[]` (`key`, `value`) — fixed values on every event, e.g. a webinar date |
| Consent | `consent.marketingText` (required when a phone is asked: the WhatsApp opt-in box), `consent.processingText` + `consent.privacyNoticeUrl` (required on a sensitive form), `consent.termsUrl` |
| Design | `look` (one of `paper`, `graphite`, `sand`, `forest`, `ocean`, `plum`, `mono`, `brand`: colours, font and shape in one choice; `brand` is tinted with `accentColor`), `accentColor`, `presentation` (overrides: `font`, `radius`, `answerStyle` `outline`/`filled`, `align`, `questionSize`, `stageHeight`, `backgroundImageUrl` + `backgroundDim`, `transparent`), `style` colour overrides (`background`, `textColor`, `headingColor`, `buttonTextColor`) and `buttonShape`, `width` (`narrow`, `medium`, `full`), `logoUrl`, `copy` (button words), `welcome` (optional first screen: `enabled`, `title`, `body`, `buttonLabel`) |
| Other | `retentionDays`, `enrollmentsPerHour` (journey enrollments per hour, default 50, at most 500; responses past it are saved but not enrolled), `analytics.dataLayer`, `defaultCountry`, `hosted` (below) |

Publishing rules: at least one question; a **required** email or phone question that `mapsTo` the person; option values and keys valid and unique; every live question in exactly one step; endings as above.

**What freezes once published:** keys, question types, option values, where an answer lands (`saveToProfile`, `profileKey`, `mapsTo`), sensitive marks, the slug and the event name. Labels stay editable. A question removed from the draft becomes *retired* (its key stays). To "rename" a key, add a new question.

## Sensitive questions

Mark a question `sensitive` for health data or as private. The form then keeps the answer encrypted, saves it only as a sensitive person attribute (agents see `[redacted]`), leaves the answer — and the score and result — off the event, and requires processing consent and a privacy-notice link. A sensitive question cannot be unmarked, retired or removed from MCP; a person does it in the app. `lead_capture_form_responses_list` always shows sensitive answers to you as `[redacted]` (and the score and result on a sensitive form).

## Install

Give the user both tags from `get`, pasted where the form should appear:

```html
<div data-boom-form="blc_live_…"></div>
<script async src="https://www.useboom.ai/widget/v1/lc/blc_live_…"></script>
```

Every site that shows it must be in `allowedOrigins` (exact origins: `https://example.com` does not cover `https://www.example.com`).

**On a Shopify store** the user places it, not you: in Shopify, **Online Store → Themes → Customize**, open the page that should show the form, **Add section → Custom Liquid**, paste both tags, **Save**. Add the public domain and the `*.myshopify.com` domain to `allowedOrigins` (the theme editor previews on the latter). If they'd rather not touch the theme, use the hosted link below.

**Hosted link** — for ads, bios and emails: set `hosted.enabled: true` (plus `hosted.title` / `hosted.description` for link previews) and publish; the page is `https://www.useboom.ai/f/<org-slug>/<form-slug>`. A hosted form cannot ask for passwords, cards, PINs or one-time codes, and its endings' links must point at an allowed site.

## Journeys on the event

The event `<slug>_submitted` carries every non-sensitive answer by key, `score`, `ending`, hidden values, UTMs, `email`, `phone` and consent. It appears in the journey builder as soon as the form is published. Results are also on the person (`<slug>_result`, `<slug>_score`), so "everyone with result X" is a segment. Journeys only enrol people who ticked the marketing box (or forms that show none; never a sensitive form without an explicit yes), never someone on Do Not Contact (their event says `consent_marketing: false`), and at most `enrollmentsPerHour` an hour per form. To keep another tool in sync while migrating, add an **HTTP request** step that posts the event to it.

A form on its own only collects. After setting one up, offer the next step: a journey on `<slug>_submitted` (build it with `design-journey`) that follows up by result, e.g. a WhatsApp with an approved template (`whatsapp-templates`) and an email fallback for people without a phone.
