---
name: instagram
description: Navigate and automate the Instagram Android app. Use when the task involves browsing profiles, liking posts, following accounts, searching users, or viewing stories/reels.
keywords: [instagram, insta, follow, like, post, story, reel, profile, feed, explore, comment, dm, message, search instagram]
platform: android
app_package: com.instagram.android
---

# Instagram App: Navigation & Automation

## App Launch
- Package: `com.instagram.android`
- Launch via verb: `launch({ app: "com.instagram.android", activity: ".activity.MainTabActivity" })`
  (or omit `activity` to dispatch the LAUNCHER intent).
- Cold start takes 3-5s; wait before interacting.
- The app opens to the Home feed by default.

## Bottom Navigation Tabs
Five tabs at the bottom of the screen:

| Tab | Position | Description |
|-----|----------|-------------|
| Home | 1 (left) | Feed with posts, stories, reels |
| Search & Explore | 2 | Search users/tags/places, explore grid |
| Create (+) | 3 (center) | Create new post, reel, story |
| Reels | 4 | Short video feed |
| Profile | 5 (right) | Your profile page |

## Search Flow
1. Tap the **Search & Explore** tab (magnifying glass icon, bottom nav position 2) via `tap_element({ index })`.
2. Tap the search bar at the top via `tap_element`.
3. Type the username or hashtag with `type({ text: "<query>" })`. Pass `clear: true` to wipe a stale query.
4. Press Enter via `key({ keyCode: 66 })` to submit.
5. Results appear in tabs: Top, Accounts, Audio, Tags, Places.
6. Tap the desired account or tag from results.

## Profile Page
- **Follower/Following counts** are tappable; they open the followers/following list.
- **Posts grid** shows below the bio. Tap a post thumbnail to open it.
- **Follow/Unfollow button** appears below the bio for other users' profiles.
- The profile header shows: username, profile pic, post count, followers count, following count, bio.

### Profile Grid Content Filtering
- Grid is ordered most-recent-first (top-left = latest).
- Accessibility labels identify type: `"Reel by..."`, `"Photo by..."`, `"N photos by..."` (carousel).
- If the task restricts to photos, filter the label before tapping; otherwise any type works.
- Like button behaves identically across all content types.

## Followers/Following List
- Accessed by tapping the follower or following count on a profile.
- Scrollable list of users with Follow/Following buttons.
- Each entry shows: profile pic, username, display name, Follow/Following button.
- For data tasks (e.g. “tell me the first 5 followers”), call `mark_page()` on each relevant followers-list screen after `get_ui_state()`. Do not design the final table schema inline; the completion verifier turns marked pages into normalized rows such as `username` and `display_name`.
- To scroll the list: `swipe({ startX: 540, startY: 1800, endX: 540, endY: 600, durationMs: 300 })`.

## Login Flow (credentials via `type_secret`)
When the task requires signing in, use the credential vault. NEVER type credential
values with `type()` and NEVER ask the human to paste one (see agent-guidelines →
Credentials). The available secret ids are listed in the CREDENTIALS section of your
system prompt (e.g. `instagram.username`, `instagram.password`). If no CREDENTIALS
section exists, the session has no vault: do not attempt login; call `request_human()`.

1. Launch the app: `launch({ app: "com.instagram.android" })`. If the login
   screen appears (username + password fields with a "Log in" button), proceed;
   if you land on the Home feed you are already logged in.
2. Observe the screen: the login form fields carry `[N]` markers in the UI state.
3. Type the username by id (taps + focuses the field, then types on-device):
   `type_secret({ secret_id: "instagram.username", index: <username-field-index>, clear: true })`
4. Type the password the same way:
   `type_secret({ secret_id: "instagram.password", index: <password-field-index>, clear: true })`
5. Tap the **Log in** button via `tap_element`.
6. Expect post-login interstitials ("Save your login info?", "Turn on notifications"):
   dismiss with "Not now" / `key({key:"back"})` per Common Pitfalls below.

