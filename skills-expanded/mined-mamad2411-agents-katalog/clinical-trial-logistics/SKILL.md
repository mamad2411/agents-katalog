---
name: clinical-trial-logistics
description: When the user wants to optimize clinical trial supply chain, manage investigational products, implement IRT systems, or ensure GCP compliance. Also use when the user mentions "clinical trial supply," "IMP logistics," "IVRS/IWRS," "drug accountability," "randomization and supply," "comparator sourcing," "depot management," "clinical packaging," "site resupply," or "GCP compliance." For pharmacy operations, see pharmacy-supply-chain. For general healthcare logistics, see hospital-logistics.
---

# Clinical Trial Logistics

You are an expert in clinical trial supply chain management and logistics. Your goal is to ensure reliable, compliant supply of investigational medicinal products (IMPs) to clinical trial sites while maintaining product integrity, regulatory compliance, and study blinding.

## Initial Assessment

Before optimizing clinical trial logistics, understand:

1. **Trial Characteristics**
   - Trial phase? (Phase I, II, III, IV)
   - Number of sites and countries?
   - Patient enrollment targets and timeline?
   - Blinding requirements? (open-label, single-blind, double-blind)
   - Randomization complexity? (stratification factors)

2. **Product Requirements**
   - Drug form? (tablets, injectables, biologics)
   - Storage conditions? (room temp, refrigerated, frozen)
   - Stability and shelf life?
   - Comparator/placebo requirements?
   - Packaging configuration?

3. **Supply Chain Infrastructure**
   - IRT/IVRS/IWRS system in place?
   - Depot locations? (global, regional)
   - Direct-to-site vs. depot model?
   - Cold chain capabilities?
   - Backup supply strategy?

4. **Compliance & Regulations**
   - GCP (Good Clinical Practice) requirements?
   - Country-specific regulations?
   - Import/export licenses needed?
   - Temperature excursion protocols?
   - Audit readiness?

---

## Clinical Trial Supply Chain Framework

### Trial Supply Models

**1. Direct-to-Site (DTS)**
- Ship directly from manufacturing to sites
- Pros: Reduced handling, faster delivery
- Cons: No buffer stock, complex global logistics
- Best for: Small trials, stable products

**2. Depot-Based Distribution**
- Regional depots hold inventory
- Ship to sites from nearest depot
- Pros: Faster resupply, buffer stock, consolidation
- Cons: Additional handling, storage costs
- Best for: Large global trials

**3. Hybrid Model**
- Depot for some regions, DTS for others
- Optimize based on site density and logistics
- Best for: Multi-regional trials with varied infrastructure

### IRT/IVRS/IWRS System Design

**Interactive Response Technology (IRT):**
- Randomization engine
- Supply allocation and tracking
- Temperature monitoring integration
- Drug accountability
- Resupply triggers

**Core Functions:**

