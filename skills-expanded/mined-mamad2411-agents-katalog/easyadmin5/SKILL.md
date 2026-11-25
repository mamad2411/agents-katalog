# EasyAdmin 5 — Quick Reference for Symfony Projects

Version: 5.0.2+ (March 2026)
Bundle: `easycorp/easyadmin-bundle`

This skill is a verified reference extracted from official documentation.
**Always consult this before writing any EasyAdmin code.**

Sources:
- https://symfony.com/bundles/EasyAdminBundle/current/index.html
- https://github.com/EasyCorp/EasyAdminBundle/blob/5.x/UPGRADE.md

---

## Breaking Changes from EasyAdmin 4

| EasyAdmin 4 | EasyAdmin 5 |
|---|---|
| `MenuItem::linkToCrud(label, icon, Entity::class)` | `MenuItem::linkTo(Controller::class, label, icon)` |
| `FormField::addPanel('Title')` | `FormField::addFieldset('Title')` |
| `->displayAsLink()` | `->renderAsLink()` |
| `->displayAsButton()` | `->renderAsButton()` |
| `->displayAsForm()` | `->renderAsForm()` |
| `{{ ea.property }}` in Twig | `{{ ea().property }}` (function call) |
| `AdminContext::getReferrer()` | `getRequest()->headers->get('referer')` |
| `AdminContext::getSignedUrls()` | Removed |
| `getCrudControllers()` | `getAdminControllers()` |
| Pretty URLs optional | Pretty URLs mandatory (only format) |
| `BatchActionDto::referrerUrl` / `getReferrerUrl()` | Removed |
| `AdminUrlGenerator::removeReferrer()` | Removed (EA5 does not append `referrer` to URLs) |
| `MenuItemMatcherInterface::isSelected()/isExpanded()` | Methods removed; use `markSelectedMenuItem()` instead |
| `createEntity()` returns untyped | Must return `object` |
| `#[Route]` on dashboard `index()` | `#[AdminDashboard]` attribute on class |
| `AdminContextProvider::hasContext()` | Removed; check `getContext() !== null` |
| `AdminRouteGenerator::usesPrettyUrls()` | Deprecated (always returns `true`; removed from interface) |
| PHP 8.1 minimum | PHP 8.2+ required |
| Symfony 5.4 supported | Symfony 6.4+ required |

### Required route config (mandatory in 5.x)

```yaml
# config/routes/easyadmin.yaml
easyadmin:
    resource: .
    type: easyadmin.routes
```

### PHPStan generic type (if using static analysis)

```php
/** @extends AbstractCrudController<Product> */
class ProductCrudController extends AbstractCrudController
```

---

## Dashboard Controller

```php
use EasyCorp\Bundle\EasyAdminBundle\Attribute\AdminDashboard;
use EasyCorp\Bundle\EasyAdminBundle\Config\Dashboard;
use EasyCorp\Bundle\EasyAdminBundle\Config\MenuItem;
use EasyCorp\Bundle\EasyAdminBundle\Config\Assets;
use EasyCorp\Bundle\EasyAdminBundle\Controller\AbstractDashboardController;

#[AdminDashboard(routePath: '/admin', routeName: 'app_admin')]
class DashboardController extends AbstractDashboardController
{
    public function index(): Response
    {
        // Option A: redirect to a CRUD controller
        $url = $this->container->get(AdminUrlGenerator::class)
            ->setController(ProductCrudController::class)
            ->generateUrl();
        return $this->redirect($url);

        // Option B: render custom template
        return $this->render('admin/dashboard.html.twig');

        // Option C: default EasyAdmin dashboard
        return parent::index();
    }

    public function configureDashboard(): Dashboard
    {
        return Dashboard::new()
            ->setTitle('My App')
            ->setFaviconPath('favicon.svg')
            ->renderContentMaximized()              // full width
            ->renderSidebarMinimized()              // narrow sidebar
            ->disableDarkMode()
            ->setDefaultColorScheme('light')         // 'light', 'dark', 'auto'
            ->setTranslationDomain('admin')
            ->generateRelativeUrls()
            ->setLocales(['en' => 'English', 'es' => 'Español'])
            ->setTextDirection('ltr')                // 'ltr' or 'rtl'
            ->useEntityTranslations();               // auto translation keys for entities
    }

    // Global CRUD defaults (applies to ALL crud controllers under this dashboard)
    public function configureCrud(): Crud
    {
        return Crud::new()
            ->setDateFormat('dd/MM/yyyy')
            ->setTimeFormat('HH:mm')
            ->setPaginatorPageSize(25);
    }
}
```

