# Product Requirements Document (PRD): FLL Team Name Generator and Voting App

## Product Overview

A lightweight web app that generates and displays FLL team names and allows users to save and vote on them. Designed to be minimal, child-friendly, and intuitive.

## Goals

- Help teams quickly brainstorm fun and meaningful team names
- Use creative name combinations to inspire students
- Create a simple interface suitable for both classroom and competition use

## Success Metrics

- App stability across devices
- Name generation in <2s
- Positive user feedback from students and teachers

## User Stories

### As a student:
- I want to generate cool team names so I can find one that suits our group.
- I want to add our own team name ideas to the voting list.
- I want to see a fun description so I know what the name means.
- I want to vote on favorites so we can decide as a group.

### As a teacher:
- I want a simple app with no login needed.
- I want to use it on my classroom screen for group discussion.

## Scope (MVP)

- Welcome screen with option to generate names or add custom names
- Generate → Vote workflow
- Local name generator for team names + descriptions
- Manual entry for custom team names
- JSON data store for both generated and user-submitted names/votes
- No user accounts, no persistent sessions

## Timeline

| Phase | Deliverables | Timeframe |
|-------|-------------|-----------|
| Phase 1 | Flask backend, static screens | Week 1 |
| Phase 2 | Local name generator implementation | Week 2 |
| Phase 3 | JSON voting and toggle logic | Week 3 |
| Phase 4 | Testing + polish | Week 4 |

## Future Enhancements (Post-MVP)

- Voting leaderboard view
- Export voted names to PDF
- Custom prompt entry for name themes
- Ability to edit/remove custom names
- Store multiple user sessions using localStorage
- Add sound or animation for selected names

## Constraints

- No user authentication
- No server database (JSON only)
- No external API dependencies
- Simple configuration (no environment variables used)

## Appendices

- Color palette samples
- Word component samples
- Accessibility checklist

---

**Prepared:** June 2025  
**Maintainer:** Rom (Teacher, FLL Mentor)