```python
from enum import Enum
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional, Dict
import random

class TreatmentArm(Enum):
    INVESTIGATIONAL = "investigational"
    COMPARATOR = "comparator"
    PLACEBO = "placebo"

class PatientStatus(Enum):
    SCREENED = "screened"
    RANDOMIZED = "randomized"
    ON_TREATMENT = "on_treatment"
    COMPLETED = "completed"
    DISCONTINUED = "discontinued"

@dataclass
class StratificationFactor:
    """Stratification criteria for randomization"""
    factor_name: str
    value: str

@dataclass
class Patient:
    """Clinical trial patient"""
    patient_id: str
    site_id: str
    screening_date: datetime
    status: PatientStatus
    stratification_factors: List[StratificationFactor] = None
    treatment_arm: Optional[TreatmentArm] = None
    randomization_date: Optional[datetime] = None
    allocated_kits: List[str] = None

@dataclass
class DrugKit:
    """IMP drug kit"""
    kit_number: str
    treatment_arm: TreatmentArm
    lot_number: str
    expiry_date: datetime
    site_id: str
    status: str  # available, allocated, dispensed, returned, destroyed
    patient_id: Optional[str] = None
    dispensed_date: Optional[datetime] = None

class IRTSystem:
    """
    Interactive Response Technology for clinical trials
    """

    def __init__(self, trial_id, randomization_ratio, blinded=True):
        self.trial_id = trial_id
        self.randomization_ratio = randomization_ratio  # e.g., {'investigational': 2, 'comparator': 1}
        self.blinded = blinded
        self.patients = {}
        self.drug_kits = {}
        self.randomization_list = []
        self.site_inventory = {}

    def generate_randomization_list(self, total_patients, block_size=6,
                                    stratification_factors=None):
        """
        Generate randomization list with blocking and stratification

        Parameters:
        - total_patients: Total randomization codes to generate
        - block_size: Block size for randomization
        - stratification_factors: List of stratification combinations
        """

        if stratification_factors is None:
            stratification_factors = [None]  # No stratification

        randomization_list = []
        randomization_number = 1

        for strata in stratification_factors:
            num_patients_per_strata = total_patients // len(stratification_factors)

            # Generate treatment sequence based on ratio
            sequence = []
            for treatment, count in self.randomization_ratio.items():
                sequence.extend([TreatmentArm[treatment.upper()]] * count)

            # Generate blocks
            num_blocks = (num_patients_per_strata // block_size) + 1

            for block in range(num_blocks):
                # Shuffle within block
                random.shuffle(sequence)

                for treatment in sequence:
                    if len(randomization_list) >= total_patients:
                        break

                    randomization_list.append({
                        'randomization_number': f"RND-{randomization_number:05d}",
                        'treatment_arm': treatment,
                        'stratification': strata,
                        'block': block + 1
                    })

                    randomization_number += 1

        self.randomization_list = randomization_list[:total_patients]

        return self.randomization_list

    def randomize_patient(self, patient_id, site_id, stratification_values=None):
        """
        Randomize patient and allocate treatment

        Parameters:
        - patient_id: Patient identifier
        - site_id: Study site
        - stratification_values: Dict of stratification factor values
        """

        if patient_id in self.patients:
            raise ValueError(f"Patient {patient_id} already randomized")

        # Find next available randomization code for stratification
        # In real system, this would be from pre-generated randomization list
        available_codes = [
            code for code in self.randomization_list
            if not any(p['randomization_code']['randomization_number'] == code['randomization_number']
                      for p in self.patients.values() if 'randomization_code' in p)
        ]

        if not available_codes:
            raise ValueError("No randomization codes available")

        # Assign next code
        randomization_code = available_codes[0]

        # Create patient record
        patient = {
            'patient_id': patient_id,
            'site_id': site_id,
            'randomization_date': datetime.now(),
            'status': PatientStatus.RANDOMIZED,
            'randomization_code': randomization_code,
            'treatment_arm': randomization_code['treatment_arm'],
            'stratification_values': stratification_values,
            'allocated_kits': []
        }

        self.patients[patient_id] = patient

        # Allocate drug kit
        kit = self._allocate_kit(patient_id, site_id, randomization_code['treatment_arm'])

        if kit:
            patient['allocated_kits'].append(kit['kit_number'])

        return {
            'patient_id': patient_id,
            'randomization_number': randomization_code['randomization_number'],
            'kit_number': kit['kit_number'] if kit else None,
            'dispensing_instructions': self._get_dispensing_instructions()
        }

    def _allocate_kit(self, patient_id, site_id, treatment_arm):
        """
        Allocate drug kit to patient from site inventory
        """

        # Find available kits at site for treatment arm
        site_kits = [
            kit for kit_num, kit in self.drug_kits.items()
            if kit['site_id'] == site_id
            and kit['treatment_arm'] == treatment_arm
            and kit['status'] == 'available'
            and kit['expiry_date'] > datetime.now()
        ]

        if not site_kits:
            # Trigger resupply
            self._trigger_resupply(site_id, treatment_arm)
            return None

        # Allocate kit with earliest expiry (FEFO)
        site_kits.sort(key=lambda x: x['expiry_date'])
        kit = site_kits[0]

        kit['status'] = 'allocated'
        kit['patient_id'] = patient_id
        kit['allocated_date'] = datetime.now()

        return kit

    def dispense_kit(self, kit_number, patient_id, dispensed_by):
        """
        Record kit dispensing to patient
        """

        if kit_number not in self.drug_kits:
            raise ValueError(f"Kit {kit_number} not found")

        kit = self.drug_kits[kit_number]

        if kit['status'] != 'allocated':
            raise ValueError(f"Kit {kit_number} is not allocated (status: {kit['status']})")

        if kit['patient_id'] != patient_id:
            raise ValueError(f"Kit {kit_number} is allocated to different patient")

        kit['status'] = 'dispensed'
        kit['dispensed_date'] = datetime.now()
        kit['dispensed_by'] = dispensed_by

        # Update patient status
        if patient_id in self.patients:
            self.patients[patient_id]['status'] = PatientStatus.ON_TREATMENT

        return {
            'kit_number': kit_number,
            'patient_id': patient_id,
            'dispensed_date': kit['dispensed_date'],
            'accountability_required': True
        }

    def return_kit(self, kit_number, return_reason, returned_by):
        """
        Record kit return (unused or partially used)
        """

        if kit_number not in self.drug_kits:
            raise ValueError(f"Kit {kit_number} not found")

        kit = self.drug_kits[kit_number]

        kit['status'] = 'returned'
        kit['return_date'] = datetime.now()
        kit['return_reason'] = return_reason
        kit['returned_by'] = returned_by

        return kit

    def check_site_inventory(self, site_id):
        """
        Check site inventory levels and trigger resupply if needed
        """

        site_kits = [
            kit for kit in self.drug_kits.values()
            if kit['site_id'] == site_id and kit['status'] == 'available'
        ]

        # Group by treatment arm
        inventory_by_arm = {}
        for arm in TreatmentArm:
            arm_kits = [k for k in site_kits if k['treatment_arm'] == arm]
            inventory_by_arm[arm.value] = {
                'available_kits': len(arm_kits),
                'expiring_soon': len([k for k in arm_kits if k['expiry_date'] < datetime.now() + timedelta(days=90)])
            }

        return inventory_by_arm

    def _trigger_resupply(self, site_id, treatment_arm):
        """
        Trigger site resupply when inventory low
        """

        resupply_request = {
            'site_id': site_id,
            'treatment_arm': treatment_arm,
            'request_date': datetime.now(),
            'priority': 'high',
            'requested_quantity': 20  # Standard resupply quantity
        }

        # In real system, this would integrate with depot management
        print(f"RESUPPLY TRIGGERED: Site {site_id} needs {treatment_arm.value} kits")

        return resupply_request

    def _get_dispensing_instructions(self):
        """
        Generate dispensing instructions for site staff
        """

        if self.blinded:
            return "Dispense assigned kit to patient. DO NOT OPEN OR INSPECT CONTENTS."
        else:
            return "Dispense assigned kit to patient. Verify drug name and strength."

# Example usage
irt = IRTSystem(
    trial_id='TRIAL-2024-001',
    randomization_ratio={'investigational': 2, 'comparator': 1, 'placebo': 1},
    blinded=True
)

# Generate randomization list
random.seed(42)
rand_list = irt.generate_randomization_list(
    total_patients=100,
    block_size=8
)

print(f"Generated {len(rand_list)} randomization codes")

# Add drug kits to site inventory
for i in range(20):
    kit_num = f"KIT-001-{1000+i}"
    arm = random.choice(list(TreatmentArm))

    irt.drug_kits[kit_num] = {
        'kit_number': kit_num,
        'treatment_arm': arm,
        'lot_number': 'LOT-2024-A',
        'expiry_date': datetime.now() + timedelta(days=730),
        'site_id': 'SITE-001',
        'status': 'available',
        'patient_id': None
    }

# Randomize patient
randomization = irt.randomize_patient(
    patient_id='PT-001-001',
    site_id='SITE-001',
    stratification_values={'age_group': '>=65', 'disease_severity': 'moderate'}
)

print(f"\nPatient randomized:")
print(f"  Randomization Number: {randomization['randomization_number']}")
print(f"  Kit Number: {randomization['kit_number']}")

# Dispense kit
dispense = irt.dispense_kit(
    kit_number=randomization['kit_number'],
    patient_id='PT-001-001',
    dispensed_by='Investigator Dr. Smith'
)

print(f"\nKit dispensed: {dispense['kit_number']} on {dispense['dispensed_date']}")

# Check site inventory
inventory = irt.check_site_inventory('SITE-001')
print(f"\nSite inventory:")
for arm, counts in inventory.items():
    print(f"  {arm}: {counts['available_kits']} kits available")
```

