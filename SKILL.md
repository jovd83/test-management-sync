---
name: test-management-sync
description: Keep test cases and results in sync with test-management tools, and render approved test cases for review. Three jobs - export approved cases as detailed or TDD markdown, summary tables, plain text, BDD/Gherkin, Xray .feature bundles, Zephyr Scale CSV, or TestLink and TestRail mappings; map the IDs a tool assigned (TestRail, Xray, Zephyr Scale, TestLink) back into local tests and docs; and publish Playwright, Cypress, Rest Assured or JUnit results into those tools. Use when the test logic already exists. Not for designing tests or choosing techniques.
metadata:
  author: jovd83
  version: 2.0.0
  dispatcher-layer: execution
  dispatcher-lifecycle: active
  dispatcher-category: testing
  dispatcher-capabilities: test-artifact-export, test-case-formatting, test-management-export, test-management-mapping, test-management-reporting
  dispatcher-accepted-intents: render_test_artifact, export_test_cases, format_test_cases, map_test_management_ids, report_test_results
  dispatcher-input-artifacts: approved_test_cases, normalized_test_case_model, scenario_list, narrative_test_docs, test_management_ids, execution_results
  dispatcher-output-artifacts: markdown_test_cases, bdd_feature, xray_feature_bundle, zephyr_csv, testlink_mapping, testrail_mapping, mapping_report, published_results
  dispatcher-stack-tags: testing, framework-agnostic, export, test-management, testrail, xray, zephyr, testlink
  dispatcher-risk: medium
  dispatcher-writes-files: true
---

# Test Management Sync

> **Author:** jovd83 | **Version:** 2.0.0

Keep test artifacts and test-management tools in step, in three jobs:

| Job | What it does | Read |
|---|---|---|
| **Export** | Render existing test cases into a review or import format | this file, from "Scope" on |
| **Map IDs back** | Apply the IDs a tool assigned to the local tests and docs | `./references/map-ids.md` |
| **Publish results** | Push execution results into TestRail, Xray, Zephyr Scale or TestLink | `./references/publish-results.md` |

The usual order is export, then map, then publish. The Playwright, Cypress, Rest Assured and JUnit 5 skill packs hand their test-management work to this skill; it replaced their `transformers/`, `mappers/` and `reporters/` sub-skills in 2.0.0. This skill never designs tests, generates coverage or analyses requirements.

## Scope

Use this skill only when the underlying test logic is already known through one of these inputs:

- approved test cases
- existing TDD, BDD, or plain-text test descriptions
- manually curated scenario lists
- framework-specific narrative test documentation
- normalized scenario data prepared by another skill or workflow

Do not use this skill to:

- choose a black-box test technique
- generate new coverage from requirements
- invent missing business rules, steps, or expected outcomes
- reverse-engineer unsupported vendor schemas from the web

If the user needs test design first, route them to the relevant test-design or test-planning skill before formatting.

## Working With Other Skills

- Accept handoffs from other skills that need test cases rendered, exported, or formatted, and from the framework skill packs for mapping IDs and publishing results.
- Consume normalized scenario data when available instead of re-deriving business intent from prose.
- Keep this skill focused on rendering and export. Do not take over technique selection or coverage planning just because the input is thin.

## Read In This Order

1. `./references/formatter-guide.md`
2. `./references/normalized-test-case-model.md`
3. `./references/destination-field-matrix.md`
4. `./references/formatting-guidelines.md`
5. Read the destination-specific template or reference only for the chosen output:
   - `./assets/templates/test-case.j2`
   - `./assets/templates/tdd-summary-table.j2`
   - `./assets/templates/plain-text-list.j2`
   - `./assets/templates/bdd-feature.j2`
   - `./assets/templates/xray-gherkin.feature.j2`
   - `./assets/templates/zephyr-scale.csv.j2`
   - `./references/xray-gherkin-import.md`
   - `./references/testlink-import-file-formats.pdf`

## Supported Destinations

### Human-review outputs

- detailed markdown test case
- TDD-style markdown test case
- markdown summary table
- plain-text scenario notes
- BDD/Gherkin feature text

### Tool-oriented outputs

- Xray-compatible `.feature` files
- Xray-compatible zipped feature bundles when the workflow explicitly needs a zip
- Zephyr Scale CSV
- TestLink-oriented mapping output based on the bundled reference
- TestRail-oriented mapping output when the target fields are known

## Runtime Inputs

Capture these signals when present:

