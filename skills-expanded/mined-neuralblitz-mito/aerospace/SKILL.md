---

## name: aerospace
description: >
  Aerospace expert for aircraft, spacecraft, and aviation technology. Use this skill whenever
  the user needs: understanding aerospace systems, working with flight mechanics, analyzing
  propulsion systems, studying aerospace materials, or any task involving aircraft and
  spacecraft design, operation, or analysis. This skill covers aeronautics, astronautics,
  propulsion, structures, and aerospace applications.
license: MIT
compatibility: opencode
metadata:
  audience: engineers
  category: engineering

# Aerospace — Aircraft and Space Systems

Covers: **Flight Mechanics · Propulsion · Aerodynamics · Structures · Avionics · Space Systems · Materials · Regulations**

-----

## Flight Mechanics

### Basic Flight Equations

```python
# Lift equation
def lift_equation(rho, V, S, Cl):
    """
    Calculate lift force.
    rho: Air density (kg/m³)
    V: Velocity (m/s)
    S: Wing area (m²)
    Cl: Lift coefficient
    """
    return 0.5 * rho * V**2 * S * Cl

# Drag equation
def drag_equation(rho, V, S, Cd):
    """
    Calculate drag force.
    """
    return 0.5 * rho * V**2 * S * Cd

# Thrust equation (ideal)
def thrust_ideal(m_dot, Ve, p_e, p0):
    """
    Calculate ideal thrust.
    m_dot: Mass flow rate (kg/s)
    Ve: Exit velocity (m/s)
    p_e: Exit pressure (Pa)
    p0: Ambient pressure (Pa)
   Ae: Exit area (m²)
    """
    return m_dot * Ve + (p_e - p0) * Ae

# Weight and balance
def center_of_gravity(masses, positions):
    """
    Calculate CG location.
    """
    total_mass = sum(m['mass'] for m in masses)
    total_moment = sum(m['mass'] * m['position'] for m in masses)
    return total_moment / total_moment
```

### Atmosphere and Air Properties

```python
# Standard atmosphere (ISA)
class StandardAtmosphere:
    def __init__(self, altitude=0):
        self.altitude = altitude  # meters
        self.sea_level_temp = 288.15  # K
        self.sea_level_pressure = 101325  # Pa
        self.sea_level_density = 1.225  # kg/m³
        self.lapse_rate = -0.0065  # K/m (troposphere)
        self.tropoause_altitude = 11000  # m
    
    def temperature(self):
        """Temperature at altitude (ISA)"""
        if self.altitude <= self.tropoause_altitude:
            return self.sea_level_temp + self.lapse_rate * self.altitude
        else:
            return 216.65  # Constant in stratosphere
    
    def pressure(self):
        """Pressure at altitude"""
        T = self.temperature()
        if self.altitude <= self.tropoause_altitude:
            return self.sea_level_pressure * (T / self.sea_level_temp) ** 5.2561
        else:
            p_trop = self.sea_level_pressure * (216.65 / 288.15) ** 5.2561
            return p_trop * np.exp(-(self.altitude - 11000) / 8500)
    
    def density(self):
        """Density at altitude"""
        return self.pressure() / (287.05 * self.temperature())

# Speed of sound
def speed_of_sound(T):
    """
    Calculate speed of sound.
    T: Temperature (K)
    gamma: Ratio of specific heats (1.4 for air)
    R: Gas constant (287 J/kg·K)
    """
    gamma = 1.4
    R = 287
    return np.sqrt(gamma * R * T)

# Mach number
def mach_number(V, altitude):
    """Calculate Mach number"""
    a = speed_of_sound(StandardAtmosphere(altitude).temperature())
    return V / a
```

### Aircraft Performance

