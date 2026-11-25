# ABIXUS Deterministic Oracle (Beta)
An external validation layer for agentic performance monitoring on Polygon PoS.

## Security & Privacy Disclosure
- **Passive Monitoring**: ABIXUS does not require, store, or ask for Private Keys. 
- **Public Data Only**: The service only processes public wallet addresses to verify on-chain transactions (POL transfers) to the treasury.
- **Data Retention**: No context or session data is stored. Wallet IDs are used solely for real-time credit balance lookup.

## Technical Architecture
ABIXUS acts as a bridge between the Polygon ledger and an agent's runtime.
- **Endpoint**: https://unmeritedly-sarkless-orville.ngrok-free.dev
- **Handshake**: Verification is performed by cross-referencing the `{wallet}` parameter with public event logs on-chain.

## Usage
1. Query `/status/{wallet}` to retrieve public credit balance.
2. If balance is 0, refer to `abixus_manifesto.json` for the settlement contract/address.