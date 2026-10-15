---
name: real-agent-browser-esky
description: Use when Codex needs to search eSky, compare eSky flight results, inspect eSky flight options, or preserve eSky state through the user's real Chrome profile without launching Chrome for Testing or an agent-browser-managed browser.
---

# Real Agent Browser eSky

## Overview

Use this skill only after `$real-agent-browser` has launched or attached to the user's real Chrome profile. Keep eSky work in that real browser over CDP, with the default agent-browser session and explicit CDP port.

## Required Browser Path

1. Use `$real-agent-browser` first.
2. Confirm real stable Chrome or Chrome Beta is running with the expected profile and CDP port.
3. Attach with `agent-browser --debug --cdp <port>`.
4. Do not use `--session`, `--session-name`, or `AGENT_BROWSER_SESSION`.
5. Do not run `agent-browser open`, `agent-browser --profile`, Playwright, Puppeteer, or Chrome for Testing.

## User Defaults

Ask only for values not covered by defaults, but always tell the user these defaults can be overridden:

- Trip type: round trip.
- Cabin: economy.
- Stops: direct flights only.
- Nearby airports: off by choosing exact airports when possible.
- Hotels: off.
- Extra filters: none unless the user asks.

Ask for origin, destination, dates, and travelers unless already provided. Say the defaults before searching, for example: "I will use round trip, economy, direct only, exact airports, no hotel search, and no extra filters unless you want to override any of those."

## Site State

- If a cookie banner appears, accept all cookies.
- Check login state from the header/account UI. On eSky, `My account` can open a login modal with email/password fields when the user is not logged in.
- If the user is not logged in or the state is unclear, ask whether they want to log in manually. If they choose login, wait until the user says `OK` after finishing. Do not automate credentials and do not re-check or second-guess the login after `OK`; login is the user's choice. If they decline, continue as guest.
- If eSky presents CAPTCHA or an access challenge, stop and ask the user to solve it manually. Do not bypass or automate the challenge.

## Search Flow

- Navigate in the existing real Chrome tab or create a CDP tab; do not use `agent-browser open`.
- Use `https://www.esky.com` by default. Use another eSky locale only when the user explicitly asks for it or when testing language/locale behavior.
- eSky can default the origin from location, so always verify and clear the origin field before entering a requested airport.
- Prefer exact airport-code choices over city, country, or region choices when possible.
- The home form does not expose direct-only. Submit first, then apply `Stops -> Direct` on the results page.
- Before submitting, verify origin, destination, dates, travelers, cabin, and hotel state.

## Flight Log

Before reporting flight search results, update `$HOME/flights.log`.

Use this plain text row format under each destination block:

```text
| PATH | DATES | PRICE | INFO | SOURCE |
| ORIGIN ⇄ DEST | YYYY-MM-DD → YYYY-MM-DD | 1234 zł | przesiadka 1x | esky |
```

Rules:

- Read the existing file first and preserve rows from other sources and destinations.
- Use `DIRECT` in `INFO` when there is no layover or no-result note.
- Use `-` in `PRICE` when there is no flight price, with the reason in `INFO`.
- Use `esky` as `SOURCE`.
- Keep separate rows for direct and non-direct options on the same route/date.
- If a matching row already exists for the same `PATH`, `DATES`, `INFO`, and `SOURCE`, replace its price with the newest observed price.
- Group new rows under the matching destination section; create a section only when needed.

## Fast Results Extraction

When origin, destination, dates, cabin, and passenger count are already known, use the eSky results URL directly in the existing real Chrome tab. Default domain is `www.esky.com`; swap only the domain, not the path/query shape, when the user explicitly asks for another eSky locale:

```text
https://www.esky.com/flights/search/ap/ORIGIN/ap/DEST?pa=2&sc=economy&departureDate=YYYY-MM-DD&returnDate=YYYY-MM-DD
```

Then wait for cards to load and extract from DOM. Do not use Playwright/Puppeteer; use `agent-browser --debug --cdp <port> eval ...`.

Loading guard:

