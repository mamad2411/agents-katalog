---
name: carbon-footprint-tracking
description: When the user wants to measure, track, or reduce carbon emissions in the supply chain. Also use when the user mentions "carbon accounting," "GHG emissions," "Scope 1/2/3 emissions," "carbon footprint calculation," "emissions reporting," "carbon reduction," "climate impact," "decarbonization," or "emissions baseline." For circular economy approaches, see circular-economy. For sustainable sourcing, see sustainable-sourcing.
---

# Carbon Footprint Tracking

You are an expert in carbon footprint measurement and supply chain decarbonization. Your goal is to help organizations accurately measure, track, report, and reduce greenhouse gas (GHG) emissions across their supply chain operations.

## Initial Assessment

Before implementing carbon tracking, understand:

1. **Organizational Context**
   - What's driving carbon tracking? (compliance, reporting, reduction targets)
   - Current carbon accounting maturity?
   - Net-zero or carbon reduction commitments?
   - Regulatory requirements? (CDP, TCFD, SEC Climate Rule)

2. **Scope of Measurement**
   - Which emission scopes to track? (Scope 1, 2, 3)
   - Geographic coverage? (facilities, regions, global)
   - Supply chain depth? (Tier 1, multi-tier)
   - Product-level vs. corporate-level footprint?

3. **Data Availability**
   - Energy consumption data available?
   - Transportation data tracked?
   - Supplier emissions data accessible?
   - Activity data quality and completeness?

4. **Reporting Requirements**
   - Internal targets and KPIs?
   - External reporting frameworks? (GRI, CDP, SASB)
   - Stakeholder expectations? (investors, customers, employees)
   - Verification and assurance needs?

---

## GHG Protocol Framework

### Emission Scopes

**Scope 1: Direct Emissions**
- Company-owned vehicles and equipment
- On-site fuel combustion
- Manufacturing processes
- Fugitive emissions (refrigerants, leaks)

**Scope 2: Indirect Energy Emissions**
- Purchased electricity
- Purchased heating and cooling
- Purchased steam

**Scope 3: Value Chain Emissions**
- **Upstream:**
  - Purchased goods and services
  - Capital goods
  - Transportation and distribution (upstream)
  - Business travel
  - Employee commuting
  - Waste disposal
  - Leased assets (upstream)
- **Downstream:**
  - Transportation and distribution (downstream)
  - Product use
  - End-of-life treatment
  - Franchises
  - Investments

### Emission Categories Priority

| Category | Typical % of Total | Measurement Complexity | Priority |
|----------|-------------------|----------------------|----------|
| Scope 3: Purchased Goods | 40-70% | High | Critical |
| Scope 3: Upstream Transport | 10-20% | Medium | High |
| Scope 2: Electricity | 5-15% | Low | High |
| Scope 1: Facilities | 5-10% | Low | Medium |
| Scope 3: Product Use | 10-30% | High | Medium |
| Scope 3: End-of-Life | 2-5% | Medium | Low |

---

## Carbon Calculation Methodology

### Emission Factor Approach

**Basic Formula:**
```
CO2e Emissions = Activity Data × Emission Factor

Where:
  Activity Data = Quantity of activity (kWh, liters, kg, tkm, etc.)
  Emission Factor = Emissions per unit (kgCO2e per unit)
  CO2e = Carbon dioxide equivalent (includes all GHGs)
```

**Python Implementation:**

