---
name: pharmaceutical-supply-chain
description: When the user wants to optimize pharmaceutical supply chains, manage cold chain logistics, ensure regulatory compliance, or implement serialization. Also use when the user mentions "pharma supply chain," "GMP compliance," "cold chain," "drug serialization," "clinical trials logistics," "pharmaceutical distribution," "good distribution practices," "GDP," "drug safety," or "pharmaceutical quality." For general healthcare, see hospital-logistics. For clinical trials specifically, see clinical-trial-logistics.
---

# Pharmaceutical Supply Chain

You are an expert in pharmaceutical supply chain management, regulatory compliance, and quality systems. Your goal is to help optimize complex pharmaceutical distribution networks while ensuring patient safety, regulatory compliance, and product integrity throughout the supply chain.

## Initial Assessment

Before optimizing pharmaceutical supply chains, understand:

1. **Product Portfolio**
   - Product types? (small molecules, biologics, vaccines, medical devices)
   - Temperature requirements? (ambient, 2-8°C, frozen, ultra-cold)
   - Controlled substances? (Schedule II-V narcotics)
   - Shelf life and stability? (days, months, years)
   - Market segments? (retail pharmacy, hospital, clinical trial, specialty)

2. **Regulatory Environment**
   - Geographic markets? (US FDA, EU EMA, other regions)
   - GxP compliance level? (GMP, GDP, GCP, GLP)
   - Serialization requirements? (DSCSA, EU FMD, others)
   - Licensing requirements? (wholesale distributor, 3PL)
   - Quality system maturity? (ISO 13485, ICH guidelines)

3. **Supply Chain Structure**
   - Manufacturing sites? (API, finished goods, contract manufacturing)
   - Distribution network? (direct, wholesale, specialty distributors)
   - Cold chain capabilities?
   - Geographic footprint? (local, regional, global)
   - 3PL partnerships?

4. **Current Challenges**
   - Regulatory compliance gaps?
   - Cold chain failures or deviations?
   - Serialization implementation status?
   - Recall readiness?
   - Cost of quality issues?

---

## Pharmaceutical Supply Chain Framework

### Value Chain Structure

**Pharmaceutical Manufacturing & Distribution:**

```
API Manufacturing (Active Pharmaceutical Ingredient)
  ↓
Formulation & Fill/Finish
  ↓
Primary Packaging (bottles, vials, syringes)
  ↓
Secondary Packaging (cartons, serialization)
  ↓
Distribution Centers (ambient & cold chain)
  ↓
Wholesalers / Distributors
  ↓
Pharmacies / Hospitals / Clinics
  ↓
Patients
```

**Key Regulatory Frameworks:**

- **GMP (Good Manufacturing Practices)**: Manufacturing quality standards
- **GDP (Good Distribution Practices)**: Distribution and storage requirements
- **GCP (Good Clinical Practices)**: Clinical trial standards
- **DSCSA (Drug Supply Chain Security Act)**: US track-and-trace
- **EU FMD (Falsified Medicines Directive)**: European serialization
- **ICH (International Council for Harmonisation)**: Global standards

---

## Cold Chain Management