---

## Drug Accountability & Reconciliation

### Accountability Requirements

**GCP Requirements:**
- Receipt records
- Dispensing records
- Return records
- Destruction records
- Complete audit trail

```python
import pandas as pd
from datetime import datetime

class DrugAccountabilitySystem:
    """
    Manage drug accountability and reconciliation for clinical trials
    """

    def __init__(self, site_id, trial_id):
        self.site_id = site_id
        self.trial_id = trial_id
        self.transactions = []
        self.inventory = {}

    def receive_shipment(self, shipment_id, kits, received_by,
                        condition, temperature_log=None):
        """
        Record receipt of IMP shipment at site
        """

        receipt_transaction = {
            'transaction_type': 'receipt',
            'transaction_date': datetime.now(),
            'shipment_id': shipment_id,
            'received_by': received_by,
            'condition': condition,
            'temperature_compliant': self._verify_temperature(temperature_log),
            'kits': kits
        }

        self.transactions.append(receipt_transaction)

        # Add to inventory
        for kit in kits:
            self.inventory[kit['kit_number']] = {
                'kit_number': kit['kit_number'],
                'lot_number': kit['lot_number'],
                'expiry_date': kit['expiry_date'],
                'status': 'available',
                'received_date': datetime.now(),
                'patient_id': None
            }

        return receipt_transaction

    def dispense_to_patient(self, kit_number, patient_id, visit_number,
                           dispensed_by, dispense_date=None):
        """
        Record kit dispensing to patient
        """

        if kit_number not in self.inventory:
            raise ValueError(f"Kit {kit_number} not in inventory")

        if self.inventory[kit_number]['status'] != 'available':
            raise ValueError(f"Kit {kit_number} is not available")

        dispense_transaction = {
            'transaction_type': 'dispensed',
            'transaction_date': dispense_date or datetime.now(),
            'kit_number': kit_number,
            'patient_id': patient_id,
            'visit_number': visit_number,
            'dispensed_by': dispensed_by
        }

        self.transactions.append(dispense_transaction)

        # Update inventory
        self.inventory[kit_number]['status'] = 'dispensed'
        self.inventory[kit_number]['patient_id'] = patient_id
        self.inventory[kit_number]['dispensed_date'] = dispense_date or datetime.now()

        return dispense_transaction

    def return_from_patient(self, kit_number, patient_id, return_date,
                           units_returned, units_used, returned_by):
        """
        Record kit return from patient (compliance check)
        """

        if kit_number not in self.inventory:
            raise ValueError(f"Kit {kit_number} not in inventory")

        return_transaction = {
            'transaction_type': 'returned_from_patient',
            'transaction_date': return_date or datetime.now(),
            'kit_number': kit_number,
            'patient_id': patient_id,
            'units_returned': units_returned,
            'units_used': units_used,
            'compliance_pct': (units_used / (units_used + units_returned) * 100) if (units_used + units_returned) > 0 else 0,
            'returned_by': returned_by
        }

        self.transactions.append(return_transaction)

        self.inventory[kit_number]['status'] = 'returned_from_patient'
        self.inventory[kit_number]['units_returned'] = units_returned
        self.inventory[kit_number]['units_used'] = units_used

        return return_transaction

    def quarantine_kit(self, kit_number, reason, quarantined_by):
        """
        Quarantine kit (temperature excursion, damaged, etc.)
        """

        if kit_number not in self.inventory:
            raise ValueError(f"Kit {kit_number} not in inventory")

        quarantine_transaction = {
            'transaction_type': 'quarantined',
            'transaction_date': datetime.now(),
            'kit_number': kit_number,
            'reason': reason,
            'quarantined_by': quarantined_by
        }

        self.transactions.append(quarantine_transaction)

        self.inventory[kit_number]['status'] = 'quarantined'
        self.inventory[kit_number]['quarantine_reason'] = reason

        return quarantine_transaction

    def destroy_kit(self, kit_number, destruction_method, witnessed_by,
                   destruction_certificate=None):
        """
        Record kit destruction
        """

        if kit_number not in self.inventory:
            raise ValueError(f"Kit {kit_number} not in inventory")

        destruction_transaction = {
            'transaction_type': 'destroyed',
            'transaction_date': datetime.now(),
            'kit_number': kit_number,
            'destruction_method': destruction_method,
            'witnessed_by': witnessed_by,
            'destruction_certificate': destruction_certificate
        }

        self.transactions.append(destruction_transaction)

        self.inventory[kit_number]['status'] = 'destroyed'
        self.inventory[kit_number]['destruction_date'] = datetime.now()

        return destruction_transaction

    def return_to_sponsor(self, kit_numbers, shipment_id, shipped_by,
                         tracking_number, return_reason):
        """
        Return kits to sponsor/depot
        """

        return_transaction = {
            'transaction_type': 'returned_to_sponsor',
            'transaction_date': datetime.now(),
            'kit_numbers': kit_numbers,
            'shipment_id': shipment_id,
            'shipped_by': shipped_by,
            'tracking_number': tracking_number,
            'return_reason': return_reason
        }

        self.transactions.append(return_transaction)

        for kit_number in kit_numbers:
            if kit_number in self.inventory:
                self.inventory[kit_number]['status'] = 'returned_to_sponsor'
                self.inventory[kit_number]['return_date'] = datetime.now()

        return return_transaction

    def reconcile_inventory(self, physical_count_by_kit):
        """
        Reconcile physical inventory with system records
        """

        discrepancies = []

        for kit_number, physical_status in physical_count_by_kit.items():
            system_status = self.inventory.get(kit_number, {}).get('status', 'NOT_IN_SYSTEM')

            if physical_status != system_status:
                discrepancies.append({
                    'kit_number': kit_number,
                    'system_status': system_status,
                    'physical_status': physical_status,
                    'discrepancy_type': self._classify_discrepancy(system_status, physical_status)
                })

        reconciliation = {
            'reconciliation_date': datetime.now(),
            'site_id': self.site_id,
            'total_kits_system': len(self.inventory),
            'total_kits_physical': len(physical_count_by_kit),
            'discrepancies': discrepancies,
            'reconciliation_status': 'CLEAN' if len(discrepancies) == 0 else 'DISCREPANCIES_FOUND'
        }

        return reconciliation

    def _classify_discrepancy(self, system_status, physical_status):
        """Classify type of discrepancy"""
        if system_status == 'NOT_IN_SYSTEM':
            return 'EXTRA_KIT_FOUND'
        elif physical_status == 'NOT_FOUND':
            return 'KIT_MISSING'
        else:
            return 'STATUS_MISMATCH'

    def _verify_temperature(self, temperature_log):
        """Verify temperature compliance during shipment"""
        if not temperature_log:
            return None

        # Check all readings in range
        compliant = all(
            log['min_temp'] <= log['temperature'] <= log['max_temp']
            for log in temperature_log
        )

        return compliant

    def accountability_report(self, report_date=None):
        """
        Generate drug accountability report
        """

        report_date = report_date or datetime.now()

        # Group inventory by status
        inventory_df = pd.DataFrame(self.inventory.values())

        if len(inventory_df) == 0:
            return None

        status_summary = inventory_df.groupby('status').size().to_dict()

        # Recent transactions
        recent_transactions = [
            t for t in self.transactions
            if t['transaction_date'] >= report_date - timedelta(days=30)
        ]

        report = {
            'site_id': self.site_id,
            'trial_id': self.trial_id,
            'report_date': report_date,
            'inventory_summary': status_summary,
            'total_kits': len(inventory_df),
            'dispensed_kits': len(inventory_df[inventory_df['status'] == 'dispensed']),
            'available_kits': len(inventory_df[inventory_df['status'] == 'available']),
            'recent_transactions': len(recent_transactions),
            'transactions': recent_transactions
        }

        return report

# Example usage
accountability = DrugAccountabilitySystem(
    site_id='SITE-001',
    trial_id='TRIAL-2024-001'
)

# Receive shipment
kits = [
    {'kit_number': 'KIT-001-1001', 'lot_number': 'LOT-A', 'expiry_date': datetime(2026, 12, 31)},
    {'kit_number': 'KIT-001-1002', 'lot_number': 'LOT-A', 'expiry_date': datetime(2026, 12, 31)},
    {'kit_number': 'KIT-001-1003', 'lot_number': 'LOT-A', 'expiry_date': datetime(2026, 12, 31)}
]

receipt = accountability.receive_shipment(
    shipment_id='SHIP-2024-0015',
    kits=kits,
    received_by='Study Coordinator Jane Doe',
    condition='Good',
    temperature_log=[{'temperature': 6, 'min_temp': 2, 'max_temp': 8}]
)

print(f"Received {len(kits)} kits")

# Dispense to patient
dispense = accountability.dispense_to_patient(
    kit_number='KIT-001-1001',
    patient_id='PT-001-001',
    visit_number='Visit 2',
    dispensed_by='Investigator Dr. Smith'
)

print(f"Dispensed kit {dispense['kit_number']} to patient {dispense['patient_id']}")

# Generate accountability report
report = accountability.accountability_report()
print(f"\nAccountability Report:")
print(f"  Total kits: {report['total_kits']}")
print(f"  Available: {report['available_kits']}")
print(f"  Dispensed: {report['dispensed_kits']}")
print(f"  Inventory summary: {report['inventory_summary']}")
```

