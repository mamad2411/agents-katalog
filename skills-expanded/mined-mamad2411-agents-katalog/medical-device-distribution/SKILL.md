---
name: medical-device-distribution
description: When the user wants to optimize medical device distribution, manage device traceability, handle consignment inventory, or ensure regulatory compliance for medical devices. Also use when the user mentions "medical device logistics," "UDI compliance," "device traceability," "consignment management," "implant tracking," "loaner sets," "FDA compliance," "sterile device distribution," "recall management," or "GS1 standards." For hospital internal logistics, see hospital-logistics. For pharmaceutical distribution, see pharmacy-supply-chain.
---

# Medical Device Distribution

You are an expert in medical device distribution and supply chain management. Your goal is to ensure compliant, efficient distribution of medical devices while maintaining traceability, managing regulatory requirements, and optimizing inventory costs.

## Initial Assessment

Before optimizing medical device distribution, understand:

1. **Device Categories**
   - Device classifications? (Class I, II, III)
   - Product types? (implants, capital equipment, disposables, loaner sets)
   - High-value vs. high-volume products?
   - Sterile vs. non-sterile requirements?

2. **Regulatory Landscape**
   - FDA registration status?
   - UDI compliance requirements?
   - QMS (Quality Management System) in place?
   - International distribution? (CE Mark, other countries)

3. **Distribution Network**
   - Direct distribution vs. through distributors?
   - Number of distribution centers?
   - Customer types? (hospitals, clinics, surgery centers)
   - Geographic coverage?

4. **Current Challenges**
   - Traceability gaps?
   - Recall preparedness?
   - Consignment inventory management?
   - Expiry/obsolescence issues?
   - Compliance violations or warning letters?

---

## Medical Device Distribution Framework

### Device Classification & Requirements

**FDA Device Classes:**

**Class I (Low Risk):**
- Examples: Bandages, examination gloves, handheld instruments
- Requirements: General controls, most exempt from 510(k)
- Distribution: Standard supply chain, minimal special handling

**Class II (Moderate Risk):**
- Examples: Powered wheelchairs, infusion pumps, surgical drapes
- Requirements: General + special controls, 510(k) clearance usually required
- Distribution: Enhanced traceability, often UDI required

**Class III (High Risk):**
- Examples: Pacemakers, heart valves, implantable defibrillators
- Requirements: Premarket approval (PMA), strictest controls
- Distribution: Full traceability, serialization, consignment common

### Unique Device Identification (UDI) Compliance

**UDI Requirements:**
- Unique identifier on device label and packaging
- Direct marking on implantable devices
- Registration in FDA's GUDID (Global Unique Device Identification Database)
- Tracking through distribution chain

**UDI Structure:**
```
UDI = Device Identifier (DI) + Production Identifier (PI)

DI: Identifies the specific device (model, version)
PI: Identifies the production unit (lot, serial number, expiry, manufacture date)
```

**Implementation:**

```python
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class UDI:
    """
    Unique Device Identification structure
    """
    device_identifier: str  # DI - identifies device model
    lot_number: Optional[str] = None
    serial_number: Optional[str] = None
    manufacturing_date: Optional[datetime] = None
    expiration_date: Optional[datetime] = None
    donation_id: Optional[str] = None  # For blood/tissue

    def to_gs1_string(self):
        """Convert to GS1 format"""
        udi_string = f"(01){self.device_identifier}"

        if self.lot_number:
            udi_string += f"(10){self.lot_number}"

        if self.serial_number:
            udi_string += f"(21){self.serial_number}"

        if self.expiration_date:
            exp_date = self.expiration_date.strftime("%y%m%d")
            udi_string += f"(17){exp_date}"

        if self.manufacturing_date:
            mfg_date = self.manufacturing_date.strftime("%y%m%d")
            udi_string += f"(11){mfg_date}"

        return udi_string

    @staticmethod
    def parse_gs1(gs1_string):
        """Parse GS1 UDI string"""
        # Application Identifiers (AI)
        patterns = {
            'device_identifier': r'\(01\)(\d{14})',
            'lot_number': r'\(10\)([A-Za-z0-9]+)',
            'serial_number': r'\(21\)([A-Za-z0-9]+)',
            'expiration_date': r'\(17\)(\d{6})',
            'manufacturing_date': r'\(11\)(\d{6})'
        }

        udi_data = {}

        for field, pattern in patterns.items():
            match = re.search(pattern, gs1_string)
            if match:
                value = match.group(1)
                if 'date' in field:
                    # Convert YYMMDD to datetime
                    udi_data[field] = datetime.strptime(value, "%y%m%d")
                else:
                    udi_data[field] = value

        return UDI(**udi_data)

# Example usage
device_udi = UDI(
    device_identifier="10884521123456",
    lot_number="LOT2024A",
    serial_number="SN123456789",
    expiration_date=datetime(2027, 12, 31)
)

gs1_string = device_udi.to_gs1_string()
print(f"GS1 UDI: {gs1_string}")

# Parse back
parsed_udi = UDI.parse_gs1(gs1_string)
print(f"Parsed Serial: {parsed_udi.serial_number}")
print(f"Parsed Expiry: {parsed_udi.expiration_date}")
```

---

## Traceability & Serialization

### End-to-End Traceability System