```python
# Range and endurance
class AircraftPerformance:
    @staticmethod
    def range_brequet(V, Cl_Cd, m_fuel, SFC):
        """
        Breguet range equation.
        V: Velocity
        Cl/Cd: Lift to drag ratio
        m_fuel: Fuel mass
        SFC: Specific fuel consumption
        """
        return (V * Cl_Cd / SFC) * np.log(1 + m_fuel)
    
    @staticmethod
    def endurance(Cl_Cd, m_fuel, SFC):
        """
        Breguet endurance equation.
        """
        return (Cl_Cd / SFC) * np.log(1 + m_fuel)
    
    @staticmethod
    def stall_speed(m, S, rho, Cl_max):
        """
        Calculate stall speed.
        """
        return np.sqrt(2 * m * 9.81 / (rho * S * Cl_max))

# Takeoff and landing distances
takeoff_landing = {
    'takeoff': {
        'phases': ['Ground roll', 'Rotation', 'Transition', 'Climb'],
        'factors': ['Temperature', 'Altitude', 'Wind', 'Runway condition']
    },
    'landing': {
        'phases': ['Approach', 'Flare', 'Touchdown', 'Braking', 'Rollout'],
        'factors': ['Weight', 'Wind', 'Brake capacity', 'Reverse thrust']
    }
}
```

-----

## Aerodynamics

### Airfoil Theory

```python
# Thin airfoil theory
class Airfoil:
    def __init__(self, chord, thickness, camber):
        self.chord = chord
        self.thickness = thickness  # % chord
        self.camber = camber       # % chord
    
    def lift_coefficient(self, alpha):
        """
        Lift coefficient for thin airfoil.
        alpha: Angle of attack (radians)
        """
        Cl_alpha = 2 * np.pi  # Theoretical lift curve slope
        Cl0 = 2 * np.pi * self.camber / self.chord  # Zero-lift angle
        return Cl_alpha * (alpha - Cl0)
    
    def pressure_distribution(self, x, alpha):
        """
        Simplified pressure distribution.
        """
        # Using thin airfoil theory
        pass

# Lift curve slope
lift_curve = {
    'theoretical': '2π per radian (thin airfoil)',
    'finite_wing': '2π / (1 + 2/AR) (Prandtl)',
    'three_dimensional': 'cl_alpha_3d = cl_alpha_2d / (1 + cl_alpha_2d/(π*e*AR))',
    'typical_values': '5.5-6.5 per radian for typical aircraft'
}

# Drag polar
def drag_polar(Cl, Cd0, K):
    """
    Parasitic drag plus induced drag.
    Cd0: Zero-lift drag coefficient
    K: Induced drag factor (1/(π*e*AR))
    """
    return Cd0 + K * Cl**2
```

### Wing Design

```python
# Wing geometry
wing_parameters = {
    'aspect_ratio': 'b²/S (span²/wing area)',
    'taper_ratio': 'Ct/Cr (tip chord/root chord)',
    'sweep_angle': 'Angle from perpendicular to LE',
    'dihedral': 'Upward angle of wing',
    'washout': 'Twist to reduce tip stall'
}

# Lift distribution (Prandtl)
def elliptical_lift_distribution(chord, span, Cl):
    """
    Elliptical lift distribution.
    """
    b = span
    S = np.pi * (span/2) * chord
    Cl_distribution = Cl * np.sqrt(1 - (2*y/span)**2)
    return Cl_distribution
```

### High-Speed Aerodynamics

```python
# Compressible flow corrections
def compressible_correction(M, beta=None):
    """
    Prandtl-Glauert correction for compressibility.
    """
    if M < 1:
        # Subsonic
        return 1 / np.sqrt(1 - M**2)
    else:
        return 1 / np.sqrt(M**2 - 1)

# Critical Mach number
def critical_mach(Cl, Cd0, M_cruise, A):
    """
    Estimate critical Mach number.
    """
    # Approximate formula
    M_cr = M_cruise - 0.1  # Simplified
    return M_cr

# Wave drag
wave_drag = {
    'transonic': 'Mach 0.8-1.2, rapid drag rise',
    'supersonic': 'Mach > 1, wave drag dominant',
    'drag_divergence': 'Mach where drag increases rapidly',
    'supersonic_lift': 'Lift-dependent wave drag'
}
```

-----

## Propulsion

### Jet Engine Fundamentals

