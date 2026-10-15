---
name: codeigniter
description: "Use when working with CodeIgniter 3 or CodeIgniter 4 applications — controllers, models, views, routing, database queries, migrations, libraries, helpers, security, file uploads, email, caching, testing, services, events, CLI commands, and deployment. Trigger on: CI3 projects with system/core/CodeIgniter.php or index.php bootstrapping CI, CI4 projects with app/Config/App.php or spark CLI, any mention of CodeIgniter, HMVC in CI3, Shield auth in CI4, CI query builder usage, or 'php spark' commands."
license: MIT
metadata:
  author: yasserstudio
  version: "1.0.0"
---

# CodeIgniter Development

You are a CodeIgniter expert. You work with both CI3 (3.1.x) and CI4 (4.x, latest stable 4.7.x) and understand their fundamental architectural differences. Always identify which version the project uses before writing any code.

For deep dives on version-specific features, see:
- [CI3 deep dive](references/ci3.md) — file uploads, email, caching, pagination, libraries, HMVC, hooks, helpers, logging
- [CI4 deep dive](references/ci4.md) — REST controllers, entities, filters, migrations, seeders, uploads, email, caching, services, events, views, cells, Spark CLI, testing, Shield auth, content negotiation
- [Deployment & migration](references/deployment.md) — server config, production checklist, full CI3→CI4 migration table

## Version Detection

| Signal | Version |
|--------|---------|
| `system/core/CodeIgniter.php` exists | CI3 |
| `$this->load->model()` / `$this->load->view()` | CI3 |
| `application/config/config.php` | CI3 |
| `app/Config/App.php` exists | CI4 |
| `namespace App\Controllers;` in controllers | CI4 |
| `spark` CLI at project root | CI4 |
| `composer.json` requires `codeigniter4/framework` | CI4 |

---

## CI3 — Core Patterns

### Project Structure

```
project/
├── application/
│   ├── config/        # autoload.php, config.php, database.php, routes.php, hooks.php
│   ├── controllers/
│   ├── models/
│   ├── views/
│   ├── libraries/
│   ├── helpers/
│   ├── hooks/
│   ├── core/          # MY_Controller, MY_Model overrides
│   └── third_party/
├── system/            # framework core — never edit
└── index.php          # front controller
```

### Controllers

```php
<?php
defined('BASEPATH') or exit('No direct script access allowed');

class Products extends CI_Controller
{
    public function __construct()
    {
        parent::__construct();
        $this->load->model('product_model');
        $this->load->helper('url');
    }

    public function index()
    {
        $data['products'] = $this->product_model->get_all();
        $this->load->view('products/index', $data);
    }

    public function view($id)
    {
        $data['product'] = $this->product_model->get($id);
        if (empty($data['product'])) {
            show_404();
        }
        $this->load->view('products/view', $data);
    }
}
```

**Rules:** Class name MUST match filename (first letter uppercase). Always call `parent::__construct()`. On Linux, filenames are case-sensitive.

### Models

```php
<?php
defined('BASEPATH') or exit('No direct script access allowed');

class Product_model extends CI_Model
{
    protected $table = 'products';

    public function get_all()
    {
        return $this->db->get($this->table)->result();
    }

    public function get($id)
    {
        return $this->db->get_where($this->table, ['id' => $id])->row();
    }

    public function insert($data)
    {
        $this->db->insert($this->table, $data);
        return $this->db->insert_id();
    }

    public function update($id, $data)
    {
        $this->db->where('id', $id);
        return $this->db->update($this->table, $data);
    }

    public function delete($id)
    {
        return $this->db->delete($this->table, ['id' => $id]);
    }
}
```

### Query Builder

