# DPMs Module

DPM (Driver Performance Marker) management features including creation, editing, approval, and viewing.

## Files

| File                      | What                                           | When to read                    |
| ------------------------- | ---------------------------------------------- | ------------------------------- |
| `dpms.routes.ts`          | DPM module routing configuration               | Adding DPM routes, route guards |
| `mixed-date.directive.ts` | Date input directive for flexible date parsing | Date input issues               |

## Directories

| Directory    | What                                        | When to read                 |
| ------------ | ------------------------------------------- | ---------------------------- |
| `home/`      | User's DPM list with expandable details     | Viewing user's own DPMs      |
| `dpm-page/`  | DPM creation page with tabs for create/edit | Creating new DPMs            |
| `new-dpm/`   | New DPM form component                      | DPM form fields, validation  |
| `edit-dpms/` | DPM types editor with drag-and-drop         | Admin DPM type configuration |
| `approvals/` | DPM approval queue for managers             | Approving/denying DPMs       |
| `autogen/`   | Auto-generation tool for bulk DPM creation  | Batch DPM operations         |
| `datagen/`   | Data generation tool for test data          | Test data creation           |
| `dpms/`      | DPMs wrapper component                      | DPM section layout           |
| `shared/`    | Shared DPM utilities and form helpers       | DPM form utilities           |
