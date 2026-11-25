---
name: unity-audio
description: >
  Unity 6000.3 LTS audio patterns. Covers AudioSource, AudioSource,
  AudioMixer, spatial audio, and WebGL audio.
  Trigger: When working with audio playback, mixing, spatial audio,
  or audio effects in Unity 6000.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- Writing C# code that controls audio playback (SFX, music, voice)
- Configuring AudioSource components for 2D/3D/spatial sound
- Setting up AudioMixer for sound routing, effects, and volume control
- Implementing spatial audio with Octahedral Spherical Harmonics (Sony/Unity)
- Working with WebGL audio constraints and workarounds
- Optimizing audio performance and memory usage
- Implementing audio ducking, snapshots, or ambient sounds
- Debugging audio playback issues

## Critical Rules

### Never Load Audio Assets Synchronously in Production

```csharp
// ❌ WRONG — Synchronous load causes frame hitches
AudioClip clip = Resources.Load<AudioClip>("Sounds/explosion");

// ✅ CORRECT — Use async loading with callback
private void LoadAudioAsync(string path, System.Action<AudioClip> onLoaded)
{
    StartCoroutine(LoadAudioCoroutine(path, onLoaded));
}

private IEnumerator LoadAudioCoroutine(string path, System.Action<AudioClip> onLoaded)
{
    var request = Resources.LoadAsync<AudioClip>(path);
    yield return request;
    onLoaded?.Invoke(request.asset as AudioClip);
}
```

**Why:** Synchronous `Resources.Load` blocks the main thread, causing audio glitches and frame drops. Always load asynchronously.

### One AudioListener Per Scene (Unless Using Split-Screen)

```csharp
// ❌ WRONG — Multiple listeners cause confusing/broken audio
// Camera 1
cam1.gameObject.AddComponent<AudioListener>();
// Camera 2 (active during split-screen)
cam2.gameObject.AddComponent<AudioListener>();

// ✅ CORRECT — Only one active listener per "audio space"
// Disable listener on secondary cameras
audioListener.enabled = false; // on secondary camera
```

**Why:** Multiple AudioListeners pick up different sets of AudioSources depending on camera culling — causes unpredictable spatial audio.

### Use AudioMixer for Dynamic Volume Control

```csharp
// ❌ WRONG — Hardcoded volume, no runtime control
audioSource.volume = 0.5f;
audioSource.Play();

// ✅ CORRECT — Route through AudioMixer for dynamic control
audioMixer.SetFloat("MusicVolume", -10f); // -10dB
audioMixer.SetFloat("SFXVolume", 0f);     // 0dB
audioSource.Play();
```

**Why:** AudioMixer allows real-time volume adjustments, audio ducking, snapshots, and effects without touching individual sources.

## AudioSource

### Essential Configuration

```csharp
AudioSource source = gameObject.AddComponent<AudioSource>();

// Output to AudioMixer (or leave null for master bus)
source.outputAudioMixerGroup = audioMixer.FindMatchingGroups("SFX")[0];

// Audio clip
source.clip = myClip;

// Playback control
source.playOnAwake = false; // Default: true — usually disable for game objects
source.loop = false;

// Volume (0-1, where 1 = full volume, 0 = silence)
source.volume = 1.0f;

// Pitch (-3 to +3, 1 = normal speed/pitch)
// Useful for randomizing SFX slightly
source.pitch = 1.0f + Random.Range(-0.1f, 0.1f);

// Priority (0 = highest, 256 = lowest)
// Use for voice vs music vs SFX priority
source.priority = 128; // Default

// Startup time offset (seconds)
source.time = 0f;        // Start position
source.timeSamples = 0;  // Start position in samples (more precise)
```

### 2D vs 3D Sound

```csharp
// 2D Sound — no spatialization
source.spatialBlend = 0f; // Full 2D (default for AudioSource)

// 3D Sound — full 3D spatialization
source.spatialBlend = 1f; // Full 3D

// Blend (0-1) — semi-3D for atmosphere
source.spatialBlend = 0.5f; // Equal 2D/3D

// 3D Volume Rolloff — how volume decreases with distance
source.rolloffMode = AudioRolloffMode.Linear;        // Linear falloff
source.rolloffMode = AudioRolloffMode.Logarithmic;   // Natural falloff (default)
source.rolloffMode = AudioRolloffMode.Custom;          // Custom curve

// Distance settings
source.minDistance = 1f;   // Volume is max within this radius
source.maxDistance = 500f; // Volume is zero beyond this radius

// Custom rolloff curve (when rolloffMode = Custom)
source.SetCustomCurve(AudioSourceCurveType.CustomRolloff, myRolloffCurve);

// Doppler effect — how pitch changes as source moves relative to listener
source.dopplerLevel = 1f;  // 0 = no doppler, 1 = realistic, 2 = exaggerated
```

### Spatial Blend (2D/3D) Deep Dive

