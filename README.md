# DM Tools: A Toolbox for Book of Trials Dungeon Mastery
## Designed and Written by Josh Beale

## Project Description
This project is a set of tools designed to assist in running tabletop game sessions using the Book of Trials Ruleset.

## [Book of Trials Ruleset](https://docs.google.com/document/d/1p_RwhtKsnAQmfPTkylT3e4ozbonpYsL-1mCrwfyxOQw/edit?usp=sharing)  

## Software Requirements
- Python version 3.12.3 or higher

```
Repository Structure
.
├── README.md
├── gameTools                   <- All tools for Dungeon Masters.
│   ├── playerManager.py        <- Core module that grants player management capabilites to all other tools.
│   ├── prepTools               <- Tools used during preparation for sessions.
│   │   └── lootGenerator.py    <- A tool to generate treasure hoards based on party size, level, dungeon size, and difficulty.
│   └── sessionTools            <- Tools used during sessions to assist in running the game.
└── savedData                   <- Data generated and read by gameTools, stored in .tsv format.
    ├── lootByLevel.tsv         <- Loot by level chart used for generating treasure hoards.
    └── players.tsv             <- Players managed by the playerManager module.
```