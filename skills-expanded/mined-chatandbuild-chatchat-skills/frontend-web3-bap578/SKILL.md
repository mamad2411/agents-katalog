---
id: frontend-web3-bap578
name: Frontend Web3 for BAP-578
description: Use this skill when integrating BAP-578 smart contract reads or writes into a Next.js or React frontend, including wallet connection, chain setup, ABI wiring, hooks, minting flows, and agent-management UI.
category: Blockchain
author: community
version: 1.0.0
---

# Frontend Web3 for BAP-578

Use this skill to integrate BAP-578 smart contract reads and writes into a Next.js/React frontend. This skill covers everything from wallet connection through to building production-quality agent management UIs.

---

## When to use this skill

- Adding Web3 wallet connectivity for BNB Chain or BSC Testnet to a Next.js app.
- Building mint flows, agent dashboards, or identity cards for BAP-578.
- Creating React hooks that wrap contract reads and writes.
- Integrating wagmi, viem, and RainbowKit with the BAP-578 ABI.
- Rendering the four identity questions as UI components.

---

## The Four Identity Questions (Frontend View)

### 1) Who are you?

The UI renders the agent's on-chain identity by reading `getAgentState` and `getAgentMetadata`. Display the token ID, owner address, persona (parsed from JSON), experience text, and logic address. Show active/inactive status with a visual indicator (green dot for active, grey for inactive). If a logic contract is bound, display the address with an indicator that behavior is externally defined.

### 2) What do you remember?

The frontend reads structured metadata from the contract and optionally fetches extended memory from `vaultURI`. To verify vault integrity, the frontend should:

1. Fetch the content at `vaultURI`.
2. Compute `keccak256` of the raw content using viem's `keccak256` utility.
3. Compare the result to the on-chain `vaultHash`.
4. Show a "Verified" badge if they match, or "Unverified" warning if not.

Display on-chain event history by querying past events filtered by token ID: `AgentCreated`, `AgentFunded`, `AgentWithdraw`, `AgentStatusChanged`, `MetadataUpdated`.

### 3) What can you do?

The UI exposes these agent capabilities as interactive forms and buttons:

- **Mint agent** — form with persona, experience, metadata URI, and optional logic address
- **Fund agent** — input for BNB amount, calls `fundAgent`
- **Withdraw** — input for amount, calls `withdrawFromAgent`
- **Toggle status** — switch to call `setAgentStatus`
- **Update metadata** — form for new persona, experience, vault URI
- **Bind logic** — address input for `setLogicAddress`

### 4) How can I trust it?

The frontend only signs transactions through the user's own wallet (MetaMask, WalletConnect, etc.). There is no backend mutation path. Every write goes directly to the on-chain contract. The UI should:

- Show the contract address prominently so users can verify on a block explorer.
- Display transaction hashes after each write for independent verification.
- Never request or store private keys.
- Treat off-chain data as untrusted unless vault hash matches.

---

## Tech Stack

- **Next.js 14+** (App Router recommended)
- **wagmi v2** — React hooks for Ethereum
- **viem** — low-level typed EVM client
- **@tanstack/react-query** — caching layer for wagmi
- **@rainbow-me/rainbowkit** — wallet connection modal
- **TypeScript** — strongly typed throughout

---

## Step-by-Step Integration

### Step 1: Install dependencies

```bash
npm install wagmi viem @tanstack/react-query @rainbow-me/rainbowkit
```

### Step 2: Create Web3 config

Create `config/web3.ts`:

```ts
import { http } from "wagmi";
import { bsc, bscTestnet } from "wagmi/chains";
import { getDefaultConfig } from "@rainbow-me/rainbowkit";

export const wagmiConfig = getDefaultConfig({
  appName: "NFA",
  projectId: process.env.NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID || "",
  chains: [bsc, bscTestnet],
  transports: {
    [bsc.id]: http(process.env.NEXT_PUBLIC_BSC_RPC_URL),
    [bscTestnet.id]: http(process.env.NEXT_PUBLIC_BSC_TESTNET_RPC_URL),
  },
  ssr: true,
});
```

