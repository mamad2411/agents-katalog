---
name: pine-optimizer
description: Optimizes Pine Script for performance and user experience. Use when improving speed, UI organization, or visual appeal.
allowed-tools: Read, Edit, Grep, Glob
---

# Pine Script Optimizer

Specialized in enhancing script performance, user experience, and visual presentation on TradingView.

## Pine Script v6 2025 Optimization Features

### July 2025: Input `active` Parameter - UX Game Changer

Create conditional input visibility for cleaner UI:

```pinescript
// ✅ BEFORE: All inputs always visible (cluttered)
maType = input.string("EMA", "MA Type", options=["SMA", "EMA", "Custom"])
customLength = input.int(20, "Custom Length")  // Always visible

// ✅ AFTER: Conditional visibility (clean UX)
maType = input.string("EMA", "MA Type", options=["SMA", "EMA", "Custom"])
customLength = input.int(20, "Custom Length",
    active=(maType == "Custom"),  // Only shown when Custom selected
    tooltip="Only available when MA Type is 'Custom'")

// Advanced mode pattern
showAdvanced = input.bool(false, "Show Advanced Settings", group="Settings")
advSetting1 = input.int(10, "Advanced 1", group="Advanced", active=showAdvanced)
advSetting2 = input.float(1.5, "Advanced 2", group="Advanced", active=showAdvanced)
advSetting3 = input.bool(true, "Advanced 3", group="Advanced", active=showAdvanced)
```

### September 2025: Plot Line Styles

More visual options without custom drawing:

```pinescript
// Use built-in line styles for cleaner visuals
plot(sma20, "SMA 20", color.blue, linestyle=plot.linestyle_solid)
plot(sma50, "SMA 50", color.red, linestyle=plot.linestyle_dashed)
plot(support, "Support", color.green, linestyle=plot.linestyle_dotted)

// Combine with conditional display
showProjections = input.bool(true, "Show Projections")
plot(showProjections ? projection : na, "Projection",
    color.new(color.yellow, 50),
    linestyle=plot.linestyle_dotted)
```

### February 2025: Unlimited Scopes

No longer limited to 550 scopes - enables more complex, modular code:

```pinescript
// Now possible: deeply nested logic without scope errors
type ComplexType
    float value1
    float value2
    array<float> history

method process(ComplexType this) =>
    if this.value1 > 0
        if this.value2 > 0
            for i = 0 to array.size(this.history) - 1
                if array.get(this.history, i) > 0
                    // Deep nesting now allowed
                    // Previously would hit 550 scope limit
```

### March 2025: Use `for...in` for Collections

The preferred and safest way to iterate over collections:

```pinescript
// ✅ BEST: Use for...in for arrays (safest, cleanest)
for element in myArray
    // Process element directly - no boundary issues

// ✅ BEST: Use for...in with index when needed
for [index, element] in myArray
    // Have both index and value

// ✅ Works with matrices (iterates rows as arrays)
for row in myMatrix
    for value in row
        // Process each value

// ✅ Works with maps (key-value pairs in insertion order)
for [key, value] in myMap
    // Process key-value pair
```

**FALLBACK: Cache boundary if traditional `for` is required:**
```pinescript
// ❌ SLOW/DANGEROUS: Re-evaluates array.size() every iteration
for i = 0 to array.size(arr) - 1
    // Can cause infinite loop if array modified

// ✅ FALLBACK: Cache boundary if you need traditional for
arrSize = array.size(arr)
for i = 0 to arrSize - 1
    // process
```

### August 2025: Longer Strings (40,960 chars)

Build more comprehensive info panels:

```pinescript
// Now possible: detailed multi-section reports
report = "═══════════════════════════════\n"
report += "      STRATEGY REPORT         \n"
report += "═══════════════════════════════\n\n"
report += "PERFORMANCE METRICS\n"
report += "───────────────────\n"
report += "Win Rate: " + str.tostring(winRate, "#.##") + "%\n"
report += "Profit Factor: " + str.tostring(pf, "#.##") + "\n"
// ... can now include much more detail
```

## ⚠️ CRITICAL: UDT-First Code Organization

**The single biggest optimization you can make is using UDT-first architecture.** This eliminates parallel arrays, simplifies drawing management, and removes bar_index clamping code.

