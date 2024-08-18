import random

# The SlotMachine class handles all the logic related to the slot machine game.
class SlotMachine:
    def __init__(self, rows, cols, symbol_count, symbol_value):
        # Initialize the slot machine with the number of rows and columns, and the symbols used in the game.
        self.rows = rows
        self.cols = cols
        self.symbol_count = symbol_count
        self.symbol_value = symbol_value

    # This method generates a random spin for the slot machine.
    def get_slot_machine_spin(self):
        all_symbols = []
        # Create a list of symbols according to their count.
        for symbol, count in self.symbol_count.items():
            all_symbols.extend([symbol] * count)

        columns = []
        # Randomly select symbols to fill each column in the slot machine.
        for _ in range(self.cols):
            column = random.sample(all_symbols, self.rows)
            columns.append(column)

        return columns

    # This method prints the current state of the slot machine after a spin.
    def print_slot_machine(self, columns):
        for row in range(self.rows):
            print(" | ".join(column[row] for column in columns))

    # This method checks if there are any winning lines after a spin.
    def check_winnings(self, columns, lines, bet):
        winnings = 0
        winning_lines = []
        # Check each line to see if all symbols in that line are the same.
        for line in range(lines):
            symbol = columns[0][line]
            if all(column[line] == symbol for column in columns):
                winnings += self.symbol_value[symbol] * bet
                winning_lines.append(line + 1)
        return winnings, winning_lines


# The Player class manages the player's actions, like betting and managing balance.
class Player:
    def __init__(self, balance=0):
        # Initialize the player's balance.
        self.balance = balance

    # This method allows the player to deposit money into their balance.
    def deposit(self):
        while True:
            amount = input("What would you like to deposit? $")
            if amount.isdigit() and int(amount) > 0:
                self.balance += int(amount)
                break
            else:
                print("Please enter a valid number greater than 0.")

    # This method asks the player how much they want to bet on each line.
    def get_bet(self, min_bet, max_bet):
        while True:
            amount = input("What would you like to bet on each line? $")
            if amount.isdigit() and min_bet <= int(amount) <= max_bet:
                return int(amount)
            else:
                print(f"Amount must be between ${min_bet} - ${max_bet}.")

    # This method asks the player how many lines they want to bet on.
    def get_number_of_lines(self, max_lines):
        while True:
            lines = input(f"Enter the number of lines to bet on (1-{max_lines}): ")
            if lines.isdigit() and 1 <= int(lines) <= max_lines:
                return int(lines)
            else:
                print("Please enter a valid number.")

    # This method updates the player's balance after each round.
    def update_balance(self, amount):
        self.balance += amount

    # This method checks if the player has enough balance to continue playing.
    def can_play(self, min_bet):
        return self.balance >= min_bet

    # This method returns the player's current balance.
    def get_balance(self):
        return self.balance


# The Game class controls the flow of the game, connecting the player with the slot machine.
class Game:
    MAX_LINES = 3  # Maximum number of lines the player can bet on.
    MAX_BET = 100  # Maximum bet per line.
    MIN_BET = 1    # Minimum bet per line.

    def __init__(self, player, slot_machine):
        self.player = player
        self.slot_machine = slot_machine

    # This method handles a single round of spinning the slot machine.
    def spin(self):
        # Get the number of lines the player wants to bet on.
        lines = self.player.get_number_of_lines(self.MAX_LINES)
        while True:
            # Get the amount the player wants to bet per line.
            bet = self.player.get_bet(self.MIN_BET, self.MAX_BET)
            total_bet = bet * lines

            # Check if the player has enough balance to make the bet.
            if total_bet > self.player.get_balance():
                print(f"You do not have enough to bet that amount, your current balance is: ${self.player.get_balance()}")
            else:
                break

        print(f"You are betting ${bet} on {lines} lines. Total bet is equal to: ${total_bet}")

        # Spin the slot machine and display the result.
        slots = self.slot_machine.get_slot_machine_spin()
        self.slot_machine.print_slot_machine(slots)
        winnings, winning_lines = self.slot_machine.check_winnings(slots, lines, bet)

        # Update the player's balance based on the winnings.
        self.player.update_balance(winnings - total_bet)
        print(f"You won ${winnings}.")
        if winning_lines:
            print(f"You won on lines:", *winning_lines)
        else:
            print("No winning lines.")

    # This method starts the game, allowing the player to play multiple rounds.
    def play(self):
        # The player deposits money before starting.
        self.player.deposit()
        while self.player.can_play(self.MIN_BET):
            print(f"Current balance is ${self.player.get_balance()}")
            answer = input("Press enter to play (q to quit).")
            if answer.lower() == 'q':
                break
            self.spin()

        print(f"You left with ${self.player.get_balance()}")


# Main part of the program that sets up and starts the game.
if __name__ == "__main__":
    # Define the symbols used in the slot machine and their respective counts and values.
    symbol_count = {"A": 2, "B": 4, "C": 6, "D": 8}
    symbol_value = {"A": 5, "B": 4, "C": 3, "D": 2}

    # Create a SlotMachine object with 3 rows, 3 columns, and the symbol configuration.
    slot_machine = SlotMachine(3, 3, symbol_count, symbol_value)
    # Create a Player object with an initial balance of 0.
    player = Player()
    # Create a Game object that links the player and the slot machine.
    game = Game(player, slot_machine)
    # Start the game.
    game.play()
