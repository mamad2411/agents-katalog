---
name: syncfusion-winui-avatar-view
description: Guide for implementing the Syncfusion WinUI AvatarView control to display user avatars and profile pictures. Use this when implementing user profiles, contact lists, or chat interfaces requiring visual user representation in WinUI applications. This skill covers initials display, image avatars, group avatars, and pre-defined avatar characters.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing WinUI AvatarView

## When to Use This Skill

Use this skill when the user needs to:
- Display user profile pictures or avatars
- Show user initials in circular or square badges
- Create contact lists with avatar images
- Implement chat interfaces with user avatars
- Display team members with profile pictures
- Show group avatars (up to 3 users)
- Use pre-defined avatar character images
- Create visual user representations in any UI

**Always apply this skill when the user mentions:** avatar, profile picture, user image, initials, contact image, user icon, profile badge, or group avatars in WinUI applications.

## Component Overview

**SfAvatarView** is a Syncfusion WinUI control that provides a graphical representation of user images with support for custom images, user initials, pre-defined avatar characters, and group views. It offers flexible shapes, sizes, and extensive customization.

**Namespace:** `Syncfusion.UI.Xaml.Core`  
**NuGet Package:** `Syncfusion.Core.WinUI`  
**Platform:** WinUI 3 Desktop (.NET 5+, Windows App SDK 1.0+)

**Key Advantage:** Provides a complete avatar solution with built-in support for initials generation, 25 pre-defined avatar characters, and group views without needing custom implementations.

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and NuGet package setup
- Namespace imports and basic initialization
- Default avatar behavior (Avatar1, Circle, Small)
- ImageSource property for custom images
- License registration requirements
- First complete example

### Content Types
📄 **Read:** [references/content-types.md](references/content-types.md)
- 5 content types (Default, Initials, CustomImage, AvatarCharacter, GroupView)
- Initials generation (SingleCharacter, DoubleCharacter)
- 25 pre-defined avatar characters
- Custom image support via ImageSource
- Group view for multiple users (up to 3)
- GroupSource and member path configuration
- Choosing the right content type

### Visual Styles and Shapes
📄 **Read:** [references/visual-styles.md](references/visual-styles.md)
- AvatarShape property (Circle, Square, Custom)
- AvatarSize property (ExtraSmall, Small, Medium, Large, ExtraLarge)
- Size comparisons and guidelines
- Custom shapes with CornerRadius
- Shape selection based on design requirements

### Customization Options
📄 **Read:** [references/customization.md](references/customization.md)
- Border customization (BorderBrush, BorderThickness)
- Background property (solid colors)
- Gradient backgrounds (LinearGradientBrush, RadialGradientBrush)
- Font customization (FontFamily, Foreground, FontSize)
- Theme integration
- Combining customizations

## Quick Start Example

```xaml
<Page
    xmlns:syncfusion="using:Syncfusion.UI.Xaml.Core">
    <Grid>
        <!-- Initials avatar -->
        <syncfusion:SfAvatarView 
            x:Name="userAvatar"
            ContentType="Initials"
            AvatarName="John Doe"
            InitialsType="DoubleCharacter"
            AvatarSize="Large"
            Background="CornflowerBlue"
            Foreground="White"
            AvatarShape="Circle"/>
    </Grid>
</Page>
```

```csharp
using Syncfusion.UI.Xaml.Core;
using Microsoft.UI;

// Create avatar with initials
SfAvatarView avatarView = new SfAvatarView
{
    ContentType = AvatarContentType.Initials,
    AvatarName = "John Doe",
    InitialsType = AvatarInitialsType.DoubleCharacter,
    AvatarSize = AvatarSize.Large,
    Background = new SolidColorBrush(Colors.CornflowerBlue),
    Foreground = new SolidColorBrush(Colors.White),
    AvatarShape = AvatarShape.Circle
};

// Add to UI
this.Content = avatarView;
```

## Common Patterns

### 1. User Profile Avatar with Initials
```xaml
<syncfusion:SfAvatarView 
    ContentType="Initials"
    AvatarName="Sarah Johnson"
    InitialsType="DoubleCharacter"
    AvatarSize="ExtraLarge"
    AvatarShape="Circle"
    Background="#FF6A5ACD"
    Foreground="White"/>
```

**When to use:** User profiles, account pages, settings screens.