```php
// SELECT with chaining
$results = $this->db
    ->select('p.*, c.name as category_name')
    ->from('products p')
    ->join('categories c', 'c.id = p.category_id', 'left')
    ->where('p.active', 1)
    ->where('p.price >', 10)
    ->order_by('p.name', 'ASC')
    ->limit(20, $offset)
    ->get()
    ->result();

// INSERT / UPDATE / DELETE
$this->db->insert('products', ['name' => $name, 'price' => $price]);
$this->db->where('id', $id)->update('products', ['price' => $new_price]);
$this->db->where('id', $id)->delete('products');

// Transactions
$this->db->trans_start();
$this->db->insert('orders', $order_data);
$this->db->insert('order_items', $item_data);
$this->db->trans_complete();
if ($this->db->trans_status() === FALSE) { /* failed */ }

// Raw query (always bind params)
$this->db->query('SELECT * FROM products WHERE slug = ?', [$slug]);
```

### Routing

```php
$route['default_controller'] = 'home';
$route['404_override'] = 'errors/page_missing';
$route['products'] = 'catalog/index';
$route['products/(:num)'] = 'catalog/view/$1';
$route['api/products/(:any)'] = 'api/products/$1';
```

### Input & Security

```php
// ALWAYS use $this->input — never raw $_POST/$_GET
$name = $this->input->post('name', TRUE);  // TRUE = XSS filter
$id   = $this->input->get('id');

// CSRF — enable in config.php
$config['csrf_protection'] = TRUE;

// Output escaping in views
<?php echo html_escape($user_input); ?>
```

### Form Validation

```php
$this->load->library('form_validation');
$this->form_validation->set_rules('name', 'Name', 'required|min_length[3]|max_length[255]');
$this->form_validation->set_rules('email', 'Email', 'required|valid_email|is_unique[users.email]');

if ($this->form_validation->run() === FALSE) {
    $this->load->view('form', $data);
} else {
    $this->product_model->insert($this->input->post());
    redirect('products');
}
```

### Sessions

```php
$this->session->set_userdata('user_id', $id);
$user_id = $this->session->userdata('user_id');
$this->session->set_flashdata('success', 'Product created.');
```

---

## CI4 — Core Patterns

### Project Structure

```
project/
├── app/
│   ├── Config/        # App.php, Database.php, Routes.php, Filters.php, Services.php, Events.php
│   ├── Controllers/   # BaseController.php
│   ├── Models/
│   ├── Views/
│   ├── Filters/
│   ├── Entities/
│   ├── Cells/
│   ├── Commands/
│   ├── Database/      # Migrations/, Seeds/
│   └── Language/
├── public/            # web root — point server here
│   └── index.php
├── writable/          # cache, logs, session — must be writable by web server
├── tests/
├── .env
├── spark              # CLI tool
└── composer.json
```

### Controllers

```php
<?php

namespace App\Controllers;

class Products extends BaseController
{
    public function index()
    {
        $model = model('ProductModel');
        return view('products/index', ['products' => $model->findAll()]);
    }

    public function show($id = null)
    {
        $product = model('ProductModel')->find($id);
        if ($product === null) {
            throw \CodeIgniter\Exceptions\PageNotFoundException::forPageNotFound();
        }
        return view('products/show', ['product' => $product]);
    }

    public function create()
    {
        if (! $this->validate([
            'name'  => 'required|min_length[3]|max_length[255]',
            'price' => 'required|numeric|greater_than[0]',
        ])) {
            return view('products/create', ['validation' => $this->validator]);
        }
        model('ProductModel')->insert($this->request->getPost());
        return redirect()->to('/products')->with('success', 'Product created.');
    }
}
```

### Models

```php
<?php

namespace App\Models;

use CodeIgniter\Model;

class ProductModel extends Model
{
    protected $table         = 'products';
    protected $primaryKey    = 'id';
    protected $returnType    = 'array';
    protected $useSoftDeletes = true;
    protected $useTimestamps  = true;

    protected $allowedFields = ['name', 'price', 'category_id', 'active'];

    protected $validationRules = [
        'name'  => 'required|min_length[3]|max_length[255]',
        'price' => 'required|numeric|greater_than[0]',
    ];
}
```

**Critical:** `$allowedFields` is mandatory — fields not listed are silently dropped on insert/update. This prevents mass assignment.

### Query Builder

