---
name: polaris-video-thumbnail
description: Shopify Polaris Video thumbnail component. Use as clickable video placeholder. Opens video player in modal or fullscreen.
---

# Video Thumbnail

## When to use
Create a clickable placeholder for video content. Display as play button for video players within media cards. Shows video preview image with optional progress indicator.

## Props
- `thumbnailUrl` string - URL source for thumbnail image
- `videoLength?` number - Length of video in seconds. Defaults to 0.
- `videoProgress?` number - Video progress in seconds. Displays progress bar. Only renders when videoLength set. Defaults to 0.
- `showVideoProgress?` boolean - Allow video progress display. Defaults to false.
- `accessibilityLabel?` string - Custom ARIA label. Defaults to "Play video of length {duration}".
- `onClick` () => void - Callback to trigger video player (modal/fullscreen)
- `onBeforeStartPlaying?` () => void - Callback on hover/focus/touch (for preload)

## Examples
```jsx
import { MediaCard, VideoThumbnail } from '@shopify/polaris';

<MediaCard
  title="Turn your side-project into a business"
  description="Learn how to scale your business"
  primaryAction={{ content: 'Learn more', onAction: () => {} }}
>
  <VideoThumbnail
    videoLength={80}
    thumbnailUrl="https://example.com/video-thumb.jpg"
    onClick={() => {
      // Trigger video player
    }}
  />
</MediaCard>
```

## Best practices
- Wrap in MediaCard component
- Use preview image that communicates video subject
- Include video timestamp
- Capture frame from actual video
- Crop to 16:9 aspect ratio
- Center on subject, avoid cropping important details

## Accessibility
- Images are decorative background (skipped by screen readers)
- Play button is keyboard accessible
- Aria-label includes timestamp when videoLength set
- Without videoLength, label reads "Play video"
- Progress bar accessible when enabled

## Required components
- Must be wrapped in MediaCard component

## Related components
- Thumbnail (for static images)
- MediaCard (required wrapper)
