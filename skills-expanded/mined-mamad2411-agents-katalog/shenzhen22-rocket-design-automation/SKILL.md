---
name: shenzhen22-rocket-design-automation
description: Automate rocket design and manufacturing workflows with TypeScript-based calculation, modeling, and production tools
triggers:
  - design a model rocket with automated calculations
  - generate rocket thrust and stability calculations
  - automate rocket manufacturing specifications
  - calculate rocket trajectory and performance
  - design rocket fins and body tube dimensions
  - optimize rocket motor selection and staging
  - generate rocket manufacturing blueprints
  - validate rocket stability and center of pressure
---

# Shenzhen22 Rocket Design Automation

> Skill by [ara.so](https://ara.so) — Design Skills collection.

A TypeScript-based automation program for designing and manufacturing model rockets, developed by students at Shenzhen 22 High School. This tool automates complex calculations for rocket stability, thrust, trajectory, and generates manufacturing specifications.

## Installation

```bash
# Clone the repository
git clone https://github.com/Kevin100202/Rocket-Design-and-Manufacturing-Automation-Program-from-Shenzhen22highschool.git
cd Rocket-Design-and-Manufacturing-Automation-Program-from-Shenzhen22highschool

# Install dependencies
npm install

# Build the TypeScript project
npm run build

# Run the program
npm start
```

## Project Structure

The project typically includes modules for:
- **Stability Calculations**: Center of gravity (CG) and center of pressure (CP)
- **Thrust Calculations**: Motor performance and impulse
- **Trajectory Modeling**: Flight path simulation
- **Fin Design**: Aerodynamic surface optimization
- **Body Tube Sizing**: Structural dimensions
- **Manufacturing Output**: Blueprints and cut lists

## Core API Usage

### Basic Rocket Design

```typescript
import { RocketDesign, StabilityCalculator, ThrustCalculator } from './rocket-design-automation';

// Create a new rocket design
const rocket = new RocketDesign({
  name: "Student Rocket Alpha",
  bodyTubeDiameter: 50, // mm
  bodyTubeLength: 600, // mm
  finCount: 3,
  finRootChord: 100, // mm
  finTipChord: 40, // mm
  finHeight: 80, // mm
  motorType: "C6-5"
});

// Calculate stability
const stabilityCalc = new StabilityCalculator(rocket);
const stability = stabilityCalc.calculate();

console.log(`Center of Gravity: ${stability.cg}mm from nose`);
console.log(`Center of Pressure: ${stability.cp}mm from nose`);
console.log(`Stability Margin: ${stability.margin} calibers`);
console.log(`Stable: ${stability.isStable ? 'Yes' : 'No'}`);
```

### Thrust and Performance Analysis

```typescript
import { ThrustCalculator, Motor } from './rocket-design-automation';

// Define motor specifications
const motor = new Motor({
  designation: "C6-5",
  totalImpulse: 10, // Newton-seconds
  averageThrust: 6, // Newtons
  burnTime: 1.6, // seconds
  propellantMass: 12.5, // grams
  totalMass: 24, // grams
  delay: 5 // seconds
});

const thrustCalc = new ThrustCalculator(rocket, motor);

// Calculate performance metrics
const performance = thrustCalc.calculatePerformance();

console.log(`Maximum Velocity: ${performance.maxVelocity.toFixed(2)} m/s`);
console.log(`Maximum Altitude: ${performance.maxAltitude.toFixed(2)} m`);
console.log(`Acceleration: ${performance.maxAcceleration.toFixed(2)} m/s²`);
console.log(`Thrust-to-Weight: ${performance.thrustToWeight.toFixed(2)}`);
```

### Trajectory Simulation

```typescript
import { TrajectorySimulator, WindConditions } from './rocket-design-automation';

const wind = new WindConditions({
  velocity: 5, // m/s
  direction: 270, // degrees
  altitude: 100 // m elevation
});

const simulator = new TrajectorySimulator(rocket, motor, wind);

// Run simulation with time steps
const trajectory = simulator.simulate({
  timeStep: 0.01, // seconds
  maxTime: 30 // seconds
});

// Access trajectory data points
trajectory.dataPoints.forEach((point, index) => {
  if (index % 100 === 0) { // Log every 100th point
    console.log(`t=${point.time.toFixed(2)}s: ` +
                `h=${point.altitude.toFixed(2)}m, ` +
                `v=${point.velocity.toFixed(2)}m/s`);
  }
});

console.log(`Apogee: ${trajectory.apogee.toFixed(2)}m at ${trajectory.apogeeTime.toFixed(2)}s`);
console.log(`Landing distance: ${trajectory.landingDistance.toFixed(2)}m from pad`);
```

### Fin Design Optimization

```typescript
import { FinDesigner, FinShape } from './rocket-design-automation';

const finDesigner = new FinDesigner(rocket);

// Design trapezoidal fins
const fins = finDesigner.design({
  shape: FinShape.TRAPEZOIDAL,
  rootChord: 100, // mm
  tipChord: 40, // mm
  height: 80, // mm
  sweepAngle: 30, // degrees
  thickness: 3, // mm
  material: "balsa"
});

// Optimize for stability
const optimized = finDesigner.optimize({
  targetStability: 1.5, // calibers
  minFinHeight: 60, // mm
  maxFinHeight: 120, // mm
  constraints: {
    maxWeight: 50, // grams
    minStrength: "moderate"
  }
});

console.log(`Optimized fin height: ${optimized.height}mm`);
console.log(`Optimized root chord: ${optimized.rootChord}mm`);
console.log(`Resulting stability: ${optimized.stability} calibers`);
```

### Manufacturing Blueprint Generation

```typescript
import { ManufacturingGenerator, OutputFormat } from './rocket-design-automation';

const generator = new ManufacturingGenerator(rocket);

// Generate cutting templates
const templates = generator.generateTemplates({
  includeFinTemplate: true,
  includeCentering: true,
  includeNoseCone: true,
  scale: 1.0 // Full scale
});

// Export to various formats
await generator.export({
  format: OutputFormat.SVG,
  filename: "rocket-templates.svg",
  outputPath: "./manufacturing/"
});

await generator.export({
  format: OutputFormat.PDF,
  filename: "rocket-blueprints.pdf",
  outputPath: "./manufacturing/"
});

// Generate parts list
const partsList = generator.generatePartsList();
console.log("Manufacturing Parts List:");
partsList.forEach(part => {
  console.log(`${part.name}: ${part.quantity}x - ${part.material} - ${part.dimensions}`);
});
```

### Complete Design Workflow

```typescript
import { 
  RocketDesign, 
  DesignWorkflow, 
  ValidationResult 
} from './rocket-design-automation';

// Create a complete design workflow
const workflow = new DesignWorkflow();

// Step 1: Initial design
const design = workflow.createDesign({
  targetAltitude: 300, // meters
  bodyDiameter: 50, // mm
  finCount: 4,
  motorClass: "C"
});

// Step 2: Validate design
const validation: ValidationResult = workflow.validate(design);

if (!validation.isValid) {
  console.error("Design validation failed:");
  validation.errors.forEach(error => console.error(`- ${error}`));
  
  // Auto-fix common issues
  const fixed = workflow.autoFix(design, validation);
  console.log("Applied automatic fixes");
}

// Step 3: Optimize
const optimized = workflow.optimize(design, {
  objective: "max_altitude",
  constraints: {
    maxWeight: 200, // grams
    maxLength: 800, // mm
    stabilityMargin: [1.0, 2.5] // calibers range
  }
});

// Step 4: Generate manufacturing data
const manufacturing = workflow.generateManufacturing(optimized);

// Step 5: Export complete package
await workflow.exportPackage({
  design: optimized,
  manufacturing: manufacturing,
  outputPath: "./rocket-build/",
  formats: ["pdf", "svg", "json"]
});

console.log("Complete rocket design package generated!");
```

## Configuration

Create a `rocket-config.json` file in the project root:

```json
{
  "units": {
    "length": "mm",
    "mass": "g",
    "force": "N"
  },
  "safety": {
    "minStabilityMargin": 1.0,
    "maxStabilityMargin": 2.5,
    "minThrustToWeight": 5.0
  },
  "simulation": {
    "timeStep": 0.01,
    "dragCoefficient": 0.75,
    "airDensity": 1.225
  },
  "manufacturing": {
    "tolerances": {
      "linear": 0.5,
      "angular": 1.0
    },
    "materials": {
      "bodyTube": "cardboard",
      "fins": "balsa",
      "noseCone": "plastic"
    }
  },
  "output": {
    "defaultFormat": "svg",
    "precision": 2
  }
}
```

Load configuration in code:

```typescript
import { ConfigLoader } from './rocket-design-automation';

const config = ConfigLoader.load('./rocket-config.json');
const workflow = new DesignWorkflow(config);
```

## Common Patterns

### Batch Design Generation

```typescript
import { BatchProcessor } from './rocket-design-automation';

const batch = new BatchProcessor();

// Generate multiple designs with varying parameters
const designs = batch.generate({
  baseDesign: {
    bodyDiameter: 50,
    bodyLength: 600,
    finCount: 3
  },
  variations: {
    finHeight: [60, 70, 80, 90, 100],
    motorType: ["C6-5", "C6-7", "D12-5"]
  }
});

// Analyze all designs
const results = batch.analyze(designs);

// Find best design
const best = results.findBest({
  criteria: "max_altitude",
  constraints: { stability: [1.0, 2.5] }
});

console.log(`Best design: ${best.name} - ${best.maxAltitude}m altitude`);
```

### Real-time Design Validation

```typescript
import { RocketDesign, RealtimeValidator } from './rocket-design-automation';

const validator = new RealtimeValidator();
const rocket = new RocketDesign({ /* ... */ });

// Listen for design changes
validator.watch(rocket);

validator.on('stabilityWarning', (data) => {
  console.warn(`Stability margin ${data.margin} outside safe range`);
});

validator.on('weightWarning', (data) => {
  console.warn(`Total weight ${data.weight}g exceeds recommendation`);
});

// Modify design - validation runs automatically
rocket.setFinHeight(120);
rocket.setMotor("D12-5");
```

## Troubleshooting

### Unstable Design

```typescript
// If stability.isStable === false
if (!stability.isStable) {
  // Option 1: Increase fin size
  rocket.setFinHeight(rocket.finHeight * 1.2);
  
  // Option 2: Move fins rearward
  rocket.setFinPosition(rocket.finPosition + 20);
  
  // Option 3: Add nose weight
  rocket.addNoseWeight(10); // grams
  
  // Recalculate
  const newStability = stabilityCalc.calculate();
}
```

### Insufficient Thrust

```typescript
// If thrustToWeight < 5.0
if (performance.thrustToWeight < 5.0) {
  // Reduce weight or upgrade motor
  console.log("Consider:");
  console.log("- Using lighter materials");
  console.log("- Upgrading to next motor class");
  console.log(`- Current T/W: ${performance.thrustToWeight.toFixed(2)}`);
}
```

### Simulation Errors

```typescript
try {
  const trajectory = simulator.simulate({ timeStep: 0.01, maxTime: 30 });
} catch (error) {
  if (error.message.includes('divergence')) {
    // Reduce time step for better accuracy
    const trajectory = simulator.simulate({ 
      timeStep: 0.001, 
      maxTime: 30 
    });
  } else if (error.message.includes('invalid motor')) {
    console.error("Motor data incomplete or invalid");
  }
}
```

### Export Issues

```typescript
import { ManufacturingGenerator } from './rocket-design-automation';

const generator = new ManufacturingGenerator(rocket);

try {
  await generator.export({
    format: OutputFormat.SVG,
    filename: "templates.svg",
    outputPath: process.env.OUTPUT_PATH || "./output/"
  });
} catch (error) {
  if (error.code === 'ENOENT') {
    console.error("Output directory does not exist");
    // Create directory and retry
  } else if (error.message.includes('permission')) {
    console.error("Insufficient write permissions");
  }
}
```

## Environment Variables

```bash
# Optional configuration via environment
export ROCKET_UNITS=metric
export ROCKET_OUTPUT_PATH=./manufacturing/
export ROCKET_PRECISION=3
export ROCKET_SIMULATION_TIMESTEP=0.01
```

Use in code:

```typescript
const config = {
  units: process.env.ROCKET_UNITS || 'metric',
  outputPath: process.env.ROCKET_OUTPUT_PATH || './output/',
  precision: parseInt(process.env.ROCKET_PRECISION || '2'),
  simulation: {
    timeStep: parseFloat(process.env.ROCKET_SIMULATION_TIMESTEP || '0.01')
  }
};
```