```python
import pandas as pd
from datetime import datetime
from enum import Enum

class EventType(Enum):
    MANUFACTURED = "manufactured"
    SHIPPED = "shipped"
    RECEIVED = "received"
    IMPLANTED = "implanted"
    RETURNED = "returned"
    RECALLED = "recalled"

class TraceabilitySystem:
    """
    Track medical devices through supply chain
    """

    def __init__(self):
        self.events = []

    def record_event(self, event_type, device_id, serial_number,
                     location, operator, timestamp=None, metadata=None):
        """
        Record a traceability event

        Parameters:
        - event_type: Type of event (EventType enum)
        - device_id: Device identifier (DI)
        - serial_number: Unique serial number
        - location: Where event occurred
        - operator: Who performed action
        - timestamp: When it occurred (defaults to now)
        - metadata: Additional data (patient ID, lot, etc.)
        """

        if timestamp is None:
            timestamp = datetime.now()

        event = {
            'event_type': event_type.value,
            'device_id': device_id,
            'serial_number': serial_number,
            'location': location,
            'operator': operator,
            'timestamp': timestamp,
            'metadata': metadata or {}
        }

        self.events.append(event)

        return event

    def trace_device_history(self, serial_number):
        """
        Get complete history for a device by serial number
        """

        device_events = [
            e for e in self.events
            if e['serial_number'] == serial_number
        ]

        # Sort by timestamp
        device_events.sort(key=lambda x: x['timestamp'])

        return pd.DataFrame(device_events)

    def find_devices_by_lot(self, lot_number):
        """
        Find all devices from a specific lot (for recalls)
        """

        devices = [
            e for e in self.events
            if e.get('metadata', {}).get('lot_number') == lot_number
        ]

        # Get unique serial numbers
        serial_numbers = list(set(e['serial_number'] for e in devices))

        return serial_numbers

    def implanted_devices_report(self, start_date, end_date):
        """
        Report of devices implanted in date range
        """

        implanted = [
            e for e in self.events
            if e['event_type'] == EventType.IMPLANTED.value
            and start_date <= e['timestamp'] <= end_date
        ]

        return pd.DataFrame(implanted)

    def audit_trail(self, device_id=None, location=None, date_range=None):
        """
        Generate audit trail for compliance
        """

        filtered_events = self.events

        if device_id:
            filtered_events = [e for e in filtered_events if e['device_id'] == device_id]

        if location:
            filtered_events = [e for e in filtered_events if e['location'] == location]

        if date_range:
            start, end = date_range
            filtered_events = [
                e for e in filtered_events
                if start <= e['timestamp'] <= end
            ]

        return pd.DataFrame(filtered_events)

# Example usage
traceability = TraceabilitySystem()

# Manufacturing event
traceability.record_event(
    EventType.MANUFACTURED,
    device_id="10884521123456",
    serial_number="SN123456789",
    location="Manufacturing Plant A",
    operator="Production Line 3",
    metadata={'lot_number': 'LOT2024A', 'manufacturing_date': '2024-01-15'}
)

# Shipment to distributor
traceability.record_event(
    EventType.SHIPPED,
    device_id="10884521123456",
    serial_number="SN123456789",
    location="Distribution Center East",
    operator="Warehouse Operator J.Smith",
    metadata={'tracking_number': 'TRACK123', 'carrier': 'FedEx'}
)

# Receipt at hospital
traceability.record_event(
    EventType.RECEIVED,
    device_id="10884521123456",
    serial_number="SN123456789",
    location="Memorial Hospital",
    operator="Materials Manager",
    metadata={'purchase_order': 'PO-2024-5678'}
)

# Implantation
traceability.record_event(
    EventType.IMPLANTED,
    device_id="10884521123456",
    serial_number="SN123456789",
    location="Memorial Hospital OR-3",
    operator="Dr. Johnson",
    metadata={
        'patient_id': 'PT-987654',  # PHI - must be secured
        'procedure_code': 'CPT-33206',
        'surgeon': 'Dr. Johnson'
    }
)

# Get device history
history = traceability.trace_device_history("SN123456789")
print("Device History:")
print(history[['timestamp', 'event_type', 'location', 'operator']])
```

---

## Consignment Inventory Management

### Consignment Optimization Model

**Consignment Characteristics:**
- Vendor owns inventory until use
- Located at customer site (hospital)
- Hospital pays only when consumed
- Vendor responsible for replenishment
- Common for high-value implants

