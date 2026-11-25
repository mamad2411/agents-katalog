---
name: p5js-creative-coding
description: Create interactive graphics, animations, and creative coding projects using p5.js. Use this skill when building 2D/3D visualizations, generative art, interactive sketches, animations, games, data visualizations, or any creative coding project that involves drawing shapes, handling user input, working with images, or creating real-time graphics in the browser. Also triggers on "p5", "p5.js", "Processing", "canvas sketch", "particle system", "noise field", "perlin noise", "generative pattern", "draw with JavaScript", "make it move on the canvas", "interactive art", "visual sketch", "pixel manipulation", "audio-reactive visuals", or any request to build something visual and creative that runs in the browser without a specific framework requirement.
---

# p5.js Creative Coding

p5.js is a JavaScript library for creative coding, making it easy to create interactive graphics, animations, and multimedia experiences in the browser. It's based on Processing and designed for artists, designers, educators, and beginners.

**Documentation**: https://p5js.org/reference/
**Online Editor**: https://editor.p5js.org/
**Examples**: https://p5js.org/examples/

## When to Use This Skill

- Creating generative art and visualizations
- Building interactive animations
- Making simple games
- Data visualization
- Interactive installations
- Educational demonstrations
- Prototyping visual ideas
- Working with images and pixels
- Creating audio-reactive visuals
- Building creative web experiences

## Project Setup

### Using CDN (Simplest)

```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.jsdelivr.net/npm/p5@1.11.0/lib/p5.min.js"></script>
</head>
<body>
  <script src="sketch.js"></script>
</body>
</html>
```

### Using npm

```bash
npm install p5
```

```javascript
import p5 from 'p5';

new p5((p) => {
  p.setup = () => {
    p.createCanvas(400, 400);
  };
  
  p.draw = () => {
    p.background(220);
    p.ellipse(p.mouseX, p.mouseY, 50, 50);
  };
});
```

## Core Structure

### Basic Sketch

```javascript
function setup() {
  // Runs once at the start
  createCanvas(400, 400);
}

function draw() {
  // Runs continuously (default 60fps)
  background(220);
  ellipse(mouseX, mouseY, 50, 50);
}
```

### Lifecycle Functions

```javascript
function preload() {
  // Load assets before setup runs
  img = loadImage('image.png');
  font = loadFont('font.ttf');
  data = loadJSON('data.json');
}

function setup() {
  // Initialize canvas and variables
  createCanvas(800, 600);
  frameRate(60);
}

function draw() {
  // Main animation loop
}
```

### Controlling the Loop

```javascript
noLoop();      // Stop draw() from looping
loop();        // Resume looping
redraw();      // Execute draw() once
isLooping();   // Check if looping

// In draw()
if (frameCount > 100) {
  noLoop();    // Stop after 100 frames
}
```

## Canvas & Environment

### Canvas Setup

```javascript
// 2D canvas (default)
createCanvas(800, 600);

// 3D canvas (WebGL)
createCanvas(800, 600, WEBGL);

// Resize canvas
resizeCanvas(windowWidth, windowHeight);

// Fullscreen canvas
function setup() {
  createCanvas(windowWidth, windowHeight);
}

function windowResized() {
  resizeCanvas(windowWidth, windowHeight);
}
```

### Environment Variables

```javascript
width           // Canvas width
height          // Canvas height
windowWidth     // Browser window width
windowHeight    // Browser window height
displayWidth    // Screen width
displayHeight   // Screen height
frameCount      // Frames since start
frameRate()     // Get/set frame rate
deltaTime       // Time since last frame (ms)
focused         // Whether window is focused
```

## Drawing Shapes

### 2D Primitives

```javascript
// Basic shapes
point(x, y);
line(x1, y1, x2, y2);
rect(x, y, width, height);
rect(x, y, width, height, radius);  // Rounded corners
square(x, y, size);
ellipse(x, y, width, height);
circle(x, y, diameter);
triangle(x1, y1, x2, y2, x3, y3);
quad(x1, y1, x2, y2, x3, y3, x4, y4);
arc(x, y, w, h, start, stop, mode);

// Arc modes: OPEN, CHORD, PIE
arc(200, 200, 100, 100, 0, HALF_PI, PIE);
```

