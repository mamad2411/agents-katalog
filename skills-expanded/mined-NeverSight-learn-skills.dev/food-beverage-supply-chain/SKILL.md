---
name: food-beverage-supply-chain
description: When the user wants to optimize food and beverage supply chains, manage perishability, ensure food safety, or handle retail distribution. Also use when the user mentions "food supply chain," "beverage distribution," "HACCP," "food safety," "perishable logistics," "shelf life management," "FEFO," "farm to fork," "CPG distribution," "grocery supply chain," or "fresh produce logistics." For retail allocation, see retail-allocation. For promotional planning, see promotional-planning.
---

# Food & Beverage Supply Chain

You are an expert in food and beverage supply chain management, food safety compliance, and perishable product logistics. Your goal is to help optimize complex multi-temperature supply networks while ensuring product freshness, food safety, regulatory compliance, and efficient retail distribution.

## Initial Assessment

Before optimizing food & beverage supply chains, understand:

1. **Product Portfolio**
   - Product categories? (fresh, frozen, shelf-stable, refrigerated)
   - Perishability level? (hours, days, weeks, months)
   - Temperature requirements? (ambient, refrigerated 2-8°C, frozen)
   - Packaging types? (bulk, consumer packaged goods, foodservice)
   - Seasonality? (year-round, seasonal peaks)

2. **Supply Chain Structure**
   - Sourcing model? (direct farm, co-packers, own manufacturing)
   - Distribution channels? (retail, foodservice, direct-to-consumer, export)
   - Network structure? (regional DCs, cross-docks, direct store delivery)
   - Cold chain capabilities?
   - Co-manufacturing partnerships?

3. **Regulatory & Quality**
   - Regulatory requirements? (FDA FSMA, HACCP, GFSI, organic)
   - Certifications needed? (SQF, BRC, IFS, Kosher, Halal)
   - Allergen management requirements?
   - Traceability depth? (one-up/one-down, farm to fork)
   - Food safety culture maturity?

4. **Market & Operations**
   - Customer types? (grocery chains, convenience, club, online)
   - Promotional intensity? (high, moderate, low)
   - Private label vs. branded?
   - Service level targets? (on-time, in-full, freshness)
   - Current waste levels?

---

## Food & Beverage Supply Chain Framework

### Value Chain Structure

**Farm to Fork Supply Chain:**

```
Agricultural Production / Raw Materials
  ↓
Primary Processing (cleaning, sorting, initial processing)
  ↓
Secondary Processing / Manufacturing
  ↓
Co-Packers / Contract Manufacturers
  ↓
Distribution Centers (multi-temperature)
  ↓
Retail Distribution
  ├─ Grocery Retailers
  ├─ Foodservice (restaurants, institutions)
  ├─ Convenience Stores
  └─ Direct-to-Consumer
  ↓
Consumers
```

**Key Regulations:**

- **FSMA (Food Safety Modernization Act)**: Preventive controls, traceability
- **HACCP (Hazard Analysis Critical Control Points)**: Food safety system
- **GFSI (Global Food Safety Initiative)**: Standards (SQF, BRC, IFS, FSSC 22000)
- **GMP (Good Manufacturing Practices)**: Manufacturing standards
- **Country of Origin Labeling**: COOL requirements
- **Allergen Labeling**: FDA and EU regulations

---

## Shelf Life & Freshness Management