```python
import numpy as np
import pandas as pd

class ConsignmentInventoryManager:
    """
    Manage consignment inventory for medical devices
    """

    def __init__(self, location_name, par_level_policy=None):
        self.location_name = location_name
        self.inventory = {}  # {serial_number: device_info}
        self.par_levels = par_level_policy or {}
        self.usage_history = []

    def add_device(self, device_id, serial_number, cost, vendor, metadata=None):
        """Add device to consignment inventory"""

        self.inventory[serial_number] = {
            'device_id': device_id,
            'serial_number': serial_number,
            'cost': cost,
            'vendor': vendor,
            'status': 'available',
            'received_date': datetime.now(),
            'metadata': metadata or {}
        }

    def consume_device(self, serial_number, patient_id, procedure_info):
        """
        Record device consumption (trigger payment to vendor)
        """

        if serial_number not in self.inventory:
            raise ValueError(f"Device {serial_number} not in consignment inventory")

        device = self.inventory[serial_number]

        if device['status'] != 'available':
            raise ValueError(f"Device {serial_number} is not available (status: {device['status']})")

        # Record usage
        usage_record = {
            'serial_number': serial_number,
            'device_id': device['device_id'],
            'vendor': device['vendor'],
            'cost': device['cost'],
            'consumption_date': datetime.now(),
            'patient_id': patient_id,
            'procedure_info': procedure_info,
            'days_in_consignment': (datetime.now() - device['received_date']).days
        }

        self.usage_history.append(usage_record)

        # Update device status
        device['status'] = 'consumed'
        device['consumption_date'] = datetime.now()

        return usage_record

    def check_par_levels(self):
        """
        Check if consignment inventory meets PAR levels
        Trigger vendor replenishment if needed
        """

        replenishment_needed = []

        for device_id, par_level in self.par_levels.items():
            # Count available devices
            available_count = sum(
                1 for device in self.inventory.values()
                if device['device_id'] == device_id and device['status'] == 'available'
            )

            if available_count < par_level:
                shortage = par_level - available_count

                replenishment_needed.append({
                    'device_id': device_id,
                    'current_qty': available_count,
                    'par_level': par_level,
                    'replenishment_qty': shortage
                })

        return replenishment_needed

    def vendor_reconciliation_report(self, vendor, month):
        """
        Generate monthly reconciliation report for vendor billing
        """

        usage_df = pd.DataFrame(self.usage_history)

        if len(usage_df) == 0:
            return pd.DataFrame()

        # Filter by vendor and month
        vendor_usage = usage_df[
            (usage_df['vendor'] == vendor) &
            (usage_df['consumption_date'].dt.to_period('M') == month)
        ]

        # Aggregate
        summary = vendor_usage.groupby('device_id').agg({
            'serial_number': 'count',
            'cost': 'sum'
        }).rename(columns={'serial_number': 'quantity', 'cost': 'total_cost'})

        summary['average_cost'] = summary['total_cost'] / summary['quantity']

        return summary

    def aging_report(self):
        """
        Report devices sitting in consignment for extended periods
        (potential obsolescence risk)
        """

        aging_data = []

        for serial, device in self.inventory.items():
            if device['status'] == 'available':
                days_on_hand = (datetime.now() - device['received_date']).days

                aging_data.append({
                    'serial_number': serial,
                    'device_id': device['device_id'],
                    'vendor': device['vendor'],
                    'cost': device['cost'],
                    'days_on_hand': days_on_hand,
                    'risk_level': self._aging_risk(days_on_hand)
                })

        aging_df = pd.DataFrame(aging_data)

        if len(aging_df) > 0:
            aging_df = aging_df.sort_values('days_on_hand', ascending=False)

        return aging_df

    @staticmethod
    def _aging_risk(days):
        """Categorize aging risk"""
        if days > 365:
            return 'Critical'
        elif days > 180:
            return 'High'
        elif days > 90:
            return 'Medium'
        else:
            return 'Low'

# Example usage
consignment = ConsignmentInventoryManager(
    location_name="Memorial Hospital",
    par_level_policy={
        'Hip-Implant-A': 5,
        'Knee-Implant-B': 8,
        'Cardiac-Stent-C': 10
    }
)

# Add devices to consignment
for i in range(5):
    consignment.add_device(
        device_id='Hip-Implant-A',
        serial_number=f'HIP-SN-{1000+i}',
        cost=3500,
        vendor='Orthopedic Devices Inc',
        metadata={'lot': 'LOT-2024-A'}
    )

# Consume a device
usage = consignment.consume_device(
    serial_number='HIP-SN-1000',
    patient_id='PT-123456',
    procedure_info={'procedure': 'Total Hip Arthroplasty', 'surgeon': 'Dr. Smith'}
)

print(f"Device consumed: {usage['serial_number']}")
print(f"Cost: ${usage['cost']:,.2f}")

# Check PAR levels
replenishment = consignment.check_par_levels()
if replenishment:
    print("\nReplenishment needed:")
    for item in replenishment:
        print(f"  {item['device_id']}: Need {item['replenishment_qty']} units")
```

---

## Loaner Set Management

### Surgical Loaner Set Tracking

**Loaner Sets:**
- Trays of specialized instruments
- Loaned by manufacturer for specific procedures
- Must be returned after use
- High value ($50K - $500K per set)
- Tracking critical to avoid loss charges

