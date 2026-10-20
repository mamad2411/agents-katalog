# Working on ToolkitCE

ToolkitCE reimplements the RPG Toolkit 3 engine in Java. Almost every question about what
the engine *should* do has an answer in the original source, so the first rule is:

## Check the original before writing anything

The Toolkit 3 source sits beside this repository, one level up:

| Path | What is in it |
| --- | --- |
| `../vc/trans3/` | The engine. `rpgcode/functions.cpp` holds the 282 RPGCode commands, `rpgcode/CProgram.cpp` the operators and control words, `movement/CSprite/` collision and program activation, `render/` the board renderer, `fight/fight.cpp` the battle rules |
| `../vc/tk3menu/` | The menu plugin, in C++, and the plugin SDK |
| `../vb/tk3Fight/` | The battle screen plugin, in Visual Basic 6 |
| `../vc/tkCommon/` | Shared code: canvases, tiles, the DOS palette |
| `../vb/Toolkit/` | The editor, which is where the file formats are written |

Read the original, port its behaviour, and say in a comment which function it came from.
Guessing at plausible behaviour produces something that runs and is quietly wrong, and the
games are old enough that nobody will report the difference.

Two things follow from this:

- **Do not reproduce the original's bugs.** Where it is plainly broken, implement what it
  meant and say so in a comment. Examples already in the tree: `giveExperience` loops forever
  at maximum level; `performAttack` reads a player through a union as an enemy.
- **Do reproduce its quirks.** A game may depend on them. The difference is judgement, so
  write down which one you decided it was.

## Comments explain why, not what

The code is a port of a fifteen-year-old C++ engine, so the valuable comment is the one that
records why something is the shape it is — what the original did, what broke, what the file
format actually says. A comment restating the line below it is noise. Match the density and
tone of the surrounding code.

Javadoc uses `<p/>` between paragraphs, which is what the existing files do.

## Testing

`./gradlew build` compiles and runs the tests. Keep them passing.

The engine draws to a screen and reads a keyboard, so most of it cannot be tested directly.
The pattern that works, and is used throughout, is to **extract the rule as a static method
and test that**, leaving the drawing and input around it untested:

- `GraphicsEngine.scrollFor(position, boardSize, resolution)` — how far the board scrolls
- `GraphicsEngine.encounterDue(...)` — whether walking starts a fight
- `PhysicsEngine.fires(program, inside, moved, ...)` — whether a board program activates
- `FightEngine.damageDealt(damage, defence, critical, random)` — how hard a blow lands

Where a rule takes a `Random`, pass one that hands out scripted values rather than seeding a
real one; a single fake value cannot stand in for two different rolls.

## Driving a game without a keyboard

The rest is verified by running a real game headlessly and looking at a frame. See the
diagnostics table in `README.md`. The two that do the heavy lifting:

```bash
java -cp build/classes/java/main \
  -Dtkce.skipStartup=true -Dtkce.walk=DOWN \
  -Dtkce.screenshot=/tmp/frame.png -Dtkce.screenshotFrame=300 \
  uk.co.tkce.engine.Driver game/sindemo/SinDemo.gam
```

`-Dtkce.run=<program.prg>` runs a program before play starts, which reproduces something
from the middle of a game without playing up to it. Drop a temporary `.prg` in the game's
`Prg` folder, use it, then delete it.

`ProgramCheck <main.gam>` parses every program in a game and lists the commands the engine
does not implement. Run it before and after a change to measure what the change bought.

Game data is not in this repository. Point the engine at a Toolkit project of your own.

## No game here has been played to the end

The tests pass, every program parses and every asset loads to its last byte, and none of
that says a game finishes. Expect bug reports and expect them to be real. Version 3 games
are the safer half, since the engine is a port of the one they were written for; a version 2
game has to survive the conversion first, and the conversion has met one game.

So when something misbehaves the first question is not "what did I break" but "what does the
original do here" — most of these are places the port is thin rather than places it
regressed. Reproduce it headlessly before changing anything, with `-Dtkce.run=` and a
screenshot, and check the symptom is what it looks like: the missing companions, the
apparently inverted `push` and the tiny message font were one bug between them — only the
selected character existed — and chasing them separately would have found three wrong
answers.