### Shape Modes

```javascript
// Rectangle mode (default: CORNER)
rectMode(CORNER);   // x,y is top-left corner
rectMode(CORNERS);  // x,y and w,h are opposite corners
rectMode(CENTER);   // x,y is center
rectMode(RADIUS);   // w,h are half-widths from center

// Ellipse mode (default: CENTER)
ellipseMode(CENTER);
ellipseMode(RADIUS);
ellipseMode(CORNER);
ellipseMode(CORNERS);
```

### Custom Shapes with Vertices

```javascript
// Simple polygon
beginShape();
vertex(30, 20);
vertex(85, 20);
vertex(85, 75);
vertex(30, 75);
endShape(CLOSE);

// Shape with curves
beginShape();
curveVertex(84, 91);
curveVertex(84, 91);
curveVertex(68, 19);
curveVertex(21, 17);
curveVertex(32, 91);
curveVertex(32, 91);
endShape();

// Bezier vertices
beginShape();
vertex(30, 20);
bezierVertex(80, 0, 80, 75, 30, 75);
endShape();

// Shape with hole (contour)
beginShape();
vertex(0, 0);
vertex(100, 0);
vertex(100, 100);
vertex(0, 100);
beginContour();
vertex(25, 25);
vertex(25, 75);
vertex(75, 75);
vertex(75, 25);
endContour();
endShape(CLOSE);
```

### Curves

```javascript
// Bezier curve
bezier(x1, y1, cx1, cy1, cx2, cy2, x2, y2);

// Catmull-Rom spline
curve(x1, y1, x2, y2, x3, y3, x4, y4);

// Adjust curve tightness (-5 to 5, default 0)
curveTightness(0);
```

## Color

### Setting Colors

```javascript
// Grayscale (0-255)
background(220);
fill(100);
stroke(0);

// RGB (0-255 each)
background(255, 0, 0);      // Red
fill(0, 255, 0);            // Green
stroke(0, 0, 255);          // Blue

// RGBA (with alpha)
fill(255, 0, 0, 128);       // Semi-transparent red

// Hex colors
fill('#ff0000');
fill('#f00');

// HSB mode
colorMode(HSB, 360, 100, 100);
fill(0, 100, 100);          // Red in HSB

// HSL mode
colorMode(HSL, 360, 100, 100);
fill(0, 100, 50);           // Red in HSL

// Named color object
let c = color(255, 0, 0);
fill(c);
```

### Stroke and Fill

```javascript
stroke(0);           // Set stroke color
strokeWeight(4);     // Set stroke width
noStroke();          // Disable stroke

fill(255, 0, 0);     // Set fill color
noFill();            // Disable fill

// Stroke caps and joins
strokeCap(ROUND);    // ROUND, SQUARE, PROJECT
strokeJoin(MITER);   // MITER, BEVEL, ROUND
```

### Color Functions

```javascript
let c = color(255, 100, 50);

// Extract components
red(c);              // 255
green(c);            // 100
blue(c);             // 50
alpha(c);            // 255 (default)
hue(c);              // Hue value
saturation(c);       // Saturation value
brightness(c);       // Brightness value

// Interpolate colors
let c1 = color(255, 0, 0);
let c2 = color(0, 0, 255);
let mixed = lerpColor(c1, c2, 0.5);  // Purple
```

## Transformations

### Basic Transforms

```javascript
translate(x, y);     // Move origin
rotate(angle);       // Rotate (radians by default)
scale(s);            // Uniform scale
scale(sx, sy);       // Non-uniform scale
shearX(angle);       // Shear along X
shearY(angle);       // Shear along Y
```

### Transform Stack

```javascript
function draw() {
  background(220);
  
  // Save current transform state
  push();
  translate(width/2, height/2);
  rotate(frameCount * 0.01);
  rect(-25, -25, 50, 50);
  pop();  // Restore previous state
  
  // This rect is unaffected by transforms above
  rect(10, 10, 30, 30);
}
```

### Angle Modes