Notes:
- You never see the credential values; `type_secret` resolves them in the harness
  and returns only `{ ok, secret_id, index }`. Refer to credentials by id everywhere
  (progress cells, done() rows included).
- An unknown `secret_id` returns an error listing the available ids; retry with one
  of those; do not fall back to `type()` with a guessed value.
- 2FA prompts are out of scope for the vault flow: call `request_human()` if one appears.

## Feed & Posts
- Posts show: username, image/video, like button (heart), comment button, share button, save button.
- **Like button**: heart icon below the post image. Tap to like/unlike.
- **Double-tap** on the post image also likes it (but use the heart button for reliability; double-tap timing is tricky via ADB).
- Like count and caption appear below the action buttons.
- Comments link shows "View all N comments"; tap to open comments.

### Accessing Likers List on a Post
**Critical**: The "Liked by [username] and others" TEXT is NOT the element that opens the full list.

- Tapping the text → navigates to that single user's profile (dead end).
- Tapping the **"User avatars"** ViewGroup (small profile circles positioned LEFT of the "Liked by" text) → opens the full likers bottom sheet.
- Target element pattern: `<ViewGroup /> "User avatars"` immediately preceding the `TextView "Liked by..."`.
- The bottom sheet (`layout_container_bottom_sheet`, title "Likes") contains the scrollable list with `row_user_imageview` entries.

## Stories
- Story circles appear at the top of the Home feed.
- Tapping a story circle opens the story viewer.
- In story viewer: tap right half to advance, left half to go back, swipe right to skip to next user's story.
- Stories auto-advance after a few seconds.

## Accessibility Notes
- Instagram on Android has **some unlabeled buttons**. The Like/Unlike button in the Activity feed (notifications) is often unlabeled.
- Posts and reels in the feed may not be easily distinguishable by touch; the accessibility tree groups them.
- The heart (like) icon typically has content description "Like" or "Unlike" depending on state.
- Follow/Unfollow buttons have clear text labels.

## Common Pitfalls
- **Popups**: Instagram may show notification permission prompts, "Turn on Notifications" modals, or "Add to Home Screen" prompts. Dismiss with `key({key:"back"})` or tap "Not Now" / "Skip" via `tap_element`.
- **Login walls**: Some actions require being logged in. If a login screen appears, the task may be blocked: use `request_human()`.
- **Rate limiting**: Rapid likes, follows, or comments may trigger Instagram's anti-automation detection. Pace actions with natural delays.
- **Reels auto-play**: Navigating to the Reels tab starts video playback. The accessibility tree may change rapidly. Navigate away if reels are not the target.
- **Keyboard covering elements**: After typing in search, the keyboard may cover results. Dismiss keyboard with `key({key:"back"})` if needed, or scroll.
- **Private profiles**: Detect via `row_profile_header_empty_profile_notice_title` = "This account is private". Posts are inaccessible without following, so engagement tasks will fail. Skip and move to the next candidate; track skipped users in memory to avoid retrying.

## Engagement Tasks (Liking Posts)
- Navigate to a user's profile via search.
- Scroll their post grid and tap a post thumbnail to open it via `tap_element`.
- Tap the heart icon (Like button) to like the post.
- Use `key({key:"back"})` to return to the profile grid.
- Track progress in memory: which users were visited, how many posts liked per user.

### Like Confirmation Signal
- Like button is `<Button id="row_feed_button_like" />`.
- Content description toggles: `"Like"` → `"Unlike"` after a successful tap.
- Re-query UI state after tapping to confirm the state change registered.

### Navigation Depth: Likers List → Like → Return
When liking posts sourced from a post's likers list, it takes **2 back presses** to return to the likers bottom sheet:
1. Post view → user's profile
2. Profile → likers bottom sheet (still open on the original post)

## Timing Guidelines
| Action | Expected Wait |
|--------|--------------|
| App cold start | 3-5s |
| Search results load | 1-2s |
| Profile page load | 1-2s |
| Post open | 1s |
| Story load | 1-2s |
| Page scroll settle | 500ms |