```python
import pandas as pd
import numpy as np

class CarbonFootprintCalculator:
    """Comprehensive carbon footprint calculator"""

    def __init__(self):
        self.emission_factors = self._load_emission_factors()
        self.gwp_factors = {
            'CO2': 1,
            'CH4': 25,      # Methane (100-year GWP)
            'N2O': 298,     # Nitrous oxide
            'HFCs': 1430,   # Hydrofluorocarbons (avg)
            'PFCs': 7390,   # Perfluorocarbons (avg)
            'SF6': 22800    # Sulfur hexafluoride
        }

    def _load_emission_factors(self):
        """Load standard emission factors database"""
        # Based on EPA, DEFRA, and other sources
        return {
            # Energy (kgCO2e per kWh)
            'electricity_us_grid': 0.417,
            'electricity_eu_grid': 0.295,
            'electricity_renewable': 0.000,
            'natural_gas': 0.202,  # per kWh

            # Fuels (kgCO2e per liter)
            'diesel': 2.68,
            'gasoline': 2.31,
            'jet_fuel': 2.50,

            # Transportation (kgCO2e per tonne-km)
            'truck_full_truckload': 0.062,
            'truck_less_than_truckload': 0.091,
            'rail': 0.022,
            'ocean_shipping': 0.008,
            'air_freight': 0.602,

            # Materials (kgCO2e per kg)
            'steel': 1.85,
            'aluminum': 8.24,
            'plastic_pet': 2.15,
            'cardboard': 0.95,
            'glass': 0.85,
            'concrete': 0.11,

            # Manufacturing (kgCO2e per unit - examples)
            'electronics_assembly': 50,
            'textile_production': 15,
            'food_processing': 2.5
        }

    def calculate_scope1_facilities(self, fuel_consumption):
        """
        Calculate Scope 1 emissions from facility fuel use

        fuel_consumption: dict with fuel types and quantities
        Example: {'diesel_liters': 10000, 'natural_gas_kwh': 50000}
        """
        emissions = 0
        breakdown = []

        # Diesel/gasoline combustion
        if 'diesel_liters' in fuel_consumption:
            diesel_co2 = fuel_consumption['diesel_liters'] * self.emission_factors['diesel']
            emissions += diesel_co2
            breakdown.append({
                'source': 'Diesel combustion',
                'activity': fuel_consumption['diesel_liters'],
                'unit': 'liters',
                'emissions_kgco2e': diesel_co2
            })

        if 'gasoline_liters' in fuel_consumption:
            gas_co2 = fuel_consumption['gasoline_liters'] * self.emission_factors['gasoline']
            emissions += gas_co2
            breakdown.append({
                'source': 'Gasoline combustion',
                'activity': fuel_consumption['gasoline_liters'],
                'unit': 'liters',
                'emissions_kgco2e': gas_co2
            })

        # Natural gas (converted to kWh)
        if 'natural_gas_kwh' in fuel_consumption:
            ng_co2 = fuel_consumption['natural_gas_kwh'] * self.emission_factors['natural_gas']
            emissions += ng_co2
            breakdown.append({
                'source': 'Natural gas',
                'activity': fuel_consumption['natural_gas_kwh'],
                'unit': 'kWh',
                'emissions_kgco2e': ng_co2
            })

        return {
            'scope': 'Scope 1',
            'total_emissions_kgco2e': round(emissions, 2),
            'total_emissions_tco2e': round(emissions / 1000, 2),
            'breakdown': breakdown
        }

    def calculate_scope1_fleet(self, vehicle_data):
        """
        Calculate Scope 1 emissions from company fleet

        vehicle_data: list of dicts with vehicle info
        Example: [{'type': 'diesel', 'distance_km': 50000, 'fuel_efficiency_l_per_100km': 8}]
        """
        emissions = 0
        breakdown = []

        for vehicle in vehicle_data:
            distance = vehicle['distance_km']
            fuel_efficiency = vehicle['fuel_efficiency_l_per_100km']
            fuel_type = vehicle['type']

            # Calculate fuel consumed
            fuel_consumed = (distance / 100) * fuel_efficiency

            # Get emission factor
            if fuel_type in ['diesel']:
                ef = self.emission_factors['diesel']
            elif fuel_type in ['gasoline', 'petrol']:
                ef = self.emission_factors['gasoline']
            else:
                ef = 2.5  # default

            vehicle_emissions = fuel_consumed * ef
            emissions += vehicle_emissions

            breakdown.append({
                'vehicle_id': vehicle.get('id', 'Unknown'),
                'fuel_type': fuel_type,
                'distance_km': distance,
                'fuel_consumed_liters': round(fuel_consumed, 2),
                'emissions_kgco2e': round(vehicle_emissions, 2)
            })

        return {
            'scope': 'Scope 1 - Fleet',
            'total_emissions_kgco2e': round(emissions, 2),
            'total_emissions_tco2e': round(emissions / 1000, 2),
            'breakdown': breakdown
        }

    def calculate_scope2_electricity(self, electricity_consumption, region='us', renewable_pct=0):
        """
        Calculate Scope 2 emissions from electricity

        electricity_consumption: kWh consumed
        region: 'us', 'eu', or custom
        renewable_pct: percentage of renewable energy (0-1)
        """

        # Select emission factor based on region
        if region == 'us':
            ef = self.emission_factors['electricity_us_grid']
        elif region == 'eu':
            ef = self.emission_factors['electricity_eu_grid']
        else:
            ef = 0.40  # global average

        # Adjust for renewable percentage
        grid_electricity = electricity_consumption * (1 - renewable_pct)
        renewable_electricity = electricity_consumption * renewable_pct

        emissions_grid = grid_electricity * ef
        emissions_renewable = renewable_electricity * self.emission_factors['electricity_renewable']

        total_emissions = emissions_grid + emissions_renewable

        return {
            'scope': 'Scope 2',
            'total_electricity_kwh': electricity_consumption,
            'grid_electricity_kwh': grid_electricity,
            'renewable_electricity_kwh': renewable_electricity,
            'emission_factor_kgco2e_per_kwh': ef,
            'total_emissions_kgco2e': round(total_emissions, 2),
            'total_emissions_tco2e': round(total_emissions / 1000, 2)
        }

    def calculate_scope3_transportation(self, shipments):
        """
        Calculate Scope 3 emissions from transportation

        shipments: list of dicts
        Example: [{'mode': 'truck_ftl', 'distance_km': 500, 'weight_tonnes': 20}]
        """
        emissions = 0
        breakdown = []

        for shipment in shipments:
            mode = shipment['mode']
            distance = shipment['distance_km']
            weight = shipment['weight_tonnes']

            # Calculate tonne-kilometers
            tkm = distance * weight

            # Get emission factor
            mode_map = {
                'truck_ftl': 'truck_full_truckload',
                'truck_ltl': 'truck_less_than_truckload',
                'rail': 'rail',
                'ocean': 'ocean_shipping',
                'air': 'air_freight'
            }

            ef_key = mode_map.get(mode, 'truck_full_truckload')
            ef = self.emission_factors[ef_key]

            shipment_emissions = tkm * ef
            emissions += shipment_emissions

            breakdown.append({
                'shipment_id': shipment.get('id', 'Unknown'),
                'mode': mode,
                'distance_km': distance,
                'weight_tonnes': weight,
                'tonne_km': tkm,
                'emission_factor': ef,
                'emissions_kgco2e': round(shipment_emissions, 2)
            })

        return {
            'scope': 'Scope 3 - Transportation',
            'total_emissions_kgco2e': round(emissions, 2),
            'total_emissions_tco2e': round(emissions / 1000, 2),
            'breakdown': breakdown
        }

    def calculate_scope3_materials(self, materials_purchased):
        """
        Calculate Scope 3 emissions from purchased materials

        materials_purchased: dict with material types and quantities (kg)
        Example: {'steel': 10000, 'plastic_pet': 5000}
        """
        emissions = 0
        breakdown = []

        for material, quantity_kg in materials_purchased.items():
            if material in self.emission_factors:
                ef = self.emission_factors[material]
                material_emissions = quantity_kg * ef
                emissions += material_emissions

                breakdown.append({
                    'material': material,
                    'quantity_kg': quantity_kg,
                    'emission_factor': ef,
                    'emissions_kgco2e': round(material_emissions, 2)
                })

        return {
            'scope': 'Scope 3 - Materials',
            'total_emissions_kgco2e': round(emissions, 2),
            'total_emissions_tco2e': round(emissions / 1000, 2),
            'breakdown': breakdown
        }

    def calculate_product_carbon_footprint(self, product_data):
        """
        Calculate product-level carbon footprint (cradle-to-gate)

        product_data: dict with all product lifecycle data
        """
        total_emissions = 0
        lifecycle_breakdown = {}

        # Materials extraction and processing
        if 'materials' in product_data:
            materials_result = self.calculate_scope3_materials(product_data['materials'])
            lifecycle_breakdown['materials'] = materials_result
            total_emissions += materials_result['total_emissions_kgco2e']

        # Manufacturing
        if 'manufacturing' in product_data:
            mfg_energy = product_data['manufacturing'].get('energy_kwh', 0)
            mfg_result = self.calculate_scope2_electricity(
                mfg_energy,
                region=product_data['manufacturing'].get('region', 'us')
            )
            lifecycle_breakdown['manufacturing'] = mfg_result
            total_emissions += mfg_result['total_emissions_kgco2e']

        # Transportation to customer
        if 'transportation' in product_data:
            transport_result = self.calculate_scope3_transportation(
                product_data['transportation']
            )
            lifecycle_breakdown['transportation'] = transport_result
            total_emissions += transport_result['total_emissions_kgco2e']

        # Use phase (if applicable)
        if 'use_phase' in product_data:
            use_emissions = product_data['use_phase'].get('emissions_kgco2e', 0)
            lifecycle_breakdown['use_phase'] = {
                'emissions_kgco2e': use_emissions
            }
            total_emissions += use_emissions

        # End of life
        if 'end_of_life' in product_data:
            eol_emissions = product_data['end_of_life'].get('emissions_kgco2e', 0)
            lifecycle_breakdown['end_of_life'] = {
                'emissions_kgco2e': eol_emissions
            }
            total_emissions += eol_emissions

        return {
            'product_id': product_data.get('product_id', 'Unknown'),
            'total_carbon_footprint_kgco2e': round(total_emissions, 2),
            'lifecycle_breakdown': lifecycle_breakdown,
            'per_unit_emissions': round(total_emissions / product_data.get('units', 1), 2)
        }

    def calculate_emissions_by_scope(self, scope1_data, scope2_data, scope3_data):
        """Generate comprehensive emissions inventory by scope"""

        scope1_result = self.calculate_scope1_facilities(scope1_data['facilities'])
        scope1_fleet = self.calculate_scope1_fleet(scope1_data['fleet'])

        scope2_result = self.calculate_scope2_electricity(
            scope2_data['electricity_kwh'],
            region=scope2_data.get('region', 'us'),
            renewable_pct=scope2_data.get('renewable_pct', 0)
        )

        scope3_transport = self.calculate_scope3_transportation(scope3_data['shipments'])
        scope3_materials = self.calculate_scope3_materials(scope3_data['materials'])

        total_scope1 = (scope1_result['total_emissions_kgco2e'] +
                       scope1_fleet['total_emissions_kgco2e'])
        total_scope2 = scope2_result['total_emissions_kgco2e']
        total_scope3 = (scope3_transport['total_emissions_kgco2e'] +
                       scope3_materials['total_emissions_kgco2e'])

        total_emissions = total_scope1 + total_scope2 + total_scope3

        return {
            'total_emissions_tco2e': round(total_emissions / 1000, 2),
            'scope1_tco2e': round(total_scope1 / 1000, 2),
            'scope2_tco2e': round(total_scope2 / 1000, 2),
            'scope3_tco2e': round(total_scope3 / 1000, 2),
            'scope1_percentage': round(total_scope1 / total_emissions * 100, 1),
            'scope2_percentage': round(total_scope2 / total_emissions * 100, 1),
            'scope3_percentage': round(total_scope3 / total_emissions * 100, 1),
            'detailed_results': {
                'scope1_facilities': scope1_result,
                'scope1_fleet': scope1_fleet,
                'scope2_electricity': scope2_result,
                'scope3_transportation': scope3_transport,
                'scope3_materials': scope3_materials
            }
        }


# Example usage
calculator = CarbonFootprintCalculator()

# Example calculation
scope1_data = {
    'facilities': {
        'diesel_liters': 5000,
        'natural_gas_kwh': 100000
    },
    'fleet': [
        {'id': 'V001', 'type': 'diesel', 'distance_km': 50000, 'fuel_efficiency_l_per_100km': 8},
        {'id': 'V002', 'type': 'diesel', 'distance_km': 30000, 'fuel_efficiency_l_per_100km': 9}
    ]
}

scope2_data = {
    'electricity_kwh': 500000,
    'region': 'us',
    'renewable_pct': 0.20  # 20% renewable
}

scope3_data = {
    'shipments': [
        {'id': 'S001', 'mode': 'truck_ftl', 'distance_km': 800, 'weight_tonnes': 20},
        {'id': 'S002', 'mode': 'ocean', 'distance_km': 5000, 'weight_tonnes': 100},
        {'id': 'S003', 'mode': 'air', 'distance_km': 2000, 'weight_tonnes': 2}
    ],
    'materials': {
        'steel': 50000,
        'plastic_pet': 10000,
        'cardboard': 5000
    }
}

results = calculator.calculate_emissions_by_scope(scope1_data, scope2_data, scope3_data)

print(f"Total Emissions: {results['total_emissions_tco2e']} tCO2e")
print(f"Scope 1: {results['scope1_tco2e']} tCO2e ({results['scope1_percentage']}%)")
print(f"Scope 2: {results['scope2_tco2e']} tCO2e ({results['scope2_percentage']}%)")
print(f"Scope 3: {results['scope3_tco2e']} tCO2e ({results['scope3_percentage']}%)")
```

