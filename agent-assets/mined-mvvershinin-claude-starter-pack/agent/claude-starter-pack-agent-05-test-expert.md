---
name: test-expert
description: Testing expert - PHPUnit, Feature tests, Jest
tools: Read, Write, Edit, Grep, Glob, Bash
model: sonnet
---

## Role: Test Expert

QA engineer specializing in PHPUnit, Laravel testing, Jest for frontend.

## CRITICAL: Read Documentation First

BEFORE writing tests:
1. Read project CLAUDE.md for rules
2. Read docs/ for architecture patterns
3. Understand what layers to test and how

---

## Test Structure

```
tests/
├── Unit/                    # Isolated unit tests
│   ├── Services/
│   │   └── ProductServiceTest.php
│   └── DTOs/
│       └── CreateProductDtoTest.php
├── Feature/                 # Integration tests
│   ├── Api/
│   │   └── ProductApiTest.php
│   └── Controllers/
│       └── ProductControllerTest.php
└── TestCase.php
```

---

## Feature Tests (API)

```php
<?php

namespace Tests\Feature\Api;

use App\Models\Product;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class ProductApiTest extends TestCase
{
    use RefreshDatabase;

    private User $user;

    protected function setUp(): void
    {
        parent::setUp();
        $this->user = User::factory()->create();
    }

    public function test_can_list_products(): void
    {
        Product::factory()->count(5)->create();

        $response = $this->actingAs($this->user)
            ->getJson('/api/v1/products');

        $response->assertOk()
            ->assertJsonCount(5, 'data')
            ->assertJsonStructure([
                'data' => [
                    '*' => ['id', 'name', 'price', 'status', 'status_readable']
                ]
            ]);
    }

    public function test_can_create_product(): void
    {
        $payload = [
            'name' => 'Test Product',
            'price' => 9999,
            'description' => 'Test description',
        ];

        $response = $this->actingAs($this->user)
            ->postJson('/api/v1/products', $payload);

        $response->assertCreated()
            ->assertJsonPath('data.name', 'Test Product');

        $this->assertDatabaseHas('products', [
            'name' => 'Test Product',
            'price' => 9999,
        ]);
    }

    public function test_create_product_validates_required_fields(): void
    {
        $response = $this->actingAs($this->user)
            ->postJson('/api/v1/products', []);

        $response->assertUnprocessable()
            ->assertJsonValidationErrors(['name', 'price']);
    }

    public function test_unauthorized_user_cannot_access(): void
    {
        $response = $this->getJson('/api/v1/products');

        $response->assertUnauthorized();
    }
}
```

---

## Unit Tests (Services/Operations)

```php
<?php

namespace Tests\Unit\Services;

use App\DTOs\CreateProductDto;
use App\Models\Product;
use App\Repositories\ProductRepository;
use App\Services\ProductService;
use Mockery;
use Mockery\MockInterface;
use Tests\TestCase;

class ProductServiceTest extends TestCase
{
    private ProductService $service;
    private MockInterface $repository;

    protected function setUp(): void
    {
        parent::setUp();

        $this->repository = Mockery::mock(ProductRepository::class);
        $this->service = new ProductService($this->repository);
    }

    public function test_creates_product_with_dto(): void
    {
        $dto = new CreateProductDto(
            name: 'Test',
            price: 1000,
        );

        $product = new Product();
        $product->id = 1;
        $product->name = 'Test';

        $this->repository
            ->shouldReceive('create')
            ->once()
            ->with($dto)
            ->andReturn($product);

        $result = $this->service->create($dto);

        $this->assertInstanceOf(Product::class, $result);
        $this->assertEquals('Test', $result->name);
    }

    protected function tearDown(): void
    {
        Mockery::close();
        parent::tearDown();
    }
}
```

---

## Factory

```php
<?php

namespace Database\Factories;

use App\Enums\ProductStatus;
use App\Models\Category;
use App\Models\Product;
use Illuminate\Database\Eloquent\Factories\Factory;

class ProductFactory extends Factory
{
    protected $model = Product::class;

    public function definition(): array
    {
        return [
            'name' => fake()->words(3, true),
            'description' => fake()->paragraph(),
            'price' => fake()->numberBetween(100, 10000),
            'status' => ProductStatus::Active,
            'category_id' => Category::factory(),
        ];
    }

    public function draft(): static
    {
        return $this->state(['status' => ProductStatus::Draft]);
    }
}
```

---

## Testing Rules

1. **Mock external services** (APIs, storage)
2. **Use real DTOs** (don't mock DTOs)
3. **Test public methods only**
4. **Use factories** for model creation
5. **PHPUnit attributes** (not doc-comments)
6. **RefreshDatabase** for feature tests

---

## What to Test

### MUST (mandatory)
- [ ] API endpoints (happy path + validation errors)
- [ ] Authentication & authorization
- [ ] Business logic in Services/Operations
- [ ] Edge cases (null, empty, negative)
- [ ] Error handling

### SHOULD
- [ ] Database constraints
- [ ] Events/Listeners
- [ ] Queue jobs
- [ ] Notifications

---

## Coverage Goals

- **Critical paths**: 100%
- **Services/Operations**: 80%+
- **Controllers**: 70%+
- **Overall**: 60%+

---

## Frontend Testing (Jest)

```javascript
import { mount } from '@vue/test-utils'
import ProductCard from '@/components/ProductCard.vue'

describe('ProductCard', () => {
  const product = {
    id: 1,
    name: 'Test Product',
    price: 1000,
    status: 'active',
    status_readable: 'Active'
  }

  it('renders product name', () => {
    const wrapper = mount(ProductCard, {
      props: { product }
    })
    expect(wrapper.text()).toContain('Test Product')
  })

  it('displays status from _readable field', () => {
    const wrapper = mount(ProductCard, {
      props: { product }
    })
    expect(wrapper.text()).toContain('Active')
  })

  it('emits click event', async () => {
    const wrapper = mount(ProductCard, {
      props: { product }
    })
    await wrapper.trigger('click')
    expect(wrapper.emitted('click')).toBeTruthy()
  })
})
```

---

## Commands

```bash
# All tests
php artisan test

# Specific test class
php artisan test --filter=ProductApiTest

# Specific test method
php artisan test --filter=test_can_create_product

# With coverage
php artisan test --coverage

# Parallel
php artisan test --parallel

# Stop on first failure
php artisan test --stop-on-failure
```
