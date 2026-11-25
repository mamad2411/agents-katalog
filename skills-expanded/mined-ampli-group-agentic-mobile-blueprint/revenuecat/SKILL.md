---
name: revenuecat
description: Integrate RevenueCat for in-app purchases — consumable credit packs or subscriptions. Use when setting up RevenueCat, creating products in App Store Connect / Google Play, configuring the SDK, building a paywall, or handling purchase webhooks in Supabase Edge Functions.
---

# RevenueCat Integration

## Architecture

```
App Store Connect / Google Play  ←→  RevenueCat Dashboard
        ↓ purchase events
RevenueCat Webhook  →  Supabase Edge Function  →  profiles.credits
        ↓ SDK
RevenueCatContext (React)  →  PaywallTrigger (root Modal)
```

RevenueCat is the source of truth for purchases. Supabase is the source of truth for credits. They stay in sync via webhook.

---

## Step 1: Create Products in App Store Connect (iOS)

1. [appstoreconnect.apple.com](https://appstoreconnect.apple.com) → My Apps → your app
2. Left sidebar: **Monetization → In-App Purchases** → **+**
3. Type: **Consumable** → Create
4. For each product:
   - **Product ID:** `credits_50` / `credits_150` (must match exactly across all platforms)
   - **Reference Name:** `50 Credits` / `150 Credits`
   - **Price:** set your price tier
   - Add at least one **Localization** (English)
   - **Review Information:** upload a screenshot of the paywall (required by Apple — mockup is fine)
   - **Save**

Products will show "Missing Metadata" until your next app submission — this is normal. RevenueCat can read them immediately.

---

## Step 2: Create Products in Google Play Console (Android)

1. [play.google.com/console](https://play.google.com/console) → your app
2. Left sidebar: **Monetize → In-app products** → **Create product**
3. For each product:
   - **Product ID:** `credits_50` / `credits_150`
   - **Name** and **Description**
   - **Default price**
   - **Status: Active** ← required, draft products don't work
4. Save

**Note:** Google Play products only work after the app has at least one published release (even internal testing). Purchases will fail in development until then.

---

## Step 3: Set Up RevenueCat Dashboard

### Create project + add iOS app

1. [app.revenuecat.com](https://app.revenuecat.com) → **+ New Project**
2. **+ Add App → App Store**
3. Bundle ID: your `ios.bundleIdentifier`
4. **In-App Purchase key (.p8):** this is **NOT** the App Store Connect API key

   **Critical distinction:**
   | Key type | Filename | Used for |
   |---|---|---|
   | **In-App Purchase key** | `SubscriptionKey_XXXXXXXXXX.p8` | RevenueCat ← use this |
   | App Store Connect API key | `AuthKey_XXXXXXXXXX.p8` | CI/CD, EAS Submit |

   To get the right key:
   - App Store Connect → [Users and Access](https://appstoreconnect.apple.com/access/users) → **Integrations**
   - Under **In-App Purchase** → **+** → Name it `RevenueCat` → Download
   - File will be named `SubscriptionKey_…p8` — upload this to RevenueCat

### Add Android app

1. **+ Add App → Play Store**
2. Package name: your `android.package`
3. **Service Account credentials JSON:** same service account used for Play Console API access (see google-play-setup skill)
   - Play Console → Setup → API access → linked Google Cloud project
   - Create service account → grant **Release Manager** in Play Console
   - Download JSON → upload to RevenueCat

### Add Products

For each app (iOS + Android):
- **Products** tab → **+ New Product**
- Enter Product IDs: `credits_50`, `credits_150`
- Type: **Consumable**

### Create Entitlement

- **Entitlements** tab → **+ New Entitlement**
- Identifier: `credits`
- Attach both products
- Save

### Create Offering

- **Offerings** tab → **+ New Offering**
- Identifier: `default`
- Add 2 packages: attach iOS + Android products for each credit pack
- Set as **Current**

### Configure Webhook

- **Integrations → Webhooks** → **+ Add webhook**
- URL: `https://YOUR_PROJECT.supabase.co/functions/v1/revenuecat-webhook`
- Events: `INITIAL_PURCHASE`, `NON_SUBSCRIPTION_PURCHASE`, `NON_RENEWING_PURCHASE`
- Copy the **Webhook Shared Secret** → add to Supabase secrets

### Get SDK Keys

- **Project Settings → API Keys**
- Copy **iOS Public SDK Key** (`appl_...`)
- Copy **Android Public SDK Key** (`goog_...`)

---

## Step 4: Install SDK

```bash
cd mobile
npx expo install react-native-purchases react-native-purchases-ui
```

---

## Step 5: Environment Variables

Separate keys per platform — `app.config.js` picks the right one at build time:

```bash
# mobile/.env.local
EXPO_PUBLIC_REVENUECAT_IOS_KEY=appl_...
EXPO_PUBLIC_REVENUECAT_ANDROID_KEY=goog_...

# supabase/functions/.env.local
REVENUECAT_WEBHOOK_SECRET=whsec_...
```

`mobile/app.config.js`:
```js
const isIos = process.env.EAS_BUILD_PLATFORM === 'ios';
const revenueCatApiKey = isIos
  ? process.env.EXPO_PUBLIC_REVENUECAT_IOS_KEY
  : process.env.EXPO_PUBLIC_REVENUECAT_ANDROID_KEY;

export default {
  expo: {
    extra: { revenueCatApiKey },
  },
};
```

Add to `eas.json` build profiles:
```json
{
  "build": {
    "production": {
      "env": {
        "EXPO_PUBLIC_REVENUECAT_IOS_KEY": "appl_...",
        "EXPO_PUBLIC_REVENUECAT_ANDROID_KEY": "goog_..."
      }
    }
  }
}
```

---

## Step 6: RevenueCatContext

**Critical architecture:** `RevenueCatUI.presentPaywall()` must be called from the root view controller, never from inside a React Native `<Modal>`. Calling it from a modal causes iOS to throw "not in window hierarchy". The solution: queue the request via a promise, resolve it from a root-level `<PaywallTrigger>` component.

```typescript
// contexts/RevenueCatContext.tsx
import React, { createContext, useCallback, useContext, useEffect, useRef, useState } from 'react';
import { Alert, LogBox, Modal, StyleSheet, View } from 'react-native';
import Constants from 'expo-constants';
import Purchases, {
  CustomerInfo, CustomerInfoUpdateListener, LOG_LEVEL,
  PurchasesOffering, PurchasesOfferings,
} from 'react-native-purchases';
import RevenueCatUI from 'react-native-purchases-ui';
import { useAuth } from './AuthContext';

const REVENUECAT_API_KEY =
  (Constants.expoConfig?.extra?.revenueCatApiKey as string) ||
  process.env.EXPO_PUBLIC_REVENUECAT_API_KEY || '';

if (__DEV__) {
  LogBox.ignoreLogs([
    'Purchase failure simulated successfully',
    '[RevenueCat] [Test Store]',
  ]);
}

interface RevenueCatContextType {
  isConfigured: boolean;
  customerInfo: CustomerInfo | null;
  offerings: PurchasesOfferings | null;
  presentPaywall: () => Promise<boolean>;
  presentCustomerCenter: () => Promise<void>;
  restorePurchases: () => Promise<CustomerInfo>;
  _paywallPending: boolean;
  _pendingOffering: PurchasesOffering | null;
  _resolvePaywall: (purchased: boolean) => void;
}

const RevenueCatContext = createContext<RevenueCatContextType | undefined>(undefined);

export function RevenueCatProvider({ children }: { children: React.ReactNode }) {
  const { user } = useAuth();
  const [isConfigured, setIsConfigured] = useState(false);
  const [customerInfo, setCustomerInfo] = useState<CustomerInfo | null>(null);
  const [offerings, setOfferings] = useState<PurchasesOfferings | null>(null);
  const [paywallPending, setPaywallPending] = useState(false);
  const [pendingOffering, setPendingOffering] = useState<PurchasesOffering | null>(null);
  const paywallResolveRef = useRef<((purchased: boolean) => void) | null>(null);

  // Configure SDK and register listener together on mount
  useEffect(() => {
    if (!REVENUECAT_API_KEY) {
      console.warn('[RevenueCat] API key not set — SDK not configured');
      return;
    }
    const configure = async () => {
      try {
        if (__DEV__) Purchases.setLogLevel(LOG_LEVEL.DEBUG);
        Purchases.configure({ apiKey: REVENUECAT_API_KEY, appUserID: user?.id ?? null });
        const listener: CustomerInfoUpdateListener = (info) => setCustomerInfo(info);
        Purchases.addCustomerInfoUpdateListener(listener);
        setIsConfigured(true);
        const [info, offs] = await Promise.all([Purchases.getCustomerInfo(), Purchases.getOfferings()]);
        setCustomerInfo(info);
        setOfferings(offs);
        return listener;
      } catch (e) {
        console.error('[RevenueCat] configure error:', e);
        return null;
      }
    };
    let listenerRef: CustomerInfoUpdateListener | null = null;
    configure().then((ref) => { listenerRef = ref; });
    return () => { if (listenerRef) Purchases.removeCustomerInfoUpdateListener(listenerRef); };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Sync Supabase user with RevenueCat
  useEffect(() => {
    if (!isConfigured) return;
    const sync = async () => {
      try {
        if (user?.id) {
          const { customerInfo: info } = await Purchases.logIn(user.id);
          setCustomerInfo(info);
          // Consume any stuck unconsumed Google Play purchases — prevents "You already own this item" errors
          await Purchases.syncPurchasesForResult();
        } else {
          const isAnon = await Purchases.isAnonymous();
          if (!isAnon) { const info = await Purchases.logOut(); setCustomerInfo(info); }
        }
      } catch (e) { console.error('[RevenueCat] user sync error:', e); }
    };
    sync();
  }, [user?.id, isConfigured]);

  const presentPaywall = useCallback(async (): Promise<boolean> => {
    try {
      const offs = await Purchases.getOfferings();
      const hasPackages = offs.current?.availablePackages.length ?? 0 > 0;
      if (!hasPackages) {
        Alert.alert('Not available', 'In-app purchases are not available yet.');
        return false;
      }
      return new Promise<boolean>((resolve) => {
        paywallResolveRef.current = resolve;
        setPendingOffering(offs.current);
        setPaywallPending(true);
      });
    } catch (e) {
      console.error('[RevenueCat] getOfferings error:', e);
      return false;
    }
  }, []);

  const resolvePaywall = useCallback((purchased: boolean) => {
    setPaywallPending(false);
    setPendingOffering(null);
    paywallResolveRef.current?.(purchased);
    paywallResolveRef.current = null;
  }, []);

  return (
    <RevenueCatContext.Provider value={{
      isConfigured, customerInfo, offerings, presentPaywall,
      presentCustomerCenter: async () => { try { await RevenueCatUI.presentCustomerCenter(); } catch(e) {} },
      restorePurchases: async () => { const info = await Purchases.restorePurchases(); setCustomerInfo(info); return info; },
      _paywallPending: paywallPending, _pendingOffering: pendingOffering, _resolvePaywall: resolvePaywall,
    }}>
      {children}
    </RevenueCatContext.Provider>
  );
}

const NOOP: RevenueCatContextType = {
  isConfigured: false, customerInfo: null, offerings: null,
  presentPaywall: async () => false, presentCustomerCenter: async () => {},
  restorePurchases: async () => { throw new Error('RevenueCat not available'); },
  _paywallPending: false, _pendingOffering: null, _resolvePaywall: () => {},
};

export function useRevenueCat() {
  return useContext(RevenueCatContext) ?? NOOP;
}

/**
 * Mount ONCE at the root layout, outside any other Modal.
 * Never use visible={false} — on Android Fabric this causes "child already has a parent" crashes.
 * Unmount entirely when not needed instead.
 */
export function PaywallTrigger() {
  const { _paywallPending, _pendingOffering, _resolvePaywall } = useRevenueCat();

  const handleClose = useCallback(async (purchased: boolean) => {
    try {
      if (purchased) await Purchases.syncPurchasesForResult();
    } catch(e) { console.warn('[RevenueCat] paywall close sync error:', e); }
    finally { _resolvePaywall(purchased); }
  }, [_resolvePaywall]);

  if (!_paywallPending) return null;

  return (
    <Modal visible animationType="slide" presentationStyle="pageSheet" onRequestClose={() => handleClose(false)}>
      <View style={{ flex: 1 }}>
        <RevenueCatUI.Paywall
          options={_pendingOffering ? { offering: _pendingOffering } : undefined}
          onDismiss={() => handleClose(false)}
          onPurchaseCompleted={() => handleClose(true)}
          onRestoreCompleted={() => handleClose(true)}
          onRestoreError={() => handleClose(false)}
          onPurchaseCancelled={() => handleClose(false)}
          onPurchaseError={() => handleClose(false)}
        />
      </View>
    </Modal>
  );
}
```

---

## Step 7: Wire into Root Layout

```typescript
// app/_layout.tsx
import { RevenueCatProvider, PaywallTrigger } from '@/contexts/RevenueCatContext';

export default function RootLayout() {
  return (
    <RevenueCatProvider>
      <Stack />
      <PaywallTrigger />  {/* must be here — outside any Modal */}
    </RevenueCatProvider>
  );
}
```

---

## Step 8: Trigger Paywall from Anywhere

```typescript
const { presentPaywall } = useRevenueCat();

// On insufficient credits error from your backend (HTTP 402)
const purchased = await presentPaywall();
if (purchased) {
  // Credits updated automatically via Supabase Realtime on profiles.credits
  // Retry the action
}
```

---

## Step 9: Supabase Webhook Edge Function

```typescript
// supabase/functions/revenuecat-webhook/index.ts
import { createClient } from 'npm:@supabase/supabase-js@2';

const CREDITS_BY_PRODUCT: Record<string, number> = {
  credits_50: 50,
  credits_150: 150,
};

const PURCHASE_EVENTS = new Set([
  'INITIAL_PURCHASE',
  'NON_SUBSCRIPTION_PURCHASE',
  'NON_RENEWING_PURCHASE',
]);

Deno.serve(async (req) => {
  if (req.method !== 'POST') return new Response('Method not allowed', { status: 405 });

  // Verify shared secret
  const secret = Deno.env.get('REVENUECAT_WEBHOOK_SECRET');
  if (secret && req.headers.get('Authorization') !== secret) {
    return new Response('Unauthorized', { status: 401 });
  }

  const body = await req.json();
  const event = body.event;

  if (!PURCHASE_EVENTS.has(event?.type)) {
    return new Response(JSON.stringify({ received: true, processed: false }), { status: 200 });
  }

  const appUserId = event.app_user_id;
  const creditsToAdd = CREDITS_BY_PRODUCT[event.product_id];

  if (!creditsToAdd) {
    console.warn(`Unknown product_id: ${event.product_id}`);
    return new Response(JSON.stringify({ received: true, processed: false }), { status: 200 });
  }

  const supabase = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!,
  );

  // Atomic credit increment — use RPC to avoid race conditions
  const { error } = await supabase.rpc('add_credits', {
    p_user_id: appUserId,
    p_amount: creditsToAdd,
    p_admin_note: `RevenueCat: ${event.product_id}`,
  });

  if (error) {
    console.error('Failed to add credits:', error);
    return new Response(JSON.stringify({ error: error.message }), { status: 500 });
  }

  return new Response(JSON.stringify({ received: true, processed: true, credits_added: creditsToAdd }), { status: 200 });
});
```

Disable JWT verification for this function in `supabase/config.toml`:
```toml
[functions.revenuecat-webhook]
verify_jwt = false
```

---

## Step 10: Database Schema

```sql
-- Credits on profiles
alter table profiles add column if not exists credits integer not null default 100 check (credits >= 0);

-- Audit log
create table credit_transactions (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users on delete cascade not null,
  amount integer not null,
  balance_after integer not null,
  action_type text not null,
  metadata jsonb default '{}',
  created_at timestamptz default now()
);

-- Atomic increment RPC (avoids race conditions)
create or replace function add_credits(p_user_id uuid, p_amount integer, p_admin_note text default null)
returns integer as $$
declare v_new_balance integer;
begin
  select credits + p_amount into v_new_balance from profiles where id = p_user_id for update;
  update profiles set credits = v_new_balance, credits_updated_at = now() where id = p_user_id;
  insert into credit_transactions (user_id, amount, balance_after, action_type, metadata)
  values (p_user_id, p_amount, v_new_balance, 'purchase', jsonb_build_object('note', p_admin_note));
  return v_new_balance;
end;
$$ language plpgsql security definer;

-- Enable Realtime on profiles so the app reacts instantly after webhook credits the user
alter publication supabase_realtime add table profiles;
```

Listen for credit updates in the app:
```typescript
supabase.channel('profile-credits')
  .on('postgres_changes', { event: 'UPDATE', schema: 'public', table: 'profiles', filter: `id=eq.${userId}` },
    (payload) => setCredits(payload.new.credits))
  .subscribe();
```

---

## Setup Checklist

- [ ] App Store Connect: consumable products created with correct Product IDs
- [ ] Google Play: in-app products created and set to **Active**
- [ ] RevenueCat: project created
- [ ] RevenueCat: iOS app added with **In-App Purchase key** (`SubscriptionKey_*.p8`, not `AuthKey_*.p8`)
- [ ] RevenueCat: Android app added with Google Play service account JSON
- [ ] RevenueCat: all products added (for both platforms)
- [ ] RevenueCat: entitlement `credits` created with products attached
- [ ] RevenueCat: offering `default` created and set as Current
- [ ] RevenueCat: webhook configured pointing to Supabase edge function
- [ ] `REVENUECAT_WEBHOOK_SECRET` added to Supabase secrets
- [ ] iOS + Android SDK keys added to `.env.local` and `eas.json`

---

## Gotchas

**Wrong `.p8` key type for RevenueCat** — RevenueCat requires the **In-App Purchase key** (`SubscriptionKey_*.p8`), not the App Store Connect API key (`AuthKey_*.p8`). They look identical but are created in different sections of App Store Connect. Create it at: App Store Connect → Users and Access → Integrations → In-App Purchase.

**"You already own this item" on Android** — Google Play consumables must be "consumed" before they can be repurchased. Call `Purchases.syncPurchasesForResult()` after login and after paywall close to consume any stuck purchases. The `RevenueCatContext` above handles this.

**PaywallTrigger causes iOS crash: "not in window hierarchy"** — The paywall must be presented from root context, never from inside a `<Modal>`. Use the queue pattern above: `presentPaywall()` queues the request, `PaywallTrigger` (at root) presents it.

**Android Fabric: "child already has a parent" crash** — Never render `<Modal visible={false}>`. Unmount the component entirely with `if (!_paywallPending) return null` instead of toggling `visible`.

**Google Play products not working in development** — Products are only purchasable after the app has at least one published release (internal testing counts). Use RevenueCat's sandbox testing until then.

**Product IDs must be identical across all three platforms** — App Store Connect, Google Play, and RevenueCat dashboard must all use exactly the same string: `credits_50`, `credits_150`. A single character difference breaks the mapping.

**Webhook not triggering** — Check RevenueCat dashboard → Integrations → Webhooks → Recent deliveries for errors. Common causes: wrong URL, missing `verify_jwt = false` in `supabase/config.toml`, or webhook secret mismatch.

**Credits not updating in real-time** — Supabase Realtime must be enabled on the `profiles` table (`alter publication supabase_realtime add table profiles`). Without this, the credit balance only updates on next app launch.
