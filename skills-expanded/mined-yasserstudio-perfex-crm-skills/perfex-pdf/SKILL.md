---
name: perfex-pdf
description: Use whenever the user is customizing, overriding, or debugging PDF output in Perfex CRM — invoice PDFs, estimate PDFs, proposal PDFs, payment receipts, contract PDFs, statement PDFs, credit note PDFs, the `my_` prefix override convention, TCPDF library usage, `App_items_table` customization, font configuration (freesans, dejavusans, droidsansfallback), PDF merge fields, logo/heading settings, or e-invoice JSON/XML export (3.4.0+). Also trigger when the user says "my PDF is blank", "Arabic text broken in PDF", "custom logo not showing in invoice PDF", "how to add a field to the invoice PDF", "PDF font wrong", "override invoicepdf.php", "items table column in PDF", or "e-invoice XML format".
license: MIT
metadata:
  author: yasserstudio
  version: "1.5.0"
---

# Perfex PDF Customization

You are a Perfex CRM PDF engineer. Your job is to customize PDF templates — invoice, estimate, proposal, contract, payment, statement, credit note — using TCPDF correctly, the `my_` prefix override convention, proper font selection for multi-language support, and the `App_items_table` class for line-item formatting.

Perfex generates PDFs via the TCPDF library. Templates live in `application/views/themes/perfex/views/` and are plain PHP files that call TCPDF methods on a `$pdf` object.

## Template file locations

| Document | Core file | Override file |
|---|---|---|
| Invoice | `invoicepdf.php` | `my_invoicepdf.php` |
| Estimate | `estimatepdf.php` | `my_estimatepdf.php` |
| Proposal | `proposalpdf.php` | `my_proposalpdf.php` |
| Payment receipt | `paymentpdf.php` | `my_paymentpdf.php` |
| Contract | `contractpdf.php` | `my_contractpdf.php` |
| Statement | `statementpdf.php` | `my_statementpdf.php` |
| Credit note | `credit_note_pdf.php` | `my_credit_note_pdf.php` |

All located in: `application/views/themes/perfex/views/`

## The `my_` prefix override convention

To customize a PDF without touching core files:

1. Copy the core template (e.g., `invoicepdf.php`)
2. Rename with `my_` prefix: `my_invoicepdf.php`
3. Place in the same directory: `application/views/themes/perfex/views/`
4. Edit the `my_` version

Perfex checks for the `my_` prefixed version first. This survives core updates — the only risk is if Perfex makes "huge changes" to the template structure in a major release.

This is not PDF-specific: `App_Loader` applies the `my_` lookup to **every** core view (`my_invoicehtml.php`, `my_dashboard.php`…), and to module views when the module calls `add_module_support($module, 'my_prefixed_view_files')`. See `perfex-theme` and `perfex-module-dev`.

## TCPDF basics

Templates receive a `$pdf` object (TCPDF instance). Common methods:

```php
// Set font
$pdf->SetFont('freesans', '', 10);

// Add content
$pdf->writeHTML($html, true, false, true, false, '');

// Add a new page
$pdf->AddPage();

// Set margins
$pdf->SetMargins(15, 15, 15);

// Cell (x, y positioned text)
$pdf->Cell(0, 10, 'Text here', 0, 1, 'L');

// Multi-cell (wrapping text)
$pdf->MultiCell(0, 10, $long_text, 0, 'L');

// Image
$pdf->Image($logo_path, 15, 15, 40);
```

Full TCPDF docs: https://tcpdf.org/docs/srcdoc/TCPDF/class-TCPDF/

## Font selection

| Language/Script | Font | Notes |
|---|---|---|
| Latin, Cyrillic | `freesans` | Default, UTF-8 support |
| Arabic | `dejavusans` | Also: `aealarabiya`, `aefurat` |
| Japanese, Chinese | `droidsansfallback` | CJK characters |

Configure default font at **Setup → Settings → PDF**.

```php
// In your my_invoicepdf.php — force Arabic font
$pdf->SetFont('dejavusans', '', 10);
```

