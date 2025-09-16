import matplotlib.pyplot as plt
import argparse
from Trissone import Tris, Trissone, draw_board, draw_big_board, VocGiocatori

# Impostazione degli argomenti:
parser = argparse.ArgumentParser(description='Gioco Interattivo: Tic Tac Toe / Trissone')
parser.add_argument('--big', action='store_true', help='Usa il Trissone (Ultimate Tic Tac Toe)')
args = parser.parse_args()

# Inizializza il gioco in base alla modalità scelta:
if args.big:
    game = Trissone()
    interactive_big = True
else:
    game = Tris()
    interactive_big = False

# Variabile per tenere traccia del giocatore corrente:
# True -> "cerchio" (O), False -> "ics" (X)
current_player = True

def on_click(event):
    global game, current_player
    # Se il gioco è finito, non gestiamo ulteriori click
    if game.fine:
        print("Gioco terminato! Vincitore:", game.vincitore)
        return
    # Se il click è fuori dall'area (xdata o ydata None) lo ignoriamo
    if event.xdata is None or event.ydata is None:
        return

    if not interactive_big:
        # Modalità Tris: il tabellone è 3×3, coordinate da 0 a 3
        x, y = event.xdata, event.ydata
        if x < 0 or x > 3 or y < 0 or y > 3:
            return
        # La funzione draw_board posiziona i simboli con: 
        #   plt.text(j+0.5, 2.5-i, ...)  per cella (i,j) con i=0 riga superiore.
        # Dunque, calcoliamo:
        col = int(x)
        row = 2 - int(y)
        cell_index = row * 3 + col
        try:
            game.add(current_player, cell_index)
            draw_board(game.pos, game.tris, showtime=0)
            if not game.fine:
                current_player = not current_player
            else:
                print("Gioco terminato! Vincitore:", game.vincitore)
        except Exception as e:
            print(e)
    else:
        # Modalità Trissone: il tabellone è 9×9, composto da 9 mini board
        x, y = event.xdata, event.ydata
        if x < 0 or x > 9 or y < 0 or y > 9:
            return
        # Determiniamo il mini board in cui è stato cliccato:
        big_col = int(x // 3)
        # Per le righe, consideriamo che l'area del tabellone:
        #  y in [6,9]  -> mini board in alto (big_row = 0)
        #  y in [3,6]  -> mini board centrale (big_row = 1)
        #  y in [0,3]  -> mini board in basso (big_row = 2)
        if y >= 6:
            big_row = 0
        elif y >= 3:
            big_row = 1
        else:
            big_row = 2
        big_index = big_row * 3 + big_col

        # Calcoliamo l'offset (angolo inferiore sinistro) del mini board selezionato,
        # come fatto in draw_big_board:
        x_offset = big_col * 3
        y_offset = (2 - big_row) * 3

        # Calcoliamo le coordinate relative all'interno del mini board:
        x_rel = x - x_offset
        y_rel = y - y_offset
        if x_rel < 0 or x_rel > 3 or y_rel < 0 or y_rel > 3:
            return
        # Nel disegno, le celle sono disposte con:
        #   x: j + 0.5
        #   y: (2.5 - i) + y_offset, dove i=0 è la riga superiore.
        cell_col = int(x_rel)
        cell_row = 2 - int(y_rel)
        cell_index = cell_row * 3 + cell_col

        # Se il gioco ha imposto una restrizione (self.next non None),
        # il giocatore deve giocare nel mini board indicato.
        if game.next is not None and game.next != big_index:
            print(f"Devi giocare nel mini board {game.next}, non in {big_index}")
            return

        try:
            game.add(current_player, cell_index, big_index)
            draw_big_board(game, game.tris, showtime=0)
            if not game.fine:
                current_player = not current_player
            else:
                print("Gioco terminato! Vincitore:", game.vincitore)
        except Exception as e:
            print(e)

def main():
    fig = plt.figure(figsize=(8,8))
    if not interactive_big:
        draw_board(game.pos, showtime=0)
        plt.title("Tic Tac Toe Interattivo\n(Clicca sulla casella per fare la mossa)")
    else:
        draw_big_board(game, showtime=0)
        plt.title("Trissone Interattivo\n(Clicca sulla casella per fare la mossa)")
    fig.canvas.mpl_connect('button_press_event', on_click)
    plt.show()

if __name__ == "__main__":
    main()

