---
name: vehicle-loading-optimization
description: When the user wants to optimize truck loading, load delivery vehicles, or plan vehicle capacity utilization. Also use when the user mentions "truck loading," "delivery vehicle optimization," "van loading," "cargo van packing," "multi-drop vehicle loading," "delivery route loading," "axle weight distribution," or "vehicle utilization." For container loading, see container-loading-optimization. For route optimization, see route-optimization.
---

# Vehicle Loading Optimization

You are an expert in vehicle loading optimization and logistics. Your goal is to help efficiently load trucks, vans, and delivery vehicles while maximizing utilization, ensuring safety, meeting weight constraints, and accommodating multi-stop delivery sequences.

## Initial Assessment

Before optimizing vehicle loading, understand:

1. **Vehicle Specifications**
   - Vehicle type? (box truck, van, semi-trailer, flatbed)
   - Cargo area dimensions: length x width x height
   - Weight capacity (GVWR - vehicle weight)
   - Axle weight limits (front/rear distribution)
   - Door configuration (rear, side, roll-up)?

2. **Cargo Characteristics**
   - Palletized, boxed, or loose cargo?
   - Pallet/package dimensions and weights
   - How many items/orders to load?
   - Stackability and fragility
   - Special handling requirements?

3. **Delivery Requirements**
   - Single destination or multi-stop route?
   - Delivery sequence (LIFO/FIFO)?
   - Unloading access (rear only, side door)?
   - Time windows at delivery locations?
   - Customer-specific requirements?

4. **Loading Constraints**
   - Weight distribution requirements
   - Axle weight limits for road compliance
   - Securing requirements (straps, nets, bars)
   - Climate control zones?
   - Hazmat separation rules?

5. **Optimization Goals**
   - Maximize vehicle utilization?
   - Minimize number of vehicles?
   - Ensure easy unloading sequence?
   - Balance weight distribution?
   - Minimize loading/unloading time?

---

## Vehicle Loading Framework

### Common Vehicle Types

**Cargo Van**
- Typical: Ford Transit, Mercedes Sprinter
- Cargo: 10-14ft L x 6ft W x 6ft H
- Capacity: 3,000-4,500 lbs
- Use: Last-mile delivery, service calls

**Box Truck (10-16ft)**
- Typical: 14ft box truck
- Cargo: 14ft L x 7ft W x 7ft H
- Capacity: 3,000-5,000 lbs
- Use: Local delivery, moving

**Box Truck (20-26ft)**
- Typical: 26ft box truck
- Cargo: 26ft L x 8ft W x 8ft H
- Capacity: 10,000-15,000 lbs
- Use: Regional delivery, freight

**Semi-Trailer (Dry Van)**
- Typical: 53ft trailer
- Cargo: 53ft L x 8.5ft W x 9ft H
- Capacity: 40,000-45,000 lbs
- Use: Long-haul, FTL shipments

### Key Loading Principles

**1. Axle Weight Distribution**
- Front axle: 12,000-13,000 lbs max (varies by state)
- Rear axle(s): 34,000 lbs max
- Gross Vehicle Weight Rating (GVWR): varies
- Target: 40% front, 60% rear (general rule)

**2. Load Sequence for Multi-Stop**
- Last stop items loaded first (LIFO)
- Accessible from door for each stop
- Zone-based loading by delivery sequence
- Minimize handling at each stop

**3. Weight Distribution**
- Heavy items at bottom, centered
- Distribute weight evenly side-to-side
- Avoid concentrated loads
- Balance front-to-back

**4. Load Securing**
- Prevent shifting during transport
- Use load bars, straps, or airbags
- Comply with DOT cargo securement rules
- Protect fragile items

---

## Mathematical Formulation

### Vehicle Loading Problem

**Decision Variables:**
- x_i, y_i, z_i = position of item i in vehicle
- v_i = vehicle assigned to item i
- s_i = delivery stop for item i
- used_j = 1 if vehicle j is used

**Objective Functions:**

1. **Minimize vehicles:**
   Minimize Σ used_j