- target destination
- source artifact type
- scenario grouping such as feature, suite, folder, section, or component
- traceability IDs such as story, requirement, ticket, or test IDs
- metadata such as priority, labels, status, execution type, or owner
- whether the user wants artifact-only output or a mapping preview first
- whether the user needs one file, many files, or a zipped bundle

If the destination is ambiguous but low-risk, infer the most likely format and state the assumption. If the destination changes required fields or the output contract materially, pause for one focused clarification.

## Normalized Working Model

Normalize the source artifact into the minimal stable structure described in `./references/normalized-test-case-model.md`.

At minimum, try to extract:

- scenario identifier
- title
- objective or behavior
- preconditions
- ordered steps or Given/When/Then flow
- expected result or observable outcome
- traceability references
- destination-specific metadata if already known

Do not persist this runtime normalization automatically.

## Memory Model

- Runtime memory: use a temporary normalized case model and missing-field checklist for the current task only.
- Project-local persistent memory: create files only when the user asked for durable artifacts such as exported feature files, CSVs, or markdown case documents in their repo.
- Credentials for mapping or publishing: read from the environment or the team's secret store at run time; never store them.

Do not automatically promote runtime notes into project-local files.

## Execution Workflow

### 1. Classify the Request

- Confirm that the user already has test logic.
- Identify the destination format.
- Determine whether the output is human-review, import-ready, or a mapping preview.

### 2. Normalize the Source

- Convert the source into the normalized working model.
- Preserve only fields that are actually present.
- Keep source facts separate from inferred structure.

### 3. Check Destination Requirements

- Use `./references/destination-field-matrix.md`.
- Build a short missing-field list only for fields that are required by the chosen destination.
- Ask for missing required fields instead of inventing them.

### 4. Render the Artifact

- Use the destination-specific template or reference contract.
- Preserve traceability when it exists.
- Keep import-ready outputs free of analysis commentary.

### 5. Validate When Possible

- Use `python ./scripts/format-validator.py markdown <path>` for detailed markdown or TDD-style markdown that uses the bundled structure.
- Use `python ./scripts/format-validator.py summary <path>` for summary-table markdown.
- Use `python ./scripts/format-validator.py plain_text <path>` for lightweight plain-text artifacts.
- Use `python ./scripts/format-validator.py bdd <path>` for generic Gherkin.
- Use `python ./scripts/format-validator.py xray <path>` for Xray `.feature` files or zipped feature bundles.
- Use `python ./scripts/format-validator.py zephyr <path>` for Zephyr Scale CSV.

If a destination has no deterministic validator in this repo, say that clearly and validate the source-to-destination field mapping manually instead of pretending stronger verification than exists.

### 6. Return the Right Final Shape

- For import-ready destinations, return only the artifact unless a missing-field or ambiguity block remains.
- For mapping previews, return the field mapping plus unresolved gaps.
- For human-review outputs, optimize for readability and stable identifiers.

## Destination Rules

### Detailed Markdown Or TDD

- Use `test-case.j2`.
- Keep one scenario per canonical case artifact unless the user explicitly asks for a summary-only deliverable.
- Use the step table with `Step | Action | Expected Result`.

### Summary Markdown

- Use `tdd-summary-table.j2`.
- Keep the summary compact and stable across revisions.

### Plain Text

- Use `plain-text-list.j2` only for lightweight review output.
- Keep each row readable and decision-oriented rather than verbose prose.

### BDD / Gherkin

- Use `bdd-feature.j2`.
- Keep each scenario focused on one observable behavior.
- Add tags only when they add real traceability or execution meaning.

### Xray

- Stay inside `.feature` file import support described in `./references/xray-gherkin-import.md`.
- Use `xray-gherkin.feature.j2`.
- Package zipped bundles only when the surrounding workflow explicitly requires a zip.
- Do not invent unsupported Xray JSON schemas.

### Zephyr Scale

- Use `zephyr-scale.csv.j2`.
- Do not render the CSV until all required columns are known.
- Repeat parent case metadata only as required by the CSV contract.

### TestLink / TestRail

- Prefer a mapping-first workflow when the import shape is ambiguous.
- Stay within fields supported by the source artifact and bundled references.
- If the user requests a concrete import payload but the destination contract is incomplete or ambiguous in this repo, say so plainly and return the mapping plan instead of fabricating a schema.

## Map IDs Back

