from modules.geo_api import GeoAPI

def main_menu():
    api = GeoAPI()

    while True:
        print("\n=== MENU ===")
        print("1️⃣   Rechercher la population par code (département ou commune)")
        print("0️⃣   Quitter")
        choice = input("\n👉 Choix : ").strip()

        if choice == "1":
            code = input("\n👉 Entrez un code (département à 2 chiffres ou postal à 5 chiffres) : ").strip()

            if code.isdigit() and len(code) in [2, 5]:
                population, nom, code_utilise = api.get_population_by_code(code)
                if population:
                    url_cp = f"https://www.code-postal.com/{code_utilise}.html"
                    print(f"\n➡️  Population de {nom} ({code_utilise}) : {population}")
                    print(f"➡️  Plus d'infos ? ce lien renvoie vers une carte qui montre la zone géographique éxacte de {nom} : {url_cp}\n")
                else:
                    print(f"\n❌ Aucune commune trouvée pour le code {code_utilise}.\n")
            else:
                print("\n❌ Entrée invalide. Veuillez entrer un code à 2 ou 5 chiffres uniquement (département ou commune).\n")
        elif choice == "0":
            print("\n👋 Au revoir !\n")
            break
        else:
            print("❌ Option invalide.")

if __name__ == "__main__":
    main_menu()
