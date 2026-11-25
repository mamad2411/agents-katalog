---
name: account-info
description: Add a persistent account information section (name, email, avatar) for the logged-in user. Use when a Settings screen or Profile tab needs to show who is signed in. Reads from Supabase auth user metadata — no extra table required.
---

Add an account information display for the currently logged-in user.

## Steps

1. **Locate the right screen** — call `get_routes` and `get_components` to find the Settings screen or Profile tab. If neither exists, ask the user where they want the section before writing any code.

2. **Read the target file** — read the full screen component so you understand its existing imports, hooks, and layout before touching it.

3. **Fetch the current user** — add a `useState<User | null>` and a `useEffect` that calls `supabase.auth.getUser()` once on mount. Import `User` from `@supabase/supabase-js`. Do **not** store the result in a Zustand store — it is auth-layer data, not app state.

   ```ts
   import type { User } from '@supabase/supabase-js'
   import { supabase } from '@/src/services/supabase'

   const [currentUser, setCurrentUser] = useState<User | null>(null)

   useEffect(() => {
     supabase.auth.getUser().then(({ data: { user } }) => setCurrentUser(user))
   }, [])
   ```

4. **Render the account card** — place it at the top of the scrollable content, above subscription or preference sections. Use the existing `SettingsCard` wrapper (or equivalent glass/card component found in step 1) so the visual style matches.

   ```tsx
   {currentUser ? (
     <SettingsCard hasGlass={hasGlass}>
       <LabelMd color="$text-disabled" textTransform="uppercase" letterSpacing={LABEL_LETTER_SPACING} mb="$3">
         <Trans>Account</Trans>
       </LabelMd>

       {(currentUser.user_metadata?.full_name || currentUser.user_metadata?.name) ? (
         <XStack items="center" justify="space-between" gap="$3" mb="$2">
           <BodySm color="$text-secondary" flexShrink={0}><Trans>Name</Trans></BodySm>
           <LabelMd color="$text-emphasis" flex={1} textAlign="right" numberOfLines={1} ellipsizeMode="tail">
             {currentUser.user_metadata.full_name ?? currentUser.user_metadata.name}
           </LabelMd>
         </XStack>
       ) : null}

       {/* email/name must flex + truncate — long emails otherwise overflow the card */}
       <XStack items="center" justify="space-between" gap="$3">
         <BodySm color="$text-secondary" flexShrink={0}><Trans>Email</Trans></BodySm>
         <LabelMd color="$text-secondary" flex={1} textAlign="right" numberOfLines={1} ellipsizeMode="middle">
           {currentUser.email}
         </LabelMd>
       </XStack>
     </SettingsCard>
   ) : null}
   ```

5. **i18n** — wrap every new user-visible string (`Account`, `Name`, `Email`) with `<Trans>` or `` t`…` ``. Run `/expo-rn-plugin:i18n` after to extract and translate all locales.

6. **Type-check** — run `tsc --noEmit` and fix all errors before reporting done.

## Where to place the card

| Scenario | Placement |
| --- | --- |
| Settings screen exists | Top of scroll content, above Subscription card |
| Dedicated Profile tab | Center of screen as the hero block |
| No settings / profile screen | Ask the user which tab to add it to |

## Data source

`user_metadata` is populated by the OAuth provider at sign-in:

| Field | Google | Apple | Email/Password |
| --- | --- | --- | --- |
| `full_name` | ✓ | ✓ (first sign-in only) | — |
| `name` | ✓ | — | — |
| `avatar_url` | ✓ | — | — |
| `email` | via `user.email` | via `user.email` | via `user.email` |

Always guard name fields with a conditional — email/password users won't have them.

## Account deletion (App Store Guideline 5.1.1(v))

Any app that supports account creation **must** offer in-app account deletion. **Apple rejects email-only / "contact support" deletion** — it has to be self-service in the app. (Google Play accepts a hosted web URL for its Data Safety form, so a common setup is in-app deletion for iOS + a web page for Play.)

**Edge function** `supabase/functions/delete-account/index.ts` — deploy with JWT verification ON (do **not** pass `--no-verify-jwt`); resolve the caller from their token, then delete with the service role:

```ts
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

Deno.serve(async (req) => {
  if (req.method !== 'POST') return new Response('Method not allowed', { status: 405 })
  const authHeader = req.headers.get('Authorization')
  if (!authHeader) return new Response('Unauthorized', { status: 401 })
  const url = Deno.env.get('SUPABASE_URL')!
  const { data: { user } } = await createClient(url, Deno.env.get('SUPABASE_ANON_KEY')!, {
    global: { headers: { Authorization: authHeader } },
  }).auth.getUser()
  if (!user) return new Response('Unauthorized', { status: 401 })
  const admin = createClient(url, Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!, { db: { schema: 'api' } })
  await admin.from('journal_entries').delete().eq('user_id', user.id) // repeat for each user-owned table
  await admin.from('device_tokens').delete().eq('user_id', user.id)
  const { error } = await admin.auth.admin.deleteUser(user.id)
  if (error) return new Response(error.message, { status: 500 })
  return new Response('ok')
})
```

`SUPABASE_URL` / `SUPABASE_ANON_KEY` / `SUPABASE_SERVICE_ROLE_KEY` are auto-injected into Edge Functions — don't set them.

**Client** — invoke then sign out:

```ts
const deleteAccount = async () => {
  const { error } = await supabase.functions.invoke('delete-account', { method: 'POST' })
  if (error) throw error
  await supabase.auth.signOut()
}
```

**Settings UI** — a destructive button (signed-in only; hidden for anonymous) behind a **two-step** confirm. For apps with IAP subscriptions, add a line that deleting the account does **not** cancel the store subscription:

```tsx
const note = isPro ? '\n\n' + t`Deleting your account does not cancel your subscription. Manage it in the App Store.` : ''
Alert.alert(t`Delete account`, t`This permanently deletes your account and all your data. This cannot be undone.` + note, [
  { text: t`Cancel`, style: 'cancel' },
  { text: t`Delete account`, style: 'destructive', onPress: () =>
    Alert.alert(t`Are you sure?`, t`This cannot be undone.`, [
      { text: t`Cancel`, style: 'cancel' },
      { text: t`Delete`, style: 'destructive', onPress: deleteAccount },
    ]) },
])
```

**Testing & App Review** — sign-up usually requires email confirmation, so make **pre-confirmed** test accounts via the admin API rather than real inboxes:

```bash
curl -X POST "https://<ref>.supabase.co/auth/v1/admin/users" \
  -H "apikey: $SERVICE_ROLE_KEY" -H "Authorization: Bearer $SERVICE_ROLE_KEY" \
  -H "Content-Type: application/json" \
  -d '{"email":"review+test@example.com","password":"…","email_confirm":true}'
```

Give the reviewer a demo account in App Review Information **plus a screen recording** of the full flow — the deletion test consumes the demo account, so the recording is the durable proof.

**Reviewer-in-guest-mode trap (real rejection):** the delete button is hidden for guest/anonymous users, so a reviewer who taps "Continue without an account" sees no deletion option and rejects under 5.1.1(v) — even though the feature works. Defend against it:
- In **App Review Information → Review Notes**, lead with: *sign in with the demo account first — do NOT use "Continue without an account"*, then the exact steps (Settings tab → scroll to bottom → Delete account → confirm).
- Put demo creds in the structured **Sign-In Information** fields (not just free-text notes), and **attach the screen recording** (you can also attach it to the Resolution Center reply).
- Tell-tale that the reviewer never signed in: the demo account is still there afterward (untouched).
- Optional hardening: show a disabled "Delete account" row or a "Sign in to manage your account" hint for guests, so the option is visible even before sign-in.

## Rules

- Long values (especially `email`) must use `flex={1}` + `numberOfLines={1}` + `ellipsizeMode` (`"middle"` for email) with the label `flexShrink={0}` — otherwise a long email overflows the card and runs off-screen
- Never read `session.user` for display — always call `supabase.auth.getUser()` which returns the authoritative server-side user object
- Never show raw PII in Sentry tags or analytics events — use `user.id` (opaque) only
- Do not create a new Zustand store for this — the Supabase auth client already owns this state
- The card must not render at all (`null`) while `currentUser` is still `null` — no empty placeholder UI
- Run `/expo-rn-plugin:i18n` after adding strings so all locales stay in sync
