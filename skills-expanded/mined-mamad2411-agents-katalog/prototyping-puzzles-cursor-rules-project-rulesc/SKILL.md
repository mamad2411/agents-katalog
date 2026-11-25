---
description: 
globs: 
alwaysApply: true
---
# Prototyping puzzles

This repository contains a series of puzzles designed to help you learn how to communicate visual design changes using Cursor AI. The goal is to help you practice making things look "not ugly" by effectively describing design improvements to AI.


## Repository structure

```
app/
├── prototypes/           # Main working directory for all puzzles
│   ├── puzzle-01/       # Each puzzle lives in its own folder
│   │   ├── README.md    # Puzzle instructions and requirements
│   │   ├── page.tsx     # The puzzle component
│   │   └── styles.module.css
│   └── puzzle-02/
├── components/          # Shared components
└── public/             # Global static assets

Each puzzle has its own CSS file. When students ask you to update a design, make sure to update only that project's CSS. If you're unclear of which project they want to edit, ask them.