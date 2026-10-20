---
description: 
globs: 
alwaysApply: false
---
# Function Naming and Line Commenting Convention

This rule applies specifically to `concepts/cursor_rules/cursor_rules.js` and enforces the following conventions:

## Function Naming
1. All function names must be abbreviated versions of their intended purpose
2. Abbreviations should be clear enough to understand the function's purpose
3. Use camelCase for multi-word abbreviations

Examples:
- `calculateTotal` → `calcTot`
- `validateUserInput` → `valUsrInp`
- `processDataStream` → `procDStr`

## Line Comments
1. Every line of code must be followed by an explanatory comment
2. Comments should be placed on the same line after the code
3. Use `//` for inline comments
4. Comments should explain the purpose of the line, not just restate the code

Example:
```javascript
const calcTot = (nums) => {  // Calculate sum of array elements
    let sum = 0;  // Initialize sum accumulator
    nums.forEach(n => {  // Iterate through each number
        sum += n;  // Add current number to running total
    });
    return sum;  // Return final calculated sum
};
```

## Enforcement
This rule must be strictly followed for all code in `concepts/cursor_rules/cursor_rules.js`. Each function definition and each line of code must adhere to these naming and commenting conventions.
