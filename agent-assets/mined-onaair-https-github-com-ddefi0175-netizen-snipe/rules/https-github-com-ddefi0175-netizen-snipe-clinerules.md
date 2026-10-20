# Cline AI Rules for Snipe Platform

Web3 trading platform: React + Vite frontend, Firebase backend, 11+ wallet providers, real-time data sync.

## Critical: Firebase-First + localStorage Fallback Pattern

**The codebase has a dual-layer architecture for graceful degradation:**

```javascript
// Always follow this pattern for new features
export const saveUserData = async (userId, data) => {
  if (!isFirebaseAvailable) {
    // Fallback: localStorage (dev/offline)
    const users = JSON.parse(localStorage.getItem('users') || '{}');
    users[userId] = data;
    localStorage.setItem('users', JSON.stringify(users));
  } else {
    // Primary: Firebase Firestore
    await setDoc(doc(db, 'users', userId), data, { merge: true });
  }
};
```

**Key singleton exports from `src/lib/firebase.js`:**
- `app`, `db`, `auth` - Never reinitialize
- `isFirebaseAvailable` - Check before every Firebase call

## Essential File Map

| Purpose | File | Notes |
|---------|------|-------|
| Firebase service | `src/lib/firebase.js` | Singleton, check `isFirebaseAvailable` |
| Firebase config | `src/config/firebase.config.js` | COLLECTIONS, env vars |
| Wallet connection | `src/lib/walletConnect.jsx` | 11 wallets, fallback strategy |
| Error handling | `src/lib/errorHandling.js` | `formatApiError()`, cold-start aware |
| Admin auth | `src/lib/adminAuth.js` | Roles, permissions, allowlist |
| DEPRECATED | `src/lib/api.js` | Old MongoDB API (don't use) |

## Development Commands

```bash
# Frontend (primary)
cd Onchainweb && npm run dev     # Dev server on :5173
npm run build                     # Production → dist/
npm run preview                   # Preview dist/

# Backend (deprecated, legacy only)
cd backend && npm run dev         # MongoDB Express on :4000
```

## Environment Setup

**Required: `Onchainweb/.env`** (8 variables)
```env
VITE_FIREBASE_API_KEY=your-key
VITE_FIREBASE_AUTH_DOMAIN=your-domain
VITE_FIREBASE_PROJECT_ID=your-project
VITE_FIREBASE_STORAGE_BUCKET=your-bucket
VITE_FIREBASE_MESSAGING_SENDER_ID=your-sender-id
VITE_FIREBASE_APP_ID=your-app-id
VITE_FIREBASE_MEASUREMENT_ID=your-measurement-id
VITE_WALLETCONNECT_PROJECT_ID=your-wc-project-id
```

## Core Code Patterns

### 1. Real-Time Listeners (Not Polling)

```javascript
// ✅ CORRECT: WebSocket listener
useEffect(() => {
  if (!isFirebaseAvailable) return;

  const unsubscribe = onSnapshot(
    doc(db, 'users', userId),
    (doc) => setUserData(doc.data())
  );

  return () => unsubscribe(); // Critical: cleanup
}, [userId]);

// ❌ WRONG: Polling wastes bandwidth
setInterval(() => fetchUser(), 3000);
```

### 2. Wallet Connection

**Supported wallets:** MetaMask, Trust, Coinbase, OKX, Phantom, Binance, TokenPocket, Rainbow, Ledger, imToken, WalletConnect

**Connection strategy:**
1. Try injected provider (browser extension)
2. Fallback to deep link (mobile)
3. Fallback to WalletConnect QR code

**Persistence:** STORAGE_KEYS in localStorage
- `wallet_connected`, `wallet_address`, `wallet_chainId`, `wallet_connector_type`, `wallet_session`

**Supported chains:** Ethereum, BSC, Polygon, Arbitrum, Optimism, Avalanche, Fantom

### 3. Error Handling

```javascript
import { formatApiError } from './lib/errorHandling';

try {
  await firebaseOperation();
} catch (error) {
  // Centralized formatter with cold-start awareness
  showNotification(formatApiError(error));
}
```

**Error mappings:**
- 401 → Invalid credentials
- 403 → Access denied
- 500+ → Server error
- ETIMEDOUT → Cold start warning (Render deployments)

### 4. Component Loading State

```javascript
const [loading, setLoading] = useState(false);

const handleAction = async () => {
  setLoading(true);
  try {
    await performAction();
  } finally {
    setLoading(false); // Always reset, even on error
  }
};
```

### 5. Admin Permissions

**Roles:** `master` | `admin` | `user`

**Permissions flags:**
- `manageUsers`, `manageBalances`, `manageKYC`
- `manageTrades`, `viewReports`, `manageDeposits`
- `manageWithdrawals`, `customerService`
- `viewLogs`, `siteSettings`, `createAdmins`

**Access modes:**
- `all` - Access all users
- `assigned` - Specific user IDs only

**Allowlist:** `VITE_ADMIN_ALLOWLIST` env var controls admin account creation

## Build Configuration (vite.config.js)

- **Manual chunking:** `vendor-react` separate bundle
- **Chunk size warning:** 1000kB (Firebase + WalletConnect large)
- **JSX loader:** esbuild handles `.js` + `.jsx` files
- **Base path:** `'/'` (works with Vercel)

## Coding Standards

### Always Do ✅
- Check `isFirebaseAvailable` before Firebase calls
- Implement localStorage fallback
- Use `onSnapshot()` for real-time data (not polling)
- Cleanup listeners in useEffect return
- Use `formatApiError()` for error messages
- Test MetaMask + WalletConnect QR flows
- Use React.memo, useCallback, useMemo for performance

### Never Do ❌
- Poll Firebase with setInterval
- Reinitialize Firebase singleton
- Use `src/lib/api.js` (deprecated MongoDB)
- Commit `.env` files or credentials
- Request private keys from wallets

## First-Time Setup

1. Install Node 18+: `node --version`
2. Install dependencies: `cd Onchainweb && npm install`
3. Create `.env` with 8 Firebase variables
4. Start dev server: `npm run dev` → http://localhost:5173

## Adding a Feature

1. **Identify data source:** Firebase or localStorage fallback?
2. **Implement CRUD:** Add to Firebase service with fallback
3. **Create component:** Use real-time listeners (not polling)
4. **Error handling:** Use `formatApiError()` for consistency
5. **Test:** Verify with Firebase Console and localStorage

## Debugging Checklist

- **F12 Console:** Check Firebase init errors
- **Firebase Console:** Verify data structure matches code
- **Network Tab:** Inspect Firestore API calls
- **Check `isFirebaseAvailable`:** Determines active data source
- **Test offline:** Verify localStorage fallback works

## Tech Stack Summary

- **Frontend:** React 18 + Vite 5.4.21 (ES modules)
- **Backend:** Firebase (Firestore + Auth + Realtime DB)
- **Styling:** Tailwind CSS v4 (PostCSS)
- **Wallets:** WalletConnect v2 + EIP-6963 (injected)
- **State:** React Context API (no Redux)

## Documentation Quick Reference

- `QUICK_START_GUIDE.md` → 5-minute setup
- `BACKEND_REPLACEMENT.md` → Why Firebase vs MongoDB
- `REALTIME_DATA_ARCHITECTURE.md` → WebSocket patterns
- `ADMIN_USER_GUIDE.md` → Permission model
- `VERCEL_DEPLOYMENT_GUIDE.md` → Deployment steps

## Performance Optimization

**React:**
- Use React.memo for expensive components
- Lazy load routes with React.lazy()
- Optimize re-renders with useCallback, useMemo

**Firebase:**
- Paginate large lists
- Check `firestore.indexes.json` for proper indexing
- Cache frequently accessed data locally

**Build:**
- Manual chunking separates vendor-react
- Tree-shaking removes unused Firebase functions
