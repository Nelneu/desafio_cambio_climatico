"""Bootstrap checks for PR workflow safety and executable metadata policy."""

import json
from pathlib import Path
import re
import subprocess
import textwrap
import unittest


WORKFLOW = Path(__file__).resolve().parents[1] / ".github/workflows/pr-validation.yml"


class WorkflowPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workflow = WORKFLOW.read_text(encoding="utf-8")
        match = re.search(r"^          script: \|\n((?:            .*\n|\n)+)", cls.workflow, re.M)
        if not match:
            raise AssertionError("metadata github-script block missing")
        cls.script = textwrap.dedent(match.group(1))

    def run_policy(self, *, body="Fixes #1", labels=None, branch="ci/pr-validation-bootstrap",
                   issue=None, api_error=False):
        payload = {
            "script": self.script,
            "body": body,
            "labels": ["type:chore"] if labels is None else labels,
            "branch": branch,
            "issue": {"state": "open", "labels": [{"name": "status:approved"}]}
                     if issue is None else issue,
            "apiError": api_error,
        }
        harness = r"""
const fs = require('node:fs');
const AsyncFunction = Object.getPrototypeOf(async function(){}).constructor;
const input = JSON.parse(fs.readFileSync(0, 'utf8'));
const calls = [];
const github = {rest: {issues: {get: async (args) => {
  calls.push(args);
  if (input.apiError) throw new Error('Not Found');
  return {data: input.issue};
}}}};
const context = {repo: {owner: 'owner', repo: 'repo'}, payload: {pull_request: {
  body: input.body, labels: input.labels.map(name => ({name})),
  head: {ref: input.branch}
}}};
(async () => {
  try {
    await new AsyncFunction('github', 'context', 'core', input.script)(github, context, {});
    console.log(JSON.stringify({ok: true, calls}));
  } catch (error) {
    console.log(JSON.stringify({ok: false, error: error.message, calls}));
  }
})().catch(error => {console.error(error); process.exitCode = 1});
"""
        result = subprocess.run(["node", "-e", harness], input=json.dumps(payload),
                                text=True, capture_output=True, check=True)
        return json.loads(result.stdout)

    def test_event_permissions_and_separation(self):
        workflow = self.workflow
        self.assertRegex(workflow, r"(?m)^on:\s*\n  pull_request:\s*\n    types: \[opened, synchronize, reopened, edited, labeled, unlabeled, ready_for_review\]")
        self.assertNotIn("pull_request_target", workflow)
        self.assertRegex(workflow, r"(?m)^permissions:\s*\n  contents: read\s*\n  issues: read\s*\n  pull-requests: read")
        metadata, tests = workflow.split("  tests:\n", 1)
        self.assertIn("actions/github-script@v7", metadata)
        self.assertNotIn("actions/checkout", metadata)
        self.assertNotIn("run:", metadata)
        self.assertIn("needs: metadata", tests)
        self.assertIn("actions/checkout@v4", tests)
        self.assertIn("persist-credentials: false", tests)
        self.assertIn("actions/setup-python@v5", tests)
        self.assertIn("python-version: '3.12'", tests)
        self.assertIn("permissions:\n      contents: read", tests)
        self.assertNotIn("secrets.", workflow)
        self.assertNotRegex(workflow, r"\$\{\{\s*github\.event\.pull_request\.(?:body|title)")

    def test_test_dependencies_discovery_and_zero_guard(self):
        workflow = self.workflow
        self.assertIn("numpy>=1.24", workflow)
        self.assertIn("pandas>=2.0", workflow)
        self.assertIn("scikit-learn>=1.3", workflow)
        self.assertNotIn("requirements.txt", workflow)
        self.assertNotIn("tensorflow", workflow.lower())
        self.assertIn("countTestCases()", workflow)
        self.assertIn("raise SystemExit", workflow)
        self.assertIn("python -m unittest discover -s tests -p 'test_*.py'", workflow)

    def test_approved_issue_and_one_type_pass(self):
        result = self.run_policy()
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["calls"], [{"owner": "owner", "repo": "repo", "issue_number": 1}])

    def test_missing_multiple_and_duplicate_issue_references(self):
        for body in ("No issue", "Fixes #1 and Closes #2", "Fixes #0"):
            with self.subTest(body=body):
                result = self.run_policy(body=body)
                self.assertFalse(result["ok"], result)
                self.assertEqual(result["calls"], [])
        result = self.run_policy(body="Fixes #1; resolves #1")
        self.assertTrue(result["ok"], result)
        self.assertEqual(len(result["calls"]), 1)

    def test_issue_must_exist_be_open_approved_and_not_pr(self):
        for issue, api_error in (
            ({}, True),
            ({"state": "closed", "labels": [{"name": "status:approved"}]}, False),
            ({"state": "open", "pull_request": {}, "labels": [{"name": "status:approved"}]}, False),
            ({"state": "open", "labels": []}, False),
        ):
            with self.subTest(issue=issue, api_error=api_error):
                self.assertFalse(self.run_policy(issue=issue, api_error=api_error)["ok"])

    def test_exactly_one_type_label(self):
        for labels in ([], ["status:approved"], ["type:chore", "type:fix"]):
            with self.subTest(labels=labels):
                result = self.run_policy(labels=labels)
                self.assertFalse(result["ok"], result)
                self.assertEqual(result["calls"], [])
        self.assertTrue(self.run_policy(labels=["type:chore", "priority:high"])["ok"])

    def test_branch_name(self):
        for branch in ("main", "Feature/Caps", "fix/", "fix/space name"):
            with self.subTest(branch=branch):
                result = self.run_policy(branch=branch)
                self.assertFalse(result["ok"], result)
                self.assertEqual(result["calls"], [])
        self.assertTrue(self.run_policy(branch="fix/delivery-readiness")["ok"])


if __name__ == "__main__":
    unittest.main()
