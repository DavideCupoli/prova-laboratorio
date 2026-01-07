import os
from pathlib import Path
import csv
import json

# 1) Scrivere un messaggio in un file
def snippet_1_path_write(nome_file):
    messaggio = "Ciao mondo!\nQuesta è la seconda riga.\n"
    
    Path(nome_file).write_text(messaggio, encoding='utf-8') # utf-8 ci serve per i caratteri con l'accento, emoji ecc
    
    print(f"File '{nome_file}' creato")


# 2) Lettura tutta in una volta
def snippet_2_path_read(nome_file):
    # Controlla se esiste
    p = Path(nome_file)
    if not p.exists():
        print("File non trovato!")
        return
    
    contenuto = p.read_text(encoding='utf-8') # utf-8 ci serve per i caratteri con l'accento, emoji ecc
    
    print("Ho letto:")
    print(contenuto)
    print(f"Lunghezza: {len(contenuto)} caratteri")

# 3) Modo alternativo con "open"
def snippet_3_open(nome_file):
    messaggio = "PYTHON"
    
    # Modalità
    # 'w' = Write: sostituisce il file se esisteva già
    # 'a' = Append: aggiunge alla fine del file

    # Per leggere: usare 'r' e i metodi f.read()
    with open(nome_file, 'w', encoding='utf-8') as f:
        for carattere in messaggio:
            # Scrivo un carattere o una stringa alla volta
            f.write(carattere)
    
    print(f"File {nome_file} creato carattere per carattere")

# 4) CSV - Scrittura
def snippet_4_csv_write():
    
    # Dati: lista di studenti con nome e voto
    studenti = [
        ['Alice', 6],
        ['Bob', 7],
        ['Charlie', 8],
        ['Diana', 9]
    ]
    
    with open('studenti.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Intestazione (nomi delle colonne)
        writer.writerow(['nome', 'voto'])
        
        # Dati
        writer.writerows(studenti)
    
    print("File 'studenti.csv' creato")


# 5) CSV - Lettura
def snippet_5_csv_read():

    # Modo alternativo per vedere se un file esiste
    if not os.path.exists('studenti.csv'):
        print("Il file 'studenti.csv' non esiste ancora!")
    
    with open('studenti.csv', 'r', encoding='utf-8') as f:
        # DictReader usa la prima riga come intestazione
        reader = csv.DictReader(f)
        
        for riga in reader:
            nome = riga['nome']
            voto = int(riga['voto'])
            print(f"  {nome}: {voto}/10")
    
# 6: JSON (JavaScript Object Notation) - Scrittura 
def snippet_6_json_write():
    
    # Struttura complessa (dizionario con liste annidate)
    gioco = {
        'giocatore': 'Mario',
        'livello': 5,
        'inventario': ['spada', 'pozione', 'chiave'],
        'statistiche': {
            'vita': 80,
            'mana': 50,
            'forza': 15
        },
        'nemici_sconfitti': ['goblin', 'troll', 'drago']
    }
    
    with open('savegame.json', 'w', encoding='utf-8') as f:
        # indent=4 rende il JSON leggibile (con indentazione)
        json.dump(gioco, f, indent=4)
    
    print("File 'savegame.json' creato")


# 8: JSON - Lettura

def snippet_7_json_read():
    """Leggere strutture complesse da JSON"""
    if not Path('savegame.json').exists():
        print("File non trovato!")
        return
    
    try:
        with open('savegame.json', 'r', encoding='utf-8') as f:
            gioco = json.load(f)
        
        print(f"Giocatore: {gioco['giocatore']}")
        print(f"Livello: {gioco['livello']}")
        print(f"Inventario: {', '.join(gioco['inventario'])}")
        print(f"Vita: {gioco['statistiche']['vita']}/100")
        print(f"Nemici sconfitti: {len(gioco['nemici_sconfitti'])}")
    
    except json.JSONDecodeError as e:
        print(f"JSON corrotto! Errore alla riga {e.lineno}: {e.msg}")
    except KeyError as e:
        print(f"Chiave mancante nel JSON: {e}")


if __name__ == "__main__":
    nome_file = input("Inserisci il nome del file:")
    snippet_1_path_write(nome_file)
    # snippet_2_path_read(nome_file)
    # snippet_3_open(nome_file)
    # snippet_4_csv_write()
    # snippet_5_csv_read()
    # snippet_6_json_write()
    # snippet_7_json_read()
    