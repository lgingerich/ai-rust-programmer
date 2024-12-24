from dataclasses import dataclass
@dataclass
class RustError:
    error_code: str
    error_name: str
    location: str
    code_context: str
    help_text: str | None = None