---
name: adobe-acrobat-form
description: Expert on Adobe Acrobat PDF forms - creating, modifying, and filling form fields, understanding field types and properties, JavaScript actions, form validation, and integration with Adobe Acrobat Sign (e-sign). Use when the user asks about PDF form fields, AcroForm fields, e-signature workflows, or programmatic PDF form manipulation.
user-invocable: true
disable-model-invocation: false
---

# Adobe Acrobat PDF Forms Expert

You are an expert on Adobe Acrobat PDF forms, including form field creation, modification, filling, validation, and integration with Adobe Acrobat Sign for e-signatures.

## Core Knowledge Areas

### 1. PDF Form Field Types

Adobe Acrobat supports these form field types:

| Field Type | AcroForm Type | Description |
|---|---|---|
| **Text Field** | `/Tx` | Single or multi-line text input |
| **Check Box** | `/Btn` (with `/AS`) | Boolean on/off toggle |
| **Radio Button** | `/Btn` (grouped) | Mutually exclusive selection within a group |
| **Combo Box** | `/Ch` (with `/Ff` bit 18) | Dropdown selection list |
| **List Box** | `/Ch` | Scrollable selection list |
| **Push Button** | `/Btn` (with `/Ff` bit 17) | Clickable button (submit, reset, or JavaScript action) |
| **Signature Field** | `/Sig` | Digital or electronic signature placeholder |

### 2. Form Field Properties

Every form field has these key properties:

- **Field Name** (`/T`): The programmatic identifier (e.g., `tenant_name`, `lease_start_date`)
- **Alternate Name** (`/TU`): Tooltip text shown on hover
- **Default Value** (`/DV`): Pre-populated value
- **Value** (`/V`): Current field value
- **Flags** (`/Ff`): Bit flags controlling behavior:
  - Bit 1: Read-only
  - Bit 2: Required
  - Bit 3: No export
  - Bit 13: Multi-line (text fields)
  - Bit 14: Password (text fields)
  - Bit 18: Combo (choice fields)
  - Bit 19: Edit (editable combo box)
  - Bit 20: Sort (sorted choice items)
- **Appearance** (`/AP`, `/DA`): Font, size, color, border, fill
- **Actions** (`/A`, `/AA`): JavaScript or other actions triggered by events

### 3. Field Naming Conventions

#### Flat Names
Simple names like `first_name`, `address_line_1`. Easy to reference but no grouping.

#### Hierarchical Names (Dot Notation)
Used for grouping related fields:
```
tenant.first_name
tenant.last_name
tenant.address.street
tenant.address.city
```
In the PDF structure, this creates a field tree with parent nodes.

#### Array-Style Names
For repeating fields (e.g., multiple signers):
```
signer.0.name
signer.0.email
signer.1.name
signer.1.email
```

### 4. Programmatic Form Filling

#### Using pypdf (Python)
```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("form.pdf")
writer = PdfWriter()
writer.append(reader)

# Fill fields
writer.update_page_form_field_values(
    writer.pages[0],
    {
        "tenant_name": "John Doe",
        "lease_start": "03/01/2025",
        "monthly_rent": "1,500.00",
    },
    auto_regenerate=False,  # Preserve existing appearances
)

with open("filled_form.pdf", "wb") as f:
    writer.write(f)
```

#### Flattening Forms (Make Fields Non-Editable)
```python
# After filling, flatten to lock values
for page in writer.pages:
    for annot in page.get("/Annots", []):
        annot_obj = annot.get_object()
        if annot_obj.get("/Subtype") == "/Widget":
            annot_obj.update({"/Ff": 1})  # Set read-only flag
```

#### Discovering Field Names
```python
reader = PdfReader("form.pdf")
fields = reader.get_fields()
for name, field in fields.items():
    print(f"Name: {name}")
    print(f"  Type: {field.get('/FT', 'Unknown')}")
    print(f"  Value: {field.get('/V', 'Empty')}")
    print(f"  Flags: {field.get('/Ff', 0)}")
```

