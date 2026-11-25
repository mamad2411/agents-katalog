---
name: extension-user-approval
description: Approval-based user management.
version: 1.0.1
compatibility:
  mops:
    caffeineai-user-approval: "~1.0.0"
    caffeineai-authorization: "~1.0.0"
caffeineai-subscription: [none]
---

# User Approval
User approval extension for [Caffeine AI](https://caffeine.ai?utm_source=caffeine-skill&utm_medium=referral).

## Overview

This skill adds approval-based user management. Users request access; admins approve or reject. Approved users gain access to protected features.

Prerequisite: You must follow [extension-authorization](../extension-authorization/SKILL.md) first, as this integration depends on it.

# Backend

## Module API

The prefabricated module `mo:caffeineai-user-approval/approval` provides low-level approval state management. Do not modify it.

```mo:caffeineai-user-approval/approval
import AccessControl "mo:caffeineai-authorization/access-control";

module {
    public type ApprovalStatus = {
        #approved;
        #rejected;
        #pending;
    };

    public type UserApprovalState = { /* internal state */ };

    public func initState(accessControlState: AccessControl.AccessControlState) : UserApprovalState;

    public func isApproved(state : UserApprovalState, caller : Principal) : Bool;
    public func requestApproval(state : UserApprovalState, caller : Principal);
    public func setApproval(state : UserApprovalState, user : Principal, approval : ApprovalStatus);

    public type UserApprovalInfo = {
        principal : Principal;
        status : ApprovalStatus;
    };

    public func listApprovals(state : UserApprovalState) : [UserApprovalInfo];
}
```

## Setup in main.mo

`include MixinUserApproval(accessControlState, approvalState)` MUST be placed in `main.mo`, not in a custom mixin file. Declare `approvalState` at actor top level and pass it into the mixin. The mixin provides these public endpoints automatically:

- `isCallerApproved()`
- `requestApproval()`
- `setApproval(user, status)`
- `listApprovals()`

Keep `approvalState` in scope for custom approval guards in app-specific endpoints.

Do NOT redeclare any of the mixin-provided functions.

```motoko filepath=src/backend/main.mo
import AccessControl "mo:caffeineai-authorization/access-control";
import MixinAuthorization "mo:caffeineai-authorization/MixinAuthorization";
import MixinUserApproval "mo:caffeineai-user-approval/MixinUserApproval";
import UserApproval "mo:caffeineai-user-approval/approval";
import Runtime "mo:core/Runtime";

actor {
    let accessControlState : AccessControl.AccessControlState;
    include MixinAuthorization(accessControlState, null);
    let approvalState : UserApproval.UserApprovalState;
    include MixinUserApproval(accessControlState, approvalState);

    // Example custom endpoint with an approval guard:
    // public shared ({ caller }) func protectedFeature() : async () {
    //     if (not (UserApproval.isApproved(approvalState, caller) or AccessControl.hasPermission(accessControlState, caller, #admin))) {
    //         Runtime.trap("Unauthorized: Only approved users can perform this action");
    //     };
    // };
};
```

The migration chain head — `UserApproval.initState` depends on the access-control state, so compute it in order inside the migration body:

```motoko filepath=src/backend/migrations/00000000_000000.mo
import AccessControl "mo:caffeineai-authorization/access-control";
import UserApproval "mo:caffeineai-user-approval/approval";

module {
    type NewActor = {
        accessControlState : AccessControl.AccessControlState;
        approvalState : UserApproval.UserApprovalState;
    };

    public func migration(_old : {}) : NewActor {
        let accessControlState = AccessControl.initState();
        {
            accessControlState;
            approvalState = UserApproval.initState(accessControlState);
        };
    };
};
```

On `initState`, existing admins are automatically approved. All other users are pending.

IMPORTANT: Apply the right authorization and/or approval check to each custom public function.

# Frontend

Approval-based user management:

# User Approval Flow
- Check approval status (`isCallerApproved`)
- If not approved, show option to request approval (`requestApproval`)
- Block access to main features for non-approved users
- Admins have access to all features of the application
- Display approval status clearly in the UI

# Admin Dashboard
For admin users, provide a dashboard to:
- List all users with their approval status (`listApprovals`)
- Approve or reject users (`setApproval`)
- View and assign user roles (using `getCallerUserRole` and `assignCallerUserRole`)

# Backend Integration
The backend already implements the following functionality.
The full interface can be found in <backend-interface>

// Check if current user is approved, admins are always approved
isCallerApproved(): Promise<boolean>;

// Submit approval request
requestApproval(): Promise<void>;

// Get all users and their approval status (admin only)
listApprovals(): Promise<Array<UserApprovalInfo>>;

// Approve or reject a user (admin only)
setApproval(user: Principal, status: ApprovalStatus): Promise<void>;

// Assign a role to a user (admin only)
assignCallerUserRole(user: Principal, role: UserRole): Promise<void>;

// Get current role for a specific user
getCallerUserRole(): Promise<UserRole>;
