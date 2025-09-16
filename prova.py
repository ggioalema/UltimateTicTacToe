import pygame
import sys
import numpy as np
from Trissone import Tris, Trissone

pygame.init()

# Dimensioni della finestra e della griglia
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe/Trissone Interattivo con Pygame")
clock = pygame.time.Clock()

# Colori e costanti
BG_COLOR = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
CELL_SIZE = WIDTH // 3
LINE_WIDTH = 10

BLUE = (0, 0, 255)   # Cerchio
RED = (255, 0, 0)    # Ics (X)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)

# Vocabolario per i giocatori
VocGiocatori = {1: "cerchio", 2: "ics", 3: "pareggio"}

# Definizione dei rettangoli per i due pulsanti
button1_rect = pygame.Rect(150, 200, 300, 80)  # Pulsante 1
button2_rect = pygame.Rect(150, 320, 300, 80)  # Pulsante 2

# Font
font = pygame.font.SysFont(None, 48)
error_font = pygame.font.SysFont(None, 36)

# Variabili globali per il messaggio d'errore
error_message = ""
error_expire_time = 0

def set_error(message, duration=2000):
    """Imposta un messaggio d'errore non bloccante da mostrare per 'duration' millisecondi."""
    global error_message, error_expire_time
    error_message = message
    error_expire_time = pygame.time.get_ticks() + duration

def display_error(screen):
    """Disegna il messaggio d'errore, se impostato e non scaduto, sullo schermo."""
    global error_message, error_expire_time
    current_time = pygame.time.get_ticks()
    if error_message and current_time < error_expire_time:
        text_surface = error_font.render(error_message, True, (255, 0, 0))
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text_surface, text_rect)
    elif current_time >= error_expire_time:
        error_message = ""  # Resetta il messaggio dopo la scadenza

def draw_board(screen, game):
    """Disegna il tabellone classico 3x3 (Tris)."""
    screen.fill(BG_COLOR)
    # Disegna la griglia principale
    pygame.draw.line(screen, LINE_COLOR, (CELL_SIZE, 0), (CELL_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * CELL_SIZE, 0), (2 * CELL_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, CELL_SIZE), (WIDTH, CELL_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * CELL_SIZE), (WIDTH, 2 * CELL_SIZE), LINE_WIDTH)
    
    # Disegna i simboli
    for idx, val in enumerate(game.pos):
        row = idx // 3
        col = idx % 3
        center_x = col * CELL_SIZE + CELL_SIZE // 2
        center_y = row * CELL_SIZE + CELL_SIZE // 2
        if val == 1:
            pygame.draw.circle(screen, BLUE, (center_x, center_y), CELL_SIZE // 3, LINE_WIDTH)
        elif val == 2:
            offset = CELL_SIZE // 3
            start_pos1 = (col * CELL_SIZE + offset, row * CELL_SIZE + offset)
            end_pos1   = ((col + 1) * CELL_SIZE - offset, (row + 1) * CELL_SIZE - offset)
            start_pos2 = (col * CELL_SIZE + offset, (row + 1) * CELL_SIZE - offset)
            end_pos2   = ((col + 1) * CELL_SIZE - offset, row * CELL_SIZE + offset)
            pygame.draw.line(screen, RED, start_pos1, end_pos1, LINE_WIDTH)
            pygame.draw.line(screen, RED, start_pos2, end_pos2, LINE_WIDTH)
    
    # Evidenzia la combinazione vincente, se esiste
    if game.tris is not None:
        for idx in game.tris:
            row = idx // 3
            col = idx % 3
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, (0, 255, 0), rect, 5)

