from modules.geo_api import GeoAPI
from modules.ascii_art import ascii_printer
from modules.log_analyzer import LogAnalyzer
from utils.validators import is_valid_excel_path
from getpass import getpass
from modules.system_diag import SystemDiagSSH


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
                    break  # sortie de la boucle après traitement
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
                print(f"\n✳️ {len(errors)} erreurs & {len(warnings)} avertissements trouvés.")

                while True:
                    export = input("\n📁 Voulez-vous exporter ces logs dans un fichier Excel ? (oui/non) : ").strip().lower()
                    if export in ["oui", "o", "yes", "y"]:
                        while True:
                            out_path = input("\n👉 Entrez le chemin de sortie du fichier Excel (ex : ./export.xlsx) : ").strip()
                            if is_valid_excel_path(out_path):
                                try:
                                    analyzer.export_to_excel(errors + warnings, out_path)
                                    print(f"\n✳️ Export terminé avec succès : {out_path}")
                                except Exception as e:
                                    print(f"\n❌ Erreur lors de l'export : {e}")
                                break
                            else:
                                print("\n❌ Chemin invalide. Le fichier doit se terminer par .xlsx, ne pas contenir de caractères interdits et ne pas être un nom réservé.")
                        break
                    elif export in ["non", "n", "no"]:
                        print("\n❌ Export annulé par l'utilisateur.")
                        break
                    else:
                        print("\n❌ Entrée invalide. Répondez par 'oui' ou 'non'.")
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

                while True:
                    export = input("\n📁 Voulez-vous enregistrer ce diagnostic dans un fichier Excel ? (oui/non) : ").strip().lower()
                    if export in ["oui", "o", "yes", "y"]:
                        while True:
                            out_path = input("\n👉 Entrez le chemin du fichier Excel (ex : ./status.xlsx) : ").strip()
                            if is_valid_excel_path(out_path):
                                try:
                                    diag.export_to_excel(out_path)
                                    print(f"\n✳️  Export terminé avec succès : {out_path}")
                                except Exception as e:
                                    print(f"\n❌ Erreur lors de l'export : {e}")
                                break
                            else:
                                print("\n❌ Chemin invalide. Le fichier doit avoir une extension .xlsx, sans caractères interdits.")
                        break
                    elif export in ["non", "n", "no"]:
                        print("\n❌ Export annulé par l'utilisateur.")
                        break
                    else:
                        print("\n❌ Entrée invalide. Répondez par 'oui' ou 'non'.")

# ------| Choix 0 |------------------------------------------
        elif choice == "0":
            print("\n👋 Au revoir !\n")
            break

# ------| Choix inexistants |--------------------------------
        else:
            print("\n❌ Option invalide.")


if __name__ == "__main__":
    main_menu()
