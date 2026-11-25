---
name: prestashop-multistore-form
description: Skill for creating multi-store compatible configuration forms in PrestaShop 8 and 9 using Symfony components.
---

# PrestaShop Multi-store Form Skill

This skill explains how to build configuration forms that correctly handle PrestaShop's Multi-store (Multishop) feature, allowing settings to be defined per shop, per group, or globally.

## 1. Technical Guide

### The Multi-store Data Configuration
Instead of `DataConfigurationInterface`, use `AbstractMultistoreConfiguration`.

```php
final class MyModuleMultistoreConfig extends AbstractMultistoreConfiguration
{
    public function getConfiguration(): array
    {
        $shopConstraint = $this->getShopConstraint();
        return [
            'my_setting' => $this->configuration->get('MY_SETTING_KEY', null, $shopConstraint),
        ];
    }

    public function updateConfiguration(array $config): array
    {
        $shopConstraint = $this->getShopConstraint();
        // This helper handles the "Use default value" checkboxes automatically
        $this->updateConfigurationValue('MY_SETTING_KEY', 'my_setting', $config, $shopConstraint);
        
        return [];
    }
}
```

### Form Type with Multi-store Headers
To display the "Multi-store configuration" header (the one with the checkboxes to override values), your form needs to be aware of it.

```php
final class MySettingType extends TranslatorAwareType
{
    public function buildForm(FormBuilderInterface $builder, array $options)
    {
        $builder->add('my_setting', TextType::class, [
            'label' => $this->trans('Setting', 'Modules.Mymodule.Admin'),
            'multistore_configuration_key' => 'MY_SETTING_KEY', // Links to the multishop override system
        ]);
    }
}
```

## 2. Professional Development Guide

### Shop Constraint
The `ShopConstraint` object encapsulates the current context (Single Shop, Group of Shops, or All Shops). `AbstractMultistoreConfiguration` provides this via `$this->getShopConstraint()`.

### Service Registration
```yaml
services:
    my_module.multistore_config:
        class: MyModule\Form\MyModuleMultistoreConfig
        arguments:
            - '@prestashop.adapter.legacy.configuration'
            - '@prestashop.adapter.shop.context'
```

## 3. User Guide

### How to use
When Multi-store is enabled:
1. The user selects a shop from the header drop-down.
2. The form loads values specifically for that shop.
3. Checkboxes appear next to fields allowing the user to "Use default value" (inherited from Group or All Shops) or override it.

## Rules & Best Practices
- **Persistence**: Never use `Configuration::get()` without the $id_shop parameter if the setting is shop-dependent.
- **UI consistency**: Always use the built-in form types that support the `multistore_configuration_key` option.
- **Defaults**: Ensure you have sensible global defaults for when a shop hasn't overridden a value yet.
