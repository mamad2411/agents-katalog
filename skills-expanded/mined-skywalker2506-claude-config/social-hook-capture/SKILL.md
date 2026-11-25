---
name: social-hook-capture
description: Analyze a project/product/game and previous posts, capture hook screenshots or GIFs with Playwright, choose Reddit/social media targets, generate post copy, and create posts/post_N.md previews with linked media. Use when Codex is asked to make Reddit posts, social media hooks, screenshot/GIF-led launch/devlog/promotional posts, community-targeted captions, or a repeatable posts/ content pipeline.
---

# Social Hook Capture

## Goal

Create a repeatable post pipeline: analyze the project and previous posts, choose the best audience/platform angle, capture a screenshot or short GIF that proves the hook, write platform-ready copy, and save a preview under `posts/post_N.md` with media assets.

## Default Strategy

Do not post automatically. Produce local drafts and previews only. The user decides what gets published.

Keep the workflow lightweight:

- Store output in the target project's `posts/` folder.
- Use `posts/assets/` for screenshots, GIFs, and temporary captured frames.
- Use `post_0.md`, `post_1.md`, etc. by default.
- Scan older `posts/post_*.md` files before writing a new one so hooks, screenshots, audiences, and wording do not repeat.
- For Reddit, treat subreddit rules and self-promo norms as changing external constraints; verify them before final posting when a subreddit is named.
- Before browser media capture, check dependencies. If Playwright or ffmpeg is missing, explicitly tell the agent/user what to install instead of failing silently.

## Workflow

1. **Check media capture dependencies when screenshot/GIF is needed.**

   ```bash
   node <skill>/scripts/check-media-deps.mjs <target-project>
   ```

   If Playwright is missing, tell the agent/user to run `npm install -D playwright` in the target project or tool environment. If GIF output is needed and ffmpeg is missing, tell them to install ffmpeg and ensure it is on `PATH`. Continue with text-only draft scaffolding if the user does not want to install dependencies yet.

2. **Analyze existing post history.**

   ```bash
   node <skill>/scripts/analyze-post-history.mjs <target-project>
   ```

   Read `posts/post-history-analysis.md`. Identify repeated hooks, used platforms, target audiences, screenshots, strongest claims, weak patterns, and the next post number.

3. **Analyze the project/product.**
   - For games/apps: inspect README, package metadata, screenshots, `public/`, recent changes, gameplay state, and built UI.
   - Identify the most postable proof: surprising mechanic, visual before/after, satisfying interaction, clear problem solved, launch milestone, Steam-ready build, localization, performance win, or funny constraint.
   - Prefer GIF when motion is the hook: physics, transformation, traversal, reveal, destruction, satisfying loop, UI interaction, before/after transition, or a funny emergent moment.
   - Define one primary audience: players, indie devs, Three.js developers, Steam shoppers, niche subreddit members, or general social feed.

4. **Choose target and hook.** Load `references/platform-hooks.md` before drafting. Pick one primary target per `post_N.md`; add alternates only as variants.

5. **Capture hook media with Playwright.** Use a screenshot for a single clear state, or a GIF when motion makes the post more clickable. If dependency check failed, state the missing install command before attempting capture.

   ```bash
   node <skill>/scripts/capture-hook-screenshot.mjs <target-project> --url http://localhost:5173 --selector canvas
   ```

   ```bash
   node <skill>/scripts/capture-hook-gif.mjs <target-project> --url http://localhost:5173 --selector canvas --duration 3500 --fps 12
   ```

   If no app URL is provided, ask for or infer the local dev/preview URL. Capture the actual product/game state, not a decorative mockup. Prefer one strong moment over a collage or noisy montage.

6. **Create the post preview scaffold.**

   ```bash
   node <skill>/scripts/create-post-preview.mjs <target-project> --platform reddit --target r/threejs --screenshot posts/assets/post_0.png --gif posts/assets/post_0.gif
   ```

   This creates the next `posts/post_N.md` and includes history notes, media links, target, hook slots, copy slots, and QA checklist. Codex should then fill the draft with real copy.

7. **Write the post copy.**
   - Make the first line carry the hook.
   - Keep claims specific and honest.
   - Avoid spammy hype, engagement bait, and repeated phrasing from older posts.
   - Use platform-native format: Reddit title/body, X short post, LinkedIn short dev note, Discord announcement, Steam community update.
   - Include a question only when it naturally invites feedback.

8. **Validate locally.**
   - Confirm screenshot/GIF paths exist and render.
   - Confirm `post_N.md` links media with relative paths.
   - Confirm GIF is short, readable, and starts quickly.
   - Confirm no TODO placeholders remain in the final version.
   - Compare against `post-history-analysis.md` for repetition.

## Output Shape

```text
target-project/
  posts/
    post_0.md
    post_1.md
    post-history-analysis.md
    assets/
      post_0.png
      post_0.gif
      post_1.png
      post_1.gif
      post_1_frames_<timestamp>/
```

If `posts/` does not exist, create it. If it exists, preserve all prior posts and append the next number.

## References

- Read `references/platform-hooks.md` before choosing target/platform copy.
- Read `references/screenshot-playwright.md` before screenshot/GIF capture or browser automation.
