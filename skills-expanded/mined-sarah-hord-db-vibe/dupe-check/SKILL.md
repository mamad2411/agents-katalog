---
name: dupe-check
description: Check whether a plugin or skill idea already exists in the vibe marketplace. Use this before building a new plugin or skill to avoid duplicating existing work. Triggers on "dupe check", "duplicate check", "does a skill exist for", "is there already a plugin for", "check if this exists", "before I build a plugin".
---

# Dupe Check Skill

Before building a new vibe plugin or skill, check whether something equivalent already exists.

## Step 1: Collect the Idea

Ask the user (if not already provided):
- What would this plugin/skill be named?
- What does it do in 1-2 sentences?
- What user prompts would trigger it?

## Step 2: Fetch Live Marketplace Data

Fetch the latest plugin list from the vibe GitHub marketplace:

```bash
gh api repos/databricks-field-eng/vibe/contents/.claude-plugin/marketplace.json \
  --hostname github.com | python3 -c "
import json, sys, base64
data = json.load(sys.stdin)
content = base64.b64decode(data['content']).decode()
marketplace = json.loads(content)
for p in marketplace['plugins']:
    print(f\"PLUGIN: {p['name']}\")
    print(f\"  Description: {p['description']}\")
    print(f\"  Keywords: {', '.join(p.get('keywords', []))}\")
    print()
"
```

If the GitHub call fails (e.g. not authenticated), fall back to the locally installed plugins:

```bash
for plugin_dir in ~/.claude/plugins/cache/fe-vibe/*/; do
  plugin_name=$(basename "$plugin_dir")
  latest=$(ls "$plugin_dir" | sort -V | tail -1)
  plugin_json="$plugin_dir$latest/.claude-plugin/plugin.json"
  if [ -f "$plugin_json" ]; then
    desc=$(python3 -c "import json; d=json.load(open('$plugin_json')); print(d.get('description',''))" 2>/dev/null)
    echo "PLUGIN: $plugin_name"
    echo "  Description: $desc"
  fi
done
```

## Step 3: Enumerate All Skills

Get the full list of skills with their descriptions from locally installed plugins:

```bash
for plugin_dir in ~/.claude/plugins/cache/fe-vibe/*/; do
  plugin_name=$(basename "$plugin_dir")
  latest=$(ls "$plugin_dir" | sort -V | tail -1)
  skills_dir="$plugin_dir$latest/skills"
  if [ -d "$skills_dir" ]; then
    for skill_dir in "$skills_dir"/*/; do
      skill_name=$(basename "$skill_dir")
      desc=$(grep -m1 "^description:" "$skill_dir/SKILL.md" 2>/dev/null | sed 's/^description: //' | sed 's/^"//' | sed 's/"$//')
      echo "SKILL: $plugin_name / $skill_name"
      echo "  $desc"
      echo
    done
  fi
done
```

## Step 4: Analyze for Overlap

Compare the user's idea against all plugins and skills. Look for:

1. **Exact duplicate** — A plugin/skill already does precisely this. Name it and explain what it covers.
2. **Strong overlap** — An existing skill covers 70%+ of the use case. Name it, describe the overlap, and note the gap.
3. **Partial overlap** — An existing skill is related but the idea adds clear new value. Suggest extending the existing plugin rather than creating a new one.
4. **No overlap** — The idea is genuinely new.

Also check:
- Could this be added as a skill to an existing plugin rather than a new plugin?
- Are there any skills in non-default plugins (fe-ee, fe-ssagent, fe-manager, fe-dnb-hunting, etc.) that match?

## Step 5: Report Results

Present results clearly:

---

### Dupe Check: `<idea name>`

**Verdict:** [DUPLICATE / STRONG OVERLAP / PARTIAL OVERLAP / CLEAR GAP]

**Existing coverage:**

| Plugin | Skill | What it already covers |
|--------|-------|------------------------|
| ...    | ...   | ...                    |

**Gap (if any):**
What the existing skills don't cover and the idea would add.

**Recommendation:**
- DUPLICATE → Don't build it. Use `/existing-skill` instead.
- STRONG OVERLAP → Consider contributing to the existing plugin rather than creating a new one. Reach out to the author.
- PARTIAL OVERLAP → Build it, but consider placing it inside `<existing-plugin>` as a new skill rather than a standalone plugin.
- CLEAR GAP → Go ahead and build. Use `/plugin-builder:create-plugin` or `/plugin-builder:create-skill` to scaffold it.

---

## Notes

- The marketplace only shows published plugins. Work-in-progress plugins in the vibe repo that haven't been released may not appear.
- If you're unsure after the check, ask in `#fe-vibe-plugins` on Slack before building.
- When in doubt, extending an existing plugin is usually preferred over creating a new one — it keeps the ecosystem consolidated.
