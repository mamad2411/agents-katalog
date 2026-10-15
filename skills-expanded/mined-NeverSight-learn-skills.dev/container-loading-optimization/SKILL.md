---
name: container-loading-optimization
description: When the user wants to optimize container loading, load shipping containers efficiently, or maximize container utilization. Also use when the user mentions "container packing," "FCL optimization," "LCL consolidation," "container stuffing," "cargo optimization," "shipping container loading," or "container utilization." For pallet-level optimization, see pallet-loading. For general 3D packing, see 3d-bin-packing.
---

# Container Loading Optimization

You are an expert in container loading optimization and cargo planning. Your goal is to help efficiently load shipping containers, maximize utilization, ensure cargo safety, and minimize shipping costs while complying with weight and safety regulations.

## Initial Assessment

Before optimizing container loading, understand:

1. **Container Types & Specifications**
   - Container size? (20ft, 40ft, 40ft HC, 45ft?)
   - Internal dimensions and weight capacity?
   - FCL (Full Container Load) or LCL (Less than Container Load)?
   - Standard dry, refrigerated (reefer), open-top, or flat-rack?
   - Number of containers available?

2. **Cargo Characteristics**
   - Palletized or loose cargo?
   - Pallet sizes if applicable (GMA, EUR, custom)?
   - Package dimensions and weights?
   - Stackability and fragility?
   - Temperature requirements?

3. **Loading Constraints**
   - Weight distribution requirements?
   - Axle weight limits for trucking?
   - Loading sequence (LIFO/FIFO)?
   - Multi-destination shipments?
   - Securing and bracing requirements?

4. **Optimization Objectives**
   - Minimize number of containers?
   - Maximize utilization of each container?
   - Minimize shipping costs?
   - Ensure even weight distribution?
   - Optimize for specific loading sequence?

---

## Container Loading Framework

### Standard Container Dimensions

**20ft Standard Dry Container**
- External: 20' L x 8' W x 8'6" H (6.1m x 2.4m x 2.6m)
- Internal: 19'4" x 7'8" x 7'10" (5.9m x 2.35m x 2.39m)
- Capacity: 1,172 cu ft (33.2 m³)
- Max Gross Weight: 67,200 lbs (30,480 kg)
- Tare Weight: ~5,000 lbs (2,300 kg)
- Payload: ~62,000 lbs (28,180 kg)

**40ft Standard Dry Container**
- External: 40' L x 8' W x 8'6" H (12.2m x 2.4m x 2.6m)
- Internal: 39'6" x 7'8" x 7'10" (12.03m x 2.35m x 2.39m)
- Capacity: 2,390 cu ft (67.7 m³)
- Max Gross Weight: 67,200 lbs (30,480 kg)
- Tare Weight: ~8,200 lbs (3,750 kg)
- Payload: ~59,000 lbs (26,730 kg)

**40ft High Cube (HC) Container**
- External: 40' L x 8' W x 9'6" H (12.2m x 2.4m x 2.9m)
- Internal: 39'6" x 7'8" x 8'10" (12.03m x 2.35m x 2.69m)
- Capacity: 2,694 cu ft (76.3 m³)
- Max Gross Weight: 67,200 lbs (30,480 kg)
- Tare Weight: ~8,800 lbs (4,000 kg)
- Payload: ~58,400 lbs (26,480 kg)

**45ft High Cube Container**
- External: 45' L x 8' W x 9'6" H (13.72m x 2.4m x 2.9m)
- Internal: 44'6" x 7'8" x 8'10" (13.55m x 2.35m x 2.69m)
- Capacity: 3,043 cu ft (86.1 m³)
- Max Gross Weight: 67,200 lbs (30,480 kg)
- Payload: ~58,000 lbs (26,300 kg)

### Key Loading Principles

**1. Weight Distribution**
- Distribute weight evenly along container length
- Target: <2% weight difference between front/back
- Consider axle weight limits for trucking
- Avoid concentrated loads

**2. Center of Gravity**
- Keep COG low (bottom 1/3 of container)
- Maintain lateral balance (side-to-side)
- Longitudinal balance (front-to-back)

**3. Load Securing**
- Secure cargo to prevent shifting
- Use dunnage, airbags, straps, or bracing
- Fill voids to minimize movement
- Consider dynamic forces during transport

**4. Loading Sequence**
- LIFO (Last In, First Out) for single destination
- FIFO (First In, First Out) for multi-drop
- Heavy items at bottom, light on top
- Fragile items protected

---

## Mathematical Formulation

### Container Loading Problem

**Decision Variables:**
- x_i, y_i, z_i = position of item i in container
- c_i = container number assigned to item i
- o_i = orientation of item i
- used_j = 1 if container j is used

**Objective Functions:**

1. Minimize containers:
   Minimize Σ used_j