```csharp
// SpatialBlend = 0: Pure 2D
// - Volume only, no panning based on position
// - Used for: UI sounds, music, voice-over

// SpatialBlend = 1: Full 3D
// - Position-based panning (left/right speaker)
// - Distance-based volume falloff
// - Used for: footstep, environmental, positional SFX

// SpatialBlend curve animation:
source.spatialBlend = Mathf.Lerp(0f, 1f, distanceFromSource / maxDistance);
```

### Playback Methods

```csharp
// Basic playback
source.Play();        // Play assigned clip
source.PlayDelayed(2f); // Play after 2 seconds
source.PlayScheduled(1000f); // Play at AudioSettings.dspTime + offset

// Stop control
source.Stop();

// Pause (keeps time position)
source.Pause();
source.UnPause();

// One-shot (plays and forgets, doesn't interrupt)
// Preferred for frequently-played SFX
AudioSource.PlayClipAtPoint(clip, position); // Static method
AudioSource.PlayClipAtPoint(clip, position, volume); // With volume

// Fade in/out using coroutines
public IEnumerator FadeIn(AudioSource source, float duration, float targetVolume = 1f)
{
    source.volume = 0f;
    source.Play();
    float elapsed = 0f;
    while (elapsed < duration)
    {
        elapsed += Time.deltaTime;
        source.volume = Mathf.Lerp(0f, targetVolume, elapsed / duration);
        yield return null;
    }
    source.volume = targetVolume;
}

public IEnumerator FadeOut(AudioSource source, float duration)
{
    float startVolume = source.volume;
    float elapsed = 0f;
    while (elapsed < duration)
    {
        elapsed += Time.deltaTime;
        source.volume = Mathf.Lerp(startVolume, 0f, elapsed / duration);
        yield return null;
    }
    source.Stop();
    source.volume = startVolume; // Reset for next play
}
```

### Randomize SFX Without Allocation

```csharp
// ❌ WRONG — Allocates array every call
public void PlayFootstep()
{
    AudioClip[] clips = new AudioClip[] { footstep1, footstep2, footstep3 };
    source.clip = clips[Random.Range(0, clips.Length)];
    source.Play();
}

// ✅ CORRECT — Pre-allocated array
private AudioClip[] _footstepClips;
private int _lastFootstepIndex = -1;

public void PlayFootstep()
{
    int index = Random.Range(0, _footstepClips.Length);
    if (index == _lastFootstepIndex)
        index = (index + 1) % _footstepClips.Length; // Avoid repeat
    _lastFootstepIndex = index;
    source.clip = _footstepClips[index];
    source.Play();
}

// ✅ ALTERNATIVE — Span for zero allocation
private static readonly AudioClip[] FootstepClips = new AudioClip[]
{
    footstep1, footstep2, footstep3, footstep4
};
```

### AudioSource Properties Reference

| Property | Range | Default | Description |
|----------|-------|---------|-------------|
| volume | 0-1 | 1 | Linear volume |
| pitch | -3 to 3 | 1 | Playback speed multiplier |
| spatialBlend | 0-1 | 0 | 2D/3D blend |
| stereoPan | -1 to 1 | 0 | Left/right pan (2D only) |
| time | 0+ | 0 | Playback position in seconds |
| timeSamples | 0+ | 0 | Playback position in samples |
| minDistance | 0+ | 1 | Near field radius |
| maxDistance | 0.01+ | 500 | Far field radius |
| rolloffMode | Linear/Log/Custom | Logarithmic | Distance model |
| dopplerLevel | 0-5 | 1 | Doppler effect intensity |
| spread | 0-360 | 0 | 3D sound spread angle |
| priority | 0-256 | 128 | Streaming priority |
| loop | bool | false | Loop playback |

## AudioListener

### Camera Attachment

```csharp
// Standard setup — one listener on main camera
public class AudioManager : MonoBehaviour
{
    [SerializeField] private Camera mainCamera;
    private AudioListener _listener;

    private void Start()
    {
        _listener = mainCamera.GetComponent<AudioListener>();
        if (_listener == null)
            _listener = mainCamera.gameObject.AddComponent<AudioListener>();
    }
}
```

### Listener Properties (Advanced)

```csharp
// In Unity 6000, AudioListener has additional properties
// accessed via the inspector or through serialization

// Audio恶心 spatialBlend on listener side (not common to change)
// Most spatialization happens on AudioSource side

// Game-wide mute (useful for pause menu)
public void MuteAll(bool mute)
{
    AudioListener.pause = mute;
}
```

### Velocity Tracking (For Doppler)

```csharp
// Unity uses velocity for doppler calculation
// Attach to moving camera or vehicle
private Vector3 _previousPosition;
private AudioListener _listener;

void LateUpdate()
{
    Vector3 velocity = (transform.position - _previousPosition) / Time.deltaTime;
    // AudioListener doesn't expose velocity directly in 6000
    // Use AudioSource.dopplerLevel instead on sources
    _previousPosition = transform.position;
}
```

## AudioMixer

### Hierarchy Structure

