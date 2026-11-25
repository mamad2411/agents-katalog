---
name: social-post
description: Make a social media announcement for a Seshboard feature or release, with a 1200×630 image in the app's look and post texts for X, Bluesky, Mastodon and LinkedIn, in the repo's social/ folder. Use when asked for a social image, a social post, an announcement, an Open Graph or share image, or "something to post about" a feature, a release or the VS Code companion.
---

# Social post

Every announcement is one folder in `social/<slug>/` with `index.html` (the image as a page), `image.png` (rendered from it) and `posts.md` (the texts). Read `social/README.md` first, and look at `social/vscode-companion/` as the worked example.

## 1. Get the facts

Take what the feature does from the repo, not from memory:

- `CHANGELOG.md` (the `## [Unreleased]` section or the release's section) for the wording people already see;
- the README, `docs/`, and for the VS Code companion `apps/vscode-extension/README.md`, `CHANGELOG.md` and `package.json` (publisher and name make the Marketplace and Open VSX links);
- the real UI: `docs/screenshots/*.png`, and component names and labels in `apps/ui/src` so the mockup shows real labels ("Add Selection to Seshboard", "Allow", "Always allow", "Deny…").

Check what is released: the version in `apps/desktop/package.json`, `git tag`, and "needs Seshboard X" notes. If part of the feature isn't released yet, say so in `posts.md` and tell the user. If the request is ambiguous (a typo, which feature), take the reading the repo supports and say which one you took.

## 2. Make the image

1. Copy `social/_template/` to `social/<slug>/` (a short kebab-case name for the feature).
2. Left column: the brand (the app icon `../../apps/desktop/build/icon.png`, or the companion's `../../apps/vscode-extension/assets/icon.png`), an eyebrow ("New in Seshboard", "New for VS Code"), a headline of at most about eight words with one phrase in `<span class="hl">`, and one or two sentences with the key words in `<b>`. The call to action at the bottom says where to get it.
3. Right column (`.stage`, 600×540): a small, made-up mockup of the feature at work, built in HTML and CSS, not a screenshot. Use the classes in `shared/base.css` (`.sb` message box, `.chip`, `.cable`) and add the rest in the page's `<style>`. Show the moment the feature helps: two or three overlapping cards, with a cable in the icon's colours (`--warm1`/`--warm2`, `--gold1`/`--gold2`) when something goes from one place to another. Use the demo world of the screenshots (acme-store, "Add dark mode toggle to settings", `theme.ts`), never real projects or paths.
4. Colours come from the tokens in `base.css` (the app's dark theme). Other apps in the mockup, such as VS Code, use their own colours, as page variables.
5. Copy follows AGENTS.md: plain, short sentences, no em dashes.

Give anything only this post needs to the page itself. When something is useful to more posts (a sidebar row, a permission card), move it to `shared/base.css`.

## 3. Render and look

```bash
social/render.sh <slug>
```

Then open `social/<slug>/image.png` with Read and check it, and render again after every fix:

- nothing is clipped (menus inside a window with `overflow: hidden` are the usual culprit) and no card runs off the edge;
- the headline keeps a clear gap from the mockup;
- cables start and end on what they connect;
- the text in the mockup is large enough to read when the image is shown at half size.

## 4. Write the posts

`posts.md` holds, in this order: the links, anything not yet released, the image's alt text (what the picture shows, for screen readers), then one section per network:

- **X**: at most 280 characters; a link counts as 23.
- **Bluesky**: at most 300 characters, links included.
- **Mastodon**: at most 500 characters, a few hashtags at the end (#ClaudeCode, #macOS, #VSCode).
- **LinkedIn**: longer, first person (Elio writes these), what it is, why it helps, a short list of what it does, links and a few hashtags.

Count the characters (for example with `python3`) instead of guessing. Lead with what it does for people, not how it's built. At most one emoji per post.

## 5. Finish

Add the post to the table in `social/README.md`. Don't post anything, and don't commit unless the user asks. Tell the user where the image and texts are, and show the image.
