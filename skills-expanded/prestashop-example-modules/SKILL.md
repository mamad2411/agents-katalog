---
name: prestashop-example-modules
description: Conocimiento extraido del repositorio oficial PrestaShop/example-modules (clonado en <herramientas>/example-modules) y contrastado con las fuentes del nucleo en <herramientas>/prestashop. Extender el formulario de producto del back-office en la pagina clasica (V1) y en la nueva (V2), hooks por demo, formularios Symfony, y que se puede hacer SIN src/ ni composer ni services.yml. Usar al desarrollar o depurar modulos de PrestaShop 1.7 / 8.x / 9.x.
---

# prestashop-example-modules

Conocimiento extraido del repositorio oficial `https://github.com/PrestaShop/example-modules` (clon local: `<herramientas>/example-modules`), contrastado en algunos puntos con el nucleo `<herramientas>/prestashop/9.1.1/`.

**Uso previsto:** material de CONSULTA para APIs, nombres de hooks y detalles tecnicos. No es autoridad sobre estructura de carpetas ni convenciones del proyecto. Si algo de aqui contradice el `CLAUDE.md` del proyecto, gana el `CLAUDE.md`.

**Aviso de version transversal:** la MAYORIA de las demos del repo oficial son **solo PS 9.x**. Los README estan desactualizados en varios modulos; la fuente fiable es siempre `$this->ps_versions_compliancy` en el fichero principal, no el README ni el `config.xml` (que casi nunca declara version).

---

## 1. Tabla resumen

| Demo | Para que sirve | Hooks | Version PS | Legacy puro? |
|---|---|---|---|---|
| **demoproductform** | Campos y PESTANAS nuevas en el formulario de producto V2 + formulario de combinacion; guardado por CQRS y por hook | `actionProductFormBuilderModifier`, `actionCombinationFormFormBuilderModifier`, `actionAfterUpdateCombinationFormFormHandler`, `displayAdminProductsExtra` | 9.0.0–9.99.99 (`demoproductform.php:45`) | NO (src/, composer, services.yml) |
| **demoproductextracontent** | Pestanas de contenido extra en la ficha de producto del **FRONT** | `displayProductExtraContent` | 1.7.0–9.99.99 (`demoproductextracontent.php:34`) | **SI** |
| **demoextrafield** | API nativa de *extra properties* (PS 9.2): campos custom en producto/categoria/cliente/direccion/CMS, con form BO, grid, API y front. Ademas via manual con hooks genericos sobre el form CMS | `displayProductAdditionalInfo`, `displayFooterProduct`, `displayCartExtraProductInfo`, `displayHeaderCategory`, `displayCustomerAccountTop`, `actionCmsPageFormBuilderModifier`, `actionCmsPageFormDataProviderData`, `actionAfterCreate/UpdateCmsPageFormHandler`, `displayCMSDisputeInformation` | 9.2.0–9.9.99 (`demoextrafield.php:52`) | **SI** |
| **demoseo** | Structured data JSON-LD + meta title/description desde un solo hook | `actionFrontControllerSetVariables` | >=9.2.0 (`demoseo.php:36`); el hook existe desde 1.7.5, los `structured_data` desde 9.2 | **SI** (ni config.xml trae) |
| **demosymfonyform** | Catalogo vivo de TODOS los form types de PrestaShop, 3 paginas BO, multiples formularios por pagina | Ninguno registrado; indirectos via `Core\Form\Handler` con hookName `DemoConfiguration` | 9.0.0+ (`demosymfonyform.php:44`) | NO |
| **demosymfonyformsimple** | Esqueleto minimo de pagina de configuracion Symfony (6 ficheros) con validacion y errores | Ninguno | 9.0.0+ (`demosymfonyformsimple.php:26`) | NO |
| **demoextendsymfonyform1** | Campo booleano en el form de Cliente + columna toggle y filtro en el grid; ObjectModel + repositorio DBAL | `actionCustomerGridDefinitionModifier`, `actionCustomerGridQueryBuilderModifier`, `actionCustomerFormBuilderModifier`, `actionAfterCreate/UpdateCustomerFormHandler` | 9.0.0–9.99.99 (`demoextendsymfonyform1.php:63-66`) | NO |
| **demoextendsymfonyform2** | Subida de imagen en el form de Proveedor + bloque HTML custom; Doctrine ORM | `actionSupplierFormBuilderModifier`, `actionAfterCreate/UpdateSupplierFormHandler` | 9.0.0–9.99.99 (`demoextendsymfonyform2.php:51`) | NO |
| **demoextendsymfonyform3** | Igual que #1 pero con CQRS propio (`#[AsCommandHandler]` / `#[AsQueryHandler]`) | Los 5 de Customer | 9.0.0–9.99.99 (`demoextendsymfonyform3.php:65-68`) | NO |
| **demoformdataproviders** | **Modificar los DATOS del formulario de producto V2 desde un modulo legacy puro** | `actionProductFormDataProviderData`, `actionProductFormDataProviderDefaultData` | 8.0.0–9.99.99 (`demoformdataproviders.php:34`) | **SI** |
| **demomultistoreform** | CRUD Symfony multitienda completo (grid, form, config multistore) | `displayFooterBefore`; indirectos `actionConfigurationFormForm/Save`, `actionContentBlockFormDataProvider*` | 9.0.0+ real (`demomultistoreform.php:48`); README dice 1.7.8-8.1 **OBSOLETO** | NO |
| **demoextendtemplates** | 5 vias de extender plantillas Twig del BO sin tocar el core + decorador de controlador + EventSubscriber | **Ninguno** | 9.1.0+ (`demoextendtemplates.php:34`) | Overrides Twig si; decorador/subscriber no |
| **democontrollertabs** | 5 escenarios de controlador Symfony + Tab de menu (`$this->tabs` vs `Tab` manual) + permisos | Ninguno | 9.0.0+ (`democontrollertabs.php:39`) | NO |
| **demo_grid** | Grid propio completo desde cero | Ninguno; su grid EMITE `action<GridId>Grid*Modifier` | 9.0.0+ (`demo_grid.php:34`) | NO |
| **demoextendgrid** | Anadir accion de fila al grid de Pedidos + JS AJAX | `actionOrderGridDefinitionModifier`, `actionAdminControllerSetMedia` | 9.0.0+ real (`demoextendgrid.php:42`); README dice 1.7.7-8.1 **OBSOLETO** | Hook si; la ruta de la accion no |
| **demofiltermodules** | Filtrar que modulos se ejecutan en un hook del front | Ninguno; tag `core.hook_module_exec_filter` | 8.2.1+ (`demofiltermodules.php:79`) | NO |
| **demomoduleroutes** | URLs amigables propias en el FRONT | `moduleRoutes` | 8.0.0–9.99.99 (`demomoduleroutes.php:30`) | **SI** |
| **demojsrouting** | Componente JS `Router` del BO para generar URLs Symfony desde JS | Ninguno; usa `$tabs` | 9.0.0+ (`demojsrouting.php:47`) | NO (pero el Router SI es usable en legacy) |
| **democonsolecommand** | Comando `bin/console` propio | Ninguno; tag `console.command` | 9.0.0+ (`democonsolecommand.php:34`) | NO |
| **demodoctrine** | CRUD completo con Doctrine ORM + entidad lang + grid + form identifiable object | `displayHome` | 9.0.0+ (`demodoctrine.php:40`) | NO |
| **demooverrideobjectmodel** | Anadir un campo a `Manufacturer` por override + ALTER TABLE. **El propio README lo marca como antipatron** | Ninguno (`Installer.php:60` array vacio) | 9.0.0+ (`demooverrideobjectmodel.php:38`); el mecanismo es identico en 1.7/8/9 | Practicamente si |
| **api_module** | Exponer recursos propios en la nueva API (API Platform) | Ninguno; atributos `#[ApiResource]` + tags de servicio | 9.0.0–9.99.99 (`api_module.php:42`) | NO |
| **dashexample** | Integracion con el Dashboard Symfony de PS 9.2. **Modulo "Symfony-light": renderiza Twig sin src/ ni services.yml** | `displayAdminDashboardZoneOne/Two/Three`, `...Top`, `...Bottom`, `...Toolbar` | 9.2.0+ (`dashexample.php:46`) + feature flag `dashboard` | **SI** |
| **demovieworderhooks** | Catalogo de hooks de la pagina "Ver pedido": PESTANA (TabLink+TabContent), zonas, botones de la barra de acciones, preview del listado | `displayAdminOrderTabLink`, `displayAdminOrderTabContent`, `displayAdminOrderMain`, `...MainBottom`, `...Side`, `...SideBottom`, `displayAdminOrder`, `displayAdminOrderTop`, `displayAdminOrderCreateExtraButtons`, `displayOrderPreview`, `actionGetAdminOrderButtons` | 9.0.0–9.99.99 (`demovieworderhooks.php:54`) | Los hooks si; Doctrine/servicios no |
| **demowsextend** | Recurso propio en el Webservice clasico `/api` | `addWebserviceResources` | 1.7.8+ (README; no declara compliancy) | **SI** |
| **example_module_mailtheme** | Temas de email: anadir tema, anadir/reemplazar layouts, inyectar variables, transformar el HTML final | `actionListMailThemes`, `actionBuildMailLayoutVariables`, `actionGetMailLayoutTransformations` | 9.0.0–9.99.99 (`example_module_mailtheme.php:60`) | Hooks si; la pagina de config Symfony no |

---

## 2. Formulario de producto

### 2.0 Regla de oro: hay DOS paginas de producto

- **V1 (clasica)**: `AdminProductsController` + HelperForm, PS 1.7 / 8.0. Del catalogo oficial, el **UNICO** hook que funciona ahi es `displayAdminProductsExtra`.
- **V2 (nueva)**: formulario Symfony (`EditProductFormType`), PS 8.1+ y 9.x. Aqui viven `actionProductFormBuilderModifier`, `actionProductFormDataProvider*`, extra properties, CQRS.

Ningun demo del repo cubre la V1 mas alla de `displayAdminProductsExtra`. Si el modulo debe soportar 8.0 clasica **y** 9.x, la unica via portable es `displayAdminProductsExtra` (solo lectura, cae en la pestana "Modulos").

### 2.1 V1 (clasica) y tambien V2: `displayAdminProductsExtra`

Hook de display normal. Recibe `$params['id_product']`, DEVUELVE un string HTML. En V2 el HTML se pinta dentro de la pestana **Modulos**. Es de SOLO LECTURA: no participa del guardado.

```php
// version Twig del demo (demoproductform.php:105-116)
public function hookDisplayAdminProductsExtra(array $params): string
{
    $customProduct = new CustomProduct($params['id_product']);
    /** @var \Twig\Environment $twig */
    $twig = $this->get('twig');
    return $twig->render('@Modules/demoproductform/views/templates/admin/extra_module.html.twig', [
        'customProduct' => $customProduct,
    ]);
}

// version LEGACY equivalente (Smarty) - valida en V1 y V2
public function hookDisplayAdminProductsExtra(array $params)
{
    $this->context->smarty->assign(['id_product' => (int) $params['id_product']]);
    return $this->display(__FILE__, 'views/templates/admin/mi_panel.tpl');
}
```
Evidencia: `demoproductform/demoproductform.php:97-116`, `views/templates/admin/extra_module.html.twig:20-31`.