Required env vars in `.env.local`:

```
NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID=your_project_id
NEXT_PUBLIC_BSC_RPC_URL=your_bsc_rpc
NEXT_PUBLIC_BSC_TESTNET_RPC_URL=your_bsc_testnet_rpc
NEXT_PUBLIC_BAP578_ADDRESS=0xYourDeployedAddress
```

### Step 3: Create providers wrapper

Create `components/Web3Provider.tsx`:

```tsx
"use client";

import { WagmiProvider } from "wagmi";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { RainbowKitProvider } from "@rainbow-me/rainbowkit";
import { wagmiConfig } from "@/config/web3";
import "@rainbow-me/rainbowkit/styles.css";

const queryClient = new QueryClient();

export function Web3Provider({ children }: { children: React.ReactNode }) {
  return (
    <WagmiProvider config={wagmiConfig}>
      <QueryClientProvider client={queryClient}>
        <RainbowKitProvider>{children}</RainbowKitProvider>
      </QueryClientProvider>
    </WagmiProvider>
  );
}
```

Add `<Web3Provider>` to your root layout wrapping `{children}`.

### Step 4: Define ABI and contract config

Create `config/bap578.ts`:

```ts
export const BAP578_ADDRESS = process.env.NEXT_PUBLIC_BAP578_ADDRESS as `0x${string}`;

export const BAP578_ABI = [
  // Minting
  {
    name: "createAgent",
    type: "function",
    stateMutability: "payable",
    inputs: [
      { name: "to", type: "address" },
      { name: "logicAddress", type: "address" },
      { name: "metadataURI", type: "string" },
      {
        name: "metadata",
        type: "tuple",
        components: [
          { name: "persona", type: "string" },
          { name: "experience", type: "string" },
          { name: "voiceHash", type: "string" },
          { name: "animationURI", type: "string" },
          { name: "vaultURI", type: "string" },
          { name: "vaultHash", type: "bytes32" },
        ],
      },
    ],
    outputs: [{ name: "tokenId", type: "uint256" }],
  },
  // Funding
  {
    name: "fundAgent",
    type: "function",
    stateMutability: "payable",
    inputs: [{ name: "tokenId", type: "uint256" }],
    outputs: [],
  },
  // Withdrawal
  {
    name: "withdrawFromAgent",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "tokenId", type: "uint256" },
      { name: "amount", type: "uint256" },
    ],
    outputs: [],
  },
  // Status
  {
    name: "setAgentStatus",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "tokenId", type: "uint256" },
      { name: "active", type: "bool" },
    ],
    outputs: [],
  },
  // Logic binding
  {
    name: "setLogicAddress",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "tokenId", type: "uint256" },
      { name: "logicAddress", type: "address" },
    ],
    outputs: [],
  },
  // Metadata update
  {
    name: "updateAgentMetadata",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "tokenId", type: "uint256" },
      { name: "newURI", type: "string" },
      {
        name: "newMetadata",
        type: "tuple",
        components: [
          { name: "persona", type: "string" },
          { name: "experience", type: "string" },
          { name: "voiceHash", type: "string" },
          { name: "animationURI", type: "string" },
          { name: "vaultURI", type: "string" },
          { name: "vaultHash", type: "bytes32" },
        ],
      },
    ],
    outputs: [],
  },
  // Views
  {
    name: "getAgentState",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "tokenId", type: "uint256" }],
    outputs: [
      {
        name: "",
        type: "tuple",
        components: [
          { name: "balance", type: "uint256" },
          { name: "active", type: "bool" },
          { name: "logicAddress", type: "address" },
          { name: "createdAt", type: "uint256" },
          { name: "owner", type: "address" },
        ],
      },
    ],
  },
  {
    name: "getAgentMetadata",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "tokenId", type: "uint256" }],
    outputs: [
      {
        name: "",
        type: "tuple",
        components: [
          { name: "persona", type: "string" },
          { name: "experience", type: "string" },
          { name: "voiceHash", type: "string" },
          { name: "animationURI", type: "string" },
          { name: "vaultURI", type: "string" },
          { name: "vaultHash", type: "bytes32" },
        ],
      },
    ],
  },
  {
    name: "tokensOfOwner",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "owner", type: "address" }],
    outputs: [{ name: "", type: "uint256[]" }],
  },
  {
    name: "getTotalSupply",
    type: "function",
    stateMutability: "view",
    inputs: [],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "getFreeMints",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "user", type: "address" }],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "isFreeMint",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "tokenId", type: "uint256" }],
    outputs: [{ name: "", type: "bool" }],
  },
] as const;
```