```javascript
angleMode(RADIANS);  // Default
angleMode(DEGREES);  // Use degrees instead

// Constants
PI           // 3.14159...
TWO_PI       // 6.28318...
HALF_PI      // 1.57079...
QUARTER_PI   // 0.78539...
TAU          // Same as TWO_PI
```

## Typography

### Text Basics

```javascript
// Display text
text('Hello World', x, y);
text('Multi-line\ntext', x, y);
text('Bounded text', x, y, width, height);

// Text properties
textSize(32);
textFont('Georgia');
textAlign(CENTER, CENTER);  // Horizontal, Vertical
textLeading(36);            // Line height
textStyle(BOLD);            // NORMAL, ITALIC, BOLD, BOLDITALIC
```

### Custom Fonts

```javascript
let myFont;

function preload() {
  myFont = loadFont('assets/font.ttf');
}

function setup() {
  createCanvas(400, 400);
  textFont(myFont);
  textSize(48);
}

function draw() {
  background(220);
  text('Custom Font', 50, 200);
}
```

### Text Measurements

```javascript
let w = textWidth('Hello');     // Width of text
let a = textAscent();           // Height above baseline
let d = textDescent();          // Height below baseline
```

## Images

### Loading and Displaying

```javascript
let img;

function preload() {
  img = loadImage('photo.jpg');
}

function setup() {
  createCanvas(400, 400);
}

function draw() {
  background(220);
  image(img, 0, 0);                    // Original size
  image(img, 0, 0, 100, 100);          // Scaled
  image(img, 0, 0, 100, 100, 50, 50, 200, 200);  // Crop
}

// Image mode (like rectMode)
imageMode(CORNER);   // Default
imageMode(CENTER);
imageMode(CORNERS);
```

### Image Manipulation

```javascript
// Tint (colorize)
tint(255, 0, 0);        // Red tint
tint(255, 128);         // 50% opacity
noTint();               // Remove tint

// Filters
filter(THRESHOLD, 0.5);
filter(GRAY);
filter(INVERT);
filter(POSTERIZE, 4);
filter(BLUR, 3);
filter(ERODE);
filter(DILATE);
```

### Pixel Manipulation

```javascript
// Access pixels
loadPixels();
for (let i = 0; i < pixels.length; i += 4) {
  pixels[i] = 255;      // Red
  pixels[i+1] = 0;      // Green
  pixels[i+2] = 0;      // Blue
  pixels[i+3] = 255;    // Alpha
}
updatePixels();

// Get/set single pixel
let c = get(x, y);      // Get color at pixel
set(x, y, color(255, 0, 0));  // Set pixel color

// Copy region
copy(srcX, srcY, srcW, srcH, dstX, dstY, dstW, dstH);
```

### Creating Images

```javascript
let img = createImage(100, 100);
img.loadPixels();
for (let x = 0; x < img.width; x++) {
  for (let y = 0; y < img.height; y++) {
    let index = (x + y * img.width) * 4;
    img.pixels[index] = x * 2.5;      // R
    img.pixels[index + 1] = y * 2.5;  // G
    img.pixels[index + 2] = 128;      // B
    img.pixels[index + 3] = 255;      // A
  }
}
img.updatePixels();
image(img, 0, 0);
```

## Mouse Input

### Mouse Variables

```javascript
mouseX          // Current X position
mouseY          // Current Y position
pmouseX         // Previous frame X position
pmouseY         // Previous frame Y position
mouseIsPressed  // Boolean: is mouse pressed?
mouseButton     // LEFT, RIGHT, or CENTER
movedX          // Horizontal movement since last frame
movedY          // Vertical movement since last frame
```

### Mouse Events

```javascript
function mousePressed() {
  // Called once when mouse button pressed
  console.log('Pressed at', mouseX, mouseY);
}

function mouseReleased() {
  // Called once when mouse button released
}

function mouseClicked() {
  // Called after press and release
}

function doubleClicked() {
  // Called on double click
}

function mouseMoved() {
  // Called when mouse moves (button not pressed)
}

function mouseDragged() {
  // Called when mouse moves while pressed
}

function mouseWheel(event) {
  // event.delta: scroll amount
  console.log(event.delta);
  return false;  // Prevent page scroll
}
```

## Keyboard Input