### 2.2 V2 — Anadir un CAMPO dentro de una pestana existente

Hook `actionProductFormBuilderModifier`. Recibe:
- `$params['form_builder']` — `FormBuilderInterface` **raiz** del formulario de producto.
- `$params['id']` — id del producto. **Ausente/null en creacion: comprobar siempre.**

Se baja a la pestana con `->get('<pestana>')` y se posiciona con el servicio del core `form.form_builder_modifier` (metodo `addAfter`). Con `->add()` a secas el campo va al final.

```php
// Version del demo (con servicio propio)
public function hookActionProductFormBuilderModifier(array $params): void
{
    $modifier  = $this->get(ProductFormModifier::class);
    $productId = isset($params['id']) ? new ProductId((int) $params['id']) : null;
    $modifier->modify($productId, $params['form_builder']);
}

// Dentro del modifier (ProductFormModifier.php:58-83)
$descriptionTab = $productFormBuilder->get('description');
$this->formBuilderModifier->addAfter(
    $descriptionTab,
    'description',                  // campo ancla existente
    'demo_module_custom_field',     // nombre nuevo
    TextType::class,
    [
        'label'       => $this->translator->trans('Demo custom field', [], 'Modules.Demoproductform.Admin'),
        'label_attr'  => ['title' => 'h2', 'class' => 'text-info'],
        'data'        => $customProduct->custom_field,   // valor precargado
        'empty_data'  => '',
        'form_theme'  => '@PrestaShop/Admin/TwigTemplateForm/prestashop_ui_kit_base.html.twig',
    ]
);
```

**Version LEGACY (sin src/, sin composer, sin services.yml)** — el servicio del core se pide por su id string:

```php
public function hookActionProductFormBuilderModifier(array $params)
{
    $builder = $params['form_builder'];
    $value   = isset($params['id']) ? $this->leerValor((int) $params['id']) : '';

    $this->get('form.form_builder_modifier')->addAfter(
        $builder->get('description'),
        'description',
        'ecom_mi_campo',
        \Symfony\Component\Form\Extension\Core\Type\TextType::class,
        [
            'label'      => 'Mi campo',
            'required'   => false,
            'data'       => $value,
            'empty_data' => '',
            'form_theme' => '@PrestaShop/Admin/TwigTemplateForm/prestashop_ui_kit_base.html.twig',
        ]
    );
}
```
Evidencia: `demoproductform.php:88-95`, `src/Form/Modifier/ProductFormModifier.php:58-83`, `config/services.yml:3-7`.

### 2.3 V2 — Anadir una PESTANA nueva completa

Una pestana **no es una API especial**: es un hijo directo del builder RAIZ cuyo tipo es un FormType propio. El **titulo** de la pestana es la opcion `'label'` declarada en `configureOptions()` del FormType.

```php
// Posiciona la pestana justo despues de "Precios" (ProductFormModifier.php:85-109)
$this->formBuilderModifier->addAfter(
    $productFormBuilder,      // BUILDER RAIZ, no un sub-builder
    'pricing',                // pestana ancla
    'custom_tab',             // nombre = clave en $formData al guardar
    CustomTabType::class,
    ['data' => ['custom_price' => $customProduct->custom_price]]
);
// Segunda pestana, anclada a la primera
$this->formBuilderModifier->addAfter(
    $productFormBuilder, 'custom_tab', 'custom_tab_content', CustomTabContentType::class,
    ['data' => ['custom_price' => $customProduct->custom_price]]
);

// El TITULO de la pestana sale de aqui (CustomTabType.php:76-85)
public function configureOptions(OptionsResolver $resolver)
{
    parent::configureOptions($resolver);
    $resolver->setDefaults(['label' => $this->trans('Customization', 'Modules.Demoproductform.Admin')]);
}
```

**Version LEGACY:** un `class MiPestanaType extends \Symfony\Component\Form\AbstractType` **sin dependencias de constructor** en `classes/` (namespace global, cargado con `require_once`) funciona: Symfony instancia solo cualquier `AbstractType` con constructor vacio. El tag `form.type` de `services.yml` **solo** hace falta cuando el type tiene argumentos que inyectar. Se pierde `TranslatorAwareType` (exige `$locales`): traducir con `Context::getContext()->getTranslator()->trans()`.

### 2.4 V2 — Pestana de solo lectura / dashboard: form theme propio

Un FormType puede declarar `'form_theme'` apuntando a un twig del modulo. Ese twig extiende el tema base del UI-kit y sobreescribe el bloque `<block_prefix>_widget`, donde `block_prefix` es el snake_case del nombre de la clase sin el sufijo `Type` (`CustomTabContentType` -> `custom_tab_content`).

```php
public function buildView(FormView $view, FormInterface $form, array $options)
{
    parent::buildView($view, $form, $options);
    $view->vars['custom_price'] = $options['data']['custom_price'] ?? null;
}
public function configureOptions(OptionsResolver $resolver)
{
    parent::configureOptions($resolver);
    $resolver->setDefaults([
        'label'      => $this->trans('Customization content', 'Modules.Demoproductform.Admin'),
        'form_theme' => '@Modules/demoproductform/views/templates/admin/FormTheme/product_tab_content_form_theme.html.twig',
    ]);
}
```
```twig
{% extends '@PrestaShop/Admin/TwigTemplateForm/prestashop_ui_kit_base.html.twig' %}
{% block custom_tab_content_widget %}
  <div class="alert alert-info">{{ 'This is your custom tab content'|trans({}, 'Modules.Demoproductform.Admin') }}</div>
  <p>{{ 'Custom price'|trans({}, 'Modules.Demoproductform.Admin') }}: {{ custom_price }}</p>
{% endblock %}
```
Evidencia: `src/Form/Type/CustomTabContentType.php:32-51`, `views/templates/admin/FormTheme/product_tab_content_form_theme.html.twig:20-30`. `@Modules` resuelve la carpeta del modulo, asi que el twig puede vivir en `views/` sin `src/`.

### 2.5 V2 — Boton / enlace en el footer del formulario

```php
$footer = $productFormBuilder->get('footer');
$footer->add('forms_info', IconButtonType::class, [
    'label' => $this->translator->trans('Open supplier website'),
    'type'  => 'link',
    'attr'  => ['href' => 'http://www.prestashop.com', 'target' => '_blank'],
]);
```
`IconButtonType` = `PrestaShopBundle\Form\Admin\Type\IconButtonType`. Evidencia: `src/Form/Modifier/ProductFormModifier.php:111-122`.

### 2.6 V2 — Cambiar solo los VALORES (sin anadir campos): `FormDataProvider*`

**El patron mas valioso para arquitectura legacy.** `demoformdataproviders` es un modulo entero de 4 ficheros (`config.xml`, el `.php`, `index.php`, `README.md`) que modifica el formulario de producto V2. Sin `src/`, sin `composer.json`, sin `config/`.

```php
class DemoFormDataProviders extends Module
{
    public function install()
    {
        if (!parent::install()) { return false; }
        return $this->registerHook('actionProductFormDataProviderData')
            && $this->registerHook('actionProductFormDataProviderDefaultData');
    }

    // Se dispara al construir el formulario SIN id (alta)
    public function hookActionProductFormDataProviderDefaultData(array $params): void
    {
        $params['data']['details']['references']['mpn'] = 'NEWMPNPREFIX_';
    }

    // Se dispara al construir el formulario CON id (edicion)
    public function hookActionProductFormDataProviderData(array $params): void
    {
        $actual = $params['data']['details']['references']['mpn'];
        if (substr($actual, 0, 13) !== 'NEWMPNPREFIX_') {
            $params['data']['details']['references']['mpn'] = 'NEWMPNPREFIX_' . $actual;
        }
    }
}
```
Evidencia: `demoformdataproviders.php:45-53, 66-82`.

**Por que funciona la mutacion aunque la firma no lleve `&`:** el nucleo mete `data` y `options` en el array de parametros **como referencias**; al copiar el array, esos elementos siguen siendo referencias. `id` **NO** es referencia. Hay que ESCRIBIR en `$params['data'][...]`; reasignar `$params` entero no sirve.

```php
// PrestaShop 9.1.1, src/Core/Form/IdentifiableObject/Builder/FormBuilder.php:119-127
$this->hookDispatcher->dispatchWithParameters(
    'action' . $this->camelize($this->getFormName()) . 'FormDataProviderData',
    ['data' => &$data, 'id' => $id, 'options' => &$options]
);
```

### 2.7 Como se calcula el nombre de estos hooks (regla general)

`action` + `camelize(getBlockPrefix() del FormType RAIZ)` + `FormDataProviderData | FormDataProviderDefaultData | FormBuilderModifier`.

Mapa real del producto V2 en PS 9.1:

| FormType raiz | block prefix | Hooks |
|---|---|---|
| `EditProductFormType` | `product` | `actionProductFormDataProviderData`, `actionProductFormBuilderModifier` |
| `CreateProductFormType` (modal de alta) | `create_product` | `actionCreateProductFormDataProviderDefaultData` |

**Consecuencia:** `hookActionProductFormDataProviderDefaultData` del demo **NO se dispara nunca en la practica** en PS 9.1 (el nucleo solo llama `getFormFor()` sobre el builder de edicion). El prefijo en un producto nuevo lo pone en realidad el hook `...Data` tras el redirect. El README del demo es enganoso.

Evidencia nucleo: `FormBuilder.php:121, 164-172`; `EditProductFormType.php:181-183`; `CreateProductFormType.php:69-72`; `form_builder.yml:218-232`; `ProductController.php:398, 467`.

### 2.8 Anclas conocidas para `addAfter`

```php
// PRODUCTO (builder raiz)
'description', 'pricing', 'stock', 'shipping', 'seo', 'options', 'header', 'footer'
$productFormBuilder->get('description');   // dentro: campo 'description'
$productFormBuilder->get('footer');

// COMBINACION
addAfter($combinationFormBuilder, 'references', ...);
addAfter($combinationFormBuilder, 'price_impact', ...);

// Ruta de datos util (arbol del form V2)
$params['data']['details']['references']['mpn']
```
Si el ancla no existe, `addAfter` falla: comprobar la version antes de asumir un nombre. Evidencia: `ProductFormModifier.php:60, 88, 100, 113`; `CombinationFormModifier.php:64, 91`; `EditProductFormType.php:80 -> Details/DetailsType.php:54 -> Details/ReferencesType.php:41`.

### 2.9 GUARDAR los datos — tres caminos

**(a) Hooks `identifiable object` — no exige Symfony.** Llegan DESPUES de que el core guarde, con `$params['form_data']` ya validado.

