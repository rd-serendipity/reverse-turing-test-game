from memory import Memory
from llm import LLM
from colorama import Fore, Back, Style
import random

# Last change


class GameEngine:
    def __init__(self, models_selected, roles, num_players=5):
        self.num_players = num_players
        self.round_count = 0
        self.role = [role.upper() for role in roles]
        self.ai_players_lst = [
            (self.role[idx], LLM(name, self.role[idx]))
            for idx, name in enumerate(models_selected)
        ]
        self.ai_player_dict = {name: llm for (name, llm) in self.ai_players_lst}
        self.player_to_color = dict(
            zip(self.role, [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.WHITE])
        )

        # EVERYONE HAS DIFFERENT MEMORIES DUE TO game_rule_initializaiton
        self.ai_memories = {name: Memory() for name, llm in self.ai_players_lst}

    def update_all_memory(self, update):
        for name in self.ai_memories:
            self.ai_memories[name].add_message(update)

    def loading_game(self):
        # Explaining game to llms
        for name, memory in self.ai_memories.items():
            memory.add_message(
                self.ai_player_dict[name].game_rules_initialization(self.role)
            )

    def statements(self):
        print(f"\n\n---------- Round Begins : {self.round_count+1} ------------\n\n")

        # 1 Opening Statement for each players/ they tell something about themselves their character

        # updating memory
        self.update_all_memory(
            f"\n\nOpening Statement of Round: {self.round_count+1}\n\n"
        )

        # print(self.ai_memories['ALEXDER THE GREAT'].get_history())

        # SEPERATE THE HUMAN THING
        for name, player in self.ai_players_lst:

            conver = player.statement(self.ai_memories[name].get_history())
            # Let's save intro given by every one by their name and *** model will address itself by it's name only
            conver_by_name = f"{name}: {conver}"

            # updating memory
            self.update_all_memory(conver_by_name + "\n")

            print(self.player_to_color[name] + conver_by_name, Fore.RESET, "\n")

        # Human's turn
        conver = input("Input your statement according to your role:\n")
        conver_by_name = f"{self.role[-1]}: {conver}"

        # updating memory
        self.update_all_memory(conver_by_name + "\n")
        print(self.player_to_color[self.role[-1]] + conver_by_name, Fore.RESET, "\n")

    def player_selection(self):
        print(
            f"\n\n---------- Round : {self.round_count+1}, Cross Questioning ------------\n\n"
        )
        # 2 Player selection for Counter Question
        # Based on statements what each model think is suspicious and can be human so they want to cross question them.
        # ***Feature - cross questioning should be alone or in front of everyone ?
        # For now in front of every one
        # ** still have to write for selecting player, cross_question, reply

        # updating memory
        self.update_all_memory(
            f"\n\Cross Questioning of Round: {self.round_count+1}\n\n"
        )

        # print(self.ai_memories['ALEXDER THE GREAT'].get_history())

        for name, player in self.ai_players_lst:
            # PLAYER SELECTION FOR CROSS QUESTIONING
            selected_player = player.cross_questioning_selector(
                self.ai_memories[name].get_history(), self.role
            )

            select_statement = (
                f"{name}: selected {selected_player} for cross questioning\n"
            )
            print(self.player_to_color[name] + select_statement, Fore.RESET, "\n")

            # updating memory
            self.update_all_memory(select_statement)

            # WHY SELECT THIS PLAYER
            # UPDATE
            reason_for_selection = player.cross_questioning_selection_reason(
                self.ai_memories[name].get_history(), selected_player
            )
            reason_select_statement = f"{name}: Reason for selecting {selected_player}: {reason_for_selection}\n"
            print(
                self.player_to_color[name] + reason_select_statement, Fore.RESET, "\n"
            )

            # update memory
            self.update_all_memory(reason_select_statement)

            # CROSS QUESTIONING
            cross_question = player.cross_question(
                self.ai_memories[name].get_history(), selected_player
            )
            cross_question_statement = f"{name}: cross question: {cross_question}\n"
            print(
                self.player_to_color[name]
                + f"{name}: I would like to ask question to :{selected_player}",
                Fore.RESET,
                "\n",
            )

            print(
                self.player_to_color[name] + f"{cross_question_statement}",
                Fore.RESET,
                "\n",
            )

            # updating memory
            self.update_all_memory(cross_question_statement)

            # REPLY TO CROSS QUESTION
            if selected_player == self.role[-1]:
                reply = input("Give reply to cross question:")
                print("\n")
            else:
                reply = self.ai_player_dict[selected_player].reply_cross_question(
                    self.ai_memories[name].get_history(), name
                )

            reply_statement = f"{selected_player}: {reply}"

            # updating memory
            self.update_all_memory(reply_statement)

            if selected_player != self.role[-1]:
                print(
                    self.player_to_color[selected_player] + f"{reply_statement}",
                    Fore.RESET,
                    "\n",
                )

            # ADD MORE TO CROSS QUESTION
            # for now randomly a player will take sides except the players involved
            filtered_name_lst = [
                rname
                for rname in self.role
                if rname not in (name, selected_player, self.role[-1])
            ]
            random_selection = random.choice(filtered_name_lst)

            # UPDATE
            add_more_reply = self.ai_player_dict[
                random_selection
            ].add_more_to_cross_questioning(
                self.ai_memories[random_selection].get_history(), selected_player, name
            )
            add_more_statement = f"{random_selection}: {add_more_reply}"

            print(
                self.player_to_color[random_selection] + add_more_statement,
                Fore.RESET,
                "\n",
            )

            # updating memory
            self.update_all_memory(add_more_statement)

            # always take human input
            if selected_player != self.role[-1]:
                human_addition = input(
                    "You want to add something (take side with one of the llm) [input no or ENTER if not]:"
                )
                print("\n")
                if human_addition.lower() == "no" or not human_addition:
                    pass
                else:
                    add_more_statement = f"{self.role[-1]}: {human_addition}"
                    self.update_all_memory(add_more_statement)

        # Human's turn
        # **** Here give options for selecting players
        # PLAYER SELECTION
        selected_player = input("choose someone to cross question:\n").upper()
        while selected_player not in self.role:
            print("ERROR ENTER CORRECT NAME:\t")
            selected_player = input("GIVE CORRECT NAME:\n").upper()

        select_statement = (
            f"{self.role[-1]}: selected {selected_player} for cross questioning\n"
        )

        # updating memory
        self.update_all_memory(select_statement)

        # WHY SELECT
        reason_for_selection = input(f"Why would you select {selected_player}: ")
        print("\n")
        reason_select_statement = f"{self.role[-1]}: Reason for selecting {selected_player}: {reason_for_selection}\n"

        # updating memory
        self.update_all_memory(reason_select_statement)

        # CROSS QUESTIONING
        cross_question = str(input("what question you want to ask:\n"))
        cross_question_statement = (
            f"{self.role[-1]}: cross question: {cross_question}\n"
        )

        # updating memory
        self.update_all_memory(cross_question_statement)

        # REPLY TO CROSS QUESTION
        reply = self.ai_player_dict[selected_player].reply_cross_question(
            self.ai_memories[selected_player].get_history(), self.role[-1]
        )
        reply_statement = f"{selected_player}: {reply}"

        # updating memory
        self.update_all_memory(reply_statement)

        print(
            self.player_to_color[selected_player] + f"{reply_statement}",
            Fore.RESET,
            "\n",
        )

        # ADD MORE TO CROSS QUESTION
        filtered_name_lst = [
            rname
            for rname in self.role
            if rname not in (selected_player, self.role[-1])
        ]
        random_selection = random.choice(filtered_name_lst)

        # UPDATE
        add_more_reply = self.ai_player_dict[
            random_selection
        ].add_more_to_cross_questioning(
            self.ai_memories[random_selection].get_history(),
            selected_player,
            self.role[-1],
        )
        add_more_statement = f"{random_selection}: {add_more_reply}"

        print(
            self.player_to_color[random_selection] + add_more_statement,
            Fore.RESET,
            "\n",
        )

        # updating memory
        self.update_all_memory(add_more_statement)

    def scoring(self):
        print(f"\n\n---------- Round: {self.round_count+1} Scoring ------------\n\n")
        # Each player will score other players based on their statements and cross question (list of int will be returned)
        # For now a simplistic approch just give name of most suspicious
        vote_players_dict = {name: 0 for name in self.role}
        for idx, (name, player) in enumerate(self.ai_players_lst):
            # SUS SELECTION
            suspicous_player = player.most_suspicious(
                self.ai_memories[name].get_history(), self.role
            )
            sus_statement = f"{name}: I suspect and vote out: {suspicous_player}"
            print(self.player_to_color[name] + sus_statement, Fore.RESET, "\n")
            vote_players_dict[suspicous_player] += 1

            # update memory
            self.update_all_memory(sus_statement)

            # WHY SUS
            # UPDATE
            sus_reason = player.why_most_suspicious(
                self.ai_memories[name].get_history(), suspicous_player
            )
            sus_reason_statement = (
                f"{name}: I vote {suspicous_player} because {sus_reason}"
            )
            print(self.player_to_color[name] + sus_reason_statement, Fore.RESET, "\n")

            # update memory
            self.update_all_memory(sus_reason_statement)

            # human voting turn
            if idx == len(self.ai_players_lst) - 1:
                kick_out_ai = input("Vote to kick out a player:\n").upper()
                while kick_out_ai not in self.role:
                    print("ERROR ENTER CORRECT NAME:\t")
                    kick_out_ai = input("GIVE CORRECT NAME:\n").upper()
                kick_out_ai_statement = (
                    f"{self.role[-1]}: I suspect and vote out: {kick_out_ai}"
                )

                vote_players_dict[kick_out_ai] += 1

                # update memory
                self.update_all_memory(kick_out_ai_statement)

                # reason
                reason_for_kick_out = input(
                    f"Give a reason why you kicked {kick_out_ai} out: "
                )
                print("\n")
                reason_for_kick_out_statement = f"{self.role[-1]}, I vote out {kick_out_ai} because {reason_for_kick_out} \n"

                # update memory
                self.update_all_memory(reason_for_kick_out_statement)

        player_kicked = max(vote_players_dict, key=vote_players_dict.get)
        elimination_statement = (
            f"\nELIMINATION:\n{player_kicked} has been eliminated on basis of voting\n"
        )

        # updating memory
        self.update_all_memory(elimination_statement)
        print(
            Fore.BLACK + Back.RED + Style.BRIGHT + elimination_statement,
            Style.RESET_ALL,
            "\n",
        )

        # Check status:
        self.check_ending(player_kicked)

    def check_ending(self, player_kicked):
        print(
            f"\n\n---------- Round: {self.round_count+1}, End Checking ------------\n\n"
        )
        # If player is human stop else contine
        if player_kicked == self.role[-1]:
            print(
                Fore.RED + Back.YELLOW + Style.BRIGHT + "YOU LOST THE GAME",
                Style.RESET_ALL,
                "\n",
            )
            exit()
        else:
            eli_statement = f"\n{player_kicked} WAS KICKED OUT, THEY WERE NOT HUMAN\n"
            print(
                Fore.GREEN + Back.YELLOW + Style.BRIGHT + eli_statement,
                Style.RESET_ALL,
                "\n",
            )

            # updating_memory
            self.update_all_memory(eli_statement)

            # Updating global parameters
            self.num_players -= 1
            self.role.remove(player_kicked)
            self.ai_players_lst = [
                tup for tup in self.ai_players_lst if tup[0] != player_kicked
            ]
            self.ai_player_dict.pop(player_kicked)
            self.ai_memories.pop(player_kicked)
            self.round_count += 1
