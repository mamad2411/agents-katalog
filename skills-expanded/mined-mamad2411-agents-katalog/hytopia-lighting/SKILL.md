---
name: hytopia-lighting
description: Helps configure lighting in HYTOPIA SDK games. Use when users need ambient light, sun/directional light, point lights, spot lights, or day/night cycles. Covers Light class, shadows, and performance optimization.
---

# HYTOPIA Lighting

This skill helps you configure lighting in HYTOPIA SDK games.

**Documentation:** https://dev.hytopia.com/sdk-guides/lighting

## When to Use This Skill

Use this skill when the user:

- Wants to set up ambient or directional lighting
- Needs to create point lights or spot lights
- Asks about day/night cycles
- Wants to configure shadows
- Needs to optimize lighting performance
- Asks about dynamic lighting effects

## Light Types Overview

HYTOPIA supports five light types:

| Type | Description | Shadows | Performance |
|------|-------------|---------|-------------|
| Ambient | Base world lighting | No | Cheap |
| Sun/Directional | Single directional source | Yes | Cheap |
| Point | Emits from a point in all directions | Yes | Expensive |
| Spot | Cone-shaped emission | Yes | Expensive |
| Emissive | From blocks (coming soon) | No | N/A |

## Ambient Light

Base lighting that affects the entire world.

```typescript
import { World } from 'hytopia';

// Set ambient light color and intensity
world.setAmbientLight({
  color: { r: 0.3, g: 0.3, b: 0.4 },  // Slight blue tint
  intensity: 0.5
});

// Bright daytime ambient
world.setAmbientLight({
  color: { r: 1, g: 1, b: 1 },
  intensity: 0.8
});

// Dark nighttime ambient
world.setAmbientLight({
  color: { r: 0.1, g: 0.1, b: 0.2 },
  intensity: 0.2
});
```

## Sun Light (Directional)

Single light source that affects the entire world with shadows.

```typescript
import { World } from 'hytopia';

// Set sun position and color
world.setSunLight({
  position: { x: 100, y: 200, z: 50 },  // Direction FROM this point
  color: { r: 1, g: 0.95, b: 0.8 },     // Warm sunlight
  intensity: 1.0
});

// Sunset lighting
world.setSunLight({
  position: { x: 50, y: 20, z: 0 },  // Low sun
  color: { r: 1, g: 0.5, b: 0.2 },   // Orange
  intensity: 0.8
});

// Moonlight
world.setSunLight({
  position: { x: -50, y: 100, z: 30 },
  color: { r: 0.6, g: 0.7, b: 1 },  // Cool blue
  intensity: 0.3
});
```

## Point Lights

Emit light in all directions from a point. **Use sparingly - expensive!**

```typescript
import { Light, LightType } from 'hytopia';

// Create point light
const torchLight = new Light({
  type: LightType.POINT,
  position: { x: 10, y: 5, z: 10 },
  color: { r: 1, g: 0.7, b: 0.3 },  // Warm fire color
  intensity: 2.0,
  range: 15  // Light falloff distance
});

world.addLight(torchLight);

// Dynamic light following entity
const playerLight = new Light({
  type: LightType.POINT,
  color: { r: 1, g: 1, b: 1 },
  intensity: 1.5,
  range: 10
});

// Attach to entity
playerLight.setTrackedEntity(player.entity);
world.addLight(playerLight);
```

## Spot Lights

Cone-shaped lights. **Use sparingly - expensive!**

```typescript
import { Light, LightType } from 'hytopia';

// Create spot light
const spotlight = new Light({
  type: LightType.SPOT,
  position: { x: 0, y: 20, z: 0 },
  target: { x: 0, y: 0, z: 0 },      // Point light looks at
  color: { r: 1, g: 1, b: 1 },
  intensity: 3.0,
  range: 30,
  angle: 45,        // Cone angle in degrees
  penumbra: 0.5     // Soft edge (0 = hard, 1 = very soft)
});

world.addLight(spotlight);

// Flashlight attached to player
const flashlight = new Light({
  type: LightType.SPOT,
  color: { r: 1, g: 1, b: 0.9 },
  intensity: 2.5,
  range: 25,
  angle: 30,
  penumbra: 0.3
});

flashlight.setTrackedEntity(player.entity);
world.addLight(flashlight);
```

## Day/Night Cycle