```php
// Producto (documentado como alternativa oficial en CustomProductCommandsBuilder.php:34-38)
public function hookActionBeforeUpdateProductFormHandler(array $params) { }
public function hookActionAfterUpdateProductFormHandler(array $params)
{
    $id   = (int) $params['id'];
    $data = $params['form_data'];
    // $data['description']['ecom_mi_campo'], $data['custom_tab']['custom_price'], ...
}

// Combinacion (demoproductform.php:137-152)
public function hookActionAfterUpdateCombinationFormFormHandler(array $params): void
{
    $combinationId = $params['form_data']['id'];
    $obj = new CustomCombination($combinationId);
    $obj->custom_field = $params['form_data']['demo_module_custom_field'] ?? '';
    $obj->custom_price = $params['form_data']['custom_tab']['custom_price'] ?? 0.0;
    if (empty($obj->id)) { $obj->id = $combinationId; $obj->force_id = true; $obj->add(); }
    else { $obj->update(); }
}
```

**(b) CQRS (`ProductCommandsBuilderInterface`) — EXIGE `services.yml`.** El core descubre el builder **por el tag** `core.product_command_builder`. No hay forma de registrar un tag sin `services.yml`.

```yaml
PrestaShop\Module\DemoProductForm\CQRS\CommandBuilder\CustomProductCommandsBuilder:
    tags: ['core.product_command_builder']   # imprescindible
PrestaShop\Module\DemoProductForm\CQRS\CommandHandler\UpdateCustomProductCommandHandler:
    autoconfigure: true                       # para que #[AsCommandHandler] surta efecto
```
```php
public function buildCommands(ProductId $productId, array $formData, ShopConstraint $c): array
{
    $command = null;
    if (isset($formData['description']['demo_module_custom_field'])) {
        $command = $this->getCommand($command, $productId->getValue())
            ->setCustomerField($formData['description']['demo_module_custom_field']);
    }
    if (isset($formData['custom_tab']['custom_price'])) {
        $command = $this->getCommand($command, $productId->getValue())
            ->setCustomPrice((string) $formData['custom_tab']['custom_price']);
    }
    return null !== $command ? [$command] : [];
}
```
Nota util: `ProductFormDataHandler::create()` crea el producto minimo y luego llama a `update()`, asi que **no hace falta enganchar la creacion aparte** (documentado en `UpdateCustomProductCommandHandler.php:40-47`). Evidencia: `config/services.yml:15-22`, `CustomProductCommandsBuilder.php:40-62`.

**(c) PS 9.2+ — `registerExtraProperty()`: el core lo guarda TODO por ti.** Ver 2.10.

### 2.10 V2 en PS 9.2+ — campos custom **sin src/, sin composer, sin services.yml**

`Module::registerExtraProperty(new ExtraPropertyDefinition(...))` hace que el nucleo cree la columna SQL, el campo en el formulario Symfony, la columna del grid y la exposicion por API.

- `associatedForms: ['product']` -> el campo cae en una **pestana nueva "Extra fields"**.
- `associatedForms: ['product:options.suppliers:before']` -> se inserta dentro de la pestana Options, seccion suppliers, antes de ella. Formato: `entidad:tab.seccion:before`.
- `formType` acepta **cualquier** FormType de Symfony o de `PrestaShopBundle` por FQCN: por eso NO hace falta `services.yml` (esos tipos ya estan registrados en el contenedor del nucleo).

```php
use PrestaShop\PrestaShop\Core\ExtraProperty\Definition\ExtraPropertyDefinition;
use PrestaShop\PrestaShop\Core\ExtraProperty\Definition\ExtraPropertyScope;
use PrestaShop\PrestaShop\Core\ExtraProperty\Definition\ExtraPropertyType;
use PrestaShopBundle\Form\Admin\Type\SwitchType;

$this->registerExtraProperty(new ExtraPropertyDefinition(
    entityName: 'product',
    propertyName: 'is_dangerous',
    type: ExtraPropertyType::BOOL,
    scope: ExtraPropertyScope::COMMON,
    defaultValue: 0,
    nullable: false,
    displayFront: true,
    associatedApis: ['/products', '/products/{productId}'],
    associatedForms: ['product:options.suppliers:before'],  // 'product' solo => pestana "Extra fields"
    associatedGrids: ['product:reference'],
    formType: SwitchType::class,
    labelWording: 'Dangerous product',
    labelDomain: 'Modules.Demoextrafield.Admin',
));
```

Scopes y tablas: `COMMON` -> `<entidad>_extra`; `LANG` -> `<entidad>_extra_lang` (una fila por idioma); `SHOP` -> por tienda.
Tipos: `BOOL, STRING, DATE, INT, FLOAT, JSON, HTML, CHOICE` (con `enumValues`). Opcionales: `sqlIndex` (`ExtraPropertySqlIndex::KEY|UNIQUE`), `size`, `required`, `nullable`, `displayFront`, `formOptions`, `constraints`.

**Las `Constraint` van en `constraints`, NUNCA en `formOptions`** (este ultimo se persiste como JSON y no admite objetos).

Lectura/escritura desde PHP con el ObjectModel nativo:
```php
$product = new Product($productId, false, $languageId); // CON langId => campos LANG como escalar
$product->extra_properties['demoextrafield']['date_last_seen'] = date('Y-m-d H:i:s');
$product->update();
```
Render en Smarty (**regla obligatoria**: el primer salto con `->`, luego notacion punto, porque `ObjectModel` no implementa `ArrayAccess`):
```smarty
{foreach from=$objectModel->extra_properties.demoextrafield key=fieldName item=fieldValue}
  <li><strong>{$fieldName|escape:'htmlall':'UTF-8'}:</strong> {$fieldValue|escape:'htmlall':'UTF-8'}</li>
{/foreach}
{if $product.extra_properties.demoextrafield.is_dangerous|intval} ... {/if}
```
Desinstalacion (el 2o argumento decide si se hace DROP de la columna):
```php
return $this->unregisterExtraProperty(new ExtraPropertyDefinition('product', 'video_link'), false) // false = conservar datos
    && $this->unregisterExtraProperty(new ExtraPropertyDefinition('product', 'is_dangerous'), false)
    && parent::uninstall();
```
Evidencia: `demoextrafield.php:76-95, 103-127, 186-220, 376-397, 531-569, 595-631`; `views/templates/hook/_extra_properties.tpl:5-28`.

### 2.11 Ficha de producto en el FRONT: pestanas extra (1.7.0 → 9.x)

Es OBLIGATORIO devolver un array de objetos `ProductExtraContent`; HTML plano no funciona. La clase la autocarga el nucleo: FQCN inline, sin `use`, sin composer.

```php
public function install() { return parent::install() && $this->registerHook('displayProductExtraContent'); }

public function hookDisplayProductExtraContent($params)
{
    return [
        (new PrestaShop\PrestaShop\Core\Product\ProductExtraContent())
            ->setTitle('Primera pestana')
            ->setContent($this->fetch('module:mimodulo/views/templates/front/tab1.tpl')),
    ];
}
```
Evidencia: `demoproductextracontent.php:45-63`.

### 2.12 Persistencia limpia: tabla propia con id espejo

Patron del demo: PK = exactamente el `id_product` (o `id_product_attribute`), `force_id = true`, y el modulo nunca toca `product` ni `product_attribute`.

```php
final class CustomProduct extends \ObjectModel
{
    public $id;
    public string $custom_field = '';
    public float  $custom_price = 0.0;
    public $force_id = true;

    public static $definition = [
        'table'   => 'demoproductform_custom_product',
        'primary' => 'id',
        'fields'  => [
            'custom_field' => ['type' => self::TYPE_STRING],
            'custom_price' => ['type' => self::TYPE_FLOAT, 'validate' => 'isPrice'],
            'date_add'     => ['type' => self::TYPE_DATE, 'validate' => 'isDate'],
            'date_upd'     => ['type' => self::TYPE_DATE, 'validate' => 'isDate'],
        ],
    ];
}
// guardado
if (empty($o->id)) { $o->id = $productId; $o->force_id = true; $o->add(); }
else { $o->setFieldsToUpdate($updatedFields); $o->update(); }
```
Evidencia: `src/Entity/CustomProduct.php:26-53`, `UpdateCustomProductCommandHandler.php:53-76`, `src/Install/install.sql:1-19`.

---

## 3. Legacy vs Symfony

### 3.1 SE PUEDE HACER SIN `src/`, SIN `composer.json`, SIN `config/services.yml`

Prueba viva: `demoformdataproviders`, `demomoduleroutes`, `demowsextend`, `demoproductextracontent`, `demoseo`, `demoextrafield` y `dashexample` no tienen ninguno de esos ficheros (o `dashexample`, que tiene `composer.json` **sin bloque autoload**).

| Capacidad | Como | Evidencia |
|---|---|---|
| Modificar VALORES de cualquier formulario Symfony del BO | `action<BlockPrefix>FormDataProviderData` / `...DefaultData` | `demoformdataproviders.php:66-82` |
| ANADIR/quitar CAMPOS y PESTANAS a formularios del BO (producto V2, cliente, categoria, proveedor, CMS…) | `action<BlockPrefix>FormBuilderModifier` + `$this->get('form.form_builder_modifier')` | `FormBuilder.php:145-157` (nucleo); `demoproductform.php:88-95` |
| PRECARGAR valores del formulario | `action<Entidad>FormDataProviderData` (`$params['data']` llega **por referencia**) | `demoextrafield.php:731-750` |
| PERSISTIR tras guardar | `actionAfterCreate<Entidad>FormHandler` / `actionAfterUpdate<Entidad>FormHandler` (`$params['id']`, `$params['form_data']`) | `demoextendsymfonyform1.php:215-263` |
| FormType propio SIN dependencias de constructor | `class X extends \Symfony\Component\Form\AbstractType` en `classes/` con `require_once` | `services.yml` solo hace falta si el type tiene argumentos |
| Form theme Twig del modulo | `'form_theme' => '@Modules/<modulo>/views/...'` | `CustomTabContentType.php:32-51` |
| Renderizar Twig en un hook del BO | `$this->get('twig')->render('@Modules/<mod>/views/templates/admin/x.html.twig', $vars)` desde la clase Module | `dashexample.php:143-149` (modulo SIN src/) |
| PESTANA en una pagina Symfony del BO | Par `display...TabLink` + `display...TabContent` devolviendo HTML plano | `demovieworderhooks/views/templates/admin/tracking_link.html.twig:12-25` |
| Columnas, filtros y acciones en grids del core | `action<GridId>GridDefinitionModifier`, `...GridQueryBuilderModifier`, `...GridDataModifier`, `...GridFilterFormModifier`, `...GridPresenterModifier` | `demoextendgrid.php:84-122` |
| Inyectar CSS/JS en el BO | `actionAdminControllerSetMedia` (+ filtrar por `controller_name` y `action`) o emitir `<link>/<script>` desde la salida de un hook con `$this->getPathUri()` | `demoextendgrid.php:64-79`; `dashexample/views/templates/admin/toolbar.html.twig:11-14` |
| Campos custom en producto V2 + grid + API + front (PS 9.2+) | `registerExtraProperty()` | `demoextrafield.php:76-95` |
| URLs amigables en el FRONT | `hookModuleRoutes` | `demomoduleroutes.php:57-88` |
| Recurso en el Webservice `/api` | `addWebserviceResources` + `$webserviceParameters` | `demowsextend.php:74-83` |
| SEO: JSON-LD y meta title/description | `actionFrontControllerSetVariables` mutando `$params['templateVars']` | `demoseo.php:51-114` |
| Pestanas extra en la ficha de producto del FRONT | `displayProductExtraContent` | `demoproductextracontent.php:54-63` |
| Temas / layouts / transformaciones de email | `actionListMailThemes`, `actionBuildMailLayoutVariables`, `actionGetMailLayoutTransformations` | `example_module_mailtheme.php:145-276` |
| Override de plantillas Twig del BO | Convencion de ruta: `views/PrestaShop/<misma ruta que el core>/x.html.twig` — **cero PHP** | `demoextendtemplates` no registra ni un hook |
| Tab de menu del BO | `$this->tabs` en el constructor, o `new Tab()` en `install()` | `democontrollertabs.php:46-60, 80-102` |
| Despachar comandos/consultas del NUCLEO | `$this->get('prestashop.core.command_bus')` / `'prestashop.core.query_bus'` | `demoextendsymfonyform3.php:197, 247` |
| Componente JS `Router` del BO | `window.prestashop.instance.router.generate('ruta_del_core')` — disponible en cualquier pagina del BO | `demojsrouting/views/js/demo-page.js:19` |

