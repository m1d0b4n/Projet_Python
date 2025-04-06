from modules.geo_api import GeoAPI
from modules.ascii_art import ascii_printer
from modules.log_analyzer import LogAnalyzer
from getpass import getpass
from modules.system_diag import SystemDiagSSH
from utils.exporter import handle_excel_export

# ------| Lancement du programme |--------------------------
def main_menu():
    ascii_printer()
    api = GeoAPI()

# ------| Menu |--------------------------------------------
    while True:
        print("\n=======| MENU |===================================================\n")
        print("1️⃣   Rechercher la population par code (département ou commune)")
        print("2️⃣   Traiter un fichier de logs .json")
        print("3️⃣   Diagnostic système distant via SSH")
        print("\n0️⃣   Quitter")
        choice = input("\n👉 Choix : ").strip()

# ------| Choix 1 |-----------------------------------------
        if choice == "1":
            while True:
                code = input("\n👉 Entrez un code (département à 2 chiffres ou postal à 5 chiffres) : ").strip()

                if code.isdigit() and len(code) in [2, 5]:
                    population, nom, code_utilise = api.get_population_by_code(code)
                    if population:
                        url_cp = f"https://www.code-postal.com/{code_utilise}.html"
                        print(f"\n✳️  Population de {nom} ({code_utilise}) : {population}")
                        print(f"✳️  Plus d'infos ?  {url_cp} (carte de la zone géographique exacte de {nom})")
                    else:
                        print(f"\n❌ Aucune commune trouvée pour le code {code_utilise}.\n")
                    break
                else:
                    print("\n❌ Entrée invalide. Veuillez entrer un code à 2 ou 5 chiffres uniquement (département ou commune).")

# ------| Choix 2 |-----------------------------------------
        elif choice == "2":
            while True:
                path = input("\n👉 Entrez le chemin du fichier JSON de logs à analyser (ex : ./data/logs.json) : ").strip()
                analyzer = LogAnalyzer(path)

                if analyzer.is_valid_path():
                    break
                else:
                    print("\n❌ Chemin invalide ou fichier introuvable. Veuillez réessayer.")

            try:
                analyzer.load_logs()
                errors, warnings = analyzer.analyze_logs()
                print(f"\n✅ {len(errors)} erreurs & {len(warnings)} avertissements trouvés.")

                handle_excel_export(lambda p: analyzer.export_to_excel(errors + warnings, p), label="fichier Excel des logs")

            except Exception as e:
                print(f"\n❌ Une erreur est survenue pendant l’analyse : {e}")

# ------| Choix 3 |------------------------------------------
        elif choice == "3":
            print("\n👉 Connexion SSH pour diagnostic distant")
            host = input("\n👉 Adresse IP ou nom de domaine de la machine distante : ").strip()
            user = input("\n👉 Nom d'utilisateur : ").strip()
            password = getpass("   Mot de passe : ")

            diag = SystemDiagSSH(host, user, password)
            if diag.connect():
                diag.collect_info()
                diag.print_summary()
                handle_excel_export(diag.export_to_excel, label="diagnostic système")

# ------| Choix 0 |------------------------------------------
        elif choice == "0":
            print("\n👋 Au revoir !\n")
            break

# ------| Choix inexistants |--------------------------------
        else:
            print("\n❌ Option invalide.")


if __name__ == "__main__":
    main_menu()
