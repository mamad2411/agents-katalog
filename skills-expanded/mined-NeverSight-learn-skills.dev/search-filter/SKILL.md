---
name: search-filter
description: "Use when building search and filtering: query input, facets and chips, result ranking display, zero results, async states, and keyboard control."
---


# Search and Filtering

Search is a conversation the user is losing by default: they type an approximation of what they want, and the interface either narrows toward it or leaves them guessing why it did not. Default posture: keep the query state fully visible and fully reversible, keep the input under the user's fingers no matter what the results do, and treat zero results as a recovery surface rather than an ending. Filtering destroys information, so every applied filter must be visible where it can be removed — most "your search is broken" reports are an invisible filter still doing its job.

The boundary with the sibling that looks like this one: **the grid, its columns, and its row density are `dense-ui`; the query, the facets, and how results are presented are here.** Two more handoffs: `ui-states` owns the anatomy and thresholds of loading, empty, and error surfaces — this skill only decides which of the three an outcome is — and `navigation` owns the URL-as-state contract filter state obeys.

**Use the query and combobox layers the project already has.** Check how URL state is managed (`URLSearchParams`, the router's search params, `nuqs`, a loader), how server state is fetched and cancelled (TanStack Query, SWR, a wrapper with `AbortController`), and which combobox primitive is installed (Radix, Headless UI, `cmdk`, Downshift). A hand-rolled listbox beside an installed one is two keyboard contracts to maintain, and one will be wrong.

## Quick Reference

| Open it when | File |
| --- | --- |
| You know the surface — command palette, faceted catalog, table filter bar, log search, typeahead — and need its recipe for trigger, filter surface, URL keys, zero-result recovery, and keyboard map | [patterns.md](references/patterns.md) |

## Decision: instant or submitted?

| Condition | Behavior |
| --- | --- |
| Filtering an already-loaded set, no network | Instant, no debounce |
| Small corpus, cheap query, results are a scannable list | Instant, debounced `300ms` |
| Expensive query, paginated corpus, or a compound query | Submitted on Enter or a button |
| A result set the user commits to and shares | Submitted, and the query lands in the URL |

Instant costs certainty: the user never learns when the query was finished. When it is ambiguous, ship submitted — someone who pressed Enter knows what they asked for.

## Core Principles

1. **Debounce reduces requests; only versioning fixes races.** A debounce still permits two requests in flight, and the slower one can land last and paint results for a query already replaced. Tag each request with a monotonic sequence number, or abort the previous one, and discard any response that is not newest. Debounce network queries at `300ms`. *Exception:* a synchronous local filter has no race, and a sequence number there is ceremony.

2. **The input never loses focus and the caret never moves.** Every result update leaves the field mounted, the caret where the user put it, and the scroll where it was; re-mounting the field per render is why search boxes drop characters. *Exception:* submitting a full-page search may move focus to the results heading — that is a navigation, and `a11y` requires it be announced.

3. **Every applied filter is visible where it can be removed.** A filter collapsed behind a panel is indistinguishable from a broken backend. Render a chip row above the results, one chip per applied value with an `×`, plus `Clear all` when more than one is applied. *Exception:* a single-control filter whose control already displays its value — the chip would duplicate the dropdown.

4. **Facets choose; chips confirm.** Not alternatives: the panel is where a value is picked, the chip row is where the user sees what is narrowing their world and undoes it in one tap. Facets alone hide state; chips alone hide what is filterable. *Exception:* the panel may collapse on narrow viewports — the chip row never may.

5. **Zero-count facet options are disabled, not hidden.** Hiding reflows the option list on every query, so the option someone is reaching for moves out from under the cursor. Show it with a `0` and disable it. *Exception:* a long-tail facet is a length problem, not a zero problem — sort by count and truncate behind "Show all".

6. **OR within a facet, AND across facets.** Two statuses means either status; a status and an owner means both. Users have been trained on this, and violating it silently produces counts nobody can explain. *Exception:* a single-select facet (one date range) is neither, and renders as a radio group so it does not look multi-select.

7. **The URL is the filter state.** If query, facets, and sort are not in the URL, the result set cannot be shared, bookmarked, restored by Back, or reproduced in a bug report. Serialize them as search params and read them as the source of truth on load. *Exception:* transient UI state — which panel is expanded, whether the palette is open — stays out.

8. **Three empty outcomes, three surfaces.** *Idle* (no query yet), *zero results* (ran, matched nothing), and *failed* (did not run) need different words and actions; collapsing them tells a user with a network error to try different search terms. `ui-states` owns each surface's anatomy. *Exception:* an idle state showing recent or popular items is not empty at all — prefer that to a prompt.

9. **Zero results is a recovery surface.** It carries three things: the query as the system interpreted it, every active filter with one-tap removal, and the nearest non-empty alternative — the same query minus the most restrictive filter, or a correction with its count attached (`Did you mean invoices (34)`). A bare "No results found" ends the session; `ui-copy` owns the wording. *Exception:* a genuinely empty corpus is an onboarding moment, and `onboarding` owns it.

10. **Show why a result matched.** Highlight the matched substring so the user can see the system's interpretation and correct the query instead of guessing. Never print a numeric relevance score — it invites a ranking debate no interface wins. *Exception:* exact-match ID lookup, where the whole string matched and highlighting is noise.

11. **Ranking and sorting are mutually exclusive, and the active one is stated.** Choosing a sort discards relevance. Label the current order in the results header (`Sorted by newest` / `Most relevant`) so a surprising order is explicable. *Exception:* a stable secondary key under relevance, which keeps ties from shuffling between renders and is not announced.

12. **The keyboard contract is fixed.** `/` or `⌘K` focuses the input; `ArrowUp`/`ArrowDown` move a highlight via `aria-activedescendant` while DOM focus stays in the input; `Enter` opens the highlight; `Escape` clears the highlight, then the query, then closes; `Tab` leaves the widget rather than cycling results. `a11y` owns the roles and the result-count announcement. *Exception:* a full-page search whose results are ordinary links — arrows scroll and Tab is the correct traversal.

13. **The search input is not a form field.** No validation, no error state, no required marker — an unparseable query is a zero-result state, not invalid input, and `forms` owns real fields. *Exception:* a structured query syntax may show an inline hint, and still never blocks submission.

## Smell / Fix

| Smell | Fix |
| --- | --- |
| A request per keystroke | Debounce `300ms` *and* version the requests |
| Results flicker back to an older query | Discard responses that are not the newest |
| Input loses focus when results arrive | Keep the field mounted; never key it on results |
| Zero results while a filter sits three panels deep | Chip row above results, every chip removable |
| Facet options vanishing between queries | Disable zero-count options in place |
| Refresh loses every filter | Serialize filter state into the URL |
| "No results" shown for a failed request | Split idle / zero / error into three surfaces |
| Zero-result screen with no way forward | Query echo + filter removal + nearest alternative |
| Relevance score printed beside each result | Highlight the match instead |
| Result list animating on every keystroke | Keyboard-initiated changes never animate (`motion`) |
| `Escape` closing the whole palette on first press | Clear highlight, then query, then close |

## Output: the search contract

Before building, emit the contract and get it agreed:

```
Corpus:    Invoices (server, paginated)
Mode:      Submitted on Enter; facets apply instantly
Debounce:  300ms on typeahead suggestions only
Requests:  AbortController per keystroke; stale responses discarded
URL keys:  ?q=&status=&owner=&from=&to=&sort=
Filters:   status (multi, OR), owner (multi, OR), date range (single)
Idle:      10 most recent invoices
Zero:      Query echo + active chips + "drop the date filter" alternative
Error:     Retry action, filters preserved
Keyboard:  / focus · ↑↓ highlight · Enter open · Esc clear→close
```

## Checklist

- [ ] Instant vs submitted chosen from query cost, not habit
- [ ] Network queries debounced at `300ms` **and** race-guarded by version or abort
- [ ] Input keeps focus and caret through every result update
- [ ] Every applied filter visible as a removable chip, with `Clear all`
- [ ] Facets choose, chips confirm; the chip row never collapses
- [ ] Zero-count facet options disabled in place; OR within a facet, AND across facets
- [ ] Query, facets, and sort in the URL; reload reproduces the result set
- [ ] Idle, zero-result, and error are three distinct surfaces
- [ ] Zero results echoes the query, exposes filters, offers the nearest alternative
- [ ] Matched substrings highlighted; no relevance scores; active ordering labeled
- [ ] Keyboard contract complete, including two-step `Escape`
