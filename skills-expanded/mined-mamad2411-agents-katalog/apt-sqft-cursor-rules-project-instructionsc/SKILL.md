---
description:
globs:
alwaysApply: true
---
# Apt SqFt app developer guide

## Goal
I am looking to build a web app that allows potential apartment renters or buyers to input some basic furniture items and some room dimensions, and have the app create a user-editable floor plan that can be used as a good approximation for scale. The user can then modify the layout with their mouse to get a close approximation to a floor plan found on a listing.

## Constraints

### Deriving accurate relative dimensions from only a few reference points

The app will have to be good at making assumptions about the overall scale based on only a little information. Normally these floor plans will have only the bedroom's rough dimensions for livable space, and does not take into account pillars and other anomalies outside of the basic length and width of the main floor area.

## Developer Approach

### data design

room: a collection of points. The point closest to absolute x0 and y0 is the represenative point. We use this if the room is being moved in space by the user.
points: an x and y coordinate. places where two Walls converge
walls: lines dynamically drawn between points

Every point has two walls, and every wall has two points.

#### shortest path principle

Between any two points, the shortest line is drawn to connect them.


### dev tooling

- React is my favorite javascript framework.
- eslint and typescript are a must.
- drag clicking is not well-supported in most graphing libraries. I don't want to over complicate it. I would like to try and solve this using HTML elements for thie MVP.

### Data structure

Use JSON

#### Room object:

user-editable
- name
- height
- width
- sq footage
- isLivable (boolean)

read-only
- x coordinate
- y coordinate
- isRelative (boolean)
- points[]
    - x coordinate
    - y coordinate

Notes
- We do not need to store the order of the points connected. We calculate how to connect points for a room by the "shortest path" princible
- the height and width are only used to calculate the initial sq footage and the first 4 points of a room. Once a point is created by the user (the 5th point), height and width are no longer editable and do not change.

#### furniture object:

Use identical structure as the room. All the features are the same, just the user label is different. Users can "scale"

#### undo/redo history of changes to the layout

allow this

### Features

### Auto-sizing rooms ("Absolute" and "Relative" rooms)

We only have a little information to start with, so my thinking is to let the user input the dimensions they have (such as the bedrooms or kitchen) and then let the user optionally input the relative size for the rest of the rooms.

#### Calculate a "relative" room
For example, the user inputs a room "8" "12" "kitchen" for an absolute room that renders a 8'x12' kitchen.

Then the user inputs "sq ft:1/5" (or "20%"), and "name:hallway" "relative to:'kitchen'" to render a 1.6'x2.4' hallway below the kitchen.

We can use these "relative" sizes as starting points for drawing out the space. Then, if the user changes the scale of the relative room visually by dragging a wall, we can update the user's input to reflect it's true size.

If a user changes the displayed stats of a relative room, it becomes an absolute room that no longer changes size relative to it's selected absolute room.

#### No Room dimension validation

The user is responsible for dealing with impossible room configurations. Minimum size of a room is whatever the grid determines.

### Drag and click editable rooms.

The app should support users dragging the walls of a room to change it's shape. If both height and width are given by the user, we must maintain this for the largest walls on each side. The room can have indented corners, short walls, etc. This will change the sq footage calculation. However the height and width inputs will continue to define the space between opposite primary walls (ignoring short walls),


#### What are the exact rules for maintaining primary dimensions when walls are modified?

The primary dimensions help with creating the first 4 points. It does not get computed ever. if the user add points to the room, it will no longer be editable.

#### How should we handle invalid user inputs?

Show a generic red-bordered input with a message below

### Layout Editor

- The layout editor is a 2d top-down view of a floorplan.
- Room length is set with `height` and room width is set with `width`.

#### Grid

There is a semi-transparent blue grid underneath the floorplan, which can be scaled by the user, with the default set to "1" (aka 1"x1") (`height: 1em; width: 1em`) per square. If the user inputs "2", it will instead be 2x2 inch for example.

This grid will also be used in calculations for mouse input to round the values of where the user has dragged their wall to the nearest grid unit. For example, if a user drags a wall 7" (`7em`) to the right but the grid is set to "6", the new width dimension will snap to the nearest value divisble by 6. (`6em`). You cannot disable the grid.

When the grid is changed, the points do not update. Only when the user edits a point, does the point's value snap to the grid.

#### computer mouse functions

- drag a left or right wall to change the width; drag a top or bottom wall to change the length.
- click on a point in the wall to create a draggable point that can add walls to the room without affecting it's primary length and width dimensions (a shortwall). For example, if the user clicks on the middle of a 12' wall and drags the point up 6' (`72em`), the layout editor will replace the old wall with two walls converging diagonally above, each with a length of 8.49' (`101.88em`) which is the hypotnuse of the right angle triangle created by the user's input.
- walls and points will always snap to the grid
- drag anywhere inside the room to move the room. This will transpose all coordinates of points in the room.

### Misc Features

- designed for laptop use primarily
- supports zoom in and out
- supports rotating the room in 15deg intervals
- Stats collapsible sidebar; Both absolute and relative room properties will be visible in a right-anchored sidebar.

### CSS

#### theme

Styling should be minimal, but built to handle dark / light themes.

#### editor

Livable rooms should have transparent backgrounds. Ulivable rooms (livable=false) display as opaque.

#### use "em" for everything
If we use "em" as the unit when defining length and width of the floor plan walls, then it should be easy to create "dependent" room sizes. For example, if we don't have the dimensions of a bathroom, the user can simply say "the bathroom looks like it takes about 1/4 of the living room". That way, we can easily maintain a 1:4 ratio between the bathroom sq ft and living room sq ft while still allowing the user to customize the walls of the bathroom without breaking the scale.

In CSS can assume "1rem" is equivalent to "1 inch". This makes it easy for users to convert their furniture dimensions (ft + inches) and room dimensions into a value our app will easily be able to work with.

#### using box-sizing: border-box for rooms

With `box-sizing: border-box`, a 200em x 100em



### Keep it simple stupid (KISS)

The code should favor simplicity over complexity. I want the MVP version with the option to expand using more complicated tools and libraries.

### Data Persistence

Save all app data in localStorage as a single JSON blob, with an easy "download data" button exposed to the user to copy the json blob. We can also have an "upload data" button that takes in a settings file previously downloaded.

## Feature ideas (not ready for implementation)

### Use total sq footage constraint
 Other times, we may have the total square footage; when we have this, we should build our logic around the rules for calculating square footage in NYC listings. For example, common spaces in an apartment building may be divided up by the number of units and added to each unit's total sq ft calculation. This is a bonus feature however, so we can safely ignore it for now.

### Hotkeys toolbar

At the top below the app header, show Hotkeys toolbar that prominently displays the hotkeys available within the app as a button with an icon that represents the tool. You can also click on these buttons to select a tool instead of using the hotkey displayed.

Hotkeys

- holding down "s" toggles scale mode. When the user drags up within a room, the coordinates for every point in the room update accordingly. The smallest increment is based on the grid size.
