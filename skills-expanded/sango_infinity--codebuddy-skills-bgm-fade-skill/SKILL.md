---
name: "bgm-fade"
description: "Implements background music fade-in/fade-out functionality for smooth transitions. Invoke when user needs to add or modify BGM transition effects in the audio system."
---

# BGM Fade In/Out Skill

This skill provides functionality for implementing smooth background music transitions with fade-in and fade-out effects in the audio system.

## Features

- Adds fade-in/fade-out functionality to the AudioManager
- Supports customizable fade duration
- Handles state management for fade transitions
- Provides a new method for switching BGM with fade effects

## Implementation Steps

1. **Add Fade State Management**
   - Add a `FadeState` enum to track the current fade state
   - Add variables for fade duration, current time, target BGM, and original volume

2. **Implement Fade Logic**
   - Add a `HandleFade` method to process fade transitions
   - Update the `Update` method to call the fade handler

3. **Add Fade Switch Method**
   - Implement `SwitchBgmWithFade` method for smooth transitions
   - This method handles both fade-out of the current BGM and fade-in of the new BGM

## Usage Example

```csharp
// Switch BGM with 1.5 second fade transition
AudioManager.Instance.SwitchBgmWithFade("bgm_main", true, 1.5f);
```

## Code Structure

The implementation includes:

- `FadeState` enum: Tracks fade states (None, FadingOut, FadingIn)
- `_fadeState`: Current fade state
- `_fadeDuration`: Duration of fade effect
- `_fadeTime`: Current fade time
- `_targetBgmName`: Name of target BGM
- `_targetBgmLoop`: Whether target BGM should loop
- `_originalVolume`: Original volume before fade
- `SwitchBgmWithFade()`: Method to switch BGM with fade
- `HandleFade()`: Method to handle fade logic

## Integration

1. Add the fade-related variables and enum to AudioManager
2. Implement the fade logic in the Update method
3. Add the SwitchBgmWithFade method
4. Use the new method whenever smooth BGM transitions are needed

This implementation ensures that background music transitions are smooth and professional, enhancing the overall audio experience in the game.