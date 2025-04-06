from utils.validators import is_valid_excel_path

def handle_excel_export(export_fn, label="fichier Excel"):
    while True:
        export = input(f"\n📁 Voulez-vous exporter dans un {label} ? (oui/non) : ").strip().lower()
        if export in ["oui", "o", "yes", "y"]:
            while True:
                out_path = input(f"\n👉 Entrez le chemin de sortie du {label} (ex : ./export.xlsx) : ").strip()
                if is_valid_excel_path(out_path):
                    try:
                        export_fn(out_path)
                        print(f"\n✅ Export terminé avec succès : {out_path}")
                    except Exception as e:
                        print(f"\n❌ Erreur lors de l'export : {e}")
                    break
                else:
                    print("\n❌ Chemin invalide. Vérifiez l'extension .xlsx et les caractères interdits.")
            break
        elif export in ["non", "n", "no"]:
            print(f"\n❌ Export annulé par l'utilisateur.")
            break
        else:
            print("\n❌ Entrée invalide. Répondez par 'oui' ou 'non'.")
