---
name: Weather&Webcam
description: Fetches current weather from wttr.in and automatically captures a live webcam image from Meteoblue or Windy for the requested location. Use it when the user asks for the weather and wants to see a real image of the current conditions.
---

# Weather Location

This skill automates weather data retrieval and live webcam image capture to provide a complete visual report.

## Workflow

1.  **Get weather (wttr.in)**:
    - Execute `curl -s "wttr.in/[Location]?format=%l:+%c+%t+%h+%w"` to get basic data (location, icon, temperature, humidity, and wind).
    - Note: Encode spaces in the URL (e.g., `Sant+Adria+de+Besos`).

2.  **Search for Webcam (Meteoblue/Windy)**:
    - Perform a web search (`web_search`) for `meteoblue [Location] webcam` or `windy [Location] webcam`.
    - Select the Meteoblue link that lists webcams for that area (e.g., `meteoblue.com/.../webcams/...`).

3.  **Capture Image (Clean Method)**:
    - Navigate to the page and use `browser(action=snapshot)` to find direct image URLs (e.g., `imgproxy.windy.com/...`).
    - **IMPORTANT**: Avoid `browser(action=screenshot)` to prevent double images (previews).
    - Download the image with `exec(command="curl -s '[URL]' -o /tmp/webcam.jpg")`.
    - Prefer 16:9 images if available.

4.  **User Response**:
    - Send the image using `message(action=send, media="/tmp/webcam.jpg", caption="[wttr.in data]\n[Comment]")`.
    - Respond with `NO_REPLY` in the main session after using the `message` tool.

## Usage Examples

- "What's the weather like in London?"
- "How's the sky in New York right now?"
- "Show me the weather in Barcelona"