### Step 5: Build React hooks

Create `hooks/useBap578.ts`:

```ts
import { useReadContract, useWriteContract, useAccount } from "wagmi";
import { parseEther, zeroAddress, zeroHash } from "viem";
import { BAP578_ADDRESS, BAP578_ABI } from "@/config/bap578";

export function useAgentState(tokenId: bigint) {
  return useReadContract({
    address: BAP578_ADDRESS,
    abi: BAP578_ABI,
    functionName: "getAgentState",
    args: [tokenId],
  });
}

export function useAgentMetadata(tokenId: bigint) {
  return useReadContract({
    address: BAP578_ADDRESS,
    abi: BAP578_ABI,
    functionName: "getAgentMetadata",
    args: [tokenId],
  });
}

export function useOwnedTokens() {
  const { address } = useAccount();
  return useReadContract({
    address: BAP578_ADDRESS,
    abi: BAP578_ABI,
    functionName: "tokensOfOwner",
    args: address ? [address] : undefined,
    query: { enabled: !!address },
  });
}

export function useFreeMints() {
  const { address } = useAccount();
  return useReadContract({
    address: BAP578_ADDRESS,
    abi: BAP578_ABI,
    functionName: "getFreeMints",
    args: address ? [address] : undefined,
    query: { enabled: !!address },
  });
}

export function useMintAgent() {
  const { writeContract, ...rest } = useWriteContract();
  const mint = (params: {
    to: `0x${string}`;
    persona: string;
    experience: string;
    metadataURI: string;
    value?: bigint;
  }) => {
    writeContract({
      address: BAP578_ADDRESS,
      abi: BAP578_ABI,
      functionName: "createAgent",
      args: [
        params.to,
        zeroAddress,
        params.metadataURI,
        {
          persona: params.persona,
          experience: params.experience,
          voiceHash: "",
          animationURI: "",
          vaultURI: "",
          vaultHash: zeroHash,
        },
      ],
      value: params.value ?? 0n,
    });
  };
  return { mint, ...rest };
}

export function useFundAgent() {
  const { writeContract, ...rest } = useWriteContract();
  const fund = (tokenId: bigint, amountBnb: string) => {
    writeContract({
      address: BAP578_ADDRESS,
      abi: BAP578_ABI,
      functionName: "fundAgent",
      args: [tokenId],
      value: parseEther(amountBnb),
    });
  };
  return { fund, ...rest };
}

export function useWithdrawFromAgent() {
  const { writeContract, ...rest } = useWriteContract();
  const withdraw = (tokenId: bigint, amountBnb: string) => {
    writeContract({
      address: BAP578_ADDRESS,
      abi: BAP578_ABI,
      functionName: "withdrawFromAgent",
      args: [tokenId, parseEther(amountBnb)],
    });
  };
  return { withdraw, ...rest };
}
```

### Step 6: Build UI components

**Recommended component set:**

