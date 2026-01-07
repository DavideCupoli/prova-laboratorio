"""
Palline Rimbalzanti
- Click per aggiungere palline random
- S: Salva con JSON 
- L: Carica lo stato precedente
"""

"""
ESPERIMENTI DA PROVARE:"
1. Crea alcune palline e salva (S)
2. Apri 'palline.json' e modifica un colore
3. Ricarica (L) e vedi le modifiche!
4. Cancella una virgola dal JSON → errore al caricamento
"""

"""
Esercitazione:
- Aggiungi l'attributo "raggio" all'interno della singola pallina
- Gestisci anche il costruttore __init__, e i vari metodi dentro la classe Pallina
- Modifica anche crea_pallina_da_dizionario
- Ad ogni collisione con un'altra pallina, il raggio diminuisce di 1
- Se il raggio della pallina è minore di 5, toglila dalla lista
- Cambia il nome del file in cui vengono salvate le palline in "palline_2.json"
- Confronta i 2 file: cosa è cambiato?

"""

import math
import arcade
import random
import json
import os

LARGHEZZA = 800
ALTEZZA = 600
VELOCITA_MAX = 5
RAGGIO = 20

class Pallina:
    def __init__(self, x, y, vx, vy, colore, raggio):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.colore = colore 
        self.raggio = raggio
    
    def aggiorna(self):
        self.x += self.vx
        self.y += self.vy
        
        # Rimbalzo sui bordi
        if self.x - self.raggio < 0 or self.x + self.raggio > LARGHEZZA:
            self.vx *= -1
            self.x = max(self.raggio, min(self.x, LARGHEZZA - self.raggio))
        
        if self.y - self.raggio < 0 or self.y + self.raggio > ALTEZZA:
            self.vy *= -1
            self.y = max(self.raggio, min(self.y, ALTEZZA - self.raggio))
    
    def disegna(self):
        arcade.draw_circle_filled(self.x, self.y, self.raggio, self.colore)
    
    def controlla_collisione(self, altra):
        dx = self.x - altra.x
        dy = self.y - altra.y
        distanza = (dx**2 + dy**2)**0.5
        
        if distanza < self.raggio * 2:
            self.vx, altra.vx = altra.vx, self.vx
            self.vy, altra.vy = altra.vy, self.vy
            
            offset = (self.raggio * 2 - distanza) / 2 + 1
            self.x += offset * (dx / distanza)
            self.y += offset * (dy / distanza)
            altra.x -= offset * (dx / distanza)
            altra.y -= offset * (dy / distanza)

            self.raggio -= 1

    def to_dict(self):
        # Converte la pallina in un dizionario (per JSON)
        return {
            'x': self.x,
            'y': self.y,
            'vx': self.vx,
            'vy': self.vy,
            'colore': list(self.colore)  # JSON vuole liste, non tuple (le tuple le vedremo, pensale come liste ma "costanti")
        }
    

def crea_pallina_da_dizionario(self, dati):
    """Ricrea una pallina da un dizionario"""
    return Pallina(
        dati['x'],
        dati['y'],
        dati['vx'],
        dati['vy'],
        tuple(dati['colore']),  # Riconvertiamo in tupla
        RAGGIO
    )
class GiocoPalline(arcade.Window):
    def __init__(self):
        super().__init__(LARGHEZZA, ALTEZZA, "Palline")
        self.palline = []
        arcade.set_background_color(arcade.color.BLACK)
    
    def on_draw(self):
        self.clear()
        
        for pallina in self.palline:
            pallina.disegna()
        
        # Istruzioni
        arcade.draw_text(
            "Click: Aggiungi | S: Salva JSON | L: Carica JSON",
            10, ALTEZZA - 30, arcade.color.WHITE, 14
        )
        arcade.draw_text(
            f"Palline: {len(self.palline)}",
            10, ALTEZZA - 55, arcade.color.YELLOW, 14
        )
    
    def on_update(self, delta_time):
        for pallina in self.palline:
            pallina.aggiorna()
        
        for i in range(len(self.palline)):
            for j in range(i + 1, len(self.palline)):
                if self.palline[j] != None and self.palline[i] != None:
                    self.palline[i].controlla_collisione(self.palline[j])
                    if self.palline[i].raggio < 10:
                        self.palline[i] = None
        
        while None in self.palline:
            self.palline.remove(None)
            print('Pallina scomparsa')
    
    def on_mouse_press(self, x, y, button, modifiers):
        colore = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255)
        )
        vx = random.uniform(-VELOCITA_MAX, VELOCITA_MAX) # Numero a caso tra i due estremi
        vy = random.uniform(-VELOCITA_MAX, VELOCITA_MAX)
        
        self.palline.append(Pallina(x, y, vx, vy, colore, RAGGIO))
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.S:
            self.salva_json()
        elif key == arcade.key.L:
            self.carica_json()
    
    def salva_json(self):
        nome_file = "palline.json"
        
        try:
            # Converti ogni pallina in un dizionario
            dati = []
            
            for p in self.palline:
                dati.append(p.to_dict())
            
            with open(nome_file, 'w', encoding='utf-8') as f:
                # indent=4 rende il JSON leggibile (con indentazione)
                json.dump(dati, f, indent=4)
            
            print(f"Salvate {len(self.palline)} palline in '{nome_file}'")
        
        except Exception as e:
            print(f"Errore JSON: {e}")
    
    def carica_json(self):
        nome_file = "palline.json"
        
        if not os.path.exists(nome_file):
            print(f"File '{nome_file}' non trovato! Salva prima con S.")
            return
        
        # Questo costrutto "try"/"except" non l'abbiamo ancora visto... Per te cosa fa?
        try:
            with open(nome_file, 'r', encoding='utf-8') as f:
                dati = json.load(f)
            
            # Ricostruisci le palline dai dizionari
            self.palline = []
            
            for d in dati:
                self.palline.append(crea_pallina_da_dizionario(d))

            print(f"Caricate {len(self.palline)} palline")
        
        except json.JSONDecodeError as e:
            print(f"JSON corrotto! Errore alla linea {e.lineno}: {e.msg}")
        except Exception as e:
            print(f"Errore caricamento JSON: {e}")


def main():
    gioco = GiocoPalline()
    arcade.run()

if __name__ == "__main__":
    main()

