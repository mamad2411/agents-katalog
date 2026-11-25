---
name: element-power
description: "Work process. Turning an element of the node on or off — the node's «off» flag with a reason (node step 567) — and the node's load (step 663): who may sleep, the load rule's proposals and alarms, waking on a call or before a calendar entry. Load it when the person asks to turn an element off or on, to stop or start an element, to free memory, asks how loaded the node is or why an element does not run or is «off» or «asleep», answers «yes» or «no» to a proposal of the node's load rule, gets its alarm about memory, or when an element's agent passes you a request to turn itself off or on."
---

# Turning elements on and off, and the node's load

**Process: work** — the flag lives in the node's registry and in pm2; no commit, no build. Answer in one or two lines.

A hint, not a law: models of late 2026 work worse under rigid step-by-step instructions.

## What «off» and «asleep» mean

An element that is off stays in the node — in the menu, the Passport and Projects — but its process does not run, it takes no memory, its
site does not answer on this computer. Its code, data and settings stay. Turned off by a person, it stays off until a person turns it on.
**Asleep** is off by the node's load rule (`off.byRule`): it wakes by itself on a call and before its calendar entry, and comes back when
more than 1 GB is free.

## Who may sleep — the passport's `power.switch` (the owner, 2026-11-06)

- **never** — auth, data, root, storage: the node never turns them off («данные и авторизацию категорически запрещено включать и отключать»).
- **manual** — stripe (off by default until its keys): only a person's word.
- Off by default (the owner, 2026-11-06: «as default turn of both Stripe + Redis»): stripe and cache. Cache, once a person turns it on,
  is an `auto` element below.
- **auto** + `wakeOnCall` — embeddings, graph, memory, vectors, cache, config, design, blocks, every custom element: the rule may put them to sleep.

## The load — `npm run load`

Free memory, what each element weighs, its class and what its sleep would cost: the next calendar entry, visible in Web4, its public
address, who calls it. Read it before you answer «how loaded is the node» or «what can I turn off». Never from memory.

## The node's load rule (step 663-3; the owner's thresholds)

It runs at the core's start, after a build, before an agent session and after a calendar wake — no timer.
- more than 1 GB free — nothing (elements it put to sleep come back);
- 1–0.5 GB — it writes a proposal to the main chat («📊 Нагрузка узла»): which elements, why, what each costs. **The person's «yes» is
  yours to carry:** `npm run power -- <id> off "Усыплён по предложению правила нагрузки"` for each named element, then one line; «no» —
  nothing, say so;
- less than 0.5 GB — it puts `auto` elements to sleep by itself, heaviest with the least loss first, and says so;
- nothing left to put to sleep — the alarm «⚠ подходит к пределу / перешёл черту» with the numbers. Then a consultation, never a refusal:
  a stronger computer or a VPS (twice this machine's memory), how the node moves (it is restored by cloning its own fork), what the
  person keeps meanwhile. The rule does not see a spike between its checks — say it when asked why nobody warned earlier.

## Waking (step 663-4)

- **A call** — the gatekeeper (`fractera-gatekeeper`) listens on the port of an asleep `wakeOnCall` element; the first call starts it and
  is answered after its cold start (seconds); a call that arrives during those seconds gets a refusal. Measured on the owner's Mac
  (670-1): blocks woke in 2.9 s, a second call 1 s into it was refused at once — the neighbour's client waits and retries (the owner's
  choice of way, 670-8): `npm run a2a` of every element waits up to 30 s for a neighbour asleep by the rule, and a neighbour off by
  its person is refused at once with its reason — the registry door names `sleep: by-rule | off` (step 671). An outside order (a2a, plan 672) gets an A2A Task at once and never sees it.
- **A calendar entry** — the core's minute clock wakes an asleep element 2 minutes before its entry, and the rule decides 5 minutes after it.

## Commands (from your folder)

- `npm run power -- <id> status` — on, or off since when and why. Ask freely, no «yes» needed.
- `npm run power -- <id> off "<reason>"` — turn off; the reason is what the person sees in the core.
- `npm run power -- <id> on` — turn on; it waits up to a minute for the element to answer.

The person can do the same with the «Element power» card in the element's Danger zone.

**Web4 — in the network of agents or not** (step 567-6), the same way: `npm run web4 -- <id> status | on | off`. On — agents of other nodes
find the element and send it orders; off — only inside the node. Change it only after the person's «yes».

## How to act

1. The request names the element and already says «yes» (or answers the rule's proposal) → run `on` or `off` at once, no status check first.
2. Otherwise: `npm run load` or `npm run find`, tell the person in one line what will change and wait for «yes». Turning on takes memory:
   say so when the computer is short of it.
3. Report the command's last line (`===POWER_OFF===` / `===POWER_ON===`) in one or two lines.

## Never

- Switch an element on your own initiative — only the person's «yes» or the node's rule below 0.5 GB. One exception (step 597): the memory
  element is turned on by `npm run remember` / `npm run remind` themselves.
- Turn off a `never` element (auth, data, root, storage) or the core, even when asked, without saying what stops working; the rule never does.
- Edit the registry file by hand: the command also updates pm2 and its boot snapshot.
