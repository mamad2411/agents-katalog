---
description: Angelia project conventions — mirrors .github/copilot-instructions.md
alwaysApply: true
---

> Canonical source: `.github/copilot-instructions.md` — when updating conventions, edit both files.

# Copilot Instructions

## App tone

Angelia is a warm, playful, and encouraging app. All user-facing copy — placeholders, labels, empty states, toasts, and prompts — should reflect that energy. Avoid formal, corporate, or overly serious language. Write like a friendly, enthusiastic teammate.

## Terminology

- Use **"Circle"** instead of "Channel" in all user-facing text.
  - "Daily Channel" → **"Daily Circle"**
  - "Custom Channel" → **"Custom Circle"**
- Use **"Host"** instead of "Owner" when referring to the person who created a Circle.
- Use **"Member"** instead of "Subscriber" when referring to people who have joined a Circle.
- Internal code identifiers (variable names, Redux slices, Firestore collections, etc.) remain unchanged — only UI-facing strings change.

## Circle badges

- Daily circles already include the word "Daily" in their badge text (the circle name itself contains "Daily").
  **Never** add a separate "Daily" label next to the badge — it is redundant.

## Daily circle display names

- Every user has exactly one daily circle, and its `name` is always `"Daily"` — showing it is meaningless.
- Wherever a daily circle's name would be displayed to the user (filter lists, pickers, labels, etc.), show the **owner's name** instead, formatted as `"FirstName L."` (first name + last initial + period).
- To resolve the owner, look up `channel.ownerId` in the users map (e.g. `selectAllUsersMapById` from `usersSlice`).
- The same rule applies to search/filter logic: match against the owner name, not the literal string `"Daily"`.

---

## Firestore indexes (`firestore.indexes.json`)

`firestore.indexes.json` is the source of truth for composite Firestore indexes. Any query that combines filters on **two or more different fields** (including `in` with a second equality/inequality filter) requires a composite index. Missing indexes cause queries to fail silently on the client — the `onSnapshot` callback simply never fires.

**Keep `firestore.indexes.json` up to date whenever:**
- A new collection query is added in `src/services/firebase/firestore.ts` that uses more than one `where()` clause on different fields.
- An existing query gains a new filter.
- A query is removed (remove its index entry to keep the file clean).

**Current required indexes:**
| Collection | Fields | Reason |
|---|---|---|
| `posts` | `channelId ASC`, `markedForDeletionAt ASC` | `subscribeToPosts` uses `in` + `== null` |
| `connectionRequests` | `fromId ASC`, `toId ASC`, `status ASC` | `getExistingConnectionRequest` uses three filters |
| `channels` | `inviteCode ASC`, `markedForDeletionAt ASC` | `getChannelByInviteCode` uses two filters |

After updating `firestore.indexes.json`, deploy with:
```bash
npm run deploy:indexes
```

---

## Firestore field conventions

- **Never** use TypeScript optional (`?`) for fields that are stored in Firestore documents. Instead, use `| null` for nullable fields. Firestore does not natively support `undefined`, and optional fields can lead to subtle bugs or missing fields in documents.
  - ✅ `note: string | null`
  - ❌ `note?: string`
- Always provide an explicit value (including `null`) when writing documents, so the field is always present in Firestore.

### Firestore subscription snapshots

- Treat every `onSnapshot` callback parameter as potentially nullable in React Native Firebase. Do **not** assume query listeners always receive a non-null snapshot.
- For collection/query listeners, never access `snap.docs` directly. Always read documents via a null-safe fallback such as `snap?.docs ?? []` or a shared helper in `src/services/firebase/firestore.ts`.
- For document listeners, guard `snap` before reading `exists` or `data`. If a null snapshot arrives transiently, preserve the previous local state or return early rather than throwing.
- When adding a new Firestore subscription, include an error callback whenever the caller has a sensible fallback state (`[]`, `null`, or previously cached data). Subscription callbacks must fail closed, not crash the app.

---

## Cloud Functions type sync

The notification types in `functions/src/index.ts` (the Cloud Functions entry point) mirror the types in `src/models/types.ts`. These **must be kept in sync** whenever notification types change.

Specifically, the following must always match between the two files:
- `AppNotificationType` union values
- `NotificationTarget` discriminated union shape
- `BaseAppNotification` fields (`actorId`, `target`, `createdAt`, `id`, `type`)
- Each per-notification-type interface (e.g. `JoinChannelRequestNotification`)
- Domain model interfaces used by Cloud Functions (e.g. `ConnectionRequest`, `ChannelJoinRequest`)

When adding a new notification type:
1. Add it to `AppNotificationType` in both files.
2. Add the corresponding interface in both files.
3. Add a `buildFcmPayload` branch in `functions/src/index.ts`.
4. Add a foreground toast handler in `src/components/DataListenerWrapper.tsx` (Effect 9).
5. Add a tap-routing branch in `src/app/_layout.tsx`.
6. **Add a Firestore test example to `NOTIFICATION_TESTING.md`** (Scenario C, D, etc.) so the notification can be manually tested without a real device action.

---

## Cross-slice selectors (`src/store/crossSelectors/`)

