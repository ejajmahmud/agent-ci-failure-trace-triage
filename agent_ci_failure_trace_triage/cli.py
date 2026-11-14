"""CLI for agent-ci-failure-trace-triage."""
import argparse
import sys
from .core import CiFailureTriage

def main():
    parser = argparse.ArgumentParser(description="Agent CI Failure Trace Triage CLI")
    parser.add_argument("--demo", action="store_true", help="Run CI failure triage demo")
    args = parser.parse_args()

    if args.demo:
        triage = CiFailureTriage()
        sample_log = """
running 15 tests...
test_auth ... ok
test_db ... FAIL
Traceback (most recent call last):
  File "tests/test_db.py", line 42, in test_connection
    import psycopg2
ModuleNotFoundError: No module named 'psycopg2'
"""
        plan = triage.analyze_log(sample_log)
        if plan:
            print(f"[+] Isolated Failure Type: {plan.failure_type}")
            print(f"    Target: {plan.file_path}:{plan.line_num}")
            print(f"    Root Cause: {plan.error_message}")
            print(f"    Action Plan: {plan.suggested_fix}")
    else:
        parser.print_help()
    sys.exit(0)

if __name__ == "__main__":
    main()
