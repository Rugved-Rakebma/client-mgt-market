---
name: ingest
description: Process a Fireflies meeting into the knowledge base
allowed-tools: Bash, Read, Write, Agent
user-invocable: true
disable-model-invocation: true
argument-hint: "<fireflies-url> or --latest [--full]"
---

# KB Ingest

Ingest a Fireflies meeting transcript into the knowledge base.

## HARD RULES

1. **NEVER write entity files.** All entities go into the DB via `just kb-add`.
2. **ALWAYS file the meeting doc** in `.knowledge-base/docs/meetings/`.
3. **ALWAYS run `just kb-status`** after adding entities.
4. **People: only track meeting participants**, not everyone mentioned. Someone discussed is not a person to track.
5. **Only spawn a subagent for `--full` transcript filing.** No other subagent usage.

## Reference

See `references/entity-extraction.md` for entity extraction guidelines.

## Pre-injection

- Run `just kb-status 2>/dev/null`

## Ingest Paths

### Fireflies URL

If the argument contains `app.fireflies.ai`:

1. Run `just kb-pull-fireflies --url "<url>"`
2. Use the CLI output directly — it contains the structured summary
3. **Do NOT read the raw JSON file.** Entity extraction uses the summary only.

### Latest from Fireflies

If the argument is `--latest` or `--from-fireflies --latest`:

1. Run `just kb-pull-fireflies --latest`
2. Same as URL path — use CLI output directly

## Flow

### Step 1: Extract entities

From the meeting content, extract entities following the guidelines in `references/entity-extraction.md`. For each entity, check if it already exists via `just kb-list --type <type>`.

Entity types emerge from content. Common types: `decisions`, `action-items`, `requirements`, `strategies`. Use what fits.

**Action item status:** New action items always get `"status": "open"`. When cross-referencing reveals an existing action item that the meeting resolves or completes, include it in the same staging batch with `"status": "completed"` and updated content reflecting how it was resolved.

### Step 2: Propose meeting doc

Propose filing a meeting doc at:
`.knowledge-base/docs/meetings/YYYY-MM-DD-<slug>.md`

- **Without `--full`:** The doc is a clean summary with frontmatter (current behavior).
- **With `--full`:** The doc will contain the full speaker-attributed transcript, filed by a subagent after approval.

Frontmatter for both:
```yaml
---
title: "Meeting Title"
date: YYYY-MM-DD
source: "Fireflies URL or transcript ID"
participants:
  - Name One
  - Name Two
---
```

### Step 3: Present proposals

Present everything for approval in ONE list:
- Entities to create/update (with type, slug, title, content preview)
- People to create/update (participants only — Hard Rule #4)
- Meeting doc location and content approach (summary or full transcript)

**Wait for explicit user approval before writing anything.**

### Step 4: Store (on approval)

**4a. Entities and people** — Build JSON:
```json
{
  "source": {
    "type": "meeting",
    "title": "Meeting Title",
    "path": "docs/meetings/YYYY-MM-DD-slug.md",
    "original_source": "fireflies-url"
  },
  "entities": [
    { "type": "decisions", "slug": "my-slug", "title": "Title", "content": "Full content..." },
    { "type": "action-items", "slug": "new-task", "title": "New Task", "content": "Details...", "status": "open" },
    { "type": "action-items", "slug": "old-task", "title": "Old Task — Completed", "content": "Resolved in this meeting because...", "status": "completed" }
  ],
  "people": [
    { "name": "Jane Doe", "slug": "jane-doe", "role": "Engineer", "org": "Acme" }
  ]
}
```

**Always** write the JSON to `.knowledge-base/.staging.json` and run `just kb-add .knowledge-base/.staging.json`. Never pass JSON inline on the command line. The CLI clears the staging file automatically after a successful write.

**4b. Meeting doc:**

**Without `--full`:** Write the meeting summary directly to `.knowledge-base/docs/meetings/YYYY-MM-DD-slug.md`.

**With `--full`:** Spawn a subagent using the Agent tool with this prompt:

```
Format and file the full meeting transcript.

1. Run: just kb format-transcript <RAW_FILE_PATH>
   (The raw file path is in the pull-fireflies output under "file")
2. Parse the JSON output — the "transcript_md" field contains the formatted transcript.
3. Write the meeting doc to: .knowledge-base/docs/meetings/YYYY-MM-DD-slug.md
   - Start with this frontmatter:
     ---
     title: "<TITLE>"
     date: YYYY-MM-DD
     source: "<FIREFLIES_URL>"
     participants:
       - <speakers from output>
     format: full-transcript
     ---
   - Then paste the full transcript markdown from "transcript_md".
4. Confirm what was written.
```

Replace the placeholders with actual values from the pull-fireflies output. The subagent handles the large transcript without polluting the main context.

### Step 5: Confirm

- Run `just kb-status` and report what was added.

## Key Behaviors

- Capture **WHY** not just WHAT — rationale, context, and reasoning matter.
- **Propose, never auto-apply.** All writes require user approval.
- Cross-reference new entities against existing ones to detect updates and contradictions.
