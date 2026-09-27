# Test Management Sync

[![Validate Skill](https://github.com/jovd83/test-management-sync/actions/workflows/validate.yml/badge.svg)](https://github.com/jovd83/test-management-sync/actions/workflows/validate.yml)
[![version](https://img.shields.io/badge/version-2.0.0-blue)](CHANGELOG.md)
[![status](https://img.shields.io/badge/status-stable-3fb950)](SKILL.md)
[![category](https://img.shields.io/badge/category-testing-0a7ea4)](SKILL.md)
[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=flat&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/jovd83)

`test-management-sync` keeps test artifacts and test-management tools in step: it exports approved test cases, maps the IDs a tool assigned back into the tests, and publishes execution results into TestRail, Xray, Zephyr Scale or TestLink. It was `test-artifact-export-skill`, and it replaces the `transformers/`, `mappers/` and `reporters/` sub-skills of the Playwright, Cypress and Rest Assured skill packs.

## What This Skill Does

Test-management work comes in three steps, whatever the test framework. Get the cases into the tool, write the tool's IDs back into the tests, and send results against those IDs. The framework packs used to carry their own copies of each step for every tool: 36 small sub-skills that were 78–97% identical once the framework name was set aside. The steps are framework-agnostic; only the result files and the place where an ID lives in the code differ, and those fit in two tables.

| Job | What it does |
|---|---|
| **Export** | Renders approved test cases as detailed or TDD markdown, summary tables, plain text, BDD/Gherkin, Xray `.feature` files or bundles, Zephyr Scale CSV, or TestLink and TestRail field mappings. Jinja templates, JSON schemas, a renderer and a format validator make the output deterministic where the contract is known. |
| **Map IDs back** | Applies TestRail case IDs, Xray keys, Zephyr Scale keys or TestLink external IDs to Playwright, Cypress, Rest Assured or JUnit 5 tests and to markdown case documents, following the repository's existing convention. It matches on stable IDs before titles and never invents or silently overwrites an ID. |
| **Publish results** | Sends JUnit XML or JSON results into the right run, execution, cycle or plan. It normalizes statuses, attaches short failure evidence, and reports back what was sent, skipped and rejected. |

## What This Skill Does Not Do

- **It does not design tests.** Choosing techniques or deriving cases from requirements belongs to `test-design-orchestrator`; reviewing drafted cases belongs to `test-case-reviewer`.
- **It does not run tests.** Execution stays with the framework packs (`playwright-skill`, `cypress-skill`, `restassured-skill`, `junit5-skill`).
- **It does not invent IDs, fields or schemas.** When a destination contract is incomplete, it returns a mapping plan instead of a guessed payload.
- **It does not administer the tools.** Creating projects, users or permissions in TestRail, Jira or TestLink is out of scope. It creates a run, execution or cycle only after confirmation.

## When To Use It

Use it when:

- approved test cases need to go into Xray, Zephyr Scale, TestRail or TestLink, or into a review format;
- the tool has assigned IDs and the tests should carry them;
- a CI run's results should appear in a test run, Test Execution or test cycle;
- a test-lifecycle chain reaches its export or reporting phase.

To design or review the cases themselves, use the sibling skills named above.

## Repository Layout

```
test-management-sync/
├── SKILL.md                         # the three jobs, export workflow, guardrails
├── references/
│   ├── map-ids.md                   # ID shapes per tool, ID placement per framework
│   ├── publish-results.md           # result files, targets, status normalization
│   ├── destination-field-matrix.md  # required fields per export destination
│   ├── formatter-guide.md, formatting-guidelines.md, normalized-test-case-model.md
│   ├── xray-gherkin-import.md, testlink-import-file-formats.pdf
│   └── new-destination-research-workflow.md
├── assets/templates/                # Jinja templates per export format
├── schemas/                         # normalized test case and render request
├── scripts/                         # render-artifact, format-validator, scaffold, validate-repo
├── examples/                        # source cases and expected renders
├── evals/trigger-queries.json       # 11 trigger and non-trigger cases
└── tests/                           # renderer and validator tests
```

## Installation

```bash
npx skills add jovd83/test-management-sync
```

Manual alternative:

```bash
git clone https://github.com/jovd83/test-management-sync.git
```

Then place the folder in `~/.agents/skills/test-management-sync/`, or wherever your agent looks for local skills.

Rendering and validation need Python 3.11 or later. Publishing uses the project's existing reporter, CLI or API client and credentials from the environment.

## Usage

| Ask | Job |
|---|---|
| "Turn these approved checkout cases into Xray feature files" | Export |
| "Convert these manual cases to a Zephyr Scale CSV" | Export |
| "TestRail assigned case IDs; add them to the Playwright tests" | Map IDs back |
| "Publish last night's Cypress results to the Zephyr cycle for 4.2" | Publish results |

```bash
python scripts/render-artifact.py markdown examples/source/checkout-cases.json out/checkout-tdd.md
python scripts/format-validator.py xray examples/expected/checkout-xray.feature
```

## Validation

```bash
python scripts/validate-repo.py
python -m unittest discover -s tests -p "test_*.py"
```

`.github/workflows/validate.yml` runs both on every push and pull request. The format validator checks rendered markdown, summaries, plain text, Xray features and Zephyr CSV against the bundled contracts.

## Evaluation Strategy

`evals/trigger-queries.json` holds 11 cases across the three jobs. The negative cases are designing new tests, setting up a TestRail instance, and diagnosing a failed test. The rendering path is covered by the unit tests against `examples/expected/`.

## Contributing

Edit in this repository, then sync the folder to `~/.agents/skills/test-management-sync/`. The installed copy is downstream and should never be edited directly. To add an export destination, follow `references/new-destination-research-workflow.md` and `scripts/scaffold-new-destination.py`.

## License

MIT — see [LICENSE](LICENSE).
