---
name: connect-social-accounts
description: "Connect Instagram, TikTok, LinkedIn, X, Threads, Bluesky, Facebook, Pinterest and YouTube accounts so the assistant can post to them through WoopSocial. Use when the user asks \"can you post to my Instagram?\", \"connect my LinkedIn\", \"link my TikTok\", \"add a new client's accounts\", or a post can't go out because no account is connected. Explains what the assistant can and can't post (not Reddit or Mastodon), creates a project per brand or client, gives a secure sign-in link and confirms the account is live."
---

# Connect social accounts

Get the user from "can you post for me?" to a connected, working account in a few minutes. WoopSocial does the posting. The assistant never sees or stores social media passwords.

The user's explicit instructions take priority over these guidelines, except that you never post, delete or change posts beyond what the user asked for.

## Step 0: Is WoopSocial available here?

If no WoopSocial tools (projects_list, social_accounts_list and so on) are available, the connector isn't set up yet. Tell the user:

1. Create a WoopSocial account: https://app.woopsocial.com/signup?utm_source=claude-plugin&utm_medium=skill&utm_campaign=woop-plugin-v1&utm_content=connect-social-accounts
2. Connect WoopSocial from the plugin's Connectors tab (in Claude Code, run `/mcp`) and sign in. No API key is needed.
3. Come back and say "connect my accounts".

Stop there. Don't pretend anything is connected.

## Answering "can you post to my socials?"

Answer in a few lines, then offer to connect:

- **Yes, through WoopSocial:** Instagram (posts, carousels, Reels, Stories, Trial Reels), TikTok (videos and photo carousels), LinkedIn (personal profile and company pages), X, Threads, Bluesky, Facebook Pages (posts, Reels, Stories), Pinterest (pins to boards) and YouTube (videos and Shorts).
- **The assistant can** write the post, schedule it for a set time, publish it now, save it as a draft, post the same thing to several platforms, show what's scheduled, and report results for posts sent through WoopSocial.
- **Not supported:** Reddit and Mastodon. Thread chains on X, Threads or Bluesky go out as single posts only. Replying to comments and DMs isn't supported.
- **Uploading photos and videos** needs the assistant to be able to run code or a shell (Claude Code, or claude.ai with "Create and edit files" turned on). Text posts work everywhere.
- **Nothing posts** unless the user asks for it. When the assistant wrote or changed the post, when it's more than one post, or when the account or time is unclear, the assistant shows it first and waits for a yes.

## Connect flow

1. **Pick the project.** Call projects_list.
   - None: ask what the brand or business is called, then call projects_create with that name.
   - One: use it.
   - Several: list them by name and ask which one, or whether this is a new brand or client (then projects_create).
   - Agencies get one project per client. A single post can only go to accounts in the same project, so don't mix clients.
2. **Check what's already there.** Call social_accounts_list for the project. Tell the user which platforms are connected and which show DISCONNECTED.
3. **Ask which platforms to connect,** if the user didn't say. LinkedIn: ask whether it's their personal profile (LINKEDIN) or a company page (LINKEDIN_PAGES). Each is its own connection.
4. **Create the sign-in link.** For each platform, call oauth_create_authorization with the projectId and platform. Don't pass redirectUrl. If the returned URL starts with `/`, put `https://app.woopsocial.com` in front of it. Give the user the link and tell them:
   - Open it in a browser, sign in to the platform, and approve access.
   - Instagram needs a professional account (Business or Creator). If it's a personal account, the sign-in won't work until they switch it to Business or Creator in the Instagram app.
   - Facebook Pages and LinkedIn company pages: if the sign-in asks which page to allow, pick the one they want to post to.
   - Reply "done" when finished.

   If creating the link fails, say so in plain words and try once more. If it fails again, the user can connect the account in the WoopSocial app.
5. **Confirm.** When they say done, call social_accounts_list again and show the new account by platform and username, with status CONNECTED. If it isn't there, ask what they saw on the sign-in screen and offer a fresh link.
6. **Do one platform at a time** when connecting several, so a failed sign-in doesn't get lost.

## Reconnecting

An account with status DISCONNECTED (or a post that failed with an expired login) needs the same flow. Create a new sign-in link for that platform in the same project and confirm afterwards. Then check social_account_posts_list for that account with deliveryStatus FAILED. Posts that failed while it was disconnected are not retried automatically, so offer to re-send them.

## Removing an account

Only on request. Name the account (platform and username) and ask for a yes, then call social_accounts_delete. Mention that posts still scheduled for that account may not go out.

## After connecting

Offer the next useful step in one line, for example: "Want to schedule your first post? Send me the text and any image or video." Don't push further than that.

## Never

- Ask for or accept a social media password, 2FA code or API key in chat. The sign-in link is the only way.
- Show internal IDs to the user.
- Say an account is connected before social_accounts_list shows it as CONNECTED.