### 3.2 EXIGE OBLIGATORIAMENTE `src/` + `composer.json` (PSR-4) + `config/services.yml` (y a veces `routes.yml`)

| Capacidad | Por que |
|---|---|
| **Crear un GRID propio** | El `GridFactory` se ensambla en `services.yml` con 4 argumentos; definition factory y query builder necesitan `parent:` de servicios del core. `demo_grid/config/services.yml:1-29` |
| **Controlador admin Symfony** (`PrestaShopAdminController`) | "when they do they must be defined as services". Necesita las tres piezas: PSR-4, `services.yml` (autowire+autoconfigure), `routes.yml`. `presentGrid()`, `buildSearchResponse()`, `addFlash()`, `createForm()`, `render()` Twig son suyos |
| **Rutas Symfony propias** | Todo lo que reciba un *nombre de ruta*: `route` de `ToggleColumn`/`SubmitRowAction`/`LinkRowAction`, `submit_route` de `SubmitBulkAction`, `path()` en Twig, `$tab->route_name`, `_legacy_link` |
| **FormType con dependencias inyectadas** | `TranslatorAwareType` exige `parent: 'form.type.translatable.aware'` + `tags: [{name: form.type}]`. `demosymfonyformsimple/config/services.yml:11-15` |
| **`Core\Form\Handler` + DataConfiguration/FormDataProvider** | Es un servicio; su 5o argumento es el hookName que genera `action<X>Form` / `action<X>Save` |
| **`FormBuilder`/`FormHandler` de IdentifiableObject** | Se crean SIEMPRE via factory del contenedor (`prestashop.core.form.builder.form_builder_factory::create`). Y son ellos los que disparan los hooks `FormDataProvider*`: un formulario montado a mano con `form.factory` **pierde la extensibilidad** |
| **CQRS propio del modulo** | `#[AsCommandHandler]` / `#[AsQueryHandler]` solo se procesan con `autoconfigure: true`. El tag `core.product_command_builder` no tiene equivalente legacy |
| **Doctrine ORM (entidades del modulo)** | Auto-descubrimiento sobre `modules/<mod>/src/Entity` — ruta obligatoria e inamovible. El repositorio se obtiene por `factory: ['@doctrine.orm.default_entity_manager', getRepository]` |
| **API Platform (nueva API)** | Atributos `#[ApiResource]` descubiertos por PSR-4 + tags `api_platform.state_provider` / `api_platform.state_processor` |
| **Comando de consola** | Unicamente el tag `console.command`. No hay API legacy |
| **Filtrar modulos por hook** | Tag `core.hook_module_exec_filter` + `HookModuleFilterInterface` (PS 8.2.1+). Requiere ademas `config/front/services.yml` |
| **Decorar un controlador del core** | `#[AsDecorator]` + `#[MapDecorated]`, procesados solo por el contenedor |
| **EventSubscriber sobre `KernelEvents`** | `autoconfigure` lo registra como listener |
| **Configuracion multitienda con checkboxes "ajuste especifico"** | Heredar `AbstractMultistoreConfiguration` (3 servicios del core inyectados) + `getParent()` devolviendo `MultistoreConfigurationType::class` |
| **`#[AdminSecurity]` y roles automaticos** | Infraestructura de seguridad Symfony; en legacy es Tab + tokens |

**Equivalencias legacy directas:**

| Symfony | Legacy |
|---|---|
| Grid propio | `ModuleAdminController` + `$this->fields_list` / `renderList()` (HelperList) |
| Ruta + accion AJAX del grid | JS inyectado por `actionAdminControllerSetMedia` que hace `$.post` contra un `ModuleAdminController` con su token (`Link::getAdminLink('AdminMiAccion')`) |
| `Core\Form\Handler` + `DataConfiguration` | `getContent()` con `Tools::isSubmit()` -> guardar -> `displayConfirmation()/displayError()`; un unico `HelperForm` con **pestanas** |
| `Configuration::set(..., ['html' => true])` | `Configuration::updateValue($key, $value, true)` |
| `SqlLoader` / DBAL | `Db::getInstance()->execute()` |
| Doctrine ORM | `ObjectModel` en `classes/` |
| `bin/console` | `ModuleFrontController` de tipo cron con token propio |
| Twig `@Modules/...` | `$this->display(__FILE__, 'views/templates/.../x.tpl')` |

---

## 4. Patrones de codigo reutilizables

### 4.1 Instalador separado + `registerHook()` con array

Funciona igual en legacy (`classes/Installer.php` con `require_once`) y en Symfony.

```php
public function install()
{
    if (!parent::install()) { return false; }
    return (new Installer())->install($this);
}

private function registerHooks(Module $module): bool
{
    $hooks = [
        'actionProductFormBuilderModifier',
        'actionAfterUpdateProductFormHandler',
        'displayAdminProductsExtra',
    ];
    return (bool) $module->registerHook($hooks);
}
```
**Cuidado:** con `$hooks = []`, `registerHook([])` devuelve falsy y el install fallaria (bug real en `demooverrideobjectmodel/src/Install/Installer.php:60`).

### 4.2 SQL de instalacion — dos variantes

```php
// (a) Nucleo/Symfony: SqlLoader con placeholders (demoproductform/src/Install/Installer.php:37-101)
$allowed = ['utf8mb4_general_ci', 'utf8mb4_unicode_ci'];
$collation = \Db::getInstance()->getValue('SELECT @@collation_database');
$loader = new SqlLoader();
$loader->setMetaData([
    'PREFIX_'     => _DB_PREFIX_,
    'ENGINE_TYPE' => _MYSQL_ENGINE_,
    'COLLATION'   => (empty($collation) || !in_array($collation, $allowed)) ? '' : 'COLLATE ' . $collation,
]);
$loader->parseFile($filepath);

// (b) LEGACY puro (demooverrideobjectmodel/src/Install/Installer.php:76-87)
$sql = Tools::file_get_contents($module->getLocalPath() . 'sql/install.sql');
$sql = str_replace(['_DB_PREFIX_', '_MYSQL_ENGINE_'], [_DB_PREFIX_, _MYSQL_ENGINE_], $sql);
Db::getInstance()->execute($sql);
```

### 4.3 El servicio del modulo NO existe todavia durante `install()`

Trampa real de PS 9. Patron: try/catch + construccion manual con servicios del CORE.

```php
private function getInstaller(): DBInstaller
{
    try { $installer = $this->get(DBInstaller::class); }
    catch (Exception) { $installer = null; }

    if (!$installer) {
        $installer = new DBInstaller(
            $this->get('doctrine.dbal.default_connection'),
            $this->getContainer()->getParameter('database_prefix')
        );
    }
    return $installer;
}
```
Evidencia: `api_module.php:74-92`; mismo problema resuelto con `require_once` incondicional del autoload en `demovieworderhooks.php:42-43`.

### 4.4 Pestana en una pagina Symfony del BO (contrato del id)

Dos hooks independientes; el core **no correlaciona nada**: si los ids no casan, la pestana aparece vacia.

```php
public function hookDisplayAdminOrderTabLink(array $params)    { return $this->render('tracking_link.html.twig'); }
public function hookDisplayAdminOrderTabContent(array $params) { return $this->render('tracking.html.twig', [...]); }
```
```twig
{# cabecera #}
<li class="nav-item">
  <a class="nav-link" id="trackingTab" data-toggle="tab" href="#trackingTabContent"
     role="tab" aria-controls="trackingTabContent" aria-selected="false">
    <i class="material-icons">pin_drop</i> {{ 'Package tracking'|trans }}
  </a>
</li>

{# panel: MISMO id, aria-labelledby = id del enlace #}
<div class="tab-pane fade show active" id="trackingTabContent" role="tabpanel" aria-labelledby="trackingTab">
```
Quitar `show active` si no quieres robar el foco a la pestana por defecto. Evidencia: `demovieworderhooks.php:142-166`.

### 4.5 Hook `action*` que MUTA una coleccion (barra de botones)

No devuelve nada: se modifica el objeto recibido.

```php
public function hookActionGetAdminOrderButtons(array $params)
{
    $order  = new Order($params['id_order']);
    $router = $this->get('router');
    /** @var \PrestaShop\PrestaShop\Core\Action\ActionsBarButtonsCollection $bar */
    $bar = $params['actions_bar_buttons_collection'];

    $bar->add(new \PrestaShop\PrestaShop\Core\Action\ActionsBarButton(
        'btn-secondary',
        ['href' => $router->generate('admin_customers_view', ['customerId' => (int) $order->id_customer])],
        'View customer'
    ));
}
```
Evidencia: `demovieworderhooks.php:83-115`.

### 4.6 Grid del core: columna toggle + filtro + JOIN