```python
from datetime import datetime, timedelta

class LoanerSetManager:
    """
    Track loaner instrument sets for surgeries
    """

    def __init__(self):
        self.loaner_sets = {}
        self.bookings = []
        self.movements = []

    def register_loaner_set(self, set_id, vendor, description, value, contents):
        """
        Register a loaner set in the system
        """

        self.loaner_sets[set_id] = {
            'set_id': set_id,
            'vendor': vendor,
            'description': description,
            'value': value,
            'contents': contents,
            'status': 'available',
            'location': 'Vendor',
            'registered_date': datetime.now()
        }

    def book_loaner_set(self, set_id, procedure_date, surgeon, procedure_type, patient_id):
        """
        Book loaner set for upcoming surgery
        """

        if set_id not in self.loaner_sets:
            raise ValueError(f"Loaner set {set_id} not registered")

        booking = {
            'booking_id': f"BOOK-{len(self.bookings)+1}",
            'set_id': set_id,
            'procedure_date': procedure_date,
            'surgeon': surgeon,
            'procedure_type': procedure_type,
            'patient_id': patient_id,
            'booking_date': datetime.now(),
            'status': 'booked'
        }

        self.bookings.append(booking)

        # Update set status
        self.loaner_sets[set_id]['status'] = 'booked'

        return booking

    def receive_loaner_set(self, set_id, received_by, condition='good'):
        """
        Record receipt of loaner set at hospital
        """

        if set_id not in self.loaner_sets:
            raise ValueError(f"Loaner set {set_id} not registered")

        movement = {
            'set_id': set_id,
            'event_type': 'received',
            'timestamp': datetime.now(),
            'location': 'Hospital Central Sterile',
            'operator': received_by,
            'condition': condition
        }

        self.movements.append(movement)

        # Update set status and location
        self.loaner_sets[set_id]['status'] = 'in_house'
        self.loaner_sets[set_id]['location'] = 'Hospital Central Sterile'
        self.loaner_sets[set_id]['received_date'] = datetime.now()

    def send_to_sterile_processing(self, set_id, processor):
        """
        Send loaner set for sterilization
        """

        movement = {
            'set_id': set_id,
            'event_type': 'sent_to_sterilization',
            'timestamp': datetime.now(),
            'location': 'Sterile Processing',
            'operator': processor
        }

        self.movements.append(movement)

        self.loaner_sets[set_id]['location'] = 'Sterile Processing'
        self.loaner_sets[set_id]['status'] = 'processing'

    def ready_for_surgery(self, set_id, sterilization_lot):
        """
        Mark loaner set as sterile and ready
        """

        movement = {
            'set_id': set_id,
            'event_type': 'sterilization_complete',
            'timestamp': datetime.now(),
            'location': 'Sterile Storage',
            'sterilization_lot': sterilization_lot
        }

        self.movements.append(movement)

        self.loaner_sets[set_id]['location'] = 'Sterile Storage'
        self.loaner_sets[set_id]['status'] = 'ready'

    def use_in_surgery(self, set_id, procedure_info):
        """
        Record use in surgery
        """

        movement = {
            'set_id': set_id,
            'event_type': 'used_in_surgery',
            'timestamp': datetime.now(),
            'location': f"OR-{procedure_info.get('or_room', 'Unknown')}",
            'procedure_info': procedure_info
        }

        self.movements.append(movement)

        self.loaner_sets[set_id]['status'] = 'used'
        self.loaner_sets[set_id]['last_used_date'] = datetime.now()

    def return_to_vendor(self, set_id, carrier, tracking_number):
        """
        Ship loaner set back to vendor
        """

        movement = {
            'set_id': set_id,
            'event_type': 'returned_to_vendor',
            'timestamp': datetime.now(),
            'location': 'In Transit to Vendor',
            'carrier': carrier,
            'tracking_number': tracking_number
        }

        self.movements.append(movement)

        self.loaner_sets[set_id]['status'] = 'returned'
        self.loaner_sets[set_id]['location'] = 'In Transit to Vendor'
        self.loaner_sets[set_id]['return_date'] = datetime.now()

    def overdue_loaners_report(self, days_threshold=14):
        """
        Identify loaner sets held beyond expected return date
        """

        overdue = []

        for set_id, loaner in self.loaner_sets.items():
            if loaner['status'] in ['available', 'returned']:
                continue

            if 'received_date' in loaner:
                days_on_hand = (datetime.now() - loaner['received_date']).days

                if days_on_hand > days_threshold:
                    overdue.append({
                        'set_id': set_id,
                        'vendor': loaner['vendor'],
                        'description': loaner['description'],
                        'value': loaner['value'],
                        'days_on_hand': days_on_hand,
                        'status': loaner['status'],
                        'location': loaner['location']
                    })

        return pd.DataFrame(overdue)

    def loaner_utilization_report(self):
        """
        Analyze loaner set utilization and costs
        """

        utilization_data = []

        for set_id, loaner in self.loaner_sets.items():
            # Count uses
            uses = [m for m in self.movements if m['set_id'] == set_id and m['event_type'] == 'used_in_surgery']

            # Calculate average time on-site
            received_events = [m for m in self.movements if m['set_id'] == set_id and m['event_type'] == 'received']
            returned_events = [m for m in self.movements if m['set_id'] == set_id and m['event_type'] == 'returned_to_vendor']

            cycles = min(len(received_events), len(returned_events))
            if cycles > 0:
                avg_days_on_site = sum([
                    (returned_events[i]['timestamp'] - received_events[i]['timestamp']).days
                    for i in range(cycles)
                ]) / cycles
            else:
                avg_days_on_site = 0

            utilization_data.append({
                'set_id': set_id,
                'vendor': loaner['vendor'],
                'description': loaner['description'],
                'value': loaner['value'],
                'times_used': len(uses),
                'avg_days_on_site': round(avg_days_on_site, 1),
                'cycles': cycles
            })

        return pd.DataFrame(utilization_data)

# Example usage
loaner_mgr = LoanerSetManager()

# Register loaner sets
loaner_mgr.register_loaner_set(
    set_id='LOANER-SPINE-001',
    vendor='Spinal Devices Corp',
    description='Lumbar Fusion Instrument Set',
    value=125000,
    contents=['Pedicle Screws', 'Rods', 'Insertion Tools', 'Measurement Guides']
)

# Book for surgery
booking = loaner_mgr.book_loaner_set(
    set_id='LOANER-SPINE-001',
    procedure_date=datetime.now() + timedelta(days=7),
    surgeon='Dr. Williams',
    procedure_type='Lumbar Fusion L4-L5',
    patient_id='PT-789012'
)

# Track through process
loaner_mgr.receive_loaner_set('LOANER-SPINE-001', received_by='Materials Clerk')
loaner_mgr.send_to_sterile_processing('LOANER-SPINE-001', processor='SPD Tech A')
loaner_mgr.ready_for_surgery('LOANER-SPINE-001', sterilization_lot='STER-20240215-001')
loaner_mgr.use_in_surgery('LOANER-SPINE-001', {'or_room': '5', 'surgeon': 'Dr. Williams'})
loaner_mgr.return_to_vendor('LOANER-SPINE-001', carrier='FedEx', tracking_number='TRACK123456')

print("Loaner set lifecycle completed")
```