If the PDF shows boxes or blank chars, the font doesn't cover the character set. Switch to the appropriate font above. The Setup → Settings → PDF dropdown is built by `get_pdf_fonts_list()`, which scans TCPDF's own font directory — only fonts that exist there are selectable.

### Custom / brand fonts — register before `setFont()`, and only what you use

Two traps, both from production:

1. **TCPDF's font directory is inside `application/vendor/`, which a Perfex upgrade replaces.** A font you drop in there disappears on the next update and every PDF dies with `Could not include font definition file`. Keep custom fonts under your theme/module and register them with a full path: `$pdf->AddFont('brandsans', '', FCPATH . 'assets/themes/my_theme/fonts/brandsans.php')`.
2. **The `pdf_construct` hook fires *after* the default `setFont()`.** `App_pdf::__construct()` calls `setFont(get_option('pdf_font'))` first, then `do_action('pdf_construct', ['pdf_instance' => $pdf, 'type' => $type])`. So if the *default* PDF font is a custom one, registering it in `pdf_construct` is too late — the constructor has already fataled. `pdf_construct` is fine for fonts a template switches to later; for a custom default font, either extend `App_pdf` or keep the default a stock font and `SetFont()` your brand font at the top of `my_invoicepdf.php`.

Register only the family a document actually draws with. TCPDF embeds every registered font whether or not it's used — registering a whole brand family put ~90 KB of unused weights on every invoice.

### PDF lifecycle hooks

| Hook | Fires | Payload |
|---|---|---|
| `pdf_construct` | after default font/margins set | `['pdf_instance' => App_pdf, 'type' => 'invoice'…]` |
| `pdf_header` | inside `Header()` | same |
| `pdf_footer` | inside `Footer()` | same |
| `pdf_close` | before output | same |
| `<type>_pdf_build_path` (filter) | when building the file path for attachments | path string |

All actions receive one array — no `accepted_args` needed.

## Adding custom data to a PDF template

Inside `my_invoicepdf.php`, you have access to the full invoice object. To add a custom field:

```php
// Read a custom field value
$passport = get_custom_field_value($invoice->id, 'invoice_passport_number', 'invoice');

// Or query directly
$CI =& get_instance();
$CI->db->select('v.value');
$CI->db->from(db_prefix() . 'customfieldsvalues v');
$CI->db->join(db_prefix() . 'customfields f', 'f.id = v.fieldid');
$CI->db->where('v.relid', $invoice->clientid);
$CI->db->where('f.slug', 'mymodule_tax_id');
$row = $CI->db->get()->row();
$tax_id = $row ? $row->value : '';

// Render it
$pdf->SetFont('freesans', 'B', 9);
$pdf->Cell(0, 5, 'Tax ID: ' . $tax_id, 0, 1, 'L');
```

## Items table customization (`App_items_table`)

The line-items table (qty, description, rate, tax, amount) is rendered by `application/libraries/App_items_table.php`, which extends the abstract `App_items_table_template`. It handles **both** HTML preview and PDF output; `$for` is `'html'` or `'pdf'`.

There is **no column-config filter** (no `items_table_columns`). The supported extension point is the `items_table_class` filter: return your own subclass and override the three abstract methods — `items()`, `html_headings()`, `pdf_headings()`.

```php
// modules/my_module/libraries/My_items_table.php
class My_items_table extends App_items_table
{
    public function pdf_headings()
    {
        // Return the <tr> of <th> cells for the PDF. Copy the parent
        // implementation and add/remove columns; widths are percentages.
        return parent::pdf_headings();
    }

    public function items()
    {
        // Build each <tr>. $this->items holds the rows; $this->type is
        // 'invoice' | 'estimate' | 'proposal' | 'credit_note'; $this->for is 'html' | 'pdf'.
        return parent::items();
    }
}

// modules/my_module/my_module.php
hooks()->add_filter('items_table_class', function ($class, $transaction, $type, $for, $admin_preview) {
    if ($type !== 'invoice') {
        return $class;                       // leave estimates/proposals alone
    }
    include_once module_libs_path('my_module') . 'My_items_table.php';
    return new My_items_table($transaction, $type, $for, $admin_preview);
}, 10, 5);
```

