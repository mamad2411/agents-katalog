---
name: order-batching-optimization
description: When the user wants to optimize order batching, group orders for efficient picking, or reduce picker travel distance. Also use when the user mentions "batch picking," "order grouping," "cluster picking," "multi-order picking," "batch-and-sort," or "zone batching." For wave planning, see wave-planning-optimization. For picker routing, see picker-routing-optimization.
---

# Order Batching Optimization

You are an expert in warehouse order batching and picking optimization. Your goal is to help group orders into optimal batches to minimize picker travel distance, maximize picking efficiency, reduce order cycle time, and improve overall warehouse productivity.

## Initial Assessment

Before optimizing order batching, understand:

1. **Picking Method**
   - Discrete picking (one order at a time)?
   - Batch picking (multiple orders)?
   - Zone picking (pass to next zone)?
   - Cluster picking (pick-to-cart)?
   - Pick-to-light or voice picking?

2. **Order Characteristics**
   - Average lines per order?
   - Order size distribution (single-line vs. multi-line)?
   - SKU overlap between orders?
   - Order priority levels?
   - Daily order volume?

3. **Warehouse Configuration**
   - Warehouse layout (grid, diagonal, irregular)?
   - Number of aisles and pick faces?
   - Pick cart capacity (orders and units)?
   - Sorting method after batch (manual, automated)?
   - Forward pick vs. reserve locations?

4. **Current Performance**
   - Current picks per hour?
   - Picker travel distance per order?
   - Batch sizes used?
   - Sort time per batch?
   - Mispick or sort error rates?

---

## Order Batching Framework

### Batching Strategies

**1. Discrete Picking (No Batching)**
- One order per trip
- **Pros**: Simple, no sorting, low error rate
- **Cons**: High travel distance, low efficiency
- **Use**: High-value orders, complex orders, each-pick only

**2. Batch Picking**
- Pick multiple orders simultaneously
- **Pros**: Reduced travel (60-80% reduction), higher productivity
- **Cons**: Requires sorting, more complex
- **Use**: Standard warehouse operations

**3. Zone Batch Picking**
- Batch orders, but each picker handles one zone
- Pass totes/carts to next zone
- **Pros**: Smaller batches, balanced workload
- **Cons**: Handoff points, coordination needed

**4. Cluster Picking (Pick-to-Cart)**
- Multi-compartment cart (e.g., 4-8 orders)
- Pick directly into order containers
- **Pros**: No sorting, medium efficiency
- **Cons**: Limited by cart capacity, order size variability

**5. Wave-Less Batching**
- Continuous batching as orders arrive
- No fixed wave times
- **Pros**: Lower cycle time, responsive
- **Cons**: Requires sophisticated WMS

### Batching Objectives

```
Primary Goals:
1. Minimize total picker travel distance
2. Maximize picks per hour
3. Balance batch sizes (avoid very small/large)
4. Minimize sort time and errors
5. Meet order cutoff times

Constraints:
- Cart capacity (units and orders)
- Sorting capacity
- Time windows (priority orders)
- Zone limitations
```

---

## Mathematical Formulation

### Batching as Clustering Problem

**Decision Variables:**
- x[o,b] = 1 if order o assigned to batch b, 0 otherwise
- y[b] = 1 if batch b is used, 0 otherwise

