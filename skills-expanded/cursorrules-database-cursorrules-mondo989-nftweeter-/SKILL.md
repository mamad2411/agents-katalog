# NFT Watcher Bot - Cursor Rules

## Project Guidelines
- Avoid complex abstractions in MVP; duplication is fine if it helps clarity.
- Use Express for any web server needs
- Use SCSS for styling if web UI is added
- Keep console logging simple and informative
- Prioritize reliability over optimization

## Nut-Tree-Fork Configuration

### Screen Region for Rarity Capture
The rarity region should be configured based on your screen resolution.
Update these values in `src/monitor.js`:

```javascript
// Example for 1920x1080 resolution
// Adjust based on where the rarity number appears on OpenSea
const RARITY_REGION = new Region(
  850,      // X coordinate of top-left corner
  400,      // Y coordinate of top-left corner  
  200,      // Width of the capture area
  60        // Height of the capture area
);
```

### Tips for Finding Correct Coordinates
1. Take a screenshot of the OpenSea collection page
2. Open in an image editor to find pixel coordinates
3. The rarity number is usually in the item details section
4. Add some padding around the text for better OCR results

### Nut-Tree-Fork Best Practices
- Add delays between keyboard/mouse actions using sleep()
- Use `await` for all nut-tree-fork operations
- Test screen capture coordinates before running the full bot
- Handle errors gracefully - automation can be flaky
- Make sure to grant accessibility permissions on macOS

### macOS Permissions Required
- Accessibility (System Preferences > Security & Privacy > Privacy > Accessibility)
- Screen Recording (System Preferences > Security & Privacy > Privacy > Screen Recording)
- Add Terminal or your Node.js executable to both lists

You always confirm before creating / adding new files to the project !IMportant