```php
public function hookActionCustomerGridDefinitionModifier(array $params)
{
    $definition = $params['definition'];

    $definition->getColumns()->addAfter('optin',
        (new ToggleColumn('is_allowed_for_review'))
            ->setName($this->trans('Allowed for review', [], 'Modules.X.Admin'))
            ->setOptions([
                'field'            => 'is_allowed_for_review',
                'primary_field'    => 'id_customer',
                'route'            => 'ps_demo_toggle_is_allowed',   // <- ESTO exige routes.yml
                'route_param_name' => 'customerId',
            ])
    );

    $definition->getFilters()->add(
        (new Filter('is_allowed_for_review', YesAndNoChoiceType::class))
            ->setAssociatedColumn('is_allowed_for_review')
    );
}

public function hookActionCustomerGridQueryBuilderModifier(array $params)
{
    /** @var \Doctrine\DBAL\Query\QueryBuilder $qb */
    $qb = $params['search_query_builder'];
    $criteria = $params['search_criteria'];

    $qb->addSelect('IF(d.`is_allowed_for_review` IS NULL,0,d.`is_allowed_for_review`) AS `is_allowed_for_review`');
    $qb->leftJoin('c', '`' . pSQL(_DB_PREFIX_) . 'mi_tabla`', 'd', 'd.`id_customer` = c.`id_customer`');

    if ('is_allowed_for_review' === $criteria->getOrderBy()) {
        $qb->orderBy('d.`is_allowed_for_review`', $criteria->getOrderWay());
    }
    foreach ($criteria->getFilters() as $name => $value) {
        if ('is_allowed_for_review' === $name) {
            $qb->andWhere('d.`is_allowed_for_review` = :v')->setParameter('v', $value);
            if (!$value) { $qb->orWhere('d.`is_allowed_for_review` IS NULL'); }
        }
    }
}
```
**Sin el QueryBuilderModifier la columna sale vacia.** Localizar la columna `actions` para anadir acciones de fila:
```php
foreach ($definition->getColumns() as $column) {
    if ('actions' === $column->getId()) { $actions = $column->getOptions()['actions']; break; }
}
$actions->add((new SubmitRowAction('mark_order'))->setName('Mark')->setIcon('push_pin')
    ->setOptions(['route' => 'x', 'route_param_name' => 'orderId', 'route_param_field' => 'id_order', 'use_inline_display' => true]));
```
Evidencia: `demoextendsymfonyform1.php:119-182`, `demoextendgrid.php:84-122`.

### 4.7 JS de accion de fila (delegacion + AJAX + growl)

```js
$(() => {
  $(document).on('click', '.js-submit-row-action', (event) => {
    event.preventDefault();
    const $t = $(event.currentTarget);
    $.post($t.data('url')).then((response) => {
      $t.find('i').addClass('text-success');
      $.growl({ message: response });
    });
  });
});
```
Delegacion sobre `document`: sobrevive a los repintados del grid. `data-url` puede apuntar a una ruta Symfony **o a un `ModuleAdminController` legacy con su token**. Evidencia: `demoextendgrid/views/js/orders-listing.js:18-27`.

### 4.8 Componentes JS del back-office (imprescindible con form types "ricos")

Sin esto, TinyMCE no aparece, el arbol de categorias no se despliega y los checkboxes multitienda no habilitan nada.

```js
window.prestashop.component.initComponents([
  'TranslatableField', 'TinyMCEEditor', 'TranslatableInput',
  'GeneratableInput', 'TextWithLengthCounter',
  'ChoiceTable', 'MultipleChoiceTable',
  'MultistoreConfigField', 'Grid', 'Router',
]);
window.prestashop.instance.generatableInput.attachOn('.js-generator-btn');
new window.prestashop.component.ChoiceTree('#form_category_choice_tree_type').enableAutoCheckChildren();

// Grid propio: el string es el GRID ID
const grid = new window.prestashop.component.Grid('mi_grid_id');
grid.addExtension(new window.prestashop.component.GridExtensions.SortingExtension());
grid.addExtension(new window.prestashop.component.GridExtensions.FiltersResetExtension());
```
Otras extensiones: `BulkActionCheckboxExtension`, `SubmitBulkExtension`, `SubmitRowActionExtension`, `ExportToSqlManagerExtension`, `LinkRowActionExtension`, `ReloadListActionExtension`, `AsyncToggleColumnExtension`.

Evidencia: `demosymfonyform/views/js/form.js:20-35`, `demo_grid/views/demo_grid.js:20-24`, `demomultistoreform/views/js/form.js:19-28`.

### 4.9 URLs amigables en el front (`moduleRoutes`)

Cuatro llaves obligatorias por ruta; `params` DEBE incluir `fc` y `module`.

```php
public function install() { return parent::install() && $this->registerHook('moduleRoutes'); }

public function hookModuleRoutes()
{
    return [
      'module-mimodulo-show' => [
        'rule'     => 'mimodulo/show/{id}/{slug}',
        'keywords' => [
          'id'   => ['regexp' => '[0-9]*', 'param' => 'id'],
          'slug' => ['regexp' => '.*',     'param' => 'slug'],
        ],
        'controller' => 'show',                                    // controllers/front/show.php
        'params'     => ['fc' => 'module', 'module' => 'mimodulo'],
      ],
    ];
}
// Clase: <ClasePrincipal>ShowModuleFrontController extends ModuleFrontController
// Los keywords se leen con Tools::getValue('id'), NO como argumentos
```
Generar la URL: `$this->context->link->getModuleLink('mimodulo', 'show', ['id' => 1, 'slug' => 'abc'])` o `{url entity='module' name='mimodulo' controller='show' params=['id'=>1]}`.
Solo funciona con **Friendly URL activo**. Evidencia: `demomoduleroutes.php:57-88`, `controllers/front/show.php:7-22`.

### 4.10 Webservice `/api` — recurso propio (100% legacy, 1.7.8+)

```php
require_once _PS_MODULE_DIR_ . 'demowsextend/src/Entity/Article.php';

public function hookAddWebserviceResources($params)
{
    return [
        'articles' => [
            'description' => 'Blog articles',
            'class'       => 'Article',
            // 'forbidden_method' => ['DELETE'],
        ],
    ];
}

class Article extends ObjectModel   // SIN namespace
{
    public static $definition = ['table' => 'article', 'primary' => 'id_article', 'multilang' => true, 'fields' => [...]];

    protected $webserviceParameters = [
        'objectNodeName'  => 'article',
        'objectsNodeName' => 'articles',
        'fields' => ['title' => ['required' => true], 'content' => []],
    ];
}
```
`$webserviceParameters['fields']` es el subconjunto EXPUESTO por la API. Evidencia: `demowsextend.php:25, 74-83`; `src/Entity/Article.php:25, 55-64`.

### 4.11 Override de plantillas Twig del BO — cero PHP

Replicar bajo `views/PrestaShop/` la **misma ruta relativa** que el twig tiene en el core.

```twig
{# views/PrestaShop/Admin/Sell/Order/Order/index.html.twig #}
{% extends '@PrestaShopCore/Admin/Sell/Order/Order/index.html.twig' %}
{% block content %}
  {{ parent() }}
  <div class="text-success"><p>Contenido anadido</p></div>
{% endblock %}
```
Bloque que vive en una plantilla **incluida**: hay que re-embeberla pasando sus variables a mano.
```twig
{% block order_grid_row %}
  {% embed '@PrestaShop/Admin/Common/Grid/grid_panel.html.twig' with {'grid': orderGrid} %}
    {% block grid_panel_header %}<div><a href="#">Mi cabecera</a></div>{% endblock %}
  {% endembed %}
{% endblock %}
```
Alias: `@PrestaShop/...` respeta overrides; `@!PrestaShop/...` y `@PrestaShopCore/...` (desde PS 8.0) fuerzan el original del core.
Evidencia: `demoextendtemplates/views/PrestaShop/Admin/Sell/Order/Order/index.html.twig:1-36`.

### 4.12 SEO desde un hook (`actionFrontControllerSetVariables`)

`$params['templateVars']` se muta **en sitio**; el metodo no devuelve nada. Comprobar `isset()` de cada rama.

```php
public function hookActionFrontControllerSetVariables($params)
{
    if ($this->context->controller->php_self === 'product') {
        if (isset($params['templateVars']['structured_data']['product'])) {
            $params['templateVars']['structured_data']['product']['aggregateRating'] = [
                '@type' => 'AggregateRating', 'ratingValue' => 4.8, 'reviewCount' => 27,
                'bestRating' => 5, 'worstRating' => 1,
            ];
        }
        if (isset($params['templateVars']['structured_data']['product']['offers'])) {
            $params['templateVars']['structured_data']['product']['offers']['availability'] = 'https://schema.org/LimitedAvailability';
        }
    }
    if ($this->context->controller->getPageName() === 'category') {
        $c = new Category(Tools::getValue('id_category'), $this->context->language->id, $this->context->shop->id);
        $params['templateVars']['page']['meta']['title'] = $c->name . ' | ' . $this->context->shop->name;
    }
}
```
Claves utiles: `structured_data.product`, `.product.offers`, `.organization`, `page.meta.title`. Evidencia: `demoseo.php:51-114`.

### 4.13 Temas y layouts de email

```php
// Anadir un TEMA completo escaneando una carpeta
public function hookActionListMailThemes(array $hookParams)
{
    if (!isset($hookParams['mailThemes'])) { return; }
    $theme = (new FolderThemeScanner())->scan(_PS_MODULE_DIR_ . 'mimodulo/mails/themes/dark_modern');
    if (null !== $theme && $theme->getLayouts()->count() > 0) { $hookParams['mailThemes']->add($theme); }
}

// REEMPLAZAR un layout del core conservando su contenido
$orderConf = $theme->getLayouts()->getLayout('order_conf', '');  // '' = layouts del core
$idx = $theme->getLayouts()->indexOf($orderConf);
$theme->getLayouts()->offsetSet($idx, new Layout($orderConf->getName(),
    '@Modules/mimodulo/mails/layouts/extended_modern_order_conf_layout.html.twig', ''));
```
```twig
{% extends '@MailThemes/modern/core/order_conf.html.twig' %}
{% block content %}{{ parent() }} ... extra ... {% endblock %}
```
Transformacion del HTML final (DOM Crawler):
```php
class MiTransformation extends AbstractTransformation
{
    public function __construct($c) { parent::__construct(MailTemplateInterface::HTML_TYPE); $this->c = $c; }
    public function apply($templateContent, array $templateVariables)
    {
        $crawler = new Crawler($templateContent);
        foreach ($crawler->filter('span[class="subtitle"]') as $span) {
            $span->setAttribute('style', sprintf('color: %s;', $this->c));
        }
        return $crawler->html();
    }
}
```
**Filtrar siempre** por `templateType` y por que el layout sea tuyo (`$hookParams['mailLayout']->getModuleName() != $this->name`) o transformas correos ajenos. Evidencia: `example_module_mailtheme.php:145-276`.

### 4.14 Tab de menu del BO — dos formas

```php
// (a) DECLARATIVA, en el CONSTRUCTOR. 'name' indexado por LOCALE
$this->tabs = [[
    'route_name'        => 'ps_controller_tabs_configure',  // solo con routes.yml
    'class_name'        => 'AdminDemoControllerTabsConfigure',
    'visible'           => true,
    'name'              => $tabNames,   // [locale => texto]
    'icon'              => 'school',
    'parent_class_name' => 'IMPROVE',
]];

// (b) MANUAL en install(). 'name' indexado por id_lang
$tabId = (int) Tab::getIdFromClassName($className);
$tab = new Tab($tabId ?: null);
$tab->active = 1;
$tab->class_name = $className;
$tab->route_name = 'ps_controller_tabs_manual_tab';   // omitir en legacy
$tab->name = []; foreach (Language::getLanguages() as $l) { $tab->name[$l['id_lang']] = '...'; }
$tab->icon = 'build';
$tab->id_parent = (int) Tab::getIdFromClassName('IMPROVE');
$tab->module = $this->name;
return (bool) $tab->save();
```
El motivo real de crear la Tab no es solo el menu: es que **se creen los roles de autorizacion**. Evidencia: `democontrollertabs.php:46-60, 80-102`.