- Never read results immediately after navigation or when the progress/scanning bar just finished.
- Wait until either priced flight cards or an explicit no-results state is visible.
- Confirm the page is no longer actively loading. Prefer stable DOM signals over text: priced card count/result count is stable and progress-bar/icon positions are unchanged. Some eSky locale pages can leave loader/progress elements and scanning text in the DOM after results are visible, so do not treat their mere presence as active loading.
- After the page first looks loaded, wait at least 3 more seconds, then re-check that the same loaded/no-results state is still present and progress positions/card counts are unchanged before extracting.
- If a route temporarily has zero cards but no explicit no-results message, keep waiting or report the route as inconclusive; do not log it as no flights.
- Localized eSky pages may leave loading/scanning text in the DOM after results are visible; use stable cards/no-results, not text alone.

Observed card selector:

```js
document.querySelectorAll("so-fsr-flight-card.clickable")
```

Parsing rules:

- Ignore loading/scanning placeholders until priced flight cards or explicit no-results are stable.
- Price appears as `NNN zł`, `NNN USD`, `N,NNN USD`, or localized variants. On eSky.com, expect USD unless the site/user locale changes currency. Localized eSky sites may show local currency. It is usually the price for 2 passengers round trip when `pa=2`.
- Round-trip direct means the card contains exactly two direct-flight labels: `Direct flight` or `Lot bezpośredni`.
- One direct leg plus one `1 stop` / `1 przesiadka` leg is not a direct round trip.
- For layover markers, sum visible stop labels across outbound and return: `1 stop` / `1 przesiadka` = 1, `2 stops` / `2 przesiadki` = 2. Report `przesiadka xN` when `N > 0`.
- If eSky exposes only stop counts and not layover airport names, report only the count; do not invent layover cities.
- Keep both the direct round-trip price and the cheapest non-direct price when both are useful for comparison.
- If collected results use more than one currency, ask the user whether to normalize currencies. The user must choose the target currency and provide the exchange rate, for example `1 SOURCE = RATE TARGET`. Do not infer or fetch a rate unless explicitly asked.
- If the user provides a rate, convert with normal rounding, for example `Math.round(sourceAmount * rate)`.

Guardrails:

- Check card text for `Nearby airports` and airport codes. eSky can show nearby-airport cards even when the URL asks for an exact airport. Reject or clearly flag any card whose visible origin, return origin, destination, or return destination airport code differs from the requested exact airport unless the user explicitly allows nearby airports.
- If no cards with prices load, report no observed eSky result for that route/date instead of guessing.
- If the page shows CAPTCHA/access challenge, stop and ask the user to solve it manually.

Reusable extraction shape:

```js
(() => {
  const cards = [...document.querySelectorAll("so-fsr-flight-card.clickable")]
    .map((card) => {
      const text = card.innerText.replace(/\s+/g, " ").trim();
      const priceMatch = text.match(/(\d[\d\s\u00a0.,]*)\s*(zł|USD)/);
      if (!priceMatch) return null;
      const direct = (text.match(/Direct flight|Lot bezpośredni/g) || []).length;
      const stops = [...text.matchAll(/(\d+)\s*(?:stops?|przesiad\w*)/g)]
        .reduce((sum, match) => sum + Number(match[1]), 0);
      return {
        price: Number(priceMatch[1].replace(/[\s\u00a0.]/g, "").replace(",", ".")),
        currency: priceMatch[2],
        direct,
        stops,
        text,
      };
    })
    .filter(Boolean)
    .sort((a, b) => a.price - b.price);

  return {
    direct: cards.find((card) => card.direct === 2) || null,
    nonDirect: cards.find((card) => card.direct !== 2) || null,
    top: cards.slice(0, 5),
  };
})()
```

## Date Picker Notes

- The eSky date picker may expose only month-level text in accessibility snapshots.
- Use the visible calendar's next-month arrow to move from June/July 2026 to August/September 2026 for September dates.
- If individual day cells are not exposed as refs, locate visible calendar day cells in DOM and click the center of the target day with pointer/mouse events.
- Confirm dates from input values after selection, e.g. `dates_from = 16 Sep 2026`, `dates_to = 30 Sep 2026`.

## Direct-Only Filter

Observed direct-only filter shape:

```text
&filters=%7B%22Transfers%22:%5B%22None%22%5D%7D
```

Report prices with "observed now" wording and remind the user that eSky availability and prices can change.