### Keyboard Variables

```javascript
keyIsPressed    // Boolean: is any key pressed?
key             // Most recent key as string
keyCode         // Numeric code of key
```

### Keyboard Events

```javascript
function keyPressed() {
  // Called once when key pressed
  if (key === 'a') {
    console.log('A pressed');
  }
  if (keyCode === ENTER) {
    console.log('Enter pressed');
  }
  return false;  // Prevent default browser behavior
}

function keyReleased() {
  // Called once when key released
}

function keyTyped() {
  // Called for printable keys only
}

// Check if specific key is down
function draw() {
  if (keyIsDown(LEFT_ARROW)) {
    x -= 5;
  }
  if (keyIsDown(RIGHT_ARROW)) {
    x += 5;
  }
}
```

### Key Codes

```javascript
// Arrow keys
UP_ARROW, DOWN_ARROW, LEFT_ARROW, RIGHT_ARROW

// Special keys
BACKSPACE, DELETE, ENTER, RETURN, TAB, ESCAPE
SHIFT, CONTROL, OPTION, ALT

// Check specific key
if (keyCode === 32) {  // Space bar
  // ...
}
```

## Math & Random

### Math Functions

```javascript
// Basic math
abs(n)              // Absolute value
ceil(n)             // Round up
floor(n)            // Round down
round(n)            // Round to nearest
sqrt(n)             // Square root
pow(base, exp)      // Power
exp(n)              // e^n
log(n)              // Natural log

// Constraints
constrain(n, low, high)  // Clamp value
min(a, b, c...)          // Minimum
max(a, b, c...)          // Maximum

// Mapping
map(value, start1, stop1, start2, stop2)
// Example: map(mouseX, 0, width, 0, 255)

lerp(start, stop, amt)   // Linear interpolation
norm(value, start, stop) // Normalize to 0-1
```

### Trigonometry

```javascript
sin(angle)
cos(angle)
tan(angle)
asin(value)
acos(value)
atan(value)
atan2(y, x)          // Angle from origin to point

degrees(radians)     // Convert to degrees
radians(degrees)     // Convert to radians
```

### Random

```javascript
random()             // 0 to 1
random(max)          // 0 to max
random(min, max)     // min to max
random(array)        // Random element from array

randomSeed(seed)     // Set random seed for reproducibility

randomGaussian()     // Gaussian distribution (mean 0, sd 1)
randomGaussian(mean, sd)
```

### Noise (Perlin)

```javascript
// 1D, 2D, or 3D noise (returns 0-1)
noise(x)
noise(x, y)
noise(x, y, z)

// Configure noise
noiseSeed(seed)
noiseDetail(octaves, falloff)

// Example: smooth animation
function draw() {
  let x = noise(frameCount * 0.01) * width;
  let y = noise(frameCount * 0.01 + 1000) * height;
  ellipse(x, y, 50);
}
```

### Vectors

```javascript
// Create vector
let v = createVector(x, y);
let v3d = createVector(x, y, z);

// Vector operations
v.add(v2)            // Add vectors
v.sub(v2)            // Subtract
v.mult(scalar)       // Multiply by scalar
v.div(scalar)        // Divide by scalar
v.mag()              // Magnitude (length)
v.magSq()            // Magnitude squared
v.normalize()        // Make unit length
v.limit(max)         // Limit magnitude
v.setMag(len)        // Set magnitude
v.heading()          // Angle of 2D vector
v.rotate(angle)      // Rotate 2D vector
v.lerp(v2, amt)      // Interpolate
v.dist(v2)           // Distance to another vector
v.dot(v2)            // Dot product
v.cross(v2)          // Cross product (3D)
v.copy()             // Create copy

// Static methods
p5.Vector.add(v1, v2)
p5.Vector.random2D()
p5.Vector.random3D()
p5.Vector.fromAngle(angle)
```

## 3D Graphics (WebGL)

### Basic 3D Setup

```javascript
function setup() {
  createCanvas(800, 600, WEBGL);
}

function draw() {
  background(200);
  
  // Camera control with mouse
  orbitControl();
  
  // Lighting
  ambientLight(100);
  directionalLight(255, 255, 255, 0, -1, -1);
  
  // Draw 3D shape
  rotateX(frameCount * 0.01);
  rotateY(frameCount * 0.01);
  box(100);
}
```