---

## Temperature-Controlled Logistics

### Cold Chain Management for Clinical Trials

**Temperature Ranges:**
- Room temperature: 15-25°C (59-77°F)
- Refrigerated: 2-8°C (36-46°F)
- Frozen: -20°C (-4°F)
- Ultra-cold: -80°C (-112°F)

```python
class ClinicalColdChainManager:
    """
    Manage temperature-controlled shipments for clinical trials
    """

    def __init__(self, trial_id):
        self.trial_id = trial_id
        self.shipments = {}
        self.excursions = []

    def create_shipment(self, shipment_id, product_name, from_location,
                       to_location, temp_requirement, packaging_type):
        """
        Create temperature-controlled shipment
        """

        shipment = {
            'shipment_id': shipment_id,
            'product_name': product_name,
            'from_location': from_location,
            'to_location': to_location,
            'temp_requirement': temp_requirement,  # e.g., (2, 8) for 2-8°C
            'packaging_type': packaging_type,
            'ship_date': None,
            'delivery_date': None,
            'temperature_log': [],
            'excursions_detected': [],
            'status': 'pending'
        }

        self.shipments[shipment_id] = shipment

        return shipment

    def ship(self, shipment_id, data_logger_id, carrier, tracking_number):
        """
        Ship temperature-controlled package
        """

        if shipment_id not in self.shipments:
            raise ValueError(f"Shipment {shipment_id} not found")

        shipment = self.shipments[shipment_id]

        shipment['ship_date'] = datetime.now()
        shipment['data_logger_id'] = data_logger_id
        shipment['carrier'] = carrier
        shipment['tracking_number'] = tracking_number
        shipment['status'] = 'in_transit'

        return shipment

    def record_temperature(self, shipment_id, timestamp, temperature, location='in transit'):
        """
        Record temperature reading from data logger
        """

        if shipment_id not in self.shipments:
            raise ValueError(f"Shipment {shipment_id} not found")

        shipment = self.shipments[shipment_id]
        min_temp, max_temp = shipment['temp_requirement']

        reading = {
            'timestamp': timestamp,
            'temperature': temperature,
            'location': location,
            'in_range': min_temp <= temperature <= max_temp
        }

        shipment['temperature_log'].append(reading)

        # Check for excursion
        if not reading['in_range']:
            excursion = {
                'shipment_id': shipment_id,
                'timestamp': timestamp,
                'temperature': temperature,
                'required_range': shipment['temp_requirement'],
                'deviation': abs(temperature - ((min_temp + max_temp) / 2)),
                'location': location
            }

            shipment['excursions_detected'].append(excursion)
            self.excursions.append(excursion)

            # Trigger alert
            self._temperature_excursion_alert(excursion)

        return reading

    def deliver_shipment(self, shipment_id, received_by, condition_assessment):
        """
        Record shipment delivery
        """

        if shipment_id not in self.shipments:
            raise ValueError(f"Shipment {shipment_id} not found")

        shipment = self.shipments[shipment_id]

        shipment['delivery_date'] = datetime.now()
        shipment['received_by'] = received_by
        shipment['condition_assessment'] = condition_assessment
        shipment['status'] = 'delivered'

        # Analyze temperature compliance
        compliance = self._analyze_temperature_compliance(shipment)

        shipment['temperature_compliance'] = compliance

        return {
            'shipment_id': shipment_id,
            'delivery_date': shipment['delivery_date'],
            'temperature_compliant': compliance['compliant'],
            'excursions': len(shipment['excursions_detected']),
            'disposition': self._determine_disposition(compliance)
        }

    def _analyze_temperature_compliance(self, shipment):
        """
        Analyze temperature compliance for shipment
        """

        temp_log = shipment['temperature_log']

        if not temp_log:
            return {'compliant': None, 'reason': 'No temperature data'}

        total_readings = len(temp_log)
        compliant_readings = sum(1 for r in temp_log if r['in_range'])
        compliance_rate = (compliant_readings / total_readings * 100) if total_readings > 0 else 0

        num_excursions = len(shipment['excursions_detected'])

        # Determine compliance
        compliant = (compliance_rate >= 95 and num_excursions == 0)

        return {
            'compliant': compliant,
            'compliance_rate': round(compliance_rate, 2),
            'num_excursions': num_excursions,
            'total_readings': total_readings,
            'compliant_readings': compliant_readings
        }

    def _determine_disposition(self, compliance):
        """
        Determine product disposition based on compliance
        """

        if compliance['compliant']:
            return 'ACCEPT - Use per protocol'
        elif compliance['num_excursions'] > 0:
            return 'QUARANTINE - Investigate excursion, stability assessment required'
        else:
            return 'QUARANTINE - Temperature compliance review required'

    def _temperature_excursion_alert(self, excursion):
        """
        Send alert for temperature excursion
        """

        print(f"⚠ TEMPERATURE EXCURSION ALERT")
        print(f"  Shipment: {excursion['shipment_id']}")
        print(f"  Temperature: {excursion['temperature']}°C")
        print(f"  Required range: {excursion['required_range']}")
        print(f"  Time: {excursion['timestamp']}")

    def excursion_investigation_report(self, shipment_id):
        """
        Generate excursion investigation report
        """

        if shipment_id not in self.shipments:
            raise ValueError(f"Shipment {shipment_id} not found")

        shipment = self.shipments[shipment_id]

        if not shipment['excursions_detected']:
            return {'investigation_required': False}

        # Analyze excursions
        excursions_df = pd.DataFrame(shipment['excursions_detected'])

        report = {
            'shipment_id': shipment_id,
            'product_name': shipment['product_name'],
            'investigation_required': True,
            'num_excursions': len(shipment['excursions_detected']),
            'excursion_details': excursions_df.to_dict('records'),
            'total_time_out_of_range': 'Calculate from timestamp data',
            'max_deviation': excursions_df['deviation'].max() if len(excursions_df) > 0 else 0,
            'recommended_action': self._excursion_recommended_action(shipment),
            'stability_data_required': True,
            'sponsor_notification_required': True
        }

        return report

    def _excursion_recommended_action(self, shipment):
        """
        Recommend action for excursion
        """

        excursions = shipment['excursions_detected']

        if not excursions:
            return 'No action required'

        max_deviation = max(e['deviation'] for e in excursions)

        if max_deviation > 10:
            return 'REJECT - Significant excursion, product unusable'
        elif max_deviation > 5:
            return 'QUARANTINE - Contact sponsor, stability data review required'
        else:
            return 'QUARANTINE - Minor excursion, sponsor review required'

# Example usage
cold_chain = ClinicalColdChainManager(trial_id='TRIAL-2024-001')

# Create shipment
shipment = cold_chain.create_shipment(
    shipment_id='SHIP-2024-0020',
    product_name='Investigational Biologic ABC-123',
    from_location='Depot - Amsterdam',
    to_location='Site 105 - Memorial Hospital',
    temp_requirement=(2, 8),  # 2-8°C
    packaging_type='Qualified shipper with dry ice'
)

# Ship
cold_chain.ship(
    shipment_id='SHIP-2024-0020',
    data_logger_id='LOGGER-5678',
    carrier='FedEx Priority Overnight',
    tracking_number='FX123456789'
)

# Simulate temperature readings
import numpy as np
np.random.seed(42)

for hour in range(36):  # 36 hours in transit
    temp = 5 + np.random.normal(0, 1.5)

    # Simulate excursion at hour 20
    if hour == 20:
        temp = 12  # Excursion

    cold_chain.record_temperature(
        shipment_id='SHIP-2024-0020',
        timestamp=datetime.now() + timedelta(hours=hour),
        temperature=round(temp, 1)
    )

# Deliver
delivery = cold_chain.deliver_shipment(
    shipment_id='SHIP-2024-0020',
    received_by='Study Coordinator at Site 105',
    condition_assessment='Package intact, data logger attached'
)

print(f"Shipment delivered:")
print(f"  Temperature compliant: {delivery['temperature_compliant']}")
print(f"  Excursions: {delivery['excursions']}")
print(f"  Disposition: {delivery['disposition']}")

# Excursion investigation
if delivery['excursions'] > 0:
    investigation = cold_chain.excursion_investigation_report('SHIP-2024-0020')
    print(f"\n Excursion Investigation Required:")
    print(f"  Number of excursions: {investigation['num_excursions']}")
    print(f"  Max deviation: {investigation['max_deviation']:.1f}°C")
    print(f"  Recommended action: {investigation['recommended_action']}")
```

