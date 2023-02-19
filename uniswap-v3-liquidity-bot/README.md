# Uniswap V3 Liquidity Event Bot

## Description

This agent detects liquidity pool transactions on Uniswap V3.

This is intended as a relatively simple example of a Forta bot constructed using Python. Instructions on building a Forta bot can be found at https://docs.forta.network/en/latest/getting-started/ and https://chainstack.com/forta-for-realtime-monitoring-and-security-of-your-smart-contract/.

## Supported Chains

- Ethereum

## Alerts

- FORTA-1
  - Fired when a liquidity pool transaction occurs on Uniswap V3
  - Severity is always set to "low"
  - Type is always set to "info"
  - Metadata includes token sender and recipient, event/transaction type and liquidity token ID

## Test Data

The agent behaviour can be verified with the following transactions:

- 0x46eec757d329fda9bdc935c331b2e0ca25680bc76b6062871adc963483cb70fc (Mint / open new position)
- 0x60b6b799bf6abb3a932a0d1917e67d66364a37271a72379e2fe3ab580c178304 (Burn / close position)