### Multiple Dashboards

Each dashboard is a separate controller with its own `#[AdminDashboard]`:

```php
#[AdminDashboard(routePath: '/admin', routeName: 'app_admin')]
class MainDashboardController extends AbstractDashboardController { ... }

#[AdminDashboard(
    routePath: '/manager',
    routeName: 'app_manager',
    allowedControllers: [OrderCrudController::class, InvoiceCrudController::class],
)]
class ManagerDashboardController extends AbstractDashboardController { ... }
```

Use `allowedControllers` or `deniedControllers` to restrict which CRUD controllers appear.

Full `#[AdminDashboard]` parameters: `routePath`, `routeName`, `allowedControllers`, `deniedControllers`, `routes`, `routeOptions`.

When generating URLs from outside EA context, specify the dashboard:

```php
$url = $this->container->get(AdminUrlGenerator::class)
    ->setDashboard(ManagerDashboardController::class)
    ->setController(OrderCrudController::class)
    ->generateUrl();
```

---

## MenuItem API (complete)

```php
// Link to dashboard
MenuItem::linkToDashboard(TranslatableInterface|string $label, ?string $icon = null)

// Link to a CRUD controller (REPLACES linkToCrud from v4)
MenuItem::linkTo(string $controllerFqcn, TranslatableInterface|string|null $label = null, ?string $icon = null)
    ->setAction(string $action)         // e.g. Action::NEW
    ->setEntityId(AbstractUid|int|string $entityId)
    ->setDefaultSort(['field' => 'DESC'])
    ->setHtmlAttribute(string $name, mixed $value)  // only on ControllerMenuItem

// Link to a Symfony route
MenuItem::linkToRoute(TranslatableInterface|string $label, ?string $icon, string $routeName, array $routeParameters = [])

// Link to external URL
MenuItem::linkToUrl(TranslatableInterface|string $label, ?string $icon, string $url)

// Visual separator
MenuItem::section(TranslatableInterface|string|null $label = null, ?string $icon = null)

// Dropdown submenu (max 2 levels)
MenuItem::subMenu(TranslatableInterface|string $label, ?string $icon = null)
    ->setSubItems(array $items)

// Logout
MenuItem::linkToLogout(TranslatableInterface|string $label, ?string $icon = null)

// Exit impersonation
MenuItem::linkToExitImpersonation(TranslatableInterface|string $label, ?string $icon = null)
```

### Common methods on all MenuItems

```php
->setCssClass(string $cssClass)
->setLinkRel(string $rel)
->setLinkTarget(string $target)             // '_blank', '_self'
->setPermission(string|Expression $permission)  // 'ROLE_ADMIN' or Expression object
->setBadge(\Stringable|string|int|float|bool|null $content, string $style = 'secondary', array $htmlAttributes = [])
->setQueryParameter(string $name, mixed $value)
->setTranslationParameters(array $parameters)
```

Note: `setLinkRel()` and `setLinkTarget()` are not available on `SubMenuItem`.

### Menu example (submenus)

```php
public function configureMenuItems(): iterable
{
    yield MenuItem::linkToDashboard('Dashboard', 'fa fa-home');

    yield MenuItem::subMenu('CRM', 'fa-solid fa-users-gear')->setSubItems([
        MenuItem::linkTo(CompanyCrudController::class, 'Companies', 'fas fa-building'),
        MenuItem::linkTo(UserCrudController::class, 'Users', 'fas fa-user'),
    ]);

    yield MenuItem::subMenu('Monitoring', 'fa fa-chart-line')->setSubItems([
        MenuItem::linkTo(LogCrudController::class, 'Logs', 'fa fa-list'),
    ]);
}
```