## Things that will catch you out

- **The player's position is stored in screen space, not board space.** Board layers are
  drawn offset by `shiftX`/`shiftY` while the player is drawn at their location untouched,
  and collision adds the shift back. Anything that places the player must work out the scroll
  and subtract it — see `scrollToPlayer()`.
- **Counts in the file formats are upper bounds.** The editor writes `For t = 0 To sz`, so a
  list holds `sz + 1` entries. Reading `count` of them ends short.
- **Movement is by whole tiles, and so is everything that follows from it.**
  `CSprite::m_bPxMovement` starts false, is set only by a save file or the `pixelMovement()`
  command, and no shipped game calls it - the main file's own pixel movement setting is read
  and then never used. So a move is 32 pixels, the keyboard is read only between moves
  (`input.cpp` queues one while the game state is idle), and `playerDoneMove` tests the board
  programs and the random encounter once per move rather than once per frame. A move that
  walks into something ends immediately with its target still on the far side, which is how
  pressing against a door or a person sets their program off.
- **A board smaller than the screen is centred, and the scroll offset goes negative to do
  it.** A screen position is a board position less `shiftX`, so `scrollFor` returning -16
  insets the board by 16 rather than scrolling it. Toolkit 3 pins such a board to the top
  left corner (`g_screen.left` is clamped at zero in `CSprite::move`); version 2 centred it,
  and a 2001 screenshot of Platinum Blade running shows its 19 by 11 tile boards - 608 by
  352 pixels - exactly 16 in and 64 down inside a 640 by 480 window. All but three of its
  193 boards are that size, which is one screenful, which is why so many of them are joined
  edge to edge.
- **Walking off the edge of a board travels, or is a wall.** `checkBoardEdges` returns
  `TT_SOLID` when there is no link that way, and `doBoardEdges` follows the one there is,
  placing the sprite against the opposite edge with its other coordinate untouched. 104 of
  Platinum Blade's 193 boards are joined this way, so without it half the game is a cliff.
- **A key can run a program, and the menu key may not open a menu.** The main file binds one
  run time program to a key of its own and fifty more besides; `openMainFile` folds them into
  one list, dropping every slot with no program, and `scanKeys` runs each match before it
  answers the menu key. A game whose menu is a program of its own binds it here: Platinum
  Blade's Return runs `MENU1.PRG` and Sin Demo's runs `Menu-Main.prg`. See
  `GraphicsEngine.requestRunTimePrograms`.
- **Tile types are a bit field**, not an enumeration. Test with a mask, never for equality.
- **Seeks must use `BinaryIO.skipFully`.** `InputStream.skip` may skip fewer bytes than asked
  and a buffered stream routinely does, which reads garbage silently.
- **Asset paths are case-insensitive** through `GamePath`, because games were authored on
  Windows. Never open a game file with `new File(...)` directly.