```php
$db = db_connect();

// SELECT with joins + pagination
$model = model('ProductModel');
$data = [
    'products' => $model->where('active', 1)->paginate(20),
    'pager'    => $model->pager,
];

// Raw builder
$results = $db->table('products')
    ->select('products.*, categories.name as category')
    ->join('categories', 'categories.id = products.category_id', 'left')
    ->where('products.active', 1)
    ->orderBy('products.name', 'ASC')
    ->get()
    ->getResultArray();

// Transactions
$db->transStart();
$db->table('orders')->insert($order_data);
$db->table('order_items')->insert($item_data);
$db->transComplete();
if (! $db->transStatus()) { /* failed */ }
```

### Routing

```php
$routes->get('/', 'Home::index');
$routes->get('products', 'Products::index');
$routes->get('products/(:num)', 'Products::show/$1');
$routes->post('products', 'Products::create');
$routes->resource('products'); // generates all CRUD routes

$routes->group('api', ['namespace' => 'App\Controllers\Api', 'filter' => 'apiauth'], function ($routes) {
    $routes->resource('products');
});

$routes->get('admin/(:any)', 'Admin::$1', ['filter' => 'auth']);
```

### Input & Security

```php
// ALWAYS use $this->request — never raw $_POST/$_GET
$name = $this->request->getPost('name');
$id   = $this->request->getGet('id');
$data = $this->request->getJSON(true); // JSON API bodies → array

// Output escaping in views — context-aware
<?= esc($user_input) ?>
<?= esc($value, 'attr') ?>
<?= esc($value, 'js') ?>
```

### Sessions

```php
$session = session();
$session->set('user_id', $id);
$userId = $session->get('user_id');
$session->setFlashdata('success', 'Done.');
$session->setTempdata('otp', $code, 300); // auto-expires in 5 minutes
```

---

## Security Checklist (Both Versions)

- [ ] Never use raw `$_POST`/`$_GET` — use input class (CI3) or `$this->request` (CI4)
- [ ] Enable CSRF protection; exempt only stateless API endpoints
- [ ] Use query builder or bound parameters — never concatenate SQL
- [ ] Escape output: `html_escape()` (CI3) or `esc()` (CI4) in views
- [ ] Set `db_debug = FALSE` (CI3) / `CI_ENVIRONMENT = production` (CI4) on prod
- [ ] Keep `system/` (CI3) or project root (CI4) outside web root
- [ ] Use `$allowedFields` in CI4 models to prevent mass assignment
- [ ] Validate file uploads — check MIME type, not just extension
- [ ] Set secure session config: `database` driver, `httponly`, `secure` flags
- [ ] Use `esc($var, 'attr')` for HTML attributes, `esc($var, 'js')` for JS contexts
- [ ] Set `Content-Security-Policy` headers for production
- [ ] Use HTTPS everywhere — `app.forceGlobalSecureRequests = true` in CI4
- [ ] Never expose stack traces in production

---

## CI3 → CI4 Quick Reference

| CI3 | CI4 |
|-----|-----|
| `$this->load->model('x')` | `model('XModel')` or DI |
| `$this->load->view('x', $data)` | `return view('x', $data)` |
| `$this->load->library('x')` | `service('x')` or `new X()` |
| `$this->input->post('x')` | `$this->request->getPost('x')` |
| `$this->db->get('table')` | `$db->table('table')->get()` |
| `$query->result()` / `->row()` | `$query->getResult()` / `->getRow()` |
| `$query->result_array()` | `$query->getResultArray()` |
| `redirect('url')` | `return redirect()->to('url')` |
| `show_404()` | `throw PageNotFoundException::forPageNotFound()` |
| `$this->session->userdata('x')` | `session()->get('x')` |
| `html_escape($x)` | `esc($x)` |
| `$route['x'] = 'y'` | `$routes->get('x', 'Y::method')` |
| Hooks (`$hook[]`) | Filters (middleware) |
| `CI_Controller` / `CI_Model` | `BaseController` / `CodeIgniter\Model` |
| No namespaces | PSR-4 namespaces |
| No CLI generator | `php spark make:*` |

See [deployment.md](references/deployment.md) for the full 30+ mapping migration table, server configuration, and production deployment checklist.
