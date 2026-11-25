---
name: x-profile-post-reader
description: Inspect and summarize publicly visible posts on an X profile. Use Mocu Browser Bridge for navigation and page inspection, and Computer Control for all on-page mouse and keyboard interaction.
---
# X Profile Post Reader

## Purpose
Read publicly accessible posts from the X profile requested by the user and summarize them accurately. Follow the visible browser workflow. Never replace required mouse interaction with DOM actions, scripts, direct page APIs, or hidden browser automation.

## Required input
- The target X username or profile URL.
- Any requested date range, topic, or selection criteria.

If the target profile is missing or ambiguous, ask the user which account to inspect before proceeding.

## Tool responsibilities
- **`/extension Mocu Browser Bridge`**: Open or focus Chrome, navigate to `https://x.com/home`, and inspect the active tab and visible page content. Use it to verify that the home page or target profile has loaded and to read posts actually visible on the page. Do not use it to click, hover, scroll, or type within X.
- **`/extension Computer Control`**: Use the mouse for all on-page interactions: visibly move/hover over controls, click them, and scroll. Use the keyboard only for typing or keyboard submission when needed. Identify targets from the current visible screen; do not guess coordinates. Do not use Browser Bridge clicks, DOM selectors, scripts, or direct APIs for on-page interaction.

## Procedure
1. Use `/extension Mocu Browser Bridge` to open or focus Chrome and navigate to exactly `https://x.com/home`.
2. Use Browser Bridge to inspect the active tab and confirm the X home page is loaded. If it is not usable, use Computer Control to click the visible page and press F5 once, then verify again with Browser Bridge. If it remains unusable, stop and report the issue.
3. Navigate to the requested profile through visible X UI. If the requested profile is the signed-in account, use Computer Control to move the mouse over the visible **Profile** navigation item and click it. If the user requested another account, use Computer Control to move the mouse over the visible X search control, click it, type the requested username, then use the mouse to select the matching visible profile result. Do not navigate directly to a constructed profile URL.
4. After the mouse click, use `/extension Mocu Browser Bridge` to check that the profile page has loaded. Verify that the displayed username/handle matches the requested account before reading posts. If the page has not loaded, wait briefly and inspect again; if it still has not loaded or the account does not match, stop and report the problem. Do not read posts from an unverified profile.
5. Use Browser Bridge to inspect the posts currently visible on the verified profile. Record only content and details visible in the current page; do not claim to have seen anything that is not displayed or accessible.
6. If more posts are needed, use `/extension Computer Control` to move the mouse over the page and scroll down with the mouse wheel in small increments. After each scroll, use Browser Bridge to inspect newly loaded posts. Scroll no more than three times total; stop sooner if the end of available posts is reached.
7. Summarize relevant posts in English. Distinguish directly observed content from interpretation, and state any loading, access, date-range, or coverage limitations. Do not claim comprehensive coverage if only a limited set of posts was inspected.

## Boundaries
- Use ordinary, transparent browser interaction. Do not pretend to be human, disguise automation, evade detection, or bypass X safeguards.
- Read only posts available to the current user/session. Do not attempt to access private, restricted, or otherwise unauthorized content.
- Do not like, repost, reply, follow, message, or make other account changes.
- Do not invent missing post details.
- Keep all instructions, searches, and the final response in English.