### 2. Contact List with Custom Images
```xaml
<ListView ItemsSource="{x:Bind Contacts}">
    <ListView.ItemTemplate>
        <DataTemplate x:DataType="local:Contact">
            <StackPanel Orientation="Horizontal" Spacing="10">
                <syncfusion:SfAvatarView 
                    ContentType="CustomImage"
                    ImageSource="{x:Bind ProfileImagePath}"
                    AvatarSize="Medium"
                    AvatarShape="Circle"/>
                <TextBlock Text="{x:Bind Name}" VerticalAlignment="Center"/>
            </StackPanel>
        </DataTemplate>
    </ListView.ItemTemplate>
</ListView>
```

**When to use:** Contact lists, chat contacts, team directories.

### 3. Chat Message with Avatar Character
```xaml
<StackPanel Orientation="Horizontal" Spacing="10">
    <syncfusion:SfAvatarView 
        ContentType="AvatarCharacter"
        AvatarCharacter="Avatar15"
        AvatarSize="Small"
        AvatarShape="Circle"/>
    <Border Background="LightGray" 
            CornerRadius="8" 
            Padding="10">
        <TextBlock Text="Hello! How are you?"/>
    </Border>
</StackPanel>
```

**When to use:** Chat interfaces, comment sections, messaging apps.

### 4. Group Avatar (Multiple Users)
```xaml
<syncfusion:SfAvatarView 
    ContentType="Group"
    GroupSource="{x:Bind TeamMembers}"
    ImageSourceMemberPath="ProfileImage"
    InitialsMemberPath="Name"
    BackgroundColorMemberPath="BackgroundColor"
    InitialsColorMemberPath="InitialsColor"
    AvatarSize="Large"/>
```

```csharp
public class TeamMember
{
    public string Name { get; set; }
    public string ProfileImage { get; set; }
    public Color BackgroundColor { get; set; }
    public Color InitialsColor { get; set; }
}

public ObservableCollection<TeamMember> TeamMembers { get; set; } = new()
{
    new TeamMember { ProfileImage = "user1.png" },
    new TeamMember { Name = "Alex", BackgroundColor = Colors.LightBlue, InitialsColor = Colors.Navy },
    new TeamMember { ProfileImage = "user3.png" }
};
```

**When to use:** Team displays, group chats, collaborative features showing multiple participants.

### 5. Dynamic Avatar Based on Data Availability
```csharp
private void ConfigureAvatar(User user)
{
    if (!string.IsNullOrEmpty(user.ProfileImageUrl))
    {
        // Use custom image if available
        avatarView.ContentType = AvatarContentType.CustomImage;
        avatarView.ImageSource = new BitmapImage(new Uri(user.ProfileImageUrl));
    }
    else if (!string.IsNullOrEmpty(user.FullName))
    {
        // Use initials if no image
        avatarView.ContentType = AvatarContentType.Initials;
        avatarView.AvatarName = user.FullName;
        avatarView.InitialsType = AvatarInitialsType.DoubleCharacter;
        avatarView.Background = GetColorFromName(user.FullName);
    }
    else
    {
        // Use default avatar character
        avatarView.ContentType = AvatarContentType.AvatarCharacter;
        avatarView.AvatarCharacter = AvatarCharacter.Avatar1;
    }
}
```

**When to use:** Fallback strategy when user data varies in completeness.

### 6. Square Avatar with Border for App Icons
```xaml
<syncfusion:SfAvatarView 
    ContentType="CustomImage"
    ImageSource="AppIcon.png"
    AvatarShape="Square"
    AvatarSize="Large"
    BorderBrush="Gray"
    BorderThickness="1"
    CornerRadius="8"/>
```

**When to use:** App icons, service logos, organization badges, square profile images.

### 7. Gradient Background Avatar with Initials
```xaml
<syncfusion:SfAvatarView 
    ContentType="Initials"
    AvatarName="Emma Wilson"
    InitialsType="DoubleCharacter"
    AvatarSize="Large"
    Foreground="White">
    <syncfusion:SfAvatarView.Background>
        <LinearGradientBrush StartPoint="0,0" EndPoint="1,1">
            <GradientStop Color="#FF6B5ACD" Offset="0"/>
            <GradientStop Color="#FF4169E1" Offset="1"/>
        </LinearGradientBrush>
    </syncfusion:SfAvatarView.Background>
</syncfusion:SfAvatarView>
```

**When to use:** Modern, visually appealing avatars with branded gradients.