### 3D Primitives

```javascript
box(size)
box(width, height, depth)
sphere(radius)
sphere(radius, detailX, detailY)
cylinder(radius, height)
cone(radius, height)
torus(radius, tubeRadius)
plane(width, height)
ellipsoid(radiusX, radiusY, radiusZ)
```

### Materials and Lighting

```javascript
// Lights
ambientLight(r, g, b)
directionalLight(r, g, b, x, y, z)
pointLight(r, g, b, x, y, z)
spotLight(r, g, b, x, y, z, dirX, dirY, dirZ, angle, concentration)

// Materials
ambientMaterial(r, g, b)      // Responds to ambient light
emissiveMaterial(r, g, b)     // Self-illuminating
specularMaterial(r, g, b)     // Shiny highlights
normalMaterial()              // Debug: shows normals as colors

// Shininess (for specular)
shininess(shine)              // 1-100+
metalness(amount)             // 0-1
```

### 3D Textures

```javascript
let img;

function preload() {
  img = loadImage('texture.jpg');
}

function draw() {
  background(200);
  texture(img);
  box(100);
}
```

### Camera

```javascript
// Perspective camera (default)
perspective(fov, aspect, near, far);

// Orthographic camera
ortho(left, right, bottom, top, near, far);

// Position camera
camera(eyeX, eyeY, eyeZ, centerX, centerY, centerZ, upX, upY, upZ);

// Create and use camera object
let cam = createCamera();
cam.setPosition(0, 0, 500);
cam.lookAt(0, 0, 0);
setCamera(cam);
```

### Custom Shaders

```javascript
let myShader;

function preload() {
  myShader = loadShader('shader.vert', 'shader.frag');
}

function setup() {
  createCanvas(800, 600, WEBGL);
}

function draw() {
  shader(myShader);
  myShader.setUniform('uTime', millis() / 1000.0);
  myShader.setUniform('uResolution', [width, height]);
  rect(0, 0, width, height);
}
```

## DOM Elements

### Creating Elements

```javascript
// Buttons
let button = createButton('Click me');
button.position(10, 10);
button.mousePressed(() => {
  console.log('Clicked!');
});

// Sliders
let slider = createSlider(0, 255, 100);
slider.position(10, 50);
// Use in draw: slider.value()

// Input fields
let input = createInput('default text');
input.position(10, 90);
input.input(() => console.log(input.value()));

// Dropdown
let sel = createSelect();
sel.option('Option 1');
sel.option('Option 2');
sel.changed(() => console.log(sel.value()));

// Checkbox
let checkbox = createCheckbox('Enable', true);
checkbox.changed(() => console.log(checkbox.checked()));

// Color picker
let colorPicker = createColorPicker('#ff0000');
// Use: fill(colorPicker.color())
```

### Styling Elements

```javascript
let button = createButton('Styled');
button.position(10, 10);
button.size(100, 40);
button.style('background-color', '#ff0000');
button.style('color', 'white');
button.style('font-size', '16px');
button.addClass('my-class');
```

## Saving Output

```javascript
// Save canvas as image
saveCanvas('mySketch', 'png');
saveCanvas('mySketch', 'jpg');

// Save GIF
saveGif('myAnimation', 5);  // 5 seconds

// Save frames
saveFrames('frame', 'png', 2, 25);  // 2 seconds at 25fps

// Save data
save(myData, 'data.json');
saveJSON(myObject, 'data.json');
saveStrings(myArray, 'data.txt');
```

## Instance Mode

For multiple sketches or better scoping:

```javascript
const sketch1 = (p) => {
  p.setup = () => {
    p.createCanvas(400, 400);
  };
  
  p.draw = () => {
    p.background(255, 0, 0);
    p.ellipse(p.mouseX, p.mouseY, 50);
  };
};

const sketch2 = (p) => {
  p.setup = () => {
    p.createCanvas(400, 400);
  };
  
  p.draw = () => {
    p.background(0, 0, 255);
    p.rect(p.mouseX, p.mouseY, 50, 50);
  };
};

new p5(sketch1, 'container1');
new p5(sketch2, 'container2');
```