### 4.15 `getContent()` que redirige a una pagina Symfony

```php
public function getContent()
{
    Tools::redirectAdmin($this->context->link->getAdminLink('AdminMiControlador'));
    // o: Tools::redirectAdmin($this->get('router')->generate('mi_ruta'));
    // o: Tools::redirectAdmin(SymfonyContainer::getInstance()->get('router')->generate('mi_ruta'));
}
```
Requiere `is_configurable=1` en `config.xml`. Con `_legacy_link` en la ruta, `getAdminLink()` resuelve a la URL Symfony.

### 4.16 `_legacy_controller` vs `_legacy_link`

| Parametro | Rol |
|---|---|
| `_legacy_controller` | Nombre logico usado por el sistema de **PERMISOS**; al declararlo se crean los roles del controlador (permite controlador seguro **sin** tab visible) |
| `_legacy_link` | Permite que `Link::getAdminLink('AdminXxx')` genere la URL de esa ruta desde codigo legacy |

Un controlador puede llevar los dos, uno o ninguno. Evidencia: `democontrollertabs/config/routes.yml:2-27`.

### 4.17 Comando de consola — registro minimo

```yaml
# config/services.yml — esto es TODO
services:
    PrestaShop\Module\DemoConsoleCommand\Command\ListManufacturersCommand:
        tags: [ console.command ]
```
```php
protected function configure() { $this->setName('demo:list-manufacturers')->setDescription('...'); }
protected function execute(InputInterface $input, OutputInterface $output)
{
    (new Table($output))->setHeaders(['id','name'])->setRows($rows)->render();
    return 0;
}
```
Se ejecuta con `php bin/console demo:list-manufacturers` desde la **raiz de PrestaShop**. La clase principal del modulo puede estar vacia. Evidencia: `democonsolecommand/config/services.yml:1-3`.

### 4.18 Filtrar modulos por hook (PS 8.2.1+)

```yaml
# config/common.yml
services:
  Module\DemoFilterModules\Service\CustomModuleList:
    tags: [ 'core.hook_module_exec_filter' ]
# config/services.yml       -> imports: [{ resource: ./common.yml }]
# config/front/services.yml -> imports: [{ resource: ../common.yml }]
```
```php
public function filterHookModuleExecList(array $modules, string $hookName): array
{
    if (defined('_PS_ADMIN_DIR_')) { return $modules; }   // no tocar el BO
    if ($hookName === 'displayFooter') {
        foreach ($modules as $i => $m) {
            if ($m['module'] === 'ps_linklist') { unset($modules[$i]); }
        }
    }
    return $modules;
}
```
Se ejecuta en **cada** ejecucion de hook: ser barato en CPU. Evidencia: `demofiltermodules/src/Service/CustomModuleList.php:7-28`.

### 4.19 Override de ObjectModel del core (**antipatron, solo referencia**)

```php
// override/classes/Manufacturer.php
class Manufacturer extends ManufacturerCore
{
    public string $code;

    public function __construct(?int $id = null, ?int $idLang = null)
    {
        // el campo se inyecta ANTES del parent::__construct
        self::$definition['fields']['code'] = ['type' => self::TYPE_STRING, 'size' => 64];
        parent::__construct($id, $idLang);
    }
}
```
```sql
-- install.sql
ALTER TABLE _DB_PREFIX_manufacturer ADD `code` VARCHAR(64) NOT NULL DEFAULT '';
-- uninstall.sql
ALTER TABLE _DB_PREFIX_manufacturer DROP COLUMN `code`;
```
Si se inyecta DESPUES del `parent::__construct`, la carga del objeto ignora la columna. El README oficial lo desaconseja: solo un modulo puede overridear una clase a la vez.

### 4.20 Modulo "Symfony-light": Twig en el BO sin `src/`

`dashexample` renderiza Twig, usa el contenedor y **no tiene `src/`, ni `config/services.yml`, ni bloque `autoload` en `composer.json`**.

```php
class DashExample extends Module      // namespace GLOBAL
{
    public function hookDisplayAdminDashboardZoneOne(array $params): string
    {
        return $this->render('zone_one.html.twig', [
            'dateFrom' => $params['date_from'] ?? null,
            'dateTo'   => $params['date_to'] ?? null,
        ]);
    }

    public function hookDisplayAdminDashboardToolbar(array $params): string
    {
        // CSS/JS del modulo emitidos desde la salida del hook, sin actionAdminControllerSetMedia
        return $this->render('toolbar.html.twig', ['moduleUri' => $this->getPathUri()]);
    }

    private function render(string $template, array $params = []): string
    {
        /** @var \Twig\Environment $twig */
        $twig = $this->get('twig');
        return $twig->render(sprintf('@Modules/%s/views/templates/admin/%s', $this->name, $template), $params);
    }
}
```
Evidencia: `dashexample.php:39, 72-78, 133-149`; `views/templates/admin/toolbar.html.twig:11-14`.

---

## 5. Errores y trampas conocidas

### 5.1 Versiones y documentacion

1. **Los README mienten.** `demoextendgrid/README.md:15` dice "1.7.7 to 8.1" pero el codigo es PS 9 (`PrestaShopAdminController`, icono `push_pin`). `demomultistoreform/README.md:47` dice "1.7.8 a 8.1" pero declara `min 9.0.0`. `demodoctrine/README.md:5` dice "1.7.7 and above" y la linea 13 del mismo fichero dice "9.0.0 and above". **Fiarse solo de `ps_versions_compliancy`.**
2. **`config.xml` casi nunca declara version de PS.** La compliancy vive en el constructor. Y hay desincronizaciones internas: `demoextendgrid/config.xml` declara 1.1.0 y el `.php` 1.2.0; `demodoctrine/config.xml` 1.0.0 vs `.php` 2.0.0.
3. **PS 8 vs PS 9 en controladores:** PS 9 usa `PrestaShopBundle\Controller\Admin\PrestaShopAdminController` + inyeccion por argumento con `#[Autowire(service: 'id')]`. PS 8 usaba `FrameworkBundleAdminController` + `$this->get('id')`. **Este codigo NO es portable tal cual a 8.x.**
4. **`demoextrafield` es SOLO 9.2.x.** `ExtraPropertyDefinition`, `registerExtraProperty()`, etc. no existen en 8.x ni en 9.0/9.1: llamarlos **rompe la instalacion**. Para 8.x el sustituto es el trio `FormBuilderModifier` + `FormDataProviderData` + `AfterCreate/UpdateFormHandler` con tabla propia.
5. **`demoseo` exige 9.2.0** para los `structured_data`, aunque el hook exista desde 1.7.5.0.
6. **`dashexample` requiere ademas el feature flag `dashboard`** activado en Parametros Avanzados > Nuevas funcionalidades experimentales.

### 5.2 Formularios

7. **`$params['id']` es `null` en la pantalla de creacion.** Comprobarlo siempre antes de cargar datos.
8. **`setData()` requiere el array COMPLETO.** `$formBuilder->setData($params['data'])` tras escribir tu clave; si pasas solo el campo nuevo, **pierdes el resto de datos del formulario**.
9. **El `FormBuilderModifier` SOLO pinta el campo; no guarda nada.** Hay que registrar ademas `actionAfterCreate...` **y** `actionAfterUpdate...`.
10. **`actionProductFormDataProviderDefaultData` no se dispara en el alta de producto de PS 9.1** (el modal usa block prefix `create_product`). Ver 2.7.
11. **Solo `data` y `options` viajan por referencia** en los hooks de FormDataProvider; `id` va por valor.
12. **Un formulario montado a mano con `form.factory` pierde los hooks.** Los `FormDataProvider*` los dispara el `FormBuilder` de factoria del core.
13. **Hay DOS interfaces distintas llamadas `FormDataProviderInterface`:**
    - `PrestaShop\PrestaShop\Core\Form\FormDataProviderInterface` — configuracion: `getData(): array`, `setData(array): array` (devuelve errores).
    - `PrestaShop\PrestaShop\Core\Form\IdentifiableObject\DataProvider\FormDataProviderInterface` — CRUD: `getData($id)`, `getDefaultData()`; el guardado va en `FormDataHandlerInterface` aparte.
    Elegir la equivocada es error de compilacion del contenedor.
14. **HelperForm/Symfony:** cada campo anadido en `renderForm()` DEBE tener valor en `fields_value` o Smarty lanza `Undefined array key`.
15. **`block_prefix != entityName` rompe la inyeccion automatica de extra properties.** Caso documentado: `ManufacturerAddressType` (prefix `manufacturer_address`) frente a la entidad `address` — el campo solo puede ir al grid, no al formulario.
16. **`GeoCoordinatesType`** se anade como `'coordinates'` pero en `$form->getData()` aparece como `latitude`/`longitude` planos. **Inspeccionar siempre la estructura real de `getData()` antes de escribir el DataConfiguration.**
17. **Sin `form_theme` del UI Kit los campos salen rotos.** Hay que ponerlo en `configureOptions()` **y** con `{% form_theme %}` en el Twig.
18. **Bug latente que NO hay que copiar** (`demoproductform`): el handler comprueba `null !== $command->getCustomerField()` pero la propiedad es `private string $customerField = ''` — nunca es null, asi que la condicion es siempre true y `setFieldsToUpdate()` no filtra nada. Tipar `?string = null`. Evidencia: `UpdateCustomProductCommand.php:45, 59-62` vs `UpdateCustomProductCommandHandler.php:57-60`.
19. **Antipatron en `demomultistoreform`:** sobrescribe `validateConfiguration()` devolviendo `true` a secas, anulando el `OptionsResolver` del padre. No copiarlo.
20. **Ruta de guardado multitienda: debe aceptar `PATCH`.** La extension fuerza `$builder->setMethod(Request::METHOD_PATCH)` cuando hay checkboxes multitienda. Si la ruta solo declara `POST` -> **405 imposible de diagnosticar**. Evidencia: `MultistoreConfigurationTypeExtension.php:41-42`.
21. **Varios formularios en una pagina:** en las acciones de guardado se comprueba solo `isSubmitted()` (no `isValid()`), porque tras el redirect el usuario no veria los errores de constraint; la validacion se hace en el DataConfiguration devolviendo errores.

### 5.3 Grids

