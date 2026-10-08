---
name: "three-kingdoms-duel-system"
description: "Implements Three Kingdoms 11 style duel system with decision-making mechanics. Invoke when user wants to add or modify duel functionality in strategy games."
---

# Three Kingdoms 11 Duel System

## Overview

This skill implements a Three Kingdoms 11 style duel system for strategy games, featuring turn-based combat with decision-making mechanics. The system includes core duel logic, decision options with counter relationships, and event-driven architecture.

## Core Components

### 1. DuelSystem.cs

The main class responsible for handling duel logic:

- **Properties**: AttackerTroop, DefenderTroop, Attacker, Defender, health values, duel state
- **Methods**:
  - `StartDuel()`: Initiates a duel if conditions are met
  - `ProcessDuelTurn()`: Processes one turn of duel combat
  - `Attack()`: Handles attack logic with decision counter relationships
  - `CalculateDamage()`: Calculates damage based on attributes and decisions
  - `HandleDuelResult()`: Processes the outcome of the duel

### 2. DuelManager.cs

Manages the duel process:

- **Methods**:
  - `StartDuel()`: Starts a new duel between two troops
  - `ProcessDuel()`: Processes the entire duel until completion
  - `GetCurrentDuel()`: Gets the current active duel
  - `IsDueling()`: Checks if a duel is in progress

### 3. DuelState.cs

Defines the state of the duel:

- `None`: No duel in progress
- `Started`: Duel has started but not yet in progress
- `InProgress`: Duel is ongoing
- `Ended`: Duel has completed

### 4. Decision System

Implements decision-making mechanics:

- **Decision Options**:
  - `Attack`: Direct attack, counters Skill
  - `Defend`: Defensive stance, counters Attack
  - `Skill`: Special technique, counters Defend

- **Counter Relationships**:
  - Attack → Skill (1.5x damage)
  - Skill → Defend (1.5x damage)
  - Defend → Attack (1.5x damage)
  - Same decisions (1.0x damage)
  - Other combinations (0.8x damage)

- **Decision Frequency**: Every 3 turns, players are prompted to choose a decision

### 5. Event System

Provides event hooks for duel-related events:

- `OnDuelStart`: Triggered when a duel begins
- `OnDuelEnd`: Triggered when a duel completes
- `OnDuelDecisionRequired`: Triggered when decisions are needed
- `OnPersonCaptured`: Triggered when a general is captured

## Usage

### Starting a Duel

```csharp
// From Troop class
public bool StartDuel(Troop targetTroop)
{
    if (targetTroop == null || !IsEnemy(targetTroop))
    {
        return false;
    }

    return DuelManager.Instance.StartDuel(this, targetTroop);
}
```

### Processing a Duel

```csharp
// Process the entire duel
DuelResult result = DuelManager.Instance.ProcessDuel();
```

### Handling Duel Events

```csharp
// Subscribe to duel events
GameEvent.OnDuelStart += OnDuelStart;
GameEvent.OnDuelEnd += OnDuelEnd;
GameEvent.OnDuelDecisionRequired += OnDuelDecisionRequired;

// Event handlers
private void OnDuelStart(DuelSystem duel)
{
    // Handle duel start
}

private void OnDuelEnd(DuelSystem duel, DuelResult result)
{
    // Handle duel end based on result
}

private void OnDuelDecisionRequired(DuelSystem duel)
{
    // Prompt user for decision
    // Set duel.AttackerDecision and duel.DefenderDecision
}
```

## Features

1. **Turn-based Combat**: Each turn consists of attacks and counter-attacks
2. **Decision Mechanics**: Every 3 turns, players choose from Attack, Defend, or Skill
3. **Counter Relationships**: Decisions have rock-paper-scissors style counter relationships
4. **Attribute-based Calculations**: Damage and success rates based on general attributes
5. **Event-driven Architecture**: Comprehensive event system for duel-related events
6. **Default Decisions**: AI-controlled generals use attribute-based default decisions
7. **Capture Mechanics**: Winners can capture enemy generals
8. **Morale Effects**: Duel outcomes affect troop morale

## Implementation Notes

- **Requirements**: Troop and Person classes with appropriate attributes
- **Integration**: Add StartDuel method to Troop class
- **UI**: Implement decision selection UI for player-controlled duels
- **Balance**: Adjust damage calculations and counter factors as needed

## Example Scenario

1. **Initiation**: Player selects an enemy troop and chooses "Duel"
2. **Start**: Duel begins, OnDuelStart event is triggered
3. **Turn 1**: Automatic attacks without decisions
4. **Turn 3**: OnDuelDecisionRequired event is triggered, player chooses Attack
5. **Turn 4-6**: Combat uses the chosen decision
6. **Resolution**: Duel ends, OnDuelEnd event is triggered with result
7. **Effects**: Morale changes, potential capture, and troop elimination

This implementation provides a faithful recreation of Three Kingdoms 11's duel system, adding depth and strategy to combat encounters.