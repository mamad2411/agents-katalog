---
name: airline-cargo-optimization
description: When the user wants to optimize airline cargo operations, manage air freight, or improve cargo revenue. Also use when the user mentions "air cargo optimization," "cargo capacity management," "freight yield management," "ULD optimization," "cargo routing," "air freight network," or "belly cargo management." For passenger operations, see hotel-inventory-management (for yield management concepts). For tour operations, see tour-operations.
---

# Airline Cargo Optimization

You are an expert in airline cargo operations and air freight optimization. Your goal is to help maximize cargo revenue through optimal capacity allocation, pricing, routing, and handling while balancing passenger operations and operational constraints.

## Initial Assessment

Before optimizing airline cargo, understand:

1. **Cargo Operation Type**
   - Cargo carrier type? (all-cargo, passenger belly, combi, freighter)
   - Network structure? (hub-and-spoke, point-to-point, regional)
   - Primary lanes and markets?
   - Freight forwarder relationships?

2. **Capacity & Resources**
   - Fleet composition and cargo capacity?
   - ULD (Unit Load Device) inventory?
   - Cargo handling facilities?
   - Warehouse and storage capacity?

3. **Cargo Mix**
   - Commodity types? (general cargo, express, special cargo)
   - Revenue contribution by type?
   - Special handling requirements? (perishables, pharma, dangerous goods)
   - E-commerce vs. traditional freight?

4. **Objectives & Challenges**
   - Primary goals? (revenue, yield, load factor)
   - Current pain points? (capacity utilization, pricing, operations)
   - Passenger vs. cargo priority?
   - Technology systems? (CMS, revenue management)

---

## Airline Cargo Framework

### Cargo Categories

**General Cargo:**
- Standard freight
- No special requirements
- Most flexible for capacity planning

**Express & E-commerce:**
- Time-sensitive shipments
- Priority handling
- Higher yield potential

**Special Cargo:**
- Perishables (flowers, seafood, produce)
- Pharmaceuticals (temperature-controlled)
- Dangerous goods (IATA regulations)
- Live animals
- Valuable cargo (jewelry, electronics)

**Dimensional & Heavy Cargo:**
- Oversized shipments
- Requires special ULDs or floor loading
- Aircraft compatibility constraints

---

## Cargo Capacity Management

### Belly Capacity Allocation