### FEFO (First Expired, First Out) Optimization

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class ShelfLifeManager:
    """
    Manage shelf life and freshness for perishable products
    """

    def __init__(self, products_df):
        """
        Initialize shelf life manager

        Parameters:
        - products_df: product master with shelf life parameters
        """
        self.products = products_df

    def calculate_remaining_shelf_life(self, inventory_df, current_date):
        """
        Calculate remaining shelf life for inventory

        Parameters:
        - inventory_df: current inventory with production/expiry dates
        - current_date: as-of date for calculation

        Returns:
        - inventory with remaining shelf life metrics
        """

        inventory_with_rsl = inventory_df.copy()

        for idx, item in inventory_with_rsl.iterrows():
            product_id = item['product_id']
            production_date = item.get('production_date')
            expiry_date = item.get('expiry_date')

            # Get product shelf life
            product_info = self.products[
                self.products['product_id'] == product_id
            ].iloc[0]

            total_shelf_life_days = product_info['shelf_life_days']

            # Calculate remaining shelf life
            if expiry_date:
                remaining_days = (expiry_date - current_date).days
            elif production_date:
                age_days = (current_date - production_date).days
                remaining_days = total_shelf_life_days - age_days
            else:
                remaining_days = None

            # Calculate as percentage
            remaining_pct = (remaining_days / total_shelf_life_days * 100
                           if remaining_days and total_shelf_life_days > 0 else None)

            inventory_with_rsl.loc[idx, 'remaining_shelf_life_days'] = remaining_days
            inventory_with_rsl.loc[idx, 'remaining_shelf_life_pct'] = remaining_pct

            # Classify freshness
            inventory_with_rsl.loc[idx, 'freshness_category'] = self._classify_freshness(
                remaining_pct
            )

        return inventory_with_rsl

    def _classify_freshness(self, remaining_pct):
        """Classify product freshness"""

        if remaining_pct is None:
            return 'unknown'
        elif remaining_pct >= 67:
            return 'fresh'
        elif remaining_pct >= 33:
            return 'medium'
        elif remaining_pct >= 0:
            return 'near_expiry'
        else:
            return 'expired'

    def optimize_fefo_picking(self, order, available_inventory):
        """
        Optimize picking sequence using FEFO logic

        Parameters:
        - order: customer order with required quantities
        - available_inventory: inventory with expiry dates

        Returns:
        - picking instructions prioritizing oldest stock
        """

        picking_plan = []

        for order_line in order:
            product_id = order_line['product_id']
            quantity_needed = order_line['quantity']

            # Get available inventory for this product, sorted by expiry
            product_inventory = available_inventory[
                available_inventory['product_id'] == product_id
            ].sort_values('expiry_date')

            quantity_allocated = 0

            for idx, inv_lot in product_inventory.iterrows():
                if quantity_allocated >= quantity_needed:
                    break

                # How much from this lot?
                available_qty = inv_lot['quantity_available']
                pick_qty = min(available_qty, quantity_needed - quantity_allocated)

                picking_plan.append({
                    'order_id': order_line['order_id'],
                    'product_id': product_id,
                    'lot_number': inv_lot['lot_number'],
                    'location': inv_lot['warehouse_location'],
                    'expiry_date': inv_lot['expiry_date'],
                    'pick_quantity': pick_qty,
                    'remaining_shelf_life_days': inv_lot.get('remaining_shelf_life_days'),
                    'pick_priority': 'FEFO'
                })

                quantity_allocated += pick_qty

            # Check if order is complete
            if quantity_allocated < quantity_needed:
                picking_plan.append({
                    'order_id': order_line['order_id'],
                    'product_id': product_id,
                    'status': 'insufficient_inventory',
                    'shortfall': quantity_needed - quantity_allocated
                })

        return pd.DataFrame(picking_plan)

    def identify_slow_moving_inventory(self, inventory_df, sales_velocity_df,
                                      near_expiry_threshold_days=30):
        """
        Identify at-risk inventory (slow moving + near expiry)

        Parameters:
        - inventory_df: current inventory with dates
        - sales_velocity_df: historical sales rates
        - near_expiry_threshold_days: days to expiry threshold

        Returns:
        - at-risk inventory with recommended actions
        """

        at_risk_inventory = []

        for idx, inv in inventory_df.iterrows():
            product_id = inv['product_id']
            quantity = inv['quantity_available']
            remaining_shelf_life = inv.get('remaining_shelf_life_days', 999)

            # Get sales velocity
            velocity = sales_velocity_df[
                sales_velocity_df['product_id'] == product_id
            ]

            if len(velocity) > 0:
                avg_daily_sales = velocity['avg_daily_units'].iloc[0]
                days_of_supply = quantity / avg_daily_sales if avg_daily_sales > 0 else 999
            else:
                days_of_supply = 999

            # Identify at-risk
            if remaining_shelf_life < near_expiry_threshold_days:
                risk_level = 'high' if days_of_supply > remaining_shelf_life else 'medium'

                # Recommend action
                if days_of_supply > remaining_shelf_life * 1.5:
                    action = 'markdown_promotion_immediate'
                elif days_of_supply > remaining_shelf_life:
                    action = 'redistribute_to_high_velocity_locations'
                else:
                    action = 'monitor_daily'

                at_risk_inventory.append({
                    'product_id': product_id,
                    'lot_number': inv['lot_number'],
                    'quantity': quantity,
                    'remaining_shelf_life_days': remaining_shelf_life,
                    'days_of_supply': days_of_supply,
                    'risk_level': risk_level,
                    'recommended_action': action,
                    'estimated_value_at_risk': quantity * inv.get('unit_cost', 0)
                })

        return pd.DataFrame(at_risk_inventory)

    def calculate_minimum_shelf_life_delivery(self, product_id, channel):
        """
        Calculate minimum remaining shelf life at delivery

        Parameters:
        - product_id: product identifier
        - channel: delivery channel (retail, foodservice, export)

        Returns:
        - minimum shelf life requirements
        """

        product_info = self.products[
            self.products['product_id'] == product_id
        ].iloc[0]

        total_shelf_life = product_info['shelf_life_days']

        # Industry standards by channel
        if channel == 'retail':
            # Retail typically requires 67-80% remaining shelf life
            min_rsl_pct = 0.67
        elif channel == 'foodservice':
            # Foodservice can accept 50% remaining
            min_rsl_pct = 0.50
        elif channel == 'export':
            # Export needs more (transit time + customer shelf life)
            min_rsl_pct = 0.80
        else:
            min_rsl_pct = 0.67

        min_rsl_days = int(total_shelf_life * min_rsl_pct)

        return {
            'product_id': product_id,
            'channel': channel,
            'total_shelf_life_days': total_shelf_life,
            'min_rsl_pct': min_rsl_pct * 100,
            'min_rsl_days': min_rsl_days,
            'reject_if_less_than_days': min_rsl_days
        }


