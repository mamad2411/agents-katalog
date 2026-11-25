---
name: twitter-morning-brief
description: Use this skill when the user wants a calm, high-quality summary of developments on X in any chosen topic or multiple topics/categories over a chosen time period. Always prioritize high-signal items regardless of reach, use neutral language, justify selections, and deliver in consistent Markdown format.
---

# Twitter Morning Brief

## Overview

This skill creates focused, signal-rich briefings from X activity. It helps the user replace mindless scrolling with a structured, 10-15 point overview plus a short synthesis, while always including objectively important developments even when they have lower engagement.

## Instructions

When the user requests a summary for one or more topics/categories and a time period:

1. Determine the exact time range and construct appropriate since: and until: operators for the search.
2. If multiple topics or categories are provided (e.g. cybersecurity + AI), gather posts for the combined scope and create one coherent briefing that covers all of them (either integrated or with clear sections per category).
3. Gather relevant posts using x_keyword_search and/or x_semantic_search, adapting the query to the provided topic(s).
4. Evaluate posts for signal strength using general criteria: objective importance and potential impact for the topic(s), novelty, authority of the source. Always include high-signal developments even if engagement is low.
5. Select 10-15 most important points across the requested scope(s), giving clear priority to high-signal items.
6. Present the points in clean Markdown using clear headers (for example ## Główne wydarzenia wysokiego sygnału and ## Inne ważne punkty). Where relevant, include direct links to posts and short quotes. If multiple categories were requested, consider using sub-headers for clarity.
7. Use neutral language throughout.
8. At the end, add a short original synthesis describing what actually happened across the requested topic(s) during the selected period.
9. Always briefly justify why the selected points (especially high-signal ones) were included.
10. Adapt the interpretation of "high signal" to the specific topic(s) the user gave.
11. The goal is to deliver a complete, satisfying overview so the user feels well-informed without needing to scroll further.