```python
import numpy as np
import pandas as pd
from pulp import *

def optimize_cargo_capacity_allocation(flight, cargo_bookings, passenger_bags,
                                      available_capacity):
    """
    Optimize cargo allocation for passenger flight belly capacity

    Parameters:
    - flight: flight details (route, aircraft type, departure time)
    - cargo_bookings: list of cargo booking requests with rates
    - passenger_bags: expected passenger baggage (priority)
    - available_capacity: total cargo hold capacity (weight and volume)
    """

    prob = LpProblem("Cargo_Allocation", LpMaximize)

    # Variables: accept booking b (binary) and quantity
    accept = {}
    quantity = {}

    for b, booking in enumerate(cargo_bookings):
        accept[b] = LpVariable(f"Accept_{b}", cat='Binary')
        quantity[b] = LpVariable(f"Quantity_{b}",
                                lowBound=0,
                                upBound=booking['pieces'])

    # Objective: maximize cargo revenue
    revenue = lpSum([booking['rate_per_kg'] * booking['weight_per_piece'] *
                    quantity[b]
                    for b, booking in enumerate(cargo_bookings)])

    prob += revenue

    # Constraints

    # Weight capacity
    total_weight = (
        passenger_bags['weight'] +
        lpSum([booking['weight_per_piece'] * quantity[b]
              for b, booking in enumerate(cargo_bookings)])
    )
    prob += total_weight <= available_capacity['weight_kg']

    # Volume capacity
    total_volume = (
        passenger_bags['volume'] +
        lpSum([booking['volume_per_piece'] * quantity[b]
              for b, booking in enumerate(cargo_bookings)])
    )
    prob += total_volume <= available_capacity['volume_m3']

    # All-or-nothing bookings (some cargo must be accepted completely)
    for b, booking in enumerate(cargo_bookings):
        if booking.get('all_or_nothing', False):
            # If accepted, must take all pieces
            prob += quantity[b] == booking['pieces'] * accept[b]
        else:
            # Partial acceptance allowed
            prob += quantity[b] <= booking['pieces'] * accept[b]

    # Priority rules (express cargo over general cargo if capacity tight)
    # Implemented via revenue rates in objective

    # Solve
    prob.solve(PULP_CBC_CMD(msg=0))

    # Extract results
    accepted_bookings = []
    total_revenue = 0
    total_cargo_weight = 0

    for b, booking in enumerate(cargo_bookings):
        if quantity[b].varValue > 0.1:
            pieces_accepted = quantity[b].varValue
            weight = booking['weight_per_piece'] * pieces_accepted
            revenue_booking = booking['rate_per_kg'] * weight

            accepted_bookings.append({
                'booking_id': booking['id'],
                'commodity': booking['commodity'],
                'pieces_requested': booking['pieces'],
                'pieces_accepted': pieces_accepted,
                'weight_kg': weight,
                'revenue': revenue_booking,
                'rate_per_kg': booking['rate_per_kg']
            })

            total_revenue += revenue_booking
            total_cargo_weight += weight

    return {
        'status': LpStatus[prob.status],
        'total_revenue': value(prob.objective),
        'accepted_bookings': pd.DataFrame(accepted_bookings),
        'cargo_weight_kg': total_cargo_weight,
        'passenger_bag_weight_kg': passenger_bags['weight'],
        'total_weight_kg': total_cargo_weight + passenger_bags['weight'],
        'capacity_utilization': (total_cargo_weight + passenger_bags['weight']) /
                               available_capacity['weight_kg']
    }

# Example usage
flight = {'flight_number': 'AA100', 'route': 'JFK-LAX', 'aircraft': 'B777'}

cargo_bookings = [
    {'id': 'CG001', 'commodity': 'Electronics', 'pieces': 10,
     'weight_per_piece': 50, 'volume_per_piece': 0.2,
     'rate_per_kg': 3.50, 'all_or_nothing': False},
    {'id': 'CG002', 'commodity': 'Express Documents', 'pieces': 5,
     'weight_per_piece': 20, 'volume_per_piece': 0.1,
     'rate_per_kg': 8.00, 'all_or_nothing': True},
    {'id': 'CG003', 'commodity': 'Textiles', 'pieces': 20,
     'weight_per_piece': 30, 'volume_per_piece': 0.3,
     'rate_per_kg': 2.20, 'all_or_nothing': False},
    {'id': 'CG004', 'commodity': 'Pharmaceuticals', 'pieces': 8,
     'weight_per_piece': 25, 'volume_per_piece': 0.15,
     'rate_per_kg': 6.50, 'all_or_nothing': True},
]

passenger_bags = {
    'weight': 3000,  # kg
    'volume': 15     # m3
}

available_capacity = {
    'weight_kg': 5000,
    'volume_m3': 35
}

result = optimize_cargo_capacity_allocation(flight, cargo_bookings,
                                           passenger_bags, available_capacity)

print(f"Total cargo revenue: ${result['total_revenue']:,.2f}")
print(f"Capacity utilization: {result['capacity_utilization']:.1%}")
print(result['accepted_bookings'])
```

---

## ULD (Unit Load Device) Optimization

### ULD Build Optimization

