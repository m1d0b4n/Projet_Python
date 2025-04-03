import re
import os

RESERVED_NAMES = {
    'CON', 'PRN', 'AUX', 'NUL',
    *{f'COM{i}' for i in range(1, 10)},
    *{f'LPT{i}' for i in range(1, 10)}
}

def is_valid_excel_path(path):
    """
    Valide un chemin de fichier Excel :
    - Se termine par .xlsx
    - Ne contient pas de caractères interdits
    - Ne correspond pas à un nom réservé sous Windows
    """
    if not path.lower().endswith('.xlsx'):
        return False

    filename = os.path.basename(path)
    name_only = os.path.splitext(filename)[0].upper()

    if name_only in RESERVED_NAMES:
        return False

    invalid_chars_pattern = r'[<>:"/\\|?*]'
    if re.search(invalid_chars_pattern, filename):
        return False

    return True
