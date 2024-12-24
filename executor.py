import subprocess
from subprocess import CompletedProcess
import re
import os
from common import RustError
from typing import List

class Executor:
    def __init__(self, cargo_path: str):
        self.cargo_path = cargo_path


    def get_code(self) -> str:
        with open(os.path.join(self.cargo_path, "src", "main.rs"), "r") as file:
            return file.read()

    # Get verbose explanation of an error code
    # NOTE: Would be better to store all Rust error codes in llm context
    def check_error(self, error_code: str) -> CompletedProcess[str]:
        result = subprocess.run(
            ["rustc", "--explain", error_code],
            cwd=self.cargo_path,
            capture_output=True,
            text=True,
        )
        return result

    def _parse_rust_errors(self, stderr: str) -> List[RustError]:
        # Regular expression to match error patterns
        error_pattern = (
            r'error\[(?P<error_code>E\d+)\]: (?P<error_name>.*?)\n'
            r'(?P<location> *--> .*?:\d+:\d+\n)'
            r'(?P<code_context>(?:[ ]*\d*\s*\|.*\n)+'  # Match the line number and code
            r'(?:[ ]*\|.*\n)*'                         # Match any pointer lines
            r'(?:[ ]*=.*\n)*)'                         # Match any note lines
        )
        
        errors = []
        for match in re.finditer(error_pattern, stderr, re.MULTILINE):
            error = RustError(
                error_code=match.group('error_code'),
                error_name=match.group('error_name').strip(),
                location=match.group('location').strip(),
                code_context=match.group('code_context').strip(),
                # TODO: Add help text
            )
            errors.append(error)
        return errors

    # Run `cargo clippy`
    def lint_code(self) -> tuple[str, List[RustError]]:
        result = subprocess.run(
            ["cargo", "clippy"],
            cwd=self.cargo_path,
            capture_output=True,
            text=True,
        )
        print(result.stderr)
        errors = self._parse_rust_errors(result.stderr)
        return result.stdout, errors

    # Run `cargo fmt`
    def format_code(self) -> tuple[str, str]:
        result = subprocess.run(
            ["cargo", "fmt"],
            cwd=self.cargo_path,
            capture_output=True,
            text=True,
        )
        return result.stdout, result.stderr

    # `cargo check` is fully covered by `cargo clippy`
    # Likely no reason to ever run `cargo check` independently
    def check_code(self) -> tuple[str, str]:
        result = subprocess.run(
            ["cargo", "check"],
            cwd=self.cargo_path,
            capture_output=True,
            text=True,
        )
        return result.stdout, result.stderr

    # Run `cargo build`
    def build_code(self) -> tuple[str, str]:
        result = subprocess.run(
            ["cargo", "build"],
            cwd=self.cargo_path,
            capture_output=True,
            text=True,
        )
        return result.stdout, result.stderr

    # Run `cargo run`
    # NOTE: I won't be programmatically running code so I don't need this
    def run_code(self) -> tuple[str, str]:
        result = subprocess.run(
            ["cargo", "run"],
            cwd=self.cargo_path,
            capture_output=True,
            text=True,
        )
        return result.stdout, result.stderr
