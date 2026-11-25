---
name: research-core
description: Constitution of the research family: the question stated before the search, the source hierarchy that ranks a primary document above a summary of it, the rule that a source is never cited unless it was actually consulted, the separation of fact from inference from opinion, and the honest report of what could not be established. Load before any research, source check, competitive analysis or synthesis.
license: MIT
metadata:
  category: research
  version: 1.0.0
  depends_on: []
  outputs: [research-question, source-hierarchy, evidence-standard, uncertainty-record]
---

# Research Core

The rules every research skill obeys and none restates. General-purpose
research, distinct from the writing tree's `research-director`, which serves
fiction. This tree answers real questions with real sources, for a decision.

It is loaded first, depends on nothing, and can be used alone.

## 1. The question before the search

A search without a stated question returns whatever is loudest. State the
question, its scope, and what an answer would have to contain, before looking.

```
question    the specific thing to be established, in one sentence
scope       what is in and what is out; the time range, the geography, the domain
answer shape   what a complete answer looks like: a number, a comparison, a
            yes-with-conditions, a list with criteria
decision    what the answer is for, so depth matches the stake
```

A question that cannot be stated in one sentence is several questions, and they
are researched separately.

## 2. The source hierarchy

Not all sources are equal. Rank them, and prefer the top of the ladder.

```
primary       the thing itself: the law, the paper, the filing, the API docs,
              the dataset, the official announcement, the source code
official      the responsible body's own statement: the vendor, the agency, the
              standards org, the maintainer
reputable     independent reporting or analysis that cites its own sources
aggregated    a summary of the above; useful for orientation, never the final word
unattributed  a claim with no source; treated as a lead to verify, never as evidence
```

A summary is a pointer to a primary source, not a substitute for it. When a
claim matters, follow it to the top of the ladder.

## 3. A source is cited only if it was consulted

The rule that makes a research report trustworthy: a source is named only if it
was actually opened and read. A plausible citation that was never consulted is a
fabrication, even when the source turns out to exist and to support the claim.

```
say     according to <source>, which was consulted, at <location>
never   a citation reconstructed from memory of what a source probably says
never   a URL that was not actually retrieved
never   a statistic attached to an authority that was not checked
mark    when a claim is believed but unverified, label it as such, do not dress
        it as a citation
```

This is the research equivalent of the engineering evidence rule: never assert
as consulted what was not consulted.

## 4. Fact, inference, opinion

Every statement in a research output is one of three things, and the reader is
told which.

```
fact        established by a consulted source; attributed
inference   the researcher's reasoning from facts; labelled as inference, with
            the facts it rests on
opinion     a judgement, the researcher's or a source's; labelled, and the
            source's authority stated
```

The failure this prevents is the confident synthesis that reads as fact and is
actually the researcher's guess. Label the guess.

## 5. Conflicts are surfaced, not smoothed

When sources disagree, the disagreement is the finding.

```
report    that they disagree, who says what, and the quality of each source
weigh     by the source hierarchy and by recency and by conflict of interest
resist    the urge to pick the answer that fits the desired conclusion
unresolved   when the conflict cannot be resolved, say so, and say what would
          resolve it
```

## 6. What could not be established

An honest report states its own gaps. The absence of a finding is itself
information.

```
say     this could not be established from the sources consulted
say     this source was paywalled, offline, or out of scope
say     this would require a source not available here, name the kind
never   fill a gap with a plausible invention to make the report look complete
```

## 7. Prohibitions

- Never search before stating the question.
- Never cite a source that was not actually consulted.
- Never present inference or opinion as fact.
- Never smooth over a conflict between sources to reach a clean answer.
- Never fill a gap with an invented fact, statistic, source, or quotation.
- Never let the desired conclusion select the evidence.
- Never treat an aggregator's summary as equal to the primary source it summarises.

## 8. Protocol

1. State the question, scope, answer shape, and the decision it serves.
2. Identify the kinds of source that would answer it, highest on the ladder first.
3. Consult them; record each as actually consulted, with its location.
4. Extract findings, labelling each as fact, inference, or opinion.
5. Surface conflicts; weigh sources; mark what stays unresolved.
6. State what could not be established and what would establish it.
7. Answer the question at the depth the decision needs, no more.

## 9. Auto-critique

Score from 0 to 5: question stated before searching, sources ranked with
primaries preferred, every citation actually consulted, fact separated from
inference and opinion, conflicts surfaced rather than smoothed, gaps stated
honestly, the answer matched to the decision.

Threshold: no axis below 3, average at least 4. Any cited-but-not-consulted
source, or any invented fact or statistic, is an automatic zero regardless of
the average.

## 10. Interfaces

- Downstream, this tree: `source-research`, `source-verification`,
  `competitive-analysis`, `synthesis-reporting` refer to this constitution and
  do not restate it.
- Other trees: `research-director` in `writing/` serves fiction and is separate.
  `report-writing` in `documents/` renders a research finding for a decision.
  `technology-selection` and `dependency-selection` in `engineering/` are
  domain-specific research with their own criteria.
- Lateral: `self-critique` for the skeptic role pass.