- **Folder names come from `../vc/trans3/common/paths.h`** — `SpcMove\`, `StatusE\`,
  `Bkrounds\`. Do not guess them from the file extension.
- **`removePath` has two overloads and they behave differently.** The one argument version
  cuts at the last backslash; the two argument version cuts at a named folder and returns the
  name untouched when it does not contain it, preserving subfolders. Using the wrong one
  turns `Item\Weapons\sword.itm` into `sword.itm`, and cuts a thread whose "file name" is a
  line of RPGCode in half at the first slash. `SaveState.removePath` and `removePathTo`.
- **A type declaration character is part of a variable's name here, and is not in the
  original.** The grammar's `tdc` rule (`var_identifier: IDENTIFIER tdc` in `yacc.txt`)
  matches a trailing `$` or `!` and throws it away, so Toolkit 3 treats `hp!` and `hp` as
  one variable; `Parser.identifierExpression` keeps the character, making them two. No
  shipped game depends on either reading, but anything that looks a variable up by name has
  to know which it is: `GameControl.statVariable` strips the character, `SaveState` keeps
  it. Worth fixing in the parser one day, which would make both agree with the grammar.

## Pathfinding: two algorithms, and the game picks

`itemPath` and friends go through `PathFinder`, a port of `CPathFind`. There are two
subclasses because the original has two, and which one a game gets is its own setting
(`MAIN_FILE::pfHeuristic`, `Project.getPathfindingAlgorithm`): the shipped games differ, so
both are needed and both are exercised.

- `TilePathFinder` searches a 32 pixel grid, for tile movement. A step is allowed when the
  sprite's base, swept from one point to the next, touches nothing solid.
- `VectorPathFinder` builds a visibility graph, for pixel movement: grow every solid area by
  the sprite base's largest extent, and the nodes are the grown corners.

The trap is `PathVector.blocks`, ported from `CPfVector::contains`. Ordinary collision
detection is useless there, because the nodes ARE the corners of the areas being tested, so
every step would begin and end touching one. Read the comment before touching it.

**A sprite's collision base is relative to its feet, and so is everything the pathfinder
does.** For a board sprite that is what `getBaseVector()` gives. For the player it is the
same, though it takes a moment to see: `PhysicsEngine.calculateDifferences` adds the vector
correction, which turns the top left corner the player's location holds into the base point.
Subtracting that correction again puts the base above the sprite's head and the search finds
nothing anywhere.

## Multitasking threads are Java threads that never run at the same time

Toolkit 3's threads are cooperative and have nothing to do with operating system threads: a
thread is a `CProgram` with a position in its own list of machine units, and `gameLogic()`
calls `CThread::execute(units)` once a frame for each of them.

A tree walking interpreter keeps that position on the Java call stack, where it cannot be put
down. So each RPGCode thread is given a Java thread to hold its stack, and they take turns by
passing a baton: `RpgThread.step()` hands it over, waits, and takes it back. **Exactly one of
them, or the game loop, is running at any moment.** Nothing in the engine needs locking, and
a thread that calls something blocking blocks the whole game, as it did in the original.

Two things follow:

- `Scope`'s call frames are per Java thread while its globals are shared, which is what makes
  a global global. Do not add per-program interpreter state without deciding which it is.
- The budget is what stops a `while(true)` thread from freezing the game, so anything that
  runs statements must go through `Interpreter.execute` and its `Cooperative` hook.

## The `tk*` constants are compile-time, not variables

`tkMV_PAUSE_THREAD`, `tkVT_SOLID`, `tkDIR_N` and the rest are substituted by the lexer, as
`CProgram::addConstant` and lex.txt do it. Adding one as a global instead would let a program
assign to it, and would write it into every save file. `Lexer.CONSTANTS`.

## Version 2 games are converted once, not read as the game runs

Platinum Blade is the only version 2 game here, in the **TK2.1 ASCII** format — CRLF text,
one value per line:

```
RPGTLKIT BOARD / 2 / 1 / 0 / NOCODE / 19 / 11 / House.tst42 / -50 -50 -50 / ...
```

At `HEAD` **both** trans3 (`../vc/trans3/common/board.cpp`) and the 3.1 editor
(`../vb/tkCommon/modules/CommonBoard.bas`) refuse major 2 / minor 0 or 1 with "Please save
this board using RPGToolkit version 3.0.6 or below to upgrade the file format". Read only
`HEAD` and version 2 support looks like reverse engineering seven formats with no reference.
It is not. It is a port, like everything else here, and `src/uk/co/tkce/convert/` is it.

**The readers are in the rpgtoolkit repository's history** (2175 commits, back to 2004):

| Commit | What |
| --- | --- |
| `8f8f03fb` | "Updated for 3.0.6.", 2005-03-26 — the last version that reads ASCII |
| `08f2fe3d` | "3.0.4 dev", 2004-08-06 |
| `526b8ecd` | "Board saving.", 2006-07-11 — where the board ASCII branch was deleted |

Every format has an ASCII branch at `8f8f03fb`, in `vb/tkCommon/modules/`, at a label named
`ver2old<something>`:

```bash
git -C .. show 8f8f03fb:vb/tkCommon/modules/CommonBoard.bas
```

Find the branches with `grep -E "Input #|fread\("` — enemies use `fread()` where boards use
`Input #`, so grepping for one alone reports formats as having no ASCII path when they do.

