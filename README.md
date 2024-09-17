# 🤖 Reverse Turing Test Game 🧠

<p align="center">
  <img src="docs/assets/game_logo.png" alt="Reverse Turing Test Game Logo" width="200"/>
</p>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

Can you outsmart AI in a battle of wits? Welcome to the Reverse Turing Test Game! 🎭

## 🌟 Overview

In this thrilling game, you'll join a group of AI players, each with a unique role. Your mission? Blend in and convince the AIs that you're one of them while trying to unmask the other players. It's a high-stakes game of deception and detection!

### 🎯 Objectives

- **For the Human**: Survive rounds of questioning and voting without being discovered
- **For the AI**: Identify and eliminate the human player while mimicking human-like behavior

## 🚀 Features

- 🤖 Dynamic AI player interactions using cutting-edge language models
- 🎭 Role-based gameplay encouraging creative improvisation
- 🔍 Multiple rounds of cunning questions and deduction
- 🗣️ AI players strive to mimic human-like communication
- 🤝 Players can support or challenge others during cross-questioning
- 🗳️ Strategic voting with explanations for eliminations
- 🌈 Color-coded terminal output for an immersive experience
- 🔌 Compatible with Groq, OpenAI, Mistral, and Anthropic APIs

## 🎮 Gameplay

### Setup
Choose your role and select AI models for other players:

<p align="center">
  <img src="docs/assets/starting_game_llm_choice.png" alt="LLM Choice Screenshot" width="600"/>
</p>

<p align="center">
  <img src="docs/assets/starting_game_role_choice.png" alt="Role Selection Screenshot" width="600"/>
</p>

### Round 1: Opening Statements
Each player makes a statement about their role:

<p align="center">
  <img src="docs/assets/round_1_opening_statements.png" alt="Round 1 Opening Statements Screenshot" width="600"/>
</p>

### Cross-Questioning
Players select and interrogate each other:

<p align="center">
  <img src="docs/assets/round_1_cross_questioning.png" alt="Round 1 Cross-Questioning Screenshot" width="600"/>
</p>

AI players ask questions to the human player:

<p align="center">
  <img src="docs/assets/round_1_cross_question_ai_to_human.png" alt="AI to Human Cross-Questioning Screenshot" width="600"/>
</p>

The human player can also ask questions to AI players:

<p align="center">
  <img src="docs/assets/round_1_cross_question_human_to_ai.png" alt="Human to AI Cross-Questioning Screenshot" width="600"/>
</p>

During cross-questioning, other players can choose to support or challenge either the questioner or the responder, adding depth to the interaction.

### Voting
All players vote on who they think is the human and provide reasoning for their choice:

<p align="center">
  <img src="docs/assets/voting_round.png" alt="Voting Round Screenshot" width="600"/>
</p>

### Elimination
The player with the most votes is eliminated:

<p align="center">
  <img src="docs/assets/elimination.png" alt="Elimination Screenshot" width="600"/>
</p>

### Next Round
The game continues with the next round of statements:

<p align="center">
  <img src="docs/assets/round_2_statements.png" alt="Round 2 Statements Screenshot" width="600"/>
</p>

## 🛠 Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/rd-serendipity/reverse-turing-test-game.git
   ```
2. Navigate to the project directory:
   ```bash
   cd reverse-turing-test-game
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up your environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys for Groq, OpenAI, Mistral, and Anthropic
   ```

## 🎮 How to Play

1. Start the game:
   ```bash
   python src/main.py
   ```
2. Follow the on-screen prompts to:
   - Choose AI models for other players
   - Select roles for all players
   - Make statements about your role
   - Select players to cross-question and explain your choice
   - Support or challenge other players during questioning
   - Vote on who you think is the human and explain your reasoning

### Game Flow

```mermaid
graph TD
    A[Start Game] --> B[Choose AI Models for Players]
    B --> C[Assign Roles]
    C --> D[Initialize Game]
    D --> E[Start Round]
    E --> F[Players Make Statements]
    F --> G[Cross-Questioning]
    G --> H[Players Vote]
    H --> I{Is Human Eliminated?}
    I -->|Yes| J[AI Wins]
    I -->|No| K{Only 2 Players Left?}
    K -->|Yes| L[Human Wins]
    K -->|No| M[Eliminate Player with Most Votes]
    M --> E
    J --> N[End Game]
    L --> N
```



1. **Setup**: Choose AI models and assign roles
2. **Rounds**:
   - All players make statements
   - Players select and cross-question each other, explaining their choices
   - Other players can support or challenge during questioning
   - Everyone votes on the most suspicious player and explains their vote
3. **Elimination**: Player with most votes is out
4. **Winning Conditions**:
   - Human wins if they are the last player remaining with one AI
   - AIs win if they successfully eliminate the human

Remember, as the human player, your goal is to vote strategically to ensure your survival while convincing the AI players that you're one of them!


## 🔌 API Compatibility

This game is compatible with multiple AI APIs, including:
- Groq
- OpenAI
- Mistral
- Anthropic

Make sure to set up your API keys in the `.env` file for the services you plan to use.

## 🤝 Contributing

We love contributions! Check out our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to:

- 🐛 Report bugs
- 💡 Suggest enhancements
- 📝 Improve documentation
- 🖥 Create a user interface

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Thanks to all the AI models and APIs that make this game possible
- Inspired by the classic Turing test and the fascinating world of AI

---

<p align="center">
  <strong>Outsmart AI, or Become One! 🏆</strong>
</p>

<p align="center">
  <a href="https://github.com/rd-serendipity/reverse-turing-test-game/issues">Report Bug</a> ·
  <a href="https://github.com/rd-serendipity/reverse-turing-test-game/issues">Request Feature</a>
</p>