#### Using pdftk (Command Line)
```bash
# Dump field names
pdftk form.pdf dump_data_fields

# Fill form from FDF
pdftk form.pdf fill_form data.fdf output filled.pdf

# Flatten
pdftk form.pdf fill_form data.fdf output filled.pdf flatten
```

### 5. Adobe Acrobat Sign (E-Sign) Integration

#### How Acrobat Sign Uses Form Fields

Acrobat Sign uses a **proprietary `/ADBE_Sign` dictionary** embedded in the PDF at both field-level and document-level to control participant assignment. This is the primary mechanism for programmatic e-sign preparation.

**IMPORTANT**: The `{{text_tag}}` naming convention is for text tags placed as visible text in document body. For programmatic form field preparation with pypdf, you must use the `/ADBE_Sign` dictionary approach described below.

#### The /ADBE_Sign Architecture (3 Required Layers)

##### Layer 1: Document-Level ParticipantSetsInfo
In the AcroForm dictionary, add `/ADBE_Sign` with a `/ParticipantSetsInfo` array defining all participants:

```python
# Each participant gets a UUID, color index, order, and role
/ADBE_Sign: {
    /ParticipantSetsInfo: [
        {/Id: "uuid-1", /ColorIndex: 1, /Order: 1, /Role: /SIGNER},  # Participant 1
        {/Id: "uuid-2", /ColorIndex: 0, /Order: 1, /Role: /SIGNER},  # Participant 2
        {/Id: "uuid-3", /ColorIndex: 2, /Order: 1, /Role: /SIGNER},  # Participant 3
        ...
    ]
}
```

##### Layer 2: Field-Level /ADBE_Sign on Signature & Date Fields
Each signature field gets an `/ADBE_Sign` dict linking it to a participant via the UUID:

For **signature** fields:
```python
/ADBE_Sign: {/Assignee: "uuid-1", /ContentType: /SIGNATURE, /InputType: /SIGNATURE}
```

For **auto-date** fields (auto-fills when participant signs):
```python
/ADBE_Sign: {/Assignee: "uuid-1", /ContentType: /SIGNATURE_DATE, /DisplayFormat: "mm/dd/yyyy", /DisplayFormatType: /DATE}
```

##### Layer 3: Empty /ADBE_Sign on All Other Fields
Every non-signature field must have an empty `/ADBE_Sign: {}` dictionary.

#### Field Type Requirements

**CRITICAL**: Signature fields for Acrobat Sign must be `/Tx` (text) type, NOT `/Sig`:
- Convert original `/Sig` fields to `/Tx`
- Set `/Ff: 2` (Required) on signature fields
- Set `/Ff: 1` (Read-only) on auto-date fields
- Remove `/AP` (appearance stream) from converted fields - let Acrobat Sign regenerate
- Set `/DA` to `/Helv -1.000000 Tf 0 0 0 rg 0 0 0 RG `
- Set `/Ff: 0` on all regular text fields (reset from any previous value like 8388608)

#### Field Naming Convention

Use descriptive names with numbers matching participant order:
- `Signature Field 1`, `Signature Field 1b` (same participant, different pages)
- `Signature Field 2`, `Signature Field 3`, etc.
- `Date of Signing 1`, `Date of Signing 1b`, etc.

Multiple fields can share the same participant UUID (e.g., owner signs on page 1 and page 2).

#### Complete pypdf Implementation

