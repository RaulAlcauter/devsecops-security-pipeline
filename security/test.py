from models import Finding, SecurityReport

finding = Finding("Semgrep",
    "SAST",
    "ERROR",
    "SQL001",
    "Possible SQL injection",
    "app/app.py")

report = SecurityReport("Semgrep", "SAST")

report.add_finding(finding)

print(report.findings[0].scanner)
print(report.findings[0].severity)
print(report.findings[0].message)
print(report.findings[0].file)