2. Minimize cost:
   Minimize Σ (cost_j × used_j) + Σ (shipping_cost_i × c_i)

3. Maximize utilization:
   Maximize (Σ volume_loaded) / (Σ container_capacity)

**Constraints:**
1. Non-overlap within container
2. Weight capacity per container
3. Weight distribution balance
4. Loading sequence if required
5. Axle weight limits
6. Cargo compatibility (chemicals, food, etc.)

---

## Algorithms and Solution Methods

### Palletized Cargo Loading

```python
class PalletizedContainerLoader:
    """
    Container loading optimizer for palletized cargo

    Handles standard pallets loaded into containers
    """

    def __init__(self, container_type='40HC'):
        """
        Initialize with container type

        Parameters:
        - container_type: '20', '40', '40HC', '45HC'
        """

        # Container internal dimensions (inches)
        containers = {
            '20': {'L': 232, 'W': 92, 'H': 94, 'capacity': 62000, 'cost': 1.0},
            '40': {'L': 474, 'W': 92, 'H': 94, 'capacity': 59000, 'cost': 1.5},
            '40HC': {'L': 474, 'W': 92, 'H': 106, 'capacity': 58400, 'cost': 1.6},
            '45HC': {'L': 534, 'W': 92, 'H': 106, 'capacity': 58000, 'cost': 1.8}
        }

        if container_type not in containers:
            raise ValueError(f"Unknown container type: {container_type}")

        self.container_type = container_type
        self.container_dims = containers[container_type]
        self.pallets = []
        self.solution = None

    def add_pallet(self, length, width, height, weight, quantity=1, pallet_id=None):
        """Add pallet to load"""
        for i in range(quantity):
            pid = f"{pallet_id}_{i}" if pallet_id and quantity > 1 else pallet_id or f"P{len(self.pallets)}"
            self.pallets.append({
                'id': pid,
                'dims': (length, width, height),
                'weight': weight
            })

    def optimize_loading(self, allow_rotation=True, double_stack=True):
        """
        Optimize pallet loading into containers

        Parameters:
        - allow_rotation: allow 90-degree rotation
        - double_stack: allow stacking pallets

        Returns loading plan
        """

        # Sort pallets by volume (largest first)
        sorted_pallets = sorted(self.pallets,
                               key=lambda p: p['dims'][0] * p['dims'][1] * p['dims'][2],
                               reverse=True)

        containers = []

        for pallet in sorted_pallets:
            placed = False

            # Try existing containers
            for container in containers:
                if self._try_place_pallet(container, pallet, allow_rotation, double_stack):
                    placed = True
                    break

            # Create new container if needed
            if not placed:
                new_container = {
                    'pallets': [],
                    'weight': 0,
                    'positions': [],
                    'grid': self._create_empty_grid()
                }

                if self._try_place_pallet(new_container, pallet, allow_rotation, double_stack):
                    containers.append(new_container)
                else:
                    print(f"Warning: Could not place pallet {pallet['id']}")

        # Calculate metrics
        self.solution = self._calculate_solution_metrics(containers)
        return self.solution

    def _try_place_pallet(self, container, pallet, allow_rotation, double_stack):
        """Try to place pallet in container"""

        L, W, H = self.container_dims['L'], self.container_dims['W'], self.container_dims['H']
        max_weight = self.container_dims['capacity']

        # Check weight
        if container['weight'] + pallet['weight'] > max_weight:
            return False

        # Try different positions and orientations
        orientations = [(pallet['dims'][0], pallet['dims'][1], pallet['dims'][2], False)]
        if allow_rotation:
            orientations.append((pallet['dims'][1], pallet['dims'][0], pallet['dims'][2], True))

        # Try floor positions first
        for l, w, h, rotated in orientations:
            # Try placing on floor
            for x in range(0, int(L - l) + 1, 4):  # 4-inch increments
                for y in range(0, int(W - w) + 1, 4):
                    if self._check_space_available(container['grid'], x, y, 0, l, w, h):
                        # Place pallet
                        self._occupy_space(container['grid'], x, y, 0, l, w, h)
                        container['pallets'].append(pallet)
                        container['weight'] += pallet['weight']
                        container['positions'].append({
                            'pallet': pallet,
                            'position': (x, y, 0),
                            'dims': (l, w, h),
                            'rotated': rotated,
                            'level': 'floor'
                        })
                        return True

        # Try stacking if allowed
        if double_stack:
            for l, w, h, rotated in orientations:
                # Find existing pallets to stack on
                for pos in container['positions']:
                    if pos['level'] == 'floor':
                        base_x, base_y, base_z = pos['position']
                        base_l, base_w, base_h = pos['dims']

                        # Check if new pallet fits on top
                        if (l <= base_l and w <= base_w and
                            base_z + base_h + h <= H):

                            stack_z = base_z + base_h

                            if self._check_space_available(container['grid'],
                                                          base_x, base_y, stack_z,
                                                          l, w, h):
                                # Stack pallet
                                self._occupy_space(container['grid'],
                                                  base_x, base_y, stack_z,
                                                  l, w, h)
                                container['pallets'].append(pallet)
                                container['weight'] += pallet['weight']
                                container['positions'].append({
                                    'pallet': pallet,
                                    'position': (base_x, base_y, stack_z),
                                    'dims': (l, w, h),
                                    'rotated': rotated,
                                    'level': 'stacked'
                                })
                                return True

        return False

    def _create_empty_grid(self):
        """Create 3D occupancy grid"""
        # Simplified grid (4-inch resolution)
        L = int(self.container_dims['L'] / 4)
        W = int(self.container_dims['W'] / 4)
        H = int(self.container_dims['H'] / 4)
        return [[[False for _ in range(H)] for _ in range(W)] for _ in range(L)]

    def _check_space_available(self, grid, x, y, z, l, w, h):
        """Check if space is available in grid"""
        x_cells = int(x / 4)
        y_cells = int(y / 4)
        z_cells = int(z / 4)
        l_cells = int((l + 3) / 4)
        w_cells = int((w + 3) / 4)
        h_cells = int((h + 3) / 4)

        try:
            for i in range(x_cells, x_cells + l_cells):
                for j in range(y_cells, y_cells + w_cells):
                    for k in range(z_cells, z_cells + h_cells):
                        if i >= len(grid) or j >= len(grid[0]) or k >= len(grid[0][0]):
                            return False
                        if grid[i][j][k]:
                            return False
            return True
        except:
            return False

    def _occupy_space(self, grid, x, y, z, l, w, h):
        """Mark space as occupied in grid"""
        x_cells = int(x / 4)
        y_cells = int(y / 4)
        z_cells = int(z / 4)
        l_cells = int((l + 3) / 4)
        w_cells = int((w + 3) / 4)
        h_cells = int((h + 3) / 4)

        for i in range(x_cells, min(x_cells + l_cells, len(grid))):
            for j in range(y_cells, min(y_cells + w_cells, len(grid[0]))):
                for k in range(z_cells, min(z_cells + h_cells, len(grid[0][0]))):
                    grid[i][j][k] = True

    def _calculate_solution_metrics(self, containers):
        """Calculate solution metrics"""

        L = self.container_dims['L']
        W = self.container_dims['W']
        H = self.container_dims['H']
        container_volume = L * W * H

        solution = {
            'num_containers': len(containers),
            'container_type': self.container_type,
            'containers': []
        }

        for idx, cont in enumerate(containers):
            # Calculate volume used
            volume_used = sum(
                pos['dims'][0] * pos['dims'][1] * pos['dims'][2]
                for pos in cont['positions']
            )

            utilization = (volume_used / container_volume * 100)

            solution['containers'].append({
                'container_id': idx,
                'num_pallets': len(cont['pallets']),
                'weight': cont['weight'],
                'volume_used': volume_used,
                'utilization': utilization,
                'positions': cont['positions']
            })

        return solution

    def print_solution(self):
        """Print loading solution"""

        if not self.solution:
            print("No solution available")
            return

        print("=" * 70)
        print("CONTAINER LOADING SOLUTION")
        print("=" * 70)
        print(f"Container Type: {self.solution['container_type']}")
        print(f"Pallets to load: {len(self.pallets)}")
        print(f"Containers used: {self.solution['num_containers']}")
        print()

        for cont in self.solution['containers']:
            print(f"Container {cont['container_id'] + 1}:")
            print(f"  Pallets: {cont['num_pallets']}")
            print(f"  Weight: {cont['weight']:,.0f} lbs")
            print(f"  Utilization: {cont['utilization']:.1f}%")
            print()


# Example Usage
if __name__ == "__main__":
    # Create loader for 40ft HC container
    loader = PalletizedContainerLoader(container_type='40HC')

    # Add GMA pallets (48x40x60 inches, 1500 lbs each)
    loader.add_pallet(48, 40, 60, 1500, quantity=20, pallet_id='GMA')

    # Add EUR pallets (47x32x55 inches, 1200 lbs each)
    loader.add_pallet(47, 32, 55, 1200, quantity=10, pallet_id='EUR')

    # Optimize
    solution = loader.optimize_loading(allow_rotation=True, double_stack=True)

    # Print results
    loader.print_solution()
```