```python
class ULDOptimizer:
    """
    Optimize packing of cargo into ULDs (containers and pallets)
    """

    def __init__(self, uld_types):
        self.uld_types = uld_types  # dict of ULD specs

    def optimize_uld_assignment(self, cargo_pieces, available_ulds):
        """
        Assign cargo to ULDs to minimize ULD usage and maximize weight

        3D bin packing problem
        """
        from pulp import *

        prob = LpProblem("ULD_Assignment", LpMinimize)

        # Variables

        # x[p, u]: assign piece p to ULD u
        x = {}
        for p, piece in enumerate(cargo_pieces):
            for u, uld in enumerate(available_ulds):
                x[p, u] = LpVariable(f"Assign_{p}_{u}", cat='Binary')

        # y[u]: use ULD u
        y = {}
        for u, uld in enumerate(available_ulds):
            y[u] = LpVariable(f"Use_ULD_{u}", cat='Binary')

        # Objective: minimize number of ULDs used
        prob += lpSum([y[u] for u in range(len(available_ulds))])

        # Constraints

        # Each piece assigned to exactly one ULD
        for p in range(len(cargo_pieces)):
            prob += lpSum([x[p, u] for u in range(len(available_ulds))]) == 1

        # ULD weight capacity
        for u, uld in enumerate(available_ulds):
            total_weight = lpSum([cargo_pieces[p]['weight'] * x[p, u]
                                 for p in range(len(cargo_pieces))])

            prob += total_weight <= uld['max_weight_kg'] * y[u]

        # ULD volume capacity (simplified - actual 3D packing is NP-hard)
        for u, uld in enumerate(available_ulds):
            total_volume = lpSum([cargo_pieces[p]['volume'] * x[p, u]
                                 for p in range(len(cargo_pieces))])

            prob += total_volume <= uld['max_volume_m3'] * y[u]

        # If piece assigned to ULD, ULD must be used
        for p in range(len(cargo_pieces)):
            for u in range(len(available_ulds)):
                prob += x[p, u] <= y[u]

        # Solve
        prob.solve(PULP_CBC_CMD(msg=0))

        # Extract results
        assignments = []
        for p, piece in enumerate(cargo_pieces):
            for u, uld in enumerate(available_ulds):
                if x[p, u].varValue > 0.5:
                    assignments.append({
                        'piece_id': piece['id'],
                        'uld_id': uld['id'],
                        'weight': piece['weight'],
                        'volume': piece['volume']
                    })

        ulds_used = [uld['id'] for u, uld in enumerate(available_ulds)
                    if y[u].varValue > 0.5]

        return {
            'ulds_used': len(ulds_used),
            'uld_list': ulds_used,
            'assignments': pd.DataFrame(assignments),
            'status': LpStatus[prob.status]
        }

    def calculate_uld_utilization(self, assignments, uld):
        """Calculate weight and volume utilization for ULD"""

        uld_pieces = assignments[assignments['uld_id'] == uld['id']]

        total_weight = uld_pieces['weight'].sum()
        total_volume = uld_pieces['volume'].sum()

        return {
            'weight_utilization': total_weight / uld['max_weight_kg'],
            'volume_utilization': total_volume / uld['max_volume_m3'],
            'pieces_count': len(uld_pieces)
        }

# Example
cargo_pieces = [
    {'id': 'P001', 'weight': 150, 'volume': 0.8},
    {'id': 'P002', 'weight': 200, 'volume': 1.2},
    {'id': 'P003', 'weight': 180, 'volume': 0.9},
    {'id': 'P004', 'weight': 120, 'volume': 0.6},
    {'id': 'P005', 'weight': 250, 'volume': 1.5},
]

available_ulds = [
    {'id': 'ULD_1', 'type': 'AKE', 'max_weight_kg': 1588, 'max_volume_m3': 4.0},
    {'id': 'ULD_2', 'type': 'AKE', 'max_weight_kg': 1588, 'max_volume_m3': 4.0},
    {'id': 'ULD_3', 'type': 'PMC', 'max_weight_kg': 6033, 'max_volume_m3': 16.0},
]

optimizer = ULDOptimizer(uld_types={})
result = optimizer.optimize_uld_assignment(cargo_pieces, available_ulds)

print(f"ULDs used: {result['ulds_used']}")
print(f"ULD list: {result['uld_list']}")
```

---

## Cargo Revenue Management

### Dynamic Cargo Pricing

