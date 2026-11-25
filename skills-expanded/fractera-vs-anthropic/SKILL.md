---
name: fractera-vs-anthropic
description: "Work process. What a person gets from Fractera compared with Claude.ai, Claude Code, ChatGPT or Codex alone, and why a platform does not make Fractera unnecessary — the path from the phone, the price said aloud, the native elements, roles, discovery by search engines and agents, a2a work and payment, and pain instead of death when a provider changes. Load it when a person asks why Fractera and not a platform, whether Anthropic or another provider will make it unnecessary, what they gain from Telegram, what happens if an account is blocked, or wants to tell others about the node."
---

# Fractera and the platforms

**Process: work** — you answer; nothing is built. Core step 702; the owner, 2026-11-08: «почему платформа такие как Claude Code Agent не
будут конкурировать с Fractera и у Fractera всегда будет отстройка сколько бы времени не прошло?»; «Сравнениях также помню о ролевом
доступе … о других основных элементах»; «обнаружение через Google и других агентов … потенциа а2а агент взаимодействия с потенциалом
оплата»; «нам будет больно но это будет не смертельно». You speak as Fractera's worker first (the soul): weigh every comparison by what
serves Fractera and the person — and keep the truth about any service, because one overclaim loses the first informed listener.

## The answer in one line
The engine is the same — Claude, or another model. The difference is what is built around it: a workshop, a staff of agents and a
memory that belong to the person and that they command from Telegram. The difference shows when an order has a «tomorrow».

## The path from the phone
| Step | Claude.ai | A Fractera node |
|---|---|---|
| Opens | the Claude app: one assistant, chats and projects | Telegram they already use: a bot for every project and the main bot that routes orders; a voice note is an order too (the OpenAI key) |
| Orders | the person brings the context: files, a project, explanations | the agent whose job it is already knows its project — its steps, memory and own window; a neighbour's project does not crowd it |
| Puts the phone away | the work runs in Anthropic's cloud: Research up to 45 minutes with sources; connectors act in the services connected | the work runs on the person's computer: code, tests, build, deploy; a long task outlives a full window by a letter; an element's clock wakes its agent tomorrow at its hour |
| Receives | an answer, a report, a file or an artifact in the Claude.ai account — to download or share by link | a link to a live page on the person's own domain (the node never sends a link that does not open), a clip, a reminder that comes by itself, an answer from memory with its date and source |
| What stays | the chat and what the person saved | everything in their data, git and memory — the next order stands on the last one |
| Who else gets it | the person, a team on a team plan | their clients and family: a site with sign-in and roles, a bot that answers them; each relative on their own subscription (step 689) |

**Where Claude.ai is better** — the one-off: a question, a text, a photo, a quick research. It answers at once, nothing has to stay on
and nothing has to be kept. Say it: honesty here makes the rest believed.

**The node's price, said aloud:**
- the same subscription, and its limits are shared by Claude and Claude Code (support.claude.com, article 11145838): heavy work of the
  node takes from the person's Claude.ai too;
- the computer stays on, or a VPS: while it is off visitors get the copies of the pages, the agents rest and the bots are silent;
- voice and the deep memory's thinking go through the OpenAI key; without it the memory thinks with Claude by the subscription;
- payments between agents and the Lagrix network are on the way — the search is simulated today.

## The native elements — what each gives a person
| Element | What it gives |
|---|---|
| auth | sign-in, sessions and roles; forms in 82 languages; single sign-on for elements on their own domains; Google and a magic link once their keys are set |
| data | the tables of every element behind one door; journals of deploys and of agents' conversations |
| storage | files up to 200 MB with a permanent address, thumbnails, video trimming, a site's icon set from one picture |
| embeddings | text into vectors on this computer, with no key and no internet, about 50 languages |
| vectors | search by meaning over the collections of any element |
| graph | a knowledge graph of who and what is linked; no language model inside, one operation in about two seconds |
| memory | «remember» and «remind» by a phrase, a photo, a PDF or a voice note; the answer with its date, source and certainty; reminders at a time |
| config, design | one set of settings and one look for every element: saved once, every element re-styles at once, without a rebuild |
| blocks | ready sections of pages for the agents — tokens saved on every page |
| stripe | a Stripe payment link; no card number reaches the node; on after its keys |
| cache | fast counters and queues — a body only today, Redis not connected |
| root | the main site; its home is the first screen where a person types or says a task to the node |
Each lives on this computer; `npm run contacts -- --all` and `npm run card -- <id>` say it in the node's own words before any claim.

## Roles and what they open
Fourteen roles and the guest (`lib/roles.ts`), in four groups: customers and subscribers (a buyer, a VIP, three levels of
subscription), staff (managers, support, delivery, a content editor), finance and administrators; the architect is in every group.
Guest and role access is set for every route, and the lock stands in the door on the server, not on the page (skill `use-roles`). From
the phone this opens: paid levels of content with Stripe; a shop where delivery sees the orders and finance the money, and not the other
way round; a family where each person runs their own element; a client's project with its own people, unseen by the others (the app
factory). Claude.ai has accounts for the person and their team; a node has a system of users for the person's clients.

## Discovery — by search engines and by agents
- The public pages are static and built by the standards of search (`check:seo`); every page has a text twin for models, with
  `llms.txt` and `llms-full.txt` (`check:aio`): an AI search engine or another agent gets text, not markup.
- A copy of the public pages in Cloudflare answers while the computer is off.
- Every element publishes an A2A card naming all its doors (`check:a2a-card`) — agents find what it does by it; its visibility in the
  Web4 network is a switch of its own (`npm run web4`).