### Before vs After: Parallel Arrays vs UDT

```pinescript
// ❌ BEFORE: 6+ parallel arrays (hard to maintain, error-prone)
var array<float> slopes = array.new<float>()
var array<float> intercepts = array.new<float>()
var array<float> stdDevs = array.new<float>()
var array<int> startBars = array.new<int>()
var array<int> endBars = array.new<int>()
var array<line> centerLines = array.new<line>()
// Must keep ALL arrays in sync - easy to have bugs!

// Push to ALL arrays when adding item
array.push(slopes, newSlope)
array.push(intercepts, newIntercept)
array.push(stdDevs, newStdDev)
array.push(startBars, newStartBar)
array.push(endBars, newEndBar)
// Forgot to push to centerLines? Bug!

// ✅ AFTER: Single UDT array (clean, self-documenting)
type Regression
    float slope
    float intercept
    float stdDev
    int startTime      // Use TIME, not bar_index!
    int endTime
    int startBarIndex  // Keep for Y calculations
    int endBarIndex
    line centerLine = na

var array<Regression> regressions = array.new<Regression>()

// One push, all data together
newReg = Regression.new(slope=newSlope, intercept=newIntercept, ...)
array.push(regressions, newReg)
```

### Performance Gain: xloc.bar_time Eliminates Clamping

```pinescript
// ❌ BEFORE: Clamping code everywhere (slow, complex)
leftBar = math.max(0, bar_index - startOffset)  // Clamp to valid range
if bar_index - startBar > 5000
    leftBar := bar_index - 5000  // Historical buffer limit!
line.set_x1(myLine, leftBar)

// ✅ AFTER: xloc.bar_time has NO limit - just draw!
line.new(startTime, y1, endTime, y2, xloc=xloc.bar_time)
// No clamping needed! Works for ANY historical bar!
```

### UDT Methods for DRY Drawing Code

```pinescript
// ❌ BEFORE: Repeated drawing blocks (~50+ lines each)
// Block for original regression drawing
if showOriginal
    if not na(origCenterLine)
        line.delete(origCenterLine)
    origCenterLine := line.new(...)
    // ... 20 more lines

// Block for live regression drawing (duplicate code!)
if showLive
    if not na(liveCenterLine)
        line.delete(liveCenterLine)
    liveCenterLine := line.new(...)
    // ... 20 more duplicate lines

// ✅ AFTER: Single method, reuse everywhere (~30 lines total)
method draw(Regression this, color baseColor, int width) =>
    this.delete()  // Clean up old
    startY = this.calculateY(this.startBarIndex)
    endY = this.calculateY(this.endBarIndex)
    this.centerLine := line.new(this.startTime, startY, this.endTime, endY,
         xloc=xloc.bar_time, color=baseColor, width=width)

// Use anywhere - no duplication!
originalRegression.draw(origColor, 2)
liveRegression.draw(liveColor, 2)
for reg in chainedRegressions
    reg.draw(chainedColor, 1)
```

### UDT Optimization Metrics

| Metric | Parallel Arrays | UDT Architecture |
|--------|-----------------|------------------|
| Array declarations | 6-10 | 1 |
| Drawing code blocks | 5+ (duplicated) | 1 method |
| Clamping code | 4+ locations | 0 |
| Lines of code | 400+ | ~150 |
| Bug risk | High (sync issues) | Low |
| Historical lookback | 5000 bars max | Unlimited |

### UDT Time Capture Pattern

```pinescript
// ALWAYS capture BOTH time and bar_index when events occur
var int eventStartTime = na
var int eventStartBar = na

if eventDetected
    eventStartTime := time        // For xloc.bar_time drawing
    eventStartBar := bar_index    // For Y calculation (slope * bar + intercept)

// Later, create UDT with both
newItem = MyType.new(
    startTime = eventStartTime,      // Drawing coordinate
    startBarIndex = eventStartBar,   // Calculation coordinate
    ...
)
```

## Core Optimization Areas

### 1. Calculation Caching

