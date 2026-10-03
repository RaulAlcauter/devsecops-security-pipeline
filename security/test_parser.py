from parsers import TrivyParser, SemgrepParser, GitleaksParser

parser = TrivyParser("trivy-results.json")
report = parser.parse()

print(report.scanner)
print(report.category)
print(len(report.findings))

parser = SemgrepParser("semgrep-results.json")
report = parser.parse()

print(report.scanner)
print(len(report.findings))

parser = GitleaksParser("gitleaks-results.json")
report = parser.parse()

print(report.scanner)
print(report.category)
print(len(report.findings))
print(report.findings[0].identifier)
print(report.findings[0].message)
print(report.findings[0].file)