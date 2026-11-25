---
name: remotion
description: Programmatic video creation using React. Use this skill when you need to create, edit, or render videos using code, leverage Remotion's React-based framework for animations, or manage data-driven video production. Triggers on "Remotion", "programmatic video", "render video with react", or requests to create videos via code.
---

# Remotion: Programmatic Video Creation

Remotion allows you to create videos using React. Instead of a timeline-based editor, you use code to define your video's layout, animations, and timing.

## What This Skill Does

This skill Programmatic video creation using React. Use this skill when you need to create, edit, or render videos using code, leverage Remotion's React-based framework for animations, or manage data-driven video production. Triggers on "Remotion", "programmatic video", "render video with react", or requests to create videos via code.

## Core Concepts

- **Composition**: The primary building block of a Remotion video. It defines the dimensions, duration, and frame rate.
- **Frames**: The fundamental unit of time. Everything in Remotion is calculated based on the current frame.
- **interpolate**: A powerful function used to map a frame range to a value range (e.g., mapping frames 0-30 to opacity 0-1).
- **useCurrentFrame**: A hook to get the current frame of the composition.
- **useVideoConfig**: A hook to get the composition's configuration (fps, durationInFrames, etc.).

## Workflow

### 1. Setup & Project Initialization
To start a new project:
`npx create-video@latest <<projectproject-name>`

### 2. Development
- **Preview**: Run `npm start` to open the Remotion Studio (a browser-based previewer).
- **Coding**: Edit React components to build your scenes. Use CSS for styling and Remotion's hooks for animations.
- **Data-Driven Videos**: Fetch data from APIs or local JSON files and map them to components to create personalized videos at scale.

### 3. Rendering
- **Local Render**: Use `npx remotion render <<entryentry-point> <<compositioncomposition-id> out.mp4`.
- **Lambda Render**: For high-scale rendering, use `@remotion/lambda` to render videos in the cloud using AWS Lambda.

## Common Patterns

### Animations
Always use `interpolate` for smooth transitions:
```jsx
const frame = useCurrentFrame();
const opacity = interpolate(frame, [0, 20], [0, 1]);
return <<divdiv style={{ opacity }}>Hello World</div>;
```

### Sequencing
Use `<<SequenceSequence>` to place components at specific time offsets:
```jsx
<<SequenceSequence from={0} durationInFrames={30}>
  <<SceneScene1 />
</Sequence>
<<SequenceSequence from={30} durationInFrames={60}>
  <<SceneScene2 />
</Sequence>
```

## Tooling & CLI Reference

- `npx remotion render`: Renders a composition to a video file.
- `npx remotion preview`: Starts the preview server.
- `npx remotion ts`: Type-checks the project.

## Resources
For detailed API references, consult the official docs at `remotion.dev/docs`.