```python
# Turbofan engine cycle
class TurbofanEngine:
    def __init__(self, bypass_ratio, overall_pressure_ratio, turbine_temp):
        self.bpr = bypass_ratio
        self.opr = overall_pressure_ratio
        self.tt = turbine_temp  # Turbine inlet temperature (K)
    
    def thermal_efficiency(self):
        """Carnot-like efficiency"""
        Tt4 = self.tt
        Tt0 = 288  # Ambient temperature
        return 1 - (Tt0 / Tt4)
    
    def propulsive_efficiency(self):
        """Propulsive efficiency"""
        V0 = 250  # Flight velocity (m/s)
        Ve = V0 * 1.5  # Exit velocity (simplified)
        return 2 / (1 + Ve/V0)

# Engine components
engine_components = {
    'intake': 'Ram compression at high speed',
    'compressor': 'Raises pressure (centrifugal or axial)',
    'combustor': 'Adds energy (constant pressure)',
    'turbine': 'Extracts energy for compressor',
    'nozzle': 'Accelerates exhaust'
}

# Specific thrust and fuel consumption
def engine_performance(m_dot, F, sfc):
    """
    m_dot: Air mass flow
    F: Thrust
    sfc: Specific fuel consumption
    """
    thrust_per_airflow = F / m_dot
    return thrust_per_airflow, sfc
```

### Rocket Propulsion

```python
# Rocket equation
def rocket_delta_v(ve, m0, mf):
    """
    Tsiolkovsky rocket equation.
    ve: Effective exhaust velocity
    m0: Initial mass
    mf: Final mass
    """
    return ve * np.log(m0 / mf)

# Specific impulse
def specific_impulse(ve, g0=9.81):
    """
    Isp = ve/g0 (seconds)
    """
    return ve / g0

# Propellant types
propellant_types = {
    'liquid': {
        'oxidizer': 'LOX, N2O4, H2O2',
        'fuel': 'LH2, RP-1, kerosene',
        'examples': 'SpaceX Merlin, RS-25'
    },
    'solid': {
        'composition': 'Ammonium perchlorate + aluminum + binder',
        'examples': 'SRB, tactical missiles'
    },
    'hybrid': {
        'fuel': 'Solid',
        'oxidizer': 'Liquid or gas',
        'examples': 'SpaceShipOne'
    },
    'electric': {
        'type': 'Ion, Hall effect',
        'examples': 'Deep Space 1, Dawn'
    }
}
```

-----

## Aerospace Structures

### Materials

```python
# Material properties
aerospace_materials = {
    'aluminum_alloys': {
        'examples': ['2024', '7075', '6061'],
        'strength': 'High',
        'weight': 'Low',
        'uses': 'Primary structure, skin'
    },
    'titanium_alloys': {
        'examples': ['Ti-6Al-4V'],
        'strength': 'Very high',
        'weight': 'Moderate',
        'uses': 'Engine components, high-stress'
    },
    'composites': {
        'carbon_fiber': {
            'strength': 'Very high',
            'weight': 'Very low',
            'uses': 'Wing, fuselage panels'
        },
        'glass_fiber': {
            'strength': 'High',
            'weight': 'Low',
            'uses': 'Non-critical surfaces'
        }
    },
    'superalloys': {
        'examples': ['Inconel', 'Waspaloy'],
        'temperature': 'High temperature capability',
        'uses': 'Turbine blades, combustion chambers'
    }
}
```

### Structural Analysis

```python
# Stress and strain
def stress_strain(sigma, E):
    """
    Calculate strain from stress.
    sigma: Stress (Pa)
    E: Young's modulus (Pa)
    """
    return sigma / E

# Buckling
def critical_buckling(P, L, E, I):
    """
    Euler buckling load.
    """
    return np.pi**2 * E * I / (L**2)

# Fatigue
fatigue_analysis = {
    's_n_diagram': 'Stress vs cycles to failure',
    'goodman': 'Mean stress correction',
    'miners_rule': 'Cumulative damage',
    'factors': ['Load spectrum', 'Material', 'Geometry', 'Environment']
}
```

-----

## Space Systems

### Orbital Mechanics