```pinescript
// ❌ BEFORE: Repeated calculations
plot(ta.sma(close, 20) > ta.sma(close, 50) ? high : low)
bgcolor(ta.sma(close, 20) > ta.sma(close, 50) ? color.green : color.red)

// ✅ AFTER: Cache once, use many times
sma20 = ta.sma(close, 20)
sma50 = ta.sma(close, 50)
bullish = sma20 > sma50
plot(bullish ? high : low)
bgcolor(bullish ? color.new(color.green, 90) : color.new(color.red, 90))
```

### 2. Security Call Optimization

```pinescript
// ❌ BEFORE: Multiple security() calls (expensive)
htfClose = request.security(syminfo.tickerid, "D", close)
htfHigh = request.security(syminfo.tickerid, "D", high)
htfLow = request.security(syminfo.tickerid, "D", low)
htfVolume = request.security(syminfo.tickerid, "D", volume)

// ✅ AFTER: Single tuple call
[htfClose, htfHigh, htfLow, htfVolume] = request.security(
    syminfo.tickerid, "D",
    [close, high, low, volume])
```

### 3. Loop Optimization (Use `for...in`)

```pinescript
// ❌ SLOW/DANGEROUS: Boundary re-evaluated each iteration
for i = 0 to array.size(arr) - 1
    val = array.get(arr, i)
    // process

// ✅ BEST: Use for...in (safe, clean, preferred)
for element in arr
    // Process element directly - no boundary issues

// ✅ BEST: With index when needed
for [i, element] in arr
    // Have both index and value

// ✅ FASTEST: Use built-in array methods when possible
total = array.sum(arr)
maxVal = array.max(arr)
avgVal = array.avg(arr)
```

### 4. Conditional Logic Optimization

```pinescript
// ❌ SLOW: All conditions evaluated
signal = cond1 and cond2 and cond3 and expensiveCalc()

// ✅ FAST: Short-circuit with cheap checks first
signal = cond1  // Cheapest first
signal := signal and cond2
signal := signal and cond3
signal := signal and expensiveCalc()  // Only if others pass
```

## User Experience Optimization

### 1. Input Organization with Active Parameter

```pinescript
// Professional input structure with conditional visibility

// === Main Settings ===
strategyMode = input.string("Trend Following", "Strategy Mode",
    options=["Trend Following", "Mean Reversion", "Custom"],
    group="Strategy")

// === Trend Following Settings (conditional) ===
tfLength = input.int(20, "Trend Length",
    group="Trend Following",
    active=(strategyMode == "Trend Following"),
    tooltip="Period for trend detection")

tfMultiplier = input.float(2.0, "Trend Multiplier",
    group="Trend Following",
    active=(strategyMode == "Trend Following"))

// === Mean Reversion Settings (conditional) ===
mrLength = input.int(14, "Reversion Length",
    group="Mean Reversion",
    active=(strategyMode == "Mean Reversion"))

mrThreshold = input.float(2.0, "Reversion Threshold",
    group="Mean Reversion",
    active=(strategyMode == "Mean Reversion"))

// === Visual Settings ===
showPlots = input.bool(true, "Show Plots", group="Visual")
plotColor = input.color(color.blue, "Plot Color",
    group="Visual",
    active=showPlots)  // Only show when plots enabled
```

### 2. Professional Color Schemes

```pinescript
// Modern, accessible color palette
var color BULL = color.new(#26a69a, 0)      // Teal green
var color BEAR = color.new(#ef5350, 0)      // Coral red
var color BULL_BG = color.new(#26a69a, 85)  // Transparent
var color BEAR_BG = color.new(#ef5350, 85)
var color NEUTRAL = color.new(#787b86, 0)   // Gray

// Gradient based on strength
strength = ta.rsi(close, 14)
gradientColor = color.from_gradient(strength, 30, 70, BEAR, BULL)

// Dark mode friendly table
var table infoTable = table.new(position.top_right, 2, 5,
    bgcolor=color.new(#131722, 10),  // TradingView dark bg
    border_color=color.new(#363a45, 0),
    border_width=1)
```

### 3. Responsive Plot Styling with Line Styles

