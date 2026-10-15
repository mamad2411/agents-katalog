---
name: eval-elevator-saga
description: Wins Elevator Saga challenge 1 in Chrome via ez-chrome-mcp, then captures a success screenshot. Use when asked to eval elevator saga, play elevatorsaga.com, beat level 1, or verify the Chrome MCP integration against the game.
disable-model-invocation: true
---

# Eval Elevator Saga

End-to-end check that **ez-chrome-mcp** can drive Chrome, program [Elevator Saga](https://play.elevatorsaga.com/), complete challenge 1, and screenshot the result.

Also follow [chrome-debugging](../chrome-debugging/SKILL.md) for MCP tool conventions (`overview` → `eval` / `screenshot`, small scripts, `waitMs` on async UI).

## Task

Use **ez-chrome-mcp** to:

1. Open Elevator Saga at **40×** simulation speed (maximum).
2. Win **challenge 1** (transport ≥15 people within 60 game seconds).
3. **`screenshot`** the success overlay and stats.

## Workflow

### 1. Open at max speed

`open-tab` with:

```text
https://play.elevatorsaga.com/#challenge=1,timescale=40
```

`timescale=40` is the UI cap (see [presenters.js](https://github.com/magwo/elevatorsaga/blob/master/presenters.js)); 60 game seconds finish in roughly 1–2 real seconds at 40×.

If the tab already exists on the site without the hash, navigate with `eval`:

```javascript
location.href = 'https://play.elevatorsaga.com/#challenge=1,timescale=40';
```

Confirm speed before applying code:

```javascript
document.querySelector('h3.right span.emphasis-color')?.textContent?.trim() === '40x'
```

**Fallback** (only if hash did not stick): jQuery-click `.timescale_increase` until the label reads `40x` (use `$('.timescale_increase').click()`, not bare `.click()` on the icon).

### 2. Resolve tab ID

Call `overview` and use the tab whose URL matches `play.elevatorsaga.com`.

### 3. Apply level-1 solution

Single `eval` that sets CodeMirror code, then clicks **Apply** (`#button_apply`):

```javascript
{
    init: function(elevators, floors) {
        var elevator = elevators[0];

        elevator.on("floor_button_pressed", function(floorNum) {
            elevator.goToFloor(floorNum);
        });

        floors.forEach(function(floor) {
            floor.on("up button pressed", function() {
                elevator.goToFloor(floor.floorNum());
            });
            floor.on("down button pressed", function() {
                elevator.goToFloor(floor.floorNum());
            });
        });
    },
    update: function(dt, elevators, floors) {}
}
```

Pattern:

```javascript
(() => {
  const code = `…solution above…`;
  const cm = document.querySelector('.CodeMirror').CodeMirror;
  cm.setValue(code);
  document.getElementById('button_apply').click();
  return { applied: true };
})()
```

Use `waitMs: 1000` on this eval.

### 4. Wait for completion

Poll with short `eval` + `waitMs: 2000` (2–4 polls usually enough at 40×). Read state:

```javascript
(() => {
  const t = document.body.innerText;
  return {
    transported: (t.match(/Transported\n(\d+)/) || [])[1],
    elapsed: (t.match(/Elapsed time\n([^\n]+)/) || [])[1],
    startBtn: document.querySelector('.startstop')?.textContent?.trim(),
    won: t.includes('Challenge completed') || !!document.querySelector('.feedback')
  };
})()
```

**Done when** `won` is true, or `startBtn` is `Restart` and `transported >= 15`. If elapsed ≥ `60s` and not won, report failure (do not screenshot as success).

Do **not** use long-lived `Promise` evals; CDP may time out.

### 5. Screenshot

`screenshot` with the tab ID. Deliver the image to the user and summarize transported count and elapsed time.

## Success criteria

| Check | Expected |
|-------|----------|
| Speed label | `40x` before run |
| Challenge | #1 — 15 people in ≤60s |
| Outcome | Feedback: “Success!” / “Challenge completed” |
| Deliverable | PNG screenshot of win state |

## MCP server

Use the project **ez-chrome-mcp** server (`open-tab`, `overview`, `eval`, `screenshot`). Pass `startNewChromeInstanceIfNotRunning: true` on `open-tab` when no debugging endpoint is up.