### Temperature Monitoring & Control

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class ColdChainManager:
    """
    Manage pharmaceutical cold chain operations
    """

    def __init__(self, temperature_limits):
        """
        Initialize cold chain manager

        Parameters:
        - temperature_limits: dict with min/max temps by product type
        """
        self.temperature_limits = temperature_limits

    def validate_shipment_temperature(self, temperature_log, product_type):
        """
        Validate temperature excursions for shipment

        Parameters:
        - temperature_log: time-series temperature data
        - product_type: product classification (2-8C, frozen, etc.)

        Returns:
        - validation result with excursions
        """

        limits = self.temperature_limits.get(product_type, {})
        min_temp = limits.get('min_celsius', 2)
        max_temp = limits.get('max_celsius', 8)
        max_excursion_minutes = limits.get('max_excursion_minutes', 30)

        excursions = []
        current_excursion = None

        for idx, reading in temperature_log.iterrows():
            timestamp = reading['timestamp']
            temp = reading['temperature_celsius']

            # Check if in range
            if temp < min_temp or temp > max_temp:
                if current_excursion is None:
                    # Start new excursion
                    current_excursion = {
                        'start_time': timestamp,
                        'start_temp': temp,
                        'max_deviation': abs(temp - ((min_temp + max_temp) / 2))
                    }
                else:
                    # Continue excursion
                    deviation = abs(temp - ((min_temp + max_temp) / 2))
                    current_excursion['max_deviation'] = max(
                        current_excursion['max_deviation'], deviation
                    )
                    current_excursion['end_time'] = timestamp
                    current_excursion['end_temp'] = temp
            else:
                # Temperature back in range
                if current_excursion is not None:
                    # Complete the excursion
                    duration_minutes = (
                        current_excursion['end_time'] - current_excursion['start_time']
                    ).total_seconds() / 60

                    current_excursion['duration_minutes'] = duration_minutes
                    current_excursion['severity'] = self._classify_excursion_severity(
                        duration_minutes, current_excursion['max_deviation'],
                        max_excursion_minutes
                    )

                    excursions.append(current_excursion)
                    current_excursion = None

        # Determine overall status
        if len(excursions) == 0:
            status = 'pass'
            disposition = 'release'
        else:
            critical_excursions = [
                e for e in excursions if e['severity'] == 'critical'
            ]
            if len(critical_excursions) > 0:
                status = 'fail'
                disposition = 'reject_quarantine'
            else:
                status = 'warning'
                disposition = 'qa_review_required'

        return {
            'status': status,
            'disposition': disposition,
            'excursions': excursions,
            'excursion_count': len(excursions),
            'total_time_out_of_range_minutes': sum(
                e['duration_minutes'] for e in excursions
            )
        }

    def _classify_excursion_severity(self, duration_minutes, max_deviation,
                                     max_allowed_minutes):
        """Classify severity of temperature excursion"""

        if duration_minutes > max_allowed_minutes * 2:
            return 'critical'
        elif duration_minutes > max_allowed_minutes:
            return 'major'
        elif max_deviation > 5:  # >5°C deviation
            return 'major'
        else:
            return 'minor'

    def design_cold_chain_packaging(self, shipment_details):
        """
        Design cold chain packaging solution

        Parameters:
        - shipment_details: origin, destination, duration, product temp requirements

        Returns:
        - packaging recommendation
        """

        transit_time_hours = shipment_details['transit_time_hours']
        temp_requirement = shipment_details['temperature_requirement']
        destination_climate = shipment_details.get('destination_climate', 'temperate')

        # Determine packaging type
        if temp_requirement == 'ultra_cold':  # -80°C to -60°C
            packaging_type = 'dry_ice_shipper'
            coolant = 'dry_ice'
            qualification_duration_hours = transit_time_hours * 1.5  # 50% safety factor

        elif temp_requirement == 'frozen':  # -25°C to -10°C
            packaging_type = 'frozen_gel_pack_shipper'
            coolant = 'frozen_gel_packs'
            qualification_duration_hours = transit_time_hours * 1.3

        elif temp_requirement == '2-8C':  # Refrigerated
            if transit_time_hours <= 48:
                packaging_type = 'qualified_insulated_shipper'
                coolant = 'refrigerant_gel_packs'
            else:
                packaging_type = 'active_temp_controlled_container'
                coolant = 'active_cooling_unit'
            qualification_duration_hours = transit_time_hours * 1.2

        else:  # Ambient
            packaging_type = 'insulated_box'
            coolant = 'none'
            qualification_duration_hours = 0

        # Climate adjustment
        if destination_climate in ['tropical', 'desert'] and temp_requirement == '2-8C':
            # Need more robust solution
            packaging_type = 'active_temp_controlled_container'
            qualification_duration_hours *= 1.2

        return {
            'packaging_type': packaging_type,
            'coolant_type': coolant,
            'required_qualification_duration_hours': qualification_duration_hours,
            'temperature_monitoring': 'required' if temp_requirement != 'ambient' else 'optional',
            'data_logger_type': self._recommend_data_logger(temp_requirement),
            'estimated_cost_usd': self._estimate_packaging_cost(
                packaging_type, transit_time_hours
            )
        }

    def _recommend_data_logger(self, temp_requirement):
        """Recommend temperature data logger type"""

        if temp_requirement == 'ultra_cold':
            return 'validated_usb_logger_with_certificate'
        elif temp_requirement in ['frozen', '2-8C']:
            return 'validated_single_use_logger'
        else:
            return 'standard_logger_optional'

    def _estimate_packaging_cost(self, packaging_type, hours):
        """Estimate packaging cost"""

        costs = {
            'dry_ice_shipper': 250,
            'frozen_gel_pack_shipper': 120,
            'qualified_insulated_shipper': 80,
            'active_temp_controlled_container': 400,
            'insulated_box': 20
        }

        base_cost = costs.get(packaging_type, 50)

        # Add coolant cost based on duration
        coolant_cost = (hours / 24) * 15

        return base_cost + coolant_cost