---

## Recall Management

### Medical Device Recall Process

**FDA Recall Classifications:**
- **Class I**: Reasonable probability of serious adverse health consequences or death
- **Class II**: Temporary or medically reversible adverse health consequences
- **Class III**: Not likely to cause adverse health consequences

```python
class RecallManager:
    """
    Manage medical device recalls
    """

    def __init__(self, traceability_system):
        self.traceability_system = traceability_system
        self.recalls = []

    def initiate_recall(self, recall_id, device_id, lot_numbers, reason,
                        recall_class, recall_date, corrective_action):
        """
        Initiate a device recall
        """

        recall = {
            'recall_id': recall_id,
            'device_id': device_id,
            'lot_numbers': lot_numbers,
            'reason': reason,
            'recall_class': recall_class,  # I, II, or III
            'recall_date': recall_date,
            'corrective_action': corrective_action,
            'status': 'active'
        }

        self.recalls.append(recall)

        return recall

    def identify_affected_devices(self, recall_id):
        """
        Identify all devices affected by recall using traceability
        """

        recall = next((r for r in self.recalls if r['recall_id'] == recall_id), None)

        if not recall:
            raise ValueError(f"Recall {recall_id} not found")

        affected_devices = []

        for lot_number in recall['lot_numbers']:
            # Find devices from affected lots
            serial_numbers = self.traceability_system.find_devices_by_lot(lot_number)

            for serial in serial_numbers:
                device_history = self.traceability_system.trace_device_history(serial)

                # Get current location/status
                latest_event = device_history.iloc[-1] if len(device_history) > 0 else None

                affected_devices.append({
                    'serial_number': serial,
                    'lot_number': lot_number,
                    'current_location': latest_event['location'] if latest_event is not None else 'Unknown',
                    'status': latest_event['event_type'] if latest_event is not None else 'Unknown',
                    'last_event_date': latest_event['timestamp'] if latest_event is not None else None
                })

        return pd.DataFrame(affected_devices)

    def identify_implanted_devices(self, recall_id):
        """
        Identify devices from recall that have been implanted (most critical)
        """

        affected = self.identify_affected_devices(recall_id)

        # Filter to implanted devices
        implanted = affected[affected['status'] == 'implanted']

        return implanted

    def customer_notification_list(self, recall_id):
        """
        Generate list of customers to notify about recall
        """

        affected = self.identify_affected_devices(recall_id)

        # Group by current location (customer)
        customers = affected.groupby('current_location').agg({
            'serial_number': 'count',
            'status': lambda x: ', '.join(x.unique())
        }).rename(columns={'serial_number': 'affected_devices'})

        return customers

    def recall_effectiveness_check(self, recall_id):
        """
        Track recall effectiveness (how many devices recovered)
        """

        affected = self.identify_affected_devices(recall_id)
        total_affected = len(affected)

        # Devices that have been returned/recovered
        recovered = affected[affected['status'] == 'returned']
        recovered_count = len(recovered)

        # Devices still implanted
        implanted = affected[affected['status'] == 'implanted']
        implanted_count = len(implanted)

        # Devices unaccounted for
        unaccounted = affected[~affected['status'].isin(['returned', 'implanted'])]
        unaccounted_count = len(unaccounted)

        effectiveness = {
            'recall_id': recall_id,
            'total_affected': total_affected,
            'recovered': recovered_count,
            'recovery_rate': (recovered_count / total_affected * 100) if total_affected > 0 else 0,
            'still_implanted': implanted_count,
            'unaccounted': unaccounted_count
        }

        return effectiveness

# Example usage
# Assuming traceability system from earlier example
recall_mgr = RecallManager(traceability)

# Initiate recall
recall = recall_mgr.initiate_recall(
    recall_id='RECALL-2024-001',
    device_id='10884521123456',
    lot_numbers=['LOT2024A', 'LOT2024B'],
    reason='Potential battery malfunction',
    recall_class='I',  # Class I - serious
    recall_date=datetime.now(),
    corrective_action='Return device to manufacturer for inspection and replacement'
)

print(f"Recall initiated: {recall['recall_id']}")
print(f"Class: {recall['recall_class']}")
print(f"Affected lots: {', '.join(recall['lot_numbers'])}")

# Identify affected devices
affected = recall_mgr.identify_affected_devices('RECALL-2024-001')
print(f"\nTotal affected devices: {len(affected)}")

# Identify implanted (most critical)
implanted = recall_mgr.identify_implanted_devices('RECALL-2024-001')
print(f"Implanted devices requiring patient notification: {len(implanted)}")

# Customer notification list
customers = recall_mgr.customer_notification_list('RECALL-2024-001')
print("\nCustomers to notify:")
print(customers)
```

