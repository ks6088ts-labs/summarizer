import os

import typer
from dotenv import load_dotenv
from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.schema import SystemMessage
from langchain.tools import tool
from langchain_community.tools.render import format_tool_to_openai_function
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_openai.chat_models import AzureChatOpenAI

app = typer.Typer()

# load environment variables
load_dotenv("./azure_chat_openai.env")

model = AzureChatOpenAI(
    api_version=os.getenv("api_version"),
    azure_endpoint=os.getenv("azure_endpoint"),
    azure_deployment=os.getenv("azure_deployment"),
    api_key=os.getenv("api_key"),
)


# Bind runtime args: https://python.langchain.com/docs/expression_language/how_to/binding
@app.command()
def primitive(query: str = "What's the weather in SF, NYC and LA?"):
    llm_with_tools = model.bind(
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "get_current_weather",
                    "description": "Get the current weather in a given location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The city and state, \
                                    e.g. San Francisco, CA",
                            },
                            "unit": {
                                "type": "string",
                                "enum": ["celsius", "fahrenheit"],
                            },
                        },
                        "required": ["location"],
                    },
                },
            }
        ],
    )

    response = llm_with_tools.invoke(input=query)
    print(f"response: {response}")


# Defining Custom Tools: https://python.langchain.com/docs/modules/agents/tools/custom_tools#tool-decorator
@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


@tool
def get_word_length(word: str) -> int:
    """Returns the length of a word."""
    return len(word)


# Tools as OpenAI Functions: https://python.langchain.com/docs/modules/agents/tools/tools_as_openai_functions
@app.command()
def tools(query: str = "５掛ける３の結果を教えてください"):
    tools = [
        multiply,
    ]
    # langchain/templates/openai-functions-agent-gmail: https://github.com/langchain-ai/langchain/blob/master/templates/openai-functions-agent-gmail/openai_functions_agent/agent.py
    functions = [format_tool_to_openai_function(t) for t in tools]
    llm_with_tools = model.bind(functions=functions)
    response = llm_with_tools.invoke(input=query)
    print(f"response: {response}")


# Custom agent: https://python.langchain.com/docs/modules/agents/how_to/custom_agent
@app.command()
def agent(query: str = "次の文章の文字数はいくつ？ 'これはテストです'"):
    tools = [
        multiply,
        get_word_length,
    ]
    llm_with_tools = model.bind(
        functions=[format_tool_to_openai_function(t) for t in tools]
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content="あなたは与えられた問題を解くアシスタントです。"),
            HumanMessagePromptTemplate.from_template("以下の質問に答えてください。\n{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_function_messages(
                x["intermediate_steps"]
            ),
        }
        | prompt
        | llm_with_tools
        | OpenAIFunctionsAgentOutputParser()
    )

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
    )
    agent_executor.invoke(
        input={"input": query},
    )


if __name__ == "__main__":
    app()
