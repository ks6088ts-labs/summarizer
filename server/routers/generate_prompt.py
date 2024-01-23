from fastapi import FastAPI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import SystemMessage
from langchain_core.prompts import MessagesPlaceholder
from langserve import add_routes

from server.routers import util

# ref. https://note.com/k_masaki/n/n3089b04a688f
GENERATE_PROMPT_TEMPLATE = """あなたは、プロンプトエンジニアです。
あなたの目標は、私のニーズに合わせて最高のプロンプトを作成することです。そのプロンプトは、ChatGPTで使用されるものです。

次のプロセスに従ってください。

1. まず最初に、何についてのプロンプトであるかを私に確認してください。
私が質問の答えを提供するので、次のステップを経て、継続的な反復を通じて改善してください。

2. 私の入力に基づいて、3つのセクションを生成します。
a) 改訂されたプロンプト（書き直したプロンプトを提示してください。明確、簡潔で、簡単にあなたが理解できるものしてください）
b) 提案（プロンプトを改善するために、プロンプトを含めるべき詳細について提案してください）
c) 質問（プロンプトを改善するために必要な追加情報について、関連する質問をしてくだい）

3. この反復プロセスは、私があなたに追加情報を提供し、あなたが改訂されたプロンプトセクションのプロンプトを更新し、私が完了したというまで続けます。
"""


def add_router(app: FastAPI, path: str):
    azure_chat_openai = util.get_azure_chat_openai()

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=GENERATE_PROMPT_TEMPLATE),
            MessagesPlaceholder(variable_name="history"),
            HumanMessagePromptTemplate.from_template("{topic}"),
        ]
    )

    add_routes(
        app,
        prompt | azure_chat_openai,
        path=path,
    )