# Example usage
products = pd.DataFrame({
    'product_id': ['PROD_001', 'PROD_002', 'PROD_003'],
    'product_name': ['Fresh Milk', 'Yogurt', 'Cheese'],
    'shelf_life_days': [14, 45, 90]
})

inventory = pd.DataFrame({
    'product_id': ['PROD_001', 'PROD_001', 'PROD_002'],
    'lot_number': ['LOT_A', 'LOT_B', 'LOT_C'],
    'production_date': pd.to_datetime(['2025-01-15', '2025-01-18', '2025-01-10']),
    'expiry_date': pd.to_datetime(['2025-01-29', '2025-02-01', '2025-02-24']),
    'quantity_available': [100, 150, 200],
    'warehouse_location': ['A-1-1', 'A-1-2', 'B-2-1'],
    'unit_cost': [2.50, 2.50, 3.00]
})

slm = ShelfLifeManager(products)

# Calculate remaining shelf life
current_date = datetime(2025, 1, 26)
inventory_rsl = slm.calculate_remaining_shelf_life(inventory, current_date)

print("Inventory with Remaining Shelf Life:")
print(inventory_rsl[['product_id', 'lot_number', 'remaining_shelf_life_days',
                     'remaining_shelf_life_pct', 'freshness_category']])
```

---

## Food Safety & Traceability

### HACCP & Traceability System

```python
class FoodSafetyManager:
    """
    Manage food safety and traceability requirements
    """

    def __init__(self):
        self.critical_control_points = []

    def define_haccp_plan(self, product_category):
        """
        Define HACCP critical control points for product category

        Parameters:
        - product_category: type of food product

        Returns:
        - HACCP plan with CCPs
        """

        haccp_plan = {
            'product_category': product_category,
            'hazard_analysis': [],
            'critical_control_points': []
        }

        # Define CCPs based on product type
        if product_category in ['fresh_produce', 'salad', 'cut_fruit']:
            haccp_plan['critical_control_points'] = [
                {
                    'ccp_id': 'CCP-1',
                    'step': 'receiving',
                    'hazard': 'biological_contamination',
                    'critical_limit': 'temperature_<=_41F',
                    'monitoring': 'check_temp_every_lot',
                    'corrective_action': 'reject_if_out_of_range'
                },
                {
                    'ccp_id': 'CCP-2',
                    'step': 'washing',
                    'hazard': 'pathogen_survival',
                    'critical_limit': 'sanitizer_concentration_50-200ppm',
                    'monitoring': 'test_every_2_hours',
                    'corrective_action': 'adjust_concentration'
                },
                {
                    'ccp_id': 'CCP-3',
                    'step': 'cold_storage',
                    'hazard': 'pathogen_growth',
                    'critical_limit': 'temperature_<=_41F',
                    'monitoring': 'continuous_monitoring',
                    'corrective_action': 'investigate_temperature_excursion'
                }
            ]

        elif product_category in ['cooked_meat', 'ready_to_eat']:
            haccp_plan['critical_control_points'] = [
                {
                    'ccp_id': 'CCP-1',
                    'step': 'cooking',
                    'hazard': 'pathogen_survival',
                    'critical_limit': 'internal_temp_>=_165F',
                    'monitoring': 'check_temp_every_batch',
                    'corrective_action': 'continue_cooking_until_temp_reached'
                },
                {
                    'ccp_id': 'CCP-2',
                    'step': 'cooling',
                    'hazard': 'pathogen_growth',
                    'critical_limit': 'cool_to_41F_within_4hours',
                    'monitoring': 'time_temperature_logs',
                    'corrective_action': 'discard_if_cooling_too_slow'
                },
                {
                    'ccp_id': 'CCP-3',
                    'step': 'packaging',
                    'hazard': 'recontamination',
                    'critical_limit': 'environmental_monitoring_negative',
                    'monitoring': 'swab_testing_weekly',
                    'corrective_action': 'sanitize_and_retest'
                }
            ]

        elif product_category in ['juice', 'beverage']:
            haccp_plan['critical_control_points'] = [
                {
                    'ccp_id': 'CCP-1',
                    'step': 'pasteurization',
                    'hazard': 'pathogen_survival',
                    'critical_limit': 'temp_time_combination_per_FDA',
                    'monitoring': 'continuous_chart_recorder',
                    'corrective_action': 'repasteurize_or_discard'
                },
                {
                    'ccp_id': 'CCP-2',
                    'step': 'hot_fill',
                    'hazard': 'post_pasteurization_contamination',
                    'critical_limit': 'fill_temp_>=_185F',
                    'monitoring': 'check_every_hour',
                    'corrective_action': 'hold_and_reheat'
                }
            ]

        return haccp_plan

    def implement_traceability(self, product_lot, supply_chain_events):
        """
        Implement one-up/one-down traceability

        Parameters:
        - product_lot: finished product lot information
        - supply_chain_events: upstream and downstream transactions

        Returns:
        - complete traceability record
        """

        traceability_record = {
            'finished_product': {
                'lot_number': product_lot['lot_number'],
                'product_id': product_lot['product_id'],
                'production_date': product_lot['production_date'],
                'quantity': product_lot['quantity']
            },
            'one_up': [],  # Ingredients and packaging received
            'one_down': []  # Customers/locations shipped to
        }

        # One-up traceability (ingredients)
        for ingredient in product_lot.get('ingredients', []):
            traceability_record['one_up'].append({
                'supplier': ingredient['supplier'],
                'ingredient_id': ingredient['ingredient_id'],
                'lot_number': ingredient['lot_number'],
                'receive_date': ingredient['receive_date'],
                'quantity_used': ingredient['quantity_used']
            })

        # One-down traceability (shipments)
        lot_shipments = [
            e for e in supply_chain_events
            if e['type'] == 'shipment' and e['lot_number'] == product_lot['lot_number']
        ]

        for shipment in lot_shipments:
            traceability_record['one_down'].append({
                'customer': shipment['customer'],
                'ship_date': shipment['ship_date'],
                'quantity_shipped': shipment['quantity'],
                'destination': shipment['destination']
            })

        return traceability_record

    def execute_mock_recall(self, recalled_lot, traceability_data):
        """
        Execute mock recall to test traceability system

        Parameters:
        - recalled_lot: lot number being recalled
        - traceability_data: complete traceability records

        Returns:
        - recall execution report
        """

        start_time = datetime.now()

        # Find lot traceability
        lot_trace = traceability_data.get(recalled_lot, {})

        if not lot_trace:
            return {
                'success': False,
                'error': 'lot_not_found_in_traceability_system'
            }

        # Identify affected ingredients (one-up)
        affected_ingredients = lot_trace.get('one_up', [])

        # Identify affected customers (one-down)
        affected_customers = lot_trace.get('one_down', [])

        # Calculate execution time
        end_time = datetime.now()
        execution_time_minutes = (end_time - start_time).total_seconds() / 60

        # Total quantity to recall
        total_quantity = sum(c['quantity_shipped'] for c in affected_customers)

        recall_report = {
            'recalled_lot': recalled_lot,
            'execution_time_minutes': execution_time_minutes,
            'meets_target_4hours': execution_time_minutes <= 240,  # 4 hours
            'affected_ingredients': len(affected_ingredients),
            'affected_customers': len(affected_customers),
            'total_quantity_to_recall': total_quantity,
            'customer_list': [c['customer'] for c in affected_customers],
            'notification_method': 'email_phone_fax',
            'next_steps': [
                'issue_recall_notification_to_customers',
                'coordinate_product_return_or_destruction',
                'investigate_root_cause',
                'implement_corrective_actions',
                'notify_FDA_if_required'
            ]
        }

        return recall_report

    def manage_allergen_control(self, product_id, ingredients, facility_allergens):
        """
        Manage allergen controls and labeling

        Parameters:
        - product_id: product being manufactured
        - ingredients: list of ingredients with allergens
        - facility_allergens: allergens present in facility

        Returns:
        - allergen control plan
        """

        # Major allergens (FDA Big 8 + sesame)
        major_allergens = [
            'milk', 'eggs', 'fish', 'shellfish', 'tree_nuts',
            'peanuts', 'wheat', 'soybeans', 'sesame'
        ]

        # Identify allergens in product
        product_allergens = set()

        for ingredient in ingredients:
            if 'allergens' in ingredient:
                product_allergens.update(ingredient['allergens'])

        # Check for cross-contact risk
        cross_contact_risk = []

        for allergen in facility_allergens:
            if allergen not in product_allergens:
                # Allergen in facility but not in product = cross-contact risk
                cross_contact_risk.append(allergen)

        # Determine controls needed
        controls = []

        if len(cross_contact_risk) > 0:
            controls.extend([
                'dedicated_production_line_or_thorough_cleaning',
                'allergen_cleaning_verification_testing',
                'production_scheduling_to_minimize_risk',
                'may_contain_labeling_if_risk_cannot_be_eliminated'
            ])

        allergen_plan = {
            'product_id': product_id,
            'contains_allergens': list(product_allergens),
            'cross_contact_risks': cross_contact_risk,
            'required_label_statement': self._generate_allergen_statement(
                product_allergens
            ),
            'controls_required': controls,
            'requires_allergen_clean': len(cross_contact_risk) > 0
        }

        return allergen_plan

    def _generate_allergen_statement(self, allergens):
        """Generate allergen labeling statement"""

        if len(allergens) == 0:
            return None

        allergen_list = ', '.join(sorted(allergens))

        return f"Contains: {allergen_list}"