The board needs a second source: reading the old text is only half of it, and the rest —
vectorising the tile types, collapsing the per tile shading into one layer, giving a program
the tile it sat on, turning tile positions into pixels — is in trans3's `pvVersion` branch
(`board.cpp`, roughly lines 575-975) and `vectorizeLayer` in
`../vc/tkCommon/board/conversion.cpp`, both at `HEAD`.

Things worth knowing before touching it:

- **The converter writes version 3 binary and the engine never sees a version 2 file.** That
  is what the original did, it keeps the engine single format, and it lets `FormatAudit`
  check the output with loaders that are already trusted.
- **A version 2 file that stops early is normal.** Four of Platinum Blade's items end before
  their description; its enemies end before their four animation names; its boards end
  before the day and night fields. Visual Basic raised an error, `On Error Resume Next`
  swallowed it, and the field kept the value `Clear` had given it. `AsciiFile` returns empty
  and zero past the end for the same reason — do not make it throw.
- **A blank line is zero.** Every version 2 character's size field is one, and reading it as
  anything else sends the reader 44,000 lines off course.
- **Counts are still upper bounds** in what the converter writes. A list of one entry writes
  a count of zero; a list of none writes -1 where the format allows it and one empty entry
  where it does not.
- **`.gph` and `.tbm` are version 3 formats**, not version 2 ones. Toolkit 3 reads a tile in
  a file of its own as readily as a tileset (`CTile::openTile`), and its own conversion
  writes a version 2 sprite out as tile bitmaps. Both are in `toolkit/types/` and both are
  reached through `TileSetCache.tile`, which is the one place that turns a tile reference
  into an image.
- **A version 2 game could turn its built in menu off, and the conversion must keep that.**
  "use built in menu? 0-yes, 1-no" is the fourth field of the main file. The original's
  conversion drops it and answers `tk3menu.dll` whatever the game said, which hangs a menu
  the game never had off the same key as the menu it wrote. `V2Main.menuPlugin` writes no
  plugin instead, and `GameControl.hasMenu` is what the engine asks before opening one.
- **Board vectors and sprites only act on their own layer.** `CSprite::boardCollisions` skips
  anything on another layer, and an under vector never blocks at all. Platinum Blade is the
  game that shows it: its first board pens the player into one square on layer 2 with stairs
  down to layer 1, and without the layer test every direction is a wall.

## Version 2 RPGCode differs from version 3, and both must work

Version 3.1 replaced the Visual Basic interpreter with a flex lexer and a yacc grammar, and
in several places the new one reads an old program differently. All of them matter, all are
ported, and all were found by running Platinum Blade.

- **A lone `=` in a condition compares.** `identifier ASSIGN value` is an assignment
  everywhere in `yacc.txt`, so 3.1 reads `if (gotKey!=1)` as an assignment whose value is the
  condition. The engine before it promoted the sign — `RPGCodeParser.bas`'s `evaluate`: "If
  (signs(idx - 1) = "=") Then signs(idx - 1) = "=="" — for any program that had not declared
  `#strict`, and nothing declares it. Platinum Blade has 710 conditions of that shape and Sin
  Demo, which is a 3.1 game, has 54 of the form `if(raise=1)`, three in a row testing one, two
  and three. `Parser.condition()`.
- **A `*` after a command's brackets is a comment.** Version 2's parser found the command
  name, took what was inside the brackets and never looked at the rest of the line, so
  `#MouseClick(x!,y!)   *waits for a click` ran. 3.1's lexer takes only `**` and a `*` opening
  a line. `Lexer.afterAVersion2Command()`, which is narrow enough to leave multiplication
  alone: the line must open with `#` and its brackets must already have closed.

