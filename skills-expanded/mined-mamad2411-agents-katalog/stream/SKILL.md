# SPH Water Simulation Project - Cursor Rules

## Project Overview
This is a Smoothed Particle Hydrodynamics (SPH) water simulation implemented in Go. The project provides a complete framework for fluid dynamics simulation using the SPH method with particle-based physics.

## Architecture
- **Modular Design**: Each component is in its own package under `internal/`
- **Clear Separation**: Vector math, particle system, configuration, and simulation logic are separated
- **Configuration-Driven**: Multiple presets for different simulation scenarios
- **Performance-Oriented**: Spatial hashing for O(1) neighbor search
- **Comprehensive Validation**: Complete kernel validation system with mathematical verification

## Key Packages
- `internal/vector`: 3D vector mathematics utilities
- `internal/particle`: Particle data structures and methods
- `internal/config`: Configuration system with validation
- `internal/simulation`: Main SPH algorithm implementation
- `internal/kernel`: SPH kernel functions with exact mathematical formulations
- `internal/spatial`: Spatial hashing for efficient neighbor search
- `internal/validation`: Comprehensive kernel validation suite
- `internal/boundary`: Advanced boundary condition system with multiple boundary types
- `internal/flow`: Stream flow system with turbulence, vorticity, and visualization

## Stream Flow System

### Flow System Architecture
The flow system (`internal/flow/`) provides realistic stream dynamics:

- **Flow Field Management**: Grid-based velocity fields with trilinear interpolation
- **Stream Path Generation**: Meandering river paths with realistic curvature
- **Turbulence Generation**: Multi-octave Perlin noise for realistic fluid turbulence
- **Vorticity Confinement**: Enhanced turbulence with proper curl calculations
- **Flow Visualization**: Streamlines with RK4 integration and flow vectors
- **Velocity Profiles**: Parabolic, logarithmic, and power law profiles

### Flow Types and Profiles
```go
// Flow types
FlowTypeStream     // Realistic stream/river flow
FlowTypeUniform    // Uniform flow field
FlowTypeTurbulent  // Turbulent flow field
FlowTypeVortex     // Vortex flow field

// Velocity profiles (faster at surface/center)
FlowProfileParabolic     // Parabolic profile (Poiseuille flow)
FlowProfileLogarithmic   // Logarithmic profile (boundary layer)
FlowProfilePowerLaw      // Power law profile
FlowProfileUniform       // Uniform velocity profile
```

### Stream Flow Implementation Rules

#### Flow Field Updates
- Update flow field every simulation step for dynamic flows
- Use trilinear interpolation for smooth velocity transitions
- Apply turbulence and vorticity in separate passes for stability
- Maintain flow rate control when enabled

#### Turbulence Generation
- Use multi-octave Perlin noise with configurable parameters:
  - **Octaves**: 4-8 for realistic complexity
  - **Persistence**: 0.3-0.7 for natural decay
  - **Lacunarity**: 1.8-2.2 for frequency scaling
- Time-evolve noise offset for dynamic turbulence
- Scale turbulence intensity based on Reynolds number

#### Vorticity Confinement
- Calculate vorticity using finite differences: `ω = ∇ × v`
- Apply confinement force: `f = ε(N × ω)` where N = ∇|ω|/|∇|ω||
- Use small epsilon (1e-3) to prevent numerical instabilities
- Update vorticity after base flow but before integration

#### Stream Path Generation
- Generate meandering paths with realistic sinuosity (1.2-2.0)
- Use multiple wavelengths for natural-looking meanders:
  - **Primary**: Main wavelength (10% of total length)
  - **Secondary**: 30% of primary wavelength
  - **Tertiary**: 10% of primary wavelength for fine detail
- Apply smoothing to reduce sharp corners
- Ensure monotonic elevation decrease (water flows downhill)

#### Velocity Profiles
- **Parabolic**: `v(r) = v_max * (1 - (r/R)²)` for laminar flow
- **Logarithmic**: `v(y) = (u*/κ) * ln(y/y₀)` for boundary layers
- **Power Law**: `v(r) = v_max * (1 - r/R)^n` where n = 1/7 typical
- Apply depth variation for 3D profiles (faster at surface)

### Flow Visualization Rules

#### Streamlines
- Use 4th-order Runge-Kutta integration for accuracy
- Terminate at stagnation points (|v| < 1e-6)
- Color-code by velocity magnitude using smooth gradients
- Limit streamline length to prevent infinite integration
- Regenerate seeds periodically for dynamic flows

