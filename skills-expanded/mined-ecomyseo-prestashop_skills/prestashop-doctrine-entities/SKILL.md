---
name: prestashop-doctrine-entities
description: Skill for using Doctrine ORM in PrestaShop modules for modern data persistence in PS 8 and 9.
---

# PrestaShop Doctrine Entities Skill

This skill explains how to define, manage, and query data using Doctrine ORM within PrestaShop modules.

## 1. Technical Guide

### Defining an Entity
Entities should be placed in `src/Entity/`. Use annotations (or attributes in PHP 8+) to map them.

```php
namespace MyModule\Entity;

use Doctrine\ORM\Mapping as ORM;

/**
 * @ORM\Table()
 * @ORM\Entity(repositoryClass="MyModule\Repository\MyEntityRepository")
 */
class MyEntity
{
    /**
     * @ORM\Id
     * @ORM\Column(name="id_my_entity", type="integer")
     * @ORM\GeneratedValue(strategy="AUTO")
     */
    private $id;

    /**
     * @ORM\Column(name="name", type="string", length=255)
     */
    private $name;

    // Getters and Setters...
}
```

### Accessing the Entity Manager
In a Symfony controller:
```php
$entityManager = $this->get('doctrine.orm.entity_manager');
$myEntity = new MyEntity();
$myEntity->setName('Example');
$entityManager->persist($myEntity);
$entityManager->flush();
```

### Translatable Entities
For multi-language support, create a secondary entity (e.g., `MyEntityLang`) and link them with `OneToMany`.

## 2. Professional Development Guide

### Schema Management
Unlike `ObjectModel`, Doctrine entities require explicit schema management. You can use the `SchemaTool` in your module's install/uninstall methods.

```php
private function installEntities()
{
    $entityManager = $this->container->get('doctrine.orm.entity_manager');
    $schemaTool = new \Doctrine\ORM\Tools\SchemaTool($entityManager);
    $schemaTool->createSchema([
        $entityManager->getClassMetadata(\MyModule\Entity\MyEntity::class),
        $entityManager->getClassMetadata(\MyModule\Entity\MyEntityLang::class),
    ]);
}
```

### Repository Pattern
Always use repositories for custom queries to keep your entities clean.

```php
namespace MyModule\Repository;

use Doctrine\ORM\EntityRepository;

class MyEntityRepository extends EntityRepository
{
    public function findAllByName(string $name)
    {
        return $this->findBy(['name' => $name]);
    }
}
```

## 3. User Guide

### Advantages
- **Type Safety**: Better IDE support and less runtime errors.
- **Complexity**: Handles relationships (OneToMany, ManyToMany) much better than `ObjectModel`.
- **Portability**: Standard Symfony practice.

## Rules & Best Practices
- **Namespace**: Ensure your namespace matches the module directory to avoid autoloading issues.
- **Prefixes**: PrestaShop tables are prefixed automatically if using standard Doctrine configuration in PS.
- **Lifecycle Callbacks**: Use `@ORM\HasLifecycleCallbacks` for things like `date_add` and `date_upd`.
