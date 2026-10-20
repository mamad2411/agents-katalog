---
name: binance-capability-router
description: Accounts for and safely routes the Binance skill collection observed on E drive without republishing unlicensed source text. Use for Binance account, market, Web3, trading, payment, loan, earn, or token-information requests only when an authorized Binance connector exposes the required operation.
license: MIT
metadata:
  authority: Creator/Human Authority > LeeWay Standards
  observed-source: binance/binance-skills-hub@084e3a637b197674e451f5ab45a9d75ab73b08f2
  manifest: config/external-binance-capabilities.json
  source-state: catalogued-not-vendored-no-license-file
---

# Binance Capability Router

Read `config/external-binance-capabilities.json`, select the smallest matching capability, then verify that an authorized connector exposes it. The observed source files are discovery evidence, not installed executors.

Market-data reads and educational explanations remain distinct from authenticated account reads, transfers, borrowing, order placement, derivatives, margin, earning products, payments, and publishing. Consequential financial operations require exact account, asset, network, amount, side, order type, limits, fees, risk acknowledgement, and explicit human confirmation through the live connector.

Never claim a price, balance, audit result, transaction, order, post, payment, loan, or yield was obtained or executed unless the connector returned fresh evidence. Never request seed phrases or private keys.
