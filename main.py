from modules.geo_api import GeoAPI

def main_menu():
    api = GeoAPI()

    while True:
        print("\n=== MENU ===")
        print("1. Rechercher la population par code (département ou commune)")
        print("2. Quitter")
        choice = input("Choix : ")

        if choice == "1":
            code = input("Entrez un code (département ou commune) : ")
            if len(code) == 2 and code.isdigit():
                population = api.get_population_by_departement(code)
                if population:
                    print(f"Population du département {code} : {population}")
                else:
                    print("Département non trouvé.")
            elif len(code) == 5 and code.isdigit():
                population = api.get_population_by_commune(code)
                if population:
                    print(f"Population de la commune {code} : {population}")
                else:
                    print("Commune non trouvée.")
            else:
                print("Code invalide. Entrez 2 ou 5 chiffres.")

        elif choice == "2":
            print("Au revoir.")
            break

        else:
            print("Option invalide.")

if __name__ == "__main__":
    main_menu()