## Complete Examples

### Animated Circles

```javascript
let circles = [];

function setup() {
  createCanvas(800, 600);
  for (let i = 0; i < 50; i++) {
    circles.push({
      x: random(width),
      y: random(height),
      r: random(10, 50),
      vx: random(-2, 2),
      vy: random(-2, 2),
      col: color(random(255), random(255), random(255), 150)
    });
  }
}

function draw() {
  background(20);
  
  for (let c of circles) {
    // Move
    c.x += c.vx;
    c.y += c.vy;
    
    // Bounce
    if (c.x < 0 || c.x > width) c.vx *= -1;
    if (c.y < 0 || c.y > height) c.vy *= -1;
    
    // Draw
    noStroke();
    fill(c.col);
    ellipse(c.x, c.y, c.r * 2);
  }
}
```

### Perlin Noise Flow Field

```javascript
let particles = [];
let flowField;
let cols, rows;
let scale = 20;

function setup() {
  createCanvas(800, 600);
  cols = floor(width / scale);
  rows = floor(height / scale);
  flowField = new Array(cols * rows);
  
  for (let i = 0; i < 1000; i++) {
    particles.push(createVector(random(width), random(height)));
  }
  background(0);
}

function draw() {
  // Generate flow field
  let yoff = 0;
  for (let y = 0; y < rows; y++) {
    let xoff = 0;
    for (let x = 0; x < cols; x++) {
      let angle = noise(xoff, yoff, frameCount * 0.005) * TWO_PI * 2;
      let v = p5.Vector.fromAngle(angle);
      flowField[x + y * cols] = v;
      xoff += 0.1;
    }
    yoff += 0.1;
  }
  
  // Update and draw particles
  for (let p of particles) {
    let x = floor(p.x / scale);
    let y = floor(p.y / scale);
    let index = constrain(x + y * cols, 0, flowField.length - 1);
    let force = flowField[index];
    
    p.add(force);
    
    // Wrap around edges
    if (p.x > width) p.x = 0;
    if (p.x < 0) p.x = width;
    if (p.y > height) p.y = 0;
    if (p.y < 0) p.y = height;
    
    stroke(255, 5);
    point(p.x, p.y);
  }
}
```

### Interactive Drawing Tool

```javascript
let brushSize = 20;
let brushColor;

function setup() {
  createCanvas(800, 600);
  background(255);
  brushColor = color(0);
  
  // UI
  let sizeSlider = createSlider(5, 100, 20);
  sizeSlider.position(10, height + 10);
  sizeSlider.input(() => brushSize = sizeSlider.value());
  
  let colorPicker = createColorPicker('#000000');
  colorPicker.position(150, height + 10);
  colorPicker.input(() => brushColor = colorPicker.color());
  
  let clearBtn = createButton('Clear');
  clearBtn.position(250, height + 10);
  clearBtn.mousePressed(() => background(255));
}

function draw() {
  if (mouseIsPressed && mouseY < height) {
    noStroke();
    fill(brushColor);
    ellipse(mouseX, mouseY, brushSize);
    
    // Smooth line between points
    stroke(brushColor);
    strokeWeight(brushSize);
    line(pmouseX, pmouseY, mouseX, mouseY);
  }
}
```

## Quick Reference

### Lifecycle Functions

| Function | When Called |
|----------|-------------|
| `preload()` | Before setup, for loading assets |
| `setup()` | Once at start |
| `draw()` | Continuously (60fps default) |
| `windowResized()` | When window size changes |

### Common Functions

| Function | Description |
|----------|-------------|
| `createCanvas(w, h)` | Create drawing canvas |
| `background(c)` | Clear and fill background |
| `fill(c)` | Set fill color |
| `stroke(c)` | Set stroke color |
| `noFill()` / `noStroke()` | Disable fill/stroke |
| `push()` / `pop()` | Save/restore drawing state |
| `translate(x, y)` | Move origin |
| `rotate(angle)` | Rotate coordinate system |
| `scale(s)` | Scale coordinate system |

### Shape Functions