---

## CRUD Controller

```php
use EasyCorp\Bundle\EasyAdminBundle\Controller\AbstractCrudController;
use EasyCorp\Bundle\EasyAdminBundle\Config\Crud;
use EasyCorp\Bundle\EasyAdminBundle\Config\Action;
use EasyCorp\Bundle\EasyAdminBundle\Config\Actions;

class ProductCrudController extends AbstractCrudController
{
    public static function getEntityFqcn(): string
    {
        return Product::class;
    }

    public function configureCrud(Crud $crud): Crud
    {
        return $crud
            ->setEntityLabelInSingular('Product')
            ->setEntityLabelInPlural('Products')
            ->setDefaultSort(['id' => 'DESC'])
            ->setSearchFields(['name', 'description', 'seller.email'])  // dot notation for associations
            ->setSearchMode(SearchMode::ALL_TERMS)    // or SearchMode::ANY_TERMS
            ->setAutofocusSearch()
            ->setPaginatorPageSize(30)
            ->setPaginatorRangeSize(5)                 // 0 = simple prev/next
            ->setPaginatorUseOutputWalkers(true)
            ->setPaginatorFetchJoinCollection(true)
            ->renderContentMaximized()
            ->setEntityPermission('ROLE_EDITOR')
            ->hideNullValues()                         // hide null values on detail page
            ->setPageTitle(Crud::PAGE_INDEX, 'Products')
            ->setPageTitle(Crud::PAGE_DETAIL, fn(Product $p) => $p->getName())
            ->setHelp(Crud::PAGE_INDEX, 'Manage your product catalog')
            ->setDefaultRowAction(Action::DETAIL)      // click row to open detail
            ->showEntityActionsInlined()               // actions as icons, not dropdown
            ->setDateFormat('dd/MM/yyyy')
            ->setTimeFormat('HH:mm')
            ->setNumberFormat('%.2d')
            ->setThousandsSeparator('.')
            ->setDecimalSeparator(',')
            ->overrideTemplate('crud/index', 'admin/product/index.html.twig')
            ->setFormOptions(
                ['validation_groups' => ['Default', 'create']],  // new form
                ['validation_groups' => ['Default', 'edit']],    // edit form
            );
    }

    public function configureActions(Actions $actions): Actions
    {
        return $actions
            ->add(Crud::PAGE_INDEX, Action::DETAIL);
    }

    public function configureFields(string $pageName): iterable
    {
        // See Fields section below
    }
}
```

### Entity persistence overrides

```php
public function createEntity(string $entityFqcn): object
{
    $entity = new Product();
    $entity->setCreatedBy($this->getUser());
    return $entity;
}

public function persistEntity(EntityManagerInterface $em, object $entityInstance): void
{
    parent::persistEntity($em, $entityInstance);
}

public function updateEntity(EntityManagerInterface $em, object $entityInstance): void
{
    parent::updateEntity($em, $entityInstance);
}

public function deleteEntity(EntityManagerInterface $em, object $entityInstance): void
{
    parent::deleteEntity($em, $entityInstance);
}
```

### Query builder override

```php
public function createIndexQueryBuilder(
    SearchDto $searchDto,
    EntityDto $entityDto,
    FieldCollection $fields,
    FilterCollection $filters,
): QueryBuilder {
    $qb = parent::createIndexQueryBuilder($searchDto, $entityDto, $fields, $filters);
    $qb->andWhere('entity.isActive = :active')->setParameter('active', true);
    return $qb;
}
```

### Response parameters override

```php
public function configureResponseParameters(KeyValueStore $responseParameters): KeyValueStore
{
    if (Crud::PAGE_INDEX === $responseParameters->get('pageName')) {
        $responseParameters->set('custom_var', 'value');
    }
    return $responseParameters;
}
```

---

## Fields (30 built-in types)

ArrayField, AssociationField, AvatarField, BooleanField, ChoiceField,
CodeEditorField, CollectionField, ColorField, CountryField, CurrencyField,
DateField, DateTimeField, EmailField, HiddenField, IdField, ImageField,
IntegerField, LanguageField, LocaleField, MoneyField, NumberField,
PercentField, SlugField, TelephoneField, TextareaField, TextEditorField,
TextField, TimeField, TimezoneField, UrlField.