22. **Sin `GridQueryBuilderModifier` la columna nueva sale vacia.** Y usar `IF(x IS NULL, 0, x)` o el toggle revienta en filas sin registro.
23. **Filtrar por "No" requiere `orWhere(... IS NULL)`.**
24. **`GRID_ID` unico.** `demo_grid` usa `'product'`, que **COLISIONA** con el grid nativo (mismo `filterId` en la tabla de filtros del empleado y mismo nombre de hook `actionProductGridDefinitionModifier`). En modulo real usar `ecom_misregistros`.
25. **El Grid necesita DOS rutas con el mismo path:** GET (index) y POST (`searchAction` -> `buildSearchResponse`). Sin la POST, el formulario de filtros da **405**.
26. **`SqlFilters` con concatenacion insegura:** `demomultistoreform/src/Grid/Query/ContentBlockQueryBuilder.php:49,71` hace `implode()` de IDs directamente en el WHERE. Usar `setParameter`/`createNamedParameter`.
27. **`GridFactory` debe ser `public: true`** para inyectarlo por id de servicio.

### 5.4 Instalacion / servicios

28. **Durante `install()` el contenedor del modulo aun no esta compilado:** `$this->get(MiServicio::class)` lanza excepcion. Patron try/catch + construccion manual (ver 4.3).
29. **Durante `install()` las entidades Doctrine no estan mapeadas:** crear tablas con SQL crudo, nunca con el `EntityManager`.
30. **`require_once vendor/autoload.php`:** obligatorio si la clase principal referencia clases de `src/` antes de que exista el contenedor (constantes `TAB_CLASS_NAME`, `InstallerFactory`). `demoextendsymfonyform1` y `3` NO lo hacen y funcionan porque PrestaShop carga el autoloader del modulo; `api_module` lo hace con `file_exists` (defensivo); `demovieworderhooks` lo hace incondicional. Recomendacion: incluirlo.
31. **`"config": {"prepend-autoloader": false}`** en `composer.json`: importante para que el autoloader del modulo no se anteponga al del nucleo y provoque conflictos de version de librerias.
32. **`public: true` es obligatorio** en todo servicio que se consuma con `$this->get('id')` desde un hook.
33. **`registerHook([])` con array vacio devuelve falsy** y hace fallar el install.
34. **`Tab::getIdFromClassName`** puede lanzar `NonUniqueResult` en PS 9 con tabs duplicadas. Usar `Db::getValue` para comprobar existencia.
35. **`hookName` generico en `Core\Form\Handler`:** `demomultistoreform` pasa `'ConfigurationForm'`, generando `actionConfigurationFormForm`/`Save` — colisionables. Usar un nombre unico (`EcomMiModuloConfiguration`).

### 5.5 Plantillas y traducciones

36. **Override de `views/PrestaShop/Admin/layout.html.twig` es GLOBAL a todo el back-office** y solo un modulo puede ganar por fichero. Dos modulos que sobrescriban el mismo twig colisionan. Redefinir la macro `alert()` cambia el HTML de TODAS las alertas del BO.
37. **`{{ parent() }}` es obligatorio** al sobrescribir `{% block javascripts %}` / `{% block stylesheets %}`, o se pierden jQuery y los componentes del BO.
38. **Inconsistencia real de dominios de traduccion en el repo oficial:** algunas plantillas Twig usan `Module.<Studly>.Admin` (singular) y el PHP usa `Modules.<Studly>.Admin` (plural). Verificar cual consume la instalacion.
39. **`demoextrafield/README.md:95` remite a `registerTranslationWordings()`, metodo que NO existe** en el codigo (fichero leido integro, 812 lineas). No copiar esa referencia.
40. **`{displayPrice price=... currency=...}` NO existe en PS 1.7/8/9** (era de 1.6) -> Fatal error. Formatear en PHP.
41. **`demodoctrine/views/templates/front/home.tpl:30-31` imprime sin `|escape`.** Viola las reglas de este proyecto.
42. **Los ejemplos usan `{l s='...' mod='modulo'}` (sistema LEGACY)** porque no declaran `isUsingNewTranslationSystem()`. Si tu modulo lo declara `true`, `mod=` **NO leera los `.xlf`**.
43. **`democontrollertabs/views/templates/admin/layout.html.twig:74,79` carga highlight.js desde un CDN externo.** Evitar en produccion.

### 5.6 Rendimiento / seguridad

44. **`demoextrafield` escribe en BD dentro de un hook de FRONT** (`displayFooterProduct`, `demoextrafield.php:595-631`): un `UPDATE` por cada visita de ficha. Util como demo, **peligroso en produccion**.
45. **`actionAdminControllerSetMedia` se dispara en TODOS los controladores del BO.** Filtrar por `$this->context->controller->controller_name` **y** por `Tools::getValue('action')` (el mismo controlador sirve listado, detalle y alta). Nunca usar `$controller::class`.
46. **`core.hook_module_exec_filter` se ejecuta en cada ejecucion de hook**: cortocircuitar el BO con `defined('_PS_ADMIN_DIR_')`.
47. **Bug real en `api_module`:** `HorseProvider.php:56` usa `$operation instanceof Patch` pero el `use` de la linea 33 solo importa `Put` — el `instanceof` resuelve a una clase inexistente del namespace local y nunca coincide.
48. **`demoextendsymfonyform2/config/routes.yml:6-7`** declara `requirements` sobre `categoryId` cuando el parametro real es `supplierId` (copy/paste erroneo: el requirement no aplica). Y el mismo modulo usa dos dominios de traduccion distintos (`Modules.DemoExtendSymfonyForm2.Admin` en :55-56 vs `Modules.DemoExtendSymfonyForm` en :95).
49. **`ProductFormModifier.php:111-122`**: la variable se llama `$headerFormBuilder` pero apunta a `'footer'`. Ruido de copy/paste del repo oficial.
50. **El `.sql` partido por lineas** (`preg_split('/\r\n|\r|\n/')`) solo funciona con UNA sentencia por linea. No parte por `;`.

### 5.7 Multitienda

51. **`$multistoreCompatibility`** (`self::MULTISTORE_COMPATIBILITY_YES|_NO|_NOT_CONCERNED|_UNKNOWN`) es una linea y evita el aviso de "compatibilidad desconocida". Funciona igual en legacy y Symfony.
52. **`getShopConstraint()` devuelve `null` en contexto "todas las tiendas"** y el `ShopConstraint` concreto en contexto tienda/grupo.
53. **Borrado consciente del contexto:** en contexto tienda, un elemento asociado a varias tiendas solo debe DESASOCIARSE del contexto actual y eliminarse cuando quede huerfano.

---

## 6. Chuleta de nombres de hook

```
# Formularios Symfony del BO (X = block prefix del FormType raiz, camelizado)
action{X}FormDataProviderDefaultData     -> valores por defecto (alta)
action{X}FormDataProviderData            -> valores al editar
action{X}FormBuilderModifier             -> anadir / quitar campos y pestanas
actionBefore{Create|Update}{X}FormHandler
actionAfter{Create|Update}{X}FormHandler -> persistir ($params['id'], $params['form_data'])

# Grids (X = getId() de la GridDefinitionFactory)
action{X}GridDefinitionModifier          -> columnas, filtros, row actions
action{X}GridQueryBuilderModifier        -> SQL del listado
action{X}GridDataModifier
action{X}GridFilterFormModifier
action{X}GridPresenterModifier

# Producto
actionProductFormBuilderModifier
actionCombinationFormFormBuilderModifier
actionAfterUpdateCombinationFormFormHandler
displayAdminProductsExtra                -> V1 y V2 (pestana "Modulos"), solo lectura
displayProductExtraContent               -> FRONT, devuelve ProductExtraContent[]
displayProductAdditionalInfo             -> FRONT
displayFooterProduct                     -> FRONT

# Pagina Ver pedido (BO)
displayAdminOrderTabLink / displayAdminOrderTabContent   -> PESTANA (ids deben casar)
displayAdminOrderMain / ...MainBottom / ...Side / ...SideBottom / ...Top / displayAdminOrder
displayAdminOrderCreateExtraButtons
displayOrderPreview                      -> $params['order_id'] (NO 'id_order')
actionGetAdminOrderButtons               -> muta $params['actions_bar_buttons_collection']

# Dashboard PS 9.2 (nuevo -> legacy)
displayAdminDashboardZoneOne/Two/Three   -> dashboardZoneOne/Two/Three
displayAdminDashboardTop                 -> displayDashboardTop
displayAdminDashboardToolbar             -> displayDashboardToolbarTopMenu
displayAdminDashboardBottom

# Email
actionListMailThemes / actionBuildMailLayoutVariables / actionGetMailLayoutTransformations

# Otros
moduleRoutes                             -> URLs amigables del FRONT (Friendly URL ON)
addWebserviceResources                   -> recurso en /api
actionFrontControllerSetVariables        -> structured_data + meta
actionAdminControllerSetMedia            -> CSS/JS en el BO (filtrar!)

# Tags de contenedor (NO son hooks; exigen services.yml)
core.product_command_builder     console.command
core.hook_module_exec_filter     api_platform.state_provider / .state_processor
form.type
```

---

## 7. Decision rapida

| Necesito… | Legacy? | Como |
|---|---|---|
| Panel de solo lectura en la ficha de producto (V1 y V2) | SI | `displayAdminProductsExtra` + Smarty |
| Campo editable en una pestana existente del producto V2 | SI | `actionProductFormBuilderModifier` + `$this->get('form.form_builder_modifier')` |
| Pestana nueva en el producto V2 | SI | `addAfter` sobre el builder RAIZ + `AbstractType` sin dependencias en `classes/` |
| Campo custom producto V2 + grid + API, en PS 9.2 | SI | `registerExtraProperty()` |
| Guardar ese campo | SI | `actionAfterUpdateProductFormHandler` + `ObjectModel` en `classes/` |
| Solo cambiar valores por defecto / precargados | SI | `action<X>FormDataProvider*Data` |
| Anadir columna/filtro/accion a un grid del core | SI (la accion, con `ModuleAdminController`+AJAX) | `action<X>GridDefinitionModifier` + `...QueryBuilderModifier` |
| Listado propio en el BO | SI | `ModuleAdminController` + `HelperList` |
| CRUD Symfony con Grid + Form del core | **NO** | `src/` + `composer.json` + `services.yml` + `routes.yml` |
| Entidades Doctrine, CQRS propio, API Platform, comando `bin/console`, decorar un controlador, filtrar modulos por hook | **NO** | Idem |
| Modulo que debe funcionar en 8.x **y** 9.x | Obligatoriamente legacy | Nada de `src/`, `services.yml`, `PrestaShopAdminController` ni extra properties |
---

## 8. Pestana propia en el producto V2 SIN `src/`, sin Composer y sin `services.yml`

Verificado en `demoproductform` (PS 9.x) y en las fuentes de 8.2.7 / 9.1.1.

### Las tres piezas

**1. Crear la pestana** desde el hook, con el `FormType` de Symfony por FQCN (no hace
falta clase propia):

```php
public function hookActionProductFormBuilderModifier($params)
{
    if (empty($params['form_builder']) || (int) ($params['id'] ?? 0) <= 0) {
        return;
    }
    $params['form_builder']->add(
        'samestock',                                              // -> #product_samestock-tab
        'Symfony\Component\Form\Extension\Core\Type\FormType',
        array(
            'label' => 'Stock compartido',
            'mapped' => false,
            'required' => false,
            'form_theme' => '@Modules/samestock/views/templates/admin/FormTheme/tab.html.twig',
        )
    );
}
```

