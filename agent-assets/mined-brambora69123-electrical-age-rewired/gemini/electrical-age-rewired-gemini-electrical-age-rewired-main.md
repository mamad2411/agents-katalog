# Electrical Age: Re-Wired - Context & Instructions

This repository contains **Electrical Age: Re-Wired**, a port of the popular Minecraft mod "Electrical Age" to version **1.12.2**. It aims to bring the mod's advanced electrical and thermal simulation to modern Minecraft versions (Forge/CleanroomMC).

## Project Overview

-   **Purpose:** Provides a large-scale, realistic in-game electrical simulation with resistive and capacitive effects.
-   **Architecture:**
    -   **Core Simulation:** A custom Modified Nodal Analysis (MNA) solver handles electrical and thermal logic.
    -   **Language:** A hybrid of **Java** and **Kotlin** (v2.2.21). Most new logic and migrations are in Kotlin.
    -   **Build System:** Uses **Gradle** with **RetroFuturaGradle (RFG)**, enabling compatibility with CleanroomMC and modern Java versions.
    -   **Minecraft Version:** 1.12.2.
-   **Key Technologies:**
    -   **Forge API:** Standard 1.12.2 modding framework.
    -   **CleanroomMC:** Recommended runtime for improved performance and modern Java support (Java 8-25).
    -   **Jabel:** Used for modern Java syntax support (optional).
    -   **MNA Solver:** Custom-built electrical engine for real-time physics simulation.

## Building and Running

The project uses the standard Gradle wrapper.

| Task | Command | Description |
| :--- | :--- | :--- |
| **Setup** | `./gradlew setupDecompWorkspace` | Initializes the decompiled Minecraft workspace for development. |
| **Run Client** | `./gradlew runClient` | Launches Minecraft with the mod installed for testing. |
| **Run Server** | `./gradlew runServer` | Launches a dedicated server with the mod. |
| **Build JAR** | `./gradlew build` | Compiles the mod and generates a JAR file in `build/libs`. |
| **Install** | `./gradlew buildAndCopyJar` | Builds the JAR and copies it directly to your local `.minecraft/mods` folder. |
| **i18n Sync** | `./gradlew updateMasterLanguageFile` | Synchronizes and updates the master language file (`en_US.lang`). |

## Development Conventions

### Code Structure
-   **Main Package:** `mods.eln` (source located in `src/main/java/mods/eln`).
-   **Entry Point:** `mods.eln.Eln.kt` (Kotlin-based `@Mod` class).
-   **Content Registration:** Handled in `mods.eln.init.ElnContent.kt`.
-   **Simulation Logic:** Located in `mods.eln.sim` and `mods.eln.solver`.
-   **Proxy Pattern:** Uses `CommonProxy` and `ClientProxy` for sided logic (rendering vs. server-side).

### Git Workflow
-   **Branching:** Follows a modified GitFlow.
    -   `master`: Stable releases only.
    -   `develop`: Primary development branch (PRs should target this).
    -   Feature branches: Used for individual features before merging into `develop`.
-   **Commit Style:** Prefer clear, concise messages focusing on "why" changes were made.

### Standards & Style
-   **Kotlin Preference:** New logic and rewrites should prioritize Kotlin.
-   **Simulation Precision:** Ensure all MNA solver changes are performance-conscious, as the simulation runs every tick.
-   **Mod Compatibility:** Integration with CoFH (RF energy), ComputerCraft, and OpenComputers should be maintained.

## Key Files & Directories
-   `build.gradle`: Main build configuration and dependency management.
-   `gradle.properties`: Project versions and toggleable build options (e.g., `use_modern_java_syntax`).
-   `PORT_TODO.md`: Roadmap of features and fixes being ported from the 1.7.10 `age-series` fork.
-   `src/main/java/mods/eln/init/Descriptors.kt`: Central definition for mod components and machines.
-   `src/main/resources/mcmod.info`: Mod metadata for the Forge loading screen.

## Current Focus (from PORT_TODO.md)
-   **MNA Solver Optimizations:** Improving simulation performance.
-   **Logic Fixes:** Porting fixes for steam generation, thermal systems, and DC/DC converters.
-   **Kotlin Migration:** Continuing the move from legacy Java code to modern Kotlin.
-   **API Development:** Creating a stable electrical integration API for other mods.