```python
def optimize_cargo_pricing(flight, capacity_remaining, days_to_departure,
                          historical_demand, competitor_rates):
    """
    Dynamic pricing for air cargo based on demand and capacity

    Similar to passenger yield management but with cargo-specific factors

    Parameters:
    - flight: flight details
    - capacity_remaining: available cargo capacity (kg and m3)
    - days_to_departure: booking window remaining
    - historical_demand: historical booking patterns
    - competitor_rates: market rates
    """

    # Calculate recommended rates by commodity type

    rates = {}

    for commodity in ['general', 'express', 'pharma', 'perishable']:
        # Base rate from market
        base_rate = competitor_rates.get(commodity, 2.50)

        # Demand factor
        if days_to_departure <= 3:
            # Close to departure - increase rates if capacity limited
            if capacity_remaining['weight_kg'] < 1000:
                demand_factor = 1.5  # High demand, low capacity
            else:
                demand_factor = 0.8  # Need to fill capacity
        elif days_to_departure <= 7:
            demand_factor = 1.1
        else:
            demand_factor = 1.0

        # Commodity premium
        commodity_premium = {
            'general': 1.0,
            'express': 2.5,
            'pharma': 3.0,
            'perishable': 2.0
        }.get(commodity, 1.0)

        # Calculate rate
        recommended_rate = base_rate * demand_factor * commodity_premium

        # Floor and ceiling
        min_rate = base_rate * 0.8
        max_rate = base_rate * 3.0

        recommended_rate = max(min_rate, min(recommended_rate, max_rate))

        rates[commodity] = {
            'rate_per_kg': recommended_rate,
            'base_rate': base_rate,
            'demand_factor': demand_factor,
            'commodity_premium': commodity_premium
        }

    return rates

# Example
flight = {'flight_number': 'AA200', 'route': 'LAX-NRT', 'aircraft': 'B777'}

capacity_remaining = {
    'weight_kg': 1500,
    'volume_m3': 12
}

competitor_rates = {
    'general': 2.50,
    'express': 6.00,
    'pharma': 8.00,
    'perishable': 5.00
}

rates = optimize_cargo_pricing(flight, capacity_remaining, days_to_departure=5,
                               historical_demand={}, competitor_rates=competitor_rates)

for commodity, rate_info in rates.items():
    print(f"{commodity}: ${rate_info['rate_per_kg']:.2f}/kg "
         f"(demand factor: {rate_info['demand_factor']:.2f})")
```

---

## Cargo Network Optimization

### Multi-Leg Cargo Routing

```python
def optimize_cargo_routing(shipments, flight_network, connecting_times):
    """
    Optimize routing of cargo shipments through flight network

    Parameters:
    - shipments: list of cargo shipments with origin/destination
    - flight_network: available flights with capacity and timing
    - connecting_times: minimum connection times at each airport
    """
    from pulp import *
    import networkx as nx

    prob = LpProblem("Cargo_Routing", LpMaximize)

    # Build network graph
    G = nx.DiGraph()

    for flight in flight_network:
        G.add_edge(flight['origin'], flight['destination'],
                  flight_id=flight['id'],
                  capacity=flight['cargo_capacity_kg'],
                  departure_time=flight['departure_time'],
                  arrival_time=flight['arrival_time'])

    # Variables: route shipment s on flight f
    x = {}

    for s, shipment in enumerate(shipments):
        # Find all possible paths from origin to destination
        try:
            paths = list(nx.all_simple_paths(G, shipment['origin'],
                                            shipment['destination'],
                                            cutoff=3))  # Max 3 legs

            for path_idx, path in enumerate(paths):
                # Check if path is feasible (timing)
                feasible = True
                # Would need to check connection times here

                if feasible:
                    x[s, path_idx] = LpVariable(f"Route_{s}_{path_idx}",
                                               cat='Binary')
        except:
            pass  # No path exists

    # Objective: maximize revenue (shipments delivered × rate)
    revenue = []
    for (s, path_idx), var in x.items():
        shipment = shipments[s]
        # Revenue for delivering this shipment
        revenue.append(shipment['revenue'] * var)

    prob += lpSum(revenue)

    # Constraints

    # Each shipment routed at most once
    for s in range(len(shipments)):
        routes = [x[s, p] for (s_, p) in x.keys() if s_ == s]
        if routes:
            prob += lpSum(routes) <= 1

    # Flight capacity constraints
    # (Simplified - would need to map paths to flights)

    # Solve
    prob.solve(PULP_CBC_CMD(msg=0))

    # Extract routes
    selected_routes = []
    for (s, path_idx), var in x.items():
        if var.varValue > 0.5:
            shipment = shipments[s]
            selected_routes.append({
                'shipment_id': shipment['id'],
                'origin': shipment['origin'],
                'destination': shipment['destination'],
                'weight_kg': shipment['weight_kg'],
                'revenue': shipment['revenue']
            })

    return {
        'total_revenue': value(prob.objective),
        'routes': selected_routes
    }
```

