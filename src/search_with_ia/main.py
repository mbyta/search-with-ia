from dotenv import load_dotenv
import os
import autogen
from datetime import datetime
from newsapi_client import NewsApiClient
from typing_extensions import Annotated

load_dotenv()

llm_config = {
    "timeout": 600,
    "cache_seed": 42,
    "config_list": [{"model": "gpt-4o-mini", "api_key": os.getenv("API_KEY_LLM")},],
    "temperature": 0.9,
}

query_generator_agent = autogen.ConversableAgent(
    name="query_generator_agent",
    llm_config=llm_config,
    human_input_mode="NEVER",
    system_message=
    f"""
    You are an assistant that, given a question or any other types of messages, transform it to the best web search query possible.
    As an additional context, note that today's date is {datetime.now().strftime("%Y-%m-%d")}
    """
)

tool_caller_agent = autogen.ConversableAgent(
    name="tool_caller_agent",
    llm_config=llm_config,
    system_message=
    f"""
    You solve tasks using your tools. Reply with 'TERMINATE' when the task has been completed.
    """
)

# create a UserProxyAgent instance named "user_proxy"
user_proxy_agent = autogen.ConversableAgent(
    name="user_proxy",
    llm_config=False,
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    code_execution_config=False,
    is_termination_msg=lambda x: x.get("content", "") is not None and "terminate" in x["content"].lower(),
    default_auto_reply="Continue if you have not finished your task, otherwise reply 'TERMINATE'."
)

def get_search_result(query: Annotated[str, "The search term"]) -> Annotated[str, "The result of the search"]:
    tool = NewsApiClient()
    return tool.get_search_result(query)

autogen.register_function(
    get_search_result,
    caller=tool_caller_agent,
    executor=user_proxy_agent,
    description="Searches on the web and returns the result"
)

if __name__ == "__main__":
    reply = user_proxy_agent.initiate_chat(
        tool_caller_agent,
        message="france current prime minister 2024",
        summary_method="reflection_with_llm",
        summary_args={"summary_prompt": "Summarize the content"})
    print("=== ANSWER ===", reply)