def draw_big_board(screen, game):
    """
    Disegna il Trissone (Ultimate Tic Tac Toe).
    'game' è un'istanza della classe Trissone che contiene 9 mini board (ogni mini board è un Tris).
    """
    screen.fill(BG_COLOR)
    mini_size = WIDTH // 3      # Dimensione in pixel di ogni mini board
    cell_size = mini_size // 3   # Dimensione in pixel di ogni cella interna al mini board

    # Disegna le linee spesse che separano i mini board
    pygame.draw.line(screen, LINE_COLOR, (mini_size, 0), (mini_size, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * mini_size, 0), (2 * mini_size, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, mini_size), (WIDTH, mini_size), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * mini_size), (WIDTH, 2 * mini_size), LINE_WIDTH)
    
    # Per ogni mini board
    for big_idx in range(9):
        mini_board = game.pos[big_idx]  # Oggetto Tris
        big_row = big_idx // 3
        big_col = big_idx % 3
        x_offset = big_col * mini_size
        y_offset = big_row * mini_size
        
        # Disegna la griglia interna del mini board (linee sottili)
        mini_line_width = 3
        pygame.draw.line(screen, LINE_COLOR, (x_offset + cell_size, y_offset), (x_offset + cell_size, y_offset + mini_size), mini_line_width)
        pygame.draw.line(screen, LINE_COLOR, (x_offset + 2 * cell_size, y_offset), (x_offset + 2 * cell_size, y_offset + mini_size), mini_line_width)
        pygame.draw.line(screen, LINE_COLOR, (x_offset, y_offset + cell_size), (x_offset + mini_size, y_offset + cell_size), mini_line_width)
        pygame.draw.line(screen, LINE_COLOR, (x_offset, y_offset + 2 * cell_size), (x_offset + mini_size, y_offset + 2 * cell_size), mini_line_width)
        
        # Disegna i simboli all'interno del mini board
        for idx, val in enumerate(mini_board.pos):
            row = idx // 3
            col = idx % 3
            center_x = x_offset + col * cell_size + cell_size // 2
            center_y = y_offset + row * cell_size + cell_size // 2
            if val == 1:
                pygame.draw.circle(screen, BLUE, (center_x, center_y), cell_size // 3, mini_line_width)
            elif val == 2:
                offset = cell_size // 3
                start_pos1 = (x_offset + col * cell_size + offset, y_offset + row * cell_size + offset)
                end_pos1   = (x_offset + (col + 1) * cell_size - offset, y_offset + (row + 1) * cell_size - offset)
                start_pos2 = (x_offset + col * cell_size + offset, y_offset + (row + 1) * cell_size - offset)
                end_pos2   = (x_offset + (col + 1) * cell_size - offset, y_offset + row * cell_size + offset)
                pygame.draw.line(screen, RED, start_pos1, end_pos1, mini_line_width)
                pygame.draw.line(screen, RED, start_pos2, end_pos2, mini_line_width)
        
        # Se il mini board ha un tris vincente, evidenzia le celle vincenti
        if mini_board.tris is not None:
            for idx in mini_board.tris:
                r = idx // 3
                c = idx % 3
                rect = pygame.Rect(x_offset + c * cell_size, y_offset + r * cell_size, cell_size, cell_size)
                pygame.draw.rect(screen, (0, 255, 0), rect, 3)
    
    # Se il Trissone è vinto globalmente, evidenzia i mini board vincenti
    if game.tris is not None:
        for big_idx in game.tris:
            big_row = big_idx // 3
            big_col = big_idx % 3
            x_offset = big_col * mini_size
            y_offset = big_row * mini_size
            rect = pygame.Rect(x_offset, y_offset, mini_size, mini_size)
            pygame.draw.rect(screen, (0, 0, 255), rect, 5)

def gameLoop(bigMode):
    """Loop principale del gioco."""
    if bigMode:
        game = Trissone()
    else:
        game = Tris()
    
    current_player = True  # True per il cerchio, False per l'ics; il cerchio inizia
    running = True

    # In base alla modalità scelta, usiamo la funzione di disegno corretta
    draw_function = draw_big_board if bigMode else draw_board

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN and not game.fine:
                x, y = pygame.mouse.get_pos()
                if not bigMode:
                    col = x // CELL_SIZE
                    row = y // CELL_SIZE
                    cell_index = row * 3 + col
                    try:
                        game.add(current_player, cell_index)
                        current_player = not current_player
                    except Exception as e:
                        set_error(f"Mossa non valida: {e}", 2000)
                else:
                    # Logica per il Trissone (da adattare in base alle regole del gioco)
                    # Per esempio, scegli il mini board e la cella in base alla posizione del click
                    mini_size = WIDTH // 3
                    big_col = x // mini_size
                    big_row = y // mini_size
                    big_index = big_row * 3 + big_col
                    cell_x = x - big_col * mini_size
                    cell_y = y - big_row * mini_size
                    cell_col = cell_x // (mini_size // 3)
                    cell_row = cell_y // (mini_size // 3)
                    cell_index = cell_row * 3 + cell_col
                    try:
                        game.add(current_player, cell_index, big_index)
                        current_player = not current_player
                    except Exception as e:
                        set_error(f"Mossa non valida: {e}", 2000)
        
        # Chiamata unica per disegnare il tabellone e poi sovrapporre l'errore
        draw_function(screen, game)
        display_error(screen)
        pygame.display.update()
        clock.tick(30)

def main():
    global big_mode
    start_screen = True

    # Schermata iniziale con due pulsanti per scegliere la modalità
    while start_screen:
        screen.fill(WHITE)
        # Disegna il pulsante per la modalità standard
        pygame.draw.rect(screen, GRAY, button1_rect)
        text1 = font.render("Standard Mode", True, BLACK)
        screen.blit(text1, text1.get_rect(center=button1_rect.center))
        # Disegna il pulsante per la modalità big
        pygame.draw.rect(screen, GRAY, button2_rect)
        text2 = font.render("Big Mode", True, BLACK)
        screen.blit(text2, text2.get_rect(center=button2_rect.center))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if button1_rect.collidepoint(pos):
                    big_mode = False
                    start_screen = False
                elif button2_rect.collidepoint(pos):
                    big_mode = True
                    start_screen = False
        clock.tick(30)
    
    # Clear dello schermo e inizio gioco
    screen.fill(WHITE)
    pygame.display.flip()
    gameLoop(big_mode)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
