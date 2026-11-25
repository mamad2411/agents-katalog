---
name: ascii-this
description: Renders text as ASCII art block letters, draws ASCII diagrams (boxes, arrows, system interactions, flowcharts, sequence diagrams), or produces freehand ASCII drawings of any subject (animals, objects, scenes, characters). Use when user says "ascii this", "draw a diagram", "draw a dragon", "make ascii art", "show me how X interacts with Y", "render in ascii", "ascii-ify", or asks for a system/flow/sequence diagram or any drawing in text form.
---

# ASCII-This

Three modes — pick automatically based on the request:

| Request type | Mode |
|---|---|
| "ascii this: Hello" / render text as big letters | **Text art** |
| "draw how A talks to B" / system diagram / flowchart / sequence | **Diagram** |
| "draw a dragon" / "draw a cat" / any subject or scene | **Freehand** |

---

## Mode 1 — Text Art

Render the requested string as 5-row block letters.

**Rules:**
1. Use the character map below — one glyph per character.
2. Separate glyphs with one column of spaces.
3. Output exactly 5 rows inside a fenced code block.
4. Unsupported characters → 3-wide `?` block.

### Character map (5 rows)

```
A        B        C        D        E        F        G
 ###     ####     ###     ####     #####    #####     ###
#   #    #   #   #   #    #   #    #        #        #   #
#####    ####    #        #   #    ####     ####     #
#   #    #   #   #   #    #   #    #        #        #  ##
#   #    ####     ###     ####     #####    #        ####

H        I        J        K        L        M        N
#   #      #         #    #   #    #        #   #    ##  #
#   #      #         #    #  #     #        ## ##    # # #
#####      #         #    ###      #        # # #    # # #
#   #      #    #    #    #  #     #        #   #    #  ##
#   #      #     ###      #   #    #####    #   #    #   #

O        P        Q        R        S        T        U
 ###     ####      ###     ####      ###     #####    #   #
#   #    #   #    #   #    #   #    #   #      #      #   #
#   #    ####     #   #    ####      ##        #      #   #
#   #    #        #  ##    #  #        ##      #      #   #
 ###     #         ## #    #   #    ###        #       ###

V        W        X        Y        Z
#   #    #   #    #   #    #   #    #####
#   #    #   #     # #     # #         #
 # #     # # #      #       #         #
  #      ## ##     # #      #        #
  #      #   #    #   #     #       #####

0        1        2        3        4        5        6
 ###      ##      ####      ###     #  #     #####     ###
#   #    # #         #        #    #  #     #         #
#  ##      #        #       ##     #####     ###      ####
## #       #       #          #       #         #    #   #
 ###      ###     #####     ###        #     ###      ####

7        8        9        !        ?
#####     ###      ###       #       ###
    #    #   #    #   #      #      #   #
   #      ###     ####       #          #
   #     #   #       #       #         #
   #      ###     ###                 #
```

### Example

Input: `Hi`
```
#   #      #
#   #      #
#####      #
#   #      #
#   #      #
```

---

## Mode 2 — ASCII Diagrams

Draw system interaction diagrams, flowcharts, and sequence diagrams using boxes, arrows, and labels.

### Box styles

```
Single border          Double border          Rounded
+------------------+   +==================+   .-------------------.
|  Component Name  |   ||  Component Name ||   |  Component Name  |
+------------------+   +==================+   '-------------------'
```

Use **single border** by default. Use **double border** for external systems or databases. Use **rounded** for users/actors.

### Arrow styles

| Meaning | Style |
|---|---|
| Sync call / request | `----->` |
| Response / return | `<-----` |
| Async / event | `- - ->` |
| Bidirectional | `<---->` |
| Dependency / uses | `......>` |

Label arrows inline above or below the shaft:
```
        [HTTP POST /orders]
Client -----------------------> API Gateway
       <-----------------------
            [200 OK + body]
```

### Layout rules

1. **Left-to-right** for request/response flows; **top-to-bottom** for flowcharts and sequences.
2. **Align boxes** on a grid — pad labels so box widths match within a column.
3. **Group related components** with a surrounding border and a title:
```
+-- Payment Domain --------------------------------+
|  +------------+       +----------------------+   |
|  |  Checkout  |-----> |  Payment Service     |   |
|  +------------+       +----------------------+   |
+-------------------------------------------------+
```
4. **Sequence diagrams**: draw vertical lifelines with `|`, use `-->` for messages, label each step with a number.
```
Client          API             DB
  |               |              |
  |--[1: GET /]--->|              |
  |               |--[2: query]-->|
  |               |<--[3: rows]--|
  |<--[4: 200]-----|              |
```