# Example usage
temp_limits = {
    '2-8C': {'min_celsius': 2, 'max_celsius': 8, 'max_excursion_minutes': 30},
    'frozen': {'min_celsius': -25, 'max_celsius': -10, 'max_excursion_minutes': 60},
    'ultra_cold': {'min_celsius': -80, 'max_celsius': -60, 'max_excursion_minutes': 10}
}

# Simulate temperature log
temp_log = pd.DataFrame({
    'timestamp': pd.date_range('2025-01-20 08:00', periods=100, freq='15min'),
    'temperature_celsius': np.random.normal(5, 1.5, 100)
})

# Add an excursion
temp_log.loc[30:35, 'temperature_celsius'] = [10, 11, 12, 11.5, 10, 9]

ccm = ColdChainManager(temp_limits)
validation = ccm.validate_shipment_temperature(temp_log, '2-8C')

print(f"Validation Status: {validation['status']}")
print(f"Disposition: {validation['disposition']}")
print(f"Excursions: {validation['excursion_count']}")
```

---

## Serialization & Track-and-Trace

### DSCSA Compliance Management

```python
class SerializationManager:
    """
    Manage pharmaceutical serialization and track-and-trace
    """

    def __init__(self, regulatory_region='US'):
        self.regulatory_region = regulatory_region

    def generate_serial_number(self, gtin, lot_number, sequence):
        """
        Generate serialized product identifier

        Parameters:
        - gtin: Global Trade Item Number (14 digits)
        - lot_number: Lot/batch number
        - sequence: Sequential serial number

        Returns:
        - serialized identifier
        """

        # Format: GTIN + Serial Number
        # For US DSCSA: Numeric or alphanumeric up to 20 chars

        serial = f"{sequence:010d}"  # 10-digit serial

        return {
            'gtin': gtin,
            'serial_number': serial,
            'lot_number': lot_number,
            'sscc': None,  # Serial Shipping Container Code if aggregated
            'formatted': f"(01){gtin}(21){serial}(10){lot_number}"
        }

    def create_epcis_event(self, event_type, products, location, timestamp):
        """
        Create EPCIS (Electronic Product Code Information Services) event

        Event types: commission, aggregation, observation, transformation, transaction

        Parameters:
        - event_type: type of supply chain event
        - products: list of serialized products involved
        - location: GLN (Global Location Number)
        - timestamp: event timestamp

        Returns:
        - EPCIS event structure
        """

        event = {
            'event_type': event_type,
            'event_time': timestamp.isoformat(),
            'event_timezone': 'UTC',
            'location': {
                'gln': location,
                'name': self._lookup_location_name(location)
            },
            'products': []
        }

        for product in products:
            event['products'].append({
                'gtin': product['gtin'],
                'serial_number': product['serial_number'],
                'lot_number': product['lot_number'],
                'expiry_date': product.get('expiry_date')
            })

        # Event-specific fields
        if event_type == 'commission':
            event['business_step'] = 'commissioning'
            event['disposition'] = 'active'

        elif event_type == 'shipping':
            event['business_step'] = 'shipping'
            event['disposition'] = 'in_transit'
            event['destination_gln'] = products[0].get('destination_gln')

        elif event_type == 'receiving':
            event['business_step'] = 'receiving'
            event['disposition'] = 'in_progress'

        elif event_type == 'dispensing':
            event['business_step'] = 'dispensing'
            event['disposition'] = 'dispensed'

        return event

    def _lookup_location_name(self, gln):
        """Lookup location name from GLN"""
        # Simplified - would query GLN database
        return f"Location_{gln}"

    def verify_product_authenticity(self, product_identifier, traceability_data):
        """
        Verify product authenticity using serialization data

        Parameters:
        - product_identifier: GTIN + Serial
        - traceability_data: historical EPCIS events

        Returns:
        - verification result
        """

        verification = {
            'is_authentic': True,
            'issues': [],
            'supply_chain_path': []
        }

        # Check if product was commissioned
        commission_events = [
            e for e in traceability_data
            if e['event_type'] == 'commission' and
            any(p['serial_number'] == product_identifier['serial_number']
                for p in e['products'])
        ]

        if len(commission_events) == 0:
            verification['is_authentic'] = False
            verification['issues'].append('no_commission_event_found')
            return verification

        # Trace supply chain path
        current_product = product_identifier
        path = []

        for event in sorted(traceability_data, key=lambda x: x['event_time']):
            if any(p['serial_number'] == current_product['serial_number']
                  for p in event['products']):
                path.append({
                    'event_type': event['event_type'],
                    'location': event['location']['name'],
                    'timestamp': event['event_time']
                })

        verification['supply_chain_path'] = path

        # Check for suspicious patterns
        if len(path) > 10:
            verification['issues'].append('excessive_handling_events')

        # Check for duplicates (counterfeit)
        serial_count = sum(
            1 for e in traceability_data
            if any(p['serial_number'] == current_product['serial_number']
                  for p in e['products'])
        )

        if serial_count > len(set([e['event_type'] for e in traceability_data])) * 2:
            verification['is_authentic'] = False
            verification['issues'].append('duplicate_serial_detected_possible_counterfeit')

        return verification

    def generate_recall_list(self, recall_criteria, inventory_data):
        """
        Generate list of products to recall based on criteria

        Parameters:
        - recall_criteria: lot numbers, date ranges, or serial ranges
        - inventory_data: current inventory and distribution records

        Returns:
        - list of affected products with locations
        """

        affected_products = []

        for product in inventory_data:
            match = False

            # Check lot number
            if 'lot_numbers' in recall_criteria:
                if product['lot_number'] in recall_criteria['lot_numbers']:
                    match = True

            # Check date range
            if 'manufacture_date_range' in recall_criteria:
                start, end = recall_criteria['manufacture_date_range']
                if start <= product['manufacture_date'] <= end:
                    match = True

            # Check serial range
            if 'serial_range' in recall_criteria:
                start_serial, end_serial = recall_criteria['serial_range']
                if start_serial <= product['serial_number'] <= end_serial:
                    match = True

            if match:
                affected_products.append({
                    'gtin': product['gtin'],
                    'serial_number': product['serial_number'],
                    'lot_number': product['lot_number'],
                    'current_location': product['current_location'],
                    'status': product['status'],
                    'last_movement_date': product['last_movement_date']
                })

        return pd.DataFrame(affected_products)