| Function | Description |
|----------|-------------|
| `point(x, y)` | Draw point |
| `line(x1, y1, x2, y2)` | Draw line |
| `rect(x, y, w, h)` | Draw rectangle |
| `ellipse(x, y, w, h)` | Draw ellipse |
| `circle(x, y, d)` | Draw circle |
| `triangle(...)` | Draw triangle |
| `beginShape()` / `endShape()` | Custom shapes |
| `vertex(x, y)` | Add vertex to shape |

### Input Variables

| Variable | Description |
|----------|-------------|
| `mouseX`, `mouseY` | Mouse position |
| `pmouseX`, `pmouseY` | Previous mouse position |
| `mouseIsPressed` | Is mouse button down? |
| `keyIsPressed` | Is any key down? |
| `key` | Last key pressed (string) |
| `keyCode` | Last key code (number) |

### Constants

| Constant | Value |
|----------|-------|
| `PI` | 3.14159... |
| `TWO_PI` | 6.28318... |
| `HALF_PI` | 1.57079... |
| `DEGREES` / `RADIANS` | Angle modes |
| `CENTER`, `CORNER`, `CORNERS`, `RADIUS` | Draw modes |
| `CLOSE` | For endShape() |


## Related Skills

### trigonometry
Covers radians, sin/cos/atan2, circular motion, oscillation, spirals, polar coordinates, and spherical geometry. Essential companion for any p5 sketch that moves things in arcs, pulses, orbits, or waves - which is most generative art.

**Use alongside this skill when:** your sketch involves  oscillations, objects orbiting a centre, rotating shapes, or anything moving along a circular or wave-based path.

### geometry
Euclidean primitives, vectors, raycasting, AABB/sphere collision, closest-point queries, normals, and frustum culling. Useful when a p5 sketch grows into an interactive simulation with hit detection or spatial lookups.

**Use alongside this skill when:** you're building a p5 game that needs collision detection, checking whether the mouse is inside a custom shape, or doing ray-vs-object intersection.

### physics
Numerical integration, force accumulation, spring systems, rigid bodies, soft bodies (PBD), and SPH fluids - all framed as code-ready simulation loops. p5's `draw()` loop is a natural home for time-stepped simulations.

**Use alongside this skill when:** the sketch simulates gravity, spring forces, cloth, fluid, or any physically-based particle system rather than just decorative motion.

### art-theory
Translates art movements (Pointillism, Constructivism, Op Art, Abstract Expressionism, Glitch Art, etc.) into language-agnostic algorithmic pseudocode that can be dropped straight into p5.

**Use alongside this skill when:** the user wants to recreate or be inspired by a specific art movement or aesthetic, and needs the underlying algorithm described before writing the p5 code.

### game-math
Vectors, matrices, coordinate systems, quaternion rotation, camera projection, and kinematics - the full math toolkit for 2D/3D interactive applications.

**Use alongside this skill when:** the sketch uses p5's WEBGL mode, needs a camera rig, requires matrix transforms beyond `rotate()`/`translate()`, or is growing into a mini game-engine.

### animation-specialist
Broad motion design: easing curves, spring dynamics, CSS animations, canvas animation, SVG morphing, GSAP timelines, and the theory behind choreography.

**Use instead of this skill when:** the user wants animated visuals on a web page but hasn't committed to p5 and might be better served by CSS transitions, the Web Animations API, or a canvas library with a smaller footprint. Use alongside when the p5 sketch has complex sequenced animations that would benefit from easing and timeline thinking.

### web-visual-effects
GPU-accelerated effects via WebGL/WebGPU shaders, post-processing, and particle systems that push beyond what the 2D Canvas API can achieve.

**Use instead of this skill when:** the visual effect requires custom GLSL/WGSL shaders, compute passes, or a level of GPU control that p5's abstraction layer does not expose. p5's WEBGL mode covers basic 3D; raw WebGL/WebGPU covers everything beyond that.

### frontend-design
Creative direction and polished interface implementation - typography, colour, layout, and component design as a unified whole.

**Use before this skill when:** the p5 sketch needs to live inside a well-designed web page and the overall layout, colour palette, and UI haven't been established yet.