2. **Maximize utilization:**
   Maximize (Σ volume_loaded) / (Σ vehicle_capacity)

3. **Minimize handling:**
   Minimize unloading moves at each stop

**Constraints:**
1. Vehicle capacity (volume and weight)
2. Axle weight limits
3. Loading sequence (multi-stop accessibility)
4. Weight distribution balance
5. Securing and safety requirements
6. Item compatibility

---

## Algorithms and Solution Methods

### Single-Stop Vehicle Loading

```python
class SingleStopVehicleLoader:
    """
    Optimize loading for single-destination delivery

    Uses 3D bin packing with vehicle-specific constraints
    """

    def __init__(self, vehicle_length, vehicle_width, vehicle_height,
                 weight_capacity, front_axle_limit=13000, rear_axle_limit=34000):
        """
        Initialize vehicle loader

        Parameters:
        - vehicle_length, vehicle_width, vehicle_height: cargo area dimensions (inches)
        - weight_capacity: max payload weight (lbs)
        - front_axle_limit, rear_axle_limit: axle weight limits (lbs)
        """

        self.vehicle_dims = (vehicle_length, vehicle_width, vehicle_height)
        self.weight_capacity = weight_capacity
        self.front_axle_limit = front_axle_limit
        self.rear_axle_limit = rear_axle_limit

        self.items = []
        self.solution = None

    def add_item(self, length, width, height, weight, item_id=None):
        """Add item to load"""
        if item_id is None:
            item_id = f"Item_{len(self.items)}"

        self.items.append({
            'id': item_id,
            'dims': (length, width, height),
            'weight': weight
        })

    def optimize_loading(self, algorithm='weight_balanced'):
        """
        Optimize vehicle loading

        Algorithms:
        - 'weight_balanced': Prioritize weight distribution
        - 'space_efficient': Maximize space utilization
        - 'easy_unload': Place items for easy access
        """

        L, W, H = self.vehicle_dims

        if algorithm == 'weight_balanced':
            # Sort by weight (heaviest first)
            sorted_items = sorted(self.items,
                                 key=lambda x: x['weight'],
                                 reverse=True)
        elif algorithm == 'space_efficient':
            # Sort by volume
            sorted_items = sorted(self.items,
                                 key=lambda x: x['dims'][0] * x['dims'][1] * x['dims'][2],
                                 reverse=True)
        else:
            sorted_items = self.items

        loaded_items = []
        current_weight = 0

        # Simple layer-based loading
        current_y = 0
        current_z = 0
        current_x = 0

        for item in sorted_items:
            l, w, h = item['dims']
            weight = item['weight']

            # Check weight
            if current_weight + weight > self.weight_capacity:
                continue  # Skip item if too heavy

            # Try to place item
            if current_x + l <= L:
                # Place in current row
                loaded_items.append({
                    'item': item,
                    'position': (current_x, current_y, current_z),
                    'dims': (l, w, h)
                })
                current_x += l
                current_weight += weight

            elif current_y + w <= W:
                # Start new row
                current_x = 0
                current_y += w
                loaded_items.append({
                    'item': item,
                    'position': (current_x, current_y, current_z),
                    'dims': (l, w, h)
                })
                current_x += l
                current_weight += weight

            elif current_z + h <= H:
                # Start new layer
                current_x = 0
                current_y = 0
                current_z += h
                loaded_items.append({
                    'item': item,
                    'position': (current_x, current_y, current_z),
                    'dims': (l, w, h)
                })
                current_x += l
                current_weight += weight

        # Check axle weights
        axle_check = self.check_axle_weights(loaded_items)

        self.solution = {
            'loaded_items': loaded_items,
            'total_weight': current_weight,
            'items_loaded': len(loaded_items),
            'items_not_loaded': len(self.items) - len(loaded_items),
            'utilization': self.calculate_utilization(loaded_items),
            'axle_weights': axle_check
        }

        return self.solution

    def check_axle_weights(self, loaded_items):
        """
        Calculate axle weight distribution

        Assumes:
        - Front axle at 0 (front of vehicle)
        - Rear axle at 60% of vehicle length
        """

        L = self.vehicle_dims[0]
        rear_axle_position = L * 0.6

        front_axle_weight = 0
        rear_axle_weight = 0

        for item_data in loaded_items:
            pos = item_data['position']
            dims = item_data['dims']
            weight = item_data['item']['weight']

            # Calculate center of mass
            com_x = pos[0] + dims[0] / 2

            # Distance from axles
            distance_from_rear = rear_axle_position - com_x

            if distance_from_rear > 0:
                # Weight forward of rear axle - distributes to both
                front_ratio = distance_from_rear / rear_axle_position
                front_axle_weight += weight * front_ratio
                rear_axle_weight += weight * (1 - front_ratio)
            else:
                # Weight behind rear axle - all on rear
                rear_axle_weight += weight

        return {
            'front_axle': front_axle_weight,
            'rear_axle': rear_axle_weight,
            'front_limit': self.front_axle_limit,
            'rear_limit': self.rear_axle_limit,
            'front_ok': front_axle_weight <= self.front_axle_limit,
            'rear_ok': rear_axle_weight <= self.rear_axle_limit,
            'balanced': abs(front_axle_weight - rear_axle_weight) / (front_axle_weight + rear_axle_weight) < 0.3
        }

    def calculate_utilization(self, loaded_items):
        """Calculate volume utilization"""
        L, W, H = self.vehicle_dims
        vehicle_volume = L * W * H

        loaded_volume = sum(
            item_data['dims'][0] * item_data['dims'][1] * item_data['dims'][2]
            for item_data in loaded_items
        )

        return (loaded_volume / vehicle_volume * 100) if vehicle_volume > 0 else 0

    def print_solution(self):
        """Print loading solution"""
        if not self.solution:
            print("No solution available")
            return

        print("=" * 70)
        print("VEHICLE LOADING SOLUTION")
        print("=" * 70)
        print(f"Vehicle: {self.vehicle_dims[0]}L x {self.vehicle_dims[1]}W x {self.vehicle_dims[2]}H in")
        print(f"Weight Capacity: {self.weight_capacity:,} lbs")
        print()
        print(f"Items Loaded: {self.solution['items_loaded']} / {len(self.items)}")
        print(f"Total Weight: {self.solution['total_weight']:,} lbs")
        print(f"Utilization: {self.solution['utilization']:.1f}%")
        print()
        print("Axle Weight Distribution:")
        axle = self.solution['axle_weights']
        print(f"  Front Axle: {axle['front_axle']:,.0f} lbs "
              f"({'OK' if axle['front_ok'] else 'OVER LIMIT'})")
        print(f"  Rear Axle: {axle['rear_axle']:,.0f} lbs "
              f"({'OK' if axle['rear_ok'] else 'OVER LIMIT'})")
        print(f"  Balanced: {'Yes' if axle['balanced'] else 'No - adjust load'}")


# Example usage
if __name__ == "__main__":
    # 26ft box truck
    loader = SingleStopVehicleLoader(
        vehicle_length=312,  # 26ft in inches
        vehicle_width=96,    # 8ft
        vehicle_height=96,   # 8ft
        weight_capacity=10000  # lbs
    )

    # Add items
    loader.add_item(48, 40, 60, 800, "Pallet_1")
    loader.add_item(48, 40, 50, 700, "Pallet_2")
    loader.add_item(48, 40, 55, 750, "Pallet_3")
    loader.add_item(36, 30, 40, 500, "Box_1")
    loader.add_item(36, 30, 40, 500, "Box_2")

    # Optimize
    solution = loader.optimize_loading(algorithm='weight_balanced')
    loader.print_solution()
```

