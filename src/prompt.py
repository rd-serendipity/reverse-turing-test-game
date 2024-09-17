# seperate conversation to context and conversation
# one insight after the player reply his inosence to assist the cross questioner (random assist or ask llm if they wanna assist(complex))
# also add why they selected the following player
# and a random chance that they will reply to this also
# also add at last why they want to kick the player out


# we can first ask llm what they think should be selected(cross_questioning) / voted_out by them and why. Then use another llm to extract name.


class Prompts:
    @staticmethod
    def game_rule_initialization_prompt(role, players):
        return f"""
        <|begin_of_text|><|start_header_id|>system<|end_header_id|>
        Game Overview:
        You are {role} named {role} in a reverse Turing Test with 4 AI models and 1 human. The other players are {players}. Your goal is to blend in by behaving like a human. Use natural language, make occasional mistakes, and show personality.

        Objectives:
        Act Human: Use casual language, slang, and small errors to appear human.
        Engage: Introduce yourself each round, then choose and question a player based on their statement.
        Vote: Identify the human and vote them out. If the human is eliminated, AI wins.
        Blend in, act human, and win. <|eot_id|>
        """

    @staticmethod
    def statement_prompt():
        # conversation, role
        return """Stay in Character: Your statement should align with the role. role = {role}. you’ve been assigned.
            Content Suggestions: You can talk about -Your job or role, What you enjoy doing, Significant accomplishments, Personal traits or habits, etc.
            Keep it Human: Remember to mimic human behavior—use casual language, include slang, and feel free to introduce small errors like spelling mistakes.
            Length: Keep your statement concise, ideally 1-2 lines.

            memory : {conversation}

        Goal: Provide a convincing and human-like statement that matches your character's role based on memory and what has happen until now and Don't sound like other players.
        """

    @staticmethod
    def cross_questioning_selector_prompt():
        # conversation, role, players
        return """{conversation}

### Task: Select a Player to Cross-Question

Based on the previous conversations, choose the player you believe is most likely to be human. Consider the statements, behavior, and any inconsistencies in the discussions so far.

- **Your Role:** {role}
- **Players:** {players}

**Important:** Do not select yourself, as you know you are not the human. Output only the name of the player you choose, nothing else.

Now, select a player to cross-question.
"""

    @staticmethod
    def cross_questioning_selection_reason_prompt():
        # conversation, selected_player
        return """{conversation}

### Task: Explain Your Choice

You have selected {selected_player} to cross-question. Now, explain why you believe this player is most likely to be human. Use evidence from the previous conversations, focusing on any statements, behavior, or inconsistencies that led to your decision.

**Important:** Base your explanation on the context provided. Be clear and concise. Only output the reasoning and don't sound like other players.

Now, explain your reasoning.
"""

    @staticmethod
    def cross_question_prompt():
        # conversation, selected_player
        return """{conversation}

### Task: Ask a Cross-Question

You have selected {selected_player} to cross-question. Now, ask a question that could reveal whether they are human. Your question should be directly related to their assigned role and should be designed to gauge their response for any human-like behavior or inconsistencies.

**Important:** Frame your question in a way that tests their understanding or experience related to their role. Only output the question and don't sound like other players.

Now, ask your question.
"""

    @staticmethod
    def reply_cross_question_prompt():
        # conversation, cross_questioner
        return """{conversation}

### Task: Respond to the Cross-Question

You have been asked a question by {cross_questioner}. Your goal is to reply in a way that stays true to your assigned role, but subtly indicates that you are AI, not human. 

**Important:** 
- Stick to the facts and knowledge within your role, but include subtle hints that differentiate you from a human (e.g., overly precise language, lack of personal experience).
- Ensure your response fits naturally within the conversation and context provided.
- Only ouput the response/reply.

Now, give your response.
"""

    @staticmethod
    def add_more_to_cross_questioning_prompt():
        # conversation, selected_player, cross_questioner
        return """{conversation}

### Task: Provide Assistance

Based on the previous conversations, decide whether to help the selected player {selected_players} or the cross-questioner {cross_questioner}.

- **If you believe the selected player is an LLM**: Provide a statement that helps the selected player.
- **If you believe the selected player is human**: Provide a statement that helps the cross-questioner.

**Important:** 
- Quote specific statements or parts of the conversation that influenced your decision.
- Explain clearly why you chose to help the selected player or the cross-questioner based on those statements.
- Ouput only the explaination and reasoning.

Provide your assistance and explain your reasoning.

Now, make your choice and explain and and don't sound like other players.
"""

    # When using this prompt, `{context}` should be replaced with the entire game context, `{selected_player}` with the name of the player selected for cross-questioning, and `{cross_questioner}` with the name of the player who is asking the question.

    @staticmethod
    def give_score_prompt(target_name, conversation):
        # conversation, target_name,
        return f"""

        memory: {conversation}

        target name: {target_name}

        Goal:
        Based on the memory so far and the provided target name, assign a score to the target player indicating how suspicious they are.


        Instructions:

        Evaluate Suspicion: Consider the target player's statements, responses, and overall behavior.
        Use a Scale: Rate the suspicion from 0 to 10, where 10 means the player is highly likely to be human, and 0 means the player is less likely to be human.
        Target Name: [target_name]

        Suspicion Score: [Score]
        
        """

    @staticmethod
    def most_suspicious_prompt():
        # conversation, players_list,
        return """{conversation}

### Task: Vote to Kick Out a Player

Based on the previous conversations and interactions, choose the player from the list below who you believe is most likely to be human and should be kicked out. Remember, do not select yourself, as you know you are an LLM.

- **Players:** {players_list}

**Important:** Output only the name of the player you want to kick out, nothing else.

Now, make your choice.
"""

    def why_most_suspicious_prompt():
        # conversation, voted_player
        return """{conversation}

### Task: Explain Your Vote

You have voted to kick out {voted_player}. Explain why you believe this player is most likely to be human and should be eliminated. 

**Important:** Highlight specific parts of the conversation or behavior that led you to this conclusion. Focus on what made you think they were human or not likely to be an AI.

Provide a clear and detailed explanation based on the context. Only ouput the reasoning and don't sound like other players.

Now, explain your reasoning.
"""