```
Master
├── Music
│   ├── Band1
│   ├── Band2
│   └── Band3
├── SFX
│   ├── Footsteps
│   ├── Impacts
│   └── UI
└── Voice
```

### Creating and Configuring via Script

```csharp
public class AudioMixerSetup : MonoBehaviour
{
    [SerializeField] private AudioMixer audioMixer;

    private void CreateMixerGroups()
    {
        // Groups are typically created in Editor
        // Scripting is mainly for runtime adjustments

        // Expose parameters for runtime control
        bool exposed = true;
        audioMixer.SetFloat("MusicVolume", 0f);
        audioMixer.ClearFloat("MusicVolume");
    }

    public void SetVolume(string groupName, float volumeDb)
    {
        // Volume in dB: 0 = full, -10 = 10x quieter, -80 = nearly silent
        audioMixer.SetFloat(groupName + "Volume", volumeDb);
    }

    public float GetVolume(string groupName)
    {
        if (audioMixer.GetFloat(groupName + "Volume", out float volume))
            return volume;
        return 0f;
    }
}
```

### Volume to Decibel Conversion

```csharp
// Linear (0-1) to Decibel (-80 to 0)
// AudioMixer uses dB scale, not linear

public static float LinearToDb(float linear)
{
    if (linear <= 0f) return -80f;
    return Mathf.Log10(linear) * 20f;
}

public static float DbToLinear(float db)
{
    return Mathf.Pow(10f, db / 20f);
}

// Usage
float volumeLinear = 0.5f; // 50%
float volumeDb = LinearToDb(volumeLinear); // -6dB
audioMixer.SetFloat("MusicVolume", volumeDb);
```

### Snapshots (Instant Transitions)

```csharp
// Get snapshots
AudioMixerSnapshot[] snapshots = audioMixer.FindSnapshots("");

// Transition to snapshot
audioMixer.TransitionToSnapshots(snapshots, new float[] { 1f }, 0f); // Instant

// Multiple snapshot blend (if multiple snapshots match)
AudioMixerSnapshot indoor = audioMixer.FindSnapshot("Indoor");
AudioMixerSnapshot outdoor = audioMixer.FindSnapshot("Outdoor");

// Blend toward outdoor (0 = indoor, 1 = outdoor)
float t = 0.3f;
audioMixer.TransitionToSnapshots(
    new AudioMixerSnapshot[] { indoor, outdoor },
    new float[] { 1f - t, t },
    0.5f // Transition time
);
```

### Ducking (Automatic Volume Reduction)

```csharp
// Ducking: When voice plays, lower music volume automatically
// Set up in AudioMixer inspector:
// 1. Select Music group
// 2. Add "Duck" effect
// 3. Set "Threshold", "Ratio", "AttackTime", "ReleaseTime"

// Or via script:
public void SetupDucking()
{
    // Get the ExposedParameter for the music volume
    // This is done in the AudioMixer inspector by right-clicking "Volume"
    // and selecting "Expose to script"

    // At runtime, voice AudioSource will trigger ducking
    // when it plays, based on AudioMixer duck settings
}
```

### Effects Chain (Per Group)

```csharp
// AudioMixer groups can have effects
// Effects order matters (top to bottom in inspector)

// Common effects:
// - Attenuation (volume)
// - Compressor
// - Noise (for lo-fi)
// - SFX Reverb
// - Lowpass/Highpass

// Add effect at runtime
AudioMixerGroup sfxGroup = audioMixer.FindMatchingGroups("SFX")[0];
var lowpass = sfxGroup.gameObject.AddComponent<AudioMixerGroupEffect>();
// Note: Not all effects are scriptable at runtime in Unity 6000
// Most effects must be configured in Editor
```

### AudioMixer Advanced Controls

```csharp
// Find groups
AudioMixerGroup master = audioMixer.FindMatchingGroups("Master")[0];
AudioMixerGroup sfx = audioMixer.FindMatchingGroups("SFX")[0];
AudioMixerGroup music = audioMixer.FindMatchingGroups("Music")[0];

// Set volume with validation
public void SafeSetVolume(string parameterName, float linearVolume)
{
    float db = LinearToDb(Mathf.Clamp01(linearVolume));
    audioMixer.SetFloat(parameterName, db);
}

// Get RMS (for visualizations)
public float GetRMS(string groupName, int samples = 256)
{
    // Note: Direct RMS reading from AudioMixer is limited in Unity 6000
    // Consider using AudioAnalyzer component or custom DSP
    return 0f;
}
```

## Spatial Audio

### Enabling Spatial Audio

```csharp
// Project Settings > Audio > Enable "Spatial Audio" checkbox
// Or via script at startup:

public void EnableSpatialAudio()
{
    AudioConfiguration config = AudioSettings.GetConfiguration();
    config.spatialAudioEnabled = true;
    AudioSettings.Reset(config);
}

// Check if spatial audio is enabled
bool IsSpatialAudioEnabled()
{
    AudioConfiguration config = AudioSettings.GetConfiguration();
    return config.spatialAudioEnabled;
}
```