### Loose Cargo Loading

```python
def optimize_loose_cargo_loading(items, container_type='40HC'):
    """
    Optimize loading of non-palletized (loose) cargo

    Uses 3D bin packing algorithms
    """

    from skills.three_d_bin_packing import ThreeDimensionalBinPacker

    # Container dimensions
    containers = {
        '20': (232, 92, 94, 62000),
        '40': (474, 92, 94, 59000),
        '40HC': (474, 92, 106, 58400),
        '45HC': (534, 92, 106, 58000)
    }

    L, W, H, max_weight = containers[container_type]

    # Use 3D bin packing
    packer = ThreeDimensionalBinPacker(L, W, H, max_weight)

    for item in items:
        packer.add_item(
            item['length'], item['width'], item['height'],
            item['weight'], item.get('id')
        )

    solution = packer.solve(algorithm='extreme_point', allow_rotation=True)

    return solution
```

### Multi-Destination Loading

```python
def optimize_multi_destination_loading(shipments, container_type='40HC'):
    """
    Optimize container loading for multi-destination shipments

    Ensures items are loaded in reverse delivery order (LIFO)

    Parameters:
    - shipments: list of dicts with 'destination', 'items', 'priority'
    - container_type: container size

    Returns: loading plan with zones
    """

    # Sort shipments by delivery order (last delivery first)
    sorted_shipments = sorted(shipments,
                             key=lambda s: s.get('priority', 0),
                             reverse=True)

    containers = []

    for shipment in sorted_shipments:
        destination = shipment['destination']
        items = shipment['items']

        # Try to add to existing container
        placed = False
        for container in containers:
            # Check if can add zone
            if container['remaining_capacity'] >= sum(i['volume'] for i in items):
                # Add zone
                container['zones'].append({
                    'destination': destination,
                    'items': items
                })
                placed = True
                break

        if not placed:
            # Create new container
            new_container = {
                'zones': [{
                    'destination': destination,
                    'items': items
                }],
                'remaining_capacity': 1000  # Simplified
            }
            containers.append(new_container)

    return {
        'containers': containers,
        'num_containers': len(containers)
    }
```

