# PR CI bootstrap

## Objective
Provide automated PR checks for issue-first integration, including the existing chained delivery PRs, without merging any delivery code prematurely.

## Constraints
- Branch `ci/pr-validation-bootstrap` starts from `main`; keep `fix/delivery-readiness` and its local `.gitignore` untouched.
- User authorized preparing a small CI PR, not merging it or starting native reviews.
- PR #1 issue is `status:approved`. Draft PRs #2–#5 depend on each other, but currently have no GitHub Actions workflow.
- Workflow must use `pull_request` (never `pull_request_target`), read-only permissions, no shell interpolation of PR content, no credentials persisted to test checkout.
- Verify linked issue approval and exactly one `type:*` label. Run source-focused unittest discovery using only the three required scientific packages, not the full TensorFlow/notebook environment. Reject a zero-test run.
- Do not claim the first bootstrap PR had checks until GitHub actually reports them. Do not merge until the user makes the separate integration decision.

## Tasks
- [x] CI-1: Map repository state and minimal test dependencies; read-only exploration identified numpy, pandas and scikit-learn and zero existing workflows/tests on `main`.
- [x] CI-2: Added `.github/workflows/pr-validation.yml` with read-only PR metadata verification, approved issue lookup, exactly one `type:*` label, safe checkout and nonempty unittest discovery; seven source tests on this bootstrap head. Strict RED before workflow existed; GREEN 7/7 focused and 7/7 full tests. Independent verifier parsed YAML/Python, exercised mock GitHub API cases and checked untracked-file whitespace; no Actions run claimed.
- [ ] CI-3: Verify the bootstrap head, commit one work unit, publish a draft PR linked to approved issue #1 with exactly one `type:chore` label, inspect actual GitHub checks and record evidence. No merge.

## Acceptance
- Workflow does not run untrusted PR code with a write token or run tests with secrets.
- A linked approved issue and exactly one `type:*` label are checked separately from test execution; missing metadata fails closed.
- PR changes fit under 400 authored diff lines and are covered by targeted regression tests and a real CI run (or a documented GitHub execution blocker).
- Pre-existing branches and OneDrive deliverables remain unchanged.

## Progress
CI-1 and CI-2 done. CI-3 in progress. Decision on merging bootstrap CI is deferred until observed checks and explicit user authorization.