---

## Cold Chain & Temperature Control

### Temperature-Controlled Distribution

**Requirements:**
- Certain biologics and tissue-based devices
- Maintain temperature range throughout distribution
- Continuous monitoring
- Excursion documentation

```python
import numpy as np

class ColdChainMonitor:
    """
    Monitor temperature-controlled shipments
    """

    def __init__(self, shipment_id, product_id, temp_range):
        self.shipment_id = shipment_id
        self.product_id = product_id
        self.min_temp, self.max_temp = temp_range
        self.temperature_log = []
        self.excursions = []

    def record_temperature(self, timestamp, temperature, location, recorder):
        """
        Record temperature reading
        """

        reading = {
            'timestamp': timestamp,
            'temperature': temperature,
            'location': location,
            'recorder': recorder,
            'in_range': self.min_temp <= temperature <= self.max_temp
        }

        self.temperature_log.append(reading)

        # Check for excursion
        if not reading['in_range']:
            excursion = {
                'excursion_start': timestamp,
                'temperature': temperature,
                'location': location,
                'severity': self._calculate_severity(temperature)
            }
            self.excursions.append(excursion)

        return reading

    def _calculate_severity(self, temperature):
        """
        Determine excursion severity
        """

        if temperature < self.min_temp:
            deviation = self.min_temp - temperature
        else:
            deviation = temperature - self.max_temp

        if deviation <= 2:
            return 'Minor'
        elif deviation <= 5:
            return 'Moderate'
        else:
            return 'Major'

    def compliance_report(self):
        """
        Generate temperature compliance report
        """

        if not self.temperature_log:
            return None

        df = pd.DataFrame(self.temperature_log)

        total_readings = len(df)
        compliant_readings = df['in_range'].sum()
        compliance_rate = (compliant_readings / total_readings * 100) if total_readings > 0 else 0

        report = {
            'shipment_id': self.shipment_id,
            'product_id': self.product_id,
            'required_range': f"{self.min_temp}°F - {self.max_temp}°F",
            'total_readings': total_readings,
            'compliant_readings': compliant_readings,
            'compliance_rate': round(compliance_rate, 2),
            'num_excursions': len(self.excursions),
            'min_temp_recorded': df['temperature'].min(),
            'max_temp_recorded': df['temperature'].max(),
            'avg_temp': round(df['temperature'].mean(), 2)
        }

        return report

    def excursion_summary(self):
        """
        Summarize temperature excursions
        """

        if not self.excursions:
            return pd.DataFrame()

        return pd.DataFrame(self.excursions)

# Example usage
cold_chain = ColdChainMonitor(
    shipment_id='SHIP-2024-001',
    product_id='Tissue-Graft-A',
    temp_range=(36, 46)  # 36-46°F required
)

# Simulate temperature readings
np.random.seed(42)
base_temp = 40
for hour in range(48):
    temp = base_temp + np.random.normal(0, 2)

    # Simulate excursion at hour 24
    if hour == 24:
        temp = 50  # Excursion

    cold_chain.record_temperature(
        timestamp=datetime.now() + timedelta(hours=hour),
        temperature=round(temp, 1),
        location='In Transit',
        recorder='Data Logger SN12345'
    )

# Generate reports
compliance = cold_chain.compliance_report()
print("Cold Chain Compliance:")
print(f"  Compliance Rate: {compliance['compliance_rate']}%")
print(f"  Excursions: {compliance['num_excursions']}")
print(f"  Temp Range: {compliance['min_temp_recorded']}°F - {compliance['max_temp_recorded']}°F")

if compliance['num_excursions'] > 0:
    excursions = cold_chain.excursion_summary()
    print("\nTemperature Excursions:")
    print(excursions)
```

---

## Distribution Performance Metrics

### Key Performance Indicators (KPIs)

