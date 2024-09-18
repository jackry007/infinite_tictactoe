import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the game window
SCREEN_SIZE = 800
GRID_SIZE = 3
CELL_SIZE = SCREEN_SIZE // GRID_SIZE
LINE_WIDTH = 5
CIRCLE_RADIUS = CELL_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = CELL_SIZE // 4

# Define colors
BG_COLOR = (0, 0, 0)  # Black
LINE_COLOR = (120, 6, 6)  # Blood Red
CIRCLE_COLOR = (4, 193, 226)  # Light Blue
CROSS_COLOR = (225, 225, 20)  # Piss Yellow
HIGHLIGHT_COLOR = (150, 150, 150)  # Highlight color for the selected piece
TEXT_COLOR = (255, 255, 255)  # White for text


# Function to dynamically adjust fonts based on screen size
def get_fonts():
    large_font_size = SCREEN_SIZE // 8
    medium_font_size = SCREEN_SIZE // 16
    small_font_size = SCREEN_SIZE // 24
    return {
        "large": pygame.font.Font(None, large_font_size),
        "medium": pygame.font.Font(None, medium_font_size),
        "small": pygame.font.Font(None, small_font_size),
    }


# Function to dynamically adjust sizes based on screen size
def get_dynamic_sizes():
    global CELL_SIZE, LINE_WIDTH, CIRCLE_WIDTH, CROSS_WIDTH, SPACE, CIRCLE_RADIUS
    CELL_SIZE = SCREEN_SIZE // GRID_SIZE
    LINE_WIDTH = SCREEN_SIZE // 120
    CIRCLE_WIDTH = SCREEN_SIZE // 40
    CROSS_WIDTH = SCREEN_SIZE // 24
    SPACE = CELL_SIZE // 4
    CIRCLE_RADIUS = CELL_SIZE // 3


# Initialize dynamic sizes and fonts
get_dynamic_sizes()
fonts = get_fonts()

# Create the screen object
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Infinite Tic-Tac-Toe")

# Set the fonts
font = pygame.font.Font(None, 60)

# Board initialization
board = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
player = "X"
move_phase = False
selected_piece = None
x_pieces, o_pieces = [], []  # Store positions of X and O pieces
game_over = False
game_started = False
score = {"X": 0, "O": 0}  # Track the score of both players


def draw_lines():
    # Draw horizontal and vertical lines
    for i in range(1, GRID_SIZE):
        pygame.draw.line(
            screen,
            LINE_COLOR,
            (0, i * CELL_SIZE),
            (SCREEN_SIZE, i * CELL_SIZE),
            LINE_WIDTH,
        )
        pygame.draw.line(
            screen,
            LINE_COLOR,
            (i * CELL_SIZE, 0),
            (i * CELL_SIZE, SCREEN_SIZE),
            LINE_WIDTH,
        )


def draw_pieces():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            piece = board[row][col]
            if piece == "X":
                draw_x(col * CELL_SIZE, row * CELL_SIZE)
            elif piece == "O":
                draw_o(col * CELL_SIZE, row * CELL_SIZE)


def draw_x(x, y):
    # Draw X
    pygame.draw.line(
        screen,
        CROSS_COLOR,
        (x + SPACE, y + SPACE),
        (x + CELL_SIZE - SPACE, y + CELL_SIZE - SPACE),
        CROSS_WIDTH,
    )
    pygame.draw.line(
        screen,
        CROSS_COLOR,
        (x + SPACE, y + CELL_SIZE - SPACE),
        (x + CELL_SIZE - SPACE, y + SPACE),
        CROSS_WIDTH,
    )


def draw_o(x, y):
    # Draw O
    pygame.draw.circle(
        screen,
        CIRCLE_COLOR,
        (x + CELL_SIZE // 2, y + CELL_SIZE // 2),
        CIRCLE_RADIUS,
        CIRCLE_WIDTH,
    )


def highlight_piece(row, col):
    """Darken the background of the selected piece to indicate it's the one to be moved."""
    pygame.draw.rect(
        screen,
        HIGHLIGHT_COLOR,
        (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE),
    )


def check_winner():
    # Check rows, columns and diagonals for a win
    for row in range(GRID_SIZE):
        if (
            board[row][0] == board[row][1] == board[row][2]
            and board[row][0] is not None
        ):
            return board[row][0]
    for col in range(GRID_SIZE):
        if (
            board[0][col] == board[1][col] == board[2][col]
            and board[0][col] is not None
        ):
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]
    return None