Selectors that need to read from **more than one Redux slice** live in
`src/store/crossSelectors/`. Do **not** put cross-slice selectors directly in
individual slice files — they create circular-import risks and make it harder to
discover shared logic.

Conventions:
- One file per domain concern, named `<domain>Selectors.ts`
  (e.g. `activitySelectors.ts`, `myPeopleSelectors.ts`).
- Use RTK `createSelector` for memoisation.
- Import the file directly from `@/store/crossSelectors/<file>` — do not create
  a barrel `index.ts` unless the directory grows large enough to warrant one.

Current files:
| File | Exports | Purpose |
|---|---|---|
| `activitySelectors.ts` | `selectHasAnyPendingActivity` | `true` when user has any pending circle join request OR connection request — drives the bell badge in the feed header |
| `myPeopleSelectors.ts` | `selectMyPeopleData` | Derives a `people` array of `{ user, inCircle }` entries for the My People screen. `inCircle` is `true` when the person also shares a circle with the current user. |

---

## Safe area insets & demo-mode header gap

### Bottom insets
Always use `useSafeAreaInsets()` to account for home-bar / system-navigation-bar height.
- For `ScrollView`, apply the inset to `contentContainerStyle`:
  ```tsx
  contentContainerStyle={{ paddingBottom: insets.bottom + 24 }}
  ```
- For fixed `View` containers, apply it inline:
  ```tsx
  style={{ paddingBottom: insets.bottom + 24 }}
  ```
- **Never** use a flat pixel constant for bottom padding — it will clip content on devices with a home bar or soft navigation buttons.
- Prefer `ScrollView` over a plain `View` for any screen whose content could exceed the viewport, so users can always reach every button/action.

### Demo-mode header gap

In demo mode the `DemoModeBanner` is rendered **above** the `Stack` navigator in `_layout.tsx`, consuming the status-bar area. Expo Router uses `@react-navigation/native-stack` (NativeStack), which reads `useSafeAreaInsets().top` internally — meaning any NativeStack-managed header would double-count that gap.

**The fix: always use `headerShown: false` + `<ScreenHeader>` for any screen that needs a back button or title.**

> ⚠️ **Do NOT use NativeStack's built-in header** (`headerShown: true`) for screens inside this layout. NativeStack ignores `headerStatusBarHeight` (a JS Stack-only prop) and always adds its own top-inset padding regardless.
> ⚠️ **Do NOT use `SafeAreaInsetsContext.Provider`** to override top insets for the Stack — it does not work with NativeStack.

**`ScreenHeader` component** lives at `src/components/ScreenHeader.tsx`:
```tsx
<ScreenHeader title="My Screen" />
// Optional props:
// showBack?: boolean  (default: true)
// onBack?: () => void (default: router.back())
```
It reads `isDemo` from Redux and handles `paddingTop` automatically:
- demo mode → `paddingTop: 10`
- normal → `paddingTop: insets.top + 10`

**Pattern for screens with a header:**
```tsx
// In _layout.tsx:
<Stack.Screen name="my-screen" options={{ headerShown: false }} />

// In my-screen.tsx:
return (
  <View style={{ flex: 1 }}>
    <ScreenHeader title="My Screen" />
    {/* rest of content, e.g. ScrollView or KeyboardAvoidingView */}
  </View>
);
```

Place `<ScreenHeader>` **outside** any `<KeyboardAvoidingView>` so the existing `KEYBOARD_VERTICAL_OFFSET = 90` constant remains valid (the header height approximately matches the old native header height).

For screens that use a fully custom animated header (e.g. `conversation.tsx`), handle `paddingTop` manually: `paddingTop: isDemo ? 10 : insets.top + 10`.

---

## User Avatar (`user` prop)

The `Avatar` component accepts a `user` prop (`Pick<User, 'avatar' | 'avatarUrl'> | null`) that automatically resolves both the preset emoji and any custom profile photo. When `user` is provided, `preset` and `uri` are ignored.

