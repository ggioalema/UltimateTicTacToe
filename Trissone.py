import numpy as np
import argparse
import random as rnd
import matplotlib.pyplot as plt
import Utility as U


# Combinazioni vincenti (per mini board e per il Trissone)
PosizioniVincenti = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
]

# Vocabolario dei giocatori
VocGiocatori = {1: "cerchio", 2: "ics", 3: "pareggio"}




def draw_board(pos, winning_positions=None, showtime=0):
    """
    Disegna graficamente il tris:
      - pos: array 1D di 9 elementi (0: vuota, 1: O, 2: X)
      - winning_positions: se non None, evidenzia le celle vincenti e mostra il tris vincente
    """
    plt.clf()
    # Disegna simboli e griglia
    for i in range(3):
        for j in range(3):
            idx = i * 3 + j
            if pos[idx] == 1:
                simbolo = "O"
            elif pos[idx] == 2:
                simbolo = "X"
            else:
                simbolo = ""
            # Posizionamento: le righe vengono visualizzate dall'alto verso il basso
            plt.text(j + 0.5, 2.5 - i, simbolo, fontsize=40, ha='center', va='center')
    # Disegna le linee della griglia
    plt.plot([1, 1], [0, 3], color='black', linewidth=2)
    plt.plot([2, 2], [0, 3], color='black', linewidth=2)
    plt.plot([0, 3], [1, 1], color='black', linewidth=2)
    plt.plot([0, 3], [2, 2], color='black', linewidth=2)
    plt.xlim(0, 3)
    plt.ylim(0, 3)
    plt.axis('off')
    # Se la partita è finita e c'è un tris vincente, evidenzia le celle
    if winning_positions is not None:
        for idx in winning_positions:
            i = idx // 3
            j = idx % 3
            rect = plt.Rectangle((j, 2 - i), 1, 1, fill=False, edgecolor='red', linewidth=3)
            plt.gca().add_patch(rect)
        # Aggiunge una riga di testo sotto la griglia
        plt.figtext(0.5, 0.01, f"Tris vincente: {winning_positions}", ha="center", fontsize=16, color='red')
    plt.draw()
    plt.pause(showtime)

def draw_big_board(trissone, winning_positions_big=None, showtime=0):
    """
    Disegna graficamente il Trissone (Ultimate Tic Tac Toe).
      - trissone: istanza della classe Trissone
      - winning_positions_big: se non None, evidenzia (con rettangoli blu) i mini board vincenti e mostra il tris vincente
    """
    plt.clf()
    # L'intero tabellone è formato da una griglia 9x9 (ogni mini board è 3x3)
    # Disegna linee sottili (griglia interna di ogni mini board)
    for x in range(10):
        plt.plot([x, x], [0, 9], color='gray', linewidth=1)
    for y in range(10):
        plt.plot([0, 9], [y, y], color='gray', linewidth=1)
    # Disegna linee spesse per delimitare i 9 mini board
    for x in [0, 3, 6, 9]:
        plt.plot([x, x], [0, 9], color='black', linewidth=3)
    for y in [0, 3, 6, 9]:
        plt.plot([0, 9], [y, y], color='black', linewidth=3)
    
    # Disegna i simboli per ciascun mini board
    for big_idx, mini_board in enumerate(trissone.pos):
        big_row = big_idx // 3
        big_col = big_idx % 3
        # Calcola l'offset per il mini board corrente
        x_offset = big_col * 3
        y_offset = (2 - big_row) * 3  # in modo che la riga 0 appaia in alto
        for i in range(3):
            for j in range(3):
                mini_idx = i * 3 + j
                val = mini_board.pos[mini_idx]
                if val == 1:
                    simbolo = "O"
                elif val == 2:
                    simbolo = "X"
                else:
                    simbolo = ""
                # Coordinate all'interno del mini board
                x_coord = x_offset + j + 0.5
                y_coord = y_offset + (2.5 - i)
                plt.text(x_coord, y_coord, simbolo, fontsize=20, ha='center', va='center')
        # Se il mini board ha un tris vincente, evidenzia la combinazione (con rettangoli rossi)
        if mini_board.tris is not None:
            for idx in mini_board.tris:
                i = idx // 3
                j = idx % 3
                x_rect = x_offset + j
                y_rect = y_offset + (2 - i)
                rect = plt.Rectangle((x_rect, y_rect), 1, 1, fill=False, edgecolor='red', linewidth=2)
                plt.gca().add_patch(rect)
    
    # Se il Trissone è concluso con un tris a livello "grande", evidenzia i mini board vincenti
    if winning_positions_big is not None:
        for idx in winning_positions_big:
            big_row = idx // 3
            big_col = idx % 3
            x_offset = big_col * 3
            y_offset = (2 - big_row) * 3
            rect = plt.Rectangle((x_offset, y_offset), 3, 3, fill=False, edgecolor='blue', linewidth=3)
            plt.gca().add_patch(rect)
        plt.figtext(0.5, 0.01, f"Tris vincente nel Trissone: {winning_positions_big}", ha="center", fontsize=16, color='blue')
    
    plt.xlim(0, 9)
    plt.ylim(0, 9)
    plt.axis('off')
    plt.draw()
    plt.pause(showtime)

