---
# Custom Agent Configuration Template for Snipe Platform
# 
# This template helps you create specialized AI agents for the Snipe Web3 trading platform.
# The Copilot CLI can be used for local testing: https://gh.io/customagents/cli
# To make this agent available, merge this file into the default repository branch.
# For format details, see: https://gh.io/customagents/config
#
# INSTRUCTIONS:
# 1. Copy this file and rename it (e.g., firebase-expert.agent.md, wallet-specialist.agent.md)
# 2. Fill in the name and description fields below
# 3. Replace the template content with your agent's specific instructions
# 4. Test locally using the Copilot CLI
# 5. Commit and merge to enable the agent

name: Custom Agent Template
description: Template for creating specialized agents for the Snipe platform
---

# Custom Agent Template

## Purpose
[Describe what this agent specializes in - e.g., Firebase integration, wallet connections, admin system, etc.]

## Expertise Areas
- [Area 1: e.g., Real-time data with Firebase Firestore]
- [Area 2: e.g., Multi-wallet provider integration]
- [Area 3: e.g., Security and authentication]

## Key Responsibilities
1. [Responsibility 1]
2. [Responsibility 2]
3. [Responsibility 3]

## Platform-Specific Knowledge

### Architecture Context
- **Frontend**: React 18 + Vite in `Onchainweb/`
- **Backend**: Firebase (Firestore + Auth) - primary backend
- **Legacy**: Express/MongoDB in `backend/` (deprecated - do not add features)
- **Fallback**: localStorage when Firebase is unavailable

### Critical Files to Know
- `src/lib/firebase.js` - Firebase singleton (never reinitialize)
- `src/config/firebase.config.js` - Configuration and COLLECTIONS
- `src/lib/walletConnect.jsx` - Wallet integration (11 providers)
- `src/lib/adminAuth.js` - Admin permissions and roles
- `src/lib/errorHandling.js` - Error formatting utilities

### Environment Variables Required
```bash
VITE_FIREBASE_API_KEY
VITE_FIREBASE_AUTH_DOMAIN
VITE_FIREBASE_PROJECT_ID
VITE_FIREBASE_STORAGE_BUCKET
VITE_FIREBASE_MESSAGING_SENDER_ID
VITE_FIREBASE_APP_ID
VITE_FIREBASE_MEASUREMENT_ID
VITE_WALLETCONNECT_PROJECT_ID
```

## Code Patterns to Follow

### Firebase Integration
```javascript
// ALWAYS check isFirebaseAvailable before Firebase operations
import { db, isFirebaseAvailable } from './lib/firebase';

if (isFirebaseAvailable) {
  // Use Firebase
  const docRef = await setDoc(doc(db, 'collection', id), data);
} else {
  // Fallback to localStorage
  localStorage.setItem(`key_${id}`, JSON.stringify(data));
}
```

### Real-time Listeners (Never Poll)
```javascript
// Use onSnapshot for real-time updates
useEffect(() => {
  if (!isFirebaseAvailable) return;
  
  const unsubscribe = onSnapshot(
    collection(db, 'trades'),
    (snapshot) => {
      setData(snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() })));
    }
  );
  
  return () => unsubscribe(); // ALWAYS clean up
}, []);
```

### Error Handling
```javascript
import { formatApiError, formatWalletError } from './lib/errorHandling';

try {
  // operation
} catch (error) {
  const message = formatApiError(error); // or formatWalletError for wallet ops
  setError(message);
}
```

## Development Commands
```bash
# Start development server
cd Onchainweb && npm install && npm run dev  # Port 5173

# Build for production
npm run build

# Preview production build
npm run preview

# Deploy Firebase rules/indexes
firebase deploy --only firestore:rules
firebase deploy --only firestore:indexes
```

## Critical Guidelines
1. **Never reinitialize Firebase** - Always reuse the singleton from `src/lib/firebase.js`
2. **Always check `isFirebaseAvailable`** before Firebase operations
3. **Use onSnapshot listeners** - Never poll with setInterval
4. **Clean up listeners** - Always return unsubscribe in useEffect
5. **Support 11 wallet providers** - See walletConnect.jsx for implementation
6. **Respect admin permissions** - Check roles (master/admin/user) and permission flags
7. **Never commit .env files** - Use .env.example as template
8. **Never request private keys** - Only work with wallet addresses

## Common Issues & Solutions

### Issue: Firebase not initializing
**Solution**: Check that all 7 Firebase env vars are set in `Onchainweb/.env`

### Issue: Cold starts or polling delays
**Solution**: Use onSnapshot listeners, not setInterval polling

### Issue: Wallet connection failures
**Solution**: Check provider availability, use injected → deep link → WalletConnect QR fallback

### Issue: Admin access denied
**Solution**: Verify email in `VITE_ADMIN_ALLOWLIST` and check permission flags

## Testing Checklist
- [ ] Firebase operations gracefully fallback to localStorage
- [ ] Real-time listeners properly clean up on unmount
- [ ] Wallet connections work across all 11 providers
- [ ] Admin permissions enforced correctly
- [ ] No Firebase singleton reinitialization
- [ ] All error messages use formatApiError/formatWalletError
- [ ] No .env files committed

## Documentation References
- `QUICK_START_GUIDE.md` - Environment setup
- `BACKEND_REPLACEMENT.md` - Firebase-first architecture rationale
- `REALTIME_DATA_ARCHITECTURE.md` - Listener patterns and best practices
- `ADMIN_USER_GUIDE.md` - Admin system and permissions
- `VERCEL_DEPLOYMENT_GUIDE.md` - Deployment procedures

## Example Agent Configurations

### Firebase Expert Agent
```markdown
name: Firebase Integration Specialist
description: Expert in Firebase Firestore operations, real-time listeners, and security rules for the Snipe platform
```

### Wallet Connection Agent
```markdown
name: Wallet Connection Specialist  
description: Expert in multi-provider wallet integration (MetaMask, Trust, WalletConnect, etc.) for Web3 applications
```

### Admin System Agent
```markdown
name: Admin & Permissions Specialist
description: Expert in role-based access control, permission management, and admin system for the Snipe platform
```

## Notes for Agent Creators
- Keep agent scope focused on a specific domain (Firebase, wallets, admin, etc.)
- Reference this template for platform-specific context
- Test thoroughly with both Firebase and localStorage fallback modes
- Ensure compatibility with all 11 supported wallet providers
- Follow the existing code patterns and conventions
