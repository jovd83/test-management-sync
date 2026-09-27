# Map IDs back

Use this after the test-management tool has assigned IDs to exported cases, when the repository's test code and docs must carry those IDs so results can be traced and published.

This job replaces the per-framework `mappers/*` sub-skills that used to ship in the Playwright, Cypress and Rest Assured skill packs.

## Inputs

- An authoritative mapping from local scenarios to tool IDs: the import response, an export from the tool, or a list the user provides. Never derive IDs from memory or from a naming pattern.
- The target test files and markdown case documents.
- The repository's existing convention for where an ID lives (tag, title prefix, annotation, document field).

## Matching order

1. Match on a stable local scenario ID or requirement link.
2. Match on the title only when no ID exists. When several local tests share a title, disambiguate with the requirement ID or, for API tests, the endpoint path and method.
3. Record every unmatched, ambiguous or colliding case instead of guessing.

## Guardrails

- Do not invent IDs.
- Do not overwrite a different existing ID. Report it as a conflict, with both values.
- Keep the convention the repository already uses; introduce a new one only when there is none, and then use one format throughout.
- Change only the ID placement, never test logic or assertions.

## ID shapes

Confirm the exact prefix on the user's instance; teams configure project keys and prefixes.

| Tool | Typical ID | Notes |
|---|---|---|
| TestRail | `C123` | Case ID; runs and results reference it |
| Xray | `PROJ-123` | The Jira issue key of the Test issue |
| Zephyr Scale | `PROJ-T123` | Test case key |
| TestLink | `PREFIX-123` | External ID: the project prefix plus a number |

## Where the ID goes, per framework

Follow the repository's existing pattern first. Common placements:

| Framework | Common placements |
|---|---|
| Playwright | A tag in the title or the `tag` option (`@C123`), a test annotation (`{ type: 'TestRail', description: 'C123' }`), or a title prefix |
| Cypress | A title prefix, or a tag when the suite uses `@cypress/grep` (`{ tags: ['@C123'] }`) |
| Rest Assured / JUnit 5 | `@Tag("C123")`, a `@DisplayName` prefix, or the annotation of the reporting library the project already uses |
| Markdown case documents | The ID field or heading prefix of the case template |

## Output

- The files changed.
- A table: local test → tool ID → where it was applied.
- Unmatched, ambiguous and conflicting cases, each with the reason.
