# Plan: Order Management System Endpoints

Building 9 endpoint files in `public/` to complete the Order Management System. The database schema and all business logic functions already exist in `includes/db_helper.php` and `includes/functions.php`. Each endpoint will provide HTML forms for demo purposes and handle both GET (show form) and POST (process data) requests. User authentication will use `$_SESSION` after login, and admin features will check the `is_admin` field from the database.

## Steps

### 1. Create `public/index.php` - Landing page
- Display welcome HTML with navigation links to all features
- Show login/register links if not logged in
- Show user menu (create order, confirm order) if logged in
- Show admin menu (search orders, bulk confirm) if logged in as admin
- Use `$_SESSION['user_id']` and `$_SESSION['is_admin']` to determine display

### 2. Create `public/seed.php` - Auto-seed database
- GET: Show simple HTML page with "Seed Database" button
- POST: Call database seed logic (execute `sql/seed.sql` queries manually or indicate already seeded via docker-entrypoint)
- Since seed.sql runs automatically in docker-compose, this endpoint can just show "Database already seeded" message
- Return success/error JSON or HTML message

### 3. Create `public/register.php` - User registration (Requirement #2)
- GET: Display HTML form with fields: email, first_name, last_name, phone, password, confirm_password
- POST: Validate form data using `validateEmail()`, `validatePassword()`, `validatePhone()`, `validateName()` from `includes/validation.php`
- Check password === confirm_password
- Call `emailExists($email)` from `includes/db_helper.php` to prevent duplicates
- Call `insertUser($email, $fname, $lname, $phone, $pass)` from `includes/db_helper.php` (stores plaintext password)
- Return success message or error with HTML/JSON mixed response

### 4. Create `public/login.php` - User login (Requirement #3)
- GET: Display HTML form with email and password fields
- POST: Call `getUserByEmail($email)` from `includes/db_helper.php`
- Compare plaintext password (no hashing!)
- If match, set `$_SESSION['user_id']`, `$_SESSION['email']`, `$_SESSION['is_admin']`
- Redirect to `public/index.php` on success
- Show error message on failure

### 5. Create `public/order.php` - Create order (Requirement #5)
- GET: Display HTML form with product selection (fetch products from DB), quantity inputs
- Show dropdown/list of all products from `products` table
- Allow adding multiple product items (JavaScript or multiple rows)
- POST: Accept `user_id` (from session), array of `{product_number, quantity}` items
- Call `processOrder($data)` from `includes/functions.php` which:
  - Generates order_number via `generateOrderNumber()`
  - Creates order record with PENDING status
  - Creates order_detail records
  - Calculates total
- Return order_number in response (JSON or HTML)

### 6. Create `public/update_order.php` - Edit order (Requirement #6)
- GET: Display HTML form asking for order_number, then show current order items with edit capability
- Fetch order details via `getOrderDetails($orderNumber)` from `includes/functions.php`
- Show editable product quantities
- POST: Accept order_number and updated items array `{product_number, quantity}`
- Call `updateOrderItems($orderNumber, $items)` from `includes/functions.php` which deletes all items and re-inserts (inefficient by design)
- Return success message

### 7. Create `public/confirm_order.php` - User confirms order with shipping address (Requirement #7)
- GET: Display HTML form with order_number input and shipping_address textarea
- POST: Accept order_number and shipping_address
- Call `confirmOrderWithAddress($orderNumber, $address)` from `includes/functions.php` (has SQL injection vulnerability by design)
- Updates `orders.shipping_address` field, keeps status as PENDING
- Return success message

### 8. Create `public/admin/orders.php` - Admin search/list orders (Requirement #4)
- Check `$_SESSION['is_admin']`, redirect to login if not admin
- GET: Display HTML form with search input (order_number or user name)
- Also display all orders by default
- Show order list with columns: order_number, user name, status, total_amount, created_at
- Each order expandable to show order_detail items
- If search parameter provided, call `searchOrders($search)` from `includes/functions.php`
- Display results with checkboxes for bulk confirm feature

### 9. Create `public/admin/confirm_orders.php` - Admin bulk confirm orders (Requirement #8)
- Check `$_SESSION['is_admin']`, redirect if not admin
- POST: Accept array of order_ids
- Call `bulkConfirmOrders($orderIds)` from `includes/functions.php` which updates multiple orders to CONFIRMED status
- Return success message with count of confirmed orders
- Can be called from `public/admin/orders.php` form submission

### 10. Create `public/logout.php` - Destroy session
- Call `session_destroy()`
- Redirect to `public/index.php`

### 11. Add session initialization to all endpoint files
- Add `session_start()` at the top of each PHP file (after includes)
- Include `config/db.php` to establish `$conn`
- Include `includes/db_helper.php`, `includes/functions.php`, `includes/validation.php`

## Verification

After implementation, test using:

1. `docker-compose up --build` to start the application
2. Access `http://localhost:8080` in browser
3. Test flow:
   - Register new user via `public/register.php`
   - Login via `public/login.php`
   - Create order via `public/order.php`, verify order_number returned
   - Update order via `public/update_order.php`
   - Confirm order with shipping address via `public/confirm_order.php`
   - Login as admin (use seeded admin user: admin@test.com / admin123)
   - Search orders via `public/admin/orders.php`
   - Bulk confirm orders via `public/admin/confirm_orders.php`
4. Verify all features work end-to-end
5. Check that SQL injection vulnerabilities exist (intentional)
6. Check that passwords are stored in plaintext (intentional)

## Decisions

- **UI approach**: Mixed HTML forms + form processing in same file (check REQUEST_METHOD to determine GET vs POST)
- **Admin auth**: Check `$_SESSION['is_admin']` from database user record, not query parameter
- **Session handling**: Use `$_SESSION` after login for stateful user tracking
- **Code style**: Follow existing spaghetti pattern - mix HTML output, business logic, and DB queries in same files, no MVC separation
- **Security**: Maintain intentional vulnerabilities (SQL injection, plaintext passwords) per project requirements

## Requirements Mapping

| Requirement | Implementation |
|------------|----------------|
| 1. Auto-seed product status/items | `public/seed.php` (note: already seeded via docker-entrypoint) |
| 2. User registration | `public/register.php` |
| 3. User login | `public/login.php` |
| 4. Admin search/list orders | `public/admin/orders.php` |
| 5. Add order | `public/order.php` |
| 6. Edit order | `public/update_order.php` |
| 7. User confirm order with shipping address | `public/confirm_order.php` |
| 8. Admin bulk confirm orders | `public/admin/confirm_orders.php` |

## Technical Notes

- All business logic functions already exist in `includes/functions.php` and `includes/db_helper.php`
- Database schema is complete in `sql/schema.sql`
- Seed data exists in `sql/seed.sql` and auto-loads via docker-compose
- No refactoring of existing code needed - only create new endpoint files
- Follow "intentionally bad legacy PHP 7 code" pattern per `.github/copilot-instructions.md`:
  - No prepared statements (SQL injection vulnerabilities)
  - Plaintext password storage
  - Mixed concerns (HTML + business logic + DB in same files)
  - Long spaghetti functions
  - Poor error handling
  - Global variables (`$conn`, `$_SESSION`)
