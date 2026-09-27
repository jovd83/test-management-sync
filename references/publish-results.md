# Publish results

Use this to push execution results from Playwright, Cypress, Rest Assured or JUnit 5 into TestRail, Xray, Zephyr Scale or TestLink.

This job replaces the per-framework `reporters/*` sub-skills that used to ship in the Playwright, Cypress and Rest Assured skill packs.

Publishing writes into a shared external system that other people read. Confirm the target and the scope before sending anything.

## Inputs

- **Connection details and credentials** from environment variables or the team's secret store. Never echo a secret, and never write one into a file or a command history.
- **The result files** (see the table below).
- **The mapping** from automated tests to tool IDs. If tests do not carry IDs yet, run the map-IDs job first (`map-ids.md`).
- **The target context:** which run, execution, cycle or plan, and which build, version or environment.

## Result sources, per framework

| Framework | Result file |
|---|---|
| Playwright | JUnit XML (`--reporter=junit`) or the JSON reporter output |
| Cypress | JUnit XML (for example via `mocha-junit-reporter`) or mochawesome JSON |
| Rest Assured / JUnit 5 | JUnit XML from Maven Surefire (`target/surefire-reports/`) or Gradle (`build/test-results/`) |

## Where results land, per tool

Confirm names and API editions on the user's instance: Cloud and Server/Data Center editions differ.

| Tool | Results go into | Typical path |
|---|---|---|
| TestRail | A test run, optionally inside a milestone or test plan | The TestRail CLI (`trcli`) or the API |
| Xray | A Test Execution issue in Jira, optionally linked to a Test Plan | Xray's import endpoints (JUnit XML, Xray JSON or Cucumber JSON) |
| Zephyr Scale | A test cycle | The Zephyr Scale API (JUnit XML or its custom format) |
| TestLink | A test plan plus a build, and a platform when the plan uses them | The XML-RPC API |

## Workflow

1. **Confirm the target and the mapping.** If the run, execution or cycle does not exist, ask before creating one; never create it silently.
2. **Normalize statuses** before sending (table below).
3. **Use the path the project already uses:** its reporter, CLI or pipeline step. Add a new client only when there is none, and say so.
4. **Publish.** Attach short evidence for failures and blocked tests: the failing assertion, the message, and a link to the trace, screenshot or log. Do not attach full logs.
5. **Report back:** what was sent, what was skipped (unmapped), and what was rejected. Call out partial publication explicitly.

## Status normalization

These are the default statuses. Instances can define custom ones, so check the target's status list before sending.

| Local outcome | TestRail | Xray | Zephyr Scale | TestLink |
|---|---|---|---|---|
| passed | Passed | PASSED | Pass | p (passed) |
| failed | Failed | FAILED | Fail | f (failed) |
| blocked (setup or dependency failed) | Blocked | FAILED, or a custom blocked status | Blocked | b (blocked) |
| skipped | Leave unreported, or Retest | TODO | Not Executed | Leave unreported |

## Troubleshooting

- **The target run, execution or cycle is missing:** confirm it, or ask to create it, before publishing.
- **The payload is rejected:** validate it against the exact endpoint and edition in use (Xray Cloud and Server accept different formats).
- **The statuses look wrong in the tool:** normalize the local statuses first, and check the instance for custom statuses.
- **A result cannot be mapped:** run the map-IDs job; never report an unmapped result.
- **Authentication fails:** stop and ask the user to fix the credentials; do not look for a workaround.

## Guardrails

- Never echo secrets.
- Never report results for tests that cannot be mapped confidently.
- Do not create runs, executions or cycles without confirmation.
- Say plainly when publication was partial.