### Common field methods

```php
->hideOnIndex() / ->hideOnDetail() / ->hideOnForm()
->hideWhenCreating() / ->hideWhenUpdating()
->onlyOnIndex() / ->onlyOnDetail() / ->onlyOnForms()
->onlyWhenCreating() / ->onlyWhenUpdating()
->setColumns(6)                              // Bootstrap grid width
->setColumns('col-sm-6 col-lg-4')           // Responsive
->setLabel('Custom Label')
->setHelp('Help text')
->setSortable(false)
->setPermission('ROLE_ADMIN')
->setFormType(TextType::class)
->setFormTypeOptions(['attr' => ['placeholder' => '...']])
->setTemplatePath('admin/field/custom.html.twig')
->addCssClass('text-bold')
->setCssClass('text-bold')                   // replaces existing classes
->setTextAlign('right')                      // 'left', 'center', 'right'
->formatValue(fn($value, $entity) => '...')
->setEmptyData('')                           // default value when field is empty
->setHtmlAttribute('data-x', 'y')
->setHtmlAttributes(['data-x' => 'y'])
->addFormTheme('admin/form/custom_theme.html.twig')
->addCssFiles(Asset::new('css/field.css')->onlyOnForms())
->addJsFiles(Asset::new('js/field.js')->onlyOnIndex())
```

### Layout fields (FormField)

```php
FormField::addTab('Tab Label')->setIcon('fas fa-icon')
FormField::addColumn(8)                      // or 'col-lg-8 col-xl-6'
FormField::addFieldset('Title')              // replaces addPanel() from v4
    ->collapsible()
    ->renderCollapsed()
FormField::addRow()                          // force new row
```

### AssociationField

```php
AssociationField::new('category')
    ->autocomplete()                         // AJAX autocomplete (recommended for large datasets)
    ->renderAsNativeWidget()                 // standard <select> without JS
    ->renderAsEmbeddedForm()                 // inline form for the related entity
    ->setCrudController(CategoryCrudController::class)  // which CRUD to use
    ->setQueryBuilder(fn(QueryBuilder $qb) => $qb->andWhere('entity.isActive = true'))
    ->setSortProperty('name')                // sort options by this field
    ->setFormTypeOption('by_reference', false)  // for collections (ManyToMany)
    ->setPreferredChoices(fn() => [...])      // items shown first in dropdown
    ->renderAsHtml()                         // render HTML in association labels
```

### BooleanField

```php
BooleanField::new('isActive')
    ->renderAsSwitch(false)                  // render as Yes/No text instead of toggle
    ->hideValueWhenFalse()                   // show nothing when false
    ->hideValueWhenTrue()                    // show nothing when true
```

### ChoiceField

```php
ChoiceField::new('status')
    ->setChoices([
        'Draft' => 'draft',
        'Published' => 'published',
    ])
    ->setChoices(StatusEnum::cases())         // PHP enum support
    ->setTranslatableChoices([
        'status.draft' => 'draft',
        'status.published' => 'published',
    ])
    ->allowMultipleChoices()                 // multiple selection
    ->renderExpanded()                       // radio buttons / checkboxes
    ->renderAsBadges()                       // colored badges on index/detail
    ->renderAsNativeWidget()                 // standard <select>
    ->autocomplete()                         // searchable dropdown
    ->setPreferredChoices(['draft'])          // items shown first in dropdown
    ->escapeHtml(false)                      // allow HTML in labels
```

### CollectionField

```php
CollectionField::new('tags')
    ->setEntryType(TagType::class)           // Symfony form type for each entry
    ->useEntryCrudForm(TagCrudController::class)  // use a CRUD form for each entry
    ->allowAdd()                             // show "Add" button (default: true)
    ->allowDelete()                          // show "Delete" button (default: true)
    ->setEntryIsComplex(true)                // for complex embedded forms
    ->renderExpanded()                       // show all entries (not collapsed)
    ->showEntryLabel(false)                  // hide entry labels
    ->setEntryToStringMethod('getName')      // method to display entry label
```