```python
def calculate_distribution_kpis(shipment_data_df, inventory_data_df, recall_data_df=None):
    """
    Calculate medical device distribution KPIs

    Parameters:
    - shipment_data_df: Shipment transactions
    - inventory_data_df: Inventory positions
    - recall_data_df: Recall events (optional)
    """

    kpis = {}

    # On-Time Delivery Rate
    if 'on_time' in shipment_data_df.columns:
        kpis['otd_rate'] = (shipment_data_df['on_time'].sum() / len(shipment_data_df) * 100)

    # Perfect Order Rate (on-time, complete, damage-free, correct documentation)
    if all(col in shipment_data_df.columns for col in ['on_time', 'complete', 'damage_free', 'docs_correct']):
        perfect_orders = shipment_data_df[
            shipment_data_df['on_time'] &
            shipment_data_df['complete'] &
            shipment_data_df['damage_free'] &
            shipment_data_df['docs_correct']
        ]
        kpis['perfect_order_rate'] = (len(perfect_orders) / len(shipment_data_df) * 100)

    # Inventory Accuracy
    if 'physical_count' in inventory_data_df.columns and 'system_count' in inventory_data_df.columns:
        accurate_items = inventory_data_df[
            inventory_data_df['physical_count'] == inventory_data_df['system_count']
        ]
        kpis['inventory_accuracy'] = (len(accurate_items) / len(inventory_data_df) * 100)

    # UDI Compliance Rate
    if 'udi_compliant' in inventory_data_df.columns:
        kpis['udi_compliance_rate'] = (inventory_data_df['udi_compliant'].sum() / len(inventory_data_df) * 100)

    # Average Recall Response Time
    if recall_data_df is not None and not recall_data_df.empty:
        if 'response_hours' in recall_data_df.columns:
            kpis['avg_recall_response_hours'] = recall_data_df['response_hours'].mean()

    # Traceability Completeness
    if 'traceability_complete' in shipment_data_df.columns:
        kpis['traceability_completeness'] = (
            shipment_data_df['traceability_complete'].sum() / len(shipment_data_df) * 100
        )

    # Cold Chain Compliance (if applicable)
    if 'temp_compliant' in shipment_data_df.columns:
        cold_chain_shipments = shipment_data_df[shipment_data_df['requires_cold_chain'] == True]
        if len(cold_chain_shipments) > 0:
            kpis['cold_chain_compliance'] = (
                cold_chain_shipments['temp_compliant'].sum() / len(cold_chain_shipments) * 100
            )

    # Format KPIs
    for key in kpis:
        if 'rate' in key or 'compliance' in key or 'accuracy' in key or 'completeness' in key:
            kpis[key] = round(kpis[key], 2)
        else:
            kpis[key] = round(kpis[key], 2)

    return kpis

# Example usage
shipment_data = pd.DataFrame({
    'shipment_id': range(1, 101),
    'on_time': np.random.choice([True, False], 100, p=[0.95, 0.05]),
    'complete': np.random.choice([True, False], 100, p=[0.98, 0.02]),
    'damage_free': np.random.choice([True, False], 100, p=[0.99, 0.01]),
    'docs_correct': np.random.choice([True, False], 100, p=[0.97, 0.03]),
    'traceability_complete': np.random.choice([True, False], 100, p=[0.99, 0.01]),
    'requires_cold_chain': np.random.choice([True, False], 100, p=[0.15, 0.85]),
    'temp_compliant': np.random.choice([True, False], 100, p=[0.98, 0.02])
})

inventory_data = pd.DataFrame({
    'item_id': range(1, 501),
    'physical_count': np.random.randint(0, 100, 500),
    'system_count': np.random.randint(0, 100, 500),
    'udi_compliant': np.random.choice([True, False], 500, p=[0.95, 0.05])
})

# Make some matching for accuracy
inventory_data.loc[0:450, 'physical_count'] = inventory_data.loc[0:450, 'system_count']

kpis = calculate_distribution_kpis(shipment_data, inventory_data)

print("Medical Device Distribution KPIs:")
for metric, value in kpis.items():
    print(f"  {metric}: {value}{'%' if 'rate' in metric or 'compliance' in metric else ''}")
```

---

## Tools & Libraries

### Medical Device Software Systems

**ERP/QMS Systems:**
- **TrackWise**: Quality management and compliance
- **MasterControl**: Document control and quality management
- **Veeva Vault**: Regulated content management
- **SAP for Medical Devices**: ERP with device-specific functionality
- **Oracle Agile PLM**: Product lifecycle management

**Traceability & Serialization:**
- **TraceLink**: Network-based track and trace
- **Systech UniSecure**: Serialization and traceability
- **Optel Vision**: End-to-end traceability
- **Antares Vision**: Track and trace solutions
- **rfxcel**: Supply chain traceability platform

**Consignment & Loaner Management:**
- **iMDsoft**: Implant and consignment management
- **Attainia**: Healthcare supply chain management
- **SmartTray**: Loaner asset tracking
- **Surgical Information Systems (SIS)**: OR asset tracking

**Cold Chain Monitoring:**
- **Sensitech**: Temperature monitoring solutions
- **Emerson Cargo Solutions**: Cold chain visibility
- **Tive**: Real-time tracking with sensors
- **Controlant**: Temperature monitoring platform

### Python Libraries

**Serialization & Barcoding:**
- `python-barcode`: Barcode generation
- `qrcode`: QR code generation
- `pylibdmtx`: Data Matrix barcode reading
- `pyzbar`: Barcode/QR code reading

**Data Analysis:**
- `pandas`: Data manipulation
- `numpy`: Numerical operations
- `scipy`: Statistical analysis
- `matplotlib`, `seaborn`: Visualization

**Database & Tracking:**
- `sqlalchemy`: Database ORM
- `pymongo`: MongoDB interface
- `redis-py`: Redis for caching
- `flask`/`fastapi`: API development

---

## Common Challenges & Solutions

### Challenge: UDI Compliance Implementation

**Problem:**
- Complex labeling requirements
- Multiple standards (GS1, HIBCC, ICCBBA)
- Integration with existing systems
- Historical data gaps

**Solutions:**
- Phase implementation by device class
- Implement GS1 standard (most common)
- Automated label generation systems
- Retrofit historical data where possible
- Partner with labeling vendors
- Train staff on scanning requirements
- Regular compliance audits

### Challenge: Implanted Device Traceability

**Problem:**
- Requires integration with hospital EMR
- Surgical documentation gaps
- PHI security concerns
- Real-time data capture difficult

