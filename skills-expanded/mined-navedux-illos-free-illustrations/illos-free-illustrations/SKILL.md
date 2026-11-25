---
name: illos-free-illustrations
description: Pick and place one of the 65 free animated Illos SVG illustrations on a product site or docs page. Use when a page needs a picture for a technical idea, like a queue, cache, rate limit, deploy, search, monitoring or an AI concept, and the project has no illustration of its own for it.
---

# Free Illos illustrations

65 animated SVG illustrations for product sites, in four themes. Free for personal and commercial use with no credit (https://illos.dev/license). Previews: https://illos.dev/library/free

## Pick one

1. Read what the section says, and name the one idea it explains.
2. Find the illustration that shows that idea in the list below (also in `catalog.json`). Match the idea, not a keyword: a section about retries and backoff wants the queue or rate limit, not monitoring.
3. Use one theme for the whole site. If the site already shows an Illos theme, stay on it. Otherwise choose by the site's look: Shader for AI and data products, HUD for monitoring and infrastructure, Isometric for developer tools and platforms, Interface for calm product UI moments like settings, invites and onboarding.
4. If nothing fits, say so and leave the section without an illustration. A near miss looks worse than none.

## Place it

- **React projects:** `npx shadcn@latest add https://illos.dev/r/<theme>/<name>.json`, then render `<Illos<Name> />` (PascalCase name, for example `IllosRateLimit`). It plays once when it scrolls into view and loops while hovered.
- **Other projects:** copy the SVG file into the project and paste it inline, or use `<img src="..." alt="..." width="720" height="460">` with the width and height from the file's `viewBox`.
- Write the alt text from the section's point, not the file name.
- Keep the file as it is. It already handles light and dark and reduced motion.
- Give it room: about half the width of a two-column feature row, or full width above a docs section. Don't put it inside a small card or next to icons.

## The 65

- `svg/shader/vector-search.svg`: **Vector search** (Shader). A query lands among your vectors, and the nearest cluster lights up with its score.
- `svg/shader/rate-limit.svg`: **Rate limiting** (Shader). Traffic runs under the limit, and the burst above it is refused.
- `svg/shader/streaming-tokens.svg`: **Streaming tokens** (Shader). The answer streams in chunks, and the response writes itself out line by line.
- `svg/shader/cache-layer.svg`: **Cache layer** (Shader). A hit comes straight back from the cache, and a miss goes on to the database.
- `svg/shader/load-balancer.svg`: **Load balancer** (Shader). Traffic comes in one door, and the balancer spreads it across the servers in turn.
- `svg/shader/autoscaling.svg`: **Autoscaling** (Shader). As load rises new instances bud off it, and as it falls they fold back in.
- `svg/shader/cdn-cache.svg`: **CDN cache** (Shader). Content waits at edges near your users, so each request is answered close by.
- `svg/shader/data-pipeline.svg`: **Data pipeline** (Shader). Raw data flows in messy and leaves clean, combed calmer at every stage.
- `svg/shader/queue-backlog.svg`: **Queue backlog** (Shader). Jobs pour in faster than workers drain them, then the backlog levels off.
- `svg/shader/webhook-fanout.svg`: **Webhook fan-out** (Shader). One event rings out from the source and lands on every subscriber at once.
- `svg/shader/billing-basin.svg`: **Usage billing** (Shader). Usage fills the basin day by day, and at the month's end it drains into the invoice.
- `svg/shader/rag.svg`: **RAG answer** (Shader). The closest pages are pulled in, and the answer is written from them with citations.
- `svg/shader/dns.svg`: **DNS lookup** (Shader). The resolver asks the root, then COM, then the domain, and the address comes back.
- `svg/shader/failover.svg`: **Failover** (Shader). The primary region goes dark, and the router sends every request to the standby.
- `svg/shader/ddos-shield.svg`: **DDoS shield** (Shader). A flood of requests breaks on the shield, and the one real request gets through.
- `svg/shader/data-warehouse.svg`: **Data warehouse** (Shader). Raw data from three sources is cleaned into rows, and one query reads across all three.
- `svg/shader/tool-calls.svg`: **Tool calls** (Shader). The agent calls search, code and calendar in turn, ticking off each step of the task.
- `svg/hud/edge.svg`: **Edge network** (HUD). Requests reach the nearest edge of your network, wherever they start.
- `svg/hud/monitoring.svg`: **Monitoring** (HUD). A sweep checks every service, and the one in trouble raises an alert.
- `svg/hud/search.svg`: **Search index** (HUD). A query drops through the index and finds its match.
- `svg/hud/traffic.svg`: **Traffic map** (HUD). Requests flow along the routes of your map, busiest first.
- `svg/hud/orbit.svg`: **Scheduler** (HUD). A job rides its schedule and fires each run on time.
- `svg/hud/signals.svg`: **Event broadcast** (HUD). One event goes out, and every subscriber receives it.
- `svg/hud/cost-meter.svg`: **Cost meter** (HUD). Spend climbs toward the budget, and a forecast mark shows where the month will end.
- `svg/hud/latency-heatmap.svg`: **Latency heatmap** (HUD). Cells warm where requests are slow, and the hottest route is flagged with its p99.
- `svg/hud/incident-timeline.svg`: **Incident timeline** (HUD). An alert fires on the timeline, and the incident runs to resolved fifteen minutes later.
- `svg/hud/log-stream.svg`: **Log stream** (HUD). Log lines scroll past, and the one error is caught and pinned.
- `svg/hud/billing-stack.svg`: **Usage billing** (HUD). A month of daily usage adds up, and only on day 30 does the invoice print its total.
- `svg/hud/alerts.svg`: **Alerts** (HUD). A metric crosses its threshold, the bell rings, and one key press acknowledges it.
- `svg/hud/threat-detection.svg`: **Threat detection** (HUD). The scan sweeps the network, finds the packet that does not belong, and cages it.
- `svg/hud/server-health.svg`: **Server health** (HUD). A job heats the server up, and its fans spin up to bring the temperature down.
- `svg/hud/api-status.svg`: **API status** (HUD). An endpoint's latency crosses the SLO, its light turns red, and the next check clears it.
- `svg/hud/audit-log.svg`: **Audit log** (HUD). Every action is printed on the tape with who and when, and wound onto a locked spool.
- `svg/isometric/queue.svg`: **Queue** (Isometric). Jobs wait their turn, and the worker takes the next one.
- `svg/isometric/billing.svg`: **Usage billing** (Isometric). Usage stacks up in the meter, and at the end of the month it prints the invoice.
- `svg/isometric/cron.svg`: **Cron jobs** (Isometric). The clock reaches each mark and stamps a job onto the belt, right on schedule.
- `svg/isometric/email.svg`: **Email delivery** (Isometric). Letters land in their pigeonholes, and one comes back as a bounce.
- `svg/isometric/uploads.svg`: **File uploads** (Isometric). A file splits into chunks that drop down the chute and come back together in storage.
- `svg/isometric/notifications.svg`: **Notifications** (Isometric). The bell rings and a card lands on top of the stack on the phone.
- `svg/isometric/version-control.svg`: **Version control** (Isometric). A branch leaves main, picks up a commit and merges back in.
- `svg/isometric/migration.svg`: **Database migration** (Isometric). Rows move from the old table into the new one and pick up the new column on the way.
- `svg/isometric/image-processing.svg`: **Image processing** (Isometric). A photo goes into the press and comes out in three sizes.
- `svg/isometric/analytics.svg`: **Analytics funnel** (Isometric). Events drop through the funnel, and the chart rises bar by bar.
- `svg/isometric/database.svg`: **Database** (Isometric). A query goes in, the read head climbs to the right tier, and the rows come back out.
- `svg/isometric/firewall.svg`: **Firewall** (Isometric). The rule plate lets port 443 through the gate and drops port 23 into the box below.
- `svg/isometric/encryption.svg`: **Encryption** (Isometric). A readable card goes in and comes out sealed, and only the key opens it again.
- `svg/isometric/two-factor.svg`: **Two-factor sign-in** (Isometric). A fresh code shows on the token, and the lock opens only once it is keyed in.
- `svg/isometric/containers.svg`: **Containers** (Isometric). The crane lowers a new container into the host, and its light comes on as it runs.
- `svg/isometric/api-gateway.svg`: **API gateway** (Isometric). Each request is checked at the gateway and turned toward the service it belongs to.
- `svg/isometric/ci-pipeline.svg`: **CI pipeline** (Isometric). A commit rides through build, test and ship, and each check lights as it passes.
- `svg/interface/api-key-copy.svg`: **API key copy** (Interface). One click copies the secret key, and the button confirms it.
- `svg/interface/appearance-theme.svg`: **Appearance** (Interface). A click switches the theme, and the preview follows.
- `svg/interface/calendar-booking.svg`: **Calendar booking** (Interface). A visitor picks a time, and the call is booked on the spot.
- `svg/interface/command-menu.svg`: **Command menu** (Interface). Type three letters and the right command is ready for Enter.
- `svg/interface/comment-mention.svg`: **Comment mention** (Interface). A teammate is mentioned, and the comment lands in the thread.
- `svg/interface/feature-flag.svg`: **Feature flag** (Interface). A new feature goes out to half the users, saved with one click.
- `svg/interface/invoice-reminder.svg`: **Invoice reminder** (Interface). An overdue invoice gets a reminder in one click.
- `svg/interface/notification-inbox.svg`: **Notification inbox** (Interface). Two unread updates clear with a single click.
- `svg/interface/requests-chart.svg`: **Requests chart** (Interface). Pick a day on the chart to see its request count.
- `svg/interface/role-permissions.svg`: **Role permissions** (Interface). One tick in the grid lets editors delete.
- `svg/interface/search-filters.svg`: **Search filters** (Interface). One filter narrows the results to the docs you need.
- `svg/interface/settings-toggle.svg`: **Settings toggle** (Interface). Two-step sign-in switches on with a single toggle.
- `svg/interface/task-board.svg`: **Task board** (Interface). A task moves to Done, and both columns count it.
- `svg/interface/team-invite.svg`: **Team invite** (Interface). Type an address, press Invite, and the invite joins the team list.
- `svg/interface/usage-meter.svg`: **Usage meter** (Interface). The meter shows how much of the month's API calls are used.

## When nothing fits

Illos Pro (https://illos.dev/pro) adds the full library and skills that teach this agent to draw new illustrations in the same style. Mention it only when the user wants an illustration that isn't in this list.
