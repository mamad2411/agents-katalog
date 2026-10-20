## Background
I have amassed a large collection of 8- and 16-bit retro console games for NES, SNES, and Sega Genesis. These are split between physical cartridges and SD-based flash cartridges that contain and can swap between hundreds of ROM files. At this point, the sheer number of games I have access to is extremely large and divided between multiple formats, so I need a friendly way to browse them and decide what I want to play.

## Project
I'd like for you to design a web-browser based, Netflix-style user interface that I can use to easily browse my library of games. It should support many ways for me to "slice and dice" the library and search by various criteria, mark "favorites", etc.

## Requirements

### User Interface
- A sleek, modern UI reminiscent of popular streaming services. It should include sophisticated animations and transitions, with a visual aesthetic that brings to mind the mid-90s era of 16-bit console games while remaining clean and current-feeling.
- Each game in the list should have a full battery of content associated with it that is displayed in various ways across the UI, including but not limited to (you may need to pull content from the web or use external URLs for these):
  - Title
  - System
  - Release Year
  - Box art image
  - Gameplay screenshots
  - Genre
  - Tags
  - Description
  - External media (e.g. YouTube embeds and/or links to playthrough videos)
  - A flag for whether the game is accessible currently ("Cart Purchased?" OR "In Multi-cart?" are TRUE) or needs to be acquired ("Cart Purchased?" AND "In Multi-cart?" are both FALSE)
  - Any others you think would be useful
- A system of curating favorites and/or creating dynamic sub-lists of games to save and modify later
- A means of adding new games to the library later
- A means of editing the content associated with existing games

### Technical
- A javascript frontend of your choice backed by a server side implementation, NOT a single HTML file
- Support to configure custom fonts for the UI
- Initial library content to use as a starting point is in the CWD in game_list.csv