### ImageField

```php
ImageField::new('photo')
    ->setBasePath('uploads/photos')          // public path for display
    ->setUploadDir('public/uploads/photos')  // filesystem path for upload
    ->setUploadedFileNamePattern('[year]/[month]/[slug]-[contenthash].[extension]')
    // Tokens: [year], [month], [day], [name], [slug], [contenthash], [uuid], [ulid], [randomhash], [timestamp], [extension]
    ->setFileConstraints(new File(maxSize: '2M', mimeTypes: ['image/jpeg', 'image/png']))
```

### MoneyField

```php
MoneyField::new('price')
    ->setCurrency('EUR')
    ->setCurrencyPropertyPath('currency')     // read currency from entity property
    ->setStoredAsCents(true)                  // value in DB is cents (default: true)
    ->setNumDecimals(2)
```

### SlugField

```php
SlugField::new('slug')
    ->setTargetFieldName('title')             // auto-generate from this field
    ->setTargetFieldName(['title', 'id'])     // or from multiple fields
    ->setUnlockConfirmationMessage('Changing the slug may break existing URLs')
```

### TextEditorField

```php
TextEditorField::new('content')
    ->setNumOfRows(10)                        // editor height
    ->setTrixEditorConfig([...])              // Trix editor configuration
    // Note: uses the Trix editor (by Basecamp), NOT TinyMCE
```

---

## Actions API

### Built-in action names

```php
Action::INDEX, Action::DETAIL, Action::NEW, Action::EDIT,
Action::DELETE, Action::BATCH_DELETE,
Action::SAVE_AND_RETURN, Action::SAVE_AND_CONTINUE,
Action::SAVE_AND_ADD_ANOTHER
```

### Configuring actions

```php
public function configureActions(Actions $actions): Actions
{
    return $actions
        // Add actions to pages
        ->add(Crud::PAGE_INDEX, Action::DETAIL)

        // Remove/disable built-in actions
        ->disable(Action::DELETE)

        // Update built-in actions
        ->update(Crud::PAGE_INDEX, Action::EDIT, fn(Action $a) => $a->setLabel('Modify'))

        // Reorder actions on a page
        ->reorder(Crud::PAGE_INDEX, [Action::DETAIL, Action::EDIT, Action::DELETE])

        // Set permissions (on Actions, NOT on individual Action objects)
        ->setPermission(Action::DELETE, 'ROLE_SUPER_ADMIN')
        ->setPermission('review', 'ROLE_REVIEWER');
}
```

### Custom actions

```php
$reviewAction = Action::new('review', 'Review', 'fa fa-eye')
    ->linkToCrudAction('reviewProduct')         // method in this controller
    ->linkToRoute('app_review', fn(Product $p) => ['id' => $p->getId()])  // closure for dynamic params
    ->linkToUrl('https://...')                   // or external URL
    ->setCssClass('btn btn-primary')
    ->setIcon('fa fa-check')
    ->displayIf(fn(Product $p) => !$p->isReviewed())
    ->askConfirmation('Are you sure you want to review %entity_name% #%entity_id%?')  // placeholders: %entity_name%, %entity_id%, %action_name%
    ->renderAsButton()                          // NOT displayAsButton (v4)
    ->asPrimaryAction()                         // or asWarningAction(), asDangerAction()
    ->createAsGlobalAction();                   // for index page header
```

### Action styling variants

```php
->asPrimaryAction()   ->asDefaultAction()   ->asSuccessAction()
->asWarningAction()   ->asDangerAction()
->renderAsLink()      ->renderAsButton()    ->renderAsForm()    ->asTextLink()
```

### Action Groups (dropdown grouping)

