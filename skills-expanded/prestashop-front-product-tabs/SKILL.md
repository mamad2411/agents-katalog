---
name: prestashop-front-product-tabs
description: Skill for adding custom tabs and extra content to the Front Office product page in PrestaShop.
---

# PrestaShop Front Product Tabs Skill

This skill explains how to add professional tabs and sections to the product page on the front-end using the `displayProductExtraContent` hook.

## 1. Technical Guide

### Implementing the Hook
The hook must return an array of `ProductExtraContent` objects.

```php
public function hookDisplayProductExtraContent($params) 
{
    $tabs = [];
    
    $tabs[] = (new \PrestaShop\PrestaShop\Core\Product\ProductExtraContent())
        ->setTitle($this->trans('Reviews', [], 'Modules.Mymodule.Shop'))
        ->setContent($this->fetch('module:mymodule/views/templates/front/reviews.tpl'))
        ->setAttr(['id' => 'mymodule-reviews-tab', 'class' => 'my-custom-class']);

    return $tabs;
}
```

### Smarty support
You can render TPL files for the content:
```php
$content = $this->context->smarty->fetch($this->local_path.'views/templates/front/tab.tpl');
```

## 2. Professional Development Guide

### Layout Compatibility
- In the "Classic" theme and most modern themes, these objects are automatically rendered as tabs.
- Some themes might render them as accordions or simple sections; your content should be responsive.

### Performance
- Lazy-load heavy content (like maps or 3D models) inside the tab using AJAX triggered when the tab is clicked.

## 3. User Guide

### How to use
- Install the module.
- The new tabs will appear alongside "Description" and "Product Details" in the product page.
- You can manage the order of the tabs by changing the module position in **Design > Positions**.

## Rules & Best Practices
- **Translations**: Use the `Shop` domain for front-office strings.
- **Escape**: Ensure all content is properly escaped in Smarty.
- **Unique IDs**: Always set unique IDs for your tabs were possible to allow CSS/JS targeting.
