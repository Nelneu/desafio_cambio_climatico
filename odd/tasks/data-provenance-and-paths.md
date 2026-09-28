# Data provenance, paths and declared inputs

## Objective
Make the five expected source workbooks auditable, use one data-path contract in the notebooks, and document the observed CSV coverage and Excel-reading dependencies. Point 4 (run the pipeline and compare outputs) is deferred by the user.

## Scope and constraints
- Preserve the pre-existing local `.gitignore` modification and the five ignored Excel files; do not include either in delivery.
- Distinguish current versioned CSV observations from unverified institutional provenance of original books.
- No package installation, notebook execution, dataset replacement or HTML regeneration in points 1–3.
- TDD: user selected strict mode with documentation-only exception for DP-3a; DP-3b observed static RED/GREEN. No configured project test runner; checks used Python3 stdlib, notebook JSON/AST and `git diff --check`.
- Route: delegated read-only mapping, delegated writers and independent verification. Feature branch `fix/data-reproducibility` started at `5e73115b9c8f3ea985bd259bbc8479455b6f4548`.
- Review budget: 455 authored lines in integrated work unit; user explicitly accepted direct `main` publication as a size exception after considering chained PRs (none were opened). Delivery: one behavior/docs work-unit commit plus this progress-record commit; do not push until remote `main` ancestry is rechecked.

## Tasks
- [x] DP-1: Document exact DS1–DS5 expected workbook names, sheet-to-output mapping, and the fact that direct download URLs, publishers, versions and institutional provenance are not verified. Evidence: `datos/originales/README.md`, `README.md`; work-unit commit `d5c841cb54302eded93a3e480ce3a444d60fcd02`.
- [x] DP-2: Standardize repository-relative `datos/originales`, `datos/limpios` and `datos/intermedios` paths from cwd ancestors or `CLIMATE_PROJECT_ROOT`; guard missing inputs and link 03→4.1. Evidence: nine notebooks and stage READMEs, isolated bootstrap checks; same work-unit commit.
- [x] DP-3a: Document observed CSV row counts, dates, provincial grain and empty cells; do not claim null rows were eliminated. Evidence: `02_Limpieza/README.md` and notebook markdown, independent recount and correction of annual 231 blanks; same work-unit commit.
- [x] DP-3b: Declare `openpyxl>=3.1.5` for `.xlsx` and `xlrd>=2.0.1` for `.xls` and explain these readers. Evidence: `requirements.txt`, `README.md`, observed static RED/GREEN; same work-unit commit.
- [ ] DP-4: On a new user request, install dependencies in an isolated environment, run the ETL **without overwriting the five versioned CSVs**, compare schemas, keys, periods and contents, and report differences. No execution authorized in this delivery.

## Verification and remaining limits
- Before the commit, independent verification parsed JSON and AST in all 10 notebooks and profiled versioned CSVs: global 464 rows/16 countries/1990–2018/18 blanks; annual 30/1990–2019/**231** blanks; monthly 96 consecutive months/2011-01–2018-12/0 blanks; provincial long 218/2011–2018/0 blanks, grain includes `region`; wide 107/2011–2018/0 blanks. `git diff --check` passed; versioned CSVs were unchanged. Four local XLSX books had plausible expected sheets/headers; DS3 XLS internals and the origin of every source book remain unverified.
- Original Excel copies in `datos/originales/` matched source SHA-256 but are ignored by Git. Generated HTML is stale. No notebooks were executed and no dependencies installed, so end-to-end reproduction remains pending.
- Native review assessment could not resolve untracked-scope authority. An explicit committed-only START for the work-unit commit was blocked **before creating a lineage**, with `candidate-target-projection-drift`; it did not produce approval. Independent read-only verification stands; do not report native review as closed.

## Next step
Publish the reviewed-as-static work-unit and progress commits only after confirming `origin/main` has not moved; preserve `.gitignore` as a local unstaged change. Tomorrow address DP-4 separately and seek original publisher/download evidence if available.
