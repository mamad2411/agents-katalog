---
description: Star World Order - Web3 DAO for Star Skrumpey NFT holders on Monad blockchain. Retro N64/synthwave UI.
globs:
  - "**/*.ts"
  - "**/*.tsx"
  - "**/*.js"
  - "**/*.jsx"
  - "**/*.sol"
alwaysApply: false
---

# Star World Order - Cursor Agent Rules

> **Sub-DAO for Star Skrumpey NFT holders on Monad blockchain (Chain ID: 143)**
> For comprehensive documentation, see `CLAUDE.md` in the repository root.

---

## ⚡ Critical Rules (MUST FOLLOW)

### 1. PR Workflow
```bash
# ⚠️ ALL PRs MUST target `dev` branch, NOT `main`
git checkout dev
git checkout -b feature/your-feature
```

### 2. Pre-Commit Validation
```bash
# ALWAYS run before committing (all must pass):
npm run type-check && npm run lint && npm run build
```

### 3. Anti-Patterns to Avoid

| ❌ DON'T | ✅ DO |
|----------|-------|
| Fetch NFT metadata from IPFS | Use `getStarSkrumpeyMetadataBatch()` from `lib/db` |
| Sequential RPC calls in loops | Use `checkStarOwnershipBatched()` from `lib/starSkrumpey` |
| Hardcode RPC endpoints | Use `getResilientClient()` from `lib/rpcClient` |
| Use `any` type in TypeScript | Define proper interfaces |
| Create PRs targeting `main` | Target `dev` branch |

---

## 🛠️ Tech Stack

| Layer | Technology | Version |
|-------|------------|---------|
| Frontend | Next.js | 16 |
| UI Framework | React | 19 |
| Language | TypeScript | 5.9+ |
| Styling | Tailwind CSS | 4 |
| Web3 | Wagmi 3 + Viem 2 | |
| Database | SQLite | better-sqlite3 |
| Blockchain | Monad | Chain ID: 143 |

---

## 🎨 Synthwave Theme (Required)

```css
/* Color palette - use in Tailwind classes */
--neon-cyan: #00f7ff      /* Primary: text-[#00f7ff], border-[#00f7ff] */
--neon-magenta: #ff00ff   /* Accent: text-[#ff00ff] */
--neon-gold: #ffd700      /* Highlight: text-[#ffd700] */
--deep-purple: #1a0033    /* Background: bg-[#1a0033] */
--dark-navy: #0a0015      /* Dark bg: bg-[#0a0015] */
```

**Typography**: Use `font-['Press_Start_2P']` for headings

**Standard Card**:
```tsx
<div className="bg-black/80 backdrop-blur-md border border-[#00f7ff]/30 rounded-lg p-4 shadow-[0_0_15px_rgba(0,247,255,0.3)]">
```

**Neon Button**:
```tsx
<button className="px-4 py-2 bg-[#00f7ff]/20 hover:bg-[#00f7ff]/30 border border-[#00f7ff] text-[#00f7ff] rounded transition-all hover:shadow-[0_0_10px_#00f7ff]">
```

---

## 📁 Key File Locations

| Purpose | File(s) |
|---------|---------|
| Environment config | `lib/config.ts` |
| Database operations | `lib/db.ts` (3500+ lines) |
| Star Skrumpey verification | `lib/starSkrumpey.ts` |
| RPC client with fallback | `lib/rpcClient.ts` |
| Wagmi/chain config | `lib/wagmi.ts` |
| API routes | `app/api/*/route.ts` |
| React components | `components/*.tsx` |
| Page components | `app/*/page.tsx` |
| **Full documentation** | `CLAUDE.md` |

---

## 🔧 Quick Patterns

### New API Endpoint

```typescript
// app/api/example/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const param = searchParams.get('param');
    if (!param) return NextResponse.json({ error: 'Missing param' }, { status: 400 });
    return NextResponse.json({ success: true, data: param });
  } catch (error) {
    console.error('API Error:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
```

### New React Component

```typescript
// components/NewComponent.tsx
'use client';

interface NewComponentProps {
  title: string;
  onAction?: () => void;
}

export default function NewComponent({ title, onAction }: NewComponentProps) {
  return (
    <div className="bg-black/80 border border-[#00f7ff]/30 rounded-lg p-4">
      <h2 className="text-[#00f7ff] font-['Press_Start_2P'] text-sm">{title}</h2>
      {onAction && (
        <button onClick={onAction} className="mt-2 px-4 py-2 bg-[#00f7ff]/20 hover:bg-[#00f7ff]/30 border border-[#00f7ff] text-[#00f7ff] rounded">
          Action
        </button>
      )}
    </div>
  );
}
```

### Web3 Interactions

```typescript
import { useReadContract, useWriteContract } from 'wagmi';

// Read
const { data } = useReadContract({
  address: CONTRACT_ADDRESS,
  abi: CONTRACT_ABI,
  functionName: 'balanceOf',
  args: [userAddress],
});

// Write
const { writeContract } = useWriteContract();
writeContract({ address, abi, functionName, args });
```

### Database Table

```typescript
// In lib/db.ts initDatabase()
db.exec(`
  CREATE TABLE IF NOT EXISTS new_table (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    wallet_address TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
  );
  CREATE INDEX IF NOT EXISTS idx_new_table_wallet ON new_table(wallet_address);
`);
```

---

## 📋 Checklist

### Before Starting
- [ ] Read relevant `CLAUDE.md` sections
- [ ] Check existing patterns in similar files

### Before Committing
- [ ] `npm run type-check` passes
- [ ] `npm run lint` passes
- [ ] `npm run build` succeeds
- [ ] PR targets `dev` branch (NOT `main`)

---

## 🔗 Quick Reference

| Resource | Value |
|----------|-------|
| Live Site | https://starworldorder.com |
| Repository | https://github.com/InverseAltruism/Star-World-Order |
| NFT Contract | `0xb0dad798c80e40dd6b8e8545074c6a5b7b97d2c0` |
| Chain ID | 143 (Monad Mainnet) |
| RPC | https://rpc.monad.xyz |
| Explorer | https://monadscan.com |

---

**For database schemas, API endpoints, deployment commands, and more details → See `CLAUDE.md`**