### Octahedral Spherical Harmonics (OSH)

Unity 6000 uses Sony's OSH system for efficient spatial audio:

```csharp
// Spatial audio requires AudioSource with:
// - Output to AudioMixer with Spatializer effect
// - Spatializer plugin enabled on the mixer group

// Enable Spatializer on AudioMixer group:
// 1. Select AudioMixer group
// 2. Add "Spatializer" effect (not just for distance, it's for OSH)

// Or use the simpler built-in panner:
// For basic 3D without full OSH, use "Spatializer" effect on group
```

### Spatializer vs HRTF

```csharp
// Built-in Spatializer: Simple 3D panning with distance attenuation
// HRTF (Head-Related Transfer Function): More realistic but more CPU

// Select in Project Settings > Audio > Spatial Audio
// - Built-in: Faster, good quality
// - HRTF: Best quality, higher CPU

// Most games: Built-in Spatializer is sufficient
```

### Occlusion (Sound Blocked by Geometry)

```csharp
// Spatial audio can model occlusion (sound blocked by walls)
// Requires:
 // 1. Enable "Occlusion" in Project Settings > Audio > Spatial Audio
// 2. Tag occluder colliders appropriately

// Note: Full occlusion requires RaycastMesh for accurate results
// Unity 6000 supports:
// - Volumetric Occlusion for complex geometry
// - Simple Box/Sphere occlusion for performance

// Scripting occlusion parameters:
public void ConfigureOcclusion()
{
    // Per-source occlusion settings are in the AudioSource inspector
    // Under "Spatial Audio" section:
    // - Occlusion Intensity
    // - Occlusion Pickup
}
```

### Distance-Based Behavior

```csharp
// When spatial audio enabled, distance behavior changes
AudioSource source = GetComponent<AudioSource>();

// minDistance: Near field radius (volume stays at max)
// maxDistance: Far field radius (volume drops to 0)

// IMPORTANT: With spatial audio, different rolloff models apply
// You may need to adjust these values for spatial audio
source.minDistance = 2f;  // Adjust for game scale
source.maxDistance = 50f; // Sound fully attenuated at this distance

// Custom curves for spatial audio:
source.SetCustomCurve(AudioSourceCurveType.SpatialSpread, spreadCurve);
source.SetCustomCurve(AudioSourceCurveType.ReverbZoneMix, reverbCurve);
```

### Runtime Spatial Audio Configuration

```csharp
public class SpatialAudioController : MonoBehaviour
{
    [SerializeField] private AudioSource source;

    void ConfigureForFootsteps()
    {
        source.spatialBlend = 1f;
        source.spread = 90; // Wider for footsteps
        source.rolloffMode = AudioRolloffMode.Linear;
        source.minDistance = 0.5f;
        source.maxDistance = 15f;
    }

    void ConfigureForAmbient()
    {
        source.spatialBlend = 1f;
        source.spread = 180; // Full spread for ambient
        source.rolloffMode = AudioRolloffMode.Logarithmic;
        source.minDistance = 5f;
        source.maxDistance = 100f;
    }

    void ConfigureForVoice()
    {
        source.spatialBlend = 0f; // 2D for voice
        source.priority = 0; // Highest priority
    }
}
```

## AudioClip

### Import Settings (Programmatic Hints)

```csharp
// AudioClip import settings affect memory and quality
// Most settings are Editor-only, but understanding helps:

// Compression format:
// - Vorbis: Good compression, ~10:1 ratio, recommended for music
// - MP3: ~10:1 ratio, widely compatible
// - PCM: Uncompressed, ~5:1 larger, use for short SFX
// - ADPCM: Good for repeated playback (footsteps), 3.5:1

// Sample rate:
// - Preserve: Keep original (higher quality, more memory)
// - Optimize: Reduce to 96% of original (good balance)
// - Override: Fixed sample rate (use lower for voice)

public class AudioClipInfo
{
    public string name;
    public int samples;
    public int channels;
    public int frequency;
    public long memorySizeBytes;
}
```

### Loading and Unloading

```csharp
// Preload audio data
public void PreloadClip(AudioClip clip)
{
    clip.LoadAudioData(); // Explicit load (usually automatic)
}

// Unload to free memory
public void UnloadClip(AudioClip clip)
{
    clip.UnloadAudioData();
}

// Check if loaded
bool IsLoaded(AudioClip clip)
{
    return clip.loadState == AudioDataLoadState.Loaded;
}
```

### Procedural Audio Generation