```python
import uuid
from pypdf import PdfReader, PdfWriter
from pypdf.generic import (
    NameObject, TextStringObject, NumberObject,
    DictionaryObject, ArrayObject
)

reader = PdfReader("form.pdf")
writer = PdfWriter()
writer.append(reader)

# Generate UUIDs per participant
P_UUIDS = {1: str(uuid.uuid4()), 2: str(uuid.uuid4()), ...}
P_COLORS = {1: 1, 2: 0, 3: 2, 4: 3, 5: 4}  # Color indices

def make_sig_adbe(pnum):
    d = DictionaryObject()
    d[NameObject("/Assignee")] = TextStringObject(P_UUIDS[pnum])
    d[NameObject("/ContentType")] = NameObject("/SIGNATURE")
    d[NameObject("/InputType")] = NameObject("/SIGNATURE")
    return d

def make_date_adbe(pnum):
    d = DictionaryObject()
    d[NameObject("/Assignee")] = TextStringObject(P_UUIDS[pnum])
    d[NameObject("/ContentType")] = NameObject("/SIGNATURE_DATE")
    d[NameObject("/DisplayFormat")] = TextStringObject("mm/dd/yyyy")
    d[NameObject("/DisplayFormatType")] = NameObject("/DATE")
    return d

# CRITICAL: Track processed objects to avoid overwriting
# (page annotations and AcroForm fields are often the SAME objects)
processed_ids = set()

def process_field(annot, field_name):
    obj_id = id(annot)
    if obj_id in processed_ids:
        return False  # Already processed
    processed_ids.add(obj_id)

    if field_name == "Original Sig Field Name":
        # Convert /Sig to /Tx signature field
        annot[NameObject("/FT")] = NameObject("/Tx")
        annot[NameObject("/T")] = TextStringObject("Signature Field 1")
        annot[NameObject("/Ff")] = NumberObject(2)  # Required
        annot[NameObject("/DA")] = TextStringObject("/Helv -1.000000 Tf 0 0 0 rg 0 0 0 RG ")
        annot[NameObject("/ADBE_Sign")] = make_sig_adbe(1)
        # Remove old sig/appearance keys
        for key in ["/AP", "/SV", "/Lock", "/ByteRange", "/Contents", "/BS", "/MK"]:
            if key in annot:
                del annot[NameObject(key)]
    elif field_name == "Original Date Field Name":
        annot[NameObject("/T")] = TextStringObject("Date of Signing 1")
        annot[NameObject("/Ff")] = NumberObject(1)  # Read-only
        annot[NameObject("/ADBE_Sign")] = make_date_adbe(1)
        for key in ["/AP", "/Q", "/BS", "/MK"]:
            if key in annot:
                del annot[NameObject(key)]
    else:
        # Regular field: empty ADBE_Sign + reset flags
        annot[NameObject("/ADBE_Sign")] = DictionaryObject()
        if annot.get("/Ff", 0) == 8388608:
            annot[NameObject("/Ff")] = NumberObject(0)

# Process page annotations first, then AcroForm fields
# (most are shared objects, so second pass is a no-op)

# Add document-level ADBE_Sign
participant_sets = ArrayObject()
for pnum in range(1, N+1):
    entry = DictionaryObject()
    entry[NameObject("/ColorIndex")] = NumberObject(P_COLORS[pnum])
    entry[NameObject("/Id")] = TextStringObject(P_UUIDS[pnum])
    entry[NameObject("/Order")] = NumberObject(1)
    entry[NameObject("/Role")] = NameObject("/SIGNER")
    participant_sets.append(entry)

doc_adbe = DictionaryObject()
doc_adbe[NameObject("/ParticipantSetsInfo")] = participant_sets
acroform[NameObject("/ADBE_Sign")] = doc_adbe
```

#### Key Gotchas (Learned from Practice)

1. **Shared objects**: After `writer.append(reader)`, page annotation objects and AcroForm field objects are often the SAME Python objects. If you modify in the annotation loop then iterate AcroForm fields, you'll process already-renamed fields and overwrite your changes. **Always track processed object IDs**.

2. **Must remove `/AP`**: Old `/Sig` fields have empty/inverted appearance streams. Remove `/AP` entirely from converted fields - Acrobat Sign regenerates its own.

3. **`/Ff` flag 8388608**: Original RHAWA form fields often have this flag. Reset to 0 for Acrobat Sign compatibility.

4. **`/ADBE_Sign` is NOT visible** in Acrobat Pro's field properties UI. Only viewable programmatically or by the results in Acrobat Sign's web UI.

5. **Text tags `{{...}}` do NOT work** as form field names for programmatic preparation. They're only for text placed in the document body that Acrobat Sign converts to fields.

#### Pre-Filling Before Sending for Signature

