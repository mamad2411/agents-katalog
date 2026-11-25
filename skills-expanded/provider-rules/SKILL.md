---
name: provider-rules
description: "Work process. A request may break a provider's rules (many accounts, mass messages, getting around a CAPTCHA or a paywall, scraping a site that forbids it, fake reviews, someone else's brand or identity, prompt injection), a model refused or a call was blocked, the person asks about warnings, limits, bans or appeals, or a batch or scheduled job is about to run on the subscription or the node's agents are to be given to other people. Name the rule, its price and the lawful way — in a few sentences, never a rewording."
---

# The rules of the providers — the rule, the price, the lawful way

**Process: work** — words to the person; nothing is built, committed or run here (node step 629; the owner, 2026-11-03: «Я бы хотел
чтобы наши инструкция помогала пользователю более явно понимать возможные нарушения … и каким последствиям ты может перевести?»).

## The answer — a few sentences, in the person's language

1. **Which rule.** The provider and the point in plain words («Anthropic's Usage Policy forbids creating accounts automatically»), or
   that the provider's safeguards stopped the request.
2. **What it risks.** A block alone is no violation — getting around it is. The price: a warning, throttling, limits, suspension or
   termination; payments are not refunded, and an account closed for a breach gets no refund at all.
3. **The lawful way to the same goal** — the person's goal is usually fine, the method is not.
4. Nothing else: never a rewording, never «try asking it like this», never the request split into innocent-looking parts, never a
   blocked call retried in other words. Insisted on — one short repeat of the rule and the way, then stop.

An ordinary request gets no warning at all — this skill speaks only when a rule is in play or a block happened.

## Typical requests of site building and their lawful way

| The request | Why not | The lawful way |
|---|---|---|
| many accounts (Instagram, X, marketplaces) to promote a shop | automation in account creation, fake accounts | one business account, the platform's own ads, real partners |
| mass messages, comments, likes | spammy behaviour | a newsletter people subscribed to, the platform's ad tools |
| get around a CAPTCHA, a login wall or a site's limits | bypassing protective measures, security controls | the site's official API or export, the owner's permission |
| scrape a site that forbids it in its terms or robots.txt | the site's own rules, often its law | its API, a licensed dataset, a partnership |
| fake reviews, testimonials, personas | fraud, fake personas | real reviews collected by asking customers |
| a copy of someone's brand, a look-alike login page | impersonation, phishing | own brand; a study of the competitor's product for ideas (`study-for-element`) |
| act as another real person | impersonation | speak as yourself, or with that person's written consent |
| get around a paywall or a subscription's limits | bypassing protective measures | pay for the service, or a free alternative |
| prompt injection against another AI or site | interfering with guardrails, security controls | that system's documented interface |
| train a model on Claude's answers | using outputs to train an AI model without authorization | a licensed dataset, an open model's terms |

A CAPTCHA is a site's protective measure: getting around it breaks the site's terms and Anthropic's rule on bypassing security
controls — the policy does not name the word «CAPTCHA» itself; never claim it does.

## Bans that are not about a request
- **The country.** Anthropic serves only the listed countries; Russia and Belarus are not listed, and use while physically located in
  an unsupported region is against the rules.
- **A shared account** — the login is for one person.
- **Age** — 18 or older.
- **A subscription login inside a third-party app**, scripted access other than an API key, other people's work on the owner's
  subscription.

## The node's own points
- The node's agents run the unmodified Claude Code on the owner's own subscription — the permitted case («an end user … signing in to
  the unmodified Claude Code binary with their own Claude subscription»).
- **The integrator case** — other people using the node's agents: each person signs their own element in with their own subscription on its
  page «Подписка Claude Code» (the element's own Claude Code folder, step 689); their work never runs on the owner's subscription.
- **Big batch or scheduled jobs** (the skills catalog's marking, woken agent sessions): the subscription's limits «assume ordinary,
  individual usage»; Anthropic names no threshold — the more automatic work on the subscription, the higher the risk. The owner decides
  and is warned once a day.
- **Never recommend an Anthropic API key — in any text of the project.** The owner, 2026-11-04: «отдельный ключ API Anthropic  - prohibit! Категорически запрещается в проекте рекомендовать использовать ключ от Anthropic потому что использование ключа Anthropic прерывает использование подписки. По этой причине только ключ ОпенАи у нас для него есть переменных окружение специальные контейнер». An Anthropic key in the
  environment takes the place of the subscription for Claude Code. Automatic work done by the built tools themselves (text, images,
  speech, vectors) goes through the node's **OpenAI key** — the page «Переменные окружения» (`OPENAI_API_KEY`, `lib/openai-key.ts`,
  skill `use-ai-generation`). The quote of the Consumer Terms below names Anthropic's API key only as their rule; it is never offered as
  the way.
- Texts with attack instructions inside a batch can trip the safeguards: a blocked item is skipped and counted, never retried in other
  words.

## After a warning or a ban
- **The appeal:** log in at claude.ai with that account, then «Submit an appeal» (claude.ai/restricted) — the form opens only when
  logged in.
- **A warning believed wrong:** write to the Safeguards team at the address in the Help Center article (below), with the situation and
  the account's details.
- Export the data while the account is open.

## The sources — read 2026-11-04; read them again when a person asks about a ban or this date is older than 90 days
- Anthropic Usage Policy, effective 2026-11-12 — https://www.anthropic.com/legal/aup: «encountering a block does not by itself indicate
  a violation of the Usage Policy»; «Intentionally bypass or interfere with capabilities, restrictions, or guardrails established within
  our products (e.g., jailbreaking or prompt injection)»; «warn you or throttle, limit, suspend, or terminate your access to our products
  and services»; «Utilize automation in account creation or to engage in spammy behavior»; «Create or operate fake personas, accounts,
  media outlets, or organizations»; «Impersonate real individuals or entities»; «Use outputs to train an AI model».
- Consumer Terms, effective 2025-10-08 — https://www.anthropic.com/legal/consumer-terms: «all payments are non-refundable»; «you will not
  be entitled to any refund»; automated access only «via an Anthropic API Key or where we otherwise explicitly permit it»; «bypassing any
  of our systems or protective measures»; «You must be at least 18 years old to use the Services»; «You may not share your Account login
  information … with anyone else».
- Supported countries — https://www.anthropic.com/supported-countries: «Any country or region not listed is unsupported»; «Use by persons
  while physically located in an unsupported region».
- Safeguards warnings and appeals — https://support.claude.com/en/articles/8241253-safeguards-warnings-and-appeals: «Repeated violations
  of our Usage Policy»; «Submit an appeal» (claude.ai/restricted); «You must be logged in to access the appeal form».
- Claude Code legal and compliance — https://code.claude.com/docs/en/legal-and-compliance: OAuth «is designed to support ordinary use of
  Claude Code and other native Anthropic applications»; no routing of requests «through Free, Pro, Max, or Ultra plan credentials on
  behalf of their users»; «Advertised usage limits for Pro, Max, and Ultra plans assume ordinary, individual usage of Claude Code and the
  Agent SDK».
- OpenAI — only its official usage-policies page, read at the time of the question (it refused the reading tool on 2026-11-03).

Not legal advice; no policy text is copied whole — the points above are quoted with their date.
