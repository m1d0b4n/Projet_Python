from modules.geo_api import GeoAPI
from modules.ascii_art import ascii_printer
from modules.log_analyzer import LogAnalyzer

# ------| Lancement du programme |--------------------------
def main_menu():
    ascii_printer()
    api = GeoAPI()

# ------| Menu |--------------------------------------------
    while True:
        print("\n=======| MENU |===================================================\n")
        print("1️⃣   Rechercher la population par code (département ou commune)")
        print("2️⃣   Traiter un fichier de logs .json")
        print("\n0️⃣   Quitter")
        choice = input("\n👉 Choix : ").strip()

# ------| Choix 1 |-----------------------------------------
        if choice == "1":
            code = input("\n👉 Entrez un code (département à 2 chiffres ou postal à 5 chiffres) : ").strip()

            if code.isdigit() and len(code) in [2, 5]:
                population, nom, code_utilise = api.get_population_by_code(code)
                if population:
                    url_cp = f"https://www.code-postal.com/{code_utilise}.html"
                    print(f"\n✳️  Population de {nom} ({code_utilise}) : {population}")
                    print(f"✳️  Plus d'infos ?  {url_cp} (carte de la zone géographique éxacte de {nom})")
                else:
                    print(f"\n❌ Aucune commune trouvée pour le code {code_utilise}.\n")
            else:
                print("\n❌ Entrée invalide. Veuillez entrer un code à 2 ou 5 chiffres uniquement (département ou commune).")
        
# ------| Choix 2 |-----------------------------------------
        elif choice == "2":
            path = input("\n👉 Entrez le chemin du fichier JSON de logs à analyser (ex : ./data/logs.json) : ").strip()
            analyzer = LogAnalyzer(path)

            if not analyzer.is_valid_path():
                print("\n❌ Chemin invalide ou fichier introuvable.")
                continue

            try:
                analyzer.load_logs()
                errors, warnings = analyzer.analyze_logs()
                print(f"\n✅ {len(errors)} erreurs & {len(warnings)} avertissements trouvés.")

                export = input("\n📁 Voulez-vous exporter ces logs dans un fichier Excel ? (oui/non) : ").strip().lower()
                if export in ["oui", "o", "yes", "y"]:
                    out_path = input("\n👉 Entrez le chemin de sortie du fichier Excel (ex : ./data/extract.xlsx) : ").strip()
                    try:
                        analyzer.export_to_excel(errors + warnings, out_path)
                        print(f"\n✅ Export terminé avec succès : {out_path}")
                    except Exception as e:
                        print(f"\n❌ Erreur lors de l'export : {e}")
                else:
                    print("\n❌ Export annulé par l'utilisateur.")
            except Exception as e:
                print(f"\n❌ Une erreur est survenue pendant l’analyse : {e}")

# ------| Choix 0 |------------------------------------------
        elif choice == "0":
            print("\n👋 Au revoir !\n")
            break

# ------| Choix inexistants |--------------------------------
        else:
            print("\n❌ Option invalide.")


if __name__ == "__main__":
    main_menu()