`EditProductFormType::getParent()` devuelve `NavigationTabType`, y
`navigation_tab_widget` (`prestashop_ui_kit_base.html.twig:1408`) convierte **todo hijo
de la raiz** en pestana. El block prefix de la raiz es `product`, asi que el id del
panel es determinista: **`#product_samestock-tab`**.

**2. El form theme del modulo.** El namespace Twig `@Modules` esta disponible sin
registrar nada (evidencia: `demoproductform/src/Form/Type/CustomTabContentType.php:49`).
El nombre del bloque es `<unique_block_prefix>_widget`; para un hijo `samestock` de la
raiz `product` es `_product_samestock_widget`:

```twig
{% extends '@PrestaShop/Admin/TwigTemplateForm/prestashop_ui_kit_base.html.twig' %}

{% block _product_samestock_widget %}
  {{ renderhook('displaySamestockProductTab', {'id_product': app.request.get('productId')}) }}
{% endblock %}
```

**3. El contenido, en PHP.** `renderhook` esta disponible en Twig, asi que el theme
puede llamar a un hook PROPIO del modulo y el HTML se genera en PHP como siempre:

```php
public function hookDisplaySamestockProductTab($params)
{
    return $this->renderProductsBlock((int) $params['id_product'])
         . $this->renderCombinationsBlock((int) $params['id_product']);
}
```

Registra `displaySamestockProductTab` como cualquier otro hook: `Hook::registerHook()`
crea la fila si el nombre no existe.

### Por que esto evita Symfony

Una clase `FormType` propia habria exigido `config/services.yml` con
`tags: [{ name: form.type }]` y `parent: 'form.type.translatable.aware'`
(`demoproductform/config/services.yml`). Usando el `FormType` generico de Symfony solo
se consigue el **contenedor** de la pestana — sin mapeo ni validacion — pero eso basta
si el modulo guarda por su cuenta desde `actionProductUpdate` leyendo el `$_POST`
crudo (patron de "inyeccion directa").

### Limitaciones

- Sin FormType propio no hay mapeo de datos ni validacion de Symfony.
- La pantalla de ALTA de producto no dispara el hook: `CreateProductFormType` usa el
  block prefix `create_product`, asi que el hook seria
  `actionCreateProductFormBuilderModifier`.
- Si el theme o el hook fallan, la pestana sale **vacia**. Conviene que el modulo
  tambien pinte en `displayAdminProductsExtra` como respaldo, o retirar la pestana.

---

## 9. Deteccion fiable de pagina de producto V1 frente a V2

**NO leer el flag `product_page_v2` de la tabla `feature_flag`.** Su columna `type`
vale `env,dotenv,db`: el valor puede venir de una variable de entorno o de `.env` y
**anular la base de datos**. Caso real: PS 8.2.0 sirviendo la V2 con la fila de la BD
a `0`.

La senal fiable es la **ruta Symfony**, que ademas PrestaShop incluye en los
parametros del hook (`'route' => 'admin_product_form'`):

| Ruta | Pagina |
|---|---|
| `admin_product_form` | clasica (V1) |
| `admin_products_edit` | nueva (V2), path `/{productId}/edit` |

```php
$route = (string) ($params['route'] ?? Tools::getValue('_route'));
if (strpos($route, 'admin_product_form') === 0) { /* V1 */ }
elseif (strpos($route, 'admin_products') === 0) { /* V2 */ }
```

Respaldos, por este orden: `_PS_VERSION_ >= 9.0.0` implica siempre V2;
`< 8.1.0` implica siempre V1; y solo como ultimo recurso, el flag en BD.

---

## 10. REGLA DE ORO: el bloque en la ficha de producto va en UN SOLO SITIO

**Verificado en produccion (PS 8.2.0). Costo 5 horas de depuracion.**

### El fallo

Un modulo pintaba su bloque en DOS sitios a la vez:

- `displayAdminProductsMainStepLeftColumnBottom` (pagina principal, `#step1`)
- `displayAdminProductsExtra` (pestana Modulos, `#hooks`)

Los dos usan los mismos `name` en los campos, asi que el POST llevaba todo repetido:

```
...&samestock_form_present=5423&samestock_add=5422&...   <- la seleccion del usuario
...&samestock_form_present=5423&samestock_add=0&...      <- la copia vacia
```

**PHP se queda SIEMPRE con el ultimo valor de un nombre repetido.** Llegaba `0` y no
se guardaba nada. El guardado funcionaba perfectamente: guardaba un cero.

Peor todavia: `displayAdminProductsExtra` se renderiza **antes** que los paneles
(`product.html.twig:33` frente a `essentials.html.twig:140`), asi que si tambien pinta
en V1, se queda el con el bloque y la pagina principal aparece vacia.

### La regla

| Pagina | Donde pintar | Que debe devolver vacio |
|---|---|---|
| V1 (PS 1.7, 8.0, y 8.1/8.2 con la V2 apagada) | `displayAdminProductsMainStepLeftColumnBottom` (Ajustes basicos) y `displayAdminProductsQuantitiesStepBottom` (Cantidades) | `displayAdminProductsExtra` |
| V2 (PS 8.1+ con la V2 activa, y unica en PS 9) | `displayAdminProductsExtra` (pestana Modulos) | los dos hooks de paneles |

Ademas de excluir los hooks entre si con la deteccion de pagina, **cada metodo de
pintado debe llevar su propio guardian estatico**:

```php
protected static $products_rendered = false;

protected function renderProductsBlock($id_product)
{
    if (self::$products_rendered) {
        return '';
    }
    self::$products_rendered = true;
    // ...
}
```

Los hooks pueden dispararse mas veces de lo previsto (multitienda, AJAX parciales,
otro modulo que reenvie el hook). El guardian es la red de seguridad.

### Guardado en cada pagina

- **V1**: los campos van dentro del `<form>` del producto y se leen con
  `Tools::getValue()` desde `hookActionProductUpdate` (patron de "inyeccion directa").
  **Funciona**: los campos SI llegan al POST. No es cierto que el JavaScript de la
  ficha los descarte — esa teoria se comprobo falsa mirando el POST real.
- **V2**: declarar los campos como campos REALES del formulario Symfony desde
  `actionProductFormBuilderModifier` (como `demo_module_custom_field` en
  `demoproductform`), y leerlos en `actionAfterUpdateProductFormHandler`, que
  PrestaShop despacha con los datos ya validados
  (`src/Core/Form/IdentifiableObject/Handler/FormHandler.php:145`: el nombre se compone
  como `'actionAfterUpdate' . camelize($form->getName()) . 'FormHandler'`, y el
  formulario de producto se llama `product`). Ningun `services.yml` necesario.

### Primer paso ante un "no guarda"

**Mirar el cuerpo del POST** (pestana Red del navegador) y buscar si los campos del
modulo aparecen repetidos. Antes de teorizar sobre hooks, tokens o JavaScript.

---

## 11. RECETA COMPLETA: pestana propia con TODO dentro en la pagina de producto V2

**Funcionando en produccion (PS 8.2.0). Sin `src/`, sin Composer, sin `services.yml`,
sin plantilla Twig propia y sin JavaScript.**

### Pieza 1 — crear la pestana y sus campos

```php
public function hookActionProductFormBuilderModifier($params)
{
    if (empty($params['form_builder']) || (int) ($params['id'] ?? 0) <= 0) {
        return;   // la pantalla de ALTA no dispara este hook (prefijo create_product)
    }
    $formType   = 'Symfony\Component\Form\Extension\Core\Type\FormType';
    $choiceType = 'Symfony\Component\Form\Extension\Core\Type\ChoiceType';
    $builder = $params['form_builder'];

    // Hijo de la RAIZ => pestana automatica (#product_mitab-tab).
    $tab = $builder->create('mitab', $formType, [
        'label'    => 'Mi pestana',
        'required' => false,
        // OJO: NADA de 'mapped' => false.  Ver mas abajo.
    ]);

    $tab->add('keep', $choiceType, [
        'choices'  => $opciones,      // ['Etiqueta' => valor, ...]
        'multiple' => true,
        'expanded' => true,           // casillas
        'required' => false,
        'data'     => $seleccionadosActuales,
    ]);
    $tab->add('add', $choiceType, ['choices' => $lista, 'required' => false, 'data' => 0]);

    $builder->add($tab);
}
```

Funciona porque `EditProductFormType::getParent()` devuelve `NavigationTabType` y el
bloque `navigation_tab_widget` convierte **todo hijo de la raiz** en pestana. El block
prefix de la raiz es `product`, asi que el id del panel es determinista.

**Los campos se pintan solos**: al ser campos reales de Symfony los renderiza
PrestaShop. No hace falta form theme — y menos aun con `@Modules`, que **no existe en
PS 8.x** (solo en 9.x).

### Pieza 2 — guardar

```php
public function hookActionAfterUpdateProductFormHandler($params)
{
    $id   = (int) $params['id'];
    $data = $params['form_data'];
    $tab  = $data['mitab'] ?? null;   // <- aqui llegan los valores
    if (!is_array($tab)) { return; }
    // $tab['keep'], $tab['add'], ...
}
```

El nombre del hook sale de
`src/Core/Form/IdentifiableObject/Handler/FormHandler.php:145`:
`'actionAfterUpdate' . camelize($form->getName()) . 'FormHandler'`, y el formulario de
producto se llama `product`. **Es un hook normal: no necesita `services.yml`.**

### LA TRAMPA: `'mapped' => false` ROMPE EL GUARDADO

Poner `'mapped' => false` en los campos parece lo natural (son datos del modulo, no del
producto) pero hace que Symfony **NO incluya el valor en `$form->getData()`**, que es
justo de donde sale `form_data`. Resultado: el hook de guardado recibe `null`, sale
antes de tocar nada, y **la pantalla dice "Actualizado correctamente" sin haber
guardado nada del modulo**.

Sintoma exacto observado: se desmarcaba una casilla, se guardaba, salia el mensaje de
exito... y al recargar la casilla volvia marcada.

**Regla: NO uses `mapped => false` en campos cuyo valor necesites leer en
`actionAfterUpdate<Form>FormHandler`.** Los datos del formulario de producto son un
array, asi que mapearlos es inofensivo: simplemente aparecen como
`$data['mitab'][...]`.

### Reparto final entre V1 y V2

| Pagina | Donde va el bloque | Que devuelve vacio |
|---|---|---|
| V1 | `displayAdminProductsMainStepLeftColumnBottom` (pagina principal) | `displayAdminProductsExtra` |
| V2 | pestana propia via `actionProductFormBuilderModifier` | `displayAdminProductsExtra` |

`displayAdminProductsExtra` (pestana Modulos) **no se usa en ninguna de las dos**:
pintar en dos sitios duplica los `name` en el POST y PHP se queda con la copia vacia.