#### Flow Vectors
- Space vectors uniformly across the domain
- Scale vector length proportional to velocity magnitude
- Use different colors for different flow components:
  - **Blue-Red**: Velocity magnitude (blue=slow, red=fast)
  - **Green-Yellow**: Vorticity magnitude (green=low, yellow=high)
- Update vectors at reduced frequency (30 FPS) for performance

## Boundary Conditions System

### Boundary Types and Implementation
The boundary system (`internal/boundary/`) supports multiple boundary types:

```go
BoundaryTypeSolid      // Solid walls using boundary particles
BoundaryTypeReflective // Reflective boundaries with damping
BoundaryTypeInflow     // Inflow with continuous particle generation
BoundaryTypeOutflow    // Outflow with particle removal
BoundaryTypeStreambed  // Streambed with friction and roughness
BoundaryTypePeriodic   // Periodic boundaries (wraparound)
```

### Boundary Implementation Rules

#### Solid Boundaries
- Use boundary particles for SPH force calculations
- Generate multiple layers (2-3) for stability
- Apply no-slip conditions at particle interfaces
- Include boundary particles in pressure and viscosity calculations

#### Reflective Boundaries
- Decompose velocity into normal and tangential components
- Apply restitution coefficient to normal component
- Preserve tangential component with friction
- Correct particle positions outside boundaries

#### Inflow/Outflow Boundaries
- **Inflow**: Generate particles at specified flow rate
- **Outflow**: Remove particles beyond threshold distance
- Maintain particle conservation with recycling
- Apply buffer zones to prevent sudden velocity changes

#### Streambed Boundaries
- Apply friction forces proportional to velocity
- Use roughness coefficient for realistic drag
- Implement velocity-dependent friction (turbulent vs laminar)
- Apply normal forces to prevent penetration

### Boundary Validation
```bash
# Run boundary validation
go build -o boundary-validation ./cmd/boundary_validation/
./boundary-validation --config=water --verbose

# Expected: High collision rates, proper force contributions
```

## Flow System Validation

### Flow Validation Command
```bash
# Complete flow system validation
go build -o flow-validation ./cmd/flow_validation/
./flow-validation --config=water --verbose

# Expected result: 10/10 tests passed (100% success rate)
```

### Flow Validation Tests
1. **Flow Field Initialization**: Grid setup and velocity field creation
2. **Base Flow Calculation**: Velocity computation at arbitrary points
3. **Turbulence Generation**: Perlin noise turbulence verification
4. **Vorticity Confinement**: Curl calculation and confinement forces
5. **Stream Path Generation**: Meandering path creation and smoothing
6. **Velocity Profiles**: Different profile implementations
7. **Flow Visualization**: Streamline and vector generation
8. **Flow Rate Control**: Automatic flow rate management
9. **Flow Forces Integration**: Integration with SPH simulation
10. **Performance Benchmarking**: Flow system performance metrics

### Flow Performance Expectations
- **Flow Updates**: >100 updates/s for real-time simulation
- **Velocity Calculations**: >1000 evaluations/s for particle forces
- **Streamline Integration**: <10ms for complex streamlines
- **Memory Efficiency**: <10MB for typical flow grids

## Configuration Management

### Flow System Configuration
```go
// Enable comprehensive flow system
cfg.EnableFlowSystem = true
cfg.FlowType = FlowTypeStream
cfg.FlowProfile = FlowProfileParabolic

// Turbulence parameters
cfg.FlowTurbulenceEnabled = true
cfg.FlowTurbulenceIntensity = 0.1  // 10% turbulence
cfg.FlowNoiseOctaves = 4           // 4 octaves for complexity

// Stream path configuration
cfg.EnableStreamPath = true
cfg.StreamPathMeander = 0.3        // 30% meandering intensity
cfg.StreamPathSmoothing = 0.3      // 30% path smoothing

// Visualization settings
cfg.EnableFlowVisualization = true
cfg.FlowStreamlineCount = 20       // 20 streamlines
cfg.FlowVectorVisualization = true // Show flow vectors
```

### Water Configuration Defaults
The `WaterConfig()` function provides optimized settings for water simulations:
- Stream flow with parabolic velocity profiles
- Moderate turbulence (10% intensity)
- Meandering stream paths with realistic curvature
- Full visualization enabled with streamlines and vectors
- Performance-optimized update intervals

