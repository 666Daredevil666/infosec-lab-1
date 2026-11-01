"""Reject an empty or incomplete native OWASP report; print its scan scope."""
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote


def normalize(name):
    return re.sub(r"[-_.]+", "-", name).lower()


def main():
    root = Path(__file__).resolve().parents[1]
    expected = {}
    for line in (root / "requirements.txt").read_text().splitlines():
        name, version = line.strip().split("==")
        expected[normalize(name)] = version
    report = json.loads(Path(sys.argv[1]).read_text())
    actual = {}
    for dependency in report.get("dependencies", []):
        for package in dependency.get("packages", []):
            identifier = unquote(package["id"])
            if identifier.startswith("pkg:pypi/"):
                name, version = identifier.removeprefix("pkg:pypi/").split("@")
                key = normalize(name)
                if key in actual:
                    raise SystemExit(f"Duplicate dependency in OWASP report: {identifier}")
                actual[key] = version
    if actual != expected:
        raise SystemExit(f"OWASP scan scope mismatch: expected {expected}; got {actual}")
    print(f"OWASP Dependency-Check {report['scanInfo']['engineVersion']}")
    print(f"Report date: {report['projectInfo']['reportDate']}")
    print(f"Verified {len(actual)} pinned runtime dependencies (including transitive dependencies).")
    for source in report["scanInfo"].get("dataSource", []):
        print(f"{source['name']}: {source['timestamp']}")
    print("Python analyzers are experimental; pip-audit provides an independent PyPI audit.")


if __name__ == "__main__":
    main()