class Tris:
    '''
    Classe che definisce una partita di tris (mini board).
    Per convenzione, inizia sempre il cerchio.
    '''
    def __init__(self):
        self.pos = np.zeros(9, dtype=int)
        self.fine = False
        self.vincitore = 0
        self.tris = None  # Salva la combinazione vincente se presente

    def Check(self):
        if not self.fine:
            vinto = False
            for item in PosizioniVincenti:
                if self.pos[item[0]] == self.pos[item[1]] == self.pos[item[2]] != 0:
                    self.fine = True
                    self.vincitore = VocGiocatori[self.pos[item[0]]]
                    self.tris = item
                    vinto = True
                    break
            if (not vinto) and (0 not in self.pos):
                self.fine = True
                self.vincitore = VocGiocatori[3]

    def add(self, cerchio: bool, posizione: int):
        if posizione < 0 or posizione > 8:
            raise IndexError("Posizione non valida")
        if self.fine:
            raise IndexError("Tris già finito")
        if self.pos[posizione] != 0:
            raise IndexError("Posizione non valida")
        self.pos[posizione] = 1 if cerchio else 2
        self.Check()

class Trissone:
    '''
    Classe che definisce il Trissone (Ultimate Tic Tac Toe),
    composto da 9 mini board (Tris).
    '''
    def __init__(self):
        # Inizializza 9 mini board
        self.pos = np.array([Tris() for _ in range(9)])
        self.fine = False
        self.vincitore = 0
        self.next = None  # Indica l'indice del mini board in cui dovrà essere giocata la prossima mossa
        self.tris = None  # Salva la combinazione vincente a livello di Trissone

    def Check(self):
        # Aggiorna lo stato di ogni mini board
        for piccolo in self.pos:
            piccolo.Check()
        # Creiamo un array "stato" per i mini board: 0 se non concluso, 1 o 2 se vinto
        stato = np.zeros(9, dtype=int)
        for i, board in enumerate(self.pos):
            if board.vincitore == VocGiocatori[1]:
                stato[i] = 1
            elif board.vincitore == VocGiocatori[2]:
                stato[i] = 2
        # in caso di pareggio o ancora non finito rimane 0
        # Verifica se esiste un tris vincente a livello di mini board
        vinto = False
        for item in PosizioniVincenti:
            if stato[item[0]] == stato[item[1]] == stato[item[2]] != 0:
                self.fine = True
                self.vincitore = VocGiocatori[stato[item[0]]]
                self.tris = item  # Combinazione vincente (gli indici dei mini board)
                vinto = True
                break
        # Se tutti i mini board sono conclusi e non c'è un vincitore, il Trissone è un pareggio
        if (not vinto) and all(board.fine for board in self.pos):
            self.fine = True
            self.vincitore = VocGiocatori[3]

    def add(self, cerchio: bool, posizione: int, posGrande: int):
        """
        Aggiunge una mossa nel Trissone.
          - cerchio: True se gioca il cerchio, False se gioca "ics"
          - posizione: posizione (0-8) all'interno del mini board
          - posGrande: indice del mini board scelto (usato solo se self.next è None)
        """
        if posizione < 0 or posizione > 8:
            raise IndexError("Posizione non valida, out of bound")
        if self.fine:
            raise IndexError("Trissone già finito")

        # Determina in quale mini board effettuare la mossa:
        if self.next is None:
            self.next = posGrande

        elif posGrande != self.next:
            raise IndexError("Non è qui che devi giocare!!!")
        
        board_index = posGrande

        if (self.pos[board_index].fine):
            self.next=None
            raise IndexError("Tris piccolo già finito")

        mini_board = self.pos[board_index]
        if mini_board.pos[posizione] != 0:
            raise IndexError("Posizione non valida")
        # Aggiunge la mossa al mini board scelto
        mini_board.add(cerchio, posizione)
        # Imposta la prossima mossa nel mini board corrispondente alla cella appena giocata
        self.next = posizione
        if self.pos[self.next].fine:
            self.next=None

        self.Check()