**Always pass `user={user}` whenever rendering an Avatar for a specific user**, including:
- Post detail screens (the post author's avatar)
- Conversation / chat headers
- Profile cards and modals
- The share-connection screen (current user's avatar)
- Any other screen that shows a user's identity

```tsx
// ✅ correct — automatically uses avatarUrl if set, falls back to avatar preset
<Avatar user={user} size="md" />

// ❌ old pattern — do not use for User objects
<Avatar preset={user.avatar} uri={user.avatarUrl} size="md" />
```

The individual `preset` and `uri` props are only for non-User contexts, such as avatar edit previews (e.g. `AccountTab`, `complete-profile.tsx`) where the values come from local state rather than a `User` object.

### Status badge visibility (`showStatus` prop)

`Avatar` renders the user's active status emoji as a badge by default (`showStatus` defaults to `true`). Pass `showStatus={false}` to suppress the badge in contexts where the status icon would be distracting or irrelevant.

**Always use `showStatus={false}` in:**
- The account/profile tab (the user's own avatar at the top)
- Connection request screens
- Join request screens
- Invite screens
- Share-connection screen
- My People list
- Notifications list
- Channel member lists / channel cards
- Private notes screens (both host and sender views)

**Leave `showStatus` at its default (`true`) in:**
- Feed posts (post author avatar)
- Conversation / chat message avatars
- User profile modal

```tsx
// ✅ feed / conversation — status badge visible
<Avatar user={author} size="sm" />

// ✅ utility / action screens — status badge hidden
<Avatar user={requester} size="md" showStatus={false} />
```

---

## Keeping docs up to date
### Repo-wide investigation docs (`/docs`)

All implementation and investigation writeups belong in the repo's central `/docs` folder. For current investigations, store documents under `/docs/YYYY/MM/DD/` so they are easy to find by date and context.

**Store docs this way when you create or archive a troubleshooting writeup:**
- `/docs/2026/06/04/INVESTIGATION_REPORT_daily_circle_post_missing.md`
- `/docs/2026/06/04/TROUBLESHOOTING_GUIDE_daily_circle_post_missing.md`
- `/docs/2026/06/04/QUICK_REFERENCE_daily_circle_post_missing.md`
- `/docs/2026/06/04/INVESTIGATION_DIAGRAMS_daily_circle_post_missing.md`

This keeps implementation notes, root-cause reports, and quick references centralized and organized by date.

### Feature implementation docs (`/docs/YYYY/MM/DD/`)

When a feature branch adds or changes user-facing behavior, data models, or Cloud Function flows, **also add a dated feature doc** under `/docs/YYYY/MM/DD/` (same date folder convention as investigations). This is the durable reference for maintainers — separate from the branch-scoped `BRANCH_NARRATIVE.md` and `TESTING.md` in `apps/mobile/`.

**Create or update a feature doc when you ship:**
- A new Firestore collection or subcollection shape
- A new notification / inbox type or surface-routing rule
- A new screen workflow or filter that affects how users find content
- Any cross-cutting refactor (listeners, selectors, mark-read rules)

**Suggested filename:** `FEATURE_NAME.md` in SCREAMING_SNAKE or descriptive kebab, e.g.:
- `/docs/2026/06/08/PRIVATE_NOTE_CONVERSATIONS.md`
- `/docs/2026/06/08/ACTIVITY_EXPIRY_INBOX.md`

**Include:** overview table, data model, access rules / surface routing, client file map, deploy steps, manual test steps, and links to `BRANCH_NARRATIVE.md` / `TESTING.md`.

**⚠️ CRITICAL:** Before marking a user-facing branch task complete, verify the `/docs` feature doc exists (or is updated) alongside `BETA_UPDATE_NOTES.txt`, `BRANCH_NARRATIVE.md`, and `TESTING.md`.

### App-specific docs (`apps/mobile/docs/`)

`apps/mobile/docs/` holds mobile-app references that are not tied to a single feature date:
- `release-process.md` — production release checklist
- `ota-modals.md` — Firestore-driven feed modals

Update these when release workflow or modal behavior changes.

### OTA / server-side feed modals (`apps/mobile/docs/ota-modals.md`)

`apps/mobile/docs/ota-modals.md` is the reference for all three Firestore-driven feed modals (app version update, broadcast message, feedback form). **Update it whenever:**

- A Firestore field is added, renamed, or removed from `appConfig/mobile`.
- A new modal type or priority level is added to `useFeedModals` (`src/hooks/useFeedModals.ts`).
- The dismissal logic for any modal changes (new or renamed AsyncStorage key).
- The `broadcastMessage` type → emoji / accent color mapping changes.
- The iOS or Android update destination changes (TestFlight → App Store, etc.).

Update the relevant section in the doc — the Firestore field table, behavior notes, and "To show / stop showing" instructions.

### BetaUpdateModal (`src/components/BetaUpdateModal.tsx`)

`BetaUpdateModal` displays a one-time "what's new" modal to beta testers when a new update is pushed. **Update it whenever:**

- A **user-visible bug fix, improvement, or new feature** ships that beta testers should be aware of.
- Changes that are mostly internal (cleanup, refactors, behind-the-scenes reliability work) should usually be grouped into one general bug-fix line, not listed as separate highlights.

**How to update:**

1. **Bump `BETA_UPDATE_VERSION`** to a new string (e.g. `"1.1.0"` or a date like `"2026-06-01"`). This is the only thing required to make the modal show again for all users — the AsyncStorage key is derived from this version string.
2. **Update `BETA_UPDATE_TITLE`** if a new headline fits better (optional).
3. **Replace `BETA_UPDATE_CHANGES`** with the current list of changes. Each entry has:
   - `emoji` — a single emoji that represents the change type
   - `title` — a short, friendly headline (max ~6 words)
   - `description` — (optional) one sentence elaborating on the change

**Keep the list to 5 entries maximum.** Focus on the most impactful user-facing changes. Minor improvements and multiple bug fixes should be collapsed into a single `{ emoji: '🐛', title: 'Bug fixes & reliability', description: '...' }` entry rather than listed individually. If you have more than 5 things, cut the least impactful ones — users don't need to be told about every tweak.

Only call out a bug or improvement as its own entry when users can clearly feel it in day-to-day use. If the work is mostly background behavior tuning, keep it under a single bug-fixes summary unless it was a serious incident users would care about directly.

Keep the tone warm and encouraging — avoid dry or technical language. Write like you're texting a friend about something cool.

```ts
// Example entry
{ emoji: '🐛', title: 'Bug fixes & stability', description: 'A few rough edges smoothed out.' }
```

**Never** show the modal in demo mode (`isDemo` guard is already in place).

### Beta update notes (`apps/mobile/BETA_UPDATE_NOTES.txt`)

Keep `apps/mobile/BETA_UPDATE_NOTES.txt` current while working on feature branches that change user-facing behavior.

Use it as the compact source of truth for the next beta update modal:
- Keep it brief, but include the meaningful user-visible changes from the branch or PR.
- Update it whenever a branch lands bug fixes, workflow changes, or new features that beta testers should know about.
- Write the entries in the same warm, friendly tone used in the app modal copy.
- Include the current branch or PR reference at the top so the next update is easy to trace.
- If the `Branch` / `Related PR` header does not match the current branch or PR, clear `Current branch highlights` before adding new bullets. Never carry over highlights from a previous branch.

**⚠️ CRITICAL: You MUST update `apps/mobile/BETA_UPDATE_NOTES.txt` before marking any task complete if it involves:**
- A new screen, feature, or user-visible workflow
- A new control (button, toggle, sort/filter option) that changes how users interact with data
- A bug fix that users would notice (visual issues, missing features, broken functionality)
- A change to existing UI, labels, or copy
- Any change that would appear in a "what's new" list
- Any enhancement that significantly impacts user experience

**This is mandatory, not optional.** Before ending your work on any user-visible task:
1. ✅ Make all code changes
2. ✅ **Update `BETA_UPDATE_NOTES.txt` with a user-friendly bullet** describing what changed
3. ✅ Confirm both files are committed together

If you forget to update the beta notes after making user-facing changes, the task is not complete. Add a bullet under "Current branch highlights" in plain, warm, friendly language that explains the benefit to users (not just what was changed).

### Version release notes (`/versions`)

Create plain text release note files in the repo root `versions/` folder for every production release. Name the file with the semantic version exactly as it appears in `app.config.js`, for example `versions/1.0.1.txt`.

Each file should be simple text and list the release updates, improvements, and bug fixes as short bullets. This is the release-specific changelog for the version and is separate from `apps/mobile/BETA_UPDATE_NOTES.txt`, which is branch/beta-focused.

Example:

```
Branch: release/1.0.1
- Bug fixes & reliability improvements for Daily Circle feed sync
- Updated release alert behavior
- Minor onboarding copy polish
```

Keep the file and version name aligned with `app.config.js` and `src/models/constants.ts`.

### Notifications release notice area (`src/app/(protected)/notifications.tsx`)

The top callout area in the Notifications screen is a **release-scoped, one-time notice area** for new notification controls.

- It is **not** a permanent shortcut row for Daily Reminders.
- Use this area to announce newly available notification controls (for example, new post activity toggles).
- Visibility is versioned by:
  - `NOTIFICATION_SETTINGS_NOTICE_VERSION`
  - `NOTIFICATION_SETTINGS_NOTICE_SEEN_KEY(version)`
  - `NOTIFICATION_SETTINGS_NOTICE_BADGE_SEEN_KEY(version)`
  in `src/models/constants.ts`.
- The notice card should be dismissed **only after the user actually opens** Notification Settings (`/(protected)/notification-settings`), not merely when the card is rendered.
- The feed bell's release-notice dot should clear once the user visits Notifications (`/(protected)/notifications`), even if the notice card still shows.
- When a new notification-control release ships, bump the notice version and refresh the card copy.

---

### APP_STORE_LISTING.txt

`APP_STORE_LISTING.txt` (repo root) is the source of truth for app store copy — short description, full description, keywords, and reviewer notes. **Keep the full description up to date whenever:**

- A **new core feature** is added or shipped (e.g. new circle type, reactions, scheduling).
- An **existing feature is removed or significantly changed** — remove or reword the relevant bullet.
- The **value proposition or positioning changes** (e.g. new target audience, new differentiator).
- A **policy URL changes** (privacy policy, data deletion page).

When updating, preserve the casual, warm, and welcoming tone. Write like a friendly teammate explaining the app — avoid corporate or formal language. Lead with the user's problem, not the feature list.

Do **not** update it for bug fixes, UI tweaks, refactors, or minor additions that don't change what the product does or how it's described to new users.

After editing, update the `Last updated` date at the top of the file.

---

### PRODUCT_SUMMARY.md

`PRODUCT_SUMMARY.md` is the canonical product overview. Keep it current when:

- A **new core feature** is added or an existing one is significantly changed (e.g. new circle type, new post tier, new notification type).
- The **tech stack** changes (new major dependency, Firebase service, or platform support).
- A **key differentiator** no longer applies or a new one emerges.

Do **not** update it for routine bug fixes, refactors, UI tweaks, or minor additions that don't change what the product fundamentally is or does.

### README.md

`README.md` is the developer reference. Keep it current when:

- An **npm script** is added, removed, or its behavior meaningfully changes — update the *npm Scripts Reference* table.
- The **project structure** changes significantly (new top-level `src/` directory, major reorganization).
- A **new prerequisite** is required for local development.
- A **tricky bug** is found and resolved — add an entry to the *Known Bugs & Solutions* section describing the symptom, root cause, and fix with a file reference. Keep entries factual and concise.

Do **not** clutter the README with:
- Every minor dependency update
- Internal implementation details that don't affect the dev workflow
- Speculative or forward-looking notes

### Branch Narrative (`BRANCH_NARRATIVE.md`)

**For every feature branch that adds user-facing functionality or significant changes, create a `BRANCH_NARRATIVE.md` file** in `apps/mobile/`. This file tells the story of what changed, why it changed, and how it technically works — all for the PR reviewer.

**Purpose:** Reviewers should be able to read the file once and understand:
- The user problem each feature solves
- The solution (UX & workflow)
- Technical implementation details for that feature
- Cross-cutting changes (data flow, selectors, types)
- What files changed and why
- Testing checklist

**Structure:**

1. **Story Overview** — 2–3 sentences about the theme and user intent
2. **Feature 1–N sections** — One per major change:
   - **The Problem** — user-facing pain point
   - **The Solution** — what changed (UX/workflow)
   - **Technical Detail** — files, key code changes, why (with `[file links](path)`)
3. **Cross-Cutting Changes** — Redux, data flow, type safety changes shared across multiple features
4. **User-Facing Impact** — table of features, benefits, where they appear
5. **Testing Checklist** — manual QA steps
6. **Files Changed** — table with line counts and purposes
7. **Summary** — recap for users, code maintainers, and experience

**When to create:**
- Any branch that adds a new screen, feature, or workflow
- Any branch that changes existing UI, controls, or copy
- Any branch that touches critical data flow, selectors, or type structures
- Do **not** create for bug fixes, refactors, or internal cleanup (unless the PR is large and complex)

**Tone & Audience:**
- Write for a code reviewer who needs both story context and technical detail
- Mix narrative ("Alice wants to...") with technical specifics ("added compareReactionGroupPriority in reaction.utils.ts")
- Include file links so reviewers can jump to implementation
- Explain **why** changes matter, not just what they do

**Example intro to a feature:**

> **The Problem:** Bob sees 🎉 at the top on the feed, but when he opens the post details, he sees ❤️ first.  
> **The Solution:** All reactions now sort by count → oldest timestamp → emoji strength → lexicographic, everywhere.  
> **Technical Detail:**
> - File: [reaction.utils.ts](../src/services/utils/reaction.utils.ts) (new shared comparator)
> - Key Changes: Added `compareReactionGroupPriority()`, `EMOJI_STRENGTH_ORDER`, new `ReactionGroupPriorityEntry` interface
> - Used by: post/[id].tsx, PostCard.tsx, ...

**Before submitting a PR, ensure:**
- ✅ `BRANCH_NARRATIVE.md` created with all six sections
- ✅ All file links use workspace-relative paths and work
- ✅ Testing checklist is concrete and manual-QA–friendly
- ✅ Files Changed table matches actual git diff
- ✅ Tone is warm and story-driven, not dry

**After merging:**
- Archive the branch narrative (paste it into a release notes doc or wiki)
- Delete the file from `main` to keep the repo clean

---

### Testing Document (`TESTING.md`)

**For every feature branch that has a `BRANCH_NARRATIVE.md`, also create and maintain a `TESTING.md` file** in `apps/mobile/`. This is the manual QA guide for the developer to verify every feature before merging.

**Purpose:** The developer reads this file, then systematically checks every feature on device. Reviewers can also use it to confirm what was tested.

**Device setup context** (always include at the top):
- **Primary:** Android — used for all standard testing
- **Secondary:** iPhone — used only when:
  - Two different user accounts are needed simultaneously
  - The feature likely behaves differently on iOS (pickers, keyboard, safe area, haptics)
  - Confirming a fix works on both platforms

**Structure:**

1. **Before You Start Testing** — a section near the top that tells the tester what to run before their first test session:
   - `npm install` (always)
   - `npm run env:pull` (after clone or env changes)
   - Whether a prebuild + native build is needed for this branch (list the commands)
   - A quick sanity check: app launches cleanly, no Metro errors
   - **Update this section whenever a new native package is added to the branch.** If the branch adds a dependency that requires a prebuild (i.e. any package with native code, a new Expo plugin, or a change to `app.config.js`), explicitly call it out here so testers know to re-run prebuild before testing.
2. **Device Setup** — brief section with Android/iPhone guidance and when to use each
3. **Feature 1–N sections** — one per feature from the Branch Narrative:
   - **Devices:** which to test on, and when to involve the iPhone
   - **Setup** — any state/data that needs to exist before testing
   - **Checklist** — concrete checkbox steps a person can follow on a real device
   - **Edge cases** — boundary conditions, unusual inputs, stress cases
3. **Regression Checks** — a final section of quick checks to confirm nothing pre-existing broke
4. **Known Limitations / Notes** — anything that is intentionally deferred, partially implemented, or needs follow-up

**Conventions:**
- All checklist items start with `- [ ]` so they can be mentally checked off while testing
- Steps are written as actions + expected outcomes: "Tap X → Y happens"
- Be specific: "Tap the 📝 badge" is better than "Open the caption modal"
- List the Android steps first; add an iPhone section only when behavior differs

**Keep it current:** Update `TESTING.md` whenever new features are added to the branch or when a bug is found during testing that reveals a gap in the checklist.

**Edit-safety rules for existing `TESTING.md`:**
- Default to **additive updates**: append a new `Feature N` section for new work.
- **Do not delete or replace** existing feature sections/checklists unless the user explicitly asks.
- **Do not rename** the testing guide title unless the user explicitly asks.
- Preserve the existing section format (`Devices`, `Setup`, `Android`, optional `iPhone`) when adding new feature sections.
- If the user asks to "add testing" for current work, add a new feature section in the existing format; do not create ad-hoc standalone sections.

**⚠️ CRITICAL: Before marking any user-facing branch task complete, verify `TESTING.md` is updated for the current branch.**

Required final check before completion:
- Confirm active branch name via git (`git rev-parse --abbrev-ref HEAD`) before editing `TESTING.md`
- Confirm `**Branch:**` in `TESTING.md` matches the active feature branch name
- Confirm feature sections in `TESTING.md` match the current `BRANCH_NARRATIVE.md`
- If branch detection is unavailable or ambiguous, ask the user for the branch name before editing `TESTING.md`
- If either is stale, update `TESTING.md` first, then mark the task complete

**Before submitting a PR, ensure:**
- ✅ `TESTING.md` exists and covers every feature in `BRANCH_NARRATIVE.md`
- ✅ Regression checklist is present
- ✅ Device guidance is clear (Android vs iPhone, when to use each)
- ✅ All checklist items are actionable on a real device (no vague "confirm it works")

---

## Confirming destructive actions

Any user-initiated action that is **irreversible or has significant consequences** must be confirmed with `useActionModal`'s `confirm()` before proceeding. Pass `destructive: true` so the confirm button renders in a destructive (red) style.

Actions that always require confirmation:
- **Disconnecting from a user** — removing a mutual connection (e.g. `disconnectUser`)
- **Leaving a circle** — unsubscribing from a custom circle (e.g. `unsubscribeFromChannel`)
- **Removing a member from a circle** — kicking a subscriber out of a custom circle (e.g. `removeChannelSubscriber`)
- **Deleting a circle** — permanently deleting a channel and all its posts (e.g. `deleteCustomChannel`)
- **Any other action that deletes or permanently removes data**

Pattern:
```tsx
const { confirm } = useActionModal();

const handleDestructiveAction = async () => {
  const ok = await confirm({
    title: 'Short title',
    message: 'One sentence explaining what will happen.',
    destructive: true,
  });
  if (!ok) return;
  // proceed with the action
};
```

**Never** perform a destructive action without first awaiting `confirm()`. If `confirm` is not yet imported in the file, add `useActionModal` from `@/hooks/useActionModal`.

---

## Code style conventions

### AsyncStorage keys

All `@angelia/…` AsyncStorage keys **must** be declared once as named exports in `src/models/constants.ts` and imported wherever they are used. Never define the same key string in more than one file. If a key is parameterised (e.g. per-post), export it as a function:

```ts
// ✅ correct — declared once, exported, imported elsewhere
export const PRIVATE_NOTES_SEEN_KEY = (postId: string) => `@angelia/private_notes_seen_${postId}`;

// ❌ wrong — local constant repeated across files
const PRIVATE_NOTES_SEEN_KEY = (postId: string) => `@angelia/private_notes_seen_${postId}`;
```

### `Number()` vs `parseInt`

Always use `Number()` to convert strings to numbers. Never use `parseInt` or `parseFloat`:

```ts
// ✅
const lastSeen = val ? Number(val) : 0;

// ❌
const lastSeen = val ? parseInt(val, 10) : 0;
```

### Arrow function return values

Arrow functions must always use an **explicit `return`** statement inside a block body `{ }`. Do not rely on implicit expression returns:

```ts
// ✅
allNotes.filter((n) => { return n.authorId === uid; })

// ❌
allNotes.filter((n) => n.authorId === uid)
```

This applies to all callbacks, `filter`, `map`, `find`, `sort`, etc.

### Icon + emoji: no duplicates

When a UI element already uses a vector icon (e.g. `<Feather name='mail' />`), do **not** also append a redundant emoji (e.g. `💌`) to the adjacent label. The icon and the emoji convey the same meaning — showing both is visually noisy.

```tsx
// ✅ icon-only with clean label
<Feather name='mail' size={15} color={theme.primary} />
<Text>or send {name} a private note</Text>

// ❌ icon + emoji duplicate
<Feather name='mail' size={15} color={theme.primary} />
<Text>Send {name} a private note 💌</Text>
```

### React Native: bottom-sheet modal keyboard handling

**Always use `ModalKeyboardView` + `useModalSheetPadding`** for any bottom-sheet `<Modal>` that contains a `TextInput`. These two exports live in `src/components/ModalKeyboardView.tsx` and centralise the cross-platform keyboard-avoidance pattern.

**Why a custom component instead of `KeyboardAvoidingView` alone:**

- **iOS:** `KeyboardAvoidingView behavior='padding'` works correctly inside a Modal and is used by `ModalKeyboardView` internally.
- **Android:** `KeyboardAvoidingView` inside a Modal is unreliable. The Modal is rendered outside the normal layout tree, so Android's `adjustPan`/`adjustResize` window soft-input modes don't apply. KAV's `paddingBottom` may leave a permanent gap below the sheet after the keyboard dismisses. The fix is to bypass KAV on Android entirely and instead track keyboard height via `Keyboard` event listeners (`keyboardDidShow` / `keyboardDidHide`), then apply it as `paddingBottom` on the sheet itself.

**Usage pattern:**

```tsx
import { ModalKeyboardView, useModalSheetPadding } from '@/components/ModalKeyboardView';

// Inside the component:
const sheetBottomPadding = useModalSheetPadding(insets.bottom + 16);

return (
  <Modal visible={visible} transparent animationType='slide'>
    <ModalKeyboardView>
      <Pressable style={styles.backdrop} onPress={onClose}>
        <View style={[styles.sheet, { paddingBottom: sheetBottomPadding }]}>
          {/* sheet content */}
        </View>
      </Pressable>
    </ModalKeyboardView>
  </Modal>
);
```

See `src/components/PrivateNoteModal.tsx` and `src/components/FeedbackSupportModal.tsx` for canonical implementations.

---

## React Native: Known Issues & Solutions

> **Policy:** Whenever a React Native-specific bug is encountered and resolved during development, add an entry here. Include the symptom, root cause, and fix with a file reference. This section is intentionally self-contained so it can be copied between React Native projects.

### Button text clipped when parent has `alignItems: 'center'`

**Symptom:** A `Button`'s label is truncated/clipped mid-word when the button sits inside a container that has `alignItems: 'center'` (e.g. a `Card` with `alignItems: 'center'`, or a column flex container).

**Root cause:** The `Pressable` inside `Button` has `flexDirection: 'row'`. In a row flex container, a `Text` without `flex: 1` sizes to its intrinsic single-line width and can overflow the container, getting clipped by the Pressable's bounds. This is a well-known React Native gotcha — text inside a `flexDirection: 'row'` View does not automatically wrap unless the Text node has `flex: 1`.

**Fix:** Do **not** add `flex: 1` to the shared `Button` `text` or `button` styles — this causes regressions in other layouts. Instead, pass `textStyle={{ flex: 1 }}` directly on the specific `<Button>` instance whose label needs to wrap. This puts `flex: 1` on the `Text` node only, making it fill the row container so long labels wrap instead of overflow.

```tsx
// ✅ targeted fix — flex: 1 on the Text node allows wrapping
<Button variant="outline" textStyle={{ flex: 1 }} onPress={...}>
  🛟 Get Help & Feedback
</Button>

// ❌ do not add flex/alignSelf to the shared Button stylesheet
```

---

### Keyboard gap / flicker below a bottom-sheet Modal (Android)

**Symptom:** After a `TextInput` inside a bottom-sheet `<Modal>` is used and the keyboard is dismissed, a visible gap appears between the bottom of the modal sheet and the bottom of the screen. Earlier versions of the same bug caused the sheet to flicker or jump.

**Root cause:** On Android, `<Modal>` renders outside the normal React Native view hierarchy. This means Android's `windowSoftInputMode` (`adjustPan` / `adjustResize`) does not apply, and `KeyboardAvoidingView`'s internal `paddingBottom` can get stuck at a non-zero value after the keyboard hides — producing either a jump (with `behavior='height'`) or a residual gap (with `behavior='padding'`).

**Fix:** Bypass `KeyboardAvoidingView` on Android entirely. Use `Keyboard.addListener('keyboardDidShow')` and `'keyboardDidHide'` to track keyboard height in state, and apply that height directly as `paddingBottom` on the sheet `View`. On iOS, `KeyboardAvoidingView behavior='padding'` still works correctly and is kept.

**Canonical implementation:** `src/components/ModalKeyboardView.tsx` — exposes `ModalKeyboardView` (wrapper component) and `useModalSheetPadding` (hook). Used by `PrivateNoteModal.tsx` and `FeedbackSupportModal.tsx`.

---

### Reanimated warning: "shared value's .value inside reanimated inline style"

**Symptom:** Reanimated console warning: `"It looks like you might be using shared value's .value inside reanimated inline style"` when rendering animated components. This typically occurs with styles that reference animated values.

**Root cause:** Creating new style objects with animated values directly in JSX inline styles (e.g., `style={[{ transform: [{ scale: scaleValue }] }]}`). On every render, a new style object is created, which Reanimated detects as an unsafe pattern. This is especially problematic in components that animate frequently or use `Animated.Value` from the React Native built-in Animated API.

**Fix:** Extract animated style objects into a `useMemo` computed reference. This ensures the style object is stable and only recalculated when its dependencies change:

```tsx
// ✅ correct — computed style in useMemo prevents Reanimated warnings
const pulseStyle = useMemo(
  () => ({
    transform: [{ scale: pulseValue }],
  }),
  [pulseValue]
);

return <Animated.View style={pulseStyle}>...</Animated.View>;
```

```tsx
// ❌ wrong — inline style object recreated on every render
return (
  <Animated.View
    style={{
      transform: [{ scale: pulseValue }], // Reanimated warning here
    }}
  >
    ...
  </Animated.View>
);
```

Also incorrect (even with array syntax):

```tsx
// ❌ wrong — inline array of styles still creates new objects
return (
  <Animated.View
    style={[
      { transform: [{ scale: pulseValue }] }, // Still a new object every render
    ]}
  >
    ...
  </Animated.View>
);
```

**When to apply:** Any component using `Animated.Value`, `Animated.ValueXY`, or other animated values passed directly to a style property should use this pattern. Examples: animating transforms (scale, rotate, translateX/Y), opacity, or other numeric style properties.

**Implementation checklist:**
- ✅ `useMemo` wraps the style object/array
- ✅ Animated/Reanimated value is a dependency: `[pulseValue]`
- ✅ Style object is stable across renders (same reference unless dependencies change)
- ✅ No console warnings on render cycles

**Examples in codebase:**
- `src/components/FeedChannelFilterModal.tsx` — three animated dots (dot1/2/3AnimatedStyle)
- `src/app/(protected)/camera.tsx` — shutter button scale animation (shutterScaleStyle)
- `src/app/complete-profile.tsx` — loading overlay animations (pulseAnimStyle, fadeAnimStyle)
- `src/app/(protected)/post/uploading.tsx` — rocket emoji pulse (pulseScaleStyle)

---

### iOS push notifications not delivered (APNs key missing from Firebase)

**Symptom:** Push notifications are working on Android but not arriving on iOS. Device permissions, app entitlements, and APNS configuration appear correct, but no notifications arrive or show any error in logs.

**Root cause:** The APNs (Apple Push Notification service) authentication key had not been uploaded to Firebase. Firebase requires a `.p8` APNs auth key to bridge FCM → APNs for iOS devices. Without it, Firebase silently fails all iOS notification deliveries. Android is unaffected because it uses FCM natively and does not require APNs.

**Diagnostic steps taken:**
1. **Apple Push Notifications Console → Tools**: Validated the device's APNs token was legitimate and correctly registered for the app.
2. **Apple Push Notifications Console → Send**: Sent a direct test notification to the device via APNs. This succeeded, confirming the device, app entitlements, and Apple Developer configuration were all correct.
3. **Firebase Console → Messaging**: Attempted a direct test send to the device's FCM token. This failed, narrowing the problem to the Firebase ↔ APNs bridge.
4. **Firebase Console → Project Settings → Cloud Messaging → Apple app configuration**: Confirmed that no APNs key or certificate had been uploaded — the missing link.

**Fix:**
1. Go to **developer.apple.com → Certificates, Identifiers & Profiles → Keys**
2. Create a new key with **Apple Push Notifications service (APNs)** enabled
3. Download the `.p8` file immediately (it can only be downloaded once) and note the **Key ID** and **Team ID**
4. Go to **Firebase Console → Project Settings → Cloud Messaging → Apple app configuration**
5. Upload the `.p8` file, and enter the **Key ID** and **Team ID**

No app reinstall or redeployment is required — notifications begin working immediately after the key is uploaded. A single `.p8` APNs auth key covers both **development and production** environments and all apps under the same Apple Developer account. If notifications still do not arrive after uploading the key, try a **full app reinstall** or **sign out/sign in** to force a fresh FCM token to be generated and saved to the backend. The `.p8` file can only be downloaded once — store it securely. If lost, the key must be revoked and a new one generated.

---

## Mono Repo Structure

This repo is organized as a mono repo under `apps/`:

| Path | Description |
|---|---|
| `apps/mobile/` | Expo / React Native app (the primary Angelia mobile app) |
| `apps/web/` | Vite + React landing site (home page & about page only) |

### apps/mobile/
- All existing React Native / Expo conventions, Redux, Firebase, and copilot rules above apply here.
- Path references in mobile-specific instructions (e.g. `src/components/…`) are relative to `apps/mobile/`.

### apps/web/
- A minimal **marketing/landing site** — only the Home page (`/`) and About page (`/about`).
- **No authentication, no Redux, no Firebase SDK** — it is purely static content.
- Uses **Vite + React + TypeScript + TailwindCSS v4**.
- UI components come exclusively from `@moondreamsdev/dreamer-ui` — see `.github/instructions/dreamer-ui-one-pager.instructions.md`.
- Styling rules:
  - Use `join` from `@moondreamsdev/dreamer-ui/utils` for conditional class names. Never template literals with `${` for `className`.
  - CSS lives in `apps/web/src/index.css` (app theme) and `apps/web/src/dreamer-ui.css` (Dreamer UI theme). Do not modify these without good reason.
- Path aliases (configured in `apps/web/vite.config.ts`):
  - `@` → `apps/web/src`
  - `@components` → `apps/web/src/components`
  - `@routes` → `apps/web/src/routes`
  - `@screens` → `apps/web/src/screens`
  - `@ui` → `apps/web/src/ui`
- Routing: `react-router-dom` v7 via `apps/web/src/routes/AppRoutes.tsx`. Only `/` and `/about` routes exist.
- Firebase Hosting deploy is handled by `.github/workflows/firebase-hosting-merge.yml` (triggered on pushes to `main` that touch `apps/web/**`).