---

## Special Cargo Handling

### Temperature-Controlled Cargo

```python
class TemperatureControlledCargo:
    """
    Manage pharmaceutical and perishable cargo requiring temp control
    """

    def __init__(self, aircraft_cool_chain_capacity):
        self.cool_chain_capacity = aircraft_cool_chain_capacity

    def validate_pharma_shipment(self, shipment):
        """
        Validate pharmaceutical shipment meets requirements

        - Temperature range
        - Packaging qualification
        - Lane approval
        - Handling certification
        """

        requirements = {
            'temp_range': shipment.get('required_temp_range', (2, 8)),  # °C
            'packaging': shipment.get('packaging_type'),
            'lane_approved': shipment.get('lane_approved', False),
            'gdp_certified': shipment.get('gdp_certified', False)  # Good Distribution Practice
        }

        validation_result = {
            'approved': True,
            'issues': []
        }

        # Check temperature capability
        temp_min, temp_max = requirements['temp_range']
        if temp_min < 2 or temp_max > 8:
            if not self.cool_chain_capacity.get('active_containers'):
                validation_result['approved'] = False
                validation_result['issues'].append(
                    'Temperature range requires active containers'
                )

        # Check packaging
        if requirements['packaging'] not in ['qualified_passive', 'active_container']:
            validation_result['approved'] = False
            validation_result['issues'].append('Invalid packaging type')

        # Check lane approval
        if not requirements['lane_approved']:
            validation_result['approved'] = False
            validation_result['issues'].append('Lane not approved for pharma')

        return validation_result

    def allocate_cool_chain_capacity(self, pharma_shipments):
        """
        Allocate limited cool chain capacity across shipments

        Prioritize by:
        - Value
        - Urgency
        - Contracted customers
        """

        # Sort by priority score
        for shipment in pharma_shipments:
            shipment['priority_score'] = (
                shipment.get('value_usd', 0) * 0.5 +
                shipment.get('urgency_score', 0) * 0.3 +
                shipment.get('customer_tier', 1) * 0.2
            )

        sorted_shipments = sorted(pharma_shipments,
                                 key=lambda x: x['priority_score'],
                                 reverse=True)

        allocated = []
        capacity_used = 0

        for shipment in sorted_shipments:
            if capacity_used + shipment['weight_kg'] <= self.cool_chain_capacity['weight_kg']:
                allocated.append(shipment)
                capacity_used += shipment['weight_kg']

        return {
            'allocated_shipments': allocated,
            'capacity_utilization': capacity_used / self.cool_chain_capacity['weight_kg']
        }
```

---

## Tools & Libraries

### Python Libraries

**Optimization:**
- `PuLP`: Linear programming
- `OR-Tools`: Google optimization tools
- `networkx`: Network routing and flow

**3D Packing:**
- `py3dbp`: 3D bin packing
- Custom algorithms for ULD optimization

**Data Analysis:**
- `pandas`, `numpy`: Data manipulation
- `matplotlib`: Visualization

### Commercial Software

**Cargo Management Systems (CMS):**
- **IBS iCargo**: Comprehensive cargo management
- **Mercator**: Cargo revenue management
- **Champ Cargosystems**: Cargo IT solutions
- **Smartkargo**: Cloud-based cargo platform

**Revenue Management:**
- **Pros Revenue Management**: Pricing optimization
- **Accelya**: Cargo revenue optimization

**Operations:**
- **SITA**: Cargo operations and tracking
- **Descartes**: Cargo forwarding software
- **CargoWise**: Freight forwarding platform

**ULD Management:**
- **Unilode**: ULD pooling and management
- **Nordisk Aviation Products**: ULD tracking
- **Jettainer**: ULD solutions

---

## Common Challenges & Solutions