---

## Supplier Emissions Tracking

### Primary Data Collection

```python
class SupplierEmissionsTracker:
    """Track and manage supplier carbon footprint data"""

    def __init__(self):
        self.suppliers = {}
        self.data_quality_tiers = {
            'tier1_primary': 1.0,      # Supplier-specific verified data
            'tier2_secondary': 0.8,    # Industry averages
            'tier3_estimated': 0.5     # Spend-based estimates
        }

    def add_supplier(self, supplier_id, supplier_name, spend, emissions_data):
        """
        Add supplier with emissions data

        emissions_data: dict with emissions info and data quality
        """
        self.suppliers[supplier_id] = {
            'name': supplier_name,
            'annual_spend': spend,
            'emissions_data': emissions_data,
            'data_quality': emissions_data.get('data_quality', 'tier3_estimated'),
            'last_updated': pd.Timestamp.now()
        }

    def calculate_supplier_emissions(self, supplier_id):
        """Calculate emissions for a specific supplier"""
        supplier = self.suppliers[supplier_id]
        emissions_data = supplier['emissions_data']

        if supplier['data_quality'] == 'tier1_primary':
            # Use supplier-reported data
            return emissions_data.get('reported_emissions_tco2e', 0)

        elif supplier['data_quality'] == 'tier2_secondary':
            # Use industry average emission factors
            category = emissions_data.get('category', 'general_manufacturing')
            revenue = emissions_data.get('revenue', 1000000)

            # Industry emission intensities (tCO2e per $1M revenue)
            intensity_map = {
                'general_manufacturing': 120,
                'electronics': 80,
                'chemicals': 250,
                'textiles': 150,
                'food_processing': 90,
                'logistics': 200
            }

            intensity = intensity_map.get(category, 100)
            emissions = (revenue / 1000000) * intensity
            return emissions

        else:  # tier3_estimated
            # Spend-based estimation
            spend = supplier['annual_spend']

            # Average emission factor: tCO2e per $1000 spend
            spend_emission_factor = 0.5

            emissions = (spend / 1000) * spend_emission_factor
            return emissions

    def generate_supplier_emissions_report(self):
        """Generate comprehensive supplier emissions report"""

        report_data = []

        for supplier_id, supplier in self.suppliers.items():
            emissions = self.calculate_supplier_emissions(supplier_id)

            data_quality = supplier['data_quality']
            quality_score = self.data_quality_tiers[data_quality]

            report_data.append({
                'supplier_id': supplier_id,
                'supplier_name': supplier['name'],
                'annual_spend': supplier['annual_spend'],
                'emissions_tco2e': round(emissions, 2),
                'data_quality': data_quality,
                'quality_score': quality_score,
                'emissions_intensity_per_1k_spend': round(emissions / (supplier['annual_spend'] / 1000), 2)
            })

        df = pd.DataFrame(report_data)

        # Sort by emissions descending
        df = df.sort_values('emissions_tco2e', ascending=False)

        # Calculate cumulative percentage
        total_emissions = df['emissions_tco2e'].sum()
        df['cumulative_pct'] = df['emissions_tco2e'].cumsum() / total_emissions * 100

        # Classify suppliers by emissions contribution
        df['classification'] = df['cumulative_pct'].apply(
            lambda x: 'A (High)' if x <= 80 else ('B (Medium)' if x <= 95 else 'C (Low)')
        )

        return df

    def identify_engagement_priorities(self, threshold_pct=80):
        """Identify suppliers to prioritize for emissions reduction engagement"""

        df = self.generate_supplier_emissions_report()

        # Prioritize suppliers contributing to top 80% of emissions
        priority_suppliers = df[df['cumulative_pct'] <= threshold_pct].copy()

        # Also prioritize poor data quality with high spend
        high_spend_poor_quality = df[
            (df['annual_spend'] > df['annual_spend'].quantile(0.75)) &
            (df['quality_score'] < 0.7)
        ]

        # Combine
        priority_list = pd.concat([priority_suppliers, high_spend_poor_quality]).drop_duplicates()

        return priority_list.sort_values('emissions_tco2e', ascending=False)


# Example usage
tracker = SupplierEmissionsTracker()

# Add suppliers
tracker.add_supplier(
    'SUP001',
    'Acme Manufacturing',
    spend=5000000,
    emissions_data={
        'reported_emissions_tco2e': 8500,
        'data_quality': 'tier1_primary',
        'verification': 'third_party'
    }
)

tracker.add_supplier(
    'SUP002',
    'Beta Chemicals',
    spend=3000000,
    emissions_data={
        'category': 'chemicals',
        'revenue': 50000000,
        'data_quality': 'tier2_secondary'
    }
)

tracker.add_supplier(
    'SUP003',
    'Gamma Logistics',
    spend=1500000,
    emissions_data={
        'data_quality': 'tier3_estimated'
    }
)

# Generate report
report = tracker.generate_supplier_emissions_report()
print(report[['supplier_name', 'emissions_tco2e', 'data_quality', 'classification']])

# Identify priorities
priorities = tracker.identify_engagement_priorities()
print("\nPriority Suppliers for Engagement:")
print(priorities[['supplier_name', 'emissions_tco2e', 'quality_score']])
```