```csharp
public class ProceduralAudio : MonoBehaviour
{
    [SerializeField] private AudioSource source;

    // Generate a simple tone
    public AudioClip CreateTone(float frequency, float duration, int sampleRate = 44100)
    {
        int samples = (int)(duration * sampleRate);
        AudioClip clip = AudioClip.Create("Tone", samples, 1, sampleRate, false);

        float[] data = new float[samples];
        for (int i = 0; i < samples; i++)
        {
            float t = (float)i / sampleRate;
            data[i] = Mathf.Sin(2f * Mathf.PI * frequency * t);
        }

        clip.SetData(data, 0);
        return clip;
    }

    // Generate noise
    public AudioClip CreateNoise(float duration, int sampleRate = 44100)
    {
        int samples = (int)(duration * sampleRate);
        AudioClip clip = AudioClip.Create("Noise", samples, 1, sampleRate, false);

        float[] data = new float[samples];
        for (int i = 0; i < samples; i++)
        {
            data[i] = Random.Range(-1f, 1f);
        }

        clip.SetData(data, 0);
        return clip;
    }
}
```

## AudioSettings

### Configuration Management

```csharp
// Get current configuration
AudioConfiguration config = AudioSettings.GetConfiguration();

// Common configuration properties:
config.sampleRate = 44100;        // or 48000
config.numRealVoices = 32;        // Max simultaneous sounds
config.numVirtualVoices = 512;    // Total voices (mixing overhead)
config.spatialAudioEnabled = true; // Enable OSH spatial audio

// Apply changes
AudioSettings.Reset(config);

// DSP Time (for precise scheduling)
double dspTime = AudioSettings.dspTime;

// Schedule sound at specific time
source.PlayScheduled(dspTime + 1.0); // Play in 1 second
```

### Speaker Mode

```csharp
// Set speaker output mode
AudioConfiguration config = AudioSettings.GetConfiguration();
config.speakerMode = AudioSpeakerMode.Stereo; // Default
// Other options: Mono, Quad, Surround, 5.1, 7.1, etc.

AudioSettings.Reset(config);

// Get current speaker mode
AudioSpeakerMode speakerMode = AudioSettings.driverCapabilities;
```

## WebGL Audio

### Critical WebGL Constraints

```csharp
// WebGL has significant audio limitations:

// 1. NO dynamic audio threading
// Audio runs on main thread in WebGL

// 2. Limited audio formats
// - MP3: ✅ Supported
// - Ogg Vorbis: ✅ Supported
// - WAV: ✅ Supported (but large)

// 3. No AudioMixer effects in WebGL (Unity 6000.3)
// Some effects work, but many don't:
// - Attenuation: ✅ Works
// - Compressor: ❌ Doesn't work
// - Reverb: ❌ Limited/no native support
// - EQ: ❌ Doesn't work

// Solution: Use cross-platform audio middleware or pre-bake effects
```

### WebGL-Compatible Audio Patterns

```csharp
public class WebGLAudioFallback : MonoBehaviour
{
    [SerializeField] private AudioSource musicSource;
    [SerializeField] private AudioSource sfxSource;

    void Start()
    {
#if UNITY_WEBGL
        // WebGL: Keep audio simple
        SetupWebGLAudio();
#else
        SetupFullAudio();
#endif
    }

    void SetupWebGLAudio()
    {
        // WebGL-friendly: No mixer effects
        musicSource.outputAudioMixerGroup = null;
        sfxSource.outputAudioMixerGroup = null;

        // Control volume directly
        musicSource.volume = PlayerPrefs.GetFloat("MusicVolume", 0.7f);
        sfxSource.volume = PlayerPrefs.GetFloat("SFXVolume", 1f);
    }

    void SetupFullAudio()
    {
        // Desktop: Full mixer support
        // Route to AudioMixer as normal
    }
}
```

### WebGL Audio Loading

```csharp
// WebGL: Use streaming for large audio files
public class WebGLAudioLoader : MonoBehaviour
{
    // Streaming in WebGL bypasses some memory limits
    public void LoadStreamingAudio(string path)
    {
        // WWW is deprecated, use UnityWebRequest
        StartCoroutine(LoadAudio(path));
    }

    private IEnumerator LoadAudio(string path)
    {
        using (var request = UnityWebRequestMultimedia.GetAudioClip(path, AudioType.UNKNOWN))
        {
            yield return request.SendWebRequest();

            if (request.result == UnityWebRequest.Result.Success)
            {
                AudioClip clip = DownloadHandlerAudioClip.GetContent(request);
                // Use clip...
            }
        }
    }
}
```

### Mobile Audio Considerations

```csharp
// iOS/Android have similar constraints to WebGL

public class MobileAudioSetup : MonoBehaviour
{
    void Awake()
    {
#if UNITY_IPHONE || UNITY_ANDROID
        // Prevent screen dimming from stopping audio
        Application.runInBackground = true;

        // Request audio session on iOS
        AudioSessionInitialize();
#endif
    }

#if UNITY_IPHONE
    [System.Runtime.InteropServices.DllImport("__Internal")]
    private static extern void AudioSessionInitialize();

    [System.Runtime.InteropServices.DllImport("__Internal")]
    private static extern void AudioSessionSetActive(bool active);
#endif
}
```

## Common Mistakes to Prevent

### Mistake 1: Forgetting to Stop Looping Sounds

