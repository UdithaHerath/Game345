import sys


def get_valid_input():
    """Get a valid starting number between 20 and 30 from the user."""
    while True:
        try:
            num = int(input("Enter a starting number (20-30): "))
            if 20 <= num <= 30:
                return num
            else:
                print("Invalid input. Choose a number between 20 and 30.")
        except ValueError:
            print("Please enter a valid integer.")


def get_human_choice():
    """Get a valid multiplier choice (3, 4, or 5) from the player."""
    while True:
        try:
            choice = int(input("Choose a multiplier (3, 4, or 5): "))
            if choice in [3, 4, 5]:
                return choice
            else:
                print("Invalid choice. Choose 3, 4, or 5.")
        except ValueError:
            print("Please enter a valid integer.")


def apply_rules(num, total_points, game_bank):
    """Apply the game rules for points and the bank based on the new number."""
    if num % 2 == 0:
        total_points += 1  # Even number: +1 point
    else:
        total_points -= 1  # Odd number: -1 point

    if num % 10 == 0 or num % 10 == 5:
        game_bank += 1  # Ends in 0 or 5: +1 bank point

    return total_points, game_bank


def evaluate_game(total_points, game_bank):
    """
    Evaluate the final game score to determine the winner.
    If total points are even, subtract the game bank; if odd, add it.
    """
    if total_points % 2 == 0:
        total_points -= game_bank
    else:
        total_points += game_bank

    return total_points


def minimax(num, total_points, game_bank, is_computer_turn, alpha, beta, depth=0):
    """
    Minimax algorithm with Alpha-Beta pruning.
    - `num`: current number
    - `total_points`: current points
    - `game_bank`: bank points
    - `is_computer_turn`: True if it's the computer's turn
    - `alpha`: best guaranteed score for the maximizing player
    - `beta`: best guaranteed score for the minimizing player
    - `depth`: current depth in the recursion (used for limiting search depth)
    """

    # Base case: If number reaches 3000 or more, evaluate the game outcome
    if num >= 3000:
        final_score = evaluate_game(total_points, game_bank)
        return final_score if final_score % 2 == 1 else -final_score  # Higher is better for the computer

    if is_computer_turn:
        best_score = -sys.maxsize  # Computer wants to maximize score
        best_move = None
        for multiplier in [3, 4, 5]:
            new_num = num * multiplier
            new_total_points, new_game_bank = apply_rules(new_num, total_points, game_bank)
            score = minimax(new_num, new_total_points, new_game_bank, False, alpha, beta, depth + 1)

            if score > best_score:
                best_score = score
                best_move = multiplier

            alpha = max(alpha, best_score)  # Update alpha
            if beta <= alpha:
                break  # Alpha-beta pruning

        if depth == 0:  # If at the root, return the best move
            return best_move
        return best_score

    else:
        best_score = sys.maxsize  # Human wants to minimize score
        for multiplier in [3, 4, 5]:
            new_num = num * multiplier
            new_total_points, new_game_bank = apply_rules(new_num, total_points, game_bank)
            score = minimax(new_num, new_total_points, new_game_bank, True, alpha, beta, depth + 1)

            best_score = min(best_score, score)
            beta = min(beta, best_score)  # Update beta
            if beta <= alpha:
                break  # Alpha-beta pruning

        return best_score


def main():
    print("Welcome to the Multiplication Game!")

    # Step 1: Get the starting number
    num = get_valid_input()

    total_points = 0
    game_bank = 0
    turn = 0  # 0 = human, 1 = computer

    while num < 3000:
        print(f"\nCurrent number: {num}")
        print(f"Total Points: {total_points}, Game Bank: {game_bank}")

        if turn == 0:
            multiplier = get_human_choice()
        else:
            multiplier = minimax(num, total_points, game_bank, True, -sys.maxsize, sys.maxsize)
            print(f"Computer chose: {multiplier}")

        # Multiply the number
        num *= multiplier

        # Apply rules
        total_points, game_bank = apply_rules(num, total_points, game_bank)

        # Switch turn
        turn = 1 - turn

    print(f"\nGame Over! Final Number: {num}")
    print(f"Total Points before bank adjustment: {total_points}")
    print(f"Game Bank: {game_bank}")

    # Step 4: Final points adjustment
    total_points = evaluate_game(total_points, game_bank)
    print(f"Final Total Points: {total_points}")

    # Step 5: Determine the winner
    if total_points % 2 == 0:
        print("The human player wins!")
    else:
        print("The computer wins!")


if __name__ == "__main__":
    main()
