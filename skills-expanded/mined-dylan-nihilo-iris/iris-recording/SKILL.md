---
name: iris-recording
description: "Record a polished demo video or GIF of an app window on macOS with the iris CLI: automatic zoom on each action, smooth pointer, backdrop, idle time removed. Use when asked to record, capture or film an interface you operate yourself (computer use, Playwright, CDP, accessibility), or to turn such a run into an MP4 or GIF. Works unattended and without the real mouse."
---

<!-- Written by `iris skill` from the guide in Sources/IrisCore/Support/Guide.swift; edit the guide there. -->

# Recording with iris

iris records a window or a screen area and renders a polished video from it: a gradient
backdrop, rounded window with a shadow, a smooth pointer, click rings, captions, and a camera
that zooms on each action and pulls back afterwards. It is built for recordings where an agent, not a
person, operates the interface. The camera goes by what you declare with `iris mark`, so it
works even when your actions never touch the real mouse (DOM or CDP clicks, accessibility
actions, scripted input).

Every command prints JSON. Every command acts on the most recent session unless you pass a
session directory. Run `iris help` for all options.

## The workflow

1. Find the window: `iris windows` lists `id`, `app`, `title` and `frame` (screen points).
2. Start: `iris start --app "Notes" --name onboarding`
   (or `--window-id N`, `--title TEXT`, or `--display 0 [--region x,y,w,h]`).
   It returns at once; the recorder runs in the background. Note `captureRect` in the reply,
   and read `note` if there is one: it says what this recording cannot show. When you have
   only just launched the application, add `--wait 10`: iris then gives the window that long
   to appear.
3. For each action, declare it first, then do it:
   `iris mark --kind click --x 640 --y 412` and then perform the click.
4. Stop and render: `iris stop --render --format both --out ~/Movies/onboarding`
   The reply lists the files written (`.mp4`, and `.gif` with `--format gif|both`). A
   `warning` in it means the picture never changed: the recording is of nothing.
5. Look at the result before you report it: `iris sheet` writes `sheet.png` in the session, one
   image with frames of the whole video and their times. Read it. Check that each action is in
   view, the pointer lands on its target, and the last frame shows the final state.

Re-rendering is cheap and never touches the recording: `iris render [options]` as often as needed.

## Declaring actions: `iris mark`

Declare an action immediately before you perform it. You do not need to hurry: the render moves
each declared click or typing mark to the moment the picture actually responds, and cuts the
waiting in between.

| What you are about to do | Command |
| --- | --- |
| Click a point | `iris mark --kind click --x X --y Y` |
| Click an element you know the box of | `iris mark --kind click --rect x,y,w,h` (clicks its centre) |
| Type into a field | `iris mark --kind type --rect x,y,w,h` (the field's box; the camera follows the text) |
| Show a result, a panel, a region | `iris mark --kind focus --rect x,y,w,h` (no pointer, zoom fits the region) |
| Show the whole window for a while | `iris mark --kind wide --hold 3` |

Options: `--zoom 2.0` sets the magnification, `--hold SECONDS` how long the camera stays,
`--caption TEXT` puts words under the picture while the camera is there, `--label TEXT` names
the mark in `iris plan`.

### Coordinates

Say what your numbers mean with `--space`:

- `--space screen` (default): screen points, origin at the top left of the main display. If you
  measured in a screenshot whose size differs from the display's point size (computer-use
  screenshots are usually scaled down), add `--ref WIDTHxHEIGHT` with the screenshot's size
  and pass the screenshot coordinates unchanged.
- `--space window`: points from the top left corner of the recorded window (or area). Add
  `--ref WIDTHxHEIGHT` when you measured in a screenshot or viewport of that window with a
  different size. For a page that fills its window (Electron, a kiosk browser), Playwright and
  DOM coordinates are window coordinates: `--space window --ref <innerWidth>x<innerHeight>`.
- `--space norm`: 0 to 1 across the recorded picture.

With no position at all, a mark uses where the real pointer is right now.

### With or without the real pointer

- You drive the real pointer (computer use, cliclick, CGEvent): iris sees the pointer, clicks,
  keys and scrolls by itself. It zooms on every click, turns the pointer's jumps into glides,
  and follows text you type when it appears out of view. Marks are optional; add `focus`
  marks where the result matters more than the click, and a `type` mark for a long field. A
  click you declare and then make with the real pointer counts once.
- You act without the pointer (Playwright, CDP, DOM, accessibility actions): marks are the only
  signal. iris draws its own pointer that glides from one declared click to the next and
  ignores the real mouse, so someone else can keep using the machine meanwhile.

`iris render --pointer declared|system` overrides the choice; `--focus visual` makes the camera
go by what changes in the picture, for a recording nobody declared anything in.

## Telling the viewer what happens

A silent video of an interface is hard to follow. Three commands say what the picture cannot;
like marks, they are declared at the moment they apply.

| To | Command |
| --- | --- |
| Say what an action is for | `iris mark --kind click --x X --y Y --caption "Open the settings"` |
| Say something about what is on screen | `iris caption "The build takes about a minute"` |
| Take the words away | `iris caption ""` (a caption also leaves by itself, and gives way to the next) |
| Show a keyboard shortcut | `iris keys cmd+shift+p`, then press it |
| Run through a slow stretch | `iris speed 8` ... `iris speed 1` |

- A caption stays as long as it takes to read; `--hold SECONDS` sets it yourself. Keep one to a
  short line, in the language of the viewer. A caption on a mark arrives with the camera, just
  before the action.
- iris never learns which keys were pressed, so a shortcut shows only when you declare it.
  Write the keys the way you pass them to your tool: `cmd+k`, `Meta+Shift+P`, `ctrl+alt+delete`,
  `shift+enter`, `esc`. Do not declare text you type, only shortcuts.