**Parameters:**
- S[o,o'] = similarity score between orders o and o' (SKU overlap, proximity)
- D[o] = total travel distance for order o alone
- L[o] = number of lines in order o
- C_max = maximum capacity per batch (orders or lines)

**Objective Function:**

```
Minimize:
  Total Travel Distance + Penalty for unbalanced batches

Formally:
  Σ Σ (travel_distance[b] × y[b])
  + α × Σ (deviation from ideal batch size)
  + β × (number of batches)

where travel_distance[b] is calculated from batched order locations
```

**Constraints:**

```python
# 1. Each order in exactly one batch
for o in orders:
    Σ x[o,b] = 1  for all b

# 2. Batch capacity (orders)
for b in batches:
    Σ x[o,b] ≤ C_max_orders  for all o

# 3. Batch capacity (lines)
for b in batches:
    Σ (L[o] × x[o,b]) ≤ C_max_lines  for all o

# 4. Link batch usage to order assignment
for b in batches:
    for o in orders:
        x[o,b] ≤ y[b]

# 5. Time window constraints (priority orders)
for o in priority_orders:
    for b in batches:
        if x[o,b] = 1:
            completion_time[b] ≤ deadline[o]
```

### Similarity-Based Clustering

Orders that should be batched together have high similarity:

```
Similarity(order_i, order_j) =
  α × (SKU overlap / total unique SKUs)
  + β × (1 - distance between order centroids / max_distance)
  + γ × (time window compatibility)

Higher similarity → Better batch candidates
```

---

## Batching Algorithms

### Greedy Seed-Based Batching

```python
import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist, squareform

def seed_based_batching(orders, locations, max_batch_size=6):
    """
    Greedy batching using seed orders

    Algorithm:
    1. Select "seed" order (e.g., most lines, earliest deadline)
    2. Add most similar orders until capacity reached
    3. Repeat for remaining orders

    Parameters:
    -----------
    orders : DataFrame
        Columns: order_id, sku_list, priority, deadline
    locations : dict
        {sku: (x, y) location}
    max_batch_size : int
        Maximum orders per batch

    Returns:
    --------
    Batch assignments
    """

    # Calculate order similarity matrix
    similarity_matrix = calculate_order_similarity(orders, locations)

    remaining_orders = set(orders['order_id'])
    batches = []
    batch_id = 1

    while remaining_orders:
        # Select seed order (highest priority remaining)
        seed_candidates = orders[orders['order_id'].isin(remaining_orders)]
        seed_order = seed_candidates.sort_values(
            ['priority', 'deadline'],
            ascending=[False, True]
        ).iloc[0]['order_id']

        # Initialize batch with seed
        batch = [seed_order]
        remaining_orders.remove(seed_order)

        # Add similar orders to batch
        while len(batch) < max_batch_size and remaining_orders:
            # Find most similar remaining order
            best_order = None
            best_similarity = -1

            for candidate in remaining_orders:
                # Average similarity to all orders in batch
                avg_similarity = np.mean([
                    similarity_matrix.loc[candidate, b_order]
                    for b_order in batch
                ])

                if avg_similarity > best_similarity:
                    best_similarity = avg_similarity
                    best_order = candidate

            if best_order and best_similarity > 0.3:  # Threshold
                batch.append(best_order)
                remaining_orders.remove(best_order)
            else:
                break  # No good candidates

        batches.append({
            'batch_id': batch_id,
            'orders': batch,
            'num_orders': len(batch),
            'seed_order': seed_order
        })
        batch_id += 1

    return pd.DataFrame(batches)


def calculate_order_similarity(orders, locations):
    """
    Calculate pairwise similarity between orders

    Similarity based on:
    - SKU overlap (Jaccard similarity)
    - Spatial proximity of pick locations
    """

    order_ids = orders['order_id'].tolist()
    n = len(order_ids)
    similarity = np.zeros((n, n))

    for i, order_i_id in enumerate(order_ids):
        for j, order_j_id in enumerate(order_ids):
            if i == j:
                similarity[i, j] = 1.0
                continue

            order_i = orders[orders['order_id'] == order_i_id].iloc[0]
            order_j = orders[orders['order_id'] == order_j_id].iloc[0]

            # SKU overlap (Jaccard)
            skus_i = set(order_i['sku_list'])
            skus_j = set(order_j['sku_list'])

            intersection = len(skus_i & skus_j)
            union = len(skus_i | skus_j)
            jaccard = intersection / union if union > 0 else 0

            # Spatial proximity (simplified: centroid distance)
            centroid_i = calculate_order_centroid(order_i['sku_list'], locations)
            centroid_j = calculate_order_centroid(order_j['sku_list'], locations)

            distance = np.linalg.norm(np.array(centroid_i) - np.array(centroid_j))
            max_distance = 500  # warehouse size
            proximity = 1 - min(distance / max_distance, 1)

            # Combined similarity
            similarity[i, j] = 0.6 * jaccard + 0.4 * proximity

    return pd.DataFrame(similarity, index=order_ids, columns=order_ids)


def calculate_order_centroid(sku_list, locations):
    """Calculate centroid of pick locations for an order"""
    coords = [locations.get(sku, (0, 0)) for sku in sku_list if sku in locations]
    if not coords:
        return (0, 0)
    return (np.mean([c[0] for c in coords]), np.mean([c[1] for c in coords]))


# Example usage
orders = pd.DataFrame({
    'order_id': [f'ORD{i:03d}' for i in range(1, 21)],
    'sku_list': [
        np.random.choice(['SKU_A', 'SKU_B', 'SKU_C', 'SKU_D', 'SKU_E',
                         'SKU_F', 'SKU_G', 'SKU_H', 'SKU_I', 'SKU_J'],
                        size=np.random.randint(1, 8), replace=False).tolist()
        for _ in range(20)
    ],
    'priority': np.random.choice([1, 2, 3], 20),
    'deadline': pd.date_range('2024-01-01 16:00', periods=20, freq='30T')
})

locations = {
    'SKU_A': (10, 20), 'SKU_B': (15, 25), 'SKU_C': (50, 30),
    'SKU_D': (55, 35), 'SKU_E': (80, 40), 'SKU_F': (85, 45),
    'SKU_G': (20, 60), 'SKU_H': (25, 65), 'SKU_I': (60, 70),
    'SKU_J': (65, 75)
}

batches = seed_based_batching(orders, locations, max_batch_size=6)

print("Order Batching Results:")
print(f"Total Batches: {len(batches)}")
for _, batch in batches.iterrows():
    print(f"Batch {batch['batch_id']}: {batch['num_orders']} orders")
    print(f"  Orders: {', '.join(batch['orders'])}")
```

### K-Means Clustering for Batching

```python
from sklearn.cluster import KMeans

def kmeans_batching(orders, locations, num_batches):
    """
    Use K-Means clustering to batch orders

    Cluster based on spatial and temporal features

    Parameters:
    -----------
    orders : DataFrame
        Order data with sku_list, priority, deadline
    locations : dict
        SKU locations
    num_batches : int
        Target number of batches

    Returns:
    --------
    Batch assignments
    """

    # Feature engineering
    features = []

    for idx, order in orders.iterrows():
        # Spatial feature: order centroid
        centroid = calculate_order_centroid(order['sku_list'], locations)

        # Temporal feature: deadline urgency (hours until deadline)
        hours_until_deadline = (
            (order['deadline'] - pd.Timestamp.now()).total_seconds() / 3600
        )

        # Size feature: number of lines
        num_lines = len(order['sku_list'])

        # Combine features (normalized)
        features.append([
            centroid[0] / 100,  # Normalize by warehouse size
            centroid[1] / 100,
            hours_until_deadline / 24,  # Normalize to days
            num_lines / 10  # Normalize by typical order size
        ])

    features = np.array(features)

    # K-Means clustering
    kmeans = KMeans(n_clusters=num_batches, random_state=42)
    cluster_labels = kmeans.fit_predict(features)

    orders['batch_id'] = cluster_labels + 1

    # Group into batches
    batches = []
    for batch_id in range(1, num_batches + 1):
        batch_orders = orders[orders['batch_id'] == batch_id]['order_id'].tolist()

        if batch_orders:
            batches.append({
                'batch_id': batch_id,
                'orders': batch_orders,
                'num_orders': len(batch_orders),
                'centroid': kmeans.cluster_centers_[batch_id - 1]
            })

    return pd.DataFrame(batches)


# Example
batches_kmeans = kmeans_batching(orders, locations, num_batches=4)

print("\nK-Means Batching Results:")
for _, batch in batches_kmeans.iterrows():
    print(f"Batch {batch['batch_id']}: {batch['num_orders']} orders")
```

### Optimization Model: MIP-Based Batching

```python
from pulp import *

def optimize_order_batching(orders, travel_distances, max_orders_per_batch=8,
                           max_lines_per_batch=100):
    """
    Optimal order batching using Mixed-Integer Programming

    Parameters:
    -----------
    orders : list
        Order identifiers
    travel_distances : dict
        {batch_composition: total_distance}
        Precomputed for all possible batch combinations
    max_orders_per_batch : int
        Cart capacity (orders)
    max_lines_per_batch : int
        Cart capacity (lines)

    Returns:
    --------
    Optimal batching
    """

    # For tractability, use a simplified model
    # In practice, would use heuristics to generate candidate batches
    # then solve assignment problem

    prob = LpProblem("Order_Batching", LpMinimize)

    # Generate candidate batches (simplified: all pairs and triples)
    candidate_batches = []
    batch_id = 0

    # Single-order batches
    for o in orders:
        candidate_batches.append({
            'batch_id': batch_id,
            'orders': [o],
            'distance': travel_distances.get((o,), 100)
        })
        batch_id += 1

    # Pair batches
    for i, o1 in enumerate(orders):
        for o2 in orders[i+1:]:
            candidate_batches.append({
                'batch_id': batch_id,
                'orders': [o1, o2],
                'distance': travel_distances.get((o1, o2), 150)
            })
            batch_id += 1

    batches = range(len(candidate_batches))

    # Decision variables
    # y[b] = 1 if batch b is used
    y = LpVariable.dicts("use_batch", batches, cat='Binary')

    # Objective: minimize total travel distance
    prob += lpSum([
        candidate_batches[b]['distance'] * y[b]
        for b in batches
    ]), "Total_Distance"

    # Constraints

    # Each order in exactly one batch
    for o in orders:
        prob += lpSum([
            y[b] for b in batches
            if o in candidate_batches[b]['orders']
        ]) == 1, f"Order_{o}"

    # Solve
    prob.solve(PULP_CBC_CMD(msg=0))

    # Extract solution
    selected_batches = []
    for b in batches:
        if y[b].varValue > 0.5:
            selected_batches.append(candidate_batches[b])

    return {
        'status': LpStatus[prob.status],
        'total_distance': value(prob.objective),
        'batches': selected_batches,
        'num_batches': len(selected_batches)
    }


# Example (simplified with mock distances)
orders_list = [f'ORD{i:03d}' for i in range(1, 11)]

# Mock travel distances
travel_distances = {
    (o,): np.random.randint(80, 120) for o in orders_list
}
for i, o1 in enumerate(orders_list):
    for o2 in orders_list[i+1:]:
        # Batched distance is less than sum of individual
        travel_distances[(o1, o2)] = int(
            travel_distances[(o1,)] + travel_distances[(o2,)] * 0.6
        )

result = optimize_order_batching(orders_list, travel_distances)

print(f"\nOptimization Status: {result['status']}")
print(f"Total Distance: {result['total_distance']:.0f}")
print(f"Number of Batches: {result['num_batches']}")
print("\nBatches:")
for batch in result['batches']:
    print(f"  Batch {batch['batch_id']}: {batch['orders']} "
          f"(distance: {batch['distance']})")
```

---

## Advanced Batching Techniques

### Dynamic Batching with Real-Time Updates

```python
class DynamicBatcher:
    """
    Dynamic order batching system with real-time updates
    """

    def __init__(self, max_batch_size=6, max_wait_time=15):
        """
        Parameters:
        -----------
        max_batch_size : int
            Maximum orders per batch
        max_wait_time : int
            Maximum minutes to wait for batch to fill
        """
        self.max_batch_size = max_batch_size
        self.max_wait_time = max_wait_time
        self.pending_orders = []
        self.completed_batches = []
        self.current_batch_id = 1

    def add_order(self, order):
        """Add new order to pending queue"""
        order['received_time'] = datetime.now()
        self.pending_orders.append(order)

    def should_release_batch(self):
        """
        Determine if a batch should be released

        Release if:
        1. Batch size reached
        2. Oldest order exceeds max wait time
        3. High-priority order needs immediate processing
        """

        if len(self.pending_orders) == 0:
            return False

        # Check size threshold
        if len(self.pending_orders) >= self.max_batch_size:
            return True

        # Check wait time
        oldest_order = min(self.pending_orders,
                          key=lambda x: x['received_time'])
        wait_time = (datetime.now() - oldest_order['received_time']).total_seconds() / 60

        if wait_time >= self.max_wait_time:
            return True

        # Check for high-priority urgent orders
        priority_orders = [o for o in self.pending_orders if o.get('priority', 3) == 1]
        if priority_orders:
            # If priority order waiting > 5 min, release
            for po in priority_orders:
                wait = (datetime.now() - po['received_time']).total_seconds() / 60
                if wait >= 5:
                    return True

        return False

    def create_batch(self):
        """
        Create batch from pending orders using similarity-based grouping
        """

        if not self.pending_orders:
            return None

        # Sort by priority and received time
        sorted_orders = sorted(
            self.pending_orders,
            key=lambda x: (x.get('priority', 3), x['received_time'])
        )

        # Take up to max_batch_size orders
        batch_orders = sorted_orders[:self.max_batch_size]

        # Remove from pending
        for order in batch_orders:
            self.pending_orders.remove(order)

        batch = {
            'batch_id': self.current_batch_id,
            'orders': batch_orders,
            'created_time': datetime.now(),
            'num_orders': len(batch_orders)
        }

        self.completed_batches.append(batch)
        self.current_batch_id += 1

        return batch

    def optimize_pending_batches(self, locations):
        """
        Re-optimize pending orders into best batches

        Called periodically or when significant orders accumulated
        """

        if len(self.pending_orders) < 2:
            return

        # Create DataFrame from pending
        pending_df = pd.DataFrame(self.pending_orders)

        # Use seed-based batching
        batches_df = seed_based_batching(
            pending_df,
            locations,
            max_batch_size=self.max_batch_size
        )

        # Update pending with batch assignments
        for idx, row in pending_df.iterrows():
            order_id = row['order_id']
            # Find batch assignment
            for _, batch in batches_df.iterrows():
                if order_id in batch['orders']:
                    # Update order with batch hint
                    for pending_order in self.pending_orders:
                        if pending_order['order_id'] == order_id:
                            pending_order['suggested_batch'] = batch['batch_id']
                    break


# Example usage
batcher = DynamicBatcher(max_batch_size=6, max_wait_time=15)

# Simulate order arrivals
for i in range(15):
    order = {
        'order_id': f'ORD{i:03d}',
        'sku_list': np.random.choice(['SKU_A', 'SKU_B', 'SKU_C'],
                                    size=np.random.randint(1, 5),
                                    replace=False).tolist(),
        'priority': np.random.choice([1, 2, 3]),
        'deadline': datetime.now() + timedelta(hours=4)
    }
    batcher.add_order(order)

# Check if should release
if batcher.should_release_batch():
    batch = batcher.create_batch()
    print(f"Released Batch {batch['batch_id']}:")
    print(f"  Orders: {len(batch['orders'])}")
    for order in batch['orders']:
        print(f"    {order['order_id']}: {order['sku_list']}")

print(f"\nPending Orders: {len(batcher.pending_orders)}")
```

### Batch-and-Sort Optimization

```python
def optimize_batch_and_sort(batch_orders, sort_stations=4):
    """
    Optimize batch picking with downstream sorting

    Minimize: Pick time + Sort time

    Parameters:
    -----------
    batch_orders : list
        Orders in the batch
    sort_stations : int
        Number of parallel sort stations

    Returns:
    --------
    Optimized pick sequence and sort assignments
    """

    # Calculate pick route (TSP-style)
    # Simplified: assume pre-calculated

    # Calculate sort time based on item distribution
    total_items = sum(len(o['sku_list']) for o in batch_orders)

    # Sort time depends on:
    # 1. Number of unique SKUs (more touchpoints)
    # 2. Number of orders (more destinations)
    # 3. Sort method (manual, automated)

    # Manual sort time estimation (seconds per item)
    items_per_order = total_items / len(batch_orders)

    if items_per_order <= 2:
        sort_time_per_item = 3  # Simple, few items per order
    elif items_per_order <= 5:
        sort_time_per_item = 5  # Moderate complexity
    else:
        sort_time_per_item = 8  # Complex, many items per order

    total_sort_time = total_items * sort_time_per_item / sort_stations

    # Pick time estimation (assuming 100 picks/hour = 36 sec/pick)
    pick_time_per_line = 36
    total_pick_time = total_items * pick_time_per_line

    # Total time
    total_time = total_pick_time + total_sort_time

    return {
        'pick_time': total_pick_time,
        'sort_time': total_sort_time,
        'total_time': total_time,
        'efficiency': total_items / (total_time / 3600)  # items per hour
    }


# Example
batch = [
    {'order_id': 'ORD001', 'sku_list': ['A', 'B', 'C']},
    {'order_id': 'ORD002', 'sku_list': ['A', 'D']},
    {'order_id': 'ORD003', 'sku_list': ['B', 'C', 'D', 'E']},
]

result = optimize_batch_and_sort(batch, sort_stations=2)
print("\nBatch-and-Sort Analysis:")
print(f"Pick Time: {result['pick_time']:.0f} seconds")
print(f"Sort Time: {result['sort_time']:.0f} seconds")
print(f"Total Time: {result['total_time']:.0f} seconds")
print(f"Efficiency: {result['efficiency']:.1f} items/hour")
```

---

## Tools & Libraries

### Order Batching Software

**Warehouse Management Systems with Batching:**
- **Manhattan WMS**: Advanced batching algorithms
- **Blue Yonder (JDA) WMS**: AI-optimized batching
- **SAP EWM**: Batch determination rules
- **HighJump WMS**: Multi-order picking strategies
- **Körber WMS**: Dynamic batch creation

**Specialized Optimization:**
- **Optislot**: Slotting and batching optimization
- **Wise Systems**: Dynamic routing and batching for last-mile
- **Lucas Systems**: Voice-directed batch picking optimization

### Python Libraries

```python
# Optimization
from pulp import *
from scipy.optimize import linear_sum_assignment
from ortools.constraint_solver import pywrapcp

# Clustering
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage

# Distance Calculations
from scipy.spatial.distance import pdist, squareform, jaccard
import networkx as nx  # For TSP routing within batch

# Analysis
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
```

---

## Common Challenges & Solutions

### Challenge: High Sort Time

**Problem:**
- Sorting takes longer than picking
- Sort errors and mispicks
- Bottleneck at sort stations

**Solutions:**
- Reduce batch size (less sorting complexity)
- Use cluster picking instead (pick-to-cart, no sorting)
- Automate sorting (put-to-light, automated sorters)
- Pre-sort during picking (numbered totes per order)
- Sequence picks by order to minimize sort mixing
- Add more sort stations or lanes

### Challenge: Uneven Order Sizes

**Problem:**
- Mix of 1-line and 20-line orders
- Small orders waste batch capacity
- Large orders can't batch with others

**Solutions:**
- Separate batching strategies by order size
  - Small orders (1-3 lines): Large batches (10-12 orders)
  - Medium (4-10 lines): Standard batches (4-6 orders)
  - Large (>10 lines): Discrete picking or small batches
- Line-based batching instead of order-based
- Adjust batch size dynamically based on order profile

### Challenge: Low SKU Overlap

**Problem:**
- Orders have unique SKUs (low overlap)
- Batching doesn't reduce travel much
- Near-discrete picking efficiency

**Solutions:**
- Focus on spatial clustering (zone proximity) over SKU overlap
- Use smaller batches (2-3 orders) with better spatial fit
- Implement zone picking instead (each zone does portion)
- Consider goods-to-person systems (no travel benefits anyway)
- Improve slotting to increase density of fast-movers

### Challenge: Priority Order Conflicts

**Problem:**
- High-priority orders interrupt batches
- Can't wait for batch to fill (urgency)
- Mix of rush and standard orders

**Solutions:**
- Separate priority lanes (express batching with size=1 or 2)
- Reserve pickers for priority orders
- Dynamic batch release (don't wait for full batch if priority)
- Use different picking methods by priority (zone for standard, discrete for priority)
- Pre-allocate inventory for known rush orders

### Challenge: Cart Capacity Limitations

**Problem:**
- Physical cart only holds 6 totes
- Can't batch more orders due to equipment
- Weight/volume limits

**Solutions:**
- Multiple cart types (4-tote, 8-tote, 12-tote)
- Batch based on available cart types
- Two-pass picking (large batches split across trips)
- Use powered carts or AGVs (higher capacity)
- Zone picking with conveyors (unlimited capacity)

---

## Output Format

### Order Batching Report

**Batch Optimization Summary - January 15, 2024**

**Performance Comparison:**

| Metric | Discrete Picking | Current Batching | Optimized Batching |
|--------|------------------|------------------|-------------------|
| Avg Orders per Batch | 1.0 | 4.2 | 5.8 |
| Avg Travel per Order (ft) | 425 | 185 | 142 |
| Travel Reduction | 0% | 56% | 67% |
| Picks per Hour | 65 | 145 | 175 |
| Sort Time per Order (min) | 0 | 2.5 | 2.1 |
| Total Cycle Time (min) | 24 | 14 | 12 |

**Batch Details:**

```
Batch 001:
  Orders: 6
  Total Lines: 42
  SKU Overlap: 68%
  Estimated Travel: 620 ft
  Estimated Pick Time: 24 min
  Estimated Sort Time: 12 min
  Priority Orders: 1 (ORD0045)

  Order Breakdown:
    ORD0042: 8 lines, Zone A (4), Zone B (3), Zone C (1)
    ORD0043: 6 lines, Zone A (3), Zone B (2), Zone C (1)
    ORD0045: 9 lines [PRIORITY], Zone A (5), Zone B (3), Zone C (1)
    ORD0047: 5 lines, Zone A (2), Zone B (2), Zone C (1)
    ORD0048: 7 lines, Zone A (4), Zone B (2), Zone C (1)
    ORD0050: 7 lines, Zone A (3), Zone B (3), Zone C (1)

  Shared SKUs: SKU_A (6 orders), SKU_B (5 orders), SKU_D (4 orders)
```

**Batching Statistics:**

- Total Orders: 120
- Total Batches: 21
- Avg Batch Size: 5.7 orders
- Batch Size Distribution:
  - 3 orders: 2 batches
  - 4 orders: 4 batches
  - 5 orders: 6 batches
  - 6 orders: 7 batches
  - 7 orders: 2 batches

**Travel Savings:**

- Total Travel (Discrete): 51,000 ft
- Total Travel (Batched): 16,850 ft
- **Savings: 34,150 ft (67% reduction)**

**Productivity Impact:**

- Picker Hours (Discrete): 30.8 hours
- Picker Hours (Batched): 17.6 hours
- **Labor Savings: 13.2 hours (43% reduction)**

**Recommendations:**
1. Implement optimized batching strategy
2. Add 2 sort stations for peak capacity
3. Separate priority orders into express batches
4. Consider 8-tote carts for larger batches

---

## Questions to Ask

If you need more context:
1. What picking method do you currently use?
2. What's your average order size (lines)?
3. Do you have sorting capability after picking?
4. What's your cart capacity (orders and units)?
5. What's your daily order volume?
6. Do you have priority or rush orders?
7. What's your warehouse layout (zones, aisles)?
8. What's your current picks per hour?

---

## Related Skills

- **picker-routing-optimization**: For optimizing pick path within batches
- **wave-planning-optimization**: For wave design and release strategy
- **warehouse-slotting-optimization**: For SKU placement affecting batching
- **traveling-salesman-problem**: For TSP-based routing within batches
- **clustering-algorithms**: For order similarity and grouping
- **task-assignment-problem**: For assigning pickers to batches
- **order-fulfillment**: For overall fulfillment process design
