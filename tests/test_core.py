"""Unit tests for agent-ci-failure-trace-triage."""
import unittest
from agent_ci_failure_trace_triage.core import CiFailureTriage

class TestCiFailureTriage(unittest.TestCase):
    def setUp(self):
        self.triage = CiFailureTriage()

    def test_missing_dependency(self):
        log = 'File "app.py", line 5, in <module>' + chr(10) + 'ModuleNotFoundError: No module named "fastapi"'
        plan = self.triage.analyze_log(log)
        self.assertIsNotNone(plan)
        self.assertEqual(plan.failure_type, "DEPENDENCY_MISSING")
        self.assertEqual(plan.line_num, 5)

    def test_assertion_failure(self):
        log = 'File "test.py", line 12, in test_x' + chr(10) + 'AssertionError: 1 != 2'
        plan = self.triage.analyze_log(log)
        self.assertIsNotNone(plan)
        self.assertEqual(plan.failure_type, "ASSERTION_FAILURE")