def mainPiccolo(show, n):
    if show:
        plt.ion()  # Modalità interattiva
        fig = plt.figure(figsize=(8,8))
    
    x = range(n)
    yc, pareggi, yi = 0, 0, 0

    for partita_num in x:
        Partita = Tris()
        move = 0
        # Disegna lo stato iniziale (tutti i mini board vuoti)
        if show:
            draw_board(Partita, showtime = show)
        while not Partita.fine:
            try:
                cell = rnd.randint(0, 8)
                Partita.add(move % 2 == 0, cell)
                move += 1
                if show:
                    draw_board(Partita,showtime = show)
            except IndexError:
                continue
        # Disegna lo stato finale, evidenziando il tris vincente (se presente) a livello di Trissone
        if show:
            draw_board(Partita, showtime = show)
        U.BarraCaricamento(args.n, partita_num)
        if Partita.vincitore == VocGiocatori[1]:
            yc += 1
        elif Partita.vincitore == VocGiocatori[2]:
            yi += 1
        else:
            pareggi += 1

    print(f"\npareggi: {pareggi}\nics: {yi}\ncerchio: {yc}\ntot: {pareggi+yi+yc}")
    if show:
        plt.ioff()
        plt.show()



def main(show, n):
    if show:
        plt.ion()  # Modalità interattiva
        fig = plt.figure(figsize=(8,8))
    
    x = range(n)
    yc, pareggi, yi = 0, 0, 0

    for partita_num in x:
        Partita = Trissone()
        move = 0
        # Disegna lo stato iniziale (tutti i mini board vuoti)
        if show:
            draw_big_board(Partita, showtime = show)
        while not Partita.fine:
            try:

                # Se non c'è una restrizione, scegliamo un mini board a caso
                posGrande = rnd.randint(0, 8)
                
                cell = rnd.randint(0, 8)
                Partita.add(move % 2 == 0, cell, posGrande)
                move += 1
                if show:
                    draw_big_board(Partita, showtime = show)
            except IndexError:
                continue
        # Disegna lo stato finale, evidenziando il tris vincente (se presente) a livello di Trissone
        if show:
            draw_big_board(Partita, Partita.tris, show)
        U.BarraCaricamento(args.n, partita_num)
        if Partita.vincitore == VocGiocatori[1]:
            yc += 1
        elif Partita.vincitore == VocGiocatori[2]:
            yi += 1
        else:
            pareggi += 1

    print(f"\npareggi: {pareggi}\nics: {yi}\ncerchio: {yc}\ntot: {pareggi+yi+yc}")
    if show:
        plt.ioff()
        plt.show()

if __name__ == "__main__":

    # Impostazione degli argomenti
    parser = argparse.ArgumentParser(description='Statistica partite di Trissone (Ultimate Tic Tac Toe)')
    parser.add_argument('-n', type=int, default=100, help='Numero di partite per la statistica')
    parser.add_argument('-show', type=float, default=0, help='Mostra le grafiche della partita')
    parser.add_argument('-Piccolo', action='store_true', help='Mostra le grafiche della partita')
    args = parser.parse_args()

    if args.Piccolo:
        mainPiccolo(args.show, args.n)
    else:
        main(args.show, args.n)