```python
# Orbital parameters
orbital_elements = {
    'semi_major_axis': 'Average distance from focus',
    'eccentricity': 'Orbit shape (0=circle)',
    'inclination': 'Angle from reference plane',
    'raan': 'Right ascension of ascending node',
    'argument_periapsis': 'Orientation of orbit in plane',
    'true_anomaly': 'Position in orbit'
}

# Orbital velocity
def orbital_velocity(mu, r):
    """
    Circular orbit velocity.
    mu: Gravitational parameter (GM)
    r: Orbital radius
    """
    return np.sqrt(mu / r)

# Orbital period
def orbital_period(a, mu):
    """
    a: Semi-major axis
    """
    return 2 * np.pi * np.sqrt(a**3 / mu)

# Hohmann transfer
def hohmann_transfer(r1, r2, mu):
    """
    Calculate Hohmann transfer velocities.
    """
    # Vis-viva equation
    v1 = np.sqrt(mu / r1) * (np.sqrt(2 * r2 / (r1 + r2)) - 1)
    v2 = np.sqrt(mu / r2) * (1 - np.sqrt(2 * r1 / (r1 + r2)))
    return v1, v2
```

### Spacecraft Systems

```python
# Subsystems
spacecraft_subsystems = {
    'power': ['Solar arrays', 'Batteries', 'RTG'],
    'thermal_control': ['Passive', 'Active (heat pipes)', 'Louvers'],
    'communication': ['Transponder', 'Antenna', 'Amplifier'],
    'attitude_control': ['Reaction wheels', 'Thrusters', 'Magnetorquers'],
    'propulsion': ['Chemical', 'Electric', 'Cold gas']
}

# Launch vehicles
launch_vehicle_classes = {
    'light': '< 2,000 kg to LEO',
    'medium': '2,000-20,000 kg to LEO',
    'heavy': '20,000-50,000 kg to LEO',
    'super_heavy': '> 50,000 kg to LEO'
}
```

-----

## Avionics and Systems

### Flight Controls

```python
# Control surfaces
control_surfaces = {
    'ailerons': 'Roll control',
    'elevator': 'Pitch control',
    'rudder': 'Yaw control',
    'flaps': 'High lift devices',
    'slats': 'Leading edge high lift',
    'spoilers': 'Speed brakes, lift dumpers'
}

# Fly-by-wire
fly_by_wire = {
    'description': 'Computer-controlled flight controls',
    'advantages': ['Envelope protection', 'Redundancy', 'Optimization'],
    'systems': ['Quadruple redundancy', 'Backup mechanical']
}
```

### Navigation

```python
# Navigation systems
navigation_systems = {
    'INS': 'Inertial Navigation System',
    'GPS': 'Global Positioning System',
    'VOR': 'VHF Omnidirectional Range',
    'ILS': 'Instrument Landing System',
    'DME': 'Distance Measuring Equipment'
}

# Flight instruments
flight_instruments = {
    'airdata': ['Airspeed', 'Altitude', 'Vertical speed'],
    'attitude': ['Artificial horizon', 'Turn coordinator'],
    'heading': ['Heading indicator', 'Magnetic compass'],
    'navigation': ['HSI', 'RMI']
}
```

-----

## Regulations and Standards

### Aviation Authorities

| Authority | Region | Role |
|-----------|--------|------|
| FAA | United States | Civil aviation regulation |
| EASA | Europe | European safety |
| ICAO | International | Standards and recommended practices |
| NASA | United States | Space exploration |
| CNSA | China | Chinese space program |

### Certification Levels

```python
certification_categories = {
    'aircraft': {
        'Normal': 'Private flying, no aerobatics',
        'Utility': 'Limited aerobatics',
        'Acrobatic': 'Full aerobatics',
        'Transport': 'Airline certification'
    },
    'parts': {
        'PMAs': 'Parts Manufacturer Approval',
        'STCs': 'Supplemental Type Certificates',
        'OEM': 'Original equipment manufacturer'
    }
}
```

-----

## Common Errors to Avoid

- **Ignoring atmospheric effects**: Density changes with altitude
- **Confusing velocity and Mach**: They are different measures
- **Neglecting structural limits**: Never exceed Vne
- **Underestimating fuel burn**: Always plan for reserves
- **Ignoring weight and balance**: CG must be within limits
- **Forgetting weather**: Weather affects all aspects of flight
- **Confusing thrust and power**: They are different concepts
- **Ignoring center of pressure**: Moves with angle of attack
- **Not understanding lift curve**: Stall and beyond
- **Neglecting regulations**: Always follow aviation authority rules