# Example
fsm = FoodSafetyManager()

# HACCP plan
haccp = fsm.define_haccp_plan('fresh_produce')
print(f"HACCP Plan for Fresh Produce - {len(haccp['critical_control_points'])} CCPs")

# Mock recall
traceability_data = {
    'LOT_123456': {
        'one_up': [
            {'supplier': 'Farm_A', 'ingredient_id': 'Lettuce', 'lot_number': 'F001',
             'receive_date': '2025-01-20', 'quantity_used': 500}
        ],
        'one_down': [
            {'customer': 'Grocery_Chain_A', 'ship_date': '2025-01-22',
             'quantity': 100, 'destination': 'DC_East'},
            {'customer': 'Grocery_Chain_B', 'ship_date': '2025-01-23',
             'quantity': 150, 'destination': 'DC_West'}
        ]
    }
}

recall = fsm.execute_mock_recall('LOT_123456', traceability_data)
print(f"\nMock Recall Results:")
print(f"Affected Customers: {recall['affected_customers']}")
print(f"Quantity to Recall: {recall['total_quantity_to_recall']} units")
```

---

## Multi-Temperature Network Optimization

### Distribution Network Design

```python
from pulp import *

class FoodDistributionOptimizer:
    """
    Optimize multi-temperature food distribution network
    """

    def __init__(self, facilities, customers, products):
        self.facilities = facilities
        self.customers = customers
        self.products = products

    def optimize_dc_network(self):
        """
        Optimize distribution center network for multi-temperature products

        Considers:
        - Ambient, refrigerated, frozen storage needs
        - Transportation costs and modes
        - Service level requirements (freshness)
        - Facility costs

        Returns:
        - optimal network configuration
        """

        prob = LpProblem("Food_Distribution_Network", LpMinimize)

        # Decision variables: assign customer to DC
        x = {}

        for facility in self.facilities:
            for customer in self.customers:
                x[facility['id'], customer['id']] = LpVariable(
                    f"Assign_{facility['id']}_{customer['id']}",
                    cat='Binary'
                )

        # Use facility or not
        y = {}
        for facility in self.facilities:
            y[facility['id']] = LpVariable(f"Use_{facility['id']}", cat='Binary')

        # Objective: minimize total cost
        # Fixed costs + transportation costs

        fixed_costs = lpSum([
            facility['fixed_cost_annual'] * y[facility['id']]
            for facility in self.facilities
        ])

        transport_costs = lpSum([
            facility['transport_cost_per_mile'] *
            self._distance(facility['location'], customer['location']) *
            customer['annual_volume_cases'] *
            x[facility['id'], customer['id']]
            for facility in self.facilities
            for customer in self.customers
        ])

        prob += fixed_costs + transport_costs

        # Constraints

        # Each customer assigned to exactly one DC
        for customer in self.customers:
            prob += lpSum([
                x[facility['id'], customer['id']]
                for facility in self.facilities
            ]) == 1

        # Can only assign to open DCs
        for facility in self.facilities:
            for customer in self.customers:
                prob += x[facility['id'], customer['id']] <= y[facility['id']]

        # DC capacity constraints (by temperature zone)
        for facility in self.facilities:
            # Ambient capacity
            ambient_volume = lpSum([
                customer['annual_volume_cases'] *
                self._ambient_pct(customer['product_mix']) *
                x[facility['id'], customer['id']]
                for customer in self.customers
            ])
            prob += ambient_volume <= facility['capacity_ambient_cases']

            # Refrigerated capacity
            refrigerated_volume = lpSum([
                customer['annual_volume_cases'] *
                self._refrigerated_pct(customer['product_mix']) *
                x[facility['id'], customer['id']]
                for customer in self.customers
            ])
            prob += refrigerated_volume <= facility['capacity_refrigerated_cases']

            # Frozen capacity
            frozen_volume = lpSum([
                customer['annual_volume_cases'] *
                self._frozen_pct(customer['product_mix']) *
                x[facility['id'], customer['id']]
                for customer in self.customers
            ])
            prob += frozen_volume <= facility['capacity_frozen_cases']

        # Service level constraint: max distance for fresh products
        for facility in self.facilities:
            for customer in self.customers:
                if customer.get('requires_fresh_daily_delivery'):
                    # Fresh products need close proximity
                    distance = self._distance(facility['location'], customer['location'])
                    prob += distance * x[facility['id'], customer['id']] <= 150  # miles

        # Solve
        prob.solve(PULP_CBC_CMD(msg=0))

        # Extract solution
        network_design = {
            'total_cost_annual': value(prob.objective),
            'facilities_used': [],
            'customer_assignments': []
        }

        for facility in self.facilities:
            if y[facility['id']].varValue > 0.5:
                network_design['facilities_used'].append(facility['id'])

        for facility in self.facilities:
            for customer in self.customers:
                if x[facility['id'], customer['id']].varValue > 0.5:
                    network_design['customer_assignments'].append({
                        'customer': customer['id'],
                        'assigned_dc': facility['id'],
                        'distance_miles': self._distance(
                            facility['location'], customer['location']
                        )
                    })

        return network_design

    def _distance(self, loc1, loc2):
        """Calculate distance between two locations (simplified)"""
        # Simplified Euclidean distance
        return np.sqrt((loc1[0] - loc2[0])**2 + (loc1[1] - loc2[1])**2)

    def _ambient_pct(self, product_mix):
        """Percentage of ambient products"""
        return product_mix.get('ambient', 0.4)

    def _refrigerated_pct(self, product_mix):
        """Percentage of refrigerated products"""
        return product_mix.get('refrigerated', 0.4)

    def _frozen_pct(self, product_mix):
        """Percentage of frozen products"""
        return product_mix.get('frozen', 0.2)
