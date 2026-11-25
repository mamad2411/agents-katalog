---
name: qa-detect-ux-actions
section: visual
description: "Catches action-button UX problems: destructive actions without confirmation pattern, multiple competing primary CTAs (broken visual hierarchy), disabled buttons without explanation, primary button hidden below the fold. Goes beyond a11y — catches UX intent failures."
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: true
requires: [hasActionButtons, hasToolbar, hasFloatingAction]
---

## What it catches — 6 issue types

| issueType | severity | What |
|---|---|---|
| `destructiveNoConfirm` | high | Button labeled Delete/Remove/Clear/Discard/Cancel-account has no `data-confirm`, no nearby modal markup, no `onclick` that opens a confirmation. Single click = data loss. |
| `multiplePrimaryCTAs` | medium | Page has > 3 elements styled as "primary button" (same dominant color/size). Visual hierarchy broken — user can't tell which is the main action. |
| `disabledNoExplanation` | medium | `[disabled]` button has no `title`, no `aria-describedby`, no visible help text. User can't discover why it's disabled or how to enable it. |
| `primaryActionBelowFold` | medium | The page's primary CTA (Save / Submit / Continue / Buy) is positioned below the viewport fold — users may not see it without scrolling. |
| `competingDestructiveAdjacent` | high | Destructive (Delete/Remove) and confirmative (Save/OK) buttons are < 16px apart. Misclick risk. |
| `submitNoVisibleAffordance` | low | Form has fields but no visible submit button or submit-like affordance — users may not realize they can submit. |

## Probe (browser_evaluate)