`get_items_table_data()` in `sales_helper.php` runs this filter and `show_error()`s if what you return isn't an `App_items_table_template`. Smaller tweaks have their own filters: `item_description_td_width` (default `38`, percent), `item_tax_table_row`, `show_tax_per_item`, `items_table_amounts_exclude_currency_symbol`.

Don't copy `App_items_table.php` over the core file — it's overwritten on update and the filter exists precisely so you don't have to.

## PDF heading text

Headings are language strings. Override in `application/language/english/custom_lang.php`:

```php
$lang['invoice_pdf_heading']     = 'TAX INVOICE';
$lang['estimate_pdf_heading']    = 'QUOTATION';
$lang['proposal_pdf_heading']    = 'PROPOSAL';
$lang['credit_note_pdf_heading'] = 'CREDIT NOTE';
```

This respects the customer's language setting — if the customer is set to French, Perfex uses the French translation of these keys.

## Logo configuration

**Setup → Settings → PDF → Custom PDF Company Logo URL**

- If blank, Perfex uses the uploaded company logo from Settings → Company
- Set a URL for a different logo (e.g., higher resolution for print)
- Width is configurable in the same settings panel

## Paper size and orientation

Configured at **Setup → Settings → PDF → Document Formats**. Perfex defaults to A4 portrait. For US Letter or landscape, change here — don't hardcode in templates.

## E-invoice support (Perfex 3.4.0+)

Perfex 3.4.0 added e-invoice compatible output:

- JSON/XML template generators for invoices and credit notes
- Bulk export in JSON/XML formats
- View/download individual invoices as JSON/XML

This is separate from PDF generation — it uses structured data templates, not TCPDF. If you need to customize e-invoice output, look for the JSON/XML template files in the same views directory.

## Multi-language PDF output

Perfex resolves PDF language by:
1. Customer's configured language (profile setting)
2. System default language (fallback)

Admin users can force output in the customer's language via **Setup → Settings → Localization**. This affects merge field labels, headings, and date formats in the PDF.

## Common pitfalls

- **Blank PDF** — usually a PHP fatal error inside the template. Enable `ENVIRONMENT = 'development'` in `index.php` to see the error. TCPDF swallows errors silently in production mode.
- **Logo not showing** — path must be absolute filesystem path for `$pdf->Image()`, not a URL. Use `FCPATH . 'uploads/company/logo.png'`.
- **Arabic text reversed** — TCPDF needs RTL direction set: `$pdf->setRTL(true)` before writing Arabic content. Reset with `$pdf->setRTL(false)` after.
- **Custom CSS ignored** — TCPDF supports a limited subset of HTML/CSS. No flexbox, no grid, no float. Use `<table>` for layout. Inline styles only (`style=""` attributes).
- **Items table changes appear in HTML preview but not the PDF** — your `items_table_class` subclass overrode `html_headings()` but not `pdf_headings()` (or `items()` branches on `$this->for`). Both surfaces come from the same class; override both.
- **`writeHTML` renders corrupted** — HTML must be well-formed XHTML (closed tags, quoted attributes). TCPDF parser is strict. Use `htmlspecialchars()` on user data.

## Related skills

- **`perfex-customfields`** — reading custom field values to display in PDF templates.
- **`perfex-core-apis`** — `_l()` for PDF heading translations, `get_option()` for PDF settings.
- **`perfex-theme`** — client-area invoice HTML preview uses theme views; PDF uses separate templates.
- **`perfex-module-dev`** — modules can register hooks that add data to the PDF context.

## Upstream docs

- Perfex PDF customization: https://help.perfexcrm.com/pdf-customization/
- TCPDF documentation: https://tcpdf.org/docs/srcdoc/TCPDF/class-TCPDF/
- TCPDF examples: https://tcpdf.org/examples/

---

*Verified against Perfex CRM 3.4.0 core source on 2026-09-15 with `scripts/verify-against-core.sh`. Version-specific notes in the text are from official changelogs.*