### Multi-Stop Vehicle Loading

```python
class MultiStopVehicleLoader:
    """
    Optimize vehicle loading for multi-stop delivery routes

    Ensures items are accessible in delivery sequence
    """

    def __init__(self, vehicle_dims, weight_capacity):
        self.vehicle_dims = vehicle_dims
        self.weight_capacity = weight_capacity
        self.stops = []  # List of delivery stops
        self.solution = None

    def add_stop(self, stop_id, items, delivery_sequence):
        """
        Add delivery stop with items

        Parameters:
        - stop_id: stop identifier
        - items: list of item dicts with 'dims' and 'weight'
        - delivery_sequence: order in route (1, 2, 3, ...)
        """

        self.stops.append({
            'id': stop_id,
            'items': items,
            'sequence': delivery_sequence
        })

    def optimize_loading(self):
        """
        Optimize loading for multi-stop delivery

        Strategy:
        - Zone vehicle by delivery sequence
        - Last stop loaded first (at door)
        - Earlier stops loaded deeper in vehicle
        """

        # Sort stops by reverse delivery sequence
        sorted_stops = sorted(self.stops,
                            key=lambda s: s['sequence'],
                            reverse=True)

        L, W, H = self.vehicle_dims

        # Calculate zones
        num_stops = len(sorted_stops)
        zone_length = L / num_stops

        zones = []
        current_weight = 0

        for idx, stop in enumerate(sorted_stops):
            zone_start = idx * zone_length
            zone_end = (idx + 1) * zone_length

            zone_items = []

            # Load items for this stop in this zone
            for item in stop['items']:
                if current_weight + item['weight'] <= self.weight_capacity:
                    # Simple placement (could be more sophisticated)
                    zone_items.append({
                        'item': item,
                        'stop_id': stop['id'],
                        'zone': (zone_start, zone_end)
                    })
                    current_weight += item['weight']

            zones.append({
                'stop': stop,
                'zone': (zone_start, zone_end),
                'items': zone_items
            })

        self.solution = {
            'zones': zones,
            'total_weight': current_weight,
            'stops_loaded': len(zones),
            'total_items': sum(len(z['items']) for z in zones)
        }

        return self.solution

    def print_solution(self):
        """Print multi-stop loading plan"""
        if not self.solution:
            print("No solution available")
            return

        print("=" * 70)
        print("MULTI-STOP VEHICLE LOADING PLAN")
        print("=" * 70)
        print(f"Total Weight: {self.solution['total_weight']:,} lbs")
        print(f"Stops: {self.solution['stops_loaded']}")
        print(f"Total Items: {self.solution['total_items']}")
        print()

        for zone_data in self.solution['zones']:
            stop = zone_data['stop']
            zone = zone_data['zone']
            print(f"Stop {stop['sequence']}: {stop['id']}")
            print(f"  Zone: {zone[0]:.0f}-{zone[1]:.0f} inches from front")
            print(f"  Items: {len(zone_data['items'])}")
            print()
```

