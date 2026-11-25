---
name: humanlike-chat-timing
description: Psychological principles and implementation patterns for AI chat interfaces that feel natural and engaging. Covers Weber-Fechner timing, beta-distribution delays, character-by-character typing simulation, and model response padding.
triggers:
  - chat timing
  - typing simulation
  - humanlike typing
  - natural typing
  - chat delay
  - first token delay
  - typing speed
  - chat animation
  - streaming delay
---

# Humanlike Chat Timing Simulation

Psychological principles and implementation patterns for AI chat interfaces that feel natural and engaging without being frustratingly slow.

## Psychology Principles

### Weber-Fechner Law
Humans perceive time logarithmically. A 100ms difference feels significant at 500ms total but imperceptible at 5000ms. Design timing variations proportionally.

### Habituation Prevention
Predictable delays train unconscious expectations, making the interface feel "mechanical." Use randomized delays with non-uniform distributions to maintain perceived spontaneity.

### Cognitive Load Simulation
Human speech naturally varies:
- **Starting:** More deliberate (gathering thoughts)
- **Middle:** Flow state (confident delivery)
- **Ending:** Slight acceleration (wrapping up)
- **Transitions:** Pauses at punctuation, paragraphs

## Implementation

### First Token Delay (2-5 seconds)

Use beta distribution approximation for natural randomness weighted toward middle values:

```typescript
function generateFirstTokenDelay(): number {
  const MIN_MS = 2000;
  const MAX_MS = 5000;

  // Beta distribution approximation using sum of uniforms
  const u1 = Math.random();
  const u2 = Math.random();
  const u3 = Math.random();
  const beta = (u1 + u2 + u3) / 3;

  // Micro-jitter prevents pattern detection
  const jitter = (Math.random() - 0.5) * 400;

  return Math.round(MIN_MS + beta * (MAX_MS - MIN_MS) + jitter);
}
```

### Character-by-Character Typing

Variable delays simulate natural speech rhythm:

```typescript
interface TimingConfig {
  CHAR_DELAY_BASE_MS: 12;      // Base per-character delay
  PAUSE_COMMA_MS: 80;          // Brief pause
  PAUSE_PERIOD_MS: 150;        // Sentence boundary
  PAUSE_PARAGRAPH_MS: 300;     // Thought transition
  SPEED_VARIATION_MIN: 0.6;    // Speed range multiplier
  SPEED_VARIATION_MAX: 1.4;
}

function calculateCharDelay(
  char: string,
  context: string,
  position: number  // 0-1 normalized position in message
): number {
  let delay = TIMING.CHAR_DELAY_BASE_MS;

  // Punctuation pauses (natural speech cadence)
  if (char === "," || char === ";") delay += TIMING.PAUSE_COMMA_MS;
  else if (char === "." || char === "!" || char === "?") delay += TIMING.PAUSE_PERIOD_MS;
  else if (char === "\n") delay += TIMING.PAUSE_PARAGRAPH_MS;

  // Position-based speed variation
  let speedFactor = 1.0;
  if (position < 0.15) {
    // Starting - more deliberate
    speedFactor = 0.8 + Math.random() * 0.3;
  } else if (position > 0.85) {
    // Finishing - wrap-up acceleration
    speedFactor = 1.1 + Math.random() * 0.2;
  } else {
    // Middle - natural variation
    speedFactor = TIMING.SPEED_VARIATION_MIN +
      Math.random() * (TIMING.SPEED_VARIATION_MAX - TIMING.SPEED_VARIATION_MIN);
  }

  // Occasional micro-hesitation (1 in 50) - thought gathering
  if (Math.random() < 0.02) {
    delay += 50 + Math.random() * 100;
  }

  return Math.round(delay * speedFactor);
}
```

### Model Response Padding

When real AI model responds faster than target delay, pad the difference:

```typescript
function createPaddedDelay(targetDelay: number) {
  const startTime = Date.now();

  return {
    targetDelay,
    startTime,

    async waitRemaining(): Promise<void> {
      const elapsed = Date.now() - startTime;
      const remaining = targetDelay - elapsed;
      if (remaining > 0) {
        await new Promise(r => setTimeout(r, remaining));
      }
      // If model was slower, returns immediately
    },

    getElapsed(): number {
      return Date.now() - startTime;
    },
  };
}

// Usage with real AI streaming:
async function streamWithPadding(prompt: string) {
  const delay = createPaddedDelay(generateFirstTokenDelay());

  const response = await fetch('/api/chat', { body: prompt });
  const reader = response.body.getReader();

  // Wait for minimum delay before showing first token
  await delay.waitRemaining();

  // Now stream normally
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    displayChunk(value);
  }
}
```

## React Implementation

```typescript
// Progressive typing effect with natural rhythm
useEffect(() => {
  if (!streamingTarget) return;

  if (displayedContent.length < streamingTarget.length) {
    const currentChar = streamingTarget[displayedContent.length];
    const position = displayedContent.length / streamingTarget.length;
    const delay = calculateCharDelay(currentChar, streamingTarget, position);

    const timer = setTimeout(() => {
      setDisplayedContent(prev =>
        streamingTarget.slice(0, prev.length + 1)
      );
    }, delay);

    return () => clearTimeout(timer);
  }
}, [streamingTarget, displayedContent]);
```

## Key Metrics

| Aspect | Target Range | Rationale |
|--------|--------------|-----------|
| First token | 2-5s | Simulates "thinking" without frustration |
| Base char delay | 10-15ms | ~65-100 chars/sec (natural typing) |
| Comma pause | 60-100ms | Brief breath |
| Period pause | 120-180ms | Sentence boundary |
| Paragraph pause | 250-350ms | Topic transition |
| Speed variation | 0.6x-1.4x | Natural rhythm |

## Anti-Patterns to Avoid

1. **Fixed delays** - Creates predictable rhythm that feels robotic
2. **Linear distributions** - Real delays cluster around means
3. **No position awareness** - Constant speed feels mechanical
4. **Skipping punctuation pauses** - Loses speech-like cadence
5. **Delays > 6 seconds** - User perceives as "broken"

## Testing

```typescript
it("produces varied delays (not predictable)", () => {
  const delays = new Set<number>();
  for (let i = 0; i < 50; i++) {
    delays.add(Math.round(generateFirstTokenDelay() / 100));
  }
  // Should have 10+ different 100ms buckets
  expect(delays.size).toBeGreaterThan(10);
});

it("averages near distribution middle", () => {
  const delays = Array.from({ length: 1000 }, generateFirstTokenDelay);
  const avg = delays.reduce((a, b) => a + b) / delays.length;
  const expectedMid = (MIN_MS + MAX_MS) / 2;
  expect(Math.abs(avg - expectedMid)).toBeLessThan(500);
});
```

## References

- Weber-Fechner psychophysics law
- Nielsen Norman Group: Response Time Guidelines
- Human typing speed studies (~40-60 WPM average)
