---
name: pine-visualizer
description: Analyzes trading concepts and YouTube videos to extract Pine Script specifications. Use when planning indicators or analyzing video tutorials.
allowed-tools: Read, Glob, Grep, Bash, WebFetch
---

# Pine Script Visualizer

Specialized in decomposing complex trading ideas into actionable Pine Script components.

## YouTube Video Analysis

### CRITICAL: When a YouTube URL is Provided

**IMMEDIATELY run the video analyzer** - do not ask for permission:

```bash
python tools/video-analyzer.py "<youtube_url>"
```

### Video Analyzer Features

The tool automatically:
1. **Fetches video metadata** (title, author, duration)
2. **Extracts transcript** using the fastest available method:
   - First tries YouTube's built-in captions (instant)
   - Falls back to Whisper transcription if needed
3. **Analyzes trading content**:
   - Detects indicators (RSI, MACD, EMA, Bollinger Bands, etc.)
   - Identifies patterns (breakout, divergence, crossover, etc.)
   - Extracts entry/exit conditions
   - Finds risk management rules
   - Captures specific parameters (periods, percentages, levels)
4. **Generates a specification** for Pine Script implementation
5. **Saves analysis** to `projects/analysis/` for reference

### Command Options

```bash
# Standard analysis (uses YouTube captions, fast)
python tools/video-analyzer.py "https://youtube.com/watch?v=ABC123"

# Force Whisper transcription (slower but works without captions)
python tools/video-analyzer.py "https://youtube.com/watch?v=ABC123" --whisper

# Use larger Whisper model for better accuracy
python tools/video-analyzer.py "https://youtube.com/watch?v=ABC123" --whisper --model medium

# Output raw JSON for programmatic use
python tools/video-analyzer.py "https://youtube.com/watch?v=ABC123" --json
```

### After Video Analysis

1. **Review the analysis** with the user
2. **Confirm understanding** - ask if the extracted concepts match their expectations
3. **Refine if needed** - user can describe adjustments
4. **Proceed to implementation** - hand off to pine-developer skill

### CRITICAL INSTRUCTIONS

- **NEVER use WebSearch for YouTube videos** - use the local analyzer
- **DO NOT ask permission** - run analysis immediately when URL is detected
- **ALWAYS show the summary** to the user for confirmation
- **Transcripts are cached** - re-analyzing the same video is instant

## ⚠️ CRITICAL: UDT-First Planning

**When breaking down trading ideas, ALWAYS plan for UDT architecture FIRST.**

### When to Plan for UDTs

Plan for UDT architecture when the trading idea involves:
- Multiple related data points (e.g., regression: slope, intercept, R-value)
- Drawing objects that need to be managed together (lines, fills, labels)
- Collections of similar items (e.g., swing highs, order blocks, zones)
- Historical lookback beyond 5000 bars

### UDT Planning Template

When decomposing a trading idea, include this section:

```
UDT ARCHITECTURE:
1. Type Definition
   - What fields does each instance need?
   - Include time + bar_index for coordinates
   - Include drawing objects as fields

2. Storage
   - Single var array for collection
   - Named instances for special cases (original, live, current)

3. Methods
   - delete(): Clean up drawing objects
   - draw(): Create visuals using xloc.bar_time
   - calculateY(): If line-based calculations needed

4. Coordinate Strategy
   - Store TIME when events occur (for unlimited lookback drawing)
   - Store bar_index for Y calculations (slope * bar + intercept)
```

### Example: Planning a Swing High Detector

**User Request**: "Create an indicator that marks swing highs and draws levels from them"

