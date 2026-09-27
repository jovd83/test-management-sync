# Changelog

All notable changes to this repository are documented here.

## [2.0.0] - 2026-09-27

`test-artifact-export-skill` becomes **`test-management-sync`**. It takes over the test-management sub-skills of the framework packs. Those were 36 near-identical copies: `transformers/`, `mappers/` and `reporters/` for TestRail, Xray, Zephyr Scale and TestLink, in Playwright, Cypress and Rest Assured.

### Added
- **Map IDs back** (`references/map-ids.md`): ID shapes per tool, ID placement per framework (Playwright, Cypress, Rest Assured / JUnit 5, markdown case docs), matching order, and conflict rules.
- **Publish results** (`references/publish-results.md`): result files per framework, targets per tool, status normalization, a failure-evidence rule, and troubleshooting.
- Six trigger evals for the new jobs (11 in total), `author` and `version` in the SKILL.md metadata, and LICENSE.

### Changed
- `name` is `test-management-sync`; `dispatcher-risk` is `medium`, because publishing writes into a shared system.
- The README is rewritten to the house standard. The old README called vendor publishing out of scope and linked a CONTRIBUTING.md that did not exist.
- `scripts/validate-repo.py` requires the two new references.

### Removed
- The shared-memory note: the shared-memory skill is retired.

## [1.1.1] - 2026-04-30

### Changed
- Trim `SKILL.md` frontmatter to fit the 1000-character dispatcher limit (description trim, migrate non-dispatcher fields to body).