## File Organization and Project Structure

### Updated Directory Structure
```
internal/
├── vector/              # 3D vector mathematics
├── particle/           # Particle data structures
├── config/            # Configuration system
├── simulation/        # Main SPH algorithm
├── kernel/           # SPH kernel functions (validated)
├── spatial/          # Spatial hashing
├── validation/       # Kernel validation suite
├── boundary/         # Boundary condition system
│   ├── boundary.go        # Core boundary types and structures
│   └── boundary_impl.go   # Boundary implementation methods
└── flow/             # Stream flow system
    ├── flow.go            # Core flow field management
    ├── flow_impl.go       # Flow calculation implementations
    ├── path.go            # Stream path generation
    └── visualization.go   # Flow visualization system

cmd/
├── kernel_validation/   # Kernel validation tool
├── boundary_validation/ # Boundary conditions validation
├── flow_validation/     # Flow system validation
└── spatial_hash_test/   # Spatial hashing test suite
```

### Key Flow System Files
- `internal/flow/flow.go`: Core flow field and system management
- `internal/flow/flow_impl.go`: Flow calculations, turbulence, vorticity
- `internal/flow/path.go`: Stream path generation with meandering
- `internal/flow/visualization.go`: Streamlines and flow visualization
- `cmd/flow_validation/main.go`: Complete flow system validation

## Performance Guidelines

### Flow System Optimization
1. **Grid Resolution**: Balance accuracy vs performance (typical: 20x20x10)
2. **Update Frequency**: Full flow updates every step for dynamic flows
3. **Visualization Updates**: Reduce to 30 FPS for interactive performance
4. **Memory Management**: Use object pooling for temporary flow structures

### Turbulence Optimization
- Cache noise calculations when possible
- Use lower octave counts for real-time applications
- Pre-compute noise gradients for vorticity calculations
- Limit turbulence to active flow regions

### Streamline Optimization
- Use adaptive step sizing for RK4 integration
- Terminate early at stagnation points or boundaries
- Limit maximum streamline length
- Update seed points only when flow changes significantly

## Integration Patterns

### SPH-Flow Integration
```go
// Initialize flow system in SPH simulation
if cfg.EnableFlowSystem {
    sim.flowSystem = flow.NewFlowSystem(cfg)
    sim.flowVisualizer = flow.NewFlowVisualizer(cfg, sim.flowSystem)
}

// Update flow in simulation step
if sim.flowSystem != nil {
    sim.flowSystem.UpdateFlow(dt)
    sim.flowSystem.ApplyFlowForces(sim.particles)
}
```

### Boundary-Flow Integration
```go
// Stream boundaries work with flow system
if cfg.EnableStreamPath && cfg.BoundaryTypeStreambed {
    // Streambed boundaries align with flow direction
    // Flow rate affects boundary particle generation
}
```

## Validation and Testing Guidelines

### Comprehensive Validation
```bash
# Run all validation systems
./kernel-validation --quick --verbose    # SPH kernels
./boundary-validation --config=water     # Boundary conditions
./flow-validation --config=water         # Flow system

# All should achieve 100% success rate
```

### Development Workflow
1. **Kernel Validation**: Ensure SPH kernels are accurate
2. **Boundary Validation**: Verify boundary conditions work
3. **Flow Validation**: Test flow system components
4. **Integration Testing**: Run complete simulation tests
5. **Performance Profiling**: Benchmark critical components

### Quality Metrics
- **SPH Kernels**: 13/13 tests passed, >50K ops/s
- **Boundary System**: 8/8 tests passed, proper force integration
- **Flow System**: 10/10 tests passed, >100 updates/s
- **Overall Simulation**: Stable for >1000 steps, realistic physics

## Critical Implementation Notes

### Flow System Validation
- **Always run flow validation** after flow modifications
- **10/10 tests must pass** for production readiness
- **Performance benchmarks** must meet minimum thresholds
- **Integration tests** verify SPH compatibility

### Stream Flow Physics
- **Maintain mass conservation** in flow rate control
- **Ensure energy conservation** in turbulence generation
- **Preserve momentum** in velocity profile calculations
- **Respect physical constraints** (water flows downhill)

### Visualization Performance
- **Limit streamline count** for interactive performance
- **Use level-of-detail** for complex flow visualizations
- **Cache unchanged data** to avoid redundant calculations
- **Optimize color mapping** for smooth gradients

This file should be updated as the project evolves and new flow patterns emerge.