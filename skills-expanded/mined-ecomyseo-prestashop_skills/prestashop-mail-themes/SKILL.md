---
name: prestashop-mail-themes
description: Skill for creating and extending modern email themes in PrestaShop 8 and 9.
---

# PrestaShop Mail Themes Skill

This skill explains how to use the modern mail engine (introduced in PS 1.7.7) to create custom email designs and apply transformations.

## 1. Technical Guide

### Registering a Mail Theme
Register your module to the `actionListMailThemes` hook.

```php
public function hookActionListMailThemes(array $params)
{
    /** @var \PrestaShop\PrestaShop\Core\MailTemplate\ThemeCollectionInterface $themes */
    $themes = $params['mailThemes'];
    
    // Scan your module directory for a theme
    $scanner = new \PrestaShop\PrestaShop\Core\MailTemplate\FolderThemeScanner();
    $myTheme = $scanner->scan(_PS_MODULE_DIR_ . $this->name . '/mails/themes/my_custom_theme');
    
    if (null !== $myTheme) {
        $themes->add($myTheme);
    }
}
```

### Adding or Extending Layouts
You can replace core layouts or add new ones.

```php
public function extendLayout(\PrestaShop\PrestaShop\Core\MailTemplate\ThemeCollectionInterface $themes)
{
    foreach ($themes as $theme) {
        if ($theme->getName() !== 'modern') continue;
        
        $orderConf = $theme->getLayouts()->getLayout('order_conf', ''); // '' means core layout
        if ($orderConf) {
            $index = $theme->getLayouts()->indexOf($orderConf);
            $theme->getLayouts()->offsetSet($index, new \PrestaShop\PrestaShop\Core\MailTemplate\Layout\Layout(
                'order_conf',
                '@Modules/mymodule/mails/layouts/extended_order_conf.html.twig',
                ''
            ));
        }
    }
}
```

### Mail Transformations
Apply transformations (like changing colors or adding footers) via `actionGetMailLayoutTransformations`.

```php
public function hookActionGetMailLayoutTransformations(array $params)
{
    $transformations = $params['layoutTransformations'];
    $transformations->add(new MyColorTransformation('#FF0000'));
}
```

## 2. Professional Development Guide

### Folder Structure
- `mails/themes/[theme_name]/`: Contains the theme files.
- `mails/layouts/`: Contains Twig layouts for emails.
- `mails/subjects/`: Subject translations.

### Layout Variables
Use `actionBuildMailLayoutVariables` to add custom variables to email templates.

```php
public function hookActionBuildMailLayoutVariables(array $params)
{
    $params['mailLayoutVariables']['my_custom_var'] = 'Dynamic Value';
}
```

## 3. User Guide

### How to access
1. Install the module.
2. Go to **Design > Mail Theme**.
3. Select your new theme in the "Choose your mail theme" dropdown and click "Generate emails".

## Rules & Best Practices
- **Twig only**: The modern system uses Twig for design and generates HTML/TXT files.
- **Compatibility**: Ensure fallback to core themes if your module is disabled.
- **Licensing**: Always include the Ecom Experts / AFL-3.0 header.