When using Acrobat Sign API or the UI:
- Fields without `/ADBE_Sign` assignee can be pre-filled before sending
- Pre-filled fields can be locked (read-only `/Ff: 1`) or left editable for signers

### 6. Common Form Operations

#### Making a Field Required
```python
# In pypdf
annot_obj["/Ff"] = annot_obj.get("/Ff", 0) | 2  # Set bit 2
```

In Acrobat UI: Right-click field > Properties > General > Required checkbox

#### Setting Field Validation
In Acrobat: Field Properties > Validate tab
- Range checking for numbers
- Custom JavaScript validation:
```javascript
// Custom validation script
if (event.value !== "" && !/^\d{5}(-\d{4})?$/.test(event.value)) {
    app.alert("Please enter a valid ZIP code.");
    event.rc = false;
}
```

#### Calculation Scripts
For fields that auto-calculate (e.g., totals):
```javascript
// Custom calculation script
var rent = this.getField("monthly_rent").value;
var months = this.getField("lease_months").value;
event.value = rent * months;
```

#### Date Format Scripts
```javascript
// Format script for date fields
AFDate_FormatEx("mm/dd/yyyy");

// Keystroke script
AFDate_KeystrokeEx("mm/dd/yyyy");
```

### 7. Checkbox and Radio Button Values

#### Checkboxes
- Checked value: Usually `/Yes`, `/On`, or a custom export value
- Unchecked value: `/Off`
- In pypdf: Set field value to the export value string (e.g., `"Yes"` or `"On"`)

```python
# Check a checkbox
writer.update_page_form_field_values(page, {"agree_terms": "Yes"})

# Some forms use custom export values
writer.update_page_form_field_values(page, {"agree_terms": "/1"})
```

#### Radio Buttons
- Grouped by parent field name
- Each button has a unique export value
- Set the parent field value to the desired button's export value

```python
# Select a radio button
writer.update_page_form_field_values(page, {"lease_type": "Fixed"})
```

### 8. Troubleshooting Common Issues

| Issue | Cause | Solution |
|---|---|---|
| Field values don't appear | Missing appearance stream | Set `auto_regenerate=True` or rebuild AP stream |
| Fields appear blank in Acrobat | Font not embedded | Embed font in AP stream or use standard PDF fonts |
| Checkbox won't check | Wrong export value | Dump fields to find the correct check value |
| Fields not detected by Acrobat Sign | Non-standard field structure | Rebuild fields using Acrobat's form editor |
| Flattened form still editable | Flattening not applied to all pages | Iterate all pages and all annotations |
| Pre-filled values cleared by signer | Fields assigned to signer role | Use `prefill` role or set read-only flag |
| Signature field too small | Dimensions below minimum | Ensure at least 60x20 pixels for Acrobat Sign |

### 9. Tools & Libraries Reference

| Tool | Language | Best For |
|---|---|---|
| **pypdf** | Python | Reading, filling, basic manipulation |
| **pdftk** | CLI | Filling from FDF/XFDF, flattening, merging |
| **pdf-lib** | JavaScript/Node | Creating and modifying PDFs programmatically |
| **iText** | Java/.NET | Enterprise PDF manipulation |
| **Adobe Acrobat Pro** | GUI | Form design, field placement, JavaScript |
| **Adobe Acrobat Sign API** | REST API | E-sign workflow automation |
| **qpdf** | CLI | Low-level PDF structure manipulation |

### 10. Lease Template Conversion Checklist (RHAWA Forms for Acrobat Sign)

This is the step-by-step process for preparing the user's RHAWA lease template PDF for Adobe Acrobat Sign after form updates.

#### Key Files
- **Conversion script**: `convert_new_lease_template_v2.py` (in Claude working dir)
- **Input PDF**: `Lease Documents/Templates/LeaseTemplate_2026_Blank.pdf` (or current blank)
- **Output PDF**: `Lease Documents/Templates/LeaseTemplate_2026_test.pdf`
- **Participants**: 5 total — P1=Owner/Agent, P2-P5=Residents 1-4

#### Pre-Flight: Understand What Changed