```typescript
import { World } from 'hytopia';

class DayNightCycle {
  private world: World;
  private timeOfDay: number = 0;  // 0-24 hours

  constructor(world: World) {
    this.world = world;
  }

  update(deltaTime: number) {
    // Advance time (adjust speed as needed)
    this.timeOfDay += deltaTime * 0.001;  // 1 real second = 1 game hour
    if (this.timeOfDay >= 24) this.timeOfDay = 0;

    this.updateLighting();
  }

  updateLighting() {
    const hour = this.timeOfDay;

    // Calculate sun position
    const sunAngle = ((hour - 6) / 12) * Math.PI;  // 6am = horizon, noon = top
    const sunY = Math.sin(sunAngle) * 200;
    const sunX = Math.cos(sunAngle) * 200;

    // Determine lighting based on time
    if (hour >= 6 && hour < 18) {
      // Daytime
      const intensity = Math.sin(sunAngle) * 0.8 + 0.2;

      this.world.setSunLight({
        position: { x: sunX, y: Math.max(sunY, 10), z: 0 },
        color: this.getSunColor(hour),
        intensity
      });

      this.world.setAmbientLight({
        color: { r: 0.6, g: 0.7, b: 0.8 },
        intensity: 0.4 + intensity * 0.3
      });
    } else {
      // Nighttime
      this.world.setSunLight({
        position: { x: -100, y: 100, z: 50 },
        color: { r: 0.5, g: 0.6, b: 0.8 },
        intensity: 0.15
      });

      this.world.setAmbientLight({
        color: { r: 0.1, g: 0.1, b: 0.2 },
        intensity: 0.2
      });
    }
  }

  getSunColor(hour: number): { r: number, g: number, b: number } {
    if (hour < 7 || hour > 17) {
      // Sunrise/sunset - orange
      return { r: 1, g: 0.5, b: 0.2 };
    } else if (hour < 9 || hour > 15) {
      // Morning/evening - warm
      return { r: 1, g: 0.85, b: 0.7 };
    } else {
      // Midday - white
      return { r: 1, g: 0.98, b: 0.95 };
    }
  }
}
```

## Dynamic Light Effects

### Flickering Torch

```typescript
class FlickeringLight {
  private light: Light;
  private baseIntensity: number;

  constructor(light: Light, baseIntensity: number = 2.0) {
    this.light = light;
    this.baseIntensity = baseIntensity;
  }

  update() {
    // Random flicker
    const flicker = 0.8 + Math.random() * 0.4;  // 0.8 to 1.2
    this.light.setIntensity(this.baseIntensity * flicker);
  }
}
```

### Pulsing Light

```typescript
class PulsingLight {
  private light: Light;
  private time: number = 0;
  private minIntensity: number;
  private maxIntensity: number;
  private speed: number;

  constructor(light: Light, min: number, max: number, speed: number) {
    this.light = light;
    this.minIntensity = min;
    this.maxIntensity = max;
    this.speed = speed;
  }

  update(deltaTime: number) {
    this.time += deltaTime * this.speed;
    const t = (Math.sin(this.time) + 1) / 2;  // 0 to 1
    const intensity = this.minIntensity + t * (this.maxIntensity - this.minIntensity);
    this.light.setIntensity(intensity);
  }
}
```

### Explosion Flash

```typescript
function createExplosionFlash(position: Vector3) {
  const flash = new Light({
    type: LightType.POINT,
    position,
    color: { r: 1, g: 0.8, b: 0.3 },
    intensity: 10,
    range: 30
  });

  world.addLight(flash);

  // Fade out
  let intensity = 10;
  const fadeInterval = setInterval(() => {
    intensity -= 0.5;
    if (intensity <= 0) {
      clearInterval(fadeInterval);
      world.removeLight(flash);
    } else {
      flash.setIntensity(intensity);
    }
  }, 16);
}
```

## Best Practices

1. **Limit dynamic lights** - Point and spot lights are expensive; use 2-4 max
2. **Use ambient + sun** - Cover most lighting needs cheaply
3. **Bake static lighting** - Use block textures for static light sources
4. **Interpolation is automatic** - Light changes smooth automatically
5. **Range matters** - Shorter range = better performance
6. **Color temperature** - Warm (fire) vs cool (moonlight) sets mood

## Performance Tips

```typescript
// Good: Few dynamic lights
const torchLight = new Light({ type: LightType.POINT, range: 10 });
const playerLight = new Light({ type: LightType.POINT, range: 8 });

// Bad: Too many dynamic lights
for (let i = 0; i < 50; i++) {
  world.addLight(new Light({ type: LightType.POINT }));  // Don't do this!
}

// Better: Use ambient + sun for general lighting
world.setAmbientLight({ color: { r: 0.4, g: 0.4, b: 0.5 }, intensity: 0.6 });
world.setSunLight({ position: { x: 100, y: 200, z: 50 }, intensity: 1.0 });
// Then add only 2-3 point lights for important effects
```