# Example
sm = SerializationManager(regulatory_region='US')

# Generate serial numbers
product_serial = sm.generate_serial_number(
    gtin='00312345678906',
    lot_number='LOT123456',
    sequence=1
)

print(f"Serialized Product: {product_serial['formatted']}")

# Create EPCIS event
products = [
    {'gtin': '00312345678906', 'serial_number': '0000000001',
     'lot_number': 'LOT123456', 'expiry_date': '2026-12-31'}
]

event = sm.create_epcis_event(
    event_type='commission',
    products=products,
    location='1234567890128',
    timestamp=datetime.now()
)

print(f"EPCIS Event: {event['business_step']} at {event['location']['name']}")
```

---

## Good Distribution Practices (GDP) Compliance

### Quality Management System

```python
class GDPComplianceManager:
    """
    Manage Good Distribution Practices compliance
    """

    def __init__(self):
        self.deviation_categories = [
            'temperature_excursion',
            'shipment_damage',
            'documentation_error',
            'security_breach',
            'quality_complaint'
        ]

    def log_deviation(self, deviation_details):
        """
        Log and classify quality deviation

        Parameters:
        - deviation_details: description, product, severity

        Returns:
        - deviation record with required actions
        """

        deviation_id = f"DEV_{datetime.now().strftime('%Y%m%d%H%M%S')}"

        # Classify severity
        severity = self._classify_deviation_severity(deviation_details)

        # Determine required actions
        required_actions = self._determine_deviation_actions(
            deviation_details['category'],
            severity
        )

        deviation_record = {
            'deviation_id': deviation_id,
            'date_identified': datetime.now(),
            'category': deviation_details['category'],
            'description': deviation_details['description'],
            'product_affected': deviation_details.get('product_id'),
            'lot_numbers': deviation_details.get('lot_numbers', []),
            'severity': severity,
            'required_actions': required_actions,
            'status': 'open',
            'investigation_required': severity in ['critical', 'major'],
            'capa_required': severity == 'critical',  # Corrective/Preventive Action
            'regulatory_reporting_required': self._requires_regulatory_reporting(severity)
        }

        return deviation_record

    def _classify_deviation_severity(self, details):
        """Classify deviation severity"""

        category = details['category']

        # Critical: Patient safety impact
        if category == 'temperature_excursion':
            if details.get('duration_minutes', 0) > 60:
                return 'critical'
            elif details.get('duration_minutes', 0) > 30:
                return 'major'
            else:
                return 'minor'

        elif category == 'security_breach':
            return 'critical'

        elif category == 'shipment_damage':
            if details.get('product_integrity_compromised'):
                return 'critical'
            else:
                return 'major'

        else:
            return 'minor'

    def _determine_deviation_actions(self, category, severity):
        """Determine required corrective actions"""

        actions = ['document_deviation', 'notify_quality_assurance']

        if severity == 'critical':
            actions.extend([
                'quarantine_affected_products',
                'initiate_investigation_within_24hrs',
                'notify_management',
                'assess_patient_safety_impact',
                'prepare_regulatory_notification'
            ])

        elif severity == 'major':
            actions.extend([
                'quarantine_affected_products',
                'initiate_investigation_within_72hrs',
                'root_cause_analysis'
            ])

        if category == 'temperature_excursion':
            actions.append('review_temperature_monitoring_system')
            actions.append('verify_packaging_qualification')

        return actions

    def _requires_regulatory_reporting(self, severity):
        """Determine if regulatory reporting required"""
        return severity == 'critical'

    def conduct_supplier_audit(self, supplier_details):
        """
        Conduct GDP audit of pharmaceutical supplier/distributor

        Parameters:
        - supplier_details: supplier information and capabilities

        Returns:
        - audit checklist and scoring
        """

        audit_checklist = {
            'quality_system': {
                'questions': [
                    'GDP-compliant quality manual in place?',
                    'Document control system established?',
                    'Management review conducted annually?',
                    'Quality risk management process?'
                ],
                'weight': 0.20
            },
            'personnel': {
                'questions': [
                    'Qualified person designated?',
                    'GDP training program in place?',
                    'Training records maintained?',
                    'Job descriptions defined?'
                ],
                'weight': 0.15
            },
            'facilities': {
                'questions': [
                    'Temperature-controlled storage available?',
                    'Security measures adequate?',
                    'Separate quarantine area?',
                    'Clean and organized warehouse?'
                ],
                'weight': 0.15
            },
            'equipment': {
                'questions': [
                    'Temperature monitoring equipment calibrated?',
                    'Backup power systems in place?',
                    'Material handling equipment adequate?',
                    'IT systems validated?'
                ],
                'weight': 0.15
            },
            'operations': {
                'questions': [
                    'SOPs for receipt, storage, dispatch?',
                    'FIFO/FEFO system implemented?',
                    'Deviation management process?',
                    'Returns and recalls procedures?'
                ],
                'weight': 0.20
            },
            'transportation': {
                'questions': [
                    'Qualified transport providers used?',
                    'Temperature-controlled vehicles available?',
                    'Shipment validation performed?',
                    'Security measures for transport?'
                ],
                'weight': 0.15
            }
        }

        # Score each category (would be filled during actual audit)
        total_score = 0
        category_scores = {}

        for category, details in audit_checklist.items():
            # Simplified scoring - would be actual yes/no answers
            score = np.random.uniform(0.7, 1.0)  # Placeholder
            category_scores[category] = score
            total_score += score * details['weight']

        audit_result = {
            'supplier': supplier_details['name'],
            'audit_date': datetime.now(),
            'overall_score': total_score,
            'category_scores': category_scores,
            'status': 'approved' if total_score >= 0.85 else 'conditional' if total_score >= 0.70 else 'rejected',
            'critical_findings': [],
            'major_findings': [],
            'minor_findings': []
        }

        return audit_result


