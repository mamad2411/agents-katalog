# Toast Notification System — CC Prompt

## What
Add floating toast notifications for PLAYER captures only. Points scored, combo quality, sweeps, and score milestones. Lightweight: ~50 lines JS, ~40 lines CSS, ~15 lines wired into main.js.

## Files
- **NEW:** `js/toastManager.js`
- **EDIT:** `css/styles.css` — append toast styles after line 1806
- **EDIT:** `game.html` — add 1 script tag between lines 243-249
- **EDIT:** `js/main.js` — ~15 lines in `handleSubmit()`, 1 line in `initGame()` ⚠️ DANGEROUS

---

## Step 1: Create `js/toastManager.js` (NEW FILE)

```javascript
// Toast notification system — player captures only
// Exposes: window.showToast(message, type) and window.resetToastMilestones()

(function() {
  let activeToasts = 0;

  window.showToast = function(message, type) {
    type = type || 'points';
    var container = document.querySelector('.game-area');
    if (!container) return;

    var toast = document.createElement('div');
    toast.className = 'toast-notification toast-' + type;
    toast.textContent = message;

    // Stack multiple toasts — each one offset upward
    var offset = activeToasts * 34;
    toast.style.top = 'calc(45% - ' + offset + 'px)';
    activeToasts++;

    container.appendChild(toast);

    toast.addEventListener('animationend', function() {
      toast.remove();
      activeToasts = Math.max(0, activeToasts - 1);
    });
  };

  // Milestone tracking — reset per game
  window._toastMilestones = {};

  window.resetToastMilestones = function() {
    window._toastMilestones = {};
  };
})();
```

---

## Step 2: Append toast CSS to `css/styles.css`

Add AFTER line 1806 (end of file, after the portrait orientation media query):

```css
/* =============================================
   SECTION: TOAST NOTIFICATIONS
   ============================================= */
.toast-notification {
  position: absolute;
  left: 50%;
  top: 45%;
  transform: translateX(-50%);
  z-index: 100;
  pointer-events: none;
  font-family: var(--font-display);
  font-weight: 900;
  letter-spacing: 1px;
  text-align: center;
  white-space: nowrap;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.7);
  animation: toast-float 1.8s ease-out forwards;
}

.toast-points {
  font-size: clamp(16px, 3vw, 22px);
  color: var(--gold-bright);
}

.toast-combo {
  font-size: clamp(18px, 3.5vw, 26px);
  color: #FF6B35;
}

.toast-sweep {
  font-size: clamp(22px, 4vw, 30px);
  color: #FF4444;
}

.toast-milestone {
  font-size: clamp(17px, 3vw, 24px);
  color: var(--gold-bright);
}

@keyframes toast-float {
  0%   { opacity: 0; transform: translateX(-50%) translateY(0); }
  8%   { opacity: 1; transform: translateX(-50%) translateY(0); }
  65%  { opacity: 1; transform: translateX(-50%) translateY(-20px); }
  100% { opacity: 0; transform: translateX(-50%) translateY(-40px); }
}
```

**Note:** `.game-area` already has `position: relative` (styles.css line 873) — no change needed. The `clamp()` values handle mobile scaling, so no breakpoint overrides needed.

---

## Step 3: Add script tag to `game.html`

Insert between `ui.js` (line 243) and `main.js` (line 249). There's an empty `<!-- Hint System -->` comment at line 245 — put it right after that:

```html
  <!-- Toast Notifications -->
  <script src="js/toastManager.js"></script>
```

---

## Step 4: Wire triggers in `js/main.js` ⚠️ DANGEROUS FILE

### 4a. Milestone reset in `initGame()` 

Find `initGame()` (around line 294). Add this AFTER the `initGameSystems()` call (around line 299):

```javascript
  // Reset toast milestones for new game
  if (typeof resetToastMilestones === 'function') {
    resetToastMilestones();
  }
```

### 4b. Toast triggers in `handleSubmit()`

Find `handleSubmit()` (around line 372). The insertion point is AFTER this existing block:

```javascript
  const points = game.calculateScore(allCapturedCards);    // ~line 438
  showLastCapture('Player', allCapturedCards, points);     // ~line 439
  window.messageController.handleGameEvent('CAPTURE_SUCCESS', {  // ~line 440
    points: points,                                         // ~line 441
    cardsCount: allCapturedCards.length                     // ~line 442
  });                                                       // ~line 443
```

Insert AFTER line 443, BEFORE the combination reset at line 445 (`game.state.combination = ...`):

```javascript
  // === TOAST NOTIFICATIONS ===
  if (typeof showToast === 'function') {
    // Points toast — always show
    showToast('+' + points + ' pts', 'points');

    // Combo quality — validCaptures counts filled combo areas (sum1/sum2/sum3/match)
    if (validCaptures.length >= 3) {
      showToast('HUGE combo!', 'combo');
    } else if (validCaptures.length >= 2) {
      showToast('Nice combo!', 'combo');
    }

    // Sweep — board empty after capture
    if (game.state.board.length === 0) {
      showToast('SWEEP!', 'sweep');
    }

    // Score milestones (player = index 0)
    // IMPORTANT: Verify game.state.overallScores[0] is updated AFTER
    // game.executeCapture() (line 429). If not, use game.state.scores[0] instead.
    // Check game.js to confirm which property holds the running total.
    var playerScore = game.state.overallScores[0];
    if (playerScore >= 150 && !window._toastMilestones.half) {
      showToast('Halfway there!', 'milestone');
      window._toastMilestones.half = true;
    }
    if (playerScore >= 250 && !window._toastMilestones.almost) {
      showToast('Almost there!', 'milestone');
      window._toastMilestones.almost = true;
    }
  }
```

**VERIFY before committing:** Open `game.js` and check `executeCapture()`. Confirm it calls `addScore()` and/or `addOverallScore()` so that `game.state.overallScores[0]` reflects the updated total by the time our toast code runs. If scores are stored differently (e.g. `game.state.scores[0]`), adjust the property name. The target score is 300 so milestones at 150 and 250 are correct.

---

## DO NOT TOUCH
- `aiTurn()` — no toasts for bots, ever
- `game.js` / `gameStateManager.js` — don't change scoring or flow
- Combo builder / drag-drop systems
- Any existing UI rendering or layout

## TEST
1. Basic capture → "+X pts" floats up from center of play area, fades out
2. Two combo areas filled → "+X pts" AND "Nice combo!" appear stacked
3. Three combo areas → "HUGE combo!" instead of "Nice combo!"
4. Capture clears the board → "SWEEP!" appears
5. Cross 150 overall → "Halfway there!" once per game
6. Cross 250 overall → "Almost there!" once per game
7. New game → milestones can trigger again
8. Bot captures → NO toasts
9. Multiple toasts simultaneously → stacked vertically, no overlap
