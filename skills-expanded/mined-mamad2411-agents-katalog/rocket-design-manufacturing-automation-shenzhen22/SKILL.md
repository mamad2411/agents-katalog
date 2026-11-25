---
name: rocket-design-manufacturing-automation-shenzhen22
description: Automated rocket design and manufacturing program built by students for aerospace engineering workflows
triggers:
  - "help me design a rocket"
  - "automate rocket manufacturing process"
  - "use the Shenzhen22 rocket design tool"
  - "calculate rocket trajectory and performance"
  - "generate rocket component specifications"
  - "optimize rocket design parameters"
  - "export rocket manufacturing files"
  - "simulate rocket flight dynamics"
---

# Rocket Design and Manufacturing Automation Program

> Skill by [ara.so](https://ara.so) — Design Skills collection.

This is a TypeScript-based automation program for rocket design and manufacturing developed by students at Shenzhen 22nd High School. The system provides tools for designing rocket components, calculating performance parameters, simulating flight dynamics, and generating manufacturing specifications.

## Installation

```bash
# Clone the repository
git clone https://github.com/Kevin100202/Rocket-Design-and-Manufacturing-Automation-Program-from-Shenzhen22highschool.git

cd Rocket-Design-and-Manufacturing-Automation-Program-from-Shenzhen22highschool

# Install dependencies
npm install

# Build the project
npm run build

# Run the program
npm start
```

## Project Structure

The project typically follows this structure for rocket design automation:

```
src/
├── core/              # Core design engine
├── components/        # Rocket component models
├── simulation/        # Flight simulation modules
├── manufacturing/     # Manufacturing file generation
├── calculations/      # Performance calculations
└── utils/            # Helper utilities
```

## Key Concepts

### Rocket Component Design

Define rocket components with physical and performance specifications:

```typescript
interface RocketComponent {
  name: string;
  type: 'noseCone' | 'bodyTube' | 'fins' | 'motor' | 'recovery';
  dimensions: {
    length: number;      // mm
    diameter: number;    // mm
    thickness?: number;  // mm
  };
  material: string;
  mass: number;          // grams
}

interface RocketDesign {
  id: string;
  name: string;
  components: RocketComponent[];
  specifications: {
    totalMass: number;
    centerOfGravity: number;
    centerOfPressure: number;
    stability: number;
  };
}
```

### Creating a Basic Rocket Design

```typescript
import { RocketDesigner } from './core/RocketDesigner';
import { MaterialLibrary } from './utils/MaterialLibrary';

// Initialize designer
const designer = new RocketDesigner();

// Create nose cone
const noseCone = designer.createComponent({
  name: 'Nose Cone',
  type: 'noseCone',
  dimensions: {
    length: 150,
    diameter: 50
  },
  material: MaterialLibrary.PLA,
  shape: 'ogive'
});

// Create body tube
const bodyTube = designer.createComponent({
  name: 'Main Body',
  type: 'bodyTube',
  dimensions: {
    length: 400,
    diameter: 50,
    thickness: 3
  },
  material: MaterialLibrary.CARDBOARD
});

// Create fin set
const fins = designer.createFinSet({
  name: 'Trapezoidal Fins',
  type: 'fins',
  count: 3,
  dimensions: {
    rootChord: 100,
    tipChord: 50,
    span: 80,
    thickness: 3
  },
  material: MaterialLibrary.BALSA_WOOD
});

// Assemble rocket
const rocket = designer.assembleRocket({
  name: 'Model Rocket Alpha',
  components: [noseCone, bodyTube, fins]
});
```

## Performance Calculations

### Stability Analysis

```typescript
import { StabilityCalculator } from './calculations/StabilityCalculator';

const calculator = new StabilityCalculator(rocket);

// Calculate center of gravity
const cog = calculator.calculateCenterOfGravity();
console.log(`Center of Gravity: ${cog} mm from nose`);

// Calculate center of pressure
const cop = calculator.calculateCenterOfPressure();
console.log(`Center of Pressure: ${cop} mm from nose`);

// Calculate stability margin (should be 1-2 calibers)
const stability = calculator.calculateStability();
console.log(`Stability Margin: ${stability} calibers`);

if (stability < 1) {
  console.warn('Warning: Rocket is unstable. Move CG forward or increase fin size.');
} else if (stability > 2) {
  console.warn('Warning: Rocket is overstable. May weathercock in wind.');
}
```

### Flight Simulation

```typescript
import { FlightSimulator } from './simulation/FlightSimulator';

const simulator = new FlightSimulator({
  rocket: rocket,
  motor: 'C6-5',  // Motor designation
  launchAngle: 90, // degrees
  windSpeed: 5,    // m/s
  temperature: 20, // celsius
  pressure: 101325 // Pa
});

// Run simulation
const flightData = await simulator.simulate();

console.log(`Maximum Altitude: ${flightData.maxAltitude.toFixed(2)} m`);
console.log(`Maximum Velocity: ${flightData.maxVelocity.toFixed(2)} m/s`);
console.log(`Flight Duration: ${flightData.flightTime.toFixed(2)} s`);
console.log(`Landing Distance: ${flightData.landingDistance.toFixed(2)} m`);

// Export trajectory data
simulator.exportTrajectory('./output/trajectory.csv');
```

## Manufacturing Automation

### Generate CAD Files

```typescript
import { CADExporter } from './manufacturing/CADExporter';

const exporter = new CADExporter(rocket);

// Export individual components
await exporter.exportComponent(noseCone, {
  format: 'STL',
  outputPath: './manufacturing/nose_cone.stl',
  units: 'mm',
  resolution: 'high'
});

await exporter.exportComponent(fins, {
  format: 'DXF',
  outputPath: './manufacturing/fins.dxf',
  units: 'mm'
});

// Export assembly
await exporter.exportAssembly({
  format: 'STEP',
  outputPath: './manufacturing/rocket_assembly.step'
});
```

### Generate Cutting Templates

```typescript
import { TemplateGenerator } from './manufacturing/TemplateGenerator';

const generator = new TemplateGenerator();

// Generate fin cutting template
const finTemplate = generator.createFinTemplate(fins, {
  includeMargins: true,
  marginSize: 5, // mm
  includeGuides: true,
  scale: 1.0
});

await finTemplate.exportPDF('./manufacturing/fin_template.pdf');
await finTemplate.exportSVG('./manufacturing/fin_template.svg');
```

### Bill of Materials

```typescript
import { BOMGenerator } from './manufacturing/BOMGenerator';

const bomGenerator = new BOMGenerator(rocket);

const bom = bomGenerator.generate({
  includeMaterials: true,
  includeHardware: true,
  includeCosts: true
});

console.log(bom.toTable());

// Export BOM
await bom.exportCSV('./manufacturing/bom.csv');
await bom.exportJSON('./manufacturing/bom.json');
```

## Advanced Features

### Parametric Design Optimization

```typescript
import { DesignOptimizer } from './core/DesignOptimizer';

const optimizer = new DesignOptimizer({
  objectives: ['maxAltitude', 'stability'],
  constraints: {
    maxMass: 500,        // grams
    maxLength: 600,      // mm
    minStability: 1.5,   // calibers
    maxStability: 2.0
  }
});

// Define parameter ranges
const optimizationResult = await optimizer.optimize({
  finSpan: { min: 60, max: 100 },
  finChord: { min: 80, max: 120 },
  bodyLength: { min: 300, max: 500 },
  noseConeLength: { min: 100, max: 200 }
});

console.log('Optimal parameters:', optimizationResult.parameters);
console.log('Expected altitude:', optimizationResult.altitude);
```

### Multi-Stage Rockets

```typescript
import { MultiStageRocket } from './core/MultiStageRocket';

const multiStage = new MultiStageRocket();

// Define first stage
const stage1 = designer.assembleRocket({
  name: 'Booster Stage',
  components: [
    boosterBody,
    boosterFins,
    boosterMotor
  ]
});

// Define second stage
const stage2 = designer.assembleRocket({
  name: 'Upper Stage',
  components: [
    upperNoseCone,
    upperBody,
    upperMotor
  ]
});

// Combine stages
multiStage.addStage(stage1, { separationDelay: 2.5 });
multiStage.addStage(stage2, { ignitionDelay: 0.5 });

// Simulate multi-stage flight
const multistageFlightData = await multiStage.simulate();
```

## Configuration

Create a `rocket.config.ts` file for project-wide settings:

```typescript
export const rocketConfig = {
  units: {
    length: 'mm',
    mass: 'g',
    velocity: 'm/s',
    force: 'N'
  },
  simulation: {
    timeStep: 0.01,        // seconds
    dragCoefficient: 0.75,
    airDensity: 1.225      // kg/m³
  },
  manufacturing: {
    tolerance: 0.5,        // mm
    defaultMaterial: 'PLA',
    printer3D: {
      bedSize: { x: 220, y: 220, z: 250 },
      layerHeight: 0.2,
      infill: 20
    }
  },
  safety: {
    minStability: 1.0,
    maxStability: 3.0,
    structuralSafetyFactor: 1.5
  }
};
```

## Common Patterns

### Design Validation Pipeline

```typescript
import { DesignValidator } from './core/DesignValidator';

async function validateAndExport(rocket: RocketDesign) {
  const validator = new DesignValidator();
  
  // Run all validation checks
  const validation = await validator.validate(rocket);
  
  if (!validation.isValid) {
    console.error('Design validation failed:');
    validation.errors.forEach(err => console.error(`- ${err}`));
    return false;
  }
  
  if (validation.warnings.length > 0) {
    console.warn('Design warnings:');
    validation.warnings.forEach(warn => console.warn(`- ${warn}`));
  }
  
  // Export if valid
  const exporter = new CADExporter(rocket);
  await exporter.exportAll('./output');
  
  return true;
}
```

### Batch Simulation

```typescript
import { BatchSimulator } from './simulation/BatchSimulator';

const batch = new BatchSimulator(rocket);

// Test multiple motor configurations
const motors = ['A8-3', 'B6-4', 'C6-5', 'D12-7'];
const results = await batch.simulateMotors(motors);

// Find optimal motor
const optimal = results.reduce((best, current) => 
  current.maxAltitude > best.maxAltitude ? current : best
);

console.log(`Optimal motor: ${optimal.motor}`);
console.log(`Altitude: ${optimal.maxAltitude.toFixed(2)} m`);
```

## Troubleshooting

### Stability Issues

If your rocket shows poor stability:

```typescript
// Check stability margin
if (rocket.specifications.stability < 1.0) {
  // Option 1: Increase fin size
  fins.dimensions.span += 10;
  
  // Option 2: Move CG forward (add nose weight)
  rocket.addBallast({ mass: 20, position: 'nose' });
  
  // Recalculate
  rocket.recalculate();
}
```

### Export Errors

If CAD export fails:

```typescript
try {
  await exporter.exportComponent(component, options);
} catch (error) {
  if (error.code === 'INVALID_GEOMETRY') {
    console.error('Component geometry is invalid. Check dimensions.');
  } else if (error.code === 'FILE_WRITE_ERROR') {
    console.error('Cannot write to output directory. Check permissions.');
  }
}
```

### Simulation Convergence

If simulations don't converge:

```typescript
const simulator = new FlightSimulator({
  rocket: rocket,
  motor: 'C6-5',
  solver: {
    method: 'RK4',         // Use Runge-Kutta 4th order
    maxIterations: 10000,
    tolerance: 1e-6,
    adaptiveStep: true
  }
});
```

## API Reference

### Core Classes

- `RocketDesigner` - Main design interface
- `StabilityCalculator` - CG/CP calculations
- `FlightSimulator` - Flight dynamics simulation
- `CADExporter` - Manufacturing file export
- `DesignOptimizer` - Parametric optimization
- `MaterialLibrary` - Material properties database

### Utility Functions

```typescript
import { convertUnits, calculateArea, interpolate } from './utils';

// Unit conversion
const meters = convertUnits(1000, 'mm', 'm'); // 1.0

// Area calculations
const finArea = calculateArea(fins);

// Data interpolation
const thrustAtTime = interpolate(motorData.thrust, 2.5);
```

## Resources

- Project repository: https://github.com/Kevin100202/Rocket-Design-and-Manufacturing-Automation-Program-from-Shenzhen22highschool
- Model rocket design guides: OpenRocket documentation
- NAR safety codes: https://www.nar.org/safety-information/model-rocket-safety-code/
