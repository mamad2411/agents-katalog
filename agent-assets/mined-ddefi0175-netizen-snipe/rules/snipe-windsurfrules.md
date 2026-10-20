# Windsurf AI Rules for Snipe Platform

## Project Overview
Web3 trading platform with React + Vite frontend, Firebase backend, multi-wallet support (11+ providers), and real-time data synchronization.

## Critical Architecture Pattern

### Dual-Layer Design: Firebase Primary + localStorage Fallback

The codebase gracefully handles missing Firebase credentials by falling back to localStorage. Always implement features with this pattern:

```javascript
export const saveData = async (data) => {
  if (!isFirebaseAvailable) {
    // Fallback: localStorage
    localStorage.setItem('key', JSON.stringify(data));
  } else {
    // Primary: Firestore
    await addDoc(collection(db, 'collectionName'), data);
  }
};
```

## Directory Structure

```
Onchainweb/src/
├── config/firebase.config.js    # Env vars, COLLECTIONS constants
├── lib/
│   ├── firebase.js              # Main service (singleton, check isFirebaseAvailable)
│   ├── walletConnect.jsx        # Universal wallet detection + connection
│   ├── errorHandling.js         # formatApiError(), formatWalletError()
│   ├── adminAuth.js             # Role permissions, email allowlist
│   └── api.js                   # DEPRECATED (don't use)
├── services/
│   ├── firebase.service.js      # Secondary wrapper (consider consolidating)
│   ├── database.service.js      # CRUD abstraction
│   └── api.service.js           # Retry logic wrapper
└── components/
    ├── WalletGateUniversal.jsx  # First render wallet gate
    ├── UniversalWalletModal.jsx # Wallet selection UI
    ├── MasterAdminDashboard.jsx # Master controls
    └── AdminPanel.jsx           # Admin features by permission
```

## Core Patterns

### 1. Firebase Real-Time Listeners (Core Pattern)
```javascript
// ✅ DO: Real-time listener
useEffect(() => {
  const unsubscribe = onSnapshot(doc(db, 'users', userId), (doc) => {
    setUserData(doc.data());
  });
  return () => unsubscribe();
}, [userId]);

// ❌ DON'T: Polling
setInterval(() => fetchUser(), 3000);
```

### 2. Wallet Connection Flow
- **11 wallets**: MetaMask, Trust, Coinbase, OKX, Phantom, Binance, TokenPocket, Rainbow, Ledger, imToken, WalletConnect
- **Strategy**: Try injected → deep link → WalletConnect QR
- **Persistence**: STORAGE_KEYS in localStorage
- **Chains**: Ethereum, BSC, Polygon, Arbitrum, Optimism, Avalanche, Fantom

### 3. Firebase Initialization
- **Singleton pattern**: Initialize once in `src/lib/firebase.js`
- **No exceptions on init**: Check `isFirebaseAvailable` flag
- **Never reinitialize**: Reuse `app`, `db`, `auth` exports

### 4. Error Handling
```javascript
import { formatApiError } from './lib/errorHandling';

try {
  await operation();
} catch (error) {
  showNotification(formatApiError(error)); // Centralized, cold-start aware
}
```

### 5. Admin Authentication
- **Roles**: `master` (full), `admin` (scoped), `user` (wallet-only)
- **Permissions**: manageUsers, manageBalances, manageTrades, viewReports, etc.
- **Access modes**: `all` users vs `assigned` users only
- **Allowlist**: `VITE_ADMIN_ALLOWLIST` env var

## Development Workflow

### Commands
```bash
cd Onchainweb && npm run dev    # → http://localhost:5173
npm run build                    # Production build → dist/
npm run preview                  # Preview dist/
```

### Environment Variables (Required)
Create `Onchainweb/.env`:
```env
VITE_FIREBASE_API_KEY=...
VITE_FIREBASE_AUTH_DOMAIN=...
VITE_FIREBASE_PROJECT_ID=...
VITE_FIREBASE_STORAGE_BUCKET=...
VITE_FIREBASE_MESSAGING_SENDER_ID=...
VITE_FIREBASE_APP_ID=...
VITE_FIREBASE_MEASUREMENT_ID=...
VITE_WALLETCONNECT_PROJECT_ID=...
```

### First Time Setup
1. Install Node 18+
2. `cd Onchainweb && npm install`
3. Ensure `.env` has all 8 Firebase vars
4. `npm run dev`

### Adding a Feature
1. Identify data source: Firebase or localStorage?
2. Implement with fallback pattern
3. Use real-time listeners (not polling)
4. Add error handling with `formatApiError()`
5. Test with Firebase Console

## Build Configuration

- **vite.config.js**: Manual chunking (vendor-react split)
- **Chunk size limit**: 1000kB (Firebase + WalletConnect are large)
- **JSX loader**: esbuild handles `.js` + `.jsx`
- **Base path**: `'/'` (Vercel + custom domains)

## Code Quality Standards

### Always Do
- ✅ Check `isFirebaseAvailable` before Firebase operations
- ✅ Implement localStorage fallback for offline
- ✅ Cleanup listeners in useEffect return
- ✅ Use `formatApiError()` for consistency
- ✅ Use React.memo, useCallback, useMemo for performance
- ✅ Test MetaMask + WalletConnect QR flows

### Never Do
- ❌ Poll Firebase (use onSnapshot)
- ❌ Reinitialize Firebase singleton
- ❌ Use `src/lib/api.js` (deprecated MongoDB API)
- ❌ Commit `.env` or credentials
- ❌ Request private keys from wallets

## Tech Stack
- **Frontend**: React 18 + Vite 5.4.21
- **Backend**: Firebase (Firestore + Auth + Realtime DB)
- **Styling**: Tailwind CSS v4 (PostCSS)
- **Wallet**: WalletConnect v2 + EIP-6963
- **State**: Context API (no Redux)

## Documentation
- `QUICK_START_GUIDE.md` - 5-min setup
- `BACKEND_REPLACEMENT.md` - Firebase architecture
- `REALTIME_DATA_ARCHITECTURE.md` - WebSocket patterns
- `ADMIN_USER_GUIDE.md` - Permissions
- `VERCEL_DEPLOYMENT_GUIDE.md` - Deploy guide

## Debugging
- **F12 Console**: Firebase init errors
- **Firebase Console**: Verify data structure
- **Network Tab**: Firestore API calls
- **Check Flag**: `isFirebaseAvailable` determines data source
