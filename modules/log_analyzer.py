import json
import os
import pandas as pd

class LogAnalyzer:
    def __init__(self, filepath):
        self.filepath = filepath
        self.entries = []

    def is_valid_path(self):
        return os.path.isfile(self.filepath)

    def load_logs(self):
        with open(self.filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
            self.entries = data.get("hits", {}).get("hits", [])

    def analyze_logs(self):
        errors = []
        warnings = []

        for entry in self.entries:
            source = entry.get("_source", {})
            level = source.get("log", {}).get("level", "").lower()
            if level == "error":
                errors.append(source)
            elif level == "warning":
                warnings.append(source)

        return errors, warnings

    def export_to_excel(self, logs, output_path):
        rows = []
        for log in logs:
            rows.append({
                "Nom de la station": log.get("host", {}).get("name", "Inconnu"),
                "Niveau de l'erreur": log.get("log", {}).get("level", "Inconnu"),
                "Message de l'erreur": log.get("message", "Non fourni")
            })

        df = pd.DataFrame(rows)
        df.to_excel(output_path, index=False)
