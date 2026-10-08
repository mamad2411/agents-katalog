# Scratchpad

## Disaster Relief Twitter Bot Implementation Plan

### Requirements Analysis

1. Bot should monitor Twitter mentions
2. When mentioned with disaster info, verify through news API
3. If verified, create a tweet with donation address
4. Store all processed mentions and created tweets in JSON

### Tools Needed

1. MentionProcessingTool

   - Monitor and index new mentions
   - Store in JSON file
   - Track processed mentions

2. NewsVerificationTool

   - Verify disaster claims using news API
   - Currently using mock data
   - Will be replaced with real news API later

3. DisasterTweetTool

   - Create tweets for verified disasters
   - Generate donation addresses
   - Store tweet details

4. DisasterStorageTool
   - Store all disaster relief campaigns
   - Track donation addresses
   - Monitor campaign status

### Implementation Steps

[ ] Create tools directory structure
[ ] Implement MentionProcessingTool
[ ] Implement NewsVerificationTool
[ ] Implement DisasterTweetTool
[ ] Implement DisasterStorageTool
[ ] Update TwitterAgent.ts to use new tools
[ ] Add data storage structure
[ ] Test the implementation

### Data Structure

```json
{
  "disasters": {
    "disaster_id": {
      "poster_name": "string",
      "poster_id": "string",
      "tweet_id": "string",
      "address": "string",
      "location": "string",
      "verified": boolean,
      "created_at": "timestamp",
      "status": "active|closed"
    }
  },
  "processed_mentions": {
    "mention_id": {
      "tweet_id": "string",
      "processed_at": "timestamp",
      "status": "verified|rejected"
    }
  }
}
```

# Lessons

## User Specified Lessons

- You have a python venv in ./venv. Use it.
- Include info useful for debugging in the program output.
- Read the file before you try to edit it.
- Due to Cursor's limit, when you use `git` and `gh` and need to submit a multiline commit message, first write the message in a file, and then use `git commit -F <filename>` or similar command to commit. And then remove the file. Include "[Cursor] " in the commit message and PR title.

## Cursor learned

- For search results, ensure proper handling of different character encodings (UTF-8) for international queries
- Add debug information to stderr while keeping the main output clean in stdout for better pipeline integration
- When using seaborn styles in matplotlib, use 'seaborn-v0_8' instead of 'seaborn' as the style name due to recent seaborn version changes
- Use 'gpt-4o' as the model name for OpenAI's GPT-4 with vision capabilities
