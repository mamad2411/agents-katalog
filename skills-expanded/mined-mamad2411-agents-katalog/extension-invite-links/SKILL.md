---
name: extension-invite-links
description: Requests invite-link / RSVP based access where guests can submit responses without login while admin can view responses with login.
version: 1.0.1
compatibility:
  mops:
    caffeineai-invite-links: "~1.0.0"
    caffeineai-authorization: "~1.0.0"
caffeineai-subscription: [none]
---

# Invite Links & RSVP
Invite links & RSVP extension for [Caffeine AI](https://caffeine.ai?utm_source=caffeine-skill&utm_medium=referral).

## Overview

This skill adds invite-link generation and RSVP collection. Admins generate unique invite codes; guests use them to submit responses without authentication.

Prerequisite: You must follow [extension-authorization](../extension-authorization/SKILL.md) first, as this integration depends on it.

# Backend

## Module API

The prefabricated module `mo:caffeineai-invite-links/invite-links-module.mo` provides low-level invite-link and RSVP state management. Do not modify it.

```mo:caffeineai-invite-links/invite-links-module
module {
    public type RSVP = {
        name : Text;
        attending : Bool;
        timestamp : Time.Time;
        inviteCode : Text;
    };

    public type InviteCode = {
        code : Text;
        created : Time.Time;
        used : Bool;
    };

    public type InviteLinksSystemState = {
        var rsvps : Map.Map<Text, RSVP>;
        var inviteCodes : Map.Map<Text, InviteCode>;
    };

    public func initState() : InviteLinksSystemState;
    public func generateUUID(blob: Blob) : Text;
    public func generateInviteCode(state: InviteLinksSystemState, code: Text);
    public func getInviteCodes(state: InviteLinksSystemState) : [InviteCode];
    public func submitRSVP(state: InviteLinksSystemState, name: Text, attending: Bool, inviteCode: Text);
    public func getAllRSVPs(state: InviteLinksSystemState) : [RSVP];
}
```

## Setup in main.mo

`include MixinInviteLinks(accessControlState, inviteState)` MUST be placed in `main.mo`, not in a custom mixin file. The mixin provides these public endpoints automatically:

- `generateInviteCode()`
- `submitRSVP(name, attending, inviteCode)`
- `getAllRSVPs()`
- `getInviteCodes()`

Do NOT redeclare any of these functions. They are provided exclusively by `MixinInviteLinks`.

```motoko filepath=src/backend/main.mo
import AccessControl "mo:caffeineai-authorization/access-control";
import MixinAuthorization "mo:caffeineai-authorization/MixinAuthorization";
import MixinInviteLinks "mo:caffeineai-invite-links/MixinInviteLinks";
import InviteLinksModule "mo:caffeineai-invite-links/invite-links-module";

actor {
    let accessControlState : AccessControl.AccessControlState;
    include MixinAuthorization(accessControlState, null);
    let inviteState : InviteLinksModule.InviteLinksSystemState;
    include MixinInviteLinks(accessControlState, inviteState);

    // Write additional application-specific code here.
};
```

The migration chain head:

```motoko filepath=src/backend/migrations/00000000_000000.mo
import AccessControl "mo:caffeineai-authorization/access-control";
import InviteLinksModule "mo:caffeineai-invite-links/invite-links-module";

module {
    type NewActor = {
        accessControlState : AccessControl.AccessControlState;
        inviteState : InviteLinksModule.InviteLinksSystemState;
    };

    public func migration(_old : {}) : NewActor {
        {
            accessControlState = AccessControl.initState();
            inviteState = InviteLinksModule.initState();
        };
    };
};
```

# Frontend

Invite links and RSVP system functionality:

Here is an example how to implement Internet Identity authentication with admin-only invite links / RSVPs in the frontend: 

```typescript filepath=src/App.tsx
import AdminDashboard from './components/AdminDashboard';
import GuestRSVP from './components/GuestRSVP';
import LoginButton from './components/LoginButton';
import { useIsCurrentUserAdmin } from './hooks/useQueries';

export default function App() {
  const { data: isAdmin } = useIsCurrentUserAdmin();

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-100 to-pink-100">
      <header className="p-4 bg-white/80 backdrop-blur-sm shadow-sm">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <h1 className="text-3xl font-bold text-purple-800">RSVP</h1>
          <LoginButton />
        </div>
      </header>
      <main className="max-w-7xl mx-auto p-4 mt-8">
        {isAdmin ? <AdminDashboard /> : <GuestRSVP />}
      </main>
    </div>
  );
}
```


```typescript filepath=src/components/GuestRSVP.tsx
import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { useSubmitRSVP } from '../hooks/useQueries';

export default function GuestRSVP() {
  const [name, setName] = useState('');
  const [inviteCode, setInviteCode] = useState('');
  const [attending, setAttending] = useState(true);
  const [submitted, setSubmitted] = useState(false);
  const submitRSVP = useSubmitRSVP();

  // Auto-populate invite code from URL
  useEffect(() => {
    const codeFromUrl = new URLSearchParams(window.location.search).get('code');
    if (codeFromUrl) setInviteCode(codeFromUrl);
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    submitRSVP.mutate({ name, attending, inviteCode }, {
      onSuccess: () => setSubmitted(true)
    });
  };

  if (submitted) return <div>Thank you! Your RSVP has been submitted.</div>;

  return (
    <form onSubmit={handleSubmit}>
      <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Your Name" required />
      <input value={inviteCode} onChange={(e) => setInviteCode(e.target.value)} placeholder="Invite Code" required />
      <label>
        <input type="radio" checked={attending} onChange={() => setAttending(true)} />
        Yes, I'll attend
      </label>
      <label>
        <input type="radio" checked={!attending} onChange={() => setAttending(false)} />
        No, I can't attend
      </label>
      <button type="submit" disabled={submitRSVP.isPending}>Submit RSVP</button>
      {submitRSVP.error && <p>Error: {submitRSVP.error.message}</p>}
    </form>
  );
}
```

### Admin Dashboard
```typescript filepath=src/components/AdminDashboard.tsx
import { useGetAllRSVPs, useGetInviteCodes, useGenerateInviteCode } from '../hooks/useQueries';

export default function AdminDashboard() {
  const { data: rsvps } = useGetAllRSVPs();
  const { data: inviteCodes } = useGetInviteCodes();
  const generateInviteCode = useGenerateInviteCode();

  const unusedCodes = inviteCodes?.filter(code => !code.used) || [];
  const attendingCount = rsvps?.filter(rsvp => rsvp.attending).length || 0;

  return (
    <div>
      <div>
        <h2>Statistics</h2>
        <p>Total RSVPs: {rsvps?.length || 0}</p>
        <p>Attending: {attendingCount}</p>
        <p>Not Attending: {(rsvps?.length || 0) - attendingCount}</p>
      </div>

      <div>
        <h2>Invite Codes</h2>
        <button onClick={() => generateInviteCode.mutate()}>Generate New Code</button>
        {unusedCodes.map(code => (
          <div key={code.code}>
            <code>{code.code}</code>
            <button onClick={() => navigator.clipboard.writeText(`${window.location.origin}?code=${code.code}`)}>
              Copy Link
            </button>
          </div>
        ))}
      </div>

      <div>
        <h2>RSVPs</h2>
        <table>
          <thead><tr><th>Name</th><th>Status</th><th>Date</th></tr></thead>
          <tbody>
            {rsvps?.map(rsvp => (
              <tr key={rsvp.inviteCode}>
                <td>{rsvp.name}</td>
                <td>{rsvp.attending ? 'Attending' : 'Not Attending'}</td>
                <td>{new Date(Number(rsvp.timestamp / BigInt(1000000))).toLocaleDateString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
```

## Required Hooks
- `useIsCurrentUserAdmin()` - Check if current user is admin
- `useSubmitRSVP()` - Submit RSVP mutation
- `useGetAllRSVPs()` - Fetch all RSVPs (admin only)
- `useGetInviteCodes()` - Fetch invite codes (admin only)  
- `useGenerateInviteCode()` - Generate new invite code (admin only)
- `useInternetIdentity()` - Internet Identity authentication

## Key Features
- URL parameter parsing for invite codes (`?code=xyz`)
- Copy invite links to clipboard functionality
- Admin/guest view switching based on authentication
- Basic form validation and error handling
- Timestamp conversion for display
