from game_engine import GameEngine
import time
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)


def print_header(text):
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{text.center(50, '=')}{Style.RESET_ALL}\n")


def print_subheader(text):
    print(f"\n{Fore.YELLOW}{text}{Style.RESET_ALL}")


def get_input(prompt):
    return input(f"{Fore.GREEN}{prompt}{Style.RESET_ALL}")


def get_model_choice(index):
    model_lst = [
        "llama-3.1-70b-versatile",
        "llama3-70b-8192",
        "llama3-8b-8192",
        "llama-3.1-8b-instant",
        "mixtral-8x7b-32768-groq",
        "gemma-7b-it",
        "gemma2-9b-it",
        "gemini-pro",
        "gemini-1.5-pro",
        "gemini-1.5-flash",
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-4-turbo",
        "gpt-4",
        "gpt-3.5-turbo",
        "chatgpt-4o-latest",
        "claude-3-opus-20240229",
        "claude-3-sonnet-20240229",
        "claude-3-haiku-20240307",
        "mistral-large-2402",
        "mistral-large-2407",
    ]

    print_subheader(f"Choose a model for AI player {index + 1}:")
    for i, model in enumerate(model_lst):
        print(f"{Fore.CYAN}{i + 1}. {Fore.WHITE}{model}")

    print()  # Add an empty line for better readability
    while True:
        try:
            choice = get_input(
                f"Enter your choice (1-{len(model_lst)}) or type part of the model name: "
            )
            if choice.isdigit():
                choice = int(choice) - 1
                if 0 <= choice < len(model_lst):
                    return model_lst[choice]
            else:
                matches = [
                    model for model in model_lst if choice.lower() in model.lower()
                ]
                if len(matches) == 1:
                    return matches[0]
                elif len(matches) > 1:
                    print_subheader("Multiple matches found. Please be more specific:")
                    for i, match in enumerate(matches):
                        print(f"{Fore.CYAN}{i + 1}. {Fore.WHITE}{match}")
                    sub_choice = int(get_input("Enter the number of your choice: ")) - 1
                    if 0 <= sub_choice < len(matches):
                        return matches[sub_choice]
            print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")
        except ValueError:
            print(
                f"{Fore.RED}Please enter a valid number or model name.{Style.RESET_ALL}"
            )


def get_sleep_preference():
    while True:
        choice = get_input(
            "Enable sleep between rounds for API rate limiting? (y/yes or n/no): "
        ).lower()
        if choice in ["y", "yes"]:
            return True
        elif choice in ["n", "no"]:
            return False
        else:
            print(f"{Fore.RED}Invalid input. Please enter 'y' or 'n'.{Style.RESET_ALL}")


if __name__ == "__main__":
    print_header("Welcome to the Reverse Turing Test Game")

    # Choose AI models
    print_header("AI Model Selection")
    ai_models = [get_model_choice(i) for i in range(4)]

    # Get roles
    print_header("Role Assignment")
    roles = [get_input(f"Enter role for AI-{i+1}: ") for i in range(4)]
    human_role = get_input("What role would you like to take up: ")
    roles.append(human_role)

    # Get sleep preference
    print_header("Game Settings")
    enable_sleep = get_sleep_preference()

    game = GameEngine(ai_models, roles)

    round_number = 1
    while True:
        print_header(f"Round {round_number}")

        print_subheader("Loading game...")
        game.loading_game()

        print_subheader("Statements")
        game.statements()
        if enable_sleep:
            print(
                f"{Fore.YELLOW}Sleeping for 60 seconds to respect API rate limits...{Style.RESET_ALL}"
            )
            time.sleep(60)

        print_subheader("Player Selection")
        game.player_selection()
        if enable_sleep:
            print(
                f"{Fore.YELLOW}Sleeping for 60 seconds to respect API rate limits...{Style.RESET_ALL}"
            )
            time.sleep(60)

        print_subheader("Scoring")
        game.scoring()
        if enable_sleep:
            print(
                f"{Fore.YELLOW}Sleeping for 60 seconds to respect API rate limits...{Style.RESET_ALL}"
            )
            time.sleep(60)

        round_number += 1