---

## Comparator Sourcing & Management

### Commercial Comparator Procurement

**Challenges:**
- Sourcing commercial drugs in different countries
- Ensuring consistent quality across batches
- Managing expiry dates
- Blinding/overencapsulation
- Import/export compliance

```python
class ComparatorManager:
    """
    Manage comparator drug sourcing and inventory
    """

    def __init__(self, trial_id):
        self.trial_id = trial_id
        self.comparators = {}
        self.procurement_orders = []

    def add_comparator(self, comparator_id, drug_name, strength,
                      countries_needed, blinding_required):
        """
        Add comparator to trial requirements
        """

        self.comparators[comparator_id] = {
            'comparator_id': comparator_id,
            'drug_name': drug_name,
            'strength': strength,
            'countries_needed': countries_needed,
            'blinding_required': blinding_required,
            'sourcing_strategy': self._determine_sourcing_strategy(countries_needed)
        }

    def _determine_sourcing_strategy(self, countries_needed):
        """
        Determine optimal sourcing strategy
        """

        if len(countries_needed) == 1:
            return 'local_sourcing'
        elif len(countries_needed) <= 5:
            return 'regional_sourcing'
        else:
            return 'global_sourcing_multiple_suppliers'

    def create_procurement_order(self, comparator_id, country, quantity,
                                target_delivery_date, supplier=None):
        """
        Create procurement order for comparator
        """

        if comparator_id not in self.comparators:
            raise ValueError(f"Comparator {comparator_id} not defined")

        comparator = self.comparators[comparator_id]

        order = {
            'order_id': f"PO-{len(self.procurement_orders)+1:05d}",
            'comparator_id': comparator_id,
            'drug_name': comparator['drug_name'],
            'country': country,
            'quantity': quantity,
            'target_delivery_date': target_delivery_date,
            'supplier': supplier or 'To be determined',
            'order_date': datetime.now(),
            'status': 'pending',
            'import_license_required': self._check_import_requirements(country),
            'blinding_required': comparator['blinding_required']
        }

        self.procurement_orders.append(order)

        return order

    def _check_import_requirements(self, country):
        """Check if import license required"""
        # Simplified - would check regulatory database
        controlled_countries = ['US', 'CA', 'AU', 'JP']
        return country in controlled_countries

    def quality_assessment(self, order_id, batch_number, test_results):
        """
        Record quality assessment of received comparator
        """

        order = next((o for o in self.procurement_orders if o['order_id'] == order_id), None)

        if not order:
            raise ValueError(f"Order {order_id} not found")

        assessment = {
            'order_id': order_id,
            'batch_number': batch_number,
            'assessment_date': datetime.now(),
            'test_results': test_results,
            'acceptable': all(t['result'] == 'pass' for t in test_results),
            'release_status': 'released' if all(t['result'] == 'pass' for t in test_results) else 'rejected'
        }

        order['quality_assessment'] = assessment
        order['status'] = assessment['release_status']

        return assessment

# Example usage
comparator_mgr = ComparatorManager(trial_id='TRIAL-2024-001')

# Add comparator requirement
comparator_mgr.add_comparator(
    comparator_id='COMP-001',
    drug_name='Lipitor (Atorvastatin) 40mg',
    strength='40mg',
    countries_needed=['US', 'UK', 'Germany', 'France', 'Japan'],
    blinding_required=True
)

# Create procurement orders
order_us = comparator_mgr.create_procurement_order(
    comparator_id='COMP-001',
    country='US',
    quantity=5000,
    target_delivery_date=datetime.now() + timedelta(days=90),
    supplier='Cardinal Health'
)

print(f"Procurement order created: {order_us['order_id']}")
print(f"  Import license required: {order_us['import_license_required']}")
print(f"  Blinding required: {order_us['blinding_required']}")

# Quality assessment
test_results = [
    {'test': 'Identification', 'result': 'pass'},
    {'test': 'Assay', 'result': 'pass', 'value': '99.2% (90-110% spec)'},
    {'test': 'Dissolution', 'result': 'pass'},
    {'test': 'Uniformity of Dosage Units', 'result': 'pass'}
]

qa = comparator_mgr.quality_assessment(
    order_id=order_us['order_id'],
    batch_number='BATCH-US-2024-A',
    test_results=test_results
)

print(f"\nQuality Assessment:")
print(f"  Acceptable: {qa['acceptable']}")
print(f"  Release status: {qa['release_status']}")
```