- `iris speed N` (0.25 to 32) plays the recording N times faster from that moment until
  `iris speed 1` or the end, and the video shows a badge meanwhile. Use it where the viewer
  should see that something takes time (an install, a long generation). A wait in which
  nothing moves needs nothing: it is cut. A wait nobody needs to see goes between `iris pause`
  and `iris resume`.

`iris render --no-captions`, `--no-keys` and `--no-speed` leave them out of a render;
`--caption-size 1.2` makes the lettering larger.

## Recording a script: `iris run`

When the whole demo is one command (a Playwright script, a test, a shell script), let iris
wrap it:

    iris run --app "Notes" --wait 15 --render --format both --out ~/Movies/demo -- node demo.mjs

iris starts the recording, runs the command, stops when it exits (also when it fails), and
with `--render` produces the video. Options before `--render` are those of `iris start`, the
ones after it those of `iris render`. The command finds the session directory in
`IRIS_SESSION`, so `iris mark`, `iris caption` and the rest called inside it reach this
recording. The exit status is the command's. The window has to be there before the command
runs: launch the application first (`--wait` covers one that is still opening), or record a
display.

## While recording

- Do not move or resize the recorded window. Keep it on one display and not minimized. It may
  sit behind other windows: a window target records only its own application.
- A window that is not on the desktop in view (another Space, or behind a full-screen
  application) is recorded by itself; the reply to `iris start` then has `"capture": "window"`
  and a `note`. Menus, popovers and dialogs that open as separate windows are missing from
  such a recording, and so is the real pointer: declare every action. An application may also
  stop drawing while out of view (Chromium and Electron do, see the example below).
- Long waits (a model generating, a build) are cut automatically when the picture stands still.
  When something keeps moving while you wait (a spinner, streaming text you do not need),
  wrap the wait in `iris pause` and `iris resume`.
- Let the final state stand for a second or two before `iris stop`.
- One recording at a time. `iris status` tells you whether one is running.

## Rendering options worth knowing

    iris render --format mp4|gif|both --out FILE --width 1920 --fps 60
                --background aurora|#101418|FILE|wallpaper --padding 0.06 --aspect 16:9
                --zoom 2.0 | --no-zoom     --cursor-size 1.5 | --no-cursor   --no-clicks
                --idle-max 1.5 | --keep-idle   --gif-width 800 --gif-fps 15
                --no-captions   --no-keys   --no-speed   --caption-size 1.0

- `iris plan` prints the zoom plan, the captions with their times, and which stretches of the
  recording are kept.
- `iris frames --at 3.5,8` saves full-size frames at those moments of the video.
- To add or correct a focus point afterwards: `iris mark --at SECONDS --kind focus --rect ...`
  (`--at` is recording time, as listed in `iris plan`), then render again. Marks live in
  `marks.jsonl` in the session directory, one JSON object per line.

## Example: a scripted browser or Electron window

    iris start --title "Notes" --name composer
    # box = await page.locator('#send').boundingBox(); vw x vh = the page's inner size
    iris mark --space window --ref 1280x800 --kind type --rect 320,690,640,44 --caption "Ask a question"
    #   ... type the text ...
    iris keys cmd+enter
    #   ... press the shortcut that sends it ...
    iris mark --space window --ref 1280x800 --kind focus --rect 300,120,700,420 --hold 4 --caption "The answer streams in"
    #   ... wait for the result ...
    iris stop --render --format both --out ~/Movies/composer
    iris sheet

## Example: an Electron application that must not take the keyboard

Somebody may be working on the machine. Start the application with a preload that shows its
window without activating it and keeps it drawing while it is out of view:

    // quiet.cjs, used as: electron -r ./quiet.cjs .
    const { BrowserWindow } = require('electron');
    const { showInactive } = BrowserWindow.prototype;
    BrowserWindow.prototype.show = function () {
      this.webContents.setBackgroundThrottling(false);
      showInactive.call(this);
    };
    BrowserWindow.prototype.focus = function () {};

`BrowserWindow.getAllWindows()[0].getMediaSourceId()` gives `window:ID:0`; that ID is what
`iris start --window-id` takes. Operate the page through Playwright or CDP and declare each
action with `--space window --ref <innerWidth>x<innerHeight>`.

## Being truthful

Record the real application doing the real thing. Do not stage a mock interface or a scripted
substitute and present it as a real run. Keep unrelated windows, credentials and private
content out of the picture; a window target already leaves other applications out. Do not
upload a recording anywhere unless you were asked to.

## When something fails

`iris doctor` says in one reply whether recording can work here: the screen recording
permission, accessibility, ffmpeg, and whether a recording is already running.

- "screen recording is not permitted": the application that launched you (the terminal, or the
  agent's desktop app) needs Screen & System Audio Recording permission in System Settings,
  then a restart. You cannot grant it yourself; tell the user.
- "a recording is already running": `iris stop` it first.
- "no window matches": run `iris windows` and use `--window-id`; for an application that is
  still starting, `iris start --wait 10`.
- A GIF needs `ffmpeg` on the PATH (`brew install ffmpeg`); MP4 does not.
- The video is black or never changes (`warning` from `iris stop`, or a `sheet.png` of
  identical frames): the window was minimized, or it is out of view and its application
  stopped drawing. Bring it into view or keep it drawing, and record again.
- Real clicks are missing from the video: they landed on another application's window lying
  over the recorded one. Bring the recorded window to the front before you click.
- The camera zooms on the wrong place: check `--space` and `--ref`; `iris plan` shows where
  each mark landed as `center` (0 to 1 across the picture).
