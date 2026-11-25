---
name: compose-patterns
description: Jetpack Compose UI patterns and best practices for Android development. Use when building Compose screens, creating reusable components, implementing Material Design 3 components, managing state in Compose, or writing component previews.
---

# Compose Patterns

Best practices và patterns cho Jetpack Compose UI development.

## Screen Structure

### Scaffold Pattern

```kotlin
@Composable
fun FeatureScreen(
    uiState: FeatureUiState,
    onAction: (FeatureAction) -> Unit
) {
    Scaffold(
        topBar = { 
            FeatureTopBar(onBackClick = { onAction(FeatureAction.NavigateBack) }) 
        },
        bottomBar = { /* optional */ },
        floatingActionButton = { /* optional */ }
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
        ) {
            // Screen content
        }
    }
}
```

### State Handling

```kotlin
Box(modifier = Modifier.fillMaxSize()) {
    when {
        uiState.isLoading -> {
            CircularProgressIndicator(modifier = Modifier.align(Alignment.Center))
        }
        uiState.errorMessage != null -> {
            Text(
                text = uiState.errorMessage,
                color = MaterialTheme.colorScheme.error,
                modifier = Modifier.align(Alignment.Center)
            )
        }
        else -> {
            Content(data = uiState.data)
        }
    }
}
```

## Component Design

### Reusable Components

```kotlin
@Composable
fun SelectableCard(
    title: String,
    isSelected: Boolean,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    Card(
        onClick = onClick,
        modifier = modifier,
        colors = CardDefaults.cardColors(
            containerColor = if (isSelected) 
                MaterialTheme.colorScheme.primaryContainer 
            else 
                MaterialTheme.colorScheme.surface
        )
    ) {
        Text(text = title, modifier = Modifier.padding(16.dp))
    }
}
```

### Component trong Screen

```kotlin
@Composable
fun FeatureScreen(
    items: List<Item>,
    onItemClick: (String) -> Unit
) {
    LazyColumn {
        items(items) { item ->
            ItemCard(
                item = item,
                onClick = { onItemClick(item.id) }
            )
        }
    }
}

@Composable
private fun ItemCard(
    item: Item,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    Card(onClick = onClick, modifier = modifier) {
        // Implementation
    }
}
```

## Material Design 3

### Theme Colors

```kotlin
Text(
    text = "Title",
    color = MaterialTheme.colorScheme.onSurface,
    style = MaterialTheme.typography.titleLarge
)

Card(
    colors = CardDefaults.cardColors(
        containerColor = MaterialTheme.colorScheme.surface
    )
)
```

### Common Components

```kotlin
// TopAppBar
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun FeatureTopBar(
    title: String,
    onBackClick: () -> Unit
) {
    TopAppBar(
        title = { Text(title) },
        navigationIcon = {
            IconButton(onClick = onBackClick) {
                Icon(
                    imageVector = Icons.AutoMirrored.Rounded.ArrowBack,
                    contentDescription = "Back"
                )
            }
        },
        colors = TopAppBarDefaults.topAppBarColors(
            containerColor = MaterialTheme.colorScheme.surface
        )
    )
}

// Button
Button(
    onClick = { onAction(FeatureAction.Submit) },
    enabled = uiState.isSubmitEnabled
) {
    Text("Submit")
}
```

## State Management

### Hoisting State

```kotlin
// Stateful version
@Composable
fun ExpandableCard(
    title: String,
    content: @Composable () -> Unit
) {
    var isExpanded by remember { mutableStateOf(false) }
    
    ExpandableCard(
        title = title,
        isExpanded = isExpanded,
        onExpandChange = { isExpanded = it },
        content = content
    )
}

// Stateless version (reusable)
@Composable
fun ExpandableCard(
    title: String,
    isExpanded: Boolean,
    onExpandChange: (Boolean) -> Unit,
    content: @Composable () -> Unit
) {
    Card(onClick = { onExpandChange(!isExpanded) }) {
        Text(title)
        if (isExpanded) content()
    }
}
```

### remember vs rememberSaveable

```kotlin
var isVisible by remember { mutableStateOf(false) }
var text by rememberSaveable { mutableStateOf("") }
```

## Layout Patterns

### Common Layouts

```kotlin
// Column với spacing
Column(
    modifier = Modifier.padding(16.dp),
    verticalArrangement = Arrangement.spacedBy(8.dp)
) {
    Text("Item 1")
    Text("Item 2")
}

// Row với weight
Row(modifier = Modifier.fillMaxWidth()) {
    Text("Left", modifier = Modifier.weight(1f))
    Text("Right")
}

// Box với alignment
Box(modifier = Modifier.fillMaxSize()) {
    Image(/* background */)
    Text(
        text = "Overlay",
        modifier = Modifier.align(Alignment.BottomCenter)
    )
}
```

## Previews

```kotlin
@Preview(name = "Light", showBackground = true)
@Preview(name = "Dark", showBackground = true, uiMode = Configuration.UI_MODE_NIGHT_YES)
@Composable
fun FeatureScreenPreview() {
    AppTheme {
        FeatureScreen(
            uiState = FeatureUiState(
                items = listOf(Item("1", "Item 1"), Item("2", "Item 2"))
            ),
            onAction = {}
        )
    }
}
```

Xem thêm: [references/compose-previews.md](references/compose-previews.md)

## Performance

### Lazy Lists

```kotlin
LazyColumn {
    items(
        items = items,
        key = { it.id }
    ) { item ->
        ItemCard(item = item)
    }
}
```

### Derived State

```kotlin
val sortedItems by remember(items) {
    derivedStateOf { items.sortedBy { it.priority } }
}
```

Xem thêm: [references/compose-performance.md](references/compose-performance.md)

## Animation

```kotlin
AnimatedVisibility(visible = isVisible) {
    Text("Now you see me")
}

AnimatedContent(targetState = count) { targetCount ->
    Text(text = "Count: $targetCount")
}
```

Xem thêm: [references/compose-animation.md](references/compose-animation.md)

## Common Pitfalls

1. **Không pass Modifier** - Luôn có `modifier: Modifier = Modifier`
2. **Hardcoded dimensions** - Dùng theme dimensions hoặc sdp extensions
3. **Business logic trong Composable** - Chuyển logic sang ViewModel
4. **Quên Preview** - Luôn viết Preview
5. **State không hoisted** - Hoist state để reusable

## References

- [references/compose-previews.md](references/compose-previews.md) - Preview patterns chi tiết
- [references/compose-performance.md](references/compose-performance.md) - Performance optimization
- [references/compose-animation.md](references/compose-animation.md) - Animation patterns
- [references/material3-components.md](references/material3-components.md) - Material 3 components
