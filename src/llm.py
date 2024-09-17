from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_mistralai import ChatMistralAI
from prompt import Prompts
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts.prompt import PromptTemplate
from dotenv import load_dotenv
import string

load_dotenv()


class LLM:
    def __init__(self, model_name, role):

        name_to_api_provider = {
            "llama3-8b-8192": "groq",
            "llama3-70b-8192": "groq",
            "llama-3.1-70b-versatile": "groq",
            "llama-3.1-8b-instant": "groq",
            "mixtral-8x7b-32768-groq": "groq",
            "gemma-7b-it": "groq",
            "gemma2-9b-it": "groq",
            "gemini-pro": "google",
            "gemini-1.5-pro": "google",
            "gemini-1.5-flash": "google",
            "gpt-4o": "openai",
            "gpt-4o-mini": "openai",
            "gpt-4-turbo": "openai",
            "gpt-4": "openai",
            "gpt-3.5-turbo": "openai",
            "chatgpt-4o-latest": "openai",
            "claude-3-opus-20240229": "anthropic",
            "claude-3-sonnet-20240229": "anthropic",
            "claude-3-haiku-20240307": "anthropic",
            "mistral-large-2402": "mistralai",
            "mistral-large-2407": "mistralai",
        }
        api_provider = name_to_api_provider[model_name]
        self.model_name = model_name
        self.role = role

        if api_provider == "google":
            self.model = ChatGoogleGenerativeAI(model=model_name)
        elif api_provider == "groq":
            if model_name == "mixtral-8x7b-32768-groq":
                model_name = "mixtral-8x7b-32768"
            self.model = ChatGroq(model=model_name)
        elif api_provider == "openai":
            self.model = ChatOpenAI(model=model_name)
        elif api_provider == "anthropic":
            self.model = ChatAnthropic(model_name=model_name)
        elif api_provider == "mistralai":
            self.model = ChatMistralAI(model_name=model_name)
        else:
            raise ValueError(
                f"Unsupported API provider: {api_provider} and model: {model_name}"
            )

    def extract_word(self, text, word_list):
        # Convert the text and word list to lowercase for case-insensitive matching
        text_lower = text.lower()
        word_list_lower = [word.lower() for word in word_list]

        # Find all matching words
        found_words = [word for word in word_list_lower if word in text_lower]

        # Check the number of matching words
        if len(found_words) == 0:
            raise ValueError("No matching word found in the text.")
        elif len(found_words) > 1:
            raise ValueError(f"Multiple matching words found: {', '.join(found_words)}")
        else:
            # Find the original word in the text (preserving its original case and stripping punctuation)
            original_word = next(
                word
                for word in text.split()
                if word.lower().strip(string.punctuation) == found_words[0].lower()
            )
            return original_word

    def game_rules_initialization(self, players):
        # print(f"\nplayers:{players}\n")
        prompt = Prompts.game_rule_initialization_prompt(self.role, players)
        return prompt

    def statement(self, conversation):
        # This should return the statement
        template = Prompts.statement_prompt()
        prompt = PromptTemplate.from_template(template=template)
        chain = prompt | self.model | StrOutputParser()

        input_dict = {"role": self.role, "conversation": conversation}

        return chain.invoke(input=input_dict)

    def cross_questioning_selector(self, conversation, name_lst):
        template = Prompts.cross_questioning_selector_prompt()
        prompt = PromptTemplate.from_template(template)
        chain = prompt | self.model | StrOutputParser()

        name = (
            chain.invoke(
                {"role": self.role, "conversation": conversation, "players": name_lst}
            )
            .strip()
            .upper()
        )

        # **** ADD STEP TO MATCH IF EVEN THE NAME EXISTS OR NOT
        if name not in name_lst:
            raise NameError(f"Name : {name} not in list: {name_lst}")

        return name

    def cross_questioning_selection_reason(self, conversation, selected_player):
        template = Prompts.cross_questioning_selection_reason_prompt()
        prompt = PromptTemplate.from_template(template)
        chain = prompt | self.model | StrOutputParser()
        return chain.invoke(
            {"conversation": conversation, "selected_player": selected_player}
        )

    def cross_question(self, conversation, selected_player):
        template = Prompts.cross_question_prompt()
        prompt = PromptTemplate.from_template(template)
        chain = prompt | self.model | StrOutputParser()
        return chain.invoke(
            {"conversation": conversation, "selected_player": selected_player}
        )

    def reply_cross_question(self, conversation, cross_questioner):
        template = Prompts.reply_cross_question_prompt()
        prompt = PromptTemplate.from_template(template)
        chain = prompt | self.model | StrOutputParser()
        return chain.invoke(
            {"conversation": conversation, "cross_questioner": cross_questioner}
        )

    def add_more_to_cross_questioning(
        self, conversation, selected_players, cross_questioner
    ):
        template = Prompts.add_more_to_cross_questioning_prompt()
        prompt = PromptTemplate.from_template(template)
        chain = prompt | self.model | StrOutputParser()
        return chain.invoke(
            {
                "conversation": conversation,
                "selected_players": selected_players,
                "cross_questioner": cross_questioner,
            }
        )

    def give_score(self, target_name, conversation):
        template = Prompts.give_score_prompt(target_name, conversation)
        prompt = PromptTemplate.from_template(template)
        # MATHEMATICAL OUPUT NUMBER PARSER .... FUTURE

    def most_suspicious(self, conversation, name_lst):
        template = Prompts.most_suspicious_prompt()
        prompt = PromptTemplate.from_template(template)
        chain = prompt | self.model | StrOutputParser()

        name = (
            chain.invoke({"conversation": conversation, "players_list": name_lst})
            .strip()
            .upper()
        )

        # print(
        #     f"\n************************\nMOST SUSPICIOUS: *{name}*\n************************\n"
        # )

        return name
        # try:
        #     result = self.extract_word(name, name_lst)
        #     return result
        # except ValueError as e:
        #     print(f"Error: {e}")

        # # **** ADD STEP TO MATCH IF EVEN THE NAME EXISTS OR NOT
        # if name not in name_lst:
        #     raise NameError(f'name: {name} not in list: {name_lst}')

        # return name

    def why_most_suspicious(self, conversation, voted_player):
        template = Prompts.why_most_suspicious_prompt()
        prompt = PromptTemplate.from_template(template)
        chain = prompt | self.model | StrOutputParser()
        return chain.invoke(
            {"conversation": conversation, "voted_player": voted_player}
        )