```csharp
// ❌ WRONG — Sound keeps playing forever
void OnTriggerEnter(Collider other)
{
    if (other.CompareTag("Hazard"))
        audioSource.Play(); // Will loop forever!
}

// ✅ CORRECT — Check loop state before playing
void OnTriggerEnter(Collider other)
{
    if (other.CompareTag("Hazard"))
    {
        audioSource.clip = hazardSound;
        audioSource.loop = true;
        audioSource.Play();
    }
}

void OnTriggerExit(Collider other)
{
    if (other.CompareTag("Hazard"))
    {
        audioSource.Stop();
    }
}
```

### Mistake 2: Multiple Sources Overlapping Incorrectly

```csharp
// ❌ WRONG — New sound doesn't stop old sound
public void PlayFootstep()
{
    source.PlayOneShot(footstepClip); // Multiple can stack
}

// ✅ CORRECT — One footstep at a time
private bool _isFootstepPlaying;

public void PlayFootstep()
{
    if (_isFootstepPlaying) return;

    _isFootstepPlaying = true;
    source.clip = footstepClip;
    source.Play();

    // Schedule footstep end
    Invoke(nameof(OnFootstepComplete), footstepClip.length);
}

private void OnFootstepComplete()
{
    _isFootstepPlaying = false;
}
```

### Mistake 3: Not Handling AudioSource Stop Properly

```csharp
// ❌ WRONG — Reset state on play, not stop
void Update()
{
    if (source.isPlaying == false && shouldBePlaying)
    {
        // Sound stopped unexpectedly!
    }
}

// ✅ CORRECT — Clean state management
public void Play()
{
    isPlaying = true;
    source.Play();
}

public void Stop()
{
    isPlaying = false;
    source.Stop();
}
```

### Mistake 4: Ignoring Audio Memory

```csharp
// ❌ WRONG — Load all audio at startup
void Start()
{
    foreach (var clip in allAudioClips)
    {
        clip.LoadAudioData(); // Loads all into memory!
    }
}

// ✅ CORRECT — Load on demand, unload when done
public void PlayAndUnloadWhenDone(AudioClip clip)
{
    source.clip = clip;
    source.Play();

    StartCoroutine(UnloadWhenFinished(clip));
}

private IEnumerator UnloadWhenFinished(AudioClip clip)
{
    yield return new WaitForSeconds(clip.length + 1f);
    if (clip.loadState == AudioDataLoadState.Loaded)
    {
        clip.UnloadAudioData();
    }
}
```

### Mistake 5: Wrong Rolloff Mode for Game Scale

```csharp
// ❌ WRONG — Using defaults for wrong scale
source.minDistance = 1f;
source.maxDistance = 500f;
// Sounds too loud up close, dies too fast

// ✅ CORRECT — Match to game scale
// For first-person shooter distances:
source.minDistance = 2f;   // Comfortable near-field
source.maxDistance = 100f; // Gunshot falls off naturally

// For RTS:
source.minDistance = 5f;
source.maxDistance = 200f;

// For mobile runner:
source.minDistance = 1f;
source.maxDistance = 30f;
```

### Mistake 6: Spatial Blend on Voice

```csharp
// ❌ WRONG — Spatializing voice that should be 2D
source.spatialBlend = 1f; // Player voice comes from wrong direction!

// ✅ CORRECT — Keep dialogue/voice 2D
source.spatialBlend = 0f;
source.priority = 0; // Highest priority
```

## Response Format

### Code Snippets

Use complete, compilable C# code blocks with:

1. **Class definition** with `MonoBehaviour` or appropriate base
2. **Serialized fields** for inspector exposure
3. **Public methods** matching the skill patterns
4. **Proper null checks** and error handling

### Structure