```

---

## Promotional Planning & Demand Management

### Promotional Demand Forecasting

```python
class PromotionalDemandPlanner:
    """
    Manage promotional demand planning for food/beverage CPG
    """

    def __init__(self, historical_promotions):
        self.historical_promotions = historical_promotions

    def forecast_promotional_lift(self, promotion_details, baseline_forecast):
        """
        Forecast demand lift from promotion

        Parameters:
        - promotion_details: promotion mechanics (discount, display, feature)
        - baseline_forecast: baseline demand without promotion

        Returns:
        - promotional forecast
        """

        # Promotional lift factors based on mechanics
        discount_pct = promotion_details.get('discount_pct', 0)
        has_display = promotion_details.get('display', False)
        has_feature = promotion_details.get('feature_ad', False)

        # Base lift from discount
        if discount_pct >= 30:
            discount_lift = 3.0  # 200% lift
        elif discount_pct >= 20:
            discount_lift = 2.0  # 100% lift
        elif discount_pct >= 10:
            discount_lift = 1.5  # 50% lift
        else:
            discount_lift = 1.0  # No lift

        # Display lift (incremental)
        display_lift = 1.3 if has_display else 1.0

        # Feature ad lift (incremental)
        feature_lift = 1.2 if has_feature else 1.0

        # Combined lift (multiplicative)
        total_lift_factor = discount_lift * display_lift * feature_lift

        # Apply to baseline
        promotional_forecast = baseline_forecast * total_lift_factor

        # Account for pantry loading and post-promotion dip
        # Pre-promotion dip
        pre_promo_weeks = promotion_details.get('weeks_before', 2)
        pre_promo_dip_factor = 0.85  # 15% dip

        # Post-promotion dip
        post_promo_weeks = promotion_details.get('weeks_after', 3)
        post_promo_dip_factor = 0.70  # 30% dip

        forecast_profile = {
            'pre_promotion': {
                'weeks': pre_promo_weeks,
                'forecast': baseline_forecast * pre_promo_dip_factor,
                'factor': pre_promo_dip_factor
            },
            'promotion': {
                'weeks': promotion_details.get('duration_weeks', 1),
                'forecast': promotional_forecast,
                'lift_factor': total_lift_factor
            },
            'post_promotion': {
                'weeks': post_promo_weeks,
                'forecast': baseline_forecast * post_promo_dip_factor,
                'factor': post_promo_dip_factor
            }
        }

        return forecast_profile

    def optimize_promotional_calendar(self, products, constraints):
        """
        Optimize promotional calendar considering manufacturing and supply constraints

        Parameters:
        - products: list of products with promotion plans
        - constraints: manufacturing capacity, cash flow, retailer limits

        Returns:
        - optimized promotional calendar
        """

        # Simplified optimization
        # In practice, would use LP/MIP optimization

        promotional_calendar = []

        for product in products:
            for promo in product.get('planned_promotions', []):
                # Check constraints
                feasible = True

                # Manufacturing capacity check
                peak_demand = promo['forecast'] * promo['lift_factor']
                if peak_demand > constraints.get('max_production_capacity', 999999):
                    feasible = False

                # Retailer constraint: max promotions per period
                period_promos = len([
                    p for p in promotional_calendar
                    if p['week'] == promo['week']
                ])

                if period_promos >= constraints.get('max_concurrent_promos', 5):
                    feasible = False

                if feasible:
                    promotional_calendar.append({
                        'product_id': product['product_id'],
                        'week': promo['week'],
                        'retailer': promo['retailer'],
                        'mechanics': promo['mechanics'],
                        'forecast': promo['forecast'],
                        'status': 'approved'
                    })
                else:
                    promotional_calendar.append({
                        'product_id': product['product_id'],
                        'week': promo['week'],
                        'status': 'deferred_constraint_violation'
                    })

        return pd.DataFrame(promotional_calendar)
