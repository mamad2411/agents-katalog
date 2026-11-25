---
name: polaris-account-connection
description: Shopify Polaris AccountConnection component. Use when merchants need to connect or disconnect third-party accounts. Displays connection status and provides action button.
---

# AccountConnection

## When to use
Use to let merchants connect or disconnect their store to third-party accounts (Facebook, Instagram, etc.). Place at the top of account-related pages.

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| title | ReactNode | Required | Platform or service name merchants can connect to |
| details | ReactNode | - | Additional details about connection status |
| termsOfService | ReactNode | - | Terms and conditions content |
| accountName | string | - | Name of connected service account |
| avatarUrl | string | - | URL for user's avatar image |
| connected | boolean | - | Set if account is connected |
| action | Action | Required | Action for connection/disconnection |

## Examples

```jsx
import { Link, AccountConnection } from '@shopify/polaris';
import { useState, useCallback } from 'react';

function AccountConnectionExample() {
  const [connected, setConnected] = useState(false);
  const accountName = connected ? 'Jane Appleseed' : '';
  const handleAction = useCallback(() => {
    setConnected((connected) => !connected);
  }, []);

  const buttonText = connected ? 'Disconnect' : 'Connect';
  const details = connected ? 'Account connected' : 'No account connected';
  const terms = connected ? null : (
    <p>
      By clicking <strong>Connect</strong>, you agree to accept Sample App's{' '}
      <Link url="Example App">terms and conditions</Link>. You'll pay a
      commission rate of 15% on sales made through Sample App.
    </p>
  );

  return (
    <AccountConnection
      accountName={accountName}
      connected={connected}
      title="Example App"
      action={{ content: buttonText, onAction: handleAction }}
      details={details}
      termsOfService={terms}
    />
  );
}
```

## Best practices

- Place at top of account page
- Clearly identify the platform merchants can connect to
- Show clear connected/disconnected status
- Include link to platform's terms and conditions with fee information
- Open terms link in new browser window
- Use "Connect" as button verb, not "Connect to app"

## Accessibility

- Links to terms/conditions open in new window (include this in labels)
- See setting toggle component for a11y guidance on connection toggles

## Related components

- [Button](../button) - for account actions
- [Link](https://polaris.shopify.com/components/link) - for terms and conditions
