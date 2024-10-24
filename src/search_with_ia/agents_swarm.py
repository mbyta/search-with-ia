from dotenv import load_dotenv
import os
from datetime import datetime
from autogen import register_function, ConversableAgent
from typing_extensions import Annotated
from newsapi_client import NewsApiClient

load_dotenv()

class AgentsSwarm():
    def __init__(self):
        self.api_key = os.getenv("API_KEY_LLM")
        self.__init_query_generator_agent()
        self.__init_user_proxy_agent()
        self.__init_tool_caller_agent()

        register_function(
            AgentsSwarm.get_search_result,
            caller=self.tool_caller_agent,
            executor=self.user_proxy_agent,
            description="This function searches on the web and returns a result"
        )

    def execute(self, user_query: str) -> str:
        search_query = self.query_generator_agent.generate_reply(messages=[{"content": user_query, "role": "user"}])

        response = self.user_proxy_agent.initiate_chat(
            self.tool_caller_agent,
            message=search_query,
            summary_method="reflection_with_llm",
            summary_args={"summary_prompt": f"Answering the following question: `{user_query}` by summarizing the content"})

        return response.summary

    @staticmethod
    def get_search_result(query: Annotated[str, "The search term"]) -> Annotated[str, "The result from the search"]:
        tool = NewsApiClient()
        return tool.get_search_result(query)

    def __init_query_generator_agent(self):
        llm_config = {
            "timeout": 60,
            "cache_seed": 42,
            "config_list": [{"model": "gpt-4o-mini", "api_key": self.api_key}],
            "temperature": 0.9
        }

        self.query_generator_agent = ConversableAgent(
            name="query_generator_agent",
            llm_config=llm_config,
            human_input_mode="NEVER",
            system_message=
            f"""
            You are an assistant that, given a question or any other types of messages, transform it to the best web search query possible.
            Always add the current date in query, that is the day of the month, the month and the year. (Note that today's date is {datetime.now().strftime("%Y-%m-%d")})
            """
        )

    def __init_user_proxy_agent(self):
        self.user_proxy_agent = ConversableAgent(
            name="user_proxy_agent",
            llm_config=False,
            human_input_mode="NEVER",
            max_consecutive_auto_reply=5,
            code_execution_config=False,
            is_termination_msg=lambda x: x.get("content", "") is not None and "terminate" in x["content"].lower(),
            default_auto_reply="Continue if you have not finished your task, otherwise reply 'TERMINATE'."
        )

    def __init_tool_caller_agent(self):
        llm_config = {
            "timeout": 60,
            "cache_seed": 42,
            "config_list": [{"model": "gpt-4o-mini", "api_key": self.api_key}],
            "temperature": 0.9
        }

        self.tool_caller_agent = ConversableAgent(
            name="tool_caller_agent",
            llm_config=llm_config,
            system_message="You answer questions using your tools. Reply with 'TERMINATE' when the task has been completed."
        )