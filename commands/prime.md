---
description: Prime session with context from the context vault
disable-model-invocation: true
argument-hint: "<project|person|topic|meeting>"
---

# Context Prime

Prime the current session with context. The argument can be anything — a project name, a person, a topic, a meeting date, or a concept.

## Workflow

### 1. Find the context vault

Look for `context-vault/` in the current directory or parent directories (up to 3 levels).

### 2. Determine what to prime on

Parse the argument:

- **Project name** (e.g., "sales-command", "wa-sales-command"): Read `context-vault/projects/{slug}/overview.md`
- **Person name** (e.g., "Kevin", "Reuben"): Search `context-vault/people/` for matching files, read the person page
- **Meeting date** (e.g., "april 7", "2026-04-07"): Search `context-vault/docs/meetings/` for matching files, read the meeting doc
- **Topic/concept** (e.g., "360dialog", "onboarding", "bigquery"): Grep across the vault for relevant entities, read the top results

### 3. Load context

For a **project**: Read the overview. Present a structured briefing:
- Project status and priority
- Key people and their roles
- Open action items (with owners)
- Recent decisions
- Key meetings
- Links to project documents

For a **person**: Read the person page. Present:
- Role and organization
- Assigned action items (open/completed)
- Decisions they're involved in
- Meetings attended

For a **meeting**: Read the meeting doc. Present:
- Summary
- Decisions made
- Action items assigned
- Participants
- Backlinked entities

For a **topic**: Show all entities that reference it:
- Grep for the term across the vault
- Read and summarize the most relevant hits
- Group by type (decisions, action-items, etc.)

### 4. Offer to go deeper

After presenting the briefing, ask if the user wants to dive into any specific entity, person, or meeting from the results.
