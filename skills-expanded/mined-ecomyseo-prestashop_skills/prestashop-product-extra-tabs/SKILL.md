
# PrestaShop Module Development: The "Direct Injection" Pattern (Foolproof Product Tabs)

## Description
This is the **DEFINITIVE, BATTLE-TESTED** method for adding extra tabs and content to PrestaShop 8+ product forms.
It bypasses Symfony's complex data mapping and retrieval mechanisms (Provider/Handler) in favor of **Direct Data Injection** and **Raw $_POST Retrieval**.
This method solves:
- Data saving failure (empty fields).
- Data display failure (empty editors).
- Multi-language indexing confusion (ID vs ISO).
- TinyMCE initialization issues.

## Core Principles (The "Anti-Magic" Rules)
1.  **Direct Read (Display)**: Fetch data via SQL inside the Form Builder and inject it directly into the form's `data` option. Do NOT use `hookActionProductFormDataProviderData`.
2.  **Direct Write (Save)**: Read `$_POST` raw data inside the Save Hook. Do NOT trust Symfony's `$params['form_data']`.
3.  **Double Indexing**: When preparing data arrays, index by **BOTH** ISO Code (`es`, `en`) AND Language ID (`1`, `2`). This covers all variations of `TranslateType` expectations.
4.  **SQL Persistence**: Use `REPLACE INTO` for atomic saving.

## The Implementation

### 1. Database Structure
Standard table with composite key.
```sql
CREATE TABLE IF NOT EXISTS `_DB_PREFIX_my_module_table` (
    `id_product` int(11) UNSIGNED NOT NULL,
    `id_shop` int(11) UNSIGNED NOT NULL,
    `id_lang` int(11) UNSIGNED NOT NULL,
    `extra_content` TEXT,
    PRIMARY KEY (`id_product`, `id_shop`, `id_lang`)
) ENGINE=_MYSQL_ENGINE_ DEFAULT CHARSET=utf8mb4;
```

### 2. Form Builder (Display Logic) - The "Direct Injection"
**Hook**: `hookActionProductFormBuilderModifier`
**Crucial**: Fetch SQL data HERE and pass it to `create()` via `'data' => ...`.

```php
public function hookActionProductFormBuilderModifier(array $params)
{
    $idProduct = (int)$params['id'];
    $formBuilder = $params['form_builder'];
    $idShop = (int)Context::getContext()->shop->id;
    $languages = Language::getLanguages(true);

    // 1. FETCH DATA DIRECTLY
    $sql = 'SELECT * FROM `' . _DB_PREFIX_ . 'my_module_table` 
            WHERE `id_product` = ' . $idProduct . ' 
            AND `id_shop` = ' . $idShop;
    $results = Db::getInstance()->executeS($sql);

    // 2. PREPARE ARRAY (Double Indexing Strategy)
    $content = [];
    foreach ($languages as $lang) {
        $content[$lang['iso_code']] = '';
        $content[$lang['id_lang']] = ''; // Initial empty for ID too
    }

    if ($results) {
        foreach ($results as $row) {
            foreach ($languages as $lang) {
                if ((int)$lang['id_lang'] === (int)$row['id_lang']) {
                    // Populate BOTH keys to be 100% sure
                    $content[$lang['iso_code']] = $row['extra_content'];
                    $content[$lang['id_lang']] = $row['extra_content'];
                    break; 
                }
            }
        }
    }

    // 3. INJECT DATA DIRECTLY INTO FORM
    $initialData = [
        'extra_content' => $content
    ];

    $extraTab = $formBuilder->create('my_module_tab', FormType::class, [
        'label' => $this->trans('My Tab', [], 'Modules.Mymodule.Admin'),
        'inherit_data' => false,
        'mapped' => false, 
        'required' => false,
        'data' => $initialData, // <--- CRITICAL: Direct Injection
    ]);

    $extraTab->add('extra_content', TranslateType::class, [
        'type' => FormattedTextareaType::class, // Standard TinyMCE
        'label' => $this->trans('Content (HTML)', [], 'Modules.Mymodule.Admin'),
        'locales' => $languages,
        'required' => false,
        // Do NOT add 'hideLabels' => false (it crashes)
        // Do NOT add 'attr' => ['class' => 'autoload_rte'] manually (it duplicates)
    ]);

    $formBuilder->add($extraTab);
}
```

### 3. Data Provider (Disable it)
DO NOT USE IT. Leave it empty to prevent conflicts if registered.
```php
public function hookActionProductFormDataProviderData(array $params)
{
    // RETIRED: Logic moved to FormBuilderModifier for reliability.
}
```

### 4. Save Logic (Write Logic) - The "Raw POST"
**Hook**: `hookActionAfterUpdateProductFormHandler`
**Crucial**: Read `$_POST` directly to bypass Symfony filtering/mapping issues.

```php
public function hookActionAfterUpdateProductFormHandler(array $params)
{
    $this->saveData($params);
}

private function saveData(array $params)
{
    // 1. RAW POST RETRIEVAL
    // Structure typically: product[my_module_tab][extra_content][1]
    $moduleData = null;
    if (isset($_POST['product']['my_module_tab'])) {
        $moduleData = $_POST['product']['my_module_tab'];
    }

    // debug log is recommended here
    
    if (!$moduleData) {
        return; 
    }

    $idProduct = (int)$params['id'];
    $idShop = (int)Context::getContext()->shop->id;
    $languages = Language::getLanguages(true);

    foreach ($languages as $lang) {
        $idLang = (int)$lang['id_lang'];
        $iso = $lang['iso_code'];
        
        // 2. RETRIEVE CONTENT (Check ID first, then ISO)
        $content = '';
        if (isset($moduleData['extra_content'][$idLang])) {
            $content = $moduleData['extra_content'][$idLang];
        } elseif (isset($moduleData['extra_content'][$iso])) {
            $content = $moduleData['extra_content'][$iso];
        }

        // 3. DIRECT SQL SAVE
        Db::getInstance()->execute('
            REPLACE INTO `' . _DB_PREFIX_ . 'my_module_table` 
            (`id_product`, `id_shop`, `id_lang`, `extra_content`)
            VALUES (' . $idProduct . ', ' . $idShop . ', ' . $idLang . ', "' . pSQL($content, true) . '")
        ');
    }
}
```

## Summary Checklist
- [ ] Table uses `id_product`, `id_shop`, `id_lang`.
- [ ] `FormBuilder`: Reads SQL and passes `'data' => $array` in `create()`.
- [ ] `FormBuilder`: `initialData` array has double keys (ISO + ID) for each language.
- [ ] `DataProvider`: Empty.
- [ ] `SaveHandler`: Reads `$_POST['product']['tab_name']`.
- [ ] `SaveHandler`: Uses `REPLACE INTO`.

## 🎨 Front-Office Persistence (AJAX)
**DANGER**: Even if your Admin Tab saves perfectly, your Front-Office JS will **DIE** when the user changes a product combination (color, size) because PrestaShop replaces the DOM via AJAX.

**OBLIGATORIO**: Always include this re-initializer in your Front JS:
```javascript
if (typeof prestashop !== 'undefined') {
    prestashop.on('updateProduct', function (event) {
        initMyModuleFrontLogic(); // Re-run your event binders
    });
}
```

**SI NO CUMPLES ESTE PROTOCOLO, CUALQUIER "FIX" SE CONSIDERA FALLIDO.**