**Solutions:**
- OR integration systems for auto-capture
- Barcode scanning at point of use
- EMR integration via HL7/FHIR
- Secure, HIPAA-compliant systems
- Simplified capture process for surgeons
- Dedicated data entry staff as backup
- Regular reconciliation audits

### Challenge: Consignment Inventory Optimization

**Problem:**
- Overstocked consignment locations
- Difficult to balance availability vs. cost
- Aging inventory risk
- Vendor relationship management

**Solutions:**
- Data-driven PAR level optimization
- Regular usage analysis by location
- Vendor scorecard for fill rates
- Transfer slow-moving stock between sites
- Demand forecasting for procedures
- Contract terms for aging inventory
- VMI (vendor-managed inventory) programs

### Challenge: Loaner Set Tracking & Returns

**Problem:**
- Lost or delayed returns
- Large financial liability
- Manual tracking processes
- Sterilization delays

**Solutions:**
- Automated loaner tracking system
- RFID tagging of loaner sets
- Alerts for overdue returns
- Dedicated loaner coordinator role
- Carrier contracts for returns
- Streamlined sterilization process
- Vendor penalties for late pickups

### Challenge: Recall Execution Speed

**Problem:**
- Difficult to locate all affected devices
- Incomplete traceability data
- Customer notification delays
- Regulatory reporting requirements

**Solutions:**
- Robust traceability system from start
- Automated recall identification
- Pre-built customer notification templates
- Recall team training and drills
- Integration with FDA recall system
- Regular traceability audits
- Mock recalls for preparedness

### Challenge: Cold Chain Compliance

**Problem:**
- Temperature excursions during transport
- Data logger failures
- Seasonal weather variations
- International shipments

**Solutions:**
- Validated packaging systems
- Redundant temperature monitoring
- Real-time alerts for excursions
- Seasonal shipping plans (avoid extreme weather)
- Qualified carriers and lanes
- Backup shipping options
- Excursion investigation protocols

---

## Output Format

### Medical Device Distribution Report

**Executive Summary:**
- Distribution network overview
- Key compliance metrics
- Performance vs. targets
- Critical issues requiring attention

**UDI & Traceability Compliance:**

| Device Category | Class | UDI Compliance | Traceability Completeness | Gap Analysis |
|----------------|-------|----------------|---------------------------|--------------|
| Cardiac Implants | III | 100% | 98% | 2% missing surgery data |
| Orthopedic Implants | III | 100% | 95% | 5% EMR integration gaps |
| Infusion Pumps | II | 98% | 100% | 2% legacy products |
| Surgical Instruments | I | 85% | N/A | 15% pending label updates |

**Consignment Inventory Summary:**

| Hospital | Device Category | On-Hand Qty | On-Hand Value | Monthly Usage | Turns | Aging >180 Days |
|----------|----------------|-------------|---------------|---------------|-------|-----------------|
| Memorial Hospital | Cardiac Stents | 45 | $67,500 | 8 | 2.1 | 3 units |
| Regional Medical | Hip Implants | 62 | $217,000 | 15 | 2.9 | 0 units |
| University Hospital | Spine Sets | 38 | $133,000 | 6 | 1.9 | 8 units |

**Active Recalls:**

| Recall ID | Device | Class | Affected Lots | Total Devices | Implanted | Recovered | Recovery Rate |
|-----------|--------|-------|---------------|---------------|-----------|-----------|---------------|
| REC-2024-001 | Pacemaker Model X | I | LOT-A, LOT-B | 247 | 89 | 158 | 64% |
| REC-2024-003 | IV Pump Series 3 | II | LOT-2024-C | 1,205 | 0 | 1,089 | 90% |

**Distribution Performance Metrics:**

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| On-Time Delivery | 96.2% | 95% | ✓ |
| Perfect Order Rate | 92.8% | 95% | ⚠ |
| Inventory Accuracy | 99.1% | 98% | ✓ |
| UDI Compliance | 97.5% | 100% | ⚠ |
| Traceability Completeness | 98.3% | 99% | ⚠ |
| Cold Chain Compliance | 99.8% | 99% | ✓ |
| Recall Response Time | 6.2 hrs | < 8 hrs | ✓ |

**Action Items:**
1. Complete UDI labeling for remaining 2.5% of Class I/II devices
2. Improve EMR integration to close traceability gaps
3. Accelerate recovery efforts for Class I recall REC-2024-001
4. Reduce consignment aging inventory at University Hospital
5. Address perfect order rate gap (documentation accuracy)

---

## Questions to Ask

If you need more context:

1. What device classes are you distributing? (I, II, III)
2. What's the current state of UDI compliance?
3. Do you have a traceability system in place?
4. What percentage of business is consignment vs. purchase?
5. How many active recalls do you manage annually?
6. Are you distributing temperature-sensitive products?
7. What's your current inventory accuracy rate?
8. Do you distribute internationally?
9. What QMS system is in use?
10. What are the biggest compliance concerns or gaps?

---

## Related Skills

- **hospital-logistics**: Hospital internal supply chain management
- **pharmacy-supply-chain**: Pharmaceutical distribution and logistics
- **clinical-trial-logistics**: Clinical trial supply chain management
- **compliance-management**: Regulatory compliance and quality systems
- **track-and-trace**: Product tracking and serialization
- **quality-management**: Quality management systems
- **inventory-optimization**: Inventory optimization techniques
- **warehouse-design**: Distribution center design
- **risk-mitigation**: Supply chain risk management
