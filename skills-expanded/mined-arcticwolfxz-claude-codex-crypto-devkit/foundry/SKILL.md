# Foundry workflow (macOS)

Use for EVM projects on Base, Ethereum, Arbitrum, Polygon.

1. `/crypto-devkit:new-evm TokenName`
2. `forge init` if greenfield
3. `forge install OpenZeppelin/openzeppelin-contracts`
4. `/crypto-devkit:test`
5. `/crypto-devkit:audit`
6. `/crypto-devkit:deploy-testnet base`

Always `.env` in `.gitignore`. Use macOS Keychain for deploy keys.
