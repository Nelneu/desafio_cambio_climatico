# PR CI bootstrap

## Objective
Provide automated PR checks for issue-first integration, including the existing chained delivery PRs, without merging any delivery code prematurely.

## Constraints
- Branch `ci/pr-validation-bootstrap` starts from `main`; keep `fix/delivery-readiness` and its local `.gitignore` untouched.
- User authorized preparing a small CI PR, not merging it or starting native reviews.
- Delivery issue #1 and CI bootstrap issue #6 are `status:approved`. Delivery PRs #2–#5 remain drafts; the new workflow is not yet on `main` or their base branches.
- Workflow must use `pull_request` (never `pull_request_target`), read-only permissions, no shell interpolation of PR content, no credentials persisted to test checkout.
- Verify linked issue approval and exactly one `type:*` label. Run source-focused unittest discovery using only the three required scientific packages, not the full TensorFlow/notebook environment. Reject a zero-test run.
- Do not claim the first bootstrap PR had checks until GitHub actually reports them. Do not merge until the user makes the separate integration decision.

## Tasks
- [x] CI-1: Map repository state and minimal test dependencies; read-only exploration identified numpy, pandas and scikit-learn and zero existing workflows/tests on `main`.
- [x] CI-2: Added `.github/workflows/pr-validation.yml` with read-only PR metadata verification, approved issue lookup, exactly one `type:*` label, safe checkout and nonempty unittest discovery; seven source tests on this bootstrap head. Strict RED before workflow existed; GREEN 7/7 focused and 7/7 full tests. Independent verifier parsed YAML/Python, exercised mock GitHub API cases and checked untracked-file whitespace; no Actions run claimed.
- [x] CI-3: Committed work unit `5e201da307b7dd61a708ebf458ca9f4b2de25503` (232 lines), published draft PR #7 against `main`, linked to separately approved CI issue #6 with one `type:chore` label. A real labelled-event Actions run `36588667118` passed metadata and test jobs; an earlier opened-event run `36588667021` failed metadata before GitHub applied the PR label and skipped tests. This is a fail-closed ordering event, not a passing result for that first run. No merge or native review.

## Acceptance
- Workflow does not run untrusted PR code with a write token or run tests with secrets.
- A linked approved issue and exactly one `type:*` label are checked separately from test execution; missing metadata fails closed.
- PR changes fit under 400 authored diff lines and are covered by targeted regression tests and a real CI run (or a documented GitHub execution blocker).
- Pre-existing branches and OneDrive deliverables remain unchanged.

## Progress
CI-1–CI-3 done subject to the final progress-commit check. PR #7 remains draft; `main` and the four delivery PR bases still lack the workflow. Its labelled-event metadata/test jobs passed, while the initial unlabelled opened event failed as designed. Bootstrap CI merge and propagation through PR bases require a later explicit decision; no merge is authorized here.
