"""Core CI failure trace triage implementation."""
import re
from typing import List, Optional

class StackTraceClassifier:
    def __init__(self):
        pass

class RemediationPlan:
    def __init__(self, failure_type: str, file_path: str, line_num: int, error_message: str, suggested_fix: str):
        self.failure_type = failure_type
        self.file_path = file_path
        self.line_num = line_num
        self.error_message = error_message
        self.suggested_fix = suggested_fix

class CiFailureTriage:
    FILE_LINE_PATTERN = re.compile(r'File "(.*?)", line (\d+), in (.*)')

    def analyze_log(self, log_content: str) -> Optional[RemediationPlan]:
        lines = log_content.splitlines()
        last_file = "unknown"
        last_line = 0

        for line in lines:
            m = self.FILE_LINE_PATTERN.search(line)
            if m:
                last_file = m.group(1)
                last_line = int(m.group(2))

        # Check for common exceptions at tail
        for line in reversed(lines):
            line_str = line.strip()
            if "ModuleNotFoundError:" in line_str:
                mod = line_str.split("named")[-1].strip().replace("'", "")
                return RemediationPlan("DEPENDENCY_MISSING", last_file, last_line, line_str, f"Add dependency '{mod}' to pyproject.toml")
            elif "SyntaxError:" in line_str:
                return RemediationPlan("SYNTAX_ERROR", last_file, last_line, line_str, f"Fix invalid python syntax at line {last_line}")
            elif "AssertionError" in line_str:
                return RemediationPlan("ASSERTION_FAILURE", last_file, last_line, line_str, f"Inspect failing assertion condition in {last_file}:{last_line}")

        return None
