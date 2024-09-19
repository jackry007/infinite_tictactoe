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
BG_COLOR = (240, 240, 240)  # Soft light gray background
LINE_COLOR = (200, 200, 200)  # Soft gray for grid lines
CIRCLE_COLOR = (100, 149, 237)  # Cornflower blue for O
CROSS_COLOR = (233, 87, 63)  # Soft coral for X
HIGHLIGHT_COLOR = (255, 255, 102)  # Soft yellow for highlighting pieces
TEXT_COLOR = (50, 50, 50)  # Dark gray for text


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
starting_player = "X"  # Keep track of who starts the game (X or O)
move_phase = False
selected_piece = None
x_pieces, o_pieces = [], []  # Store positions of X and O pieces
game_over = False
game_started = False
score = {"Player 1": 0, "Player 2": 0}  # Track the score of both players

# Load the start screen image
start_screen_image = pygame.image.load("rule_page.png")


def draw_start_screen():
    screen.fill(BG_COLOR)  # Clear screen with background color (optional)
    scaled_image = pygame.transform.scale(
        start_screen_image, (SCREEN_SIZE, SCREEN_SIZE)
    )
    screen.blit(scaled_image, (0, 0))
    pygame.display.flip()


def draw_lines():
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
    pygame.draw.circle(
        screen,
        CIRCLE_COLOR,
        (x + CELL_SIZE // 2, y + CELL_SIZE // 2),
        CIRCLE_RADIUS,
        CIRCLE_WIDTH,
    )


def highlight_piece(row, col):
    pygame.draw.rect(
        screen,
        HIGHLIGHT_COLOR,
        (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE),
    )


def check_winner():
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
                    selected_piece = random.choice(x_pieces)
                    move_phase = True
            elif player == "O":
                if len(o_pieces) < 3:
                    board[row][col] = player
                    o_pieces.append((row, col))
                else:
                    selected_piece = random.choice(o_pieces)
                    move_phase = True
            if not move_phase:
                switch_player()


# Reset the game state
def reset_game():
    global board, player, move_phase, selected_piece, game_over, game_started, x_pieces, o_pieces, starting_player
    board = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    player = starting_player  # Use the starting player for the new game
    starting_player = (
        "O" if starting_player == "X" else "X"
    )  # Alternate starting player
    move_phase = False
    selected_piece = None
    game_over = False
    game_started = True  # Start the game immediately after reset
    x_pieces = []
    o_pieces = []


# Draw the end screen with improved formatting
def draw_end_screen(winner):
    screen.fill(BG_COLOR)

    # Display the game result (winner or draw)
    if winner:
        end_text = fonts["large"].render(
            f"{'Player 1' if winner == 'X' else 'Player 2'} Wins!", True, TEXT_COLOR
        )
    else:
        end_text = fonts["large"].render("It's a Draw!", True, TEXT_COLOR)

    # Get the rectangle object to center the text
    end_text_rect = end_text.get_rect(center=(SCREEN_SIZE // 2, SCREEN_SIZE // 4))
    screen.blit(end_text, end_text_rect)

    # Display the score
    score_text_1 = fonts["medium"].render(
        f"Player 1: {score['Player 1']}", True, TEXT_COLOR
    )
    score_text_2 = fonts["medium"].render(
        f"Player 2: {score['Player 2']}", True, TEXT_COLOR
    )

    # Get the rectangle objects for centering the score
    score_text_1_rect = score_text_1.get_rect(
        center=(SCREEN_SIZE // 2, SCREEN_SIZE // 2)
    )
    score_text_2_rect = score_text_2.get_rect(
        center=(SCREEN_SIZE // 2, SCREEN_SIZE // 2 + 40)
    )

    screen.blit(score_text_1, score_text_1_rect)
    screen.blit(score_text_2, score_text_2_rect)

    # Display the restart prompt
    restart_text = fonts["small"].render("Press R to Restart", True, TEXT_COLOR)
    restart_text_rect = restart_text.get_rect(
        center=(SCREEN_SIZE // 2, SCREEN_SIZE * 3 // 4)
    )
    screen.blit(restart_text, restart_text_rect)

    pygame.display.flip()


def draw_turn_indicator():
    # Show "Player 1's Turn" or "Player 2's Turn" based on who's playing
    turn_text = fonts["small"].render(
        f"{'Player 1' if player == 'X' else 'Player 2'}'s Turn", True, TEXT_COLOR
    )
    screen.blit(turn_text, (10, 10))


# Game loop
running = True
while running:
    if not game_started:
        draw_start_screen()

    if game_over:
        winner = check_winner()
        draw_end_screen(winner)

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
        draw_turn_indicator()

        if move_phase and selected_piece:
            highlight_piece(selected_piece[0], selected_piece[1])

        winner = check_winner()
        if winner or all(cell is not None for row in board for cell in row):
            game_over = True
            if winner:
                score["Player 1" if winner == "X" else "Player 2"] += 1

    pygame.display.flip()