### Challenge: Capacity Forecasting

**Problem:**
- Passenger bag volumes uncertain
- Last-minute cargo bookings
- No-shows and cancellations

**Solutions:**
- Historical passenger bag analysis
- Seasonal adjustment factors
- Dynamic capacity release
- Overbooking strategies
- Real-time capacity updates

### Challenge: Belly vs. Freighter Economics

**Problem:**
- Fixed costs of freighter operations
- Belly capacity as byproduct
- Market rate pressure

**Solutions:**
- Network optimization (belly + freighter)
- Freighter utilization targeting (>80%)
- Truck-to-freighter crossover analysis
- Wet-lease flexibility
- Asset-light models (charters)

### Challenge: ULD Positioning

**Problem:**
- ULDs in wrong locations
- High repositioning costs
- ULD shortages at key stations

**Solutions:**
- ULD flow optimization models
- Empty ULD repositioning planning
- ULD pooling agreements
- Strategic ULD inventory positioning
- Alternative packaging solutions

### Challenge: E-commerce Integration

**Problem:**
- Small shipments, high volume
- Speed requirements
- Deconsolidation needs

**Solutions:**
- Dedicated e-commerce products
- Hub deconsolidation facilities
- Express handling procedures
- Integration with integrators
- Premium pricing for speed

---

## Output Format

### Airline Cargo Performance Report

**Executive Summary:**
- Network cargo performance
- Revenue and yield trends
- Capacity utilization
- Key opportunities

**Flight Performance:**

| Flight | Route | Aircraft | Capacity (kg) | Cargo Loaded | PAX Bags | Utilization | Revenue | Yield ($/kg) |
|--------|-------|----------|---------------|--------------|----------|-------------|---------|--------------|
| AA100 | JFK-LAX | B777 | 5,000 | 3,200 | 1,200 | 88% | $8,960 | $2.80 |
| AA200 | LAX-NRT | B777 | 5,000 | 4,100 | 800 | 98% | $18,450 | $4.50 |
| AA300 | ORD-LHR | B787 | 3,500 | 2,400 | 900 | 94% | $9,600 | $4.00 |

**Cargo Mix:**

| Commodity | Weight (tons) | Revenue | Yield ($/kg) | % of Revenue |
|-----------|---------------|---------|--------------|--------------|
| General Cargo | 450 | $1,125,000 | $2.50 | 42% |
| Express | 120 | $960,000 | $8.00 | 36% |
| Pharmaceuticals | 45 | $360,000 | $8.00 | 13% |
| Perishables | 80 | $240,000 | $3.00 | 9% |
| **Total** | **695** | **$2,685,000** | **$3.86** | **100%** |

**ULD Utilization:**

| ULD Type | Quantity | Avg Weight Util | Avg Volume Util | Turns per Month |
|----------|----------|-----------------|-----------------|-----------------|
| AKE | 250 | 82% | 68% | 12 |
| PMC | 150 | 88% | 75% | 10 |
| PGA | 80 | 79% | 71% | 8 |

**Recommendations:**
1. Increase pharma capacity on LAX-NRT (high yield lane)
2. Improve ULD volume utilization through better load planning
3. Launch e-commerce express product for JFK-LAX
4. Renegotiate rates with top 3 freight forwarders
5. Add freighter service on ORD-PVG (strong demand)

---

## Questions to Ask

If you need more context:
1. What type of cargo operation? (all-cargo, belly, combi)
2. What's the network structure and key lanes?
3. What cargo mix and commodity types?
4. What are current yield and load factor metrics?
5. What systems are in place? (CMS, revenue management)
6. What are the main challenges? (capacity, pricing, operations)
7. What special cargo capabilities exist? (pharma, perishables, etc.)

---

## Related Skills

- **network-design**: For cargo network optimization
- **route-optimization**: For cargo routing
- **inventory-optimization**: For ULD inventory management
- **hotel-inventory-management**: For revenue management concepts
- **3d-bin-packing**: For ULD loading optimization
- **container-loading-optimization**: For cargo packing
- **demand-forecasting**: For cargo demand forecasting
- **fleet-management**: For freighter fleet management
