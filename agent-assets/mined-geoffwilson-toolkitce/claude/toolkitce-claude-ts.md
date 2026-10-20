# Working on the TypeScript port

`ts/` is a port of the RPG Toolkit 3 engine to TypeScript and a canvas: you drop a game's ZIP
on a page and it plays in the browser. It sits beside the Java engine in the same repository
and shares its research, not its code.

Read `README.md` first. It is the *why* — what the engine does and why each piece is the shape
it is. This file is the *how*: the rules for working here.

## Follow trans3, not the Java port

The rule from the repository root applies here and is the first rule: **check the original
before writing anything, and say in a comment which function it came from.** Guessing at
plausible behaviour produces something that runs and is quietly wrong.

The Toolkit 3 source is not in this repository. On this machine it is beside it:

| Path from `ts/` | What is in it |
| --- | --- |
| `../../rpgtoolkit/vc/trans3/` | The engine. `rpgcode/functions.cpp` holds the commands, `rpgcode/CProgram.cpp` the machine and the operators, `rpgcode/lex.txt` and `yacc.txt` the grammar, `movement/`, `render/`, `common/board.cpp` |
| `../../rpgtoolkit/vc/tkCommon/` | Canvases, tiles, the DOS palette |
| `../../rpgtoolkit/vb/` | The 3.0.6 Visual Basic engine and the editor, which is where the file formats are written |
| `../src/` | The Java engine, in this repository |

The repository's own `CLAUDE.md` writes those as `../vc/` because it was written for a
checkout that lives inside `rpgtoolkit/`. Both are the same tree.

**The Java engine is a second opinion, not the specification.** Almost every rule in it names
the `trans3` function it came from, and that research is the expensive part — so read it to
find *where* to look. But where it made a choice that only makes sense on the JVM, follow the
original instead; `README.md` lists the three that matter. Several bugs fixed here were
inherited from it, and one (`grow` assuming a polygon's curl) is still there.

Two things that follow, both from the root `CLAUDE.md` and both still true:

- **Do not reproduce the original's bugs.** Where it is plainly broken, implement what it
  meant and say so in a comment.
- **Do reproduce its quirks.** A game may depend on them. The difference is judgement, so
  write down which one you decided it was.

## Comments explain why, not what

The valuable comment records why something is the shape it is — what the original did, what
broke, what the file format actually says. A comment restating the line below it is noise.
Match the density and tone of the surrounding code.

Javadoc-style blocks use `<p/>` between paragraphs, which is what the existing files do.

## Testing

```bash
npm test                          # vitest, 321 tests
npx tsc -p tsconfig.json --noEmit  # strict, with noUncheckedIndexedAccess
```

Keep both passing. The engine draws to a screen and reads a keyboard, so most of it cannot be
tested directly; the pattern that works, and is used throughout, is to **extract the rule and
test that**, leaving the drawing and the input around it untested — `Game.scrollFor`,
`polygonsOverlap`, `PathVector.blocks`, `splitLines`, `stanceNumbered`.

Where a rule takes a random roll, mock it rather than seeding one. Where a rule takes time,
install `game.clock` rather than waiting: `test/screen-effects.test.ts` shows both.

Two things that will catch you out in a test:

- **Comparing two screens as arrays is a deep equality over a megabyte** and costs more than
  everything else in the file. Fingerprint them.
- **An ordinary program hands the screen back to the board when it ends**, so a test that
  checks what a program drew has to keep it alive — end it on `wait()`.

## Driving a game without a keyboard

The rest is verified by running a real game headlessly and looking at a frame. `tools/drive.ts`
is the workhorse:

```bash
npx vite-node tools/drive.ts -- ../games/Afterlife \
  --frames=6000 --key="$(python3 -c "print(','.join(['-']*60+['ENTER']))")" \
  --shot=/tmp/frame.png
```

It has a virtual clock, so a nine second title sequence takes nine simulated seconds and not
nine real ones; `--walk`, `--key` (a `-` is a frame with nothing pressed), `--click`, `--run`
and `--trace` are the rest. Pictures are decoded by shelling out to ImageMagick, which stands
in for the browser's `createImageBitmap`.

`tools/programs.ts <game>` parses every program in a game — the `.prg` files and the inline
board and sprite ones — and prints the commands the engine does not implement, with counts.
Run it before and after a change to measure what the change bought.

Read the frame you took. Half the bugs found here looked like something else until a
screenshot was compared with what the game meant to draw.

## Game data is not in this repository

`public/*.zip` and `games/` are ignored, as `game/` is at the root: they are other people's
games and hundreds of megabytes of them. Point the tools at a Toolkit project of your own.

Four are used in the writing here, and each is exercised for a different reason:

- **the 3.1 demo** — the reference game, small, and the only one in `games/` by default
- **Afterlife** — a 3.1 game whose boards are pictures rather than tiles, with a bitmap font
  and a long scripted introduction
- **Platinum Blade** — a version 2 game, converted to version 3 by the Java converter first;
  the engine never sees a version 2 file
- **ThreeGuysNoBeer, Garquest** — load, but lean on plugins the port has no answer for

## No game here has been played to the end

The tests pass and every program parses, and none of that says a game finishes. Expect bug
reports and expect them to be real.

When something misbehaves the first question is not "what did I break" but "what does the
original do here" — most of these are places the port is thin rather than places it regressed.
Reproduce it headlessly before changing anything, and check the symptom is what it looks like:
the overlapping prologue text was `pause()` resolving to a built-in that should not exist,
and chasing it as a drawing bug would have found the wrong answer.

## Things that will catch you out

Most of these have a section of their own in `README.md`. In brief:

- **Visual Basic writes True as -1**, so every boolean in these formats is a test against
  zero, never against one.
- **Counts in the file formats are upper bounds.** The editor writes `For t = 0 To sz`, so a
  list holds `sz + 1` entries.
- **A COLORREF is `0x00BBGGRR`**, not the other way round.
- **A picture has no alpha in the original.** `drawImage` is `StretchDIBits` with `SRCCOPY`;
  transparency only ever comes from a *named colour* passed to `BltTransparent`. Toolkit tile
  formats do have a real mask, so alpha is honoured for them and ignored for picture files.
- **Tile types are a bit field**, not an enumeration. Test with a mask, never for equality —
  except the under-vector rule, which really is an equality test.
- **Asset paths are case-insensitive and use backslashes**, through `GameFiles`. Folder names
  come from `paths.h` — `Item\`, `Misc\`, `Bkrounds\` — and are not to be guessed from the
  extension.
- **A command that waits asks to be run again** rather than blocking, and keeps its state on
  the `Game` because a machine unit has nowhere to put it. `wait`, `animation`, `earthquake`,
  `fade`, `cursorMapRun`, anything that needs a picture.
- **A built-in command shadows a game's own method of the same name**, which is what yacc.txt
  does — so registering a command that does not exist in the original silently breaks every
  game that defines it. `pause()` is the cautionary tale.
- **`~=` is not-equal**, and an unset variable equals both `0` and `""`.

## Committing

Do not commit `public/*.zip`, `games/`, `node_modules/` or `dist/`. Commit only when asked.