```pinescript
// Use new linestyle parameter for visual hierarchy
ma = ta.ema(close, maLength)
maPlot = plot(ma, "MA", color.blue, linewidth=2,
    linestyle=plot.linestyle_solid)  // Primary: solid

// Secondary indicators: dashed
plot(upperBand, "Upper", color.gray,
    linestyle=plot.linestyle_dashed)
plot(lowerBand, "Lower", color.gray,
    linestyle=plot.linestyle_dashed)

// Projections/targets: dotted
plot(showTargets ? target : na, "Target", color.green,
    linestyle=plot.linestyle_dotted)
```

### 4. Smart Alert Messages

```pinescript
// Comprehensive alert with all relevant info
buildAlert(direction, price, strength) =>
    msg = "🔔 " + syminfo.ticker + " ALERT\n"
    msg += "═══════════════════\n"
    msg += "Direction: " + direction + "\n"
    msg += "Price: $" + str.tostring(price, "#,###.##") + "\n"
    msg += "Strength: " + str.tostring(strength, "#.#") + "/10\n"
    msg += "Time: " + str.format_time(time, "yyyy-MM-dd HH:mm") + "\n"
    msg += "═══════════════════"
    msg

alertcondition(buySignal,
    "Buy Signal",
    buildAlert("LONG", close, signalStrength))
```

## Performance Checklist

### Architecture (Check First!)
- [ ] Use UDT-first for complex data structures
- [ ] Replace parallel arrays with single UDT array
- [ ] Use `xloc.bar_time` for drawings (eliminates clamping)
- [ ] Store time + bar_index for each coordinate
- [ ] Add methods to UDT for encapsulated logic

### Must-Do Optimizations
- [ ] Cache all repeated calculations
- [ ] Combine security() calls into tuples
- [ ] Cache loop boundaries (March 2025 critical)
- [ ] Put cheap conditions before expensive ones
- [ ] Use `var` for values that don't change per bar

### UX Optimizations (2025 Features)
- [ ] Use `active` parameter for conditional inputs
- [ ] Group related inputs logically
- [ ] Add tooltips to complex inputs
- [ ] Use new `linestyle` parameter for visual hierarchy
- [ ] Implement mobile-friendly compact mode option

### Visual Optimizations
- [ ] Use consistent color scheme
- [ ] Implement gradient colors for strength
- [ ] Use appropriate plot line widths
- [ ] Add transparency to background colors
- [ ] Make tables dark-mode friendly

## Mobile-Friendly Optimization

```pinescript
// Compact mode for mobile viewing
compactMode = input.bool(false, "📱 Compact Mode",
    group="Display",
    tooltip="Enable for better mobile viewing")

// Adjust based on mode
plotWidth = compactMode ? 1 : 2
labelSize = compactMode ? size.tiny : size.small

// Conditional table display
if not compactMode
    // Full table with details
    table.cell(infoTable, 0, 0, "Full Statistics", text_color=color.white)
    // ... more cells
else
    // Minimal display
    table.cell(infoTable, 0, 0, bullish ? "↑" : "↓",
        text_color=bullish ? BULL : BEAR,
        text_size=size.large)
```

## Memory Optimization

```pinescript
// Use var for persistent values
var float highestHigh = na
var int barsSinceSignal = 0

// Limit array sizes
var array<float> recentPrices = array.new<float>(100)
if barstate.isconfirmed
    array.push(recentPrices, close)
    if array.size(recentPrices) > 100
        array.shift(recentPrices)

// Clear unused data
if newDay
    array.clear(intradayData)
```

## Optimization Quick Wins

| Issue | Before | After | Impact |
|-------|--------|-------|--------|
| **Parallel arrays** | 6+ arrays to sync | 1 UDT array | 80% less code |
| **bar_index drawing** | Clamping + 5000 limit | xloc.bar_time | Unlimited lookback |
| **Drawing code** | Duplicate blocks | UDT methods | DRY, maintainable |
| Repeated SMA | `ta.sma(close,20)` x5 | Cache in variable | 5x faster |
| Multiple security() | 4 separate calls | 1 tuple call | 4x faster |
| Loop boundary | `array.size(arr)` in loop | Cache before loop | Prevents hang |
| All inputs visible | Cluttered UI | Use `active` param | Clean UX |
| One line style | All solid | solid/dashed/dotted | Better hierarchy |

**The top 3 optimizations (UDT-related) provide the biggest gains.** Balance optimization with readability. Don't over-optimize at the expense of maintainability.