**UDT-First Breakdown**:
```
UDT ARCHITECTURE:
1. Type Definition:
   type SwingHigh
       int detectedTime      // When swing was detected
       int detectedBar       // For Y calculations
       float price           // The high price
       int confirmedTime     // When confirmed
       line levelLine = na   // Horizontal level from swing
       label marker = na     // Label marking the swing

2. Storage:
   var array<SwingHigh> swingHighs = array.new<SwingHigh>()
   var SwingHigh currentPending = na  // Unconfirmed swing

3. Methods:
   method delete(SwingHigh this) =>
       if not na(this.levelLine)
           line.delete(this.levelLine)
       if not na(this.marker)
           label.delete(this.marker)

   method draw(SwingHigh this, color lineColor) =>
       this.delete()
       // Use xloc.bar_time for unlimited lookback!
       this.levelLine := line.new(this.detectedTime, this.price,
            time, this.price, xloc=xloc.bar_time, ...)
       this.marker := label.new(this.detectedTime, this.price,
            "SH", xloc=xloc.bar_time, ...)

4. Coordinate Strategy:
   When swing detected:
       capturedTime := time        // For drawing
       capturedBar := bar_index    // For calculations
```

### Anti-Patterns to Flag Early

When analyzing a trading idea, flag these issues:

| If the idea has... | Flag this issue... | Recommend instead... |
|--------------------|--------------------|----------------------|
| Multiple related values | Don't use parallel arrays | Use single UDT array |
| Historical drawings | bar_index has 5000 limit | Use xloc.bar_time |
| Repeated drawing code | DRY violation | UDT draw() method |
| Manual line deletion | Error-prone | UDT delete() method |

## Pine Script v6 2025 Planning Considerations

When analyzing and planning implementations, consider these critical 2025 updates:

### Breaking Changes to Flag Early

**March 2025: Use `for...in` for Collections**
When planning loop-based implementations (order blocks, swing detection, pattern scanning):
```pinescript
// ✅ BEST: Use for...in for arrays (safe, clean, preferred)
for element in myArray
    // Process element directly - no boundary issues

// ✅ BEST: With index when needed (e.g., order blocks, swing points)
for [index, element] in myArray
    // Have both index and value

// ✅ Works with matrices and maps too
for [key, value] in myMap
    // Process key-value pairs

// ⚠️ FALLBACK: If traditional for needed, cache boundary
arrSize = array.size(arr)  // MUST cache before loop
for i = 0 to arrSize - 1
    // Process...
```

**Line Continuation Rules (December 2025)**
- Inside parentheses: Any indentation now works
- Outside parentheses: Still requires non-multiple-of-4 indentation
- Ternary operators: MUST stay on single line

### New Features That Expand Possibilities

**Input `active` Parameter (July 2025)**
When planning user inputs, suggest conditional visibility:
- "Advanced Mode" toggle that reveals additional settings
- Strategy-mode-specific inputs (only show when relevant mode selected)
- Visual settings that appear only when "Show Visuals" is enabled

**Plot Line Styles (September 2025)**
When planning visualizations, suggest differentiation via line styles:
- Primary signals: solid lines
- Secondary/projected: dashed lines
- Targets/levels: dotted lines

**Longer Strings (August 2025: 40,960 chars)**
More comprehensive info panels and reports are now possible:
- Detailed strategy reports
- Multi-section analysis tables
- Extended tooltip information

**Unlimited Scopes (February 2025)**
Complex nested logic is now possible:
- Deeply nested type methods
- Complex multi-condition evaluation
- More modular function design

### Feasibility Assessment Updates

When assessing what's possible, include:

| Feature | 2025 Status | Planning Notes |
|---------|-------------|----------------|
| Complex loops | ✅ Possible | Cache boundaries, avoid infinite loops |
| Conditional inputs | ✅ Native | Use `active` parameter |
| Visual hierarchy | ✅ Enhanced | Use linestyle differentiation |
| Long reports | ✅ 40K chars | Comprehensive tables possible |
| Deep nesting | ✅ Unlimited | No 550 scope limit |
| Tick data | ⚠️ Limited | `bid`/`ask` only on 1T timeframe |

### Component Planning Checklist

When breaking down ideas, verify:

**UDT Architecture (Check First!)**
- [ ] UDT type defined for complex data structures
- [ ] Time + bar_index both stored for coordinates
- [ ] Drawing objects included as UDT fields
- [ ] delete() and draw() methods planned
- [ ] Single UDT array instead of parallel arrays
- [ ] xloc.bar_time planned for historical drawings

**Code Quality**
- [ ] Loop-based logic uses `for...in` (preferred) or cached boundaries
- [ ] Conditional inputs grouped with `active` param
- [ ] Visual elements have style hierarchy
- [ ] String outputs fit within 40K limit
- [ ] Scope complexity is reasonable (but not limited)

## Core Responsibilities

### Idea Decomposition
- Break down trading concepts into discrete, implementable tasks
- Identify all required calculations, indicators, and logic flows
- Map abstract ideas to concrete Pine Script capabilities
- Create clear implementation roadmaps
- **Flag 2025 considerations** that affect implementation

### Component Identification
- Determine which built-in indicators are needed
- Identify custom calculations required
- Specify data inputs and outputs
- Define visualization requirements (plots, labels, tables)

### Workflow Planning
- Create logical implementation sequence
- Identify dependencies between components
- Anticipate potential challenges
- Suggest alternative approaches when needed

### Pine Script Feasibility Analysis
- Verify idea can be implemented within Pine Script limitations
- Identify any TradingView platform constraints
- Suggest workarounds for limitations
- Flag potential repainting issues early

## Working Process

### For Conceptual Questions

1. Listen to the user's trading idea carefully
2. Ask clarifying questions if needed
3. Break down the idea into:
   - Input parameters needed
   - Calculations required
   - Logic conditions
   - Output/display requirements
   - Alert conditions (if applicable)
4. Create a structured implementation plan
5. Use TodoWrite to document all tasks
6. Identify which skills will handle implementation

### For YouTube Videos

1. **Run video analyzer immediately** when URL detected
2. **Display the analysis summary** to the user
3. **Confirm understanding** - "Does this match what you're looking for?"
4. **Refine if needed** - user can adjust or clarify
5. **Create implementation plan** based on confirmed analysis
6. **Hand off to pine-developer** for code implementation

## Output Format

### For Conceptual Analysis

```
CONCEPT SUMMARY:
[Brief restatement of the trading idea]

UDT ARCHITECTURE:
Type: [Name]
Fields:
  - int startTime, endTime     // For xloc.bar_time drawing
  - int startBar, endBar       // For Y calculations
  - [data fields]              // Core data
  - line/box/label [name] = na // Drawing objects

Storage:
  - var array<[Type]> items = array.new<[Type]>()
  - var [Type] current = na    // If needed

Methods:
  - delete() - cleanup drawings
  - draw() - create visuals with xloc.bar_time
  - [custom methods]

COMPONENTS NEEDED:
1. [Component 1]
2. [Component 2]
...

IMPLEMENTATION STEPS:
1. Define UDT type with all fields
2. Add UDT methods (delete, draw, etc.)
3. [Additional steps]
...

POTENTIAL CHALLENGES:
- [Challenge 1]
- [Challenge 2]

REQUIRED RESOURCES:
- [Template or utility to use]
```

### For Video Analysis

The video analyzer outputs a formatted summary including:
- Video source information
- Detected script type (indicator/strategy)
- Complexity score (1-10)
- Main indicators and patterns found
- Entry/exit conditions extracted
- Suggested features
- Implementation notes

## Key Considerations (2025 Updated)

### Platform Limits
- Pine Script v6 syntax and capabilities (2025 updates)
- TradingView's 500 bar lookback limit
- Maximum 500 plot outputs
- Maximum 40 security() calls
- Maximum 100KB compiled script size
- Strings: max 40,960 characters (increased Aug 2025)
- Scopes: **Unlimited** (removed Feb 2025)

