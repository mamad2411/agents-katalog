---
name: rea-looksmaxxing
description: Run the /rea-looksmaxxing play - reverse engineer how a creator gets paid (Clavicular is the worked example) from their most viral clips, then post that formula through your own accounts and funnel everyone who replies or DMs into your offer, in your voice. Use when someone says /rea-looksmaxxing, "how does <creator> get paid", "moneymaxx like <creator>", or wants a creator's viral formula turned into posts, replies and DMs. Builds on treg's web-access skill for the social data and on log's MCP tools for the accounts.
metadata:
  summary: Finds a creator's most viral clips and the formula behind them, then posts it through your accounts and funnels the replies and DMs into your offer, in your voice.
  requires: "treg web-access skill (social data), log MCP server (logMcp)"
  dependsOn: treg.to/treg treg.to/web-access
---

# /rea-looksmaxxing

Reverse engineer how a creator makes money, then run the same play on your own accounts. Two tools do
the work:

- **treg** reads the social data: the creator's clips, the clip farms around them, views, captions and
  comments. This skill builds on treg's `web-access` skill, so read it once before the first call
  (`https://treg.to/.well-known/skills/web-access/SKILL.md`, or the copy the installer put beside this one).
- **log** runs your accounts: posts, replies, DMs, Discord, Instagram, each through the account's one
  session, every message checked against how you write before it goes out. Its MCP server is `logMcp`.
  Load its guide first: `getGuide({ topic: "logMcpInstructions" })`.

The worked example is Clavicular: treg pulled 40 of his clips, the top one had 8.44M views, and his
offer is a looksmaxxing program. Swap in any creator and any offer.

## Before you start

```
treg --version && treg balance            # treg is set up and has a balance
log --help                                # log is installed (its MCP server is logMcp)
```

Neither there? Don't install on your own. Tell the user what each adds and point them at:

```
curl -fsSL https://log.listeningkit.com/install.sh | sh -s -- --skills rea-looksmaxxing
```

Social data through treg costs cents or fractions of a cent a call. Say the price before a batch, and
send `X-Treg-Route-Max-Cost` on every batch call.

## The play

### 1. Find what made them go viral (treg, reads only)

Search the catalog by the job, never a remembered endpoint id (web-access, "Finding the endpoint"):

| You want | Search the catalog for |
| --- | --- |
| Their clips and the clip farms reposting them | "tiktok search videos" with the creator's name |
| One account's posts | "tiktok user posts", "instagram user reels", "x user tweets", "youtube channel videos" |
| What people say under the best ones | "tiktok video comments", "instagram post comments", "x tweet replies" |

`treg catalog get <id>` for the price, then one small call, then the batch. Keep for every clip: the
account, the caption, views, likes, the date and the URL. Rank by views and keep the source next to
every number.

### 2. Decode the formula

Sort the top clips into formats (a comedy skit, a mog edit, a morning routine, a "NEVER do X" take,
a hot take) and count the views per format. Three things decide a winner: the hook in the first two
seconds, the tension (the outlandish claim) and the payoff. Write down the 3 formats with the most
views, each with its best clip as proof. Then find the money: how the creator sells (a program, a
Discord, merch, a link in bio). That is the funnel you copy.

### 3. Connect your accounts (log)

| Step | MCP tool | Done when |
| --- | --- | --- |
| Add each account once | `localAccount` (or `log localAccount add --platform <p> --account <name>` in a terminal) | it's listed |
| Check each one is signed in | `twitterSessionCheck`, `instagramSessionCheck`, `discordSessionCheck` | the platform says loggedIn |

### 4. Post the formula

Write each post in one of the winning formats, in the user's voice, never copied word for word. On X,
`twitterPost` posts one (a dry run until `twitterPostLive` with `confirmLive: true` and the user's yes).
Several go through the account's one queue (`twitterQueueBuild`, `twitterQueuePlan`,
`twitterQueueRunLive`), at random times, never a loop.

### 5. Funnel everyone into the offer

| Step | MCP tool | Done when |
| --- | --- | --- |
| See who replied, liked or followed | `twitterNotifications` | a list of real people with what they did |
| Read each person's whole thread first | `twitterDms` { with }, `instagramDms`, `discordRead` | you know what they asked |
| Draft in the user's voice, then check it | `voice` { to, with, context }, then `voice` with `text` | the check passes |
| Answer them | `twitterReplyLive`, `twitterDmLive`, `instagramSendLive`, `discordSendLive` | the platform answers `sent` |
| Point them at the offer once they're keen | the same send tools | they're in the Discord, or on the offer |

The first message is about them and what they said, never the pitch. The offer comes after they answer.

## Lines not to cross

- **Reads first, sends only with a yes.** Every tool that acts is its own `…Live` tool and needs
  `confirmLive: true`. Nothing is posted or sent unless the user asked for it.
- **One session per account, never in quick succession.** A 429 or any refusal stops the run, and
  nothing resumes on that account until the user says so.
- **Every send is checked by `voice`.** A draft that fails is rewritten, never forced.
- **Public data only** through treg: never log in as anyone or get round a paywall.
- Step 7 of the video says to build the offer on people's insecurities, and adds "we don't recommend
  it". Neither do we. Sell the outcome.
