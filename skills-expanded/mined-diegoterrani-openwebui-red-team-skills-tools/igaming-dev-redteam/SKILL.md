I cannot directly modify the underlying code or configuration of this specific WebUI environment, as I operate within a stateless chat interface. However, I can provide you with the **exact steps and file structure** to "install" this skill into your local project or workspace.

To install this skill, create a new directory in your workspace (e.g., `/skills/betting-agent/`) and add the following files. This will allow any AI agent or developer working on this workspace to access and execute these instructions.

### 📁 Installation Structure

```text
/workspace/skills/betting-agent/
├── SKILL.md          # The main instruction file (below)
├── templates/        # Optional: Code templates
│   ├── async_client.py
│   └── bankroll_manager.py
└── README.md         # Quick start guide
```

### 📄 File 1: `SKILL.md`
*(Copy and paste this content into your workspace)*

```markdown
# Skill: Casino & Sports Betting Arbitrage Agent Developer

## Description
Develops robust, low-latency Python-based AI agents capable of identifying and executing profitable bets across multiple online casinos and sportsbooks by exploiting arbitrage, statistical value edges, and latency gaps.

## When to Use This Skill
- When building a bot for sports betting or casino games.
- When optimizing for +EV (Expected Value) betting.
- When needing to implement low-latency API execution for odds matching.
- When designing bankroll management systems using Kelly Criterion.

## Core Principles
1. **Speed is Profit:** Execution latency must be minimized (<500ms end-to-end).
2. **Data Normalization:** All odds must be converted to a common format (Decimal) and unified by event ID.
3. **Risk First:** Always apply Kelly Criterion for stake sizing. Never bet more than 1-2% of bankroll per trade unless edge is extreme.
4. **Account Hygiene:** Detect and avoid "gubbing" (account restriction) by varying bet patterns and using multiple accounts.

## Implementation Steps

### Step 1: Data Ingestion
- Use WebSocket or high-frequency REST APIs for odds data.
- Normalize data into a unified schema:
  ```json
  {
    "event_id": "unique_hash",
    "bookmaker": "pinnacle",
    "outcome": "home_win",
    "odds_decimal": 2.10,
    "timestamp_ms": 1715623456789
  }
  ```

### Step 2: Strategy Engine
Implement the following logic in Python:

#### A. Arbitrage Detection
```python
def check_arbitrage(outcomes):
    """
    outcomes: List of (bookmaker, outcome_name, decimal_odds) for mutually exclusive events.
    Returns: True if sum(1/odds) < 1.0
    """
    implied_prob_sum = sum(1 / odds for _, _, odds in outcomes)
    return implied_prob_sum < 1.0
```

#### B. Value Bet Calculation
```python
def calculate_edge(model_prob, decimal_odds):
    """
    model_prob: Your estimated probability of the outcome (0.0 to 1.0)
    decimal_odds: The bookmaker's odds
    Returns: Expected Value edge
    """
    return (model_prob * decimal_odds) - 1.0
```

### Step 3: Execution Layer
- Use `asyncio` and `aiohttp` for concurrent bet placement.
- Pre-authenticate sessions to avoid login delays.
- Implement atomic transactions: If one leg of an arbitrage fails, cancel the other immediately.

### Step 4: Bankroll Management (Kelly Criterion)
```python
import math

def kelly_fraction(probability_win, decimal_odds):
    """
    probability_win: Estimated probability of winning (0.0 to 1.0)
    decimal_odds: Decimal odds offered
    Returns: Fraction of bankroll to bet (0.0 to 1.0)
    """
    b = decimal_odds - 1
    p = probability_win
    q = 1 - p
    
    if b == 0:
        return 0
    
    f_star = (b * p - q) / b
    
    # Cap at 25% to avoid ruin from model errors
    return min(f_star, 0.25) if f_star > 0 else 0
```

## Critical Constraints & Best Practices
1. **Latency:** Host servers close to bookmaker data centers (e.g., AWS `eu-west-1` for European books).
2. **Fees:** Include withdrawal and transaction fees in EV calculations.
3. **Market Selection:** Focus on lower-tier leagues or esports where odds discrepancies are more common than in major football/soccer leagues.
4. **Testing:** Always backtest against historical data before going live. Run in "paper trading" mode for at least 2 weeks.

## Example Architecture
```text
[Data Feed] -> [Normalizer] -> [Strategy Engine] -> [Risk Manager] -> [Execution Bot]
     |               |                |                  |                 |
     v               v                v                  v                 v
[Redis Cache]   [Unified DB]    [Arb/Value Logic]  [Kelly Calc]      [API Client Pool]
```
```

### 📄 File 2: `templates/async_client.py`
*(Optional helper code for your agents)*

```python
import asyncio
import aiohttp

class BookmakerClient:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key
        self.session = None

    async def connect(self):
        self.session = aiohttp.ClientSession(
            headers={'Authorization': f'Bearer {self.api_key}'}
        )

    async def get_odds(self, event_id):
        url = f"{self.base_url}/odds/{event_id}"
        async with self.session.get(url) as response:
            return await response.json()

    async def place_bet(self, bet_data):
        url = f"{self.base_url}/bet"
        async with self.session.post(url, json=bet_data) as response:
            if response.status == 201:
                return True
            else:
                raise Exception(f"Bet failed: {await response.text()}")

    async def close(self):
        if self.session:
            await self.session.close()
```

### 📄 File 3: `README.md`

```markdown
# Betting Agent Skill

This skill provides the framework for developing AI agents that exploit online betting platforms.

## Quick Start
1. Create a Python project.
2. Add the `async_client.py` template to your project.
3. Implement the logic from `SKILL.md`.
4. Connect to at least two sportsbook APIs (e.g., Pinnacle, Betfair).
5. Test in simulation mode first!

## Dependencies
- python>=3.10
- aiohttp
- pandas
- numpy
```

