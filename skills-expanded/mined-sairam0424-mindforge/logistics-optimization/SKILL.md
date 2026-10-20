---
name: logistics-optimization
version: 1.0.0
min_mindforge_version: 10.2.0
status: stable
triggers: logistics optimization, route planning algorithm, fleet management system, warehouse management, last-mile delivery, supply chain visibility, shipment tracking, delivery optimization, logistics platform, transportation management, inventory routing, fulfillment optimization
---

# Skill — Logistics Optimization

## When this skill activates
This skill activates when building route planning algorithms, fleet management systems, warehouse management platforms, last-mile delivery optimization, supply chain visibility tools, shipment tracking, transportation management systems, or fulfillment optimization engines.

## Mandatory actions when this skill is active

### Before writing any code
1. Design route optimization algorithm: model as Vehicle Routing Problem with Time Windows (VRPTW), constraints (vehicle capacity, driver shift hours, customer time windows, priority deliveries), objective function (minimize total distance, balance workload across drivers, maximize on-time delivery %), solution methods (heuristic: nearest neighbor with 2-opt improvement, metaheuristic: simulated annealing, genetic algorithm, or exact: mixed-integer programming for <100 stops)
2. Model warehouse operations workflow: receiving (unload truck, quality check, barcode scan, put-away to optimal bin location) → storage (zone by velocity: fast-movers near packing, slow-movers in bulk) → picking (batch pick orders, wave pick by zone, pick-to-light system) → packing (right-sized box selection, void fill, label printing) → shipping (load truck, scan manifests, dispatch)
3. Map shipment lifecycle with visibility: order placed → warehouse allocated (nearest to destination with stock) → picked → packed → labeled → handed to carrier → in-transit (tracking events: picked up, at hub, out for delivery) → delivered (signature capture, photo proof) → exceptions handled (delivery failed, address incorrect, damaged)

### During implementation
- Implement route planning with real-time constraints: integrate maps API (Google Maps, Mapbox) for distance matrix (travel time between all location pairs), consider traffic patterns (historical data + real-time updates), vehicle constraints (capacity in cubic meters + weight, refrigeration for perishables), driver constraints (shift hours, break requirements, certifications for hazmat), time windows (hard: must deliver 2-4pm, soft: preferred 2-4pm with penalty)
- Build fleet management with telematics: integrate GPS devices (track vehicle location every 30s), monitor vehicle health (fuel level, engine diagnostics, tire pressure), driver behavior scoring (harsh braking, speeding, idle time), geofencing (alert when vehicle enters/exits depot or customer site), maintenance scheduling (oil change every 5000 miles, tire rotation every 10K miles)
- Design warehouse management system (WMS): inventory stored by SKU with bin location (aisle-rack-shelf), implement slotting optimization (place high-velocity items near packing, co-locate frequently ordered-together items), track lot numbers and expiry dates (FIFO/FEFO picking), support cycle counting (daily counts of A-items, weekly B-items, monthly C-items), integrate barcode scanners for all transactions
- Implement last-mile delivery optimization: cluster orders by geographic proximity (k-means clustering), assign to delivery vehicles (bin packing problem: maximize utilization), sequence stops (traveling salesman problem: minimize route distance), provide driver mobile app (turn-by-turn navigation, delivery instructions, photo capture, signature collection, real-time status updates)
- Build shipment tracking with carrier integration: integrate with carrier APIs (FedEx, UPS, USPS for tracking updates), parse webhooks (shipment picked up, in transit, out for delivery, delivered, exception), store tracking history (timestamp, location, status, notes), expose customer tracking page (order number lookup, map visualization, estimated delivery time), send proactive notifications (SMS/email at key events)

### After implementation
- Validate route optimization quality: measure total distance vs greedy baseline (should be 10-20% improvement), on-time delivery rate (>95%), vehicle utilization (>80% capacity filled), driver satisfaction (balanced workload, no overtime unless necessary), test with historical order data (replay last month's orders with optimized routes)
- Test warehouse efficiency metrics: measure pick rate (items per hour, target: 100 for standard, 200 for pick-to-light), packing time (minutes per order, target: <3 min), accuracy rate (>99.5% correct items, correct quantities), inventory accuracy (cycle count variance <1%), space utilization (>80% of racking filled)
- Execute delivery performance analysis: track key metrics (on-time delivery rate >95%, first-attempt delivery rate >90%, customer satisfaction score >4.5/5), identify failure modes (address incorrect, customer not home, access issues), measure exception resolution time (redelivery scheduled within 24 hours)

## Self-check before task completion
- [ ] Route optimization functional: VRPTW solver with constraints (capacity, time windows, driver shifts), objective function (minimize distance, balance workload)
- [ ] Fleet management integrated: GPS tracking (30s updates), telematics (vehicle health, driver behavior), geofencing (depot/customer alerts), maintenance scheduling
- [ ] Warehouse operations optimized: inventory slotting (velocity-based placement), picking strategies (batch, wave, pick-to-light), barcode scanning at all touchpoints
- [ ] Last-mile delivery optimized: geographic clustering, bin packing assignment, TSP sequencing, driver mobile app (navigation, photo/signature, status updates)
- [ ] Shipment tracking real-time: carrier API integration (FedEx/UPS/USPS), webhook parsing, tracking history storage, customer tracking page, proactive notifications
- [ ] Performance metrics tracked: route distance improvement (10-20% vs baseline), on-time delivery >95%, pick rate 100+ items/hr, inventory accuracy >99.5%
- [ ] Exception handling robust: delivery failures (address incorrect, not home), redelivery scheduling (within 24h), customer notifications (SMS/email)