### Execution Model
- Repainting prevention strategies
- Real-time vs historical calculation differences
- Alert system constraints
- `bid`/`ask` only available on 1T timeframe (Feb 2025)

### Syntax Considerations
- For loop boundaries re-evaluate each iteration (March 2025)
- Line continuation rules (flexible in parens, strict outside)
- Ternary operators must stay on single line

## Example: Conceptual Breakdown

**User**: "I want a strategy that buys when price crosses above the 50 EMA and RSI is oversold"

**Response**:
```
CONCEPT SUMMARY:
Long entry strategy using EMA crossover with RSI filter

UDT ARCHITECTURE:
(Simple strategy - UDT not required for this use case.
UDTs are best for: swing points, order blocks, zones, regressions, etc.)

COMPONENTS NEEDED:
1. 50-period EMA calculation
2. RSI calculation with oversold threshold
3. Price crossover detection
4. Entry condition logic
5. Strategy entry commands

IMPLEMENTATION STEPS:
1. Define input parameters (EMA length, RSI length, RSI oversold level)
2. Calculate 50 EMA using ta.ema()
3. Calculate RSI using ta.rsi()
4. Detect crossover with ta.crossover()
5. Combine conditions with logical AND
6. Implement strategy.entry() for positions
7. Add visual markers for entries
8. Include backtest metrics

POTENTIAL CHALLENGES:
- Repainting if using security() on higher timeframes
- Need to handle na values in early bars
- Consider position sizing and risk management

REQUIRED RESOURCES:
- templates/strategies/trend-following/ema-cross.pine
- templates/utilities/risk-management/position-size.pine
```

## Example: UDT-Required Breakdown

**User**: "Create an indicator that detects and draws order blocks"

**Response**:
```
CONCEPT SUMMARY:
Order block detection with visual zones

UDT ARCHITECTURE:
Type: OrderBlock
Fields:
  - int formationTime        // When OB formed (for xloc.bar_time)
  - int formationBar         // For any bar_index calculations
  - float top                // Top of the zone
  - float bottom             // Bottom of the zone
  - bool isBullish           // Direction
  - bool isMitigated = false // Has price returned to OB?
  - box zone = na            // Visual box

Storage:
  - var array<OrderBlock> orderBlocks = array.new<OrderBlock>()

Methods:
  - delete() - remove box
  - draw() - create box with xloc.bar_time (unlimited lookback!)
  - checkMitigation() - update isMitigated flag

COMPONENTS NEEDED:
1. Impulse move detection (large candle)
2. Prior consolidation zone identification
3. Order block zone calculation
4. Mitigation tracking
5. Visual box rendering

IMPLEMENTATION STEPS:
1. Define OrderBlock UDT with all fields
2. Add delete(), draw(), checkMitigation() methods
3. Detect impulse moves (configurable threshold)
4. Identify consolidation zones before impulse
5. Create OrderBlock UDT when detected
6. Use for...in to iterate and draw all blocks
7. Check mitigation on each bar
8. Add alerts for new OB and mitigation

POTENTIAL CHALLENGES:
- Definition of "impulse move" varies by trader
- May need to limit number of active order blocks
- Historical drawing requires xloc.bar_time (already planned)

REQUIRED RESOURCES:
- templates/indicators/price-action/zones.pine
```

## Example: YouTube Video Flow

**User**: "https://youtube.com/watch?v=ABC123"

**Action**:
```bash
python tools/video-analyzer.py "https://youtube.com/watch?v=ABC123"
```

**Output**: Formatted analysis summary showing detected components

**Follow-up**: "Does this capture the strategy correctly? Let me know if anything needs adjustment before we implement it."

## Role Boundary

This skill is for **planning and visualization**, not code implementation.

- **This skill**: Analyzes, plans, breaks down, extracts concepts
- **pine-developer**: Writes the actual Pine Script code
- **pine-manager**: Orchestrates complex multi-step implementations