```php
$actionGroup = ActionGroup::new('actions', 'Actions', 'fa fa-ellipsis-v')  // name, label, icon
    ->addMainAction(Action::new('approve', 'Approve')->linkToCrudAction('approve'))
    ->addAction(Action::new('archive', 'Archive')->linkToCrudAction('archive'))
    ->addHeader('Danger zone')
    ->addDivider()
    ->addAction(Action::new('delete', 'Delete')->linkToCrudAction('softDelete'))
    ->displayIf(fn(?EntityDto $entityDto) => $entityDto?->getInstance()->isPublished())
    ->createAsGlobalActionGroup();            // for index page header
```

---

## Batch Actions

```php
public function configureActions(Actions $actions): Actions
{
    $exportAction = Action::new('export', 'Export Selected')
        ->linkToCrudAction('exportBatch')
        ->createAsBatchAction();              // appears when rows are selected

    return $actions
        ->add(Crud::PAGE_INDEX, $exportAction);
}

public function exportBatch(BatchActionDto $batchActionDto): Response
{
    $entityIds = $batchActionDto->getEntityIds();
    // ... process selected entities
    // Note: getReferrerUrl() was removed in v5. Use AdminUrlGenerator to redirect back.
    $url = $this->container->get(AdminUrlGenerator::class)
        ->setController(static::class)
        ->setAction(Action::INDEX)
        ->generateUrl();
    return $this->redirect($url);
}
```

Batch action confirmation:

```php
public function configureCrud(Crud $crud): Crud
{
    return $crud
        ->askConfirmationOnBatchActions(false)              // disable confirmation
        ->askConfirmationOnBatchActions('Custom message')   // custom message (supports %action_name%, %num_items%);
```

---

## Filters

```php
use EasyCorp\Bundle\EasyAdminBundle\Config\Filters;

public function configureFilters(Filters $filters): Filters
{
    return $filters
        ->add('name')                         // auto-detect filter type from Doctrine metadata
        ->add(EntityFilter::new('category'))  // explicit filter type
        ->add(ChoiceFilter::new('status')->setChoices([
            'Published' => 'published',
            'Draft' => 'draft',
        ]))
        ->add(DateTimeFilter::new('createdAt'))
        ->add(BooleanFilter::new('isActive'))
        ->add(NumericFilter::new('price'))
        ->add(NullFilter::new('deletedAt'));
}
```

### Built-in filter types (14)

ArrayFilter, BooleanFilter, ChoiceFilter, ComparisonFilter,
CountryFilter, CurrencyFilter, DateTimeFilter, EntityFilter,
LanguageFilter, LocaleFilter, NullFilter, NumericFilter,
TextFilter, TimezoneFilter.

### Custom filter

```php
class ActiveFilter implements FilterInterface
{
    use FilterTrait;

    public static function new(string $propertyName, string $label = null): self
    {
        return (new self())
            ->setFilterFqcn(__CLASS__)
            ->setProperty($propertyName)
            ->setLabel($label ?? 'Active');
    }

    public function apply(QueryBuilder $qb, FilterDataDto $filterDataDto, ?FieldDto $fieldDto, EntityDto $entityDto): void
    {
        $qb->andWhere(sprintf('%s.%s = :active', $filterDataDto->getEntityAlias(), $filterDataDto->getProperty()))
           ->setParameter('active', $filterDataDto->getValue());
    }
}
```

### Unmapped filters

Filters can apply to properties that don't exist on the entity (virtual/computed):

```php
$filters->add(TextFilter::new('custom')->setFormTypeOption('mapped', false));
```

---

## Security

### Controller-level

```php
#[AdminDashboard(
    routePath: '/admin',
    allowedControllers: [ProductCrudController::class, OrderCrudController::class],
    deniedControllers: [SecretCrudController::class],
)]
```

Or via `security.yaml`:

```yaml
security:
    access_control:
        - { path: ^/admin, roles: ROLE_ADMIN }
```

### Action-level permissions

```php
public function configureActions(Actions $actions): Actions
{
    return $actions
        ->setPermission(Action::DELETE, 'ROLE_SUPER_ADMIN')
        ->setPermission(Action::NEW, 'ROLE_EDITOR');
}
```

### Field-level permissions

```php
TextField::new('internalNotes')->setPermission('ROLE_ADMIN')
```

### Entity-level permissions

