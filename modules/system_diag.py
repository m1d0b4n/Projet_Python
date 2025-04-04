from fabric import Connection
import pandas as pd
import os

class SystemDiagSSH:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.conn = None
        self.results = {}
        self.failures = []

    def connect(self):
        try:
            self.conn = Connection(
                host=self.host,
                user=self.user,
                connect_kwargs={"password": self.password},
                connect_timeout=10
            )
            self.conn.open()
            return True
        except Exception as e:
            print(f"\n❌ Connexion SSH échouée : {e}")
            return False

    def run_command(self, label, command, parse=False):
        try:
            result = self.conn.run(command, hide=True, warn=True, encoding='utf-8')
            output = result.stdout.strip()
            if parse and label == "CPU":
                parsed = {}
                for line in output.splitlines():
                    if ":" in line:
                        key, value = line.split(":", 1)
                        parsed[key.strip()] = value.strip()
                self.results[label] = parsed
            else:
                self.results[label] = output
        except Exception:
            self.results[label] = None
            self.failures.append(label)

    def collect_info(self):
        cmds = {
            "OS": ("uname -srmo", False),
            "CPU": ("lscpu | grep -E \"Nom|Architecture|Processeur\"", True),
            "RAM": ("free -h | grep Mem", False),
            "Bigs process": ("ps -eo pid,comm,%mem --sort=-%mem | head -n 6", False),
            "Env variable": ("printenv | grep -E \"^(PATH|HOME|USER)=\"", False),
            "Disks": ("lsblk -o NAME,SIZE,TYPE,MOUNTPOINT", False),
            "Disk usage": ("df -h --output=source,size,used,avail,pcent,target", False),
            "Network interfaces": ("ip -o link show | awk -F': ' '{print $2}'", False),
            "Boot time": ("who -b | awk '{print $3, $4}'", False)
        }
        for label, (cmd, parse) in cmds.items():
            self.run_command(label, cmd, parse=parse)

    def print_summary(self):
        if self.failures:
            print("\n🚨 Certaines informations n'ont pas pu être récupérées :")
            for label in self.failures:
                print(f"  ❌ {label}")
        else:
            print("\n✅ Diagnostic complété avec succès !")

    def export_to_excel(self, path):
        data = {label: self.results.get(label, "N/A") for label in [
            "OS", "CPU", "RAM", "Bigs process", "Env variable",
            "Disks", "Disk usage", "Network interfaces", "Boot time"
        ]}
        # Formater joliment les dicts (comme CPU)
        for key, val in data.items():
            if isinstance(val, dict):
                data[key] = '\n'.join(f"{k} : {v}" for k, v in val.items())
        data = {"IP target": self.host, **data}

        df = pd.DataFrame([data])

        sheet_name = "System status"
        file_exists = os.path.exists(path)

        if file_exists:
            with pd.ExcelWriter(path, engine='openpyxl', mode='a', if_sheet_exists='new') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        else:
            with pd.ExcelWriter(path, engine='openpyxl', mode='w') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