---

## Clinical Trial Supply Chain Metrics

### Key Performance Indicators

```python
def calculate_clinical_trial_kpis(supply_data, enrollment_data, shipment_data):
    """
    Calculate clinical trial supply chain KPIs

    Parameters:
    - supply_data: Site inventory and supply data
    - enrollment_data: Patient enrollment data
    - shipment_data: Shipment performance data
    """

    kpis = {}

    # Stockout rate (sites without adequate supply)
    if 'stockout_event' in supply_data.columns:
        kpis['stockout_rate'] = (supply_data['stockout_event'].sum() / len(supply_data) * 100)

    # Depot-to-site delivery time
    if 'delivery_time_days' in shipment_data.columns:
        kpis['avg_delivery_time_days'] = shipment_data['delivery_time_days'].mean()

    # Temperature compliance rate
    if 'temp_compliant' in shipment_data.columns:
        kpis['temp_compliance_rate'] = (shipment_data['temp_compliant'].sum() / len(shipment_data) * 100)

    # Drug accountability compliance
    if 'accountability_complete' in supply_data.columns:
        kpis['accountability_compliance'] = (supply_data['accountability_complete'].sum() / len(supply_data) * 100)

    # Expiry waste rate
    if 'expired_kits' in supply_data.columns and 'total_kits' in supply_data.columns:
        total_expired = supply_data['expired_kits'].sum()
        total_kits = supply_data['total_kits'].sum()
        kpis['expiry_waste_rate'] = (total_expired / total_kits * 100) if total_kits > 0 else 0

    # Randomization-to-supply time (time to get drug after randomization)
    if 'randomization_to_supply_hours' in enrollment_data.columns:
        kpis['avg_randomization_to_supply_hours'] = enrollment_data['randomization_to_supply_hours'].mean()

    # Forecasting accuracy (planned vs. actual enrollment)
    if all(col in enrollment_data.columns for col in ['planned_enrollment', 'actual_enrollment']):
        planned = enrollment_data['planned_enrollment'].sum()
        actual = enrollment_data['actual_enrollment'].sum()
        kpis['enrollment_vs_forecast_pct'] = (actual / planned * 100) if planned > 0 else 0

    # Format KPIs
    for key in kpis:
        if 'rate' in key or 'compliance' in key or 'pct' in key:
            kpis[key] = round(kpis[key], 2)
        else:
            kpis[key] = round(kpis[key], 1)

    return kpis

# Example data
supply_data = pd.DataFrame({
    'site_id': [f'SITE-{i:03d}' for i in range(1, 51)],
    'stockout_event': np.random.choice([True, False], 50, p=[0.05, 0.95]),
    'accountability_complete': np.random.choice([True, False], 50, p=[0.98, 0.02]),
    'expired_kits': np.random.randint(0, 5, 50),
    'total_kits': np.random.randint(20, 100, 50)
})

shipment_data = pd.DataFrame({
    'shipment_id': range(1, 201),
    'delivery_time_days': np.random.normal(5, 2, 200),
    'temp_compliant': np.random.choice([True, False], 200, p=[0.97, 0.03])
})

enrollment_data = pd.DataFrame({
    'site_id': [f'SITE-{i:03d}' for i in range(1, 51)],
    'planned_enrollment': [20] * 50,
    'actual_enrollment': np.random.randint(15, 25, 50),
    'randomization_to_supply_hours': np.random.normal(2, 0.5, 50)
})

kpis = calculate_clinical_trial_kpis(supply_data, enrollment_data, shipment_data)

print("Clinical Trial Supply Chain KPIs:")
for metric, value in kpis.items():
    suffix = '%' if any(x in metric for x in ['rate', 'pct', 'compliance']) else ''
    print(f"  {metric}: {value}{suffix}")
```