```php
public function configureCrud(Crud $crud): Crud
{
    return $crud->setEntityPermission('ROLE_EDITOR');
}
```

---

## Events

### Entity lifecycle events

```php
use EasyCorp\Bundle\EasyAdminBundle\Event\BeforeEntityPersistedEvent;
use EasyCorp\Bundle\EasyAdminBundle\Event\AfterEntityPersistedEvent;
use EasyCorp\Bundle\EasyAdminBundle\Event\BeforeEntityUpdatedEvent;
use EasyCorp\Bundle\EasyAdminBundle\Event\AfterEntityUpdatedEvent;
use EasyCorp\Bundle\EasyAdminBundle\Event\BeforeEntityDeletedEvent;
use EasyCorp\Bundle\EasyAdminBundle\Event\AfterEntityDeletedEvent;
use EasyCorp\Bundle\EasyAdminBundle\Event\AfterEntityBuiltEvent;

class ProductEventSubscriber implements EventSubscriberInterface
{
    public static function getSubscribedEvents(): array
    {
        return [
            BeforeEntityPersistedEvent::class => 'onBeforePersist',
            AfterEntityUpdatedEvent::class => 'onAfterUpdate',
        ];
    }

    public function onBeforePersist(BeforeEntityPersistedEvent $event): void
    {
        $entity = $event->getEntityInstance();
        if (!$entity instanceof Product) {
            return;
        }
        $entity->setCreatedAt(new \DateTimeImmutable());
    }
}
```

### CRUD action events

```php
use EasyCorp\Bundle\EasyAdminBundle\Event\BeforeCrudActionEvent;
use EasyCorp\Bundle\EasyAdminBundle\Event\AfterCrudActionEvent;
```

### JavaScript events

```javascript
// Available in EA5 Twig templates
document.addEventListener('ea.form.submit', (event) => { ... });
document.addEventListener('ea.form.error', (event) => { ... });
document.addEventListener('ea.collection.item-added', (event) => { ... });
document.addEventListener('ea.collection.item-removed', (event) => { ... });
// Symfony UX Autocomplete events (used by AssociationField with autocomplete)
document.addEventListener('autocomplete:pre-connect', (event) => { ... });
document.addEventListener('autocomplete:connect', (event) => { ... });
```

---

## Pretty URLs (mandatory in v5)

Default routes for each CRUD controller:

| Action | Default path | Default name |
|---|---|---|
| index | `/<controller>/` | `<routeName>_<entity>_index` |
| new | `/<controller>/new` | `<routeName>_<entity>_new` |
| detail | `/<controller>/{entityId}` | `<routeName>_<entity>_detail` |
| edit | `/<controller>/{entityId}/edit` | `<routeName>_<entity>_edit` |
| delete | `/<controller>/{entityId}/delete` | `<routeName>_<entity>_delete` |
| batch_delete | `/<controller>/batch-delete` | `<routeName>_<entity>_batch_delete` |
| autocomplete | `/<controller>/autocomplete` | `<routeName>_<entity>_autocomplete` |
| render_filters | `/<controller>/render-filters` | `<routeName>_<entity>_render_filters` |

`<routeName>` is the `routeName` from `#[AdminDashboard]` (mandatory, no default — e.g. `app_admin`).

### Custom routes per action

`#[AdminRoute]` can be applied to individual action methods or to the class (repeatable):

```php
use EasyCorp\Bundle\EasyAdminBundle\Attribute\AdminRoute;

class ProductCrudController extends AbstractCrudController
{
    #[AdminRoute(path: '/products/{entityId}/edit', name: 'admin_product_edit')]
    public function edit(AdminContext $context): KeyValueStore|Response
    {
        return parent::edit($context);
    }
}
```

### Custom routes via dashboard

```php
#[AdminDashboard(routes: [
    'index' => ['routePath' => '/all', 'routeName' => 'list'],
    'new' => ['routePath' => '/create', 'routeName' => 'create'],
])]
```

---

## Design Customization

### Custom CSS via configureAssets()

