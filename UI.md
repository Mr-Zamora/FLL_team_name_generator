# Frontend Architecture & Style Guide

This document outlines the frontend architecture and coding standards for consistent, maintainable, and scalable web applications.

## Table of Contents
1. [Directory Structure](#directory-structure)
2. [CSS Architecture](#css-architecture)
3. [Naming Conventions](#naming-conventions)
4. [Component Guidelines](#component-guidelines)
5. [Responsive Design](#responsive-design)
6. [Performance](#performance)
7. [Accessibility](#accessibility)
8. [Code Organization](#code-organization)
9. [Best Practices](#best-practices)
10. [Common Components](#common-components)

## Directory Structure

```
static/
├── css/
│   ├── base/           # Base styles, variables, resets
│   │   ├── _variables.css
│   │   ├── _reset.css
│   │   └── _typography.css
│   ├── components/     # Reusable UI components
│   │   ├── _buttons.css
│   │   ├── _cards.css
│   │   ├── _forms.css
│   │   └── _modals.css
│   ├── layout/         # Layout-specific styles
│   │   ├── _header.css
│   │   ├── _footer.css
│   │   └── _grid.css
│   ├── utilities/      # Helper classes
│   │   ├── _spacing.css
│   │   ├── _display.css
│   │   └── _text.css
│   └── main.css        # Main CSS file (imports all others)
├── js/
│   ├── components/     # Component-specific JS
│   ├── utils/          # Utility functions
│   └── main.js         # Main JS file
└── images/             # Image assets
```

## CSS Architecture

### 1. CSS Variables

Define all colors, spacing, and typography as CSS variables in `_variables.css`:

```css
:root {
  /* Colors */
  --color-primary: #0055BF;
  --color-secondary: #FF9E1B;
  --color-success: #00852B;
  --color-error: #D01012;
  --color-text: #333333;
  --color-text-light: #666666;
  --color-background: #F5F5F5;
  --color-white: #FFFFFF;
  --color-border: #E0E0E0;

  /* Spacing */
  --spacing-xxs: 0.25rem;  /* 4px */
  --spacing-xs: 0.5rem;    /* 8px */
  --spacing-sm: 0.75rem;   /* 12px */
  --spacing-md: 1rem;      /* 16px */
  --spacing-lg: 1.5rem;    /* 24px */
  --spacing-xl: 2rem;      /* 32px */
  --spacing-xxl: 3rem;     /* 48px */

  /* Typography */
  --font-size-sm: 0.875rem;  /* 14px */
  --font-size-base: 1rem;    /* 16px */
  --font-size-md: 1.25rem;   /* 20px */
  --font-size-lg: 1.5rem;    /* 24px */
  --font-size-xl: 2rem;      /* 32px */
  
  /* Border Radius */
  --border-radius-sm: 0.25rem;  /* 4px */
  --border-radius-md: 0.5rem;   /* 8px */
  --border-radius-lg: 1rem;     /* 16px */
  
  /* Transitions */
  --transition-default: 0.3s ease;
  
  /* Z-index */
  --z-modal: 1000;
  --z-notification: 1100;
  --z-dropdown: 100;
}
```

### 2. Reset and Base Styles

Use a CSS reset to ensure consistent rendering across browsers in `_reset.css`:

```css
/* Reset and base styles */
*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html {
  scroll-behavior: smooth;
}

body {
  font-family: 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  line-height: 1.5;
  color: var(--color-text);
  background-color: var(--color-background);
}

/* Standardize form elements */
button,
input,
select,
textarea {
  font-family: inherit;
  font-size: 100%;
  line-height: 1.15;
  margin: 0;
}

/* Remove default button styling */
button {
  border: none;
  background: none;
  cursor: pointer;
  padding: 0;
}

/* Remove list styles */
ul, ol {
  list-style: none;
}

/* Make images responsive */
img {
  max-width: 100%;
  height: auto;
  display: block;
}

/* Remove underlines from links */
a {
  text-decoration: none;
  color: inherit;
}
```

## Naming Conventions

### BEM (Block Element Modifier)

Use BEM methodology for naming CSS classes:

```html
<article class="card">
  <img src="..." alt="..." class="card__image">
  <div class="card__content">
    <h3 class="card__title">Title</h3>
    <p class="card__description">Description</p>
    <button class="card__button card__button--primary">Click me</button>
  </div>
</article>
```

### Utility Classes

Use utility classes for common styles:

```css
/* Text alignment */
.text-center { text-align: center; }
.text-right { text-align: right; }

/* Display */
.d-block { display: block; }
.d-flex { display: flex; }
.d-none { display: none; }

/* Spacing */
.mt-1 { margin-top: var(--spacing-xs); }
.mt-2 { margin-top: var(--spacing-sm); }
.mt-3 { margin-top: var(--spacing-md); }
/* ... and so on for other directions and properties */
```

## Component Guidelines

### 1. Buttons

```html
<button class="btn btn--primary">Primary Button</button>
<button class="btn btn--secondary">Secondary Button</button>
<button class="btn btn--outline">Outline Button</button>
```

```css
/* _buttons.css */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--border-radius-sm);
  font-weight: 600;
  font-size: var(--font-size-base);
  line-height: 1.5;
  transition: background-color var(--transition-default),
              color var(--transition-default),
              border-color var(--transition-default);
  cursor: pointer;
  text-align: center;
  white-space: nowrap;
  vertical-align: middle;
  user-select: none;
  border: 2px solid transparent;
}

.btn--primary {
  background-color: var(--color-primary);
  color: var(--color-white);
}

.btn--primary:hover {
  background-color: var(--color-primary-dark);
}

.btn--secondary {
  background-color: var(--color-secondary);
  color: var(--color-white);
}

.btn--outline {
  background-color: transparent;
  border: 2px solid var(--color-primary);
  color: var(--color-primary);
}

.btn--outline:hover {
  background-color: var(--color-primary);
  color: var(--color-white);
}
```

### 2. Cards

```html
<article class="card">
  <img src="..." alt="..." class="card__image">
  <div class="card__content">
    <h3 class="card__title">Card Title</h3>
    <p class="card__description">Card description goes here.</p>
    <div class="card__actions">
      <button class="btn btn--primary">Action</button>
    </div>
  </div>
</article>
```

## Responsive Design

### Breakpoints

```css
/* _variables.css */
:root {
  --breakpoint-sm: 576px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 992px;
  --breakpoint-xl: 1200px;
}

/* Usage in components */
.element {
  width: 100%;
}

@media (min-width: 48em) {
  .element {
    width: 50%;
  }
}
```

## Performance

1. **Critical CSS**
   - Inline critical CSS in the `<head>`
   - Load non-critical CSS asynchronously

2. **Image Optimization**
   - Use modern image formats (WebP, AVIF)
   - Include `width` and `height` attributes
   - Use `loading="lazy"` for below-the-fold images

3. **JavaScript**
   - Defer non-critical JavaScript
   - Use `defer` or `async` attributes
   - Code split large bundles

## Accessibility

1. **Semantic HTML**
   - Use appropriate HTML5 elements
   - Maintain a logical heading hierarchy
   - Include proper ARIA attributes

2. **Keyboard Navigation**
   - Ensure all interactive elements are keyboard accessible
   - Add `:focus` styles
   - Use `tabindex` appropriately

3. **Color Contrast**
   - Maintain sufficient contrast (minimum 4.5:1 for normal text)
   - Don't rely solely on color to convey information

## Code Organization

### JavaScript

```javascript
// components/ExampleComponent.js
export default class ExampleComponent {
  constructor(element) {
    this.element = element;
    this.init();
  }

  init() {
    // Initialize component
    this.bindEvents();
  }


  bindEvents() {
    // Add event listeners
  }

  
  // Cleanup method for when component is removed
  destroy() {
    // Remove event listeners
  }
}

// main.js
import ExampleComponent from './components/ExampleComponent';

document.addEventListener('DOMContentLoaded', () => {
  // Initialize components
  document.querySelectorAll('[data-example]').forEach(element => {
    new ExampleComponent(element);
  });
});
```

## Best Practices

1. **Separation of Concerns**
   - Keep HTML, CSS, and JavaScript separate
   - Avoid inline styles and scripts
   - Use semantic class names

2. **Performance**
   - Minimize DOM manipulation
   - Debounce or throttle event handlers
   - Use event delegation for dynamic content

3. **Maintainability**
   - Follow consistent naming conventions
   - Add comments for complex logic
   - Keep components small and focused

4. **Browser Support**
   - Use feature detection
   - Include appropriate polyfills
   - Test in target browsers

## Common Components

### Modal

```html
<div class="modal" id="exampleModal" aria-hidden="true">
  <div class="modal__overlay" data-modal-close></div>
  <div class="modal__container" role="dialog" aria-modal="true">
    <button class="modal__close" aria-label="Close modal">&times;</button>
    <div class="modal__content">
      <!-- Modal content -->
    </div>
  </div>
</div>
```

### Form Elements

```html
<form class="form">
  <div class="form-group">
    <label for="name" class="form-label">Name</label>
    <input type="text" id="name" class="form-control" required>
    <div class="form-feedback">Please enter your name</div>
  </div>
  
  <div class="form-group">
    <label class="form-checkbox">
      <input type="checkbox">
      <span>I agree to the terms</span>
    </label>
  </div>
  
  <button type="submit" class="btn btn--primary">Submit</button>
</form>
```

## Implementation Checklist

1. [ ] Set up directory structure
2. [ ] Configure build tools (if needed)
3. [ ] Add base styles and variables
4. [ ] Implement responsive breakpoints
5. [ ] Create common components
6. [ ] Add utility classes
7. [ ] Test in target browsers
8. [ ] Optimize for performance
9. [ ] Verify accessibility
10. [ ] Document components and usage

## Resources

- [BEM Methodology](http://getbem.com/)
- [CSS Guidelines](https://cssguidelin.es/)
- [A11Y Project](https://www.a11yproject.com/)
- [MDN Web Docs](https://developer.mozilla.org/)
- [CSS Tricks](https://css-tricks.com/)