```js
() => {
  const sel = el => {
    const id = el.id ? '#' + el.id : '';
    const cls = (el.className && typeof el.className === 'string')
      ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : '';
    return (el.tagName.toLowerCase() + id + cls).slice(0, 120);
  };
  const bb = el => {
    const r = el.getBoundingClientRect();
    return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) };
  };
  const visible = el => {
    if (!el || el.nodeType !== 1) return false;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') return false;
    const r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0;
  };
  const out = [];

  const DESTRUCTIVE_RE = /\b(delete|remove|clear|discard|reset|cancel\s*account|destroy|deactivate|drop|trash|wipe|terminate)\b/i;
  const CONFIRMATIVE_RE = /\b(save|submit|create|update|continue|confirm|ok|yes|apply|proceed|next|finish|publish|send|approve)\b/i;
  const PRIMARY_CTA_RE = /\b(save|submit|continue|buy|sign\s*up|register|create|start|get\s*started|proceed|add|book|order|checkout|publish|send)\b/i;

  const allBtns = [...document.querySelectorAll('button, a[href], [role="button"], input[type="submit"], input[type="button"]')].filter(visible);

  // ── 1. Destructive without confirmation ───────────────────────────────
  let destructFlagged = 0;
  for (const b of allBtns) {
    if (destructFlagged >= 6) break;
    const text = ((b.innerText || b.value || b.getAttribute('aria-label') || '') + '').trim();
    if (!DESTRUCTIVE_RE.test(text)) continue;
    // Check for confirmation indicators
    const hasConfirmAttr = b.hasAttribute('data-confirm') ||
                          b.hasAttribute('data-confirmation') ||
                          b.hasAttribute('confirm');
    const onclick = (b.getAttribute('onclick') || '').toLowerCase();
    const hasConfirmHandler = /confirm\(|swal|alert\(|dialog\.open|modalservice|matdialog/i.test(onclick);
    const ariaHasPopup = b.getAttribute('aria-haspopup') === 'dialog' ||
                        b.getAttribute('aria-haspopup') === 'true';
    if (hasConfirmAttr || hasConfirmHandler || ariaHasPopup) continue;
    // Check nearby modal markup (sibling or descendant of common container)
    const container = b.closest('form, .form, .card, tr, .item, li') || b.parentElement;
    if (container && container.querySelector('dialog, [role="dialog"], .modal, .confirmation, [class*="confirm"]')) continue;
    destructFlagged++;
    out.push({
      issueType: 'destructiveNoConfirm', severity: 'high',
      selector: sel(b), bbox: bb(b),
      description: `"${text.slice(0, 40)}" button has no visible confirmation mechanism (no data-confirm, no aria-haspopup, no onclick handler opening a dialog). Single click triggers data loss.`
    });
  }

  // ── 2. Multiple primary CTAs ──────────────────────────────────────────
  // Heuristic: count buttons whose computed background is dominant/saturated
  // AND text length is small (typical CTA shape)
  const primaryButtons = [];
  for (const b of allBtns) {
    const text = (b.innerText || b.value || '').trim();
    if (text.length < 2 || text.length > 30) continue;
    const cs = getComputedStyle(b);
    const bg = cs.backgroundColor;
    const m = bg.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?\)/);
    if (!m) continue;
    const [r, g, bC] = [+m[1], +m[2], +m[3]];
    const alpha = m[4] !== undefined ? parseFloat(m[4]) : 1;
    if (alpha < 0.5) continue;
    // Saturated color = max(r,g,b) - min(r,g,b) > 80, not white/grey
    const max = Math.max(r, g, bC), min = Math.min(r, g, bC);
    if (max < 80 || max - min < 60) continue;   // grey-ish, not primary CTA
    primaryButtons.push({ btn: b, text });
  }
  if (primaryButtons.length > 3) {
    const sample = primaryButtons.slice(0, 5).map(p => `"${p.text.slice(0, 20)}"`).join(', ');
    out.push({
      issueType: 'multiplePrimaryCTAs', severity: 'medium', selector: 'body',
      description: `${primaryButtons.length} buttons styled as primary CTA on screen: ${sample}. Visual hierarchy broken — users can't identify the main action.`
    });
  }

  // ── 3. Disabled button without explanation ────────────────────────────
  // Helper: is this disabled button STRUCTURALLY disabled by context (boundary case)?
  // If yes, no tooltip is required — the surrounding UI tells the user why.
  const isStructurallyDisabled = (b) => {
    const ariaLabel = (b.getAttribute('aria-label') || '').toLowerCase();
    const btnText = (b.innerText || b.value || '').trim();
    // (a) Pagination Next/Prev/First/Last at the boundary
    const paginationContainer = b.closest(
      '.pagination, .pager, [class*="pagination"], [class*="paginator"], [class*="Pagination"], ' +
      '[role="navigation"][aria-label*="page" i], [aria-label*="pagination" i]'
    );
    const looksLikePagerArrow = /^[‹›«»<>‍]\s*$|next|prev|previous|first|last|page/.test(ariaLabel) ||
                                /^[‹›«»<>]$/.test(btnText) ||
                                (btnText.length <= 2 && /[‹›«»<>]/.test(btnText));
    if (paginationContainer || looksLikePagerArrow) {
      // Look in the page for a "Showing 1-N of N" / "Page 1 of 1" / "1 of 1" hint
      // that indicates we're at a pagination boundary (single page or last page)
      const wrap = paginationContainer ? paginationContainer.parentElement : (b.closest('.card, [class*="card"], [class*="table"], main, [role="main"]') || document.body);
      const ctx = (wrap && wrap.innerText) ? wrap.innerText.toLowerCase() : '';
      // "Showing 1-2 of 2", "1-30 of 2", "page 1 of 1", "showing all"
      const boundaryHint = /(?:showing\s+)?(\d+)\s*[\-–to]+\s*(\d+)\s+of\s+(\d+)/i.exec(ctx) ||
                           /page\s+(\d+)\s+of\s+(\d+)/i.exec(ctx);
      if (boundaryHint) {
        // Pattern 1: "1-2 of 2" → end == total → last page (Next disabled correctly)
        if (boundaryHint.length >= 4) {
          const end = +boundaryHint[2], total = +boundaryHint[3];
          if (end >= total) return true; // on last page; Next is correctly disabled
          const start = +boundaryHint[1];
          if (start === 1 && /prev|previous|first|‹|«|</.test(ariaLabel + btnText)) return true; // on first page; Prev disabled
        }
        // Pattern 2: "page 1 of 1" → single page; both arrows correctly disabled
        if (boundaryHint.length === 3 && +boundaryHint[1] === +boundaryHint[2]) return true;
      }
      // "Showing all" / "no more results" — single-page indicator
      if (/showing\s+all|no\s+more\s+(records|results|pages)/i.test(ctx)) return true;
    }
    // (b) Bulk-action buttons (Delete Selected, Archive Selected) disabled when no row is checked
    if (/delete\s+selected|archive\s+selected|export\s+selected|bulk\s+\w+/i.test(btnText + ' ' + ariaLabel)) {
      const tableScope = b.closest('main, [role="main"], .card, [class*="card"]') || document.body;
      const anyChecked = tableScope.querySelector('tbody input[type="checkbox"]:checked, [role="row"] input[type="checkbox"]:checked, [aria-selected="true"]');
      if (!anyChecked) return true; // nothing selected → correctly disabled
    }
    return false;
  };

  let disabledFlagged = 0;
  const disabledBtns = [...document.querySelectorAll('button[disabled], button[aria-disabled="true"], input[disabled][type="submit"], input[disabled][type="button"], [role="button"][aria-disabled="true"]')];
  for (const b of disabledBtns) {
    if (disabledFlagged >= 4) break;
    if (!visible(b)) continue;
    const title = (b.getAttribute('title') || '').trim();
    const ariaDescribedBy = b.getAttribute('aria-describedby');
    const hasHelpRef = ariaDescribedBy && document.getElementById(ariaDescribedBy);
    if (title.length > 3 || hasHelpRef) continue;
    // Check for visible help text nearby
    const container = b.closest('.form-group, .field, fieldset, .input-group') || b.parentElement;
    const hasHelp = container && container.querySelector('.help, .help-text, .hint, [class*="help-text"], .form-text');
    if (hasHelp) continue;
    // Skip structurally-disabled controls (pagination at boundary, bulk actions with no selection)
    if (isStructurallyDisabled(b)) continue;
    disabledFlagged++;
    const text = (b.innerText || b.value || '').trim().slice(0, 40);
    out.push({
      issueType: 'disabledNoExplanation', severity: 'medium',
      selector: sel(b), bbox: bb(b),
      description: `Disabled "${text}" button has no title, no aria-describedby, no visible help text. Users can't tell why it's disabled.`
    });
  }

  // ── 4. Primary action below fold ──────────────────────────────────────
  const vpH = window.innerHeight;
  let belowFoldFlagged = 0;
  for (const b of allBtns) {
    if (belowFoldFlagged >= 1) break;
    const text = (b.innerText || b.value || '').trim();
    if (!PRIMARY_CTA_RE.test(text)) continue;
    const r = b.getBoundingClientRect();
    if (r.top > vpH) {
      belowFoldFlagged++;
      out.push({
        issueType: 'primaryActionBelowFold', severity: 'medium',
        selector: sel(b), bbox: { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) },
        description: `Primary CTA "${text.slice(0, 30)}" at y=${r.top.toFixed(0)}px is below viewport fold (vh=${vpH}px). Users must scroll to find it.`
      });
    }
  }

  // ── 5. Destructive + confirmative adjacent ────────────────────────────
  let adjacentFlagged = 0;
  for (let i = 0; i < allBtns.length && adjacentFlagged < 2; i++) {
    const a = allBtns[i];
    const aText = (a.innerText || a.value || '').trim();
    if (!DESTRUCTIVE_RE.test(aText)) continue;
    const ar = a.getBoundingClientRect();
    for (let j = 0; j < allBtns.length; j++) {
      if (j === i) continue;
      const b = allBtns[j];
      const bText = (b.innerText || b.value || '').trim();
      if (!CONFIRMATIVE_RE.test(bText)) continue;
      const br = b.getBoundingClientRect();
      // Same row (top within 12px) and < 16px apart horizontally
      if (Math.abs(ar.top - br.top) < 12) {
        const hGap = Math.abs(ar.right - br.left) < Math.abs(br.right - ar.left)
          ? Math.abs(ar.right - br.left) : Math.abs(br.right - ar.left);
        if (hGap < 16) {
          adjacentFlagged++;
          out.push({
            issueType: 'competingDestructiveAdjacent', severity: 'high',
            selector: sel(a), bbox: bb(a),
            description: `Destructive "${aText.slice(0, 20)}" and confirmative "${bText.slice(0, 20)}" buttons are ${hGap.toFixed(0)}px apart. Misclick will lose data — increase gap or move destructive to secondary location.`
          });
          break;
        }
      }
    }
  }

  // ── 6. Form with no visible submit button ─────────────────────────────
  let noSubmitFlagged = 0;
  const forms = [...document.querySelectorAll('form')].filter(visible);
  for (const f of forms) {
    if (noSubmitFlagged >= 2) break;
    const fields = f.querySelectorAll('input:not([type="hidden"]):not([type="submit"]):not([type="button"]), select, textarea');
    if (fields.length < 2) continue;   // not a real form
    const submitLike = f.querySelector('button[type="submit"], input[type="submit"], button:not([type]), [role="button"]');
    if (!submitLike) {
      // Maybe there's a button outside the form via form="ID"
      const formId = f.id;
      const externalSubmit = formId ? document.querySelector(`button[form="${formId}"], input[form="${formId}"][type="submit"]`) : null;
      if (!externalSubmit) {
        noSubmitFlagged++;
        out.push({
          issueType: 'submitNoVisibleAffordance', severity: 'low',
          selector: sel(f), bbox: bb(f),
          description: `Form with ${fields.length} fields has no visible submit button (and no external button[form=${formId}]). Users may not realize how to submit.`
        });
      }
    }
  }

  return out;
}
```

## Notes

- Self-skips: page with no buttons returns []
- Bounded: 6 destructive + 1 primary count + 4 disabled + 1 below-fold + 2 adjacent + 2 no-submit = max ~16 findings
- Viewport-sensitive: `primaryActionBelowFold` finds different bugs at different viewport heights
