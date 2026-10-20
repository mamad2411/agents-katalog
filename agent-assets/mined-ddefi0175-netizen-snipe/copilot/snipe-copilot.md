## Copilot Instructions for Snipe (Firebase-first Web3 DeFi Platform)

### 🎯 Architecture Snapshot
**React 18 + Vite frontend** (Onchainweb/) with **Firebase serverless backend** (Firestore + Auth). No server to maintain; legacy Express/MongoDB backend (backend/) is deprecated—never add features there.

**Dual-layer data access**: Snipe works offline via **Firebase-first + localStorage fallback** pattern. Always check `isFirebaseAvailable` before any Firebase operation. Never reinitialize Firebase; reuse singleton from [Onchainweb/src/lib/firebase.js](../Onchainweb/src/lib/firebase.js).

### 🗂️ Key Codepaths & Patterns

| Purpose | File(s) | Critical Details |
|---------|---------|------------------|
| **Firebase singleton** | [src/lib/firebase.js](../Onchainweb/src/lib/firebase.js) | Exports `isFirebaseAvailable`, `db`, `auth`, all CRUD helpers. Graceful fallback if config incomplete. |
| **Config centralization** | [src/config/firebase.config.js](../Onchainweb/src/config/firebase.config.js) | `COLLECTIONS` const (users, trades, deposits, chatMessages, etc.), env vars, listener limits. |
| **Services layer (PREFERRED)** | [src/services/](../Onchainweb/src/services/) | firebase.service.js, database.service.js, walletService.js, adminService.js. Use these, not firebase.js directly, for complex ops. |
| **Wallet integration** | [src/lib/walletConnect.jsx](../Onchainweb/src/lib/walletConnect.jsx) | 11 providers (MetaMask, Coinbase, WalletConnect, etc.). **Fallback strategy**: injected → deep link → WalletConnect QR. Never request private keys. |
| **Admin roles & permissions** | [src/lib/adminAuth.js](../Onchainweb/src/lib/adminAuth.js) | Roles: `master` (all permissions), `admin`, `user`. Email allowlist via `VITE_ADMIN_ALLOWLIST` env. |
| **Error handling** | [src/lib/errorHandling.js](../Onchainweb/src/lib/errorHandling.js) | `formatApiError()`, `formatWalletError()`. Cold-start aware messages for Render deployments. |
| **Data Connect Services** | [src/services/dataconnect.service.ts](../Onchainweb/src/services/dataconnect.service.ts) | **PREFERRED for new code**. Type-safe services: `usersService`, `tradesService`, `chatService`, `notificationsService`. 25+ methods with caching. |
| **Data Connect Types** | [src/types/dataconnect.types.ts](../Onchainweb/src/types/dataconnect.types.ts) | Generated TypeScript interfaces for all data models (User, Trade, Notification, etc.). |
| **⚠️ DEPRECATED** | [src/lib/api.js](../Onchainweb/src/lib/api.js) | **DO NOT USE**—old MongoDB API client. |

### 💾 Core Data Patterns

**Real-time listeners (NOT polling)**:
```javascript
useEffect(() => {
  if (!isFirebaseAvailable) return;
  const unsubscribe = onSnapshot(doc(db, 'users', userId), (doc) => {
    setUserData(doc.data());
  });
  return () => unsubscribe(); // ALWAYS cleanup
}, [userId]);
```

**Guard Firebase calls**:
```javascript
if (isFirebaseAvailable) {
  await setDoc(doc(db, 'trades', tradeId), data);
} else {
  localStorage.setItem(`trade_${tradeId}`, JSON.stringify(data));
}
```

**Error handling** (centralized):
```javascript
try {
  await firebaseOperation();
} catch (error) {
  notify(formatApiError(error)); // Handles cold-start, network, auth errors
}
```

**Data Connect Service Pattern (NEW - PREFERRED)**:
```typescript
import { usersService, tradesService } from '@/services/dataconnect.service'

// Type-safe, cached, with offline fallback
const user = await usersService.getUser(userId)
const trades = await tradesService.listUserTrades(userId, 20, 0)
const tradeId = await tradesService.createTrade({
  userId, pair: 'BTC/USD', direction: 'up', entryPrice: 50000, amount: 100
})
```

### 🚀 Development Workflows
- **Dev server**: `cd Onchainweb && npm install && npm run dev` → http://localhost:5173
- **Production build**: `npm run build:production` (runs clean + build with production mode)
- **Firebase deployment**: `firebase deploy --only firestore:rules` (when database.rules.json changes)
- **Required .env vars**: All 8 Firebase vars (`VITE_FIREBASE_*`) + `VITE_WALLETCONNECT_PROJECT_ID`
- **Admin panel**: Set `VITE_ENABLE_ADMIN=true` in .env to enable admin login

### 📦 Project Structure
- **Onchainweb/**: React frontend (Vite bundler, no build server)
- **Onchainweb/src/components/**: UI (Header, AdminPanel, Wallet, Trade, Dashboard, etc.)
- **database.rules.json** / **firestore.indexes.json**: Firestore security & indexing
- **backend/**, **functions/**: Deprecated (MongoDB/Express); ignore unless maintaining legacy features

### ⚠️ Build & Deployment Notes
- **Vite chunking**: Manual vendor-react split expected (see vite.config.js); 1000kB warning is normal
- **CSP compliance**: esbuild minification instead of terser (no `unsafe-eval` needed)
- **Cloudflare Workers**: Optional scaling layer (see workers/ folder)
- **No tests configured**: Vitest config exists but no test suite—focus on manual testing

### 📚 Key Docs
[QUICK_START_GUIDE.md](../QUICK_START_GUIDE.md), [BACKEND_REPLACEMENT.md](../BACKEND_REPLACEMENT.md), [REALTIME_DATA_ARCHITECTURE.md](../REALTIME_DATA_ARCHITECTURE.md), [FIREBASE_DATA_CONNECT_SUMMARY.md](../FIREBASE_DATA_CONNECT_SUMMARY.md), [FIREBASE_DATA_CONNECT_SETUP.md](../FIREBASE_DATA_CONNECT_SETUP.md)
