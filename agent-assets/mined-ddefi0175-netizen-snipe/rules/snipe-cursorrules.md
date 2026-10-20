# Cursor AI Rules for Snipe Platform

## Project: Web3 Trading Platform (React + Vite + Firebase)

### Critical Architecture: Firebase-First + localStorage Fallback

**ALWAYS check `isFirebaseAvailable` before Firebase operations**
```javascript
if (isFirebaseAvailable) {
  // Use Firebase
  await setDoc(doc(db, 'users', userId), data);
} else {
  // Fallback: localStorage
  localStorage.setItem(`user_${userId}`, JSON.stringify(data));
}
```

### Key Files & Patterns

**Firebase Services:**
- `src/lib/firebase.js` - Main singleton (check `isFirebaseAvailable` flag)
- `src/config/firebase.config.js` - Centralized env vars, COLLECTIONS const

**Wallet Integration:**
- `src/lib/walletConnect.jsx` - 11+ wallets, injected → WalletConnect fallback
- STORAGE_KEYS for persistence (wallet_address, wallet_chainId, etc.)

**Error Handling:**
- `src/lib/errorHandling.js` - Use `formatApiError(error)` for consistency
- Cold-start aware messages for Render deployments

**Admin System:**
- `src/lib/adminAuth.js` - Role-based permissions (master/admin/user)
- Email allowlist via `VITE_ADMIN_ALLOWLIST`

### Development Commands

```bash
cd Onchainweb && npm run dev     # Dev server → localhost:5173
npm run build                     # Production build
npm run preview                   # Preview dist/
```

### Required Environment Variables (.env)

```
VITE_FIREBASE_API_KEY
VITE_FIREBASE_AUTH_DOMAIN
VITE_FIREBASE_PROJECT_ID
VITE_FIREBASE_STORAGE_BUCKET
VITE_FIREBASE_MESSAGING_SENDER_ID
VITE_FIREBASE_APP_ID
VITE_FIREBASE_MEASUREMENT_ID
VITE_WALLETCONNECT_PROJECT_ID
```

### Code Patterns to Follow

**Real-Time Listeners (NOT polling):**
```javascript
useEffect(() => {
  if (!isFirebaseAvailable) return;
  const unsubscribe = onSnapshot(doc(db, 'users', userId), (doc) => {
    setUserData(doc.data());
  });
  return () => unsubscribe(); // Always cleanup
}, [userId]);
```

**Loading States:**
```javascript
const [loading, setLoading] = useState(false);
const handleAction = async () => {
  setLoading(true);
  try {
    await performAction();
  } finally {
    setLoading(false); // Always reset
  }
};
```

**Error Handling:**
```javascript
try {
  await operation();
} catch (error) {
  showNotification(formatApiError(error)); // Use centralized formatter
}
```

### Build Configuration

- **Manual chunking**: vendor-react split in vite.config.js
- **Chunk size limit**: 1000kB (Firebase + WalletConnect are large)
- **JSX loader**: esbuild handles .js + .jsx files

### Never Do

- ❌ DON'T poll Firebase (use onSnapshot)
- ❌ DON'T reinitialize Firebase (singleton pattern)
- ❌ DON'T use deprecated `src/lib/api.js` (legacy MongoDB)
- ❌ DON'T commit .env files
- ❌ DON'T request private keys from wallets

### Always Do

- ✅ Check `isFirebaseAvailable` before Firebase calls
- ✅ Implement localStorage fallback for offline scenarios
- ✅ Use `formatApiError()` for error messages
- ✅ Cleanup Firebase listeners in useEffect return
- ✅ Use React.memo, useCallback, useMemo for performance
- ✅ Test wallet connections: MetaMask + WalletConnect QR

### Tech Stack

- React 18 + Vite 5.4.21 (ES modules)
- Firebase (Firestore, Auth, Realtime DB)
- Tailwind CSS v4 (PostCSS)
- WalletConnect v2 + EIP-6963
- No Redux (Context API only)

### Documentation References

- QUICK_START_GUIDE.md - Setup in 5 min
- BACKEND_REPLACEMENT.md - Why Firebase
- REALTIME_DATA_ARCHITECTURE.md - WebSocket patterns
- ADMIN_USER_GUIDE.md - Permission model
- VERCEL_DEPLOYMENT_GUIDE.md - Deploy steps
