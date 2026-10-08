---
name: "population-military-system"
description: "Implements population and military service system for cities. Invoke when adding population growth, military recruitment, and resource management to city-based games."
---

# Population and Military Service System

This skill implements a comprehensive population and military service system for city-based games, providing functionality for population growth, military recruitment, and resource management.

## Features

- **Population Growth**: Automatic population growth based on growth factors and city level
- **Population Limit**: Dynamic population cap based on city level
- **Military Service**: Conversion of population to military personnel
- **Resource Management**: Population affects food consumption and gold income
- **UI Integration**: Exposes system variables to user interface for configuration

## Implementation Details

### 1. Variables Added

In `ScenarioVariables.cs`:
- `populationLimitBase`: Base population limit for cities
- `populationLimitPerLevel`: Additional population limit per city level
- `baseTroopPopulationRatio`: Base ratio of population that can serve in military
- `maxTroopPopulationRatio`: Maximum ratio of population that can serve in military
- `populationFoodCostFactor`: Factor for population's impact on food consumption
- `populationGoldIncomeFactor`: Factor for population's impact on gold income

### 2. City Class Enhancements

In `City.cs`:
- Added `PopulationLimit` property: Calculates maximum population based on city level
- Added `MaxTroopPopulation` property: Calculates maximum military personnel based on population
- Added `BaseTroopPopulation` property: Calculates base military personnel based on population
- Modified `OnMonthStart` method: Implements population growth with limits
- Modified `FoodCost` method: Adds population-based food consumption

### 3. Income Calculation

In `ClassicsCityWorking.cs` and `BuildingWorking.cs`:
- Added population impact on food and gold income calculations
- Ensures population contributes to city resources

### 4. UI Integration

In `UIScenarioVariables.cs`:
- Added UI controls for adjusting population and military system parameters
- Allows users to configure system behavior

## Usage

1. **Enable the System**: Set `populationEnable` to `true` in scenario variables
2. **Configure Parameters**: Adjust population growth rate, limits, and ratios via UI
3. **Monitor Population**: Track population growth and military personnel in city status
4. **Manage Resources**: Balance population growth with food production and gold income

## Examples

### Enabling the System

```csharp
// In scenario variables configuration
scenario.Variables.populationEnable = true;
scenario.Variables.populationIncreaseBaseFactor = 0.0113f;
scenario.Variables.populationLimitBase = 10000;
scenario.Variables.populationLimitPerLevel = 5000;
```

### Monitoring Population

```csharp
// In city status display
string status = $"Population: {city.population}/{city.PopulationLimit}\n" +
                $"Military Personnel: {city.troopPopulation}/{city.MaxTroopPopulation}";
```

## Integration Notes

- **Compatibility**: Works with existing city and resource systems
- **Performance**: Efficient calculations with minimal performance impact
- **Extensibility**: Easy to add new population-related features
- **Configuration**: All parameters can be adjusted via UI or code

This system adds depth to city management, requiring players to balance population growth with resource production and military needs.