# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 21:10:15 2024

@author: oyeni
"""

import pygame
import sys
import random
import tkinter as tk
from tkinter import messagebox

# Initialize Pygame
pygame.init()

# Screen dimensions and colors
WIDTH, HEIGHT = 650, 750  # Increased height to give more space for the scoreboard and buttons
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LINE_COLOR = (0, 100, 200)
BUTTON_COLOR = (200, 200, 255)
HOVER_COLOR = (150, 150, 255)

# Default Colors
DEFAULT_PLAYER1_COLOR = (255, 0, 0)  # Red (Computer)
DEFAULT_PLAYER2_COLOR = (0, 255, 0)  # Green (User)

# Game board points (representing intersections where sticks can be placed)
points = {
    1: (150, 150), 2: (300, 150), 3: (450, 150),
    4: (150, 300), 5: (300, 300), 6: (450, 300),
    7: (150, 450), 8: (300, 450), 9: (450, 450)
}

# Winning combinations
winning_combinations = [
    [1, 5, 9],  # Diagonal
    [2, 5, 8],  # Vertical middle
    [3, 5, 7],  # Diagonal
    [4, 5, 6]   # Horizontal middle
]

# Movement rules (valid movement groups) based on adjacency
valid_moves = {
    1: [2, 4, 5],  # 1 can move to 2, 4, and 5
    2: [1, 3, 5],  # 2 can move to 1, 3, and 5
    3: [2, 6, 5],  # 3 can move to 2, 6, and 5
    4: [1, 5, 7],  # 4 can move to 1, 5, and 7
    5: [1, 2, 3, 4, 6, 7, 8, 9],  # 5 can move to all adjacent points
    6: [3, 5, 9],  # 6 can move to 3, 5, and 9
    7: [4, 5, 8],  # 7 can move to 4, 5, and 8
    8: [5, 7, 9],  # 8 can move to 5, 7, and 9
    9: [5, 6, 8]   # 9 can move to 5, 6, and 8
}

# Keep track of occupied points
occupied_points = {point: "" for point in points.keys()}

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tactix")

# Variables to manage dragging
dragging = False
selected_point = None
user_turn = True

# Pre-placed pieces (positions) for user (B) and computer (R)
player1_positions = [1, 2, 3]  # Computer's initial positions (Red)
player2_positions = [7, 8, 9]  # User's initial positions (Green)

# Player Colors
player1_color = DEFAULT_PLAYER1_COLOR  # Computer's color (Red by default)
player2_color = DEFAULT_PLAYER2_COLOR  # User's color (Green by default)

# Score tracking
player1_score = 0
player2_score = 0
round_count = 1  # Track number of rounds

# Draw board and grid
def draw_board():
    # Fill background
    screen.fill(WHITE)
   
    # Draw board lines
    pygame.draw.line(screen, LINE_COLOR, (150, 150), (450, 150), 3)  # Top horizontal
    pygame.draw.line(screen, LINE_COLOR, (150, 300), (450, 300), 3)  # Middle horizontal
    pygame.draw.line(screen, LINE_COLOR, (150, 450), (450, 450), 3)  # Bottom horizontal
    pygame.draw.line(screen, LINE_COLOR, (150, 150), (150, 450), 3)  # Left vertical
    pygame.draw.line(screen, LINE_COLOR, (300, 150), (300, 450), 3)  # Middle vertical
    pygame.draw.line(screen, LINE_COLOR, (450, 150), (450, 450), 3)  # Right vertical
    pygame.draw.line(screen, LINE_COLOR, (150, 150), (450, 450), 3)  # Diagonal top-left to bottom-right
    pygame.draw.line(screen, LINE_COLOR, (450, 150), (150, 450), 3)  # Diagonal top-right to bottom-left

    # Draw sticks (user: Green, computer: Red)
    for point, player in occupied_points.items():
        if player == "B":
            pygame.draw.circle(screen, player2_color, points[point], 20)
        elif player == "R":
            pygame.draw.circle(screen, player1_color, points[point], 20)

    # If dragging, draw the selected stick under the cursor
    if dragging and selected_point is not None:
        pygame.draw.circle(screen, player2_color if user_turn else player1_color, pygame.mouse.get_pos(), 20)

# Check for a winner
def check_winner(player):
    for combination in winning_combinations:
        if all(occupied_points[point] == player for point in combination):
            return True
    return False

# Display messages (e.g., "User wins!" or "Computer wins!")
def display_message(message, color, y_offset=0):
    font = pygame.font.SysFont(None, 48)
    text = font.render(message, True, color)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    screen.blit(text, text_rect)

# Reset the game after a win
def reset_game():
    global occupied_points, user_turn, round_count, player1_positions, player2_positions
    # Reset the board and positions
    occupied_points = {point: "" for point in points.keys()}
    for point in player1_positions:
        occupied_points[point] = "R"  # Computer's initial positions
    for point in player2_positions:
        occupied_points[point] = "B"  # User's initial positions
    user_turn = True  # User starts the game again

# Function to handle the quit confirmation dialog
def quit_game():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    result = messagebox.askquestion("Quit Game", "Are you sure you want to quit?", icon='warning')
    if result == 'yes':
        pygame.quit()
        sys.exit()

# Draw buttons (Restart and Quit)
def draw_buttons():
    # Define button dimensions and positions (below the board)
    button_width, button_height = 150, 50
    restart_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT - 120, button_width, button_height)
    quit_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT - 60, button_width, button_height)

    # Draw buttons
    pygame.draw.rect(screen, BUTTON_COLOR, restart_button)
    pygame.draw.rect(screen, BUTTON_COLOR, quit_button)

    # Button text
    font = pygame.font.SysFont(None, 36)
    restart_text = font.render("Reset", True, BLACK)
    quit_text = font.render("Quit", True, BLACK)

    # Button text positioning
    screen.blit(restart_text, (WIDTH // 2 - button_width // 2 + (button_width - restart_text.get_width()) // 2, HEIGHT - 120 + (button_height - restart_text.get_height()) // 2))
    screen.blit(quit_text, (WIDTH // 2 - button_width // 2 + (button_width - quit_text.get_width()) // 2, HEIGHT - 60 + (button_height - quit_text.get_height()) // 2))

    return restart_button, quit_button

# Get computer move (random valid move)
def get_computer_move():
    empty_points = [point for point, player in occupied_points.items() if player == ""]
    computer_positions = [point for point, player in occupied_points.items() if player == "R"]
    for from_point in computer_positions:
        possible_moves = valid_moves[from_point]
        for move in possible_moves:
            if move in empty_points:
                return move, from_point
    return None

# Draw the score tracker
def draw_score():
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Player 1 (Computer): {player1_score} | Player 2 (User): {player2_score} | Round: {round_count}", True, BLACK)
    screen.blit(score_text, (10, 10))

# Main game loop
def main():
    global dragging, selected_point, user_turn, player1_score, player2_score, round_count, game_over

    # Reset the game state
    reset_game()

    # Main loop variables
    running = True
    game_over = False

    while running:
        draw_board()
        draw_score()  # Display the score tracker

        # Draw buttons
        restart_button, quit_button = draw_buttons()

        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Quit button logic
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if quit_button.collidepoint(mouse_pos):  # Quit button clicked
                    quit_game()  # Show the quit confirmation dialog

            # Game logic only if it's not a game-over state
            if not game_over:
                if event.type == pygame.MOUSEBUTTONDOWN and user_turn:
                    mouse_pos = pygame.mouse.get_pos()

                    # Check if user clicked on one of their sticks
                    for point, coords in points.items():
                        if occupied_points[point] == "B" and pygame.math.Vector2(mouse_pos).distance_to(coords) < 30:
                            dragging = True
                            selected_point = point
                            break

                elif event.type == pygame.MOUSEBUTTONUP and dragging:
                    mouse_pos = pygame.mouse.get_pos()
                    dragging = False

                    # Find a valid drop point and move the stick
                    for point, coords in points.items():
                        if occupied_points[point] == "" and pygame.math.Vector2(mouse_pos).distance_to(coords) < 30:
                            if point in valid_moves[selected_point]:
                                occupied_points[point] = "B"
                                occupied_points[selected_point] = ""
                                selected_point = None
                                user_turn = False

                                # Check if user wins
                                if check_winner("B"):
                                    player2_score += 1
                                    display_message("User wins!", player2_color, 100)
                                    if player2_score == 3:
                                        display_message("User wins the game!", player2_color, 200)
                                        game_over = True
                                        pygame.display.flip()
                                        pygame.time.delay(2000)  # Delay to show the message for 2 seconds
                                        reset_game()  # Automatically reset the game after delay
                                    else:
                                        round_count += 1  # Only increment round count after a player wins
                                        reset_game()  # Automatically reset the game after a win
                                    break

                # Computer's turn if it's not the user's turn
                if not user_turn and not game_over:
                    pygame.time.delay(500)  # Brief delay for computer move
                    move = get_computer_move()

                    if move:
                        target_point, from_point = move
                        occupied_points[target_point] = "R"
                        occupied_points[from_point] = ""

                        # Check if computer wins
                        if check_winner("R"):
                            player1_score += 1
                            display_message("Computer wins!", player1_color, 100)
                            if player1_score == 3:
                                display_message("Computer wins the game!", player1_color, 200)
                                game_over = True
                                pygame.display.flip()
                                pygame.time.delay(2000)  # Delay to show the message for 2 seconds
                                reset_game()  # Automatically reset the game after delay
                            else:
                                round_count += 1  # Only increment round count after a player wins
                                reset_game()  # Automatically reset the game after a win
                            break
                    user_turn = True

            # If game over, let the user restart or quit
            if game_over:
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if restart_button.collidepoint(mouse_pos):
                            reset_game()
                            round_count = 1  # Reset round count
                            player1_score = 0  # Reset scores
                            player2_score = 0
                            game_over = False
                        elif quit_button.collidepoint(mouse_pos):
                            quit_game()

        pygame.display.flip()

if __name__ == "__main__":
    main()