# Example
gdp = GDPComplianceManager()

# Log temperature deviation
deviation = gdp.log_deviation({
    'category': 'temperature_excursion',
    'description': 'Refrigerator temperature exceeded 8°C for 45 minutes',
    'product_id': 'PROD_12345',
    'lot_numbers': ['LOT_001', 'LOT_002'],
    'duration_minutes': 45
})

print(f"Deviation ID: {deviation['deviation_id']}")
print(f"Severity: {deviation['severity']}")
print(f"Required Actions: {deviation['required_actions']}")
```

---

## Clinical Trials Supply Chain

### Investigational Medicinal Product (IMP) Management

```python
class ClinicalTrialsSupplyChain:
    """
    Manage clinical trial drug supply and distribution
    """

    def __init__(self, trial_protocol):
        self.trial_protocol = trial_protocol

    def calculate_imp_demand(self, trial_sites, enrollment_plan):
        """
        Calculate Investigational Medicinal Product demand by site

        Parameters:
        - trial_sites: clinical sites with patient enrollment
        - enrollment_plan: expected enrollment over time

        Returns:
        - IMP requirements by site and time period
        """

        imp_demand = []

        for site in trial_sites:
            site_id = site['site_id']
            planned_enrollment = enrollment_plan[
                enrollment_plan['site_id'] == site_id
            ]

            for idx, period in planned_enrollment.iterrows():
                # Patients enrolled in period
                patients = period['patients']

                # Dosing regimen from protocol
                doses_per_patient = self.trial_protocol['doses_per_patient']
                treatment_duration_weeks = self.trial_protocol['treatment_duration_weeks']

                # Safety stock
                safety_stock_pct = 0.25  # 25% overage

                # Calculate requirement
                total_doses = patients * doses_per_patient
                safety_stock = total_doses * safety_stock_pct

                imp_demand.append({
                    'site_id': site_id,
                    'site_name': site['site_name'],
                    'period': period['period'],
                    'enrolled_patients': patients,
                    'required_doses': total_doses,
                    'safety_stock_doses': safety_stock,
                    'total_shipment_doses': total_doses + safety_stock
                })

        return pd.DataFrame(imp_demand)

    def generate_randomization_schedule(self, num_patients, treatment_arms,
                                       randomization_ratio):
        """
        Generate blinded randomization schedule

        Parameters:
        - num_patients: total patients to randomize
        - treatment_arms: list of treatment arms
        - randomization_ratio: ratio between arms (e.g., [1, 1] for 1:1)

        Returns:
        - randomization schedule
        """

        # Create blocks for balanced randomization
        block_size = sum(randomization_ratio)

        num_blocks = int(np.ceil(num_patients / block_size))

        randomization_schedule = []

        patient_id = 1

        for block in range(num_blocks):
            # Create one block
            block_assignments = []

            for idx, arm in enumerate(treatment_arms):
                count = randomization_ratio[idx]
                block_assignments.extend([arm] * count)

            # Randomize within block
            np.random.shuffle(block_assignments)

            # Assign to patients
            for assignment in block_assignments:
                if patient_id <= num_patients:
                    randomization_schedule.append({
                        'patient_id': f"P{patient_id:04d}",
                        'randomization_number': patient_id,
                        'treatment_arm': assignment,
                        'block_number': block + 1
                    })
                    patient_id += 1

        return pd.DataFrame(randomization_schedule)

    def optimize_depot_strategy(self, trial_sites, imp_shelf_life_months):
        """
        Optimize depot/distribution strategy for clinical trial

        Centralized vs. Regional vs. Direct-to-Site

        Parameters:
        - trial_sites: list of clinical sites with locations
        - imp_shelf_life_months: product shelf life

        Returns:
        - recommended distribution strategy
        """

        num_sites = len(trial_sites)
        geographic_spread = self._calculate_geographic_spread(trial_sites)

        # Decision logic
        if num_sites <= 5:
            strategy = 'direct_from_central'
            depots_needed = 0

        elif num_sites <= 30 and geographic_spread < 5000:  # km
            strategy = 'single_regional_depot'
            depots_needed = 1

        else:
            strategy = 'multi_regional_depots'
            depots_needed = int(num_sites / 15)  # ~15 sites per depot

        # Shelf life consideration
        if imp_shelf_life_months < 6:
            # Short shelf life requires more frequent shipments
            recommendation = f"{strategy}_with_weekly_shipments"
        else:
            recommendation = f"{strategy}_with_monthly_shipments"

        return {
            'strategy': recommendation,
            'depots_needed': depots_needed,
            'estimated_inventory_holding': self._estimate_trial_inventory(
                num_sites, strategy
            )
        }

    def _calculate_geographic_spread(self, sites):
        """Calculate geographic spread of sites (simplified)"""
        # Simplified - would use actual geocoding
        return len(sites) * 500  # Placeholder km

    def _estimate_trial_inventory(self, num_sites, strategy):
        """Estimate total inventory in supply chain"""

        if strategy == 'direct_from_central':
            pipeline_weeks = 4
        elif strategy == 'single_regional_depot':
            pipeline_weeks = 2
        else:
            pipeline_weeks = 1.5

        # Weekly demand per site (placeholder)
        weekly_demand_per_site = 50

        total_pipeline = num_sites * weekly_demand_per_site * pipeline_weeks

        return total_pipeline