```

---

## Tools & Libraries

### Python Libraries

**Supply Chain Optimization:**
- `pulp`: Linear programming for network optimization
- `scipy`: Statistical methods
- `networkx`: Supply network modeling

**Data Analysis:**
- `pandas`: Data manipulation and inventory management
- `numpy`: Numerical computations
- `matplotlib`, `seaborn`: Visualization

**Forecasting:**
- `statsmodels`: Time series forecasting
- `prophet`: Demand forecasting with seasonality
- `sklearn`: ML-based forecasting

### Commercial Software

**ERP/Supply Chain Planning:**
- **SAP S/4HANA**: Enterprise resource planning
- **Oracle Food & Beverage**: Industry-specific ERP
- **Microsoft Dynamics 365**: Supply chain management
- **Blue Yonder (JDA)**: Demand and supply planning

**Warehouse Management:**
- **Manhattan WMS**: Warehouse management with FEFO
- **SAP EWM**: Extended warehouse management
- **JDA WMS**: Food-grade warehouse management
- **HighJump**: WMS for food distribution

**Food Safety & Traceability:**
- **FoodLogiQ**: Farm to fork traceability
- **SafetyChain**: Food safety and quality management
- **Aptean Food & Beverage**: ERP with traceability
- **rfXcel**: Serialization and traceability
- **FarmSoft**: Agricultural traceability

**Transportation:**
- **Descartes**: Route optimization and TMS
- **Blue Yonder Transportation**: TMS with temperature monitoring
- **MercuryGate**: Multi-temperature TMS

---

## Common Challenges & Solutions

### Challenge: Managing Perishability & Waste

**Problem:**
- Short shelf lives (days to weeks)
- High waste/spoilage rates (3-8% of sales)
- Slow-moving inventory near expiry
- Markdowns eroding margin

**Solutions:**
- **FEFO implementation**: Strict first-expired, first-out
- **Demand forecasting**: Reduce forecast error, especially for promotions
- **Dynamic pricing**: Markdown near-expiry products automatically
- **Inventory redistribution**: Move slow stock to high-velocity stores
- **Shorter order cycles**: Order more frequently in smaller quantities
- **Direct store delivery**: Bypass DC for ultra-fresh products
- **Waste tracking**: Measure and analyze root causes

### Challenge: Cold Chain Integrity

**Problem:**
- Temperature excursions during storage and transport
- Product quality degradation
- Food safety risks
- No real-time visibility

**Solutions:**
- **Temperature monitoring**: IoT sensors with real-time alerts
- **Insulated transport**: Refrigerated trucks and trailers
- **Cross-dock operations**: Minimize dwell time in temp zones
- **Preventive maintenance**: Regular equipment servicing
- **Driver training**: Proper door management and temp checks
- **Packaging innovation**: Phase change materials for last mile
- **Route optimization**: Minimize transit time for fresh products

### Challenge: Promotional Demand Volatility

**Problem:**
- 40-60% of food/beverage sales on promotion
- Demand spikes of 2-5x baseline
- Post-promotion dips
- Forecast accuracy suffers
- Inventory imbalances

**Solutions:**
- **Promotional forecasting models**: Separate baseline from lift
- **Pre-build inventory**: Manufacture ahead of promotion
- **Flexible manufacturing**: Rapid changeovers
- **Retailer collaboration**: Advance promotional calendars
- **Mix optimization**: Balance high and low promoted weeks
- **Co-packer flexibility**: Surge capacity through CMs
- **Safety stock strategies**: Higher stock for promotional SKUs

### Challenge: Seasonal Supply Variability

**Problem:**
- Agricultural products seasonal (tomatoes, berries, etc.)
- Quality and pricing fluctuate
- Supply disruptions (weather, pests)
- Need year-round supply

**Solutions:**
- **Geographic diversity**: Source from multiple growing regions
- **Forward contracts**: Lock in supply and pricing
- **Alternative sources**: Import during off-season
- **Product reformulation**: Design for available ingredients
- **Inventory building**: Process and freeze peak season product
- **Supplier relationships**: Long-term partnerships with growers
- **Vertical integration**: Own or partner on farms

### Challenge: Food Safety & Recalls

**Problem:**
- Foodborne illness outbreaks
- Product recalls (contamination, allergen, foreign material)
- Brand damage and costs
- Complex traceability requirements

**Solutions:**
- **Robust HACCP**: Well-designed food safety systems
- **Supplier audits**: Verify ingredient safety upstream
- **Environmental monitoring**: Detect pathogens in facility
- **Traceability systems**: One-up/one-down digitized
- **Mock recalls**: Quarterly practice drills (<4 hour target)
- **Food safety culture**: Training and accountability
- **Rapid response**: Crisis management procedures
- **Insurance**: Product recall and contamination coverage

---

## Output Format

### Food & Beverage Supply Chain Report

**Executive Summary:**
- Product categories overview (fresh, frozen, shelf-stable)
- Key supply chain metrics
- Food safety and quality status
- Major initiatives

**Freshness & Waste Metrics:**

| Category | Avg Shelf Life | Inventory Days | Waste % | Near-Expiry Value | FEFO Compliance |
|----------|----------------|----------------|---------|-------------------|-----------------|
| Fresh Dairy | 14 days | 4 days | 2.8% | $45,000 | 98% |
| Fresh Produce | 7 days | 2 days | 5.2% | $82,000 | 95% |
| Frozen Foods | 365 days | 45 days | 0.5% | $12,000 | 90% |
| Beverages | 180 days | 30 days | 1.2% | $28,000 | 92% |
| **Total** | - | - | **2.4%** | **$167,000** | **94%** |

**Supply Chain Performance:**

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| OTIF Delivery | 94% | 96% | ⚠ Yellow |
| Inventory Turns | 18.5 | 20.0 | ⚠ Yellow |
| Waste Rate | 2.4% | <2.0% | ⚠ Yellow |
| Order Fill Rate | 97% | 98% | ⚠ Yellow |
| Cold Chain Compliance | 99.2% | 99.5% | ⚠ Yellow |

**Food Safety Status:**

| Metric | Status |
|--------|--------|
| HACCP Compliance | ✓ Compliant |
| Last Mock Recall Time | 2.5 hours (target <4 hrs) |
| Environmental Monitoring | All negative |
| Supplier Audits Current | 100% |
| GFSI Certification | SQF Level 2 |
| FDA Inspections | No observations |

**Promotional Performance:**

| Month | Promotions | Forecast Accuracy | Stockouts | Excess Inventory |
|-------|-----------|-------------------|-----------|------------------|
| Jan | 12 | 78% | 2 | $45,000 |
| Feb | 15 | 82% | 1 | $38,000 |
| Mar | 18 | 75% | 4 | $67,000 |

**Action Items:**
1. Reduce dairy waste from 2.8% to <2.0% - implement dynamic pricing
2. Improve promotional forecast accuracy - refine lift models
3. Complete cold chain upgrade at DC3 - install backup refrigeration
4. Launch traceability system digitization - complete by Q2
5. Resolve produce stockouts - add backup supplier

---

## Questions to Ask

If you need more context:
1. What product categories? (fresh, frozen, shelf-stable, beverages)
2. What are the shelf lives? (days, weeks, months)
3. What temperature requirements? (ambient, refrigerated, frozen)
4. What distribution channels? (retail, foodservice, DTC, export)
5. What are current waste/spoilage rates?
6. What food safety certifications are needed? (HACCP, GFSI, organic)
7. How promotional is the business? (% sales on promotion)
8. What are the main supply chain challenges?

---

## Related Skills

- **inventory-optimization**: For safety stock and inventory policies
- **demand-forecasting**: For baseline and promotional forecasting
- **network-design**: For distribution network optimization
- **route-optimization**: For delivery route planning
- **warehouse-slotting-optimization**: For FEFO-based slotting
- **promotional-planning**: For CPG promotional calendars
- **retail-allocation**: For store allocation and replenishment
- **co-packing-management**: For contract manufacturing
- **cold-chain**: For temperature-controlled logistics
- **quality-management**: For food safety and HACCP
- **seasonal-planning**: For seasonal demand planning
- **shelf-life-management**: For expiry date management
