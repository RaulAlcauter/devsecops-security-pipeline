

class SecurityAggregator:
    def __init__(self, reports):
        self.reports = reports

    def get_findings(self):
        allFindings = []
        for report in self.reports:
            for finding in report.findings:
                allFindings.append(finding)

        return allFindings

    def has_blocking_findings(self):
        for finding in self.get_findings():
            if finding.severity is not None:
                if finding.severity in ["HIGH", "CRITICAL", "ERROR"]:
                    return True
            elif finding.scanner == "Gitleaks":
                return True
        return False

    def get_blocking_findings(self):
        blockingFinds = []
        for finding in self.get_findings():
            if finding.severity is not None:
                if finding.severity in ["HIGH", "CRITICAL", "ERROR"]:
                    blockingFinds.append(finding)
            elif finding.scanner == "Gitleaks":
                blockingFinds.append(finding)
        return blockingFinds

    def get_summary(self):
        findings = self.get_findings()

        summary = {
            "total": len(findings),
            "blocking": len(self.get_blocking_findings()),
            "by_scanner":{
                "Semgrep": sum(1 for finding in findings if finding.scanner == "Semgrep"),
                "Trivy": sum(1 for finding in findings if finding.scanner == "Trivy"),
                "Gitleaks": sum(1 for finding in findings if finding.scanner == "Gitleaks")
            }
        }
        return summary
            