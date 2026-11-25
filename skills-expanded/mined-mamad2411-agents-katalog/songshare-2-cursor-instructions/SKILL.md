# Cursor Instructions

Cursor should carefully consider the documentation in the `docs/` folder for every change. This includes reviewing relevant files to ensure consistency and adherence to the project's guidelines.

## Additional Guidelines

1. **Code Style Guidelines**: Follow the project's coding standards, including naming conventions, formatting rules, and preferred libraries or frameworks.

2. **Testing Requirements**: Ensure all changes include appropriate unit tests, integration tests, or end-to-end tests, as outlined in `docs/TESTING.md`.

3. **Documentation Updates**: Accompany any new features or changes with updates to the relevant documentation in the `docs/` folder.

4. **Dependency Management**: Add new dependencies only if necessary and document them in `docs/DEPENDENCIES.md`.

5. **Security Considerations**: Adhere to security best practices, especially when working with sensitive data, Firestore rules, or authentication mechanisms, as described in `docs/FIRESTORE.md` and `docs/AUTHENTICATION.md`.

6. **Performance Optimization**: Review `docs/OPTIMISTIC_UI.md` and `docs/OFFLINE_MUTATIONS.md` for performance-related best practices.

7. **Feature-Based Structure**: Use the feature-based code structure outlined in `docs/FEATURE_BASED_CODE_STRUCTURE.md`.

8. **Commit Messages**: Write clear and descriptive commit messages to document changes effectively.

9. **TypeScript Guidelines**: Use `type` instead of `interface` for defining types in TypeScript.

10. **Documentation Linking**: Ensure that any new documentation files are linked in the main `README.md` or other relevant documentation files.

## Reminder

This is an Expo.dev project, not a Next.js project. Ensure all code suggestions and changes are appropriate for Expo.dev.

### Additional Note

Never modify files or folders within the `old-project` directory.

Never create Cursor instructions in the `docs/` folder. Cursor instructions should only reside in the `.cursor/` folder.

## Reminder for Cursor

To ensure adherence to user-provided instructions, always:

1. **Review Documentation**: Check the `docs/` folder for relevant guidelines before making any changes.
2. **Follow Coding Standards**: Adhere to the project's coding style, testing requirements, and feature-based structure.
3. **Update Documentation**: Accompany changes with updates to the relevant documentation files.
4. **Link New Documentation**: Ensure new documentation files are linked in the `README.md` or other relevant files.
5. **Avoid Restricted Areas**: Never modify files or folders within the `old-project` directory.

By following these steps, you can ensure consistency and quality in all generated code.