```
// What this does
[Optional: when to use]
```csharp
// Full code example
```

### Variable Naming

- `_source` for AudioSource
- `_clip` for AudioClip
- `_mixer` for AudioMixer
- `_volume` for linear volume (0-1)
- `_db` suffix for decibel values

### Performance Notes

Mark hot paths with:
```csharp
// PERFORMANCE: This is called per-frame
```

Mark allocations with:
```csharp
// ⚠️ ALLOCATION: Creates garbage - use pooling in production
```

## Audio Manager Pattern

### Complete Implementation

```csharp
using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AudioManager : MonoBehaviour
{
    public static AudioManager Instance { get; private set; }

    [Header("Mixer")]
    [SerializeField] private AudioMixer audioMixer;

    [Header("Sources")]
    [SerializeField] private AudioSource musicSource;
    [SerializeField] private AudioSource sfxSource;
    [SerializeField] private AudioSource voiceSource;
    [SerializeField] private AudioSource ambientSource;

    [Header("Clips")]
    [SerializeField] private AudioClip menuMusic;
    [SerializeField] private AudioClip gameplayMusic;
    [SerializeField] private AudioClip[] footstepClips;
    [SerializeField] private AudioClip jumpClip;
    [SerializeField] private AudioClip landClip;

    private int _lastFootstepIndex = -1;
    private const string MusicVolumeKey = "MusicVolume";
    private const string SFXVolumeKey = "SFXVolume";
    private const string VoiceVolumeKey = "VoiceVolume";

    private void Awake()
    {
        if (Instance != null && Instance != this)
        {
            Destroy(gameObject);
            return;
        }
        Instance = this;
        DontDestroyOnLoad(gameObject);

        LoadVolumes();
    }

    private void LoadVolumes()
    {
        float musicVol = PlayerPrefs.GetFloat(MusicVolumeKey, 0.7f);
        float sfxVol = PlayerPrefs.GetFloat(SFXVolumeKey, 1f);
        float voiceVol = PlayerPrefs.GetFloat(VoiceVolumeKey, 1f);

        SetMusicVolume(musicVol);
        SetSFXVolume(sfxVol);
        SetVoiceVolume(voiceVol);
    }

    // --- Music Control ---

    public void PlayMusic(AudioClip clip, bool loop = true)
    {
        if (clip == null) return;

        musicSource.clip = clip;
        musicSource.loop = loop;
        musicSource.Play();
    }

    public void StopMusic()
    {
        musicSource.Stop();
    }

    public void FadeMusic(AudioClip newClip, float duration, bool loop = true)
    {
        StartCoroutine(FadeMusicCoroutine(newClip, duration, loop));
    }

    private IEnumerator FadeMusicCoroutine(AudioClip newClip, float duration, bool loop)
    {
        float startVolume = musicSource.volume;
        float elapsed = 0f;

        // Fade out
        while (elapsed < duration / 2f)
        {
            elapsed += Time.deltaTime;
            musicSource.volume = Mathf.Lerp(startVolume, 0f, elapsed / (duration / 2f));
            yield return null;
        }

        // Switch clip
        musicSource.clip = newClip;
        musicSource.loop = loop;
        musicSource.Play();

        // Fade in
        elapsed = 0f;
        while (elapsed < duration / 2f)
        {
            elapsed += Time.deltaTime;
            musicSource.volume = Mathf.Lerp(0f, startVolume, elapsed / (duration / 2f));
            yield return null;
        }

        musicSource.volume = startVolume;
    }

    // --- SFX Control ---

    public void PlayFootstep()
    {
        if (footstepClips == null || footstepClips.Length == 0) return;

        int index = UnityEngine.Random.Range(0, footstepClips.Length);
        if (index == _lastFootstepIndex && footstepClips.Length > 1)
            index = (index + 1) % footstepClips.Length;

        _lastFootstepIndex = index;
        sfxSource.pitch = 1f + UnityEngine.Random.Range(-0.05f, 0.05f);
        sfxSource.PlayOneShot(footstepClips[index]);
    }

    public void PlayJump()
    {
        if (jumpClip == null) return;
        sfxSource.PlayOneShot(jumpClip);
    }

    public void PlayLand()
    {
        if (landClip == null) return;
        sfxSource.PlayOneShot(landClip);
    }

    public void PlayOneShot(AudioClip clip, float volumeScale = 1f)
    {
        if (clip == null) return;
        sfxSource.PlayOneShot(clip, volumeScale);
    }

    public void PlayAtPoint(AudioClip clip, Vector3 position, float volume = 1f)
    {
        if (clip == null) return;
        AudioSource.PlayClipAtPoint(clip, position, volume);
    }

    // --- Voice Control ---

    public void PlayVoice(AudioClip clip)
    {
        if (clip == null) return;

        voiceSource.clip = clip;
        voiceSource.Play();
    }

    public void StopVoice()
    {
        voiceSource.Stop();
    }

    // --- Volume Control ---

    public void SetMusicVolume(float linear)
    {
        linear = Mathf.Clamp01(linear);
        float db = LinearToDb(linear);
        audioMixer.SetFloat(MusicVolumeKey, db);
        PlayerPrefs.SetFloat(MusicVolumeKey, linear);
    }

    public void SetSFXVolume(float linear)
    {
        linear = Mathf.Clamp01(linear);
        float db = LinearToDb(linear);
        audioMixer.SetFloat(SFXVolumeKey, db);
        PlayerPrefs.SetFloat(SFXVolumeKey, linear);
    }

    public void SetVoiceVolume(float linear)
    {
        linear = Mathf.Clamp01(linear);
        float db = LinearToDb(linear);
        audioMixer.SetFloat(VoiceVolumeKey, db);
        PlayerPrefs.SetFloat(VoiceVolumeKey, linear);
    }

    public float GetMusicVolume() => PlayerPrefs.GetFloat(MusicVolumeKey, 0.7f);
    public float GetSFXVolume() => PlayerPrefs.GetFloat(SFXVolumeKey, 1f);
    public float GetVoiceVolume() => PlayerPrefs.GetFloat(VoiceVolumeKey, 1f);

    // --- Utility ---

    public void MuteAll(bool mute)
    {
        audioMixer.SetFloat(MusicVolumeKey, mute ? -80f : LinearToDb(GetMusicVolume()));
        audioMixer.SetFloat(SFXVolumeKey, mute ? -80f : LinearToDb(GetSFXVolume()));
        audioMixer.SetFloat(VoiceVolumeKey, mute ? -80f : LinearToDb(GetVoiceVolume()));
    }

    public void PauseAll()
    {
        AudioListener.pause = true;
    }

    public void ResumeAll()
    {
        AudioListener.pause = false;
    }

    private static float LinearToDb(float linear)
    {
        if (linear <= 0f) return -80f;
        return Mathf.Log10(linear) * 20f;
    }
}
```

## Performance Optimization

### Key Numbers

| Setting | Default | Impact |
|---------|---------|--------|
| Real Voices | 32 | Max simultaneous sounds |
| Virtual Voices | 512 | Voices managed by mixer |
| Sample Rate | 44100 or 48000 | Quality vs CPU |
| DSP Buffer | Small | Latency vs stability |

### Voice Stealing

```csharp
// When all voices are used, Unity steals from oldest/quietest
// Configure in Project Settings > Audio:

