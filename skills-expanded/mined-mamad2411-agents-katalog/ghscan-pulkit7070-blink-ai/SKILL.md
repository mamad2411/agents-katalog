---
description: Screen capture and analysis capabilities for visual AI assistance
---

# Screen Capture Skill

Enables the AI to see and analyze the user's screen for debugging, documentation, and visual assistance.

## Capabilities

- **Full Screen Capture**: Capture entire screen or specific monitor
- **Window Capture**: Capture specific application window
- **Area Selection**: Capture user-selected screen region
- **OCR**: Extract text from screenshots using Tesseract.js
- **Visual Analysis**: Analyze screenshots using vision-capable AI models
- **Screen Recording**: Record screen activity (optional)

## Tools

### capture_screen
Capture a screenshot of the current screen.

**Input:**
- `type`: 'full' | 'window' | 'selection'
- `windowName`: Target window name (for 'window' type)
- `bounds`: Selection bounds {x, y, width, height} (for 'selection' type)

**Output:**
- `imageData`: Base64 encoded PNG image
- `width`: Image width
- `height`: Image height
- `timestamp`: Capture timestamp

### extract_text_from_image
Perform OCR on an image to extract text.

**Input:**
- `imageData`: Base64 encoded image
- `language`: OCR language (default: 'eng')

**Output:**
- `text`: Extracted text
- `confidence`: OCR confidence score
- `blocks`: Text blocks with bounding boxes

### analyze_screenshot
Analyze a screenshot using AI vision capabilities.

**Input:**
- `imageData`: Base64 encoded image
- `query`: Analysis query (e.g., "What errors do you see?")

**Output:**
- `analysis`: AI analysis of the screenshot
- `findings`: Key findings/observations
- `suggestions`: Recommended actions

### get_active_window
Get information about the currently active window.

**Output:**
- `title`: Window title
- `appName`: Application name
- `bounds`: Window bounds {x, y, width, height}

## Usage Examples

```typescript
// Capture full screen
const screenshot = await tools.capture_screen({ type: 'full' });

// Extract text from screenshot
const ocr = await tools.extract_text_from_image({
  imageData: screenshot.imageData
});

// Analyze screenshot
const analysis = await tools.analyze_screenshot({
  imageData: screenshot.imageData,
  query: 'What code errors are visible?'
});
```

## Configuration

No additional API keys required. Uses:
- Electron's `desktopCapturer` API for screen capture
- Tesseract.js for OCR (local processing)
- Vision-capable AI model for analysis

## Best Practices

1. Always ask user permission before capturing screen
2. Highlight or annotate areas of interest in the UI
3. Use OCR to extract code/errors for copy-paste
4. Respect user privacy - don't capture sensitive information
5. Provide quick capture shortcuts (e.g., Cmd+Shift+5)