---

## Common Challenges & Solutions

### Challenge: Cube Out vs. Weight Out

**Problem:**
- Container full by volume but under weight limit (cube out)
- OR hit weight limit with space remaining (weight out)
- Inefficient use of capacity

**Solutions:**
- Mix dense and light cargo for balance
- Calculate cubic weight ratio
- Use appropriatecontainer size for cargo density
- Consider consolidation with other shipments
- For heavy cargo: use smaller containers or ship by weight
- For light cargo: maximize volume usage

### Challenge: Weight Distribution

**Problem:**
- Uneven weight distribution
- Axle weight violations
- Container instability

**Solutions:**
- Calculate weight per linear foot
- Target even distribution (±2% variance)
- Place heavy items in middle/bottom
- Use load planning software
- Balance left/right, front/back
- Consider trucking axle limits

### Challenge: Mixed Pallet Sizes

**Problem:**
- GMA and EUR pallets don't pack well together
- Wasted space between different sizes

**Solutions:**
- Group similar pallet sizes
- Load largest pallets first
- Use filler cargo for gaps
- Consider separate containers for different pallet types
- Optimize pallet patterns before containerization

---

## Output Format

### Container Loading Plan

**Summary:**
- Shipment: Order #12345
- Containers Required: 2 x 40ft HC
- Total Pallets: 22
- Total Weight: 48,500 lbs
- Average Utilization: 87%

**Container 1 - 40ft HC:**
- Pallets Loaded: 11
- Weight: 24,800 lbs (42% of capacity)
- Volume Utilization: 89%
- Weight Distribution: Front 48%, Rear 52% ✓

Loading Pattern:
```
[Front]                [Rear]
Row 1: P1 P2 P3 P4    P5 P6
Row 2: P7 P8 P9       P10 P11
```

**Container 2 - 40ft HC:**
- Pallets Loaded: 11
- Weight: 23,700 lbs (41% of capacity)
- Volume Utilization: 85%
- Weight Distribution: Front 51%, Rear 49% ✓

**Securing Requirements:**
- Stretch wrap all pallets
- Use load bars between rows
- Airbags for void spaces
- Secure doors with seal #ABC123

---

## Questions to Ask

1. What container size are you using? (20ft, 40ft, 40ft HC, 45ft HC)
2. Are items palletized or loose cargo?
3. What are the pallet dimensions and weights?
4. Is there a weight limit or distribution requirement?
5. Is this single destination or multi-drop delivery?
6. Any special cargo (fragile, hazmat, temperature-controlled)?
7. Loading sequence requirements (LIFO/FIFO)?

---

## Related Skills

- **pallet-loading**: For pallet-level optimization before container loading
- **3d-bin-packing**: For loose cargo packing
- **vehicle-loading-optimization**: For truck loading
- **load-building-optimization**: For order consolidation
- **freight-optimization**: For shipping cost optimization