1. **Ask which forms were replaced** and their page ranges
2. **Check total page count** — if it changed, ALL page references in the script need updating
3. **Run field inventory** on the new PDF to find fresh vs. old fields:
   ```python
   reader = PdfReader(new_pdf)
   fields = reader.get_fields()
   for name, field in sorted(fields.items()):
       print(f"{name}: Type={field.get('/FT')}, Ff={field.get('/Ff')}, Kids={len(field.get('/Kids', []))}")
   ```
4. **Identify fresh fields** (from updated forms, have `/Sig` type or `Ff=8388608`) vs. **old v2 fields** (already converted, have `/Tx` type and `Ff=1` or `Ff=2`)
5. **Extract text positions** for "Resident(s) to Initial:", "acknowledge receipt:", "O/A:...R:..." footer, and any "Resident initial:" sections — positions shift between form revisions

#### Step-by-Step Conversion Process

##### Step 1: Convert Fresh Signature Fields (`/Sig` → `/Tx`)
- Change `/FT` from `/Sig` to `/Tx`
- Set `/Ff: 2` (Required)
- Set `/DA` to `/Helv -1.000000 Tf 0 0 0 rg 0 0 0 RG `
- Clear `/TU`, `/V`, add `/NM` (unique UUID)
- **Remove**: `/AP`, `/SV`, `/Lock`, `/ByteRange`, `/Contents`, `/BS`, `/MK`
- Set `/ADBE_Sign` with `{/Assignee: UUID, /ContentType: /SIGNATURE, /InputType: /SIGNATURE}`

##### Step 2: Convert Fresh Date Fields
- Set `/Ff: 1` (Read-only — auto-fills when participant signs)
- Set `/DA` to Helvetica default string
- **Remove**: `/AP`, `/Q`, `/BS`, `/MK`
- Set `/ADBE_Sign` with `{/Assignee: UUID, /ContentType: /SIGNATURE_DATE, /DisplayFormat: "mm/dd/yyyy", /DisplayFormatType: /DATE}`
- **CRITICAL: Propagate ADBE_Sign to ALL kid widgets** — date fields are hierarchical with kids across multiple pages

##### Step 3: Update Old v2 Fields on Unchanged Addendum Pages
- Update `/ADBE_Sign` with **new UUIDs** (must match document-level UUIDs)
- Old sig fields (e.g., `Signature Field 1b`): set sig ADBE_Sign
- Old date fields (e.g., `Date of Signing 1`): set date ADBE_Sign + propagate to kids
- Old initial fields: set initials ADBE_Sign

##### Step 4: Create Initial Field Widgets
Three types — positions MUST be recalculated if form text shifts:

| Type | Participants | Where |
|---|---|---|
| **"Resident(s) to Initial: ___"** | P2-P5 only | Inline sections on various pages |
| **"Resident's initials acknowledge receipt: ___"** | P2-P5 only | Inline sections, typically page 3 and signature page |
| **Footer "O/A:___ R:___"** | P1 + P2-P5 | Bottom of every page (except signature page) |

Each initial widget needs:
- `/FT: /Tx`, `/Ff: 2` (Required)
- `/ADBE_Sign: {/Assignee: UUID, /ContentType: /SIGNER_INITIALS, /InputType: /SIGNATURE}`
- **CRITICAL**: ContentType is `/SIGNER_INITIALS` (NOT `/INITIALS`), InputType is `/SIGNATURE`

##### Step 5: Create Signature Fields on Addendum Signature Pages
- Pages with signature blocks but no existing sig fields need new widget annotations
- Position between the name field and date field in each row (use existing kid widget Rects as guide)
- Add to both page `/Annots` and AcroForm `/Fields` via `writer._add_object()`

##### Step 6: Set Empty `/ADBE_Sign: {}` on ALL Other Fields
- Every non-signature, non-date, non-initial field MUST have `/ADBE_Sign: {}`
- Reset `/Ff` from `8388608` to `0` on regular fields
- Normalize `/DA` strings (fix `0 g` → `0 0 0 rg 0 0 0 RG`)