5. Keep the total width ≤ 80 characters when possible; break into sub-diagrams if needed.
6. Add a legend when arrow types or box styles are mixed.

### Example — system interaction

Request: *"Show how a browser talks to an API that queries a database"*

```
.----------.     +------------------+     +==============+
|  Browser |     |   REST API       |     ||  PostgreSQL ||
|          |     |                  |     ||  Database   ||
'----------'     +------------------+     +==============+
     |                   |                      |
     |  [GET /products]  |                      |
     |------------------>|                      |
     |                   |  [SELECT * FROM      |
     |                   |   products]          |
     |                   |--------------------->|
     |                   |                      |
     |                   |  [rows]              |
     |                   |<---------------------|
     |  [200 OK + JSON]  |                      |
     |<------------------|                      |
```

### Example — flowchart

Request: *"Draw the order processing flow"*

```
        +-------------+
        | Order placed |
        +------+------+
               |
               v
        +------+------+
        | Validate     |
        | payment      |
        +------+------+
               |
       +-------+-------+
       |               |
   [success]        [failure]
       |               |
       v               v
+------+------+  +-----+------+
| Fulfillment |  | Notify user|
| triggered   |  | of failure |
+-------------+  +------------+
```

---

## Mode 3 — Freehand Drawing

Draw any subject as expressive ASCII art — animals, objects, characters, scenes, vehicles, food, etc.

### Principles

1. **Silhouette first** — capture the overall shape and recognisable outline before adding detail.
2. **Use the full ASCII palette** — choose characters for their visual weight and shape:

| Character(s) | Use for |
|---|---|
| `@`, `#`, `W`, `M` | Dense fills, dark areas, fur, shadow |
| `o`, `0`, `*`, `·` | Eyes, spots, round features |
| `/`, `\`, `_`, `-` | Smooth curves, limbs, ground lines |
| `(`, `)`, `[`, `]` | Body curves, enclosed shapes |
| `~`, `=`, `-` | Horizontal texture, water, ground |
| `"`, `'`, `` ` ``, `,` | Fur, feathers, grass, fine texture |
| `^`, `v`, `<`, `>` | Pointed features, beaks, ears, arrows |
| `|` | Vertical lines, legs, tails, stems |
| `.` | Fine detail, eyes, distant objects |

3. **Scale to the subject** — small subjects (cat, cup) fit in ~10×20 chars; large or complex subjects (dragon, landscape) deserve ~20–40 rows.
4. **Orientation** — animals and characters face right by default unless specified.
5. **Add context** — include a simple ground line (`~~~~~~~~~~` or `__________`) or background elements when it adds clarity.
6. **Label optionally** — if the subject might be ambiguous, add a small caption below.

### Example — dragon

```
                                                    / \
          /\                 /\                   /   |
         /  \  _____________/  \______           /   /
        / /\/                         \__       /  /`
       / /   \  <*>               <*>   \\____/ /`
      ( (     \___         ___________//      /`
       \ \        \       /           \\    /`
        \ \        \_____/     /\      \\  |
         \/\              ____/  \______\\ |
            \____________/                \|
             |    |   ||  \
           __/    |   ||   \___
          /      _|_  ||       \
         /______/   \_/\_______/
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
```

### Example — cat

```
  /\_____/\
 (  o   o  )
 =( Y  Y )=
  )       (
 (_/-^^^-\_)
  |       |
  (__|__|__)
```

### Example — rocket

```
      /\
     /  \
    | () |
    |    |
   /|    |\
  / |    | \
 /  |    |  \
|  /|    |\  |
| / |    | \ |
|/  '----'  \|
    |    |
    |    |
   /|    |\
  ( |____| )
  (________}
   \  /\  /
    \/  \/
```

### Handling difficult subjects

- **Abstract concepts** (love, freedom): render a symbolic representation (heart, bird in flight).
- **Scenes** (forest, city): use layered rows — sky, background, midground, foreground.
- **Very detailed requests**: produce the best-effort render, then offer to zoom into a specific part.

---

## Activation

Once loaded, stay active for the entire session. Infer the mode from context. When ambiguous, ask: *"Big letters, a diagram, or a drawing?"*