### Fleet Loading Optimization

```python
def optimize_fleet_loading(orders, vehicles):
    """
    Optimize loading across multiple vehicles

    Assigns orders to vehicles to minimize:
    - Number of vehicles used
    - Total distance traveled
    - Loading/unloading complexity

    Parameters:
    - orders: list of order dicts with items, destination, priority
    - vehicles: list of available vehicle specs

    Returns: assignment of orders to vehicles
    """

    from pulp import *

    n_orders = len(orders)
    n_vehicles = len(vehicles)

    # Create problem
    prob = LpProblem("Fleet_Loading", LpMinimize)

    # Decision variables
    # x[i,j] = 1 if order i assigned to vehicle j
    x = LpVariable.dicts("assign",
                        [(i, j) for i in range(n_orders) for j in range(n_vehicles)],
                        cat='Binary')

    # y[j] = 1 if vehicle j is used
    y = LpVariable.dicts("use_vehicle", range(n_vehicles), cat='Binary')

    # Objective: Minimize vehicles used + routing cost
    prob += lpSum([y[j] * vehicles[j]['cost']
                   for j in range(n_vehicles)]), "Total_Cost"

    # Constraints

    # 1. Each order assigned to exactly one vehicle
    for i in range(n_orders):
        prob += lpSum([x[i,j] for j in range(n_vehicles)]) == 1, f"Order_{i}"

    # 2. Vehicle capacity (weight)
    for j in range(n_vehicles):
        prob += (lpSum([orders[i]['weight'] * x[i,j] for i in range(n_orders)]) <=
                vehicles[j]['weight_capacity']), f"Weight_{j}"

    # 3. Vehicle capacity (volume)
    for j in range(n_vehicles):
        prob += (lpSum([orders[i]['volume'] * x[i,j] for i in range(n_orders)]) <=
                vehicles[j]['volume_capacity']), f"Volume_{j}"

    # 4. Vehicle used if orders assigned
    for j in range(n_vehicles):
        for i in range(n_orders):
            prob += x[i,j] <= y[j], f"VehicleUsed_{i}_{j}"

    # Solve
    prob.solve(PULP_CBC_CMD(msg=0))

    # Extract solution
    assignments = [[] for _ in range(n_vehicles)]

    for i in range(n_orders):
        for j in range(n_vehicles):
            if x[i,j].varValue and x[i,j].varValue > 0.5:
                assignments[j].append(i)

    return {
        'status': LpStatus[prob.status],
        'vehicles_used': sum(1 for a in assignments if a),
        'assignments': assignments
    }
```

