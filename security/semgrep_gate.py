import json
import sys

with open("/tmp/semgrep-results.json", "r") as f:
    data = json.load(f)
    results = data["results"]

    has_errors = False
    for finding in results:
        severity = finding["extra"]["severity"]
        if severity == "ERROR":
            has_errors = True

    if has_errors:
        print("Security Gate: FAIL")
        sys.exit(1)
    else:
        print("Security Gate: PASS")
        sys.exit(0)

