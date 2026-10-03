import json

from models import Finding, SecurityReport

class Parser:
    def __init__(self, file):
        self.file = file
    
    def load_data(self):
        with open(self.file, "r") as f:
            return json.load(f)

class SemgrepParser(Parser):

    def parse(self):

        data = self.load_data()

        results = data["results"]

        report = SecurityReport("Semgrep", "SAST")
        for finding in results:
            report.add_finding(Finding(
                "Semgrep",
                "SAST",
                finding["extra"]["severity"],
                finding["check_id"],
                finding["extra"]["message"],
                finding["path"]
            ))

        return report

class TrivyParser(Parser):

    def parse(self):
        data = self.load_data()
        
        results = data["Results"]
        
        report = SecurityReport("Trivy", "SCA")
        for result in results:
            for vulnerability in result.get("Vulnerabilities", []):
                report.add_finding(Finding(
                    "Trivy",
                    "SCA",
                    vulnerability["Severity"],
                    vulnerability["VulnerabilityID"],
                    vulnerability["Title"],
                    result["Target"]
                ))
        
        return report

class GitleaksParser(Parser):

    def parse(self):
        data = self.load_data()

        report = SecurityReport("Gitleaks", "Secrets")

        for finding in data:
            report.add_finding(Finding(
                "Gitleaks",
                "Secrets",
                None,
                finding["RuleID"],
                finding["Description"],
                finding["File"]
            ))

        return report

    