// Voice Stealing: What happens when limit reached
// - Stop: Stop the oldest sound (simple)
// - Pitch Down: Slow down oldest sound (gradual)
// - Virtualize: Keep playing silently (for music)

// For most games: "Stop" is fine
// For music-heavy games: Consider "Virtualize"
```

### Reduce Memory

```csharp
// 1. Use compressed audio (Vorbis/MP3)
// 2. Load sounds async, not at startup
// 3. Unload unused clips
// 4. Use streaming for long audio (>30 sec)
// 5. Downsample voice to 22kHz

// Memory per minute (44.1kHz stereo):
// - PCM: ~10 MB
// - MP3/Vorbis: ~1 MB
// - Streaming: Near zero (buffered)
```

### Reduce CPU

```csharp
// 1. Reduce simultaneous sounds (lower real voice count)
// 2. Use simple rolloff (Linear instead of Logarithmic)
// 3. Minimize spatial blend calculations
// 4. Disable doppler for moving sources where not needed
// 5. Use AudioSource.PlayOneShot instead of multiple sources
```

## Unity 6000-Specific Features

### Audio Mixer Enhancements

```csharp
// Unity 6000 introduces improvements to AudioMixer workflows

// New: Dynamic mixer groups can be created at runtime
// Note: Still recommended to pre-configure in Editor

// New: Better profiling tools
// Use Profiler > Audio window to debug voice allocation
```

### Spatial Audio Improvements

```csharp
// Unity 6000 spatial audio improvements:

// 1. Better OSH (Octahedral Spherical Harmonics)
//    - More efficient spatial positioning
//    - Improved occlusion

// 2. Enhanced distance models
//    - Custom attenuation curves more flexible

// 3. Better multipath handling
//    - Simulates sound reflecting off surfaces
```

### Profiling Audio

```csharp
// Use Profiler window to monitor:
// - Audio CPU Usage
// - Number of active voices
// - Memory used by audio clips
// - Audio clip load states

// Common bottlenecks:
// - Too many simultaneous AudioSources
// - AudioMixer effects (especially on mobile)
// - Loading audio synchronously
// - Memory pressure from loaded clips
```

## Common Issues / Gotchas

| Issue | Cause | Solution |
|-------|-------|----------|
| No sound playing | AudioListener missing or disabled | Add AudioListener to camera |
| Sound cuts out | Voice limit reached | Increase Real Voices or reduce sounds |
| Audio desyncs | Wrong sample rate | Match all audio to 44100 or 48000 |
| 3D sound wrong | SpatialBlend = 0 | Set spatialBlend to 1 for 3D |
| Volume changes don't work | Not using AudioMixer | Route through mixer, use dB |
| WebGL audio broken | Unsupported effects | Remove compressor/reverb or pre-bake |
| Popping/clicking | Buffer underrun | Increase DSP buffer size |
| Audio delays | Large buffer | Use "Best latency" in settings |
| Music skips | Memory pressure | Use streaming for long tracks |
| Footsteps overlap | Multiple sources | Use single source with state check |

## Best Practices

1. **Use AudioMixer for all volume control** — Never set volume directly on sources
2. **Prefer PlayOneShot for frequently-played SFX** — Efficient voice management
3. **Load audio asynchronously** — Never `Resources.Load` synchronously
4. **Set playOnAwake = false** — Control when sounds play explicitly
5. **Use spatialBlend correctly** — 0 for UI/voice/music, 1 for positional SFX
6. **Match rolloff to game scale** — Default values rarely fit your game
7. **Unload unused audio clips** — Free memory for level loading
8. **Use pooling for frequently-played sounds** — Avoid Instantiate/Destroy
9. **Test on target platform** — WebGL and mobile have different constraints
10. **Profile audio performance** — Use Profiler > Audio window
11. **Keep one AudioListener** — Unless doing split-screen correctly
12. **Prefer 2D for dialogue** — Spatialization on voice is usually wrong

(End of file - total 1073 lines)