---

## Tools & Libraries

### Clinical Trial Supply Systems

**IRT/IVRS/IWRS:**
- **Almac IVRS**: Interactive voice/web response
- **Perceptive MyTrials**: Cloud-based IRT
- **Oracle InForm IWRS**: Integrated with EDC
- **Signant SmartSignals**: IRT with supply forecasting
- **DATATRAK eIVRS**: Electronic interactive system

**Supply Chain Management:**
- **Marken**: Clinical trial logistics and distribution
- **Thermo Fisher Clinical Trials**: Depot and distribution
- **Almac Clinical Services**: Packaging, labeling, distribution
- **Sharp Clinical Services**: Clinical packaging and logistics
- **Catalent**: Packaging and logistics

**Temperature Monitoring:**
- **Sensitech**: Cold chain monitoring
- **Tive**: Real-time tracking and monitoring
- **Emerson Cargo Solutions**: Temperature monitoring
- **Controlant**: Real-time supply chain visibility

### Python Libraries

**Data Analysis:**
- `pandas`: Data manipulation
- `numpy`: Numerical computing
- `scipy`: Statistical analysis

**Randomization:**
- `random`: Random number generation
- `numpy.random`: Advanced randomization

**Optimization:**
- `pulp`: Linear programming (supply optimization)
- `scipy.optimize`: Optimization algorithms

**Visualization:**
- `matplotlib`, `seaborn`: Charts
- `plotly`: Interactive dashboards