---

## Carbon Reduction Strategies

### Reduction Opportunity Analysis

```python
class CarbonReductionPlanner:
    """Identify and prioritize carbon reduction opportunities"""

    def __init__(self, baseline_emissions):
        self.baseline_emissions = baseline_emissions
        self.reduction_initiatives = []

    def add_initiative(self, initiative_name, category, reduction_potential_tco2e,
                      investment_required, timeline_years, complexity='medium'):
        """
        Add carbon reduction initiative

        complexity: 'low', 'medium', 'high'
        """

        # Calculate abatement cost ($ per tCO2e reduced)
        annual_reduction = reduction_potential_tco2e
        abatement_cost = investment_required / (annual_reduction * timeline_years) if annual_reduction > 0 else float('inf')

        self.reduction_initiatives.append({
            'initiative': initiative_name,
            'category': category,
            'reduction_potential_tco2e': reduction_potential_tco2e,
            'reduction_percentage': (reduction_potential_tco2e / self.baseline_emissions) * 100,
            'investment_required': investment_required,
            'timeline_years': timeline_years,
            'complexity': complexity,
            'abatement_cost_per_tco2e': round(abatement_cost, 2)
        })

    def prioritize_initiatives(self):
        """Prioritize initiatives using cost-benefit analysis"""

        df = pd.DataFrame(self.reduction_initiatives)

        # Score each initiative
        # Lower cost, higher reduction, lower complexity = higher score

        # Normalize metrics (0-100 scale)
        if len(df) > 0:
            df['cost_score'] = 100 - (
                (df['abatement_cost_per_tco2e'] - df['abatement_cost_per_tco2e'].min()) /
                (df['abatement_cost_per_tco2e'].max() - df['abatement_cost_per_tco2e'].min() + 0.01) * 100
            )

            df['impact_score'] = (
                (df['reduction_potential_tco2e'] - df['reduction_potential_tco2e'].min()) /
                (df['reduction_potential_tco2e'].max() - df['reduction_potential_tco2e'].min() + 0.01) * 100
            )

            complexity_map = {'low': 100, 'medium': 60, 'high': 30}
            df['complexity_score'] = df['complexity'].map(complexity_map)

            # Overall priority score (weighted)
            df['priority_score'] = (
                df['impact_score'] * 0.4 +
                df['cost_score'] * 0.35 +
                df['complexity_score'] * 0.25
            )

            # Classify priority
            df['priority'] = pd.cut(
                df['priority_score'],
                bins=[0, 40, 70, 100],
                labels=['Low', 'Medium', 'High']
            )

            df = df.sort_values('priority_score', ascending=False)

        return df

    def generate_reduction_roadmap(self, target_reduction_pct, budget_limit):
        """
        Generate optimal roadmap to achieve reduction target within budget

        Uses greedy algorithm to select best initiatives
        """

        df = self.prioritize_initiatives()

        # Sort by priority score
        df = df.sort_values('priority_score', ascending=False)

        target_reduction_tco2e = self.baseline_emissions * (target_reduction_pct / 100)

        selected_initiatives = []
        total_reduction = 0
        total_investment = 0

        for idx, initiative in df.iterrows():
            # Check if we can afford it
            if total_investment + initiative['investment_required'] <= budget_limit:
                # Check if we still need more reduction
                if total_reduction < target_reduction_tco2e:
                    selected_initiatives.append(initiative)
                    total_reduction += initiative['reduction_potential_tco2e']
                    total_investment += initiative['investment_required']

        achievement_pct = (total_reduction / self.baseline_emissions) * 100

        return {
            'selected_initiatives': pd.DataFrame(selected_initiatives),
            'total_reduction_tco2e': round(total_reduction, 2),
            'achievement_percentage': round(achievement_pct, 1),
            'total_investment': total_investment,
            'remaining_budget': budget_limit - total_investment,
            'gap_to_target_tco2e': round(target_reduction_tco2e - total_reduction, 2)
        }


# Example reduction planning
baseline = 10000  # tCO2e
planner = CarbonReductionPlanner(baseline)

# Add various initiatives
planner.add_initiative(
    'Switch to renewable electricity',
    category='Energy',
    reduction_potential_tco2e=2000,
    investment_required=500000,
    timeline_years=10,
    complexity='low'
)

planner.add_initiative(
    'Fleet electrification',
    category='Transportation',
    reduction_potential_tco2e=1500,
    investment_required=2000000,
    timeline_years=5,
    complexity='high'
)

planner.add_initiative(
    'Supplier engagement program',
    category='Supply Chain',
    reduction_potential_tco2e=3000,
    investment_required=200000,
    timeline_years=3,
    complexity='medium'
)

planner.add_initiative(
    'Energy efficiency improvements',
    category='Operations',
    reduction_potential_tco2e=800,
    investment_required=300000,
    timeline_years=7,
    complexity='low'
)

planner.add_initiative(
    'Modal shift to rail',
    category='Transportation',
    reduction_potential_tco2e=600,
    investment_required=150000,
    timeline_years=5,
    complexity='medium'
)

# Prioritize all initiatives
priorities = planner.prioritize_initiatives()
print("All Initiatives (Prioritized):")
print(priorities[['initiative', 'reduction_potential_tco2e', 'abatement_cost_per_tco2e', 'priority']])

# Generate roadmap
roadmap = planner.generate_reduction_roadmap(
    target_reduction_pct=40,  # 40% reduction target
    budget_limit=1500000
)

print(f"\n\nReduction Roadmap:")
print(f"Target: 40% reduction from {baseline} tCO2e")
print(f"Achieved: {roadmap['achievement_percentage']}% ({roadmap['total_reduction_tco2e']} tCO2e)")
print(f"Investment: ${roadmap['total_investment']:,.0f}")
print(f"Gap to target: {roadmap['gap_to_target_tco2e']} tCO2e")
print(f"\nSelected Initiatives:")
print(roadmap['selected_initiatives'][['initiative', 'reduction_potential_tco2e', 'investment_required']])
```

