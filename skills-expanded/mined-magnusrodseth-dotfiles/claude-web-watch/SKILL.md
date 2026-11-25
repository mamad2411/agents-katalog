---
name: claude-web-watch
description: Creates a web watch, a cloud routine that checks a web page and emails Magnus on a hit (stock, price limit, new listing, changed text). Use for "monitor X", "si fra når", "varsle meg når" or "overvåk".
---

# Web watch

A **watch** is a cloud routine (RemoteTrigger) that runs without the Mac. It stays **silent until the condition is met**, and it **fails loud**: a broken check sends an email too, so silence always means "checked, no hit". The Hetzner CX alert (`trig_01L29PrV8FDszYVQSZK962Vt`) is the reference watch.

Never build a watch as a T3 or local scheduled task. Magnus needs it to run with the Mac off.

## Steps

1. **Pin down the watch.** You need five facts. Ask once for the ones the request leaves open:
   - **Target:** the URL(s) to check.
   - **Condition:** a checkable rule, such as "size L can be added to cart", "price ≤ 600 kr", or "a new listing under 3 M kr in Torshov". "A good deal" is not a condition until you have a threshold.
   - **Cadence:** how often. Twice a day for stock, daily for prices, weekly for slow-moving things.
   - **End:** pause after the first hit, or on a set date.
   - **Report:** alert only, or also a weekly status. The default is alert only.
   Done when you can phrase the condition as a yes/no question about the page text.

2. **Probe the page from here** before writing any prompt. Use `curl -sL -A 'Mozilla/5.0' -w '%{http_code}'` first. If the content is rendered by JavaScript, use headless `agent-browser`. Find the exact **markers** for both states: the text or class that marks "hit" and the one that marks "no hit". Done when you have quoted both markers from the real page. If you can only find one, the watch cannot tell "no hit" from "page changed", so keep looking.
   - A Cloudflare page ("Just a moment..."), a captcha or a login wall means the cloud cannot read the page. Stop, and offer the alternatives in [REFERENCE.md](REFERENCE.md#when-the-page-cannot-be-read).
   - The cloud runs from a datacenter IP. A page that loads here can still block there, and step 5 settles that.

3. **Check for an existing watch** with `RemoteTrigger list`. Extend a matching watch instead of creating a second one.

4. **Write the routine** from [TEMPLATE.md](TEMPLATE.md). Fill in the target, both markers, the condition and the email texts. Choose the model, cron and tools as described in [REFERENCE.md](REFERENCE.md#create-body). Create it with `RemoteTrigger create`.

5. **Run it once** with `RemoteTrigger run`, then follow the run with `get_run_log` until a `result:` line appears. Done when the log shows that the run found the markers and reached the verdict that matches the page today. A run that guessed, or that emailed for a false hit, is a failure: fix the prompt, `update`, and run it again.

6. **Report to Magnus:** the watch name, the condition, when it runs in Oslo time, the next run, the claude.ai routine link, what the test run found, and how the watch ends. If it emailed during the test, say so.

## Rules every watch prompt carries

- Read-only. It must not edit, commit or push in the repo, log in anywhere, buy anything or add to a cart.
- One email per hit, sent with the Gmail connector's `send_message` to Magnus's own address (the account the Gmail connector is signed in as; copy it from an existing watch's prompt). Magnus approved emails to himself for watches. Watches never use Slack.
- Never get past a captcha or bot check. Report it as a failure.
- Never guess. A missing marker means the check failed, so it sends the failure email.
- Write emails in Norwegian bokmål with correct æ, ø and å, with no em dashes.