## Key Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `ContentType` | AvatarContentType | Default | Type of content to display. Options: Default, Initials, CustomImage, AvatarCharacter, Group. |
| `ImageSource` | ImageSource | null | Custom image for CustomImage content type. Path to user's profile picture. |
| `AvatarName` | string | null | Name to generate initials from. Used with Initials content type. |
| `AvatarCharacter` | AvatarCharacter | Avatar1 | Pre-defined avatar character (Avatar1-Avatar25). Used with AvatarCharacter content type. |
| `InitialsType` | AvatarInitialsType | SingleCharacter | How initials are formatted. Options: SingleCharacter (first letter), DoubleCharacter (two letters). |
| `AvatarShape` | AvatarShape | Circle | Visual shape. Options: Circle, Square, Custom. |
| `AvatarSize` | AvatarSize | Small | Pre-defined size. Options: ExtraSmall, Small, Medium, Large, ExtraLarge. |
| `GroupSource` | IEnumerable | null | Collection for Group content type. Supports up to 3 items. |
| `InitialsMemberPath` | string | null | Property path for initials in GroupSource items. |
| `ImageSourceMemberPath` | string | null | Property path for image in GroupSource items. |
| `BackgroundColorMemberPath` | string | null | Property path for background color in GroupSource items. |
| `InitialsColorMemberPath` | string | null | Property path for initials color in GroupSource items. |
| `Background` | Brush | Gray | Background color or gradient for the avatar. |
| `Foreground` | Brush | Black | Text color for initials. |
| `BorderBrush` | Brush | null | Border color around the avatar. |
| `BorderThickness` | Thickness | 0 | Border thickness around the avatar. |
| `CornerRadius` | CornerRadius | Auto | Corner radius for Custom shape. |
| `FontFamily` | FontFamily | Segoe UI | Font for initials text. |
| `FontSize` | double | Auto | Font size for initials (auto-calculated based on AvatarSize). |

## Common Use Cases

### User Profiles
- Profile pages with user avatars
- Account settings with profile pictures
- User dashboards
- Member profiles

**Best Approach:** Use CustomImage if available, fallback to Initials with user's name.

### Contact Lists
- Phone contacts with avatars
- Email contacts
- Team member directories
- Organization charts

**Best Approach:** Circle shape, Medium or Small size, CustomImage or Initials.

### Chat/Messaging
- Chat conversations with user avatars
- Message threads
- Comment sections
- Forum posts

**Best Approach:** Small or Medium size, Circle shape, quick loading with Initials or AvatarCharacter.

### Group Displays
- Team collaboration views
- Group chat participants
- Project members
- Shared document contributors

**Best Approach:** Use Group content type to show up to 3 participants.

### App Navigation
- User menu with profile picture
- Navbar with logged-in user
- Drawer navigation with profile
- App bar with user avatar

**Best Approach:** Small or ExtraSmall size, Circle shape, initials for quick display.

## Implementation Tips

1. **Initials Generation:**
   - SingleCharacter: First letter of AvatarName ("Alex" → "A")
   - DoubleCharacter single word: First and last letter ("Alex" → "AX")
   - DoubleCharacter multiple words: First letter of first two words ("John Doe" → "JD")

2. **Avatar Character Selection:** 25 pre-defined avatars (Avatar1-Avatar25) provide diverse representation without custom images.

3. **Group View Limitations:** Supports up to 3 items. If more items in GroupSource, only first 3 are displayed.

4. **Image Loading:** Use BitmapImage with ms-appx:/// or https:// URIs. Handle loading errors gracefully.

5. **Background Colors:** Generate consistent colors from user names using hash functions for visual consistency.

6. **Size Guidelines:**
   - ExtraSmall (32x32): Navigation bars, compact lists
   - Small (48x48): Chat messages, dense lists
   - Medium (64x64): Standard lists, cards
   - Large (96x96): Profile pages, prominent displays
   - ExtraLarge (128x128): Large profile headers, focus areas

7. **Performance:** Initials render faster than images. Use initials for long lists, custom images for detail views.

8. **Accessibility:** Avatar images should have AutomationProperties.Name set to user's name for screen readers.

9. **Theme Integration:** Use ThemeResource for Background to auto-adapt to light/dark themes:
   ```xaml
   Background="{ThemeResource SystemAccentColor}"
   ```

10. **Caching:** Cache avatar images to avoid repeated downloads. Use local storage for frequently accessed avatars.

## Related Documentation

- **Content Types:** See [references/content-types.md](references/content-types.md) for detailed content type options
- **Visual Styles:** See [references/visual-styles.md](references/visual-styles.md) for shape and size configurations
- **Customization:** See [references/customization.md](references/customization.md) for appearance customization options
