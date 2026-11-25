# Anchor / Solana workflow

1. `/crypto-devkit:new-solana program_name`
2. `anchor build && anchor test`
3. Review PDA seeds and signers
4. `/crypto-devkit:audit`
5. `anchor deploy --provider.cluster devnet`

See `docs/chains/solana.md`.