Once the tool has assigned IDs, apply them to the local tests and case documents so results can be traced and published. Follow `./references/map-ids.md`. In short:
- Match on stable IDs or requirement links before titles.
- Keep the repository's existing ID convention.
- Never invent an ID or silently overwrite a different one.
- Return a table of what was applied where, plus the unmatched cases.

## Publish Results

Push Playwright, Cypress, Rest Assured or JUnit 5 results into the tool. Follow `./references/publish-results.md`. In short:
- Confirm the target run, execution or cycle, and never create one silently.
- Normalize statuses, and use the reporting path the project already has.
- Attach short evidence for failures.
- Report back what was sent, skipped and rejected.

Publishing writes into a shared system, so confirm before sending, keep secrets out of output, and never report an unmapped result.

## Failure And Escalation Rules

- If the source artifact is incomplete for the requested destination, ask only for the missing required fields.
- If the source mixes designed and undesigned scenarios, format only the designed subset and call out the blocked items.
- If the user requests an unsupported tool or schema, say it is unsupported in the current implementation.
- If multiple output destinations are requested, complete them one at a time from the same normalized model.

## Researching New Destinations

If the user asks for a new output format that this repository does not yet support:

1. Confirm that the task is to extend the skill, not merely to describe the format.
2. Research the destination using primary or official sources only.
3. Capture the contract locally before claiming support:
   - add or update a reference under `./references/`
   - extend `./references/destination-field-matrix.md`
   - add templates or static assets under `./assets/templates/` when rendering is deterministic
   - add or extend validator logic only when local deterministic checks are feasible
   - add source and expected examples under `./examples/`
   - add or extend automated tests under `./tests/`
4. State what was verified, what remains ambiguous, and whether the new destination is artifact-ready or mapping-only.

Use `./references/new-destination-research-workflow.md` and `./scripts/scaffold-new-destination.py` to keep this expansion path structured and auditable.

## Gotchas

- **Xray Destination Overwrites**: Importing feature files into Xray without existing Test issue keys will create new Test issues. If you import them into a project where the same scenarios (by title or path) already exist but keys aren't provided in the feature file tags, you may end up with duplicates instead of updates.
- **Zephyr Scale CSV Header Sensitivity**: The Zephyr Scale CSV importer is highly sensitive to column headers. Do not rename columns in the generated CSV or the import will fail silently or with ambiguous errors.
- **TestRail Template Matching**: Ensure the exported CSV structure matches the TestRail template type (e.g., *Test Case (Text)* vs. *Test Case (Steps)*) you intend to select during import. Mapping a multi-step format to a single-text template will lead to truncated or poorly formatted steps.
- **BDD/Gherkin Step Variance**: If the source artifact uses slightly different phrasing for the same step across multiple scenarios, the exporter will preserve that variance. This can lead to fragmented step libraries in tools like Xray Cloud. Normalize steps in the source before exporting if you want them to be reusable.
- **Character Encoding**: Ensure that your environment supports UTF-8 when generating CSV or feature files. Special characters (like smart quotes or non-ASCII symbols) in the source artifact might be mangled if the file is saved with a different encoding (e.g., Windows-1252), leading to import failures in TestRail or Xray.
- **Traceability ID Formatting**: Many tools (like Jira-based Xray/Zephyr) require traceability IDs to match a specific regex (e.g., `PROJ-123`). If the source artifact contains malformed IDs, the export will still happen, but the link will fail in the destination tool.
- **Batch Limits**: Large exports (e.g., >1000 scenarios in one CSV or a massive zip bundle) might hit destination tool API or UI upload limits. Break large test suites into smaller logical chunks before exporting.
- **Silent Failures in Mapping**: If a required field for a destination is missing in the source, this skill will ask for it. However, if you provide a placeholder, the destination tool might accept the import but ignore the data if it doesn't match the tool's internal validation rules (e.g., priority "High" vs "P1").

## Guardrails

- Do not redesign coverage.
- Do not add missing business logic.
- Do not silently assign invented metadata.
- Do not mix analysis commentary into import-ready artifacts.
- Do not claim a destination is validated when the repo only supports heuristic checks.
- Do not turn runtime normalization into persistent skill memory.
- Do not claim support for a newly researched destination until the repo contains the necessary references, examples, and tests.

## Extensibility Hooks

- Add new destinations by extending `./references/destination-field-matrix.md`, adding or updating the relevant template or reference contract, and teaching `./scripts/format-validator.py` only when deterministic validation is feasible.
- Keep destination-specific behavior in references and templates, not bloated into this file.
- Preserve backward compatibility for existing destination names unless there is a clear migration reason.