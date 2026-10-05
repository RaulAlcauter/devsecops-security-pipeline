from parsers import TrivyParser, SemgrepParser, GitleaksParser
from aggregator import SecurityAggregator
import sys

reports = [
    SemgrepParser("semgrep-results.json").parse(),
    TrivyParser("trivy-results.json", "SCA").parse(),
    GitleaksParser("gitleaks-results.json").parse(),
    TrivyParser("container-trivy-results.json", "Container Security").parse()
]

aggregator = SecurityAggregator(reports)
summary = aggregator.get_summary()

print("Security Scan Summary\n")

print(f"Total findings: {summary['total']}")
print(f"Blocking findings: {summary['blocking']}\n")

print(f"Semgrep: {summary['by_scanner']['Semgrep']}")
print(f"Trivy: {summary['by_scanner']['Trivy']}")
print(f"Gitleaks: {summary['by_scanner']['Gitleaks']}\n")

if summary["blocking"] > 0:
    print("Security Gate: FAIL")
    sys.exit(1)
else:
    print("Security Gate: PASS")
    sys.exit(0)