---

## Tools & Libraries

### Python Libraries

**Carbon Calculation:**
- `pandas`: Data manipulation and analysis
- `numpy`: Numerical computations
- `scipy`: Statistical analysis

**Data Collection:**
- `requests`: API integration for emission factors
- `beautifulsoup4`: Web scraping for data
- `sqlalchemy`: Database management

**Visualization:**
- `matplotlib`, `seaborn`: Emissions charts
- `plotly`: Interactive dashboards
- `folium`: Geographic emission maps

**Specialized:**
- `brightway2`: Life cycle assessment (LCA)
- `openLCA`: Open-source LCA framework
- `carbon-footprint`: Carbon calculation utilities

### Commercial Software

**Carbon Accounting Platforms:**
- **Watershed**: Enterprise carbon accounting
- **Persefoni**: Climate management and accounting
- **Plan A**: Carbon management platform
- **Normative**: Business carbon accounting
- **Sweep**: Carbon measurement and reduction
- **CarbonChain**: Supply chain carbon tracking

**Sustainability Platforms:**
- **SAP Product Footprint Management**: Product-level carbon
- **Enablon**: ESG and sustainability management
- **Sphera**: Sustainability performance management
- **thinkstep (Sphera)**: LCA software

**Reporting Platforms:**
- **Workiva**: ESG reporting
- **Emitwise**: Carbon accounting and reporting
- **FigBytes**: Net-zero planning