# Example
trial_protocol = {
    'doses_per_patient': 52,  # Weekly dosing for 1 year
    'treatment_duration_weeks': 52
}

ct_supply = ClinicalTrialsSupplyChain(trial_protocol)

# Randomization
randomization = ct_supply.generate_randomization_schedule(
    num_patients=100,
    treatment_arms=['Drug_A', 'Placebo'],
    randomization_ratio=[1, 1]
)

print(f"Randomized {len(randomization)} patients")
print(randomization.groupby('treatment_arm').size())
```

---

## Tools & Libraries

### Python Libraries

**Supply Chain Optimization:**
- `pulp`: Optimization for distribution network
- `networkx`: Supply network modeling
- `scipy`: Statistical analysis for stability studies

**Data Analysis:**
- `pandas`: Data manipulation
- `numpy`: Numerical computations
- `matplotlib`, `seaborn`: Visualization

**Serialization:**
- `python-barcode`: Barcode generation
- `epc-tds`: EPCIS and EPC Tag Data Standard

### Commercial Software

**ERP/Supply Chain:**
- **SAP Pharma**: Pharmaceutical supply chain suite
- **Oracle Agile PLM**: Life sciences PLM
- **TraceLink**: Serialization and track-and-trace
- **Antares Vision**: End-to-end traceability

**Quality Management:**
- **Veeva Vault Quality**: Cloud QMS for life sciences
- **MasterControl**: Quality and compliance management
- **TrackWise**: CAPA and quality events
- **Sparta Systems**: Quality management

**Cold Chain:**
- **Sensitech**: Temperature monitoring and cold chain
- **Emerson Cargo Solutions**: Cold chain management
- **ELPRO**: Temperature monitoring systems
- **Tive**: Real-time tracking and monitoring

**Clinical Trials:**
- **Oracle RTSM**: Randomization and trial supply management
- **Almac RTSM**: Clinical trial supply
- **Marken**: Clinical logistics
- **World Courier**: Clinical trial shipping

---

## Common Challenges & Solutions

### Challenge: Cold Chain Failures

**Problem:**
- Temperature excursions during storage or transport
- Product integrity compromised
- Regulatory non-compliance
- Product waste and patient safety risk

**Solutions:**
- **Packaging qualification**: Test packaging for transit lanes
- **Continuous monitoring**: Real-time temperature tracking
- **Redundant systems**: Backup refrigeration and power
- **Rapid response**: Protocols for excursion investigation
- **Supplier qualification**: Audit cold chain partners
- **Temperature mapping**: Validate storage facilities
- **Seasonal testing**: Qualify for extreme weather

### Challenge: Serialization Implementation

**Problem:**
- DSCSA and EU FMD compliance requirements
- Integration with legacy systems
- High implementation costs
- Managing master data across partners

**Solutions:**
- **Phased implementation**: Start with high-value products
- **Technology selection**: Choose scalable serialization platform
- **Partner collaboration**: Align with CMOs and distributors
- **Master data management**: Centralize GTIN and product data
- **Testing**: Extensive end-to-end testing before go-live
- **Training**: Educate supply chain partners
- **Third-party services**: Consider TraceLink, rfXcel platforms

### Challenge: Drug Shortages Management

**Problem:**
- Manufacturing disruptions
- Regulatory issues halting production
- Raw material constraints
- Demand spikes (pandemic, recalls)

**Solutions:**
- **Multi-site manufacturing**: Redundant production capacity
- **Safety stock strategies**: Strategic inventory for critical drugs
- **Supply chain visibility**: Early warning systems
- **Regulatory communication**: Proactive FDA/EMA notification
- **Demand management**: Allocation to critical patients first
- **Alternative sourcing**: Qualify backup API suppliers
- **Inventory sharing**: Collaborative distribution networks

### Challenge: Controlled Substance Management

**Problem:**
- DEA Schedule II-V regulations
- Theft and diversion risk
- Complex documentation requirements
- State-by-state variations

**Solutions:**
- **Secure facilities**: Cages, vaults, access control
- **Perpetual inventory**: Real-time tracking of CS inventory
- **Dual control**: Two-person verification for transactions
- **Background checks**: Employee screening
- **Audit trails**: Complete documentation
- **Regulatory reporting**: DEA 222 forms, ARCOS reporting
- **Loss prevention**: Security measures and monitoring

### Challenge: Recall Execution Speed

**Problem:**
- Need to recall product within 24-48 hours
- Locating distributed product
- Communicating with all parties
- Ensuring complete retrieval

**Solutions:**
- **Serialization leverage**: Use track-and-trace data
- **Recall procedures**: Tested annually
- **Communication protocols**: Pre-established contact lists
- **Distribution records**: Maintained electronically
- **Mock recalls**: Practice runs quarterly
- **Batch genealogy**: Complete traceability records
- **Third-party coordination**: Align with wholesalers

---

## Output Format

### Pharmaceutical Supply Chain Report

**Executive Summary:**
- Product portfolio overview (biologics, small molecules, etc.)
- Regulatory compliance status
- Quality metrics and deviations
- Supply chain performance

**Cold Chain Performance:**

| Product | Temp Range | Shipments | Excursions | Excursion Rate | Product Loss |
|---------|------------|-----------|------------|----------------|--------------|
| Vaccine_A | 2-8°C | 1,250 | 8 | 0.64% | $12,400 |
| Biologic_B | 2-8°C | 850 | 3 | 0.35% | $45,000 |
| Insulin_C | 2-8°C | 3,200 | 15 | 0.47% | $8,200 |
| **Total** | - | **5,300** | **26** | **0.49%** | **$65,600** |

**Quality Metrics:**

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| GDP Compliance | 98% | 100% | ⚠ Yellow |
| Serialization Coverage | 95% | 100% | ⚠ Yellow |
| Deviation Closure (30d) | 87% | 95% | ⚠ Yellow |
| Supplier Audit Compliance | 100% | 100% | ✓ Green |
| OTIF Delivery | 96% | 98% | ⚠ Yellow |

**Deviation Summary:**

| Severity | Count | Open | Overdue | CAPA Required |
|----------|-------|------|---------|---------------|
| Critical | 2 | 1 | 0 | 2 |
| Major | 15 | 4 | 1 | 8 |
| Minor | 42 | 12 | 3 | 0 |
| **Total** | **59** | **17** | **4** | **10** |

**Clinical Trials Status:**

| Trial ID | Phase | Sites | Patients | IMP Stock (weeks) | Issues |
|----------|-------|-------|----------|-------------------|--------|
| TRIAL_001 | III | 45 | 350 | 8 | None |
| TRIAL_002 | II | 12 | 80 | 4 | Low stock at 2 sites |
| TRIAL_003 | I | 3 | 24 | 12 | None |

**Action Items:**
1. Complete CAPA for 2 critical deviations - due by Feb 15
2. Implement backup refrigeration at DC3 - prevent future excursions
3. Complete serialization rollout for remaining 5% of products - by Q2
4. Resolve IMP stock shortage at Trial 002 sites - ship within 48 hours
5. Update GDP procedures for new EU regulations - compliance by March 1

---

## Questions to Ask

If you need more context:
1. What types of pharmaceutical products? (small molecule, biologics, vaccines)
2. What temperature requirements? (2-8°C, frozen, ultra-cold, ambient)
3. What regulatory markets? (US, EU, other regions)
4. What is the current serialization status?
5. Are there any clinical trials requiring support?
6. What are the main quality/compliance challenges?
7. What is the distribution network structure?
8. Are controlled substances involved?

---

## Related Skills

- **clinical-trial-logistics**: For investigational product management
- **cold-chain**: For temperature-controlled logistics
- **quality-management**: For QMS and GxP compliance
- **track-and-trace**: For serialization implementation
- **inventory-optimization**: For safety stock and inventory policies
- **network-design**: For distribution network optimization
- **risk-mitigation**: For supply chain risk management
- **compliance-management**: For regulatory compliance
- **medical-device-distribution**: For device-specific requirements
- **hospital-logistics**: For hospital pharmacy supply chain