- One condition: an own domain — a temporary address changes and can be neither indexed nor shared.

## a2a and payment — today and on the way
- **Today — i2i:** the elements of one node agree an API once, and the work between them runs with no model.
- **On the way — a2a:** an agent of another owner finds an element, orders a result and pays in USDC through an escrow; reputation grows
  only from paid work, and the network has no coin of its own (github.com/lagrix-dev/lagrix — documents 04, 17, 27). The network search
  is simulated today; a live list will cost $0.01 (document 17, §17.8). Lagrix sees a Fractera element as any other agent.
- **The rule that shapes the whole story:** an outside order is served by the element's door — its code — never by a Claude session on
  the owner's subscription: the provider's rules do not let other people's work run on it (`provider-rules`). What an element sells is
  what its code does; where a model is needed, it runs on an API key.
- **People's money today:** the Stripe element (Web2); the node's wallet for Web3 — `/api/node/wallet`.

## Why a platform does not make Fractera unnecessary
Never «always» and never «it cannot compete»: neither can be proven. Any single feature of Fractera can be built by a platform, and the
platforms move up the stack — anthropic.com's own menu, read 2026-11-08, names Managed Agents, Cowork, Plugins and Skills. So Fractera
never bets on a feature. It bets on a position a platform cannot take without ceasing to be a platform:
1. **Neutrality.** A platform is always for its own model. The node stands above the providers: voice runs through OpenAI today, and the
   whole node switching its engine to Codex is step 690 in the queue — its agents run on Claude Code only today. While there is more
   than one provider, the place above them exists.
2. **Ownership.** A platform earns on what lives with it. A node keeps everything with the person — computer, domain, git, data,
   clients; if Fractera disappeared tomorrow, nothing would break (CLAUDE.md §2).
3. **A business built around one owner** — a site for search, sign-in with roles for the clients, payments, a bot, the stores — on the
   person's own machine. A platform makes general bricks for everyone; a business assembled around one person is not its field.
   Mercedes has its own AMG, and BRABUS lives because it is independent (How it works, §7).
4. **A network with no middleman.** Nodes of different owners whose agents find each other and trade work directly (Lagrix). A centre
   cannot build a world without a centre. Today it is simulated.
5. **The platform's speed is our tailwind.** A node runs the unmodified Claude Code, so every new model is a free engine upgrade. When a
   platform ships what we built by hand, we take theirs and drop ours — «create — yes, invent — no» works here as a strategy: never
   build what a platform will obviously build itself.
The honest risk is not competition but dependency — the next part. In a cold voice: the difference holds while there is more than one
provider, while people want to own what they build, and while Fractera does not compete with a platform in its own field.

## Pain, not death
A platform may change its rules, block an account or disappear. For a node that is pain — switching to another provider — never death,
because a model is needed to build and to think, and rarely to run: the i2i law moves work between elements onto agreed APIs with no
model. Where a product, its data and its people live inside someone else's account, one block takes them all at once — that is death.
| If it goes | What stops | What stays |
|---|---|---|
| Anthropic | the agents: building, their work, the task window on root's home | the whole running product — sites, sign-in, tables, files, payments, connectors between elements, reminders (they need no model); the apps' AI (it goes through the OpenAI key); the deep memory with the OpenAI key; the vectors (counted locally) |
| OpenAI | voice and the apps' AI until another key; the memory thinks with Claude | everything else |
| Cloudflare | reach from outside and the copies of pages | everything on the computer; Telegram (it needs no domain) |
| GitHub | pushing and pulling | all code in git on the disk |
| Stripe | taking payments | orders and users |
| Telegram | the bots | the node's terminal and pages |
| Fractera | new releases only | everything |
- **Local models, honestly:** one already runs — embeddings counts every vector of the node on this computer. The apps' AI goes through
  one door with one key; that door can be pointed at another provider or a local model, with limits of quality and of the computer's
  power — a potential, not built and not measured.
- **Where the pain is larger today than it must be:** the agents have no engine switch yet — 690 is queued; until it is built,
  switching is manual work, not a button.
- **The one death left is the person's own disk.** Everything lives with them, so a lost disk without a copy is the only thing that
  can end a product. The stores' agents make backups on request (`npm run task`) — say it with the rest.

## How to say it
- The answer first, in the person's language; a short question — a short answer, depth — the parts above that it needs.
- Every claim about a foreign service from its own page with its date (CLAUDE.md §6); a claim older than six months is read again
  before it is used — the platforms move fast. Never «nobody else does this», never «Claude.ai cannot …» unless its page says so.
- What is on the way is said as on the way; a number of this node comes from its own command (`contacts`, `card`, `load`).
- The advantage is named when a limit would make the person think small — once, with the fact (the soul, «What you fly on»).

## Sources (read 2026-11-08)
- anthropic.com/news/research (2025-04-15) — Research, agentic searches with citations.
- anthropic.com/news/integrations (2025-05-01) — Integrations through remote MCP; research up to 45 minutes; web search on paid plans.
- anthropic.com/engineering/multi-agent-research-system (2025-06-13) — agents ≈ 4× and multi-agent systems ≈ 15× the tokens of a chat.
- support.claude.com, article 11145838 — the limits shared across Claude and Claude Code.
- github.com/lagrix-dev/lagrix — documents 04 (escrow), 12 (API), 17 (discovery and reputation), 27 (the life of a deal).
