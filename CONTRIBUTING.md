# Contributing to edocAI

Thank you for your interest in contributing. This document outlines the process for reporting bugs, suggesting improvements, and submitting code changes.

---

## Table of Contents

- [Contributing to edocAI](#contributing-to-edocai)
  - [Table of Contents](#table-of-contents)
  - [Code of Conduct](#code-of-conduct)
  - [Getting Started](#getting-started)
  - [How to Contribute](#how-to-contribute)
  - [Branch Naming](#branch-naming)
  - [Commit Messages](#commit-messages)
  - [Pull Request Process](#pull-request-process)
    - [PR Description Template](#pr-description-template)
  - [What does this PR do?](#what-does-this-pr-do)
  - [Why is this change needed?](#why-is-this-change-needed)
  - [How was it tested?](#how-was-it-tested)
  - [Related issue](#related-issue)
  - [Screenshots (if applicable)](#screenshots-if-applicable)
  - [Code Style](#code-style)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Features](#suggesting-features)
  - [Questions](#questions)

---

## Code of Conduct

This project follows a simple rule: be respectful. Constructive criticism is welcome; personal attacks are not. Any contributor who violates this will be removed from the project.

---

## Getting Started

1. Fork the repository
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/edocai.git
   cd edocai
   ```
3. Install dependencies:
   ```bash
   npm install
   ```
4. Copy the environment file and fill in the required values:
   ```bash
   cp .env.example .env
   ```
5. Start the development server:
   ```bash
   npm run dev
   ```

The app will be running at `http://localhost:3000`. You will also need a running instance of the [backend API](https://github.com/ymahrous/edocai-backend), see the backend repository for setup instructions.

---

## How to Contribute

1. Check the [open issues](https://github.com/ymahrous/edocai/issues) before starting work to avoid duplicating effort.
2. If no issue exists for what you want to work on, open one first and wait for confirmation before starting.
3. Fork the repo and create your branch from `main`.
4. Make your changes, following the code style guidelines below.
5. Test your changes locally.
6. Open a pull request against `main`.

---

## Branch Naming

Use the following prefixes depending on the type of change:

| Type | Prefix | Example |
|---|---|---|
| New feature | `feat/` | `feat/mobile-navbar` |
| Bug fix | `fix/` | `fix/logout-cta-sync` |
| Refactor | `refactor/` | `refactor/auth-form-component` |
| Documentation | `docs/` | `docs/update-readme` |
| Performance | `perf/` | `perf/polling-backoff` |
| Chore / config | `chore/` | `chore/add-prettier` |

---

## Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <short description>

[optional body]

[optional footer]
```

**Examples:**
```
feat(auth): add confirm password field to signup
fix(navbar): sync logout state on landing page
refactor(api): replace manual token fetch with authFetch in uploadDocument
chore: rename package name from extractiq-frontend to edocai
```

**Rules:**
- Use the imperative mood in the description ("add" not "added")
- Keep the first line under 72 characters
- Reference related issues in the footer: `Closes #12`

---

## Pull Request Process

1. **One concern per PR** — keep PRs focused. A PR that fixes a bug and adds a feature will be asked to split.
2. **Fill out the PR template** — describe what changed and why, not just what.
3. **Link the related issue** — every PR should close or reference an issue.
4. **All checks must pass** — lint, type-check, and build must be green before review.
5. **Request a review** — assign `ymahrous` as the reviewer.
6. **No force-pushing** to a PR branch after review has started.

### PR Description Template

When opening a PR, use this structure:

## What does this PR do?
A short summary of the change.

## Why is this change needed?
The problem it solves or the improvement it makes.

## How was it tested?
Steps you took to verify the change works locally.

## Related issue
Closes #<issue number>

## Screenshots (if applicable)

---

## Code Style

This project uses TypeScript with strict mode enabled. Follow these rules:

**TypeScript**
- No `any` types — use `unknown` and narrow explicitly
- All function parameters and return types should be typed
- Prefer `interface` over `type` for object shapes

**React**
- All components are functional — no class components
- Keep components focused — if a component exceeds ~150 lines, consider splitting it
- Extract repeated JSX into its own component rather than duplicating

**Naming**
- Components: `PascalCase`
- Functions and variables: `camelCase`
- Constants: `SCREAMING_SNAKE_CASE`
- Files: `kebab-case` for utilities, `PascalCase` for components

**Tailwind**
- Use the `cn()` utility from `lib/utils.ts` when conditionally combining classes
- Avoid arbitrary values (`w-[327px]`) where a standard scale value works
- Keep dark mode variants co-located: `isDark ? "..." : "..."`

---

## Reporting Bugs

Open a [GitHub Issue](https://github.com/ymahrous/edocai/issues/new) with the following information:

- **Description** — what happened vs. what you expected
- **Steps to reproduce** — numbered, minimal steps
- **Environment** — OS, browser, Node version
- **Screenshots or error logs** if applicable

Please search existing issues before opening a new one.

---

## Questions and Suggesting Features

Open a [GitHub Issue](https://github.com/ymahrous/edocai/issues/new) with:

- **Problem** — what gap or pain point this addresses
- **Proposed solution** — what you'd like to see
- **Alternatives considered** — other approaches you thought of
- **Additional context** — mockups, examples, or prior art

Feature requests are not guaranteed to be implemented but all suggestions are read and considered.
