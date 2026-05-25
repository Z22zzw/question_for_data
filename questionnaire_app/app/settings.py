from __future__ import annotations

import json
from pathlib import Path
from typing import Any

QUESTIONNAIRE_VERSIONS = ("python", "c", "agent")
QUESTIONNAIRE_VERSION_LABELS = {
    "python": "Python version",
    "c": "C version",
    "agent": "Agent supervision version",
}


class QuestionnaireSettings:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def read(self) -> dict[str, bool]:
        defaults = {version: True for version in QUESTIONNAIRE_VERSIONS}
        if not self.path.exists():
            return defaults
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return defaults
        enabled = data.get("enabled_versions", data)
        if not isinstance(enabled, dict):
            return defaults
        return {
            version: bool(enabled.get(version, defaults[version]))
            for version in QUESTIONNAIRE_VERSIONS
        }

    def write(self, enabled: dict[str, bool]) -> dict[str, bool]:
        current = self.read()
        for version, value in enabled.items():
            if version in current:
                current[version] = bool(value)
        self.path.write_text(
            json.dumps({"enabled_versions": current}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return current

    def is_enabled(self, version: str) -> bool:
        return self.read().get(version, False)

    def as_payload(self) -> dict[str, Any]:
        enabled = self.read()
        return {
            "versions": [
                {
                    "version": version,
                    "label": QUESTIONNAIRE_VERSION_LABELS[version],
                    "enabled": enabled[version],
                }
                for version in QUESTIONNAIRE_VERSIONS
            ]
        }
