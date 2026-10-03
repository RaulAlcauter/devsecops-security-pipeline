
class Finding:
    def __init__(self, scanner, category, severity, identifier, message, file):
        self.scanner = scanner
        self.category = category
        self.severity = severity
        self.identifier = identifier
        self.message = message
        self.file = file

class SecurityReport:
    def __init__(self, scanner, category):
        self.scanner = scanner
        self.category = category
        self.findings = []

    def add_finding(self, finding):
        self.findings.append(finding)

    def has_findings(self):
        return len(self.findings) > 0


