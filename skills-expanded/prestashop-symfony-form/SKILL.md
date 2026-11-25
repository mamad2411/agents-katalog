---
name: prestashop-symfony-form
description: Skill for creating custom Symfony forms and configuration pages in PrestaShop 8 and 9.
---

# PrestaShop Symfony Form Skill

This skill explains how to build modern back-office forms using Symfony Form component, integrated with PrestaShop's Configuration and Data Provider system.

## 1. Technical Guide

### The Triple-Pattern for Forms
Modern PrestaShop forms often use three classes:
1. **Type**: The form structure (fields).
2. **DataProvider**: Handles loading and saving data for the form.
3. **DataConfiguration**: Specifically for forms that save to the `ps_configuration` table.

#### Form Type (`src/Form/MyCustomType.php`)
```php
final class MyCustomType extends TranslatorAwareType
{
    public function buildForm(FormBuilderInterface $builder, array $options)
    {
        $builder
            ->add('my_setting', TextType::class, [
                'label' => $this->trans('Setting Name', 'Modules.Mymodule.Admin'),
            ]);
    }
}
```

#### Data Configuration (`src/Form/MyDataConfiguration.php`)
This class defines how fields map to `Configuration` keys.
```php
final class MyDataConfiguration implements DataConfigurationInterface
{
    private $configuration;

    public function getConfiguration()
    {
        return [
            'my_setting' => $this->configuration->get('MY_MODULE_SETTING'),
        ];
    }

    public function updateConfiguration(array $config)
    {
        $this->configuration->set('MY_MODULE_SETTING', $config['my_setting']);
        return []; // errors
    }
}
```

### Rendering the Form in a Controller
```php
public function indexAction(Request $request)
{
    $formHandler = $this->get('my_module.form.handler');
    $form = $formHandler->getForm();
    $form->handleRequest($request);

    if ($form->isSubmitted() && $form->isValid()) {
        $errors = $formHandler->save($form->getData());
        if (empty($errors)) {
            $this->addFlash('success', $this->trans('Successful update.', 'Admin.Notifications.Success'));
        }
    }

    return $this->render('@Modules/my_module/views/templates/admin/form.html.twig', [
        'form' => $form->createView(),
    ]);
}
```

## 2. Professional Development Guide

### Services definition (`config/services.yml`)
```yaml
services:
  my_module.form.type:
    class: MyModule\Form\MyCustomType
    parent: 'form.type.translatable.aware'
    tags:
      - { name: form.type }

  my_module.form.data_configuration:
    class: MyModule\Form\MyDataConfiguration
    arguments: ['@prestashop.adapter.legacy.configuration']

  my_module.form.data_provider:
    class: PrestaShop\PrestaShop\Core\Form\ConfigurableFormDataProvider
    arguments:
      - '@my_module.form.data_configuration'
      - '@prestashop.core.localization.locale.context'

  my_module.form.handler:
    class: PrestaShop\PrestaShop\Core\Form\FormHandler
    arguments:
      - '@form.factory'
      - '@prestashop.core.hook.dispatcher'
      - '@my_module.form.data_provider'
      - 'MyModule\Form\MyCustomType'
      - 'MyModuleForm' # Hook name suffix
```

## 3. User Guide

### Advantages
- Automatic validation.
- Consistent UI with PrestaShop core.
- Easy integration with Symfony debug tools.

## Rules & Best Practices
- **Reuse Core Types**: Use `PrestaShopBundle\Form\Admin\Type\*` types for standard PrestaShop inputs (switches, translatable inputs, etc.).
- **Translations**: Use `TranslatorAwareType` to simplify translations inside the Form Type.
- **CSRF**: PrestaShop/Symfony handles CSRF protection automatically if using the FormHandler.