def switch_player():
    global player
    player = "O" if player == "X" else "X"


def move_piece(old_row, old_col, new_row, new_col):
    global move_phase, selected_piece, x_pieces, o_pieces
    if board[new_row][new_col] is None:
        board[new_row][new_col] = board[old_row][old_col]
        board[old_row][old_col] = None

        # Update the list of pieces
        if board[new_row][new_col] == "X":
            x_pieces.remove((old_row, old_col))  # Remove the old position
            x_pieces.append((new_row, new_col))  # Add the new position
        elif board[new_row][new_col] == "O":
            o_pieces.remove((old_row, old_col))  # Remove the old position
            o_pieces.append((new_row, new_col))  # Add the new position

        move_phase = False
        selected_piece = None
        switch_player()


def handle_click(x, y):
    global move_phase, selected_piece, x_pieces, o_pieces
    row = y // CELL_SIZE
    col = x // CELL_SIZE

    if move_phase:
        old_row, old_col = selected_piece
        move_piece(old_row, old_col, row, col)
    else:
        if board[row][col] is None:
            if player == "X":
                if len(x_pieces) < 3:
                    board[row][col] = player
                    x_pieces.append((row, col))
                else:
                    # Randomly select one of X's pieces to move
                    selected_piece = random.choice(x_pieces)
                    move_phase = True
            elif player == "O":
                if len(o_pieces) < 3:
                    board[row][col] = player
                    o_pieces.append((row, col))
                else:
                    # Randomly select one of O's pieces to move
                    selected_piece = random.choice(o_pieces)
                    move_phase = True
            if not move_phase:
                switch_player()


# Reset the game state
def reset_game():
    global board, player, move_phase, selected_piece, game_over, game_started
    board = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    player = "X"
    move_phase = False
    selected_piece = None
    game_over = False
    game_started = False


# Draw the starting screen
def draw_start_screen():
    screen.fill(BG_COLOR)
    title_text = fonts["large"].render("INFINITE ", True, TEXT_COLOR)
    title_text_2 = fonts["large"].render("TIC-TAC-TOE ", True, TEXT_COLOR)
    screen.blit(title_text, (SCREEN_SIZE // 4, SCREEN_SIZE // 4))
    screen.blit(title_text_2, (SCREEN_SIZE // 4, SCREEN_SIZE // 3))

    start_text = fonts["medium"].render("Press SPACE to Start", True, TEXT_COLOR)
    screen.blit(start_text, (SCREEN_SIZE // 4, SCREEN_SIZE // 2))
    
    
    pygame.display.flip()


# Draw the end screen
def draw_end_screen(winner):
    screen.fill(BG_COLOR)
    if winner:
        end_text = fonts["large"].render(f"{winner} Wins!", True, TEXT_COLOR)
    else:
        end_text = fonts["large"].render("It's a Draw!", True, TEXT_COLOR)

    screen.blit(end_text, (SCREEN_SIZE // 4, SCREEN_SIZE // 4))

    score_text = fonts["medium"].render(
        f"Score: X {score['X']} - O {score['O']}", True, TEXT_COLOR
    )
    screen.blit(score_text, (SCREEN_SIZE // 4, SCREEN_SIZE // 2))

    restart_text = fonts["small"].render("Press R to Restart", True, TEXT_COLOR)
    screen.blit(restart_text, (SCREEN_SIZE // 4, SCREEN_SIZE * 3 // 4))
    pygame.display.flip()


# Game loop
running = True
while running:
    if not game_started:
        draw_start_screen()

    if game_over:
        draw_end_screen(check_winner())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if not game_started and event.key == pygame.K_SPACE:
                game_started = True
            if game_over and event.key == pygame.K_r:
                reset_game()

        if game_started and not game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                handle_click(x, y)

    if game_started and not game_over:
        screen.fill(BG_COLOR)
        draw_lines()
        draw_pieces()
        if move_phase and selected_piece:
            highlight_piece(selected_piece[0], selected_piece[1])

        winner = check_winner()
        if winner or all(cell is not None for row in board for cell in row):
            game_over = True
            if winner:
                score[winner] += 1

    pygame.display.flip()
