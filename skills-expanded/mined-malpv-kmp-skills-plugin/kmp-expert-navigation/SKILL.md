---
name: kmp-expert-navigation
description: Build type-safe navigation in a Compose Multiplatform app — @Serializable destinations, a centralized Actions controller, and a NavHost whose screens take callbacks instead of the NavController. Use whenever the user adds navigation, mentions NavHost, routes, deep links, passing arguments between screens, back-stack/popUpTo behavior, or a startDestination decision — even if they only say "move to the next screen" or "go back after login".
---

# Skill: KMP Expert Navigation

This skill defines how to implement a robust, typed, and decoupled navigation system using the official **Jetpack Compose Navigation (v<version>+)** library in Kotlin Multiplatform environments.

> [!NOTE]
> **Placement (architecture-agnostic):** destinations, the `Actions` controller, and the `NavHost` belong to the **presentation** layer (shared UI, typically the aggregator/`:shared` module). In a **modular** project (feature + layers) the graph lives in the aggregator while each screen lives in its feature's presentation layer — see `kmp-modular-architecture`. In a **single-module** project they are packages under `commonMain`. This skill does not assume a module layout.

## Navigation Standards

1. **Absolute Type-Safety**: The use of String-based routes is prohibited. Kotlin objects and classes annotated with `@Serializable` must be used exclusively.
2. **Centralized Actions**: All navigation interaction logic (pops, navigate, popUpTo) is housed in a centralized navigation controller class named `Actions`.
3. **Decoupled Composables**: Screen Composables do not reference or receive the `NavController`. Instead, they expose callback lambdas for user interactions, delegating routing mechanics entirely to the `NavHost`.
4. **Backstack Protection**: Prevent double taps and accidental multiple navigations by managing the navigation backstack correctly.

---

## 1. Destination Configuration (Destinations.kt)

Navigation entry points are centralized in a logical destinations file using Kotlin Serialization.

```kotlin
import kotlinx.serialization.Serializable

@Serializable
object Destinations {

    @Serializable
    data object Dashboard // Parameterless destinations use "data object"

    @Serializable
    data object Settings

    @Serializable
    data class Detail(val id: String, val mode: String = "view") // Parameterized destinations use "data class"
}
```

### Best Practices in Routing:
- **Optional Parameters**: Define default values for `data class` arguments to make navigation routing flexible.
- **Avoid Passing Complex Objects**: Do not pass large serialized models in routes. Pass only unique identifiers (`id: String`, `uuid: Long`) and let the target screen fetch fresh data from the database or repository layer.

---

## 2. NavHost and Actions Implementation

To avoid propagating the `NavController` throughout the UI tree, we encapsulate screen transitions in a stable container wrapper.

### Centralized Actions Class
```kotlin
import androidx.navigation.NavHostController

class Actions(private val nav: NavHostController) {
    
    fun navigateBack() {
        nav.popBackStack()
    }

    fun openDetail(id: String) {
        nav.navigate(Destinations.Detail(id = id))
    }

    fun openSettings() {
        nav.navigate(Destinations.Settings)
    }
}
```

### Routing Setup Structure (AppNavigation.kt)
```kotlin
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import androidx.navigation.toRoute

@Composable
fun AppNavigation() {
    val navController = rememberNavController()
    val actions = remember(navController) { Actions(navController) }

    NavHost(
        navController = navController,
        startDestination = Destinations.Dashboard
    ) {
        composable<Destinations.Dashboard> {
            DashboardScreen(onDetailClick = actions::openDetail)
        }
        
        composable<Destinations.Detail> { backStackEntry ->
            // Extract type-safe arguments from backstack
            val args = backStackEntry.toRoute<Destinations.Detail>()
            DetailScreen(
                id = args.id, 
                mode = args.mode,
                onBack = actions::navigateBack
            )
        }

        composable<Destinations.Settings> {
            SettingsScreen(onBack = actions::navigateBack)
        }
    }
}
```

---

## Best Practices

- **Actions Stability**: Ensure the `Actions` controller is wrapped in a `remember(navController)` block so that it does not re-instantiate on every recomposition.
- **Absolute Decoupling of Screens**: Screen composables (`DashboardScreen`, `DetailScreen`) should receive lambda callbacks (e.g., `onDetailClick: (String) -> Unit`) in their constructor arguments instead of depending on the navigation framework. This enables Compose Previews and isolated UI testing without mock NavControllers.
- **toRoute<T>()**: Use this extension function instead of manually extracting arguments from `arguments?.getString()`. It is type-safe and parses objects and enums automatically.