### Emission Factor Databases

- **EPA Emission Factors**: US EPA data
- **DEFRA**: UK Government conversion factors
- **Ecoinvent**: Global LCA database
- **GHG Protocol**: Calculation tools and guidance
- **Carbon Trust**: Footprinting tools
- **GLEC Framework**: Logistics emissions

---

## Common Challenges & Solutions

### Challenge: Scope 3 Data Collection

**Problem:**
- Suppliers reluctant to share emissions data
- Inconsistent data quality
- Limited visibility beyond Tier 1 suppliers

**Solutions:**
- Phased data quality improvement (spend-based → industry avg → primary)
- Supplier engagement programs with incentives
- Collaborative industry initiatives
- Third-party data providers (CDP Supply Chain, EcoVadis)
- Contractual requirements for emissions disclosure
- Standardized templates and tools for suppliers

### Challenge: Emission Factor Selection

**Problem:**
- Multiple emission factor sources available
- Region-specific vs. global factors
- Uncertainty in calculations
- Keeping factors up-to-date

**Solutions:**
- Document methodology and factor sources
- Use most specific factors available (supplier-specific > industry > generic)
- Consistency over time for trend analysis
- Annual review and update of factors
- Sensitivity analysis for key assumptions
- Follow GHG Protocol guidance

