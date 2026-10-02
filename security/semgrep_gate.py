import json
import sys

def security_gate(results):
    has_errors = False
    for finding in results:
        severity = finding["extra"]["severity"]
        if severity == "ERROR":
            has_errors = True
    
    return not has_errors

try:
    with open("semgrep-results.json", "r") as f:
        data = json.load(f)

except FileNotFoundError:
    print("Error: semgrep-results.json no existe")
    sys.exit(1)

except json.JSONDecodeError:
    print("Error: semgrep-results.json no contiene JSON válido")
    sys.exit(1)

if "results" not in data:
    print("results field not in json data")
    sys.exit(1)

results = data["results"]

if security_gate(results):
    print("Security Gate: PASS")
    sys.exit(0)
else:
    print("Security Gate: FAIL")
    sys.exit(1)




