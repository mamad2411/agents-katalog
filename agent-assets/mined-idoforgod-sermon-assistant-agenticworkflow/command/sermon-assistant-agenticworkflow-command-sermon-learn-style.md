# /sermon-learn-style — Manual Style Analysis

Manually trigger sermon style analysis from user samples.

## Usage
```
/sermon-learn-style
```

## Prerequisites
Place sermon samples in `user-sermon-style-sample/` directory.

## Process
1. Check `user-sermon-style-sample/` exists and contains files
2. Dispatch @style-analyzer to analyze samples
3. Generate style-profile.json
4. Display style profile summary to user

## Output
- `style-profile.json` in the current sermon output directory