- **An unquoted word is a literal.** Version 2 had no grammar: `GetElement` cut the argument
  list on its commas and `getValue` decided what each piece was, so a word naming no variable
  was simply text. Games write it constantly — `fontProperties(Verdana, 16)`,
  `fontPropertiesExtended(off, off, off, 0ff, 7)`, `push(w, "janus")`. Here the same word
  parses as a variable and reads as zero, so `Arguments.literal()` falls back to the name it
  was written with. **`push()` still uses `text()`**, so its 160 unquoted directions in
  Platinum Blade do nothing; that is the next thing to fix here.
- **Version 2 wrote brackets on everything, `return` included.** `#return()` is a keyword
  followed by an empty pair, which the grammar has no rule for. `Parser.returnStatement()`.
- **A `>` before `)` or `,` belongs to the string in front of it.** Platinum Blade's menu has
  `#drawText(160,36,"<1lev!">)` four times where it meant `"<1lev!>"`. Version 2 stripped the
  first and last character of a quoted argument without checking what they were, so the `>`
  went back inside the text. No valid program has `>` there — a comparison needs a right hand
  side — so putting it back cannot break anything else. `Lexer.scanOperator()`.
- **`setConstants` fills in the variables the engine reserves**: `gameTime!`,
  `playerHandle[]$`, `playerX/Y/Layer[]!`, `boardTitle[]$`, `constant[]!`, `music$`. A program
  reads them and never writes them. 3.0.6 refreshes them when the board changes and 3.1 makes
  them live (`virtualvar.cpp`); this refreshes before each program runs, which is the cheap
  way to the live answer. `GameControl.setConstants()`.
- **A type character after a subscript belongs to the name.** `boardTitle[1]$` is the array
  `boardTitle$` indexed by 1 — the grammar's `identifier LARRAY value RARRAY tdc` — and that
  is where the parser stores it. `Splice` has to know, or `"<boardTitle[1]$>"` looks up
  something nothing ever wrote.

## The version 2 engine is in the tree, and its strings are a source

`game/platinumblade069/` is the shipped version 2 game, and it includes the engine that ran
it. Neither `vc/` nor `vb/` has any version 2 source, but the binaries carry every error
message, and those give a command's arity and argument types exactly:

```bash
strings -e l -n 4 game/platinumblade069/trans2.exe | grep -i "error: fade"
strings -a -n 3 game/platinumblade069/Plugin/TrueType.dll | grep -i drawtext
```

`trans2.exe` also holds the whole command-name table. Use it before guessing.

- **Some commands are a plugin's, not the Toolkit's.** `drawText`, `fontProperties` and
  `fontPropertiesExtended` come from `Plugin/TrueType.dll`, which Platinum Blade's menu and
  credits are built out of; version 3 has nothing of the sort. It draws through `CreateFontA`
  and `TextOutA`, so its font is its own and `font()` does not reach it, its `y` is the top
  of the character cell, and `fontPropertiesExtended`'s four flags are CreateFont's weight,
  italic, underline and strike out, in that order, followed by "BoldAmt ... 0 - 10". That
  last reading is inferred from the API it calls, not read from source — nothing of the
  plugin survives but its strings.

## The party is a list of sprites, not one player

`addPlayer` loads a character into the party; `putPlayer` puts one on a board. Everyone except
the character being controlled is drawn from `Player.getBoardX/Y`, in board pixels, and the
selected one from `currentXLocation`, in screen pixels, with the scroll added back. That
asymmetry is the engine's, not the format's — see the first entry under "Things that will
catch you out" — so anything that reaches for a party member's position must ask which of the
two it is holding.

`push("n", "Janus")`, `stance(9, "Janus")` and `playerLocation("Janus", ...)` all take a
handle, and ignoring it walks the player instead: Platinum Blade's opening scene pushes Janus
north eight times, so the player drifts up the board while the companion never appears.
`Party.find` matches a name, a file name or a place in the party, because games use all three.

## Committing

Do not commit `game/`, build output, or anything under `.gradle/`. Commit only when asked.
