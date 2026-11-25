# Content Topic Judgment Framework

A decision framework for content operators: given a topic, decide whether to write it, and
if so, with what priority. Distilled from real-world brand content operations.

The core problem this solves: content teams waste effort on topics that feel productive but
don't convert — topics loosely related to the product, topics that chase keywords the team
doesn't actually understand, or topics that recycle past wins whose opening has closed.

This framework runs every candidate topic through 4 gates.

## Gate 1 — Relevance (the first filter)

The first question for any topic: how directly does it connect to the product or business?

Trace the path from the topic's entry point to your product. Count the turns.

- **0-1 turns** — strong. The topic naturally leads to the product. Pass.
- **2 turns** — borderline. Only proceed if Gate 2 (signal) is strong.
- **3+ turns** — reject. This is a "forced connection." If you need a long chain of logic to get from the topic to your product, readers will feel the stretch.

**Forced connection (reject):** an unrelated industry policy → some intermediate consequence → another consequence → finally your product. Too many turns; the starting point has nothing to do with what you sell.

**Strong relevance (pass):** a topic where the product is the subject itself — explaining how the product works, correcting a misunderstanding about it, or answering a question users actually have about it.

**Compensation rule:** Relevance is a *soft* gate. If a topic has very high traffic potential, it can compensate for weaker relevance. Nothing else compensates — relevance is the only gate that flexes.

## Gate 2 — Signal (is this grounded in something real?)

Strong topics come from real external signals, not from brainstorming in a vacuum. Rank the signal source by reliability:

**Tier 1 — highest reliability:**
- **Direct user questions** — the questions customers ask most often, directly. When users repeatedly open with the same question, that's the strongest and lowest-effort signal there is: a real need, and the frequency itself tells you the traffic.
- **Keyword co-occurrence in user feedback** — what users mention *alongside* your category. When people discussing an adjacent topic naturally bring up something in your domain, that co-occurrence is a precise signal that real users need your product in that context — often more precise than people directly searching your category, because it reveals the surrounding need.
- **Backend / behavioral data** — patterns in what your users actually do. Reverse-engineer the scenario from the data, then write for it. Data-driven, high reliability.

**Tier 2 — reactive but valuable:**
- **Misconceptions to correct** — when your product is misrepresented somewhere, a clarification piece is high-value and naturally relevant.

**Tier 3 — monitor, don't chase blindly:**
- **Competitor moves / industry news** — sometimes worth it, but check relevance carefully (these often fail Gate 1).

**Tier 0 — no judgment needed, just do it:**
- **Product updates / official announcements** — you write what there is to write. No filtering required.

**A topic with no signal behind it — purely "I think this would be interesting" — gets downgraded.** Find the signal first.

## Gate 3 — Depth (can this become something worth reading?)

The gate that separates substantial content from keyword-bait.

The question is NOT "can we run a hands-on demo." Some topics are operational (how-to, configuration, workflows) and depth means giving the reader concrete, reproducible steps. Other topics are explanatory (why something happens, how a concept works, where a trend is going) and depth means understanding the subject well enough to explain it clearly and non-obviously.

Either path is valid. The real test is:

- **Do we genuinely understand this topic** — well enough to give the reader something they can take away, whether that's a set of steps or a clear explanation that goes beyond the obvious?
- **Or are we only writing it to chase a keyword,** with nothing of our own to add?

If it's the former, write it. If it's the latter — a topic that looks writable but, once you start, has nothing concrete or insightful behind it — reject it, no matter how good the keyword looks.

## Gate 4 — Prioritization (which one first?)

Topics that pass Gates 1-3 are usually few. Among them, decide order by weighing two factors together:

- **Traffic potential** — how many people are looking for this?
- **Timeliness** — is there a window that closes? Is this tied to a current event or a freshly trending signal?

Weigh them together. A high-traffic evergreen topic and a medium-traffic time-sensitive one might swap priority depending on whether the window is closing.

## The critical failure mode: recycling past wins

The most common mistake — and the one AI is most prone to — is **assuming past performance predicts future performance.**

A topic that performed well historically is tempting to rewrite. But rewriting it often underperforms.

Why: the original may have won because of *timeliness* or because it *filled a gap that existed at the time*. Rewrite it later and the gap may be filled, the timing may have passed — even if the subject is identical, the opening is gone.

**Rule:** Don't judge a topic only by its historical numbers. Judge whether the gap still exists *at this specific moment.* Has someone else already covered it well? Has the timing passed? If the opening is gone, strong historical data doesn't save it.

## How to apply this framework

When given a topic or a list of topics:

1. Run each through Gate 1 (relevance — count the turns to the product)
2. For survivors, identify the signal source and tier (Gate 2)
3. Test depth — do we understand it well enough to give the reader something real, whether steps or a clear explanation? (Gate 3)
4. Apply the compensation rule (high traffic can save weak relevance)
5. Check the failure mode (is this a recycled win whose opening has closed?)
6. Rank survivors by traffic × timeliness (Gate 4)
7. Output a clear verdict per topic: Write / Borderline / Reject, with the reason

## Output format

```
## 选题判断

**选题**,[topic]

- 相关性(Gate 1),X 次转折 → 通过 / 边缘 / 否决
- 信号来源(Gate 2),[Tier 0-3 / 无信号] — [具体信号]
- 深度(Gate 3),能给读者带走的东西(步骤或讲透) / 只能蹭词 → 通过 / 否决
- 二次写作风险,[是否为历史选题重写,当下空白是否还在]

**结论**,写 / 边缘可写 / 否决
**理由**,[一句话]

---
[多个选题时,最后给出优先级排序及依据]
```
