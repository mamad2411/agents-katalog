---
name: ai-ppt-generator
description: Generate PPT with SkillBoss API Hub. Smart template selection based on content.
metadata: { "openclaw": { "emoji": "??", "requires": { "bins": ["python3"], "env":["SkillBoss_API_KEY"]},"primaryEnv":"SkillBoss_API_KEY" } }
---

# AI PPT Generator

Generate PPT using SkillBoss API Hub with intelligent template selection.

## Smart Workflow
1. **User provides PPT topic**
2. **Agent asks**: "Want to choose a template style?"
3. **If yes**  Show styles from `ppt_theme_list.py`  User picks  Use `generate_ppt.py` with chosen `tpl_id` and real `style_id`
4. **If no**  Use `random_ppt_theme.py` (auto-selects appropriate template based on topic content)

## Intelligent Template Selection
`random_ppt_theme.py` analyzes the topic and suggests appropriate template:
- **Business topics**  ҵ style
- **Technology topics**  δƼ style
- **Education topics**  ֻͨ style
- **Creative topics**  Ȥζ style
- **Cultural topics**  й or Ļ style
- **Year-end reports**  ܽ style
- **Minimalist design**  ƽԼ style
- **Artistic content**   style

## Scripts
- `scripts/ppt_theme_list.py` - List all available templates with style_id and tpl_id
- `scripts/random_ppt_theme.py` - Smart template selection + generate PPT
- `scripts/generate_ppt.py` - Generate PPT with specific template (uses real style_id and tpl_id from API)

## Key Features
- **Smart categorization**: Analyzes topic content to suggest appropriate style
- **Fallback logic**: If template not found, automatically uses random selection
- **Complete parameters**: Properly passes both style_id and tpl_id to API

## Usage Examples
```bash
# List all templates with IDs
python3 scripts/ppt_theme_list.py

# Smart automatic selection (recommended for most users)
python3 scripts/random_ppt_theme.py --query "˹ܷչƱ"

# Specific template with proper style_id
python3 scripts/generate_ppt.py --query "ͯӢμ" --tpl_id 106

# Specific template with auto-suggested category
python3 scripts/random_ppt_theme.py --query "ҵܽ" --category "ҵ"
```

## Agent Steps
1. Get PPT topic from user
2. Ask: "Want to choose a template style?"
3. **If user says YES**:
   - Run `ppt_theme_list.py` to show available templates
   - User selects a template (note the tpl_id)
   - Run `generate_ppt.py --query "TOPIC" --tpl_id ID`
4. **If user says NO**:
   - Run `random_ppt_theme.py --query "TOPIC"`
   - Script will auto-select appropriate template based on topic
5. Set timeout to 300 seconds (PPT generation takes 2-5 minutes)
6. Monitor output, wait for `is_end: true` to get final PPT URL

## Output Examples
**During generation:**
```json
{"status": "PPT", "run_time": 45}
```

**Final result:**
```json
{
  "status": "PPT",
  "is_end": true,
  "data": {"ppt_url": "https://...ppt"}
}
```

## Technical Notes
- **API integration**: Fetches real style_id from SkillBoss API Hub for each template
- **Error handling**: If template not found, falls back to random selection
- **Timeout**: Generation takes 2-5 minutes, set sufficient timeout
- **Streaming**: Uses streaming API, wait for `is_end: true` before considering complete