---

## Common Challenges & Solutions

### Challenge: Axle Weight Violations

**Problem:**
- Front or rear axle exceeds legal limit
- Roadside inspection failure
- Safety issues

**Solutions:**
- Use axle weight calculation in optimization
- Place heavy items between axles
- Avoid loading too much at front or rear
- Use load bars to shift weight
- Consider adding/removing items

### Challenge: Multi-Stop Accessibility

**Problem:**
- Items for early stops buried deep
- Need to unload/reload at each stop
- Time wasted, risk of damage

**Solutions:**
- Zone loading by delivery sequence
- Last stop at door, first stop at front
- Use vertical stacking per zone
- Load light/small items on top for easy removal
- Consider side-door access vehicles

### Challenge: Mixed Item Sizes

**Problem:**
- Pallets + loose boxes
- Different heights cause wasted space
- Difficult to secure

**Solutions:**
- Group similar items together
- Use pallets as base for loose items
- Fill gaps with soft goods or dunnage
- Stack smaller items on larger bases
- Use load nets or straps

---

## Output Format

### Vehicle Loading Report

**Vehicle: 26ft Box Truck**
- Dimensions: 26'L x 8'W x 8'H
- Weight Capacity: 12,000 lbs
- Route: 5 stops

**Loading Plan:**

Zone 1 (0-5ft) - Stop 5 (Last):
- 3 pallets: P045, P046, P047
- Weight: 2,100 lbs
- Accessible from rear door

Zone 2 (5-10ft) - Stop 4:
- 2 pallets + 8 boxes
- Weight: 1,850 lbs

Zone 3 (10-15ft) - Stop 3:
- 4 pallets
- Weight: 2,800 lbs

Zone 4 (15-20ft) - Stop 2:
- 3 pallets + 12 boxes
- Weight: 2,400 lbs

Zone 5 (20-26ft) - Stop 1 (First):
- 2 pallets
- Weight: 1,600 lbs

**Summary:**
- Total Weight: 10,750 lbs (90% capacity)
- Volume Utilization: 82%
- Axle Weights: Front 4,200 lbs, Rear 6,550 lbs ✓
- Load Secured: Yes (4 load bars, stretch wrap)

---

## Questions to Ask

1. What type of vehicle? (van, box truck, semi?)
2. What are the cargo dimensions and weight capacity?
3. Single destination or multiple stops?
4. If multi-stop, what's the delivery sequence?
5. Any axle weight concerns or restrictions?
6. Are items palletized or loose cargo?
7. Any special handling requirements?

---

## Related Skills

- **route-optimization**: For delivery route planning
- **3d-bin-packing**: For general 3D packing algorithms
- **pallet-loading**: For pallet-level optimization
- **container-loading-optimization**: For container loading
- **fleet-management**: For vehicle fleet optimization
- **last-mile-delivery**: For final delivery optimization
