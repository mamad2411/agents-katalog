---
name: appshots-library
description: >
  Saved design management for App Screenshots.
  Save, load, organize into folders, import/export .appshots files.
  Includes design versioning and iteration tips.
---

# App Screenshots Library

Manage saved screenshot designs: save, load, organize, and share.

## Save & Load Workflow

### Save Current Design

```bash
# Save single design
appshots editor save-design --name "My Design v1"

# Save multi-screenshot set
appshots multi save-design --name "iPhone 6.7 Screenshots v1"

# Update existing saved design (overwrites)
appshots multi save-design --name "iPhone 6.7 Screenshots v1" --override
```

### Load Saved Design

```bash
# List all saved designs first
appshots library list

# Load by ID
appshots editor load-design --id <design-id>
```

### Best Practice: Version Your Designs

When iterating on screenshots (especially for A/B testing), save named versions:

```bash
appshots multi save-design --name "Dark Mode v1 - Original"
# ... make changes ...
appshots multi save-design --name "Dark Mode v2 - Bolder Text"
# ... make changes ...
appshots multi save-design --name "Dark Mode v3 - With Gradients"
```

This makes it easy to revert and compare during Apple's Product Page Optimization testing.

## Folders

Organize designs by device, platform, or campaign:

```bash
# List all folders
appshots library folders

# Create folders by device type
appshots library create-folder --name "iPhone 6.7"
appshots library create-folder --name "iPad Pro 13"
appshots library create-folder --name "Mac App Store"

# Move designs into folders
appshots library move --design-id <design-id> --folder-id <folder-id>

# Delete folder
appshots library delete-folder --id <folder-id>
appshots library delete-folder --id <folder-id> --with-designs   # also delete contents
```

## Import / Export

Share designs across machines or with team members:

```bash
# Export as .appshots file
appshots library export --id <design-id>

# Import from .appshots file
appshots library import --file /path/to/design.appshots
```

## Renaming & Deleting

```bash
appshots library rename --id <design-id> --name "New Name"
appshots library delete --id <design-id>
```

## Viewing Details

```bash
# Get full design details (JSON)
appshots --json library get --id <design-id>
```

## Commands Reference

| Command | Description |
|---------|-------------|
| `library list` | List all saved designs |
| `library get --id X` | Get design details |
| `library delete --id X` | Delete a design |
| `library rename --id X --name "..."` | Rename a design |
| `library folders` | List all folders |
| `library create-folder --name "..."` | Create a folder |
| `library delete-folder --id X` | Delete a folder |
| `library move --design-id X --folder-id Y` | Move to folder |
| `library import --file /path` | Import .appshots file |
| `library export --id X` | Export as .appshots |
