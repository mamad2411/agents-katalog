---
name: web-publish
description: Insert, update or translate content inside a web admin panel using the `beam` CLI — posts, pages, products, custom fields, media uploads, on WordPress or any other CMS or back-office. Use it when the user asks to publish an article, load content, do data entry on a site, fill backoffice forms or translate pages.
---

# web-publish

Content work inside a web backoffice, driven by the HTML structure rather than
by screenshots. The tool is `beam` (see the `beam` skill for the commands): it
reads the page as text, writes into fields, uploads files, saves.

This skill is **CMS-agnostic**. WordPress is the only one with a verified
recipe; for everything else, apply the discovery procedure and save an adapter,
so the next time is immediate.

## Before you start

1. `beam ping` — if it answers `extension not connected`, ask the user to click
   the Beam icon in Chrome.
2. `beam open <url>` for the screen you need. It lives in Beam's own window,
   unfocused, and the same tab is reused — do not pass `--new` or `--focus`,
   and do not close it when you are done. `beam use <id>` only when the person
   already has the right tab open; it does not bring it forward. Beam refuses
   to write if that tab changes from outside: that is a guard, not an error to
   force past.
3. Check the session: if a `beam snap` shows a login form, stop and ask the user
   to authenticate. Never enter credentials yourself.

## The method, in six phases

**1. Get oriented.** `beam info` and `beam snap --max 60` on the starting
screen. If the CMS keeps its editor inside an iframe (Gutenberg, most page
builders), `beam frames` reveals it and you work there with `--frame <id>`.

**2. Map the fields.** `beam fields` gives the label, `name`, id and selector of
every field. That is the map everything else is built on: prefer `name=` and
`css=#id` as targets, because they survive reloads; `@n` refs only last until
the next snap.

**3. Prepare the content.** If the text arrives as Markdown:
`beam-mdconv text.md --format gutenberg|html|text [--json]`. `--json` also
returns the title, the excerpt and the list of images referenced. Write the
payload to a JSON file instead of passing it inline: apostrophes in the copy
break the command line.

**4. Preview, then write.** `beam set --dry @payload.json` shows the diff field
by field. Actually look at it: that is when ambiguous labels surface. Then
`beam set @payload.json`.

**5. Media.** `beam upload <file-input-target> <url>` downloads a file and drops
it into the input the way a person would. It needs a reachable
`input[type=file]`: nearly every CMS has one in a "classic" upload page, often
simpler than the modern modal. When a dropzone is the only way in,
`beam drop <zone> <file|url>` drops the file onto it, as a desktop drag would.
Local files work too: `beam upload <target> ./photo.jpg`.

**6. Save and verify.** Always save as a **draft**. Then read it back:
`beam fields --json` and compare against the payload — a click on "Save" does
not prove the server accepted it. Check the status stayed what you wanted, too.

## Rules

- **Draft by default.** Never press "Publish", "Update" on already-live content,
  "Delete" or "Send" unless the user asked for it explicitly in this
  conversation. If it is ambiguous, ask in one line.
- **Verify after saving.** A `beam text` of the page after saving catches 403s,
  expired sessions and failed validation. If you read a server error (WAF, 403,
  500), stop and report it: do not retry in a loop.
- **No credentials.** Login, 2FA and CAPTCHAs are the user's job.
- **One site at a time.** Re-check `beam info` before writing.
- **On already-published content** run `beam fields --json > backup.json` first:
  it is the only undo you have.

## Adapters: learn a site once

Every site you work out goes into `~/.beam/adapters/<host>.json`. **At the start
of a job, check whether an adapter for that domain already exists**: if it does,
you already have the selectors and the traps and you can skip discovery.

```json
{
  "host": "wordpress.test",
  "cms": "WordPress 7.1 · block editor",
  "note": "post-new.php is hijacked by the Aura builder: add ?aipb=skip",
  "tasks": {
    "post.create": {
      "url": "https://wordpress.test/wp-admin/post-new.php?post_type=post&aipb=skip",
      "prepare": ["Options → Code editor: the body is pasted as block markup"],
      "fields": {
        "title": "css=#inspector-textarea-control-0",
        "body": "css=#post-content-0"
      },
      "media": {
        "url": "https://wordpress.test/wp-admin/media-new.php?browser-uploader",
        "input": "css=#async-upload",
        "submit": "css=#html-upload"
      },
      "save_draft": "text=Save draft",
      "verify": "https://wordpress.test/wp-admin/edit.php?post_type=post"
    }
  }
}
```

The fields are free-form: they are notes for you, not a rigid schema. What
matters is that next time they are enough to act without exploring again. Update
the file when you find something has changed. There is a commented example in
`examples/adapters/` in the Beam repo.

## Working out a CMS you do not know

The full procedure is in `references/discovery.md`. In short: start from the
creation screen, `beam frames` for iframes, `beam fields` for the fields, look
for the "HTML/code" editor (it almost always exists and is far more reliable
than the visual one), find the save-as-draft button, do a full dry run on a test
item, and only then write the adapter.

## Verified recipes

- **WordPress** (posts, pages, ACF, media, featured image, WPML):
  `references/wordpress.md`.

No recipes exist for other CMSes yet: apply discovery and write the adapter. Do
not invent selectors "typical" of a platform you have not inspected — read it.

## Recurring traps

| symptom | cause | what to do |
|---|---|---|
| everything reads `(hidden)` | the tab is not the selected one of its window | Beam's window already is; on a tab of theirs, `beam focus` only if they asked, or read with `--hidden` |
| the editor is missing from the snap | it is inside an iframe | `beam frames`, then `--frame <id>` |
| I write into the field but the app ignores it | a framework listening for its own events | `beam fill` already fires them; if that is not enough, find the code editor |
| `@n` refs stop resolving | the page or iframe was recreated | run `beam snap` again, or use `name=`/`css=` |
| saving returns 403 | an application firewall on the server | stop: it is not a browser problem, it has to be fixed on the hosting |
| a long list "loses" items | a virtualized list | filter or search instead of scrolling |