### Challenge: Data Quality and Completeness

**Problem:**
- Missing activity data
- Inconsistent data formats
- Lack of automated data collection
- Manual processes prone to errors

**Solutions:**
- Implement data governance framework
- Automate data collection where possible
- Integrate with ERP, TMS, WMS systems
- Regular data quality audits
- Use estimation methods for gaps (document assumptions)
- Prioritize data collection for material emissions sources

### Challenge: Baseline Setting

**Problem:**
- Historical data unavailable
- Business changes (acquisitions, divestitures)
- Choosing base year
- Recalculation triggers

**Solutions:**
- Choose base year with best data quality
- Document baseline scope clearly
- Establish recalculation policy (typically >5% change triggers recalculation)
- Track both absolute and intensity metrics
- Use normalized metrics (per revenue, per unit output)

### Challenge: Reduction Attribution

**Problem:**
- Difficult to measure impact of specific initiatives
- Business growth vs. efficiency improvements
- External factors (grid decarbonization)

**Solutions:**
- Track intensity metrics (emissions per unit output)
- Set up measurement and verification (M&V) protocols
- Use control groups where possible
- Document baseline and changes carefully
- Separate organic reduction from business changes
- Regular progress reviews with clear KPIs

### Challenge: Balancing Cost and Accuracy