```php
public function configureAssets(): Assets
{
    return Assets::new()
        ->addCssFile('css/admin.css')
        ->addCssFile(Asset::new('css/detail.css')->onlyOnDetail())
        ->addJsFile('js/admin.js')
        ->addJsFile(Asset::new('js/form.js')->defer()->onlyOnForms())
        ->addAssetMapperEntry('admin')
        ->addWebpackEncoreEntry('admin-app')
        ->addHtmlContentToHead('<meta name="robots" content="noindex">')
        ->addHtmlContentToBody('<div id="modal-container"></div>');
}
```

### CSS Variables (override in custom CSS)

```css
:root {
    --body-max-width: 100%;
    --body-bg: #f5f5f5;
    --font-size-base: 13px;
    --border-radius: 0px;
}
```

### Template overrides

Place in `templates/bundles/EasyAdminBundle/`:

```twig
{# templates/bundles/EasyAdminBundle/layout.html.twig #}
{% extends '@!EasyAdmin/layout.html.twig' %}

{% block sidebar %}
    {# custom sidebar #}
{% endblock %}
```

Per-CRUD template override (in controller):

```php
public function configureCrud(Crud $crud): Crud
{
    return $crud
        ->overrideTemplate('crud/index', 'admin/product/index.html.twig')
        ->overrideTemplates([
            'crud/detail' => 'admin/product/detail.html.twig',
            'crud/edit' => 'admin/product/edit.html.twig',
        ]);
}
```

### Body CSS selectors (per-page styling)

| Page | body id | body class |
|---|---|---|
| index | `ea-index-Product` | `ea-index ea-index-Product` |
| detail | `ea-detail-Product-42` | `ea-detail ea-detail-Product` |
| edit | `ea-edit-Product-42` | `ea-edit ea-edit-Product` |
| new | `ea-new-Product` | `ea-new ea-new-Product` |

### Dark mode

EA5 supports dark mode via `data-bs-theme` attribute. CSS classes `.light-theme` / `.dark-theme` are available for conditional styling.

---

## User Menu

```php
public function configureUserMenu(UserInterface $user): UserMenu
{
    return parent::configureUserMenu($user)
        ->setName($user->getFullName())
        ->setAvatarUrl($user->getAvatarUrl())
        ->setGravatarEmail($user->getEmail())
        ->displayUserName(false)                 // hide username in top bar
        ->displayUserAvatar(false)               // hide avatar in top bar
        ->addMenuItems([
            MenuItem::linkToRoute('My Profile', 'fa fa-id-card', 'user_profile'),
            MenuItem::section(),
            MenuItem::linkToLogout('Logout', 'fa fa-sign-out'),
        ]);
}
```

---

## URL Generation

### In a controller

```php
use EasyCorp\Bundle\EasyAdminBundle\Router\AdminUrlGenerator;

$url = $this->container->get(AdminUrlGenerator::class)
    ->setController(ProductCrudController::class)
    ->setAction(Action::EDIT)
    ->setEntityId($product->getId())
    ->generateUrl();

// Additional methods
$urlGenerator->set('custom_param', 'value');
$urlGenerator->unset('custom_param');
$urlGenerator->unsetAll();
$urlGenerator->setDashboard(ManagerDashboardController::class);
```

Note: `AdminUrlGenerator::removeReferrer()` was removed in v5. The generated URL no longer carries a `referrer` query parameter, so no replacement is needed — just drop the call from any migrated EA4 code.

### In Twig

```twig
{# ea_url() = AdminUrlGenerator (URL building) #}
{% set url = ea_url()
    .setController('App\\Controller\\Admin\\ProductCrudController')
    .setAction('edit')
    .setEntityId(product.id) %}

{# ea() = AdminContext (current request context) #}
{% set dashboardTitle = ea().dashboardTitle %}
{% set currentAction = ea().crud.currentAction %}
```

Note: `ea_url()` and `ea()` are different functions. `ea_url()` generates URLs. `ea()` accesses the current `AdminContext`.

---

## Notes

- **Export (CSV/Excel)** is NOT a native EA5 feature. Use third-party bundles if needed.
- **Search** is per-CRUD controller, not global. Users can quote terms for exact match.
- **Trix editor** is used by TextEditorField (not TinyMCE).
