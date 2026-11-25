---
name: mobile-testing-patterns
description: "Test code for XCTest with async/await, XCUITest with accessibility identifiers, Espresso with Compose, Flutter widget, golden, and integration tests, and a testing pyramid per platform. Use when writing or structuring mobile tests."
---

# Mobile Testing Patterns

## iOS: XCTest Unit Test with Async/Await

```swift
import XCTest
@testable import MyApp

final class ProductRepositoryTests: XCTestCase {
    var sut: ProductRepository!
    var mockAPIClient: MockAPIClient!

    override func setUp() async throws {
        try await super.setUp()
        mockAPIClient = MockAPIClient()
        sut = ProductRepositoryImpl(apiClient: mockAPIClient)
    }

    override func tearDown() async throws {
        sut = nil
        mockAPIClient = nil
        try await super.tearDown()
    }

    func testFetchProducts_returnsProductsOnSuccess() async throws {
        // Given
        let expectedProducts = [Product(id: "1", name: "Widget"), Product(id: "2", name: "Gadget")]
        mockAPIClient.stubbedProducts = expectedProducts

        // When
        let products = try await sut.fetchProducts()

        // Then
        XCTAssertEqual(products.count, 2)
        XCTAssertEqual(products.first?.name, "Widget")
    }

    func testFetchProducts_throwsOnNetworkError() async {
        // Given
        mockAPIClient.stubbedError = URLError(.notConnectedToInternet)

        // When / Then
        do {
            _ = try await sut.fetchProducts()
            XCTFail("Expected error to be thrown")
        } catch {
            XCTAssertTrue(error is URLError)
        }
    }
}

// Mock using protocol
class MockAPIClient: APIClientProtocol {
    var stubbedProducts: [Product] = []
    var stubbedError: Error?

    func fetchProducts() async throws -> [Product] {
        if let error = stubbedError { throw error }
        return stubbedProducts
    }
}
```

---

## iOS: XCUITest with Accessibility Identifiers

```swift
final class CheckoutUITests: XCTestCase {
    var app: XCUIApplication!

    override func setUpWithError() throws {
        continueAfterFailure = false
        app = XCUIApplication()
        app.launchArguments = ["--uitesting"]
        app.launchEnvironment = ["MOCK_API": "true"]
        app.launch()
    }

    func testCheckoutFlow_completesSuccessfully() throws {
        // Navigate to cart
        app.tabBars.buttons["Cart"].tap()

        // Verify item count
        let cartCount = app.staticTexts["cart_item_count"]
        XCTAssertTrue(cartCount.waitForExistence(timeout: 2))
        XCTAssertEqual(cartCount.label, "3 items")

        // Tap checkout
        app.buttons["checkout_button"].tap()

        // Fill shipping form
        let nameField = app.textFields["shipping_name_field"]
        nameField.tap()
        nameField.typeText("John Doe")

        // Submit
        app.buttons["place_order_button"].tap()

        // Assert success screen
        let confirmation = app.staticTexts["order_confirmation_title"]
        XCTAssertTrue(confirmation.waitForExistence(timeout: 5))
        XCTAssertEqual(confirmation.label, "Order Confirmed")
    }
}
```

---

## Android: Espresso with Compose

```kotlin
@RunWith(AndroidJUnit4::class)
class ProductScreenTest {

    @get:Rule
    val composeTestRule = createComposeRule()

    @Test
    fun productList_displaysItems() {
        val fakeProducts = listOf(
            Product(id = "1", name = "Widget", price = 9.99),
            Product(id = "2", name = "Gadget", price = 19.99)
        )
        val fakeViewModel = FakeProductViewModel(fakeProducts)

        composeTestRule.setContent {
            ProductScreen(viewModel = fakeViewModel)
        }

        // Assert items visible
        composeTestRule.onNodeWithText("Widget").assertIsDisplayed()
        composeTestRule.onNodeWithText("Gadget").assertIsDisplayed()
        composeTestRule.onNodeWithText("$9.99").assertIsDisplayed()
    }

    @Test
    fun productItem_tapAddsToCart() {
        composeTestRule.setContent {
            ProductScreen(viewModel = FakeProductViewModel(sampleProducts))
        }

        composeTestRule
            .onNodeWithText("Widget")
            .performClick()

        composeTestRule
            .onNodeWithContentDescription("Cart badge")
            .assertTextEquals("1")
    }
}
```

---

## Flutter: Widget Test

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:myapp/features/cart/cart_screen.dart';

void main() {
  group('CartScreen', () {
    testWidgets('displays empty state when cart is empty', (tester) async {
      await tester.pumpWidget(
        ProviderScope(
          overrides: [
            cartProvider.overrideWith((ref) => CartNotifier()),
          ],
          child: const MaterialApp(home: CartScreen()),
        ),
      );

      expect(find.text('Your cart is empty'), findsOneWidget);
      expect(find.byType(CartItemTile), findsNothing);
    });

    testWidgets('shows item count after adding product', (tester) async {
      final cartNotifier = CartNotifier();

      await tester.pumpWidget(
        ProviderScope(
          overrides: [
            cartProvider.overrideWith((ref) => cartNotifier),
          ],
          child: const MaterialApp(home: CartScreen()),
        ),
      );

      // Add item programmatically
      cartNotifier.add(Product(id: '1', name: 'Widget', price: 9.99));
      await tester.pump();

      expect(find.byType(CartItemTile), findsOneWidget);
      expect(find.text('Widget'), findsOneWidget);
    });
  });
}
```

### Flutter: Golden Test
```dart
testWidgets('ProductCard matches golden', (tester) async {
  await tester.pumpWidget(
    MaterialApp(
      home: ProductCard(product: Product(id: '1', name: 'Widget', price: 9.99)),
    ),
  );

  await expectLater(
    find.byType(ProductCard),
    matchesGoldenFile('goldens/product_card.png'),
  );
});
// Update goldens: flutter test --update-goldens
```

---

## Flutter: Integration Test

```dart
// integration_test/checkout_test.dart
import 'package:integration_test/integration_test.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('complete checkout flow', (tester) async {
    app.main();
    await tester.pumpAndSettle();

    // Navigate to products
    await tester.tap(find.byKey(const Key('products_tab')));
    await tester.pumpAndSettle();

    // Add first product
    await tester.tap(find.byKey(const Key('add_to_cart_0')));
    await tester.pumpAndSettle();

    // Go to cart
    await tester.tap(find.byKey(const Key('cart_tab')));
    await tester.pumpAndSettle();

    expect(find.text('1 item'), findsOneWidget);

    // Proceed to checkout
    await tester.tap(find.text('Checkout'));
    await tester.pumpAndSettle();

    expect(find.text('Shipping Details'), findsOneWidget);
  });
}
```

---

## Testing Pyramid by Platform

| Layer | iOS | Android | Flutter | Speed |
|-------|-----|---------|---------|-------|
| Unit | XCTest | JUnit + Mockito | dart test | Fast |
| Component | XCTest (no UI) | Robolectric | widget test | Fast |
| Integration | XCUITest | Espresso / Compose | integration_test | Slow |
| Device Farm | Firebase Test Lab | Firebase Test Lab | Firebase Test Lab | Slowest |

Run unit + widget tests on every PR. Integration and device farm tests pre-release or nightly.