**Problem:**
- Perfect measurement is expensive
- Diminishing returns on data quality
- Limited resources

**Solutions:**
- Apply materiality principle (focus on significant sources)
- Use tiered approach (detailed for Scope 1&2, estimated for some Scope 3)
- Prioritize data quality for largest emission sources
- Accept estimation for long tail of small emissions
- Document data quality assessments
- Continuous improvement over time

---

## Output Format

### Carbon Footprint Report

**Executive Summary:**
- Total carbon footprint (tCO2e)
- Year-over-year change
- Progress toward reduction targets
- Key emission sources
- Major initiatives and impact

**Emissions Inventory by Scope:**

| Scope | Category | Emissions (tCO2e) | % of Total | vs. Prior Year |
|-------|----------|-------------------|------------|----------------|
| Scope 1 | Facilities | 850 | 8.5% | -5% |
| Scope 1 | Fleet | 1,200 | 12.0% | -2% |
| Scope 2 | Electricity | 1,500 | 15.0% | -12% |
| Scope 3 | Purchased Goods | 4,200 | 42.0% | +3% |
| Scope 3 | Transportation | 1,800 | 18.0% | -8% |
| Scope 3 | Other | 450 | 4.5% | -1% |
| **Total** | | **10,000** | **100%** | **-3%** |

**Emissions by Business Unit:**

| Business Unit | Emissions (tCO2e) | Intensity (tCO2e/$M revenue) | Target | Status |
|---------------|-------------------|------------------------------|--------|--------|
| Manufacturing | 5,500 | 220 | 200 | Behind |
| Distribution | 2,800 | 180 | 190 | On Track |
| Retail | 1,700 | 85 | 90 | Ahead |

**Supplier Emissions:**

| Supplier | Spend ($M) | Emissions (tCO2e) | Data Quality | Priority |
|----------|-----------|-------------------|--------------|----------|
| Supplier A | 5.0 | 2,100 | Primary | A |
| Supplier B | 3.5 | 1,800 | Industry Avg | A |
| Supplier C | 2.0 | 300 | Estimated | B |

**Reduction Initiatives:**

| Initiative | Status | Reduction (tCO2e/yr) | Investment | Timeline | ROI |
|-----------|--------|---------------------|------------|----------|-----|
| Renewable Energy | Implemented | 1,200 | $500K | Complete | 4.2 years |
| Fleet Optimization | In Progress | 400 | $150K | Q3 2026 | 2.8 years |
| Supplier Program | Planning | 800 | $200K | 2027 | TBD |

**Data Quality Assessment:**

| Scope | Coverage | Primary Data % | Estimation % | Quality Score |
|-------|----------|----------------|--------------|---------------|
| Scope 1 | 100% | 100% | 0% | High |
| Scope 2 | 100% | 95% | 5% | High |
| Scope 3 | 85% | 30% | 70% | Medium |

---

## Questions to Ask

If you need more context:
1. What's driving the carbon tracking initiative? (reporting, reduction, compliance)
2. Which emission scopes need to be measured? (1, 2, 3 or specific categories)
3. What data is currently available? (energy bills, transportation records, supplier data)
4. Are there existing carbon reduction targets or commitments?
5. What reporting frameworks must be followed? (GHG Protocol, CDP, GRI, TCFD)
6. What's the organizational boundary? (locations, business units, geographic regions)
7. Is product-level carbon footprinting needed?
8. What's the desired data quality and accuracy level?
9. Are there verification or assurance requirements?
10. What systems are in place? (ERP, TMS, energy management)

---

## Related Skills

- **circular-economy**: For closed-loop and waste reduction strategies
- **sustainable-sourcing**: For environmentally responsible procurement
- **compliance-management**: For regulatory requirements and reporting
- **risk-mitigation**: For climate-related supply chain risks
- **supplier-selection**: For incorporating carbon criteria in sourcing
- **network-design**: For optimizing supply chain configuration for emissions
- **route-optimization**: For transportation emissions reduction
- **demand-forecasting**: For accurate production planning to minimize waste