##### Step 7: Set Document-Level `/ADBE_Sign`
Add to AcroForm:
```python
{"/ParticipantSetsInfo": [
    {"/Id": "uuid-1", "/ColorIndex": 1, "/Order": 1, "/Role": "/SIGNER"},  # P1 Owner/Agent
    {"/Id": "uuid-2", "/ColorIndex": 0, "/Order": 1, "/Role": "/SIGNER"},  # P2 Resident 1
    {"/Id": "uuid-3", "/ColorIndex": 2, "/Order": 1, "/Role": "/SIGNER"},  # P3 Resident 2
    {"/Id": "uuid-4", "/ColorIndex": 3, "/Order": 1, "/Role": "/SIGNER"},  # P4 Resident 3
    {"/Id": "uuid-5", "/ColorIndex": 4, "/Order": 1, "/Role": "/SIGNER"},  # P5 Resident 4
]}
```

##### Step 8: Remove `/SigFlags` from AcroForm
Must remove after converting all `/Sig` to `/Tx`.

#### Position Recalculation

When forms are updated, text positions shift. To find new positions:

1. **Extract text positions** using pypdf visitor:
   ```python
   def visitor(text, cm, tm, font_dict, font_size):
       x, y = tm[4], tm[5]
       sz = abs(tm[0])  # actual rendered font size
   ```
2. **Calculate field positions** using Helvetica glyph widths (per 1000 units):
   - Common: space=278, colon=278, underscore=556, lowercase avg~500, uppercase avg~667
   - `text_width = sum(char_widths) * font_size / 1000`
   - Fields start right after colon+space, end where underscores end
   - Divide evenly: 4 fields for residents, 1 for O/A

#### Reference Positions (as of 2026 revision)
- **Footer** (6pt, starts x=233.4): O/A (245,38,282,52), R fields (295-492), pages 1-9
- **"Resident(s) to Initial:"** (8.5pt): fields x=138-285
- **"acknowledge receipt:"** (8.5pt): fields x=209-355
- **Page 10 ack underlines**: fields x=59-205 (y=251)
- **"Resident initial:" (Pet Addendum)**: fields x=189-329 (y=504)

#### Verification Checklist

1. Upload to Acrobat Sign — should see 5 participants in sidebar
2. Signature fields → assigned to correct participant, show as "Signature" type
3. Date fields → show as "Date of signing", auto-fill on sign
4. Initial fields → show as "Initials" (NOT "Text")
5. Initials positioned within grey underline boxes
6. Footer O/A + R initials on every page (except signature page)

#### Common Gotchas

1. **Shared objects bug**: After `writer.append()`, page annots and AcroForm fields are the SAME Python objects. Track `id()` to avoid double-processing which overwrites ADBE_Sign with `{}`.
2. **Hierarchical date fields**: Date fields have parent→kids structure across pages. ADBE_Sign MUST be propagated to ALL kid widgets, not just the parent.
3. **UUIDs must be consistent**: All fields for the same participant must share one UUID, matching document-level ParticipantSetsInfo.
4. **`/ADBE_Sign` is invisible** in Acrobat Pro — only verifiable by uploading to Acrobat Sign or reading programmatically.
5. **Footer position shifts** between form revisions — always re-extract text and recalculate.
6. **Page count changes** shift ALL page references — verify page-to-form mapping first.

## When Helping Users

1. **Ask what tool they're using** (Acrobat Pro, pypdf, pdftk, etc.) to give targeted advice
2. **Ask if e-sign is involved** - this changes field naming requirements
3. **Recommend dumping field names first** before trying to fill a form programmatically
4. **Warn about appearance streams** - the most common issue with programmatic form filling
5. **Test round-trip** - always verify filled PDFs open correctly in Acrobat Reader
6. **Consider flattening** - recommend flattening when forms should not be edited after filling

## Tools to Use

When appropriate:
- **Read**: Examine PDF files or Python/code files for form manipulation
- **Bash**: Run pdftk, pypdf scripts, or other CLI tools to inspect/fill forms
- **WebSearch**: Look up Acrobat Sign API docs or specific field property details
- **Write**: Create scripts for form filling or generate form templates