- `WalletButton` — uses `<ConnectButton />` from RainbowKit
- `MintAgentForm` — collects persona, experience, URI; calls `useMintAgent`
- `AgentDashboard` — lists owned tokens via `useOwnedTokens`, renders cards
- `AgentIdentityCard` — displays one agent's four-question profile
- `FundAgentForm` — BNB amount input, calls `useFundAgent`
- `WithdrawAgentForm` — amount input, calls `useWithdrawFromAgent`
- `AgentStatusToggle` — switch that calls `setAgentStatus`
- `VaultVerifier` — fetches vault URI, hashes content, compares to on-chain hash

---

## Vault Verification Pattern

```ts
import { keccak256, toHex } from "viem";

async function verifyVault(vaultURI: string, onChainHash: `0x${string}`) {
  const res = await fetch(vaultURI);
  const content = await res.text();
  const hash = keccak256(toHex(content));
  return hash === onChainHash;
}
```

Display a green "Verified" badge if true, or a red "Unverified — data may have been tampered with" warning if false. If `vaultHash` is the zero hash, display "No vault data registered".

---

## Event History Display

Use viem's `getContractEvents` to fetch historical events for a token:

```ts
import { publicClient } from "@/config/web3";
import { BAP578_ADDRESS, BAP578_ABI } from "@/config/bap578";

async function getAgentHistory(tokenId: bigint) {
  const events = await publicClient.getContractEvents({
    address: BAP578_ADDRESS,
    abi: BAP578_ABI,
    fromBlock: 0n,
    toBlock: "latest",
  });
  return events.filter((e) => {
    const args = e.args as Record<string, unknown>;
    return args.tokenId === tokenId;
  });
}
```

Render these as a timeline component showing creation, funding, withdrawals, status changes, and metadata updates with timestamps and transaction hashes.

---

## Constraints and Safety Rules

- **Free mints must go to self.** The UI should auto-set `to` = connected address when free mints remain.
- **Send exact fee.** After free mints are exhausted, send the exact mint fee. Read the fee from the contract or config.
- **No private keys.** Never ask for or store private keys. All signing happens in the wallet.
- **Untrusted off-chain data.** Always verify vault content against `vaultHash` before displaying.
- **Chain switching.** Prompt users to switch to BNB Chain if they are on the wrong network.
- **Error handling.** Catch and display user-friendly messages for common revert reasons.

---

## Common Frontend Errors and Fixes

- **"User rejected transaction"** — user declined in wallet; no action needed.
- **"Insufficient funds"** — not enough BNB for gas + value; show balance warning.
- **"Execution reverted: incorrect fee"** — free mints exhausted; recalculate fee.
- **"Execution reverted: not token owner"** — wrong wallet connected.
- **"Execution reverted: contract is paused"** — admin has paused; show notice.

---

## Output Format

When asked for frontend help, respond with:

1. **Components/files to create or modify**
2. **Complete code snippets** (not fragments)
3. **Env vars required**
4. **How to test the flow** (connect wallet → perform action → verify result)
5. **Error handling notes**

---

## Mobile Considerations

### Responsive design

The BAP-578 frontend should work on mobile devices where most Web3 users interact:

- Use responsive layouts (CSS Grid/Flexbox) for agent cards
- Make wallet connect buttons large and touch-friendly
- Simplify forms on mobile (collapsible metadata fields)
- Test with mobile wallets (MetaMask Mobile, Trust Wallet)

### Deep linking

Support deep links to specific agents for sharing:

```
https://app.example.com/agent/17
https://app.example.com/owner/0xABC...
```

### Progressive Web App (PWA)

Consider PWA support for mobile users who want an app-like experience:
- Offline agent profile caching
- Push notifications for funding and status events
- Home screen installation

---

## Accessibility

- Use semantic HTML for agent cards and forms
- Provide alt text for agent animation assets
- Ensure wallet address displays are screen-reader friendly (e.g., "Address starting with 0 x A B C")
- Support keyboard navigation for all interactive elements
- Use ARIA labels on custom components (status toggles, fund buttons)
- Ensure color contrast meets WCAG 2.1 AA standards

---

## Related Skills

- `bap578`
- `bap578-scanner`
- `bap578-metadata-design`