---

## Common Challenges & Solutions

### Challenge: Patient Randomization Without Supply Available

**Problem:**
- Patient randomized but no kit available at site
- Impacts patient care and protocol compliance
- Site frustration

**Solutions:**
- Conservative forecasting with buffer stock
- Real-time inventory monitoring in IRT
- Automatic resupply triggers
- Emergency supply procedures
- Alternative site supply (if blinding permits)

### Challenge: Temperature Excursions During Shipment

**Problem:**
- Product exposed to out-of-spec temperatures
- Uncertainty about product integrity
- Potential patient safety risk
- Protocol deviation

**Solutions:**
- Qualified packaging validation
- Redundant temperature monitoring
- Real-time alerts for excursions
- Pre-defined disposition protocols
- Stability data to support use decisions
- Alternative routing/carriers for problem lanes

### Challenge: Expired Product at Sites

**Problem:**
- Kits expire before use
- Waste and resupply costs
- Enrollment delays if resupply needed

**Solutions:**
- Just-in-time supply strategy
- FEFO allocation in IRT
- Expiry-based resupply triggers
- Pooling/transfer between sites (if protocol allows)
- Reduced PAR levels for slow-enrolling sites
- Return programs for usable inventory

### Challenge: Drug Accountability Discrepancies

**Problem:**
- Physical count doesn't match system records
- Regulatory compliance risk
- Audit findings

**Solutions:**
- Electronic drug accountability systems
- Regular reconciliation (monthly minimum)
- Two-person verification for high-value products
- Training for site staff
- Clear procedures and documentation
- Root cause analysis for all discrepancies

### Challenge: Global Import/Export Delays

**Problem:**
- Regulatory delays at customs
- Missing documentation
- Import license delays
- Product stuck at border

**Solutions:**
- Early import license applications
- Experienced customs brokers
- Complete documentation packages
- Regulatory intelligence monitoring
- Buffer stock in-country
- Pre-positioning inventory where possible

### Challenge: Comparator Sourcing Complexity

**Problem:**
- Different formulations/packaging by country
- Quality consistency across batches
- Blinding challenges
- Supply availability

**Solutions:**
- Early sourcing (12+ months before site activation)
- Quality agreements with suppliers
- Overencapsulation for blinding
- Multiple supplier qualification
- Central testing and release
- Contingency suppliers identified

---

## Output Format

### Clinical Trial Supply Report

**Executive Summary:**
- Trial overview (phase, sites, enrollment)
- Supply chain model (depot vs. direct-to-site)
- Key performance metrics
- Critical issues and actions

**Site Supply Status:**

| Site ID | Country | Enrollment | Available Kits by Arm | Days Supply | Expiry Risk | Last Shipment | Status |
|---------|---------|------------|----------------------|-------------|-------------|---------------|--------|
| SITE-001 | USA | 12/20 | Inv:15, Comp:15, Pbo:15 | 45 days | None | 2024-02-01 | ✓ OK |
| SITE-015 | UK | 8/20 | Inv:3, Comp:3, Pbo:3 | 12 days | None | 2024-01-28 | ⚠ Low |
| SITE-023 | Germany | 15/20 | Inv:8, Comp:7, Pbo:8 | 20 days | 2 kits <90d | 2024-02-05 | ⚠ Expiry |

**Shipment Performance:**

| Metric | Current Month | YTD | Target | Status |
|--------|---------------|-----|--------|--------|
| On-Time Delivery | 94.2% | 95.8% | 95% | ✓ |
| Temperature Compliance | 97.1% | 98.3% | 98% | ✓ |
| Avg Delivery Time | 4.8 days | 5.2 days | <5 days | ✓ |
| Customs Delays | 2 shipments | 8 shipments | - | ⚠ |

**Drug Accountability:**

| Status | Kits | % |
|--------|------|---|
| Available | 1,245 | 52% |
| Dispensed | 892 | 37% |
| Returned | 215 | 9% |
| Quarantined | 12 | 0.5% |
| Destroyed | 25 | 1% |
| Expired | 8 | 0.3% |

**Temperature Excursions:**

| Shipment ID | Route | Excursion Type | Max Deviation | Duration | Disposition |
|-------------|-------|----------------|---------------|----------|-------------|
| SHIP-2024-0045 | Depot→Site-023 | High temp | +6°C | 2 hours | Under investigation |
| SHIP-2024-0031 | Depot→Site-008 | Low temp | -3°C | 30 min | Accepted - within stability |

**Action Items:**
1. Resupply SITE-015 (priority shipment initiated)
2. Transfer expiring inventory from SITE-023 to SITE-029
3. Complete excursion investigation for SHIP-2024-0045
4. Address customs delays in Italy (2 shipments affected)

---

## Questions to Ask

If you need more context:

1. What phase is the clinical trial? (I, II, III, IV)
2. How many sites and countries?
3. What are the product storage requirements?
4. Is the study blinded? (single, double, open-label)
5. What's the enrollment target and timeline?
6. Is an IRT system in place?
7. What distribution model? (depot, direct-to-site, hybrid)
8. Are there comparators or placebos?
9. What are the main supply chain challenges currently?
10. What's the regulatory landscape? (FDA, EMA, other)

---

## Related Skills

- **pharmacy-supply-chain**: Pharmaceutical supply chain management
- **hospital-logistics**: Hospital materials management
- **medical-device-distribution**: Medical device logistics
- **compliance-management**: Regulatory compliance and quality
- **track-and-trace**: Product traceability
- **inventory-optimization**: Inventory optimization techniques
- **demand-forecasting**: Forecasting for supply planning
- **cold-chain-logistics**: Temperature-controlled logistics (if exists)
- **quality-management**: Quality management systems
