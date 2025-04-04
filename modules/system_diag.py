from fabric import Connection
import pandas as pd
import datetime
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

    def run_command(self, label, command):
        try:
            result = self.conn.run(command, hide=True, warn=True)
            self.results[label] = result.stdout.strip()
        except Exception:
            self.results[label] = None
            self.failures.append(label)

    def collect_info(self):
        cmds = {
            "OS": "uname -a",
            "CPU": "lscpu",
            "RAM": "free -h",
            "TOP_RAM_Procs": "ps aux --sort=-%mem | head -n 6",
            "ENV_VARS": "printenv",
            "DISKS": "lsblk",
            "DISK_USAGE": "df -h",
            "NETWORK_INTERFACES": "ip -o link show | awk -F': ' '{print $2}'",
            "BOOT_TIME": "who -b | awk '{print $3, $4}'"
        }
        for label, cmd in cmds.items():
            self.run_command(label, cmd)

    def print_summary(self):
        if self.failures:
            print("\n🚨 Certaines informations n'ont pas pu être récupérées :")
            for label in self.failures:
                print(f"  ❌ {label}")
        else:
            print("\n✅ Diagnostic complété avec succès !")

    def export_to_excel(self, path):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        rows = [{"Clé": k, "Valeur": v, "Date": now} for k, v in self.results.items() if v]

        df = pd.DataFrame(rows)
        sheet_name = "System status"

        file_exists = os.path.exists(path)

        if file_exists:
            with pd.ExcelWriter(path, engine='openpyxl', mode='a', if_sheet_exists='new') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        else:
            with pd.ExcelWriter(path, engine='openpyxl', mode='w') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
