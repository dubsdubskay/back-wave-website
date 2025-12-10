# Black Wave Website – Changelog


## Table of Contents
- [v0.2 – Hero & Capabilities Refinement](#v02-hero-capabilities-refinement)
  - [Header / Navigation](#header-navigation)
  - [Hero & Capabilities Interaction](#hero-capabilities-interaction)
  - [Capabilities (Pillars) Layout](#capabilities-pillars-layout)
  - [Home Anchor Behavior](#home-anchor-behavior)
  - [Files Touched](#files-touched)
- [v0.3 – Hero Spacing, Scroll Behavior, and Logo](#v03-hero-spacing-scroll-behavior-and-logo)
  - [Header / Logo](#header-logo)
  - [Hero / Capabilities Spacing](#hero-capabilities-spacing)
  - [Hero Toggle Scroll Behavior](#hero-toggle-scroll-behavior)
  - [Files Touched](#files-touched)


## v0.2 – Hero & Capabilities Refinement
_Date: YYYY-MM-DD_

### Header / Navigation
- Updated **logo** styling so “Black Wave” text uses the dirty gold accent color (`--accent`).
- Simplified main navigation items to:
  - `Home` → anchors to `#top` (exact top of page)
  - `Capabilities` → anchors to `#pillars`
  - `Past Performance`, `About`, `Contact`
- Removed separate `Construction` and `Decision & GenAI` nav items since capabilities are now handled within the hero toggles and Capabilities section.

### Hero & Capabilities Interaction
- Hero buttons now act as **capability toggles**:
  - `Construction Services`
  - `Decision & GenAI Support`
- Both buttons link to `#pillars` and carry a `data-target` attribute to map to the corresponding capability card.
- Added JavaScript logic so:
  - The selected hero button uses the **primary** style (filled gold).
  - The non-selected button uses the **ghost** style (outlined).
  - The matching capability card gains an `.active` class for visual emphasis.

### Capabilities (Pillars) Layout
- Reduced the visual gap between hero and capability cards by:
  - Tightening hero bottom padding.
  - Adding a small negative top margin on `.pillars`.
- Added `.pillar-card.active` style:
  - Gold border and subtle gold-tinted background.
  - Slight lift and deeper shadow for a clear selected state.
- Default active state set to **Construction & Field Services** on initial load.

### Home Anchor Behavior
- Introduced a `#top` anchor at the top of `<body>` so the **Home** link scrolls to a stable, flush position without overshooting.
- Both the logo and `Home` nav item now point to `#top`.

### Files Touched
- `index.html`
  - Updated navigation items.
  - Added `#top` anchor.
  - Added `hero-toggle` buttons with `data-target` attributes.
  - Marked capability cards with `data-pillar` and default `.active`.
- `styles.css`
  - Updated `.logo-mark` color to dirty gold.
  - Adjusted `.hero` and `.pillars` spacing.
  - Added `.pillar-card.active` styling and transitions.
- `script.js`
  - Added hero toggle → pillar highlight behavior.
  - Left existing nav toggle, tabs, and footer year logic intact.

## v0.3 – Hero Spacing, Scroll Behavior, and Logo

_Date: YYYY-MM-DD_

### Header / Logo
- Replaced text-only logo with combined image + text:
  - Added `assets/img/Final_Logo.png` and `<img>` tag in header.
  - Updated `.logo` styles to use flex layout with `.logo-icon` and `.logo-text`.
  - Kept “Black Wave” wordmark in dirty gold (`--accent`).

### Hero / Capabilities Spacing
- Reduced bottom padding of `.hero` and increased negative `margin-top` on `.pillars` to visually tighten the space between:
  - Hero toggles (`Construction Services`, `Decision & GenAI Support`)
  - Capabilities cards (`Construction & Field Services`, `Decision Science & GenAI Enablement`).

### Hero Toggle Scroll Behavior
- Overrode default `href="#pillars"` jump for `.hero-toggle` buttons:
  - Added `event.preventDefault()` and custom `window.scrollTo` with a 160px offset.
  - Ensures capability cards scroll into view **while hero toggles remain visible**.
- Left existing highlight behavior intact (selected button appears filled; corresponding pillar card gets `.active` styling).

### Files Touched
- `index.html`
  - Updated header logo markup to include `Final_Logo.png`.
- `styles.css`
  - Added styles for `.logo-icon` and `.logo-text`.
  - Adjusted spacing for `.hero` and `.pillars`.
- `script.js`
  - Enhanced hero toggle logic to control scroll offset while preserving card highlighting.

## v0.4 – Logo Scaling and Past Performance Carousel

_Date: YYYY-MM-DD_

### Header Logo
- Increased visual prominence of the Black Wave logo:
  - Updated `.logo-icon` height to `44px`.
  - Slightly enlarged `.logo-mark` font size.
  - Adjusted `.logo` layout to vertically center image and text with consistent spacing.

### Past Performance Carousel
- Replaced static `cards-grid` layout in Past Performance with a horizontal **carousel** for each tab:
  - Each tab (`Construction Projects`, `Decision & GenAI Projects`) now uses a `.project-carousel` wrapper with:
    - Left/right arrow buttons (`.carousel-arrow.prev` / `.carousel-arrow.next`).
    - A horizontally scrollable `.carousel-track` containing one `.project-card` per past performance.
  - Enabled `scroll-snap-type: x mandatory` for a “lazy-susan” style glide where each card snaps into the center.
  - Arrows move the carousel by ~90% of the viewport width for predictable card-to-card navigation.

### Files Touched
- `index.html`
  - Wrapped project cards in new `.project-carousel` and `.carousel-track` elements for both Past Performance tabs.
- `styles.css`
  - Updated header logo styles (`.logo`, `.logo-icon`, `.logo-text`, `.logo-mark`, `.logo-tagline`).
  - Added styles for `.project-carousel`, `.carousel-track`, `.carousel-arrow`, and responsive tweaks.
- `script.js`
  - Added arrow click handlers to smoothly scroll each Past Performance carousel.
