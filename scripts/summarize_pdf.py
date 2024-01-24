import os
import timeit
from typing import List

from dotenv import load_dotenv
from langchain.prompts.chat import (
    ChatPromptTemplate,
)
from langchain.schema.output_parser import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_core.runnables import RunnableParallel
from langchain_openai.chat_models import AzureChatOpenAI


def load_documents(file_path: str) -> List[Document]:
    loader = PyPDFLoader(file_path=file_path)
    return loader.load_and_split()


def split_documents_to_chunks(documents: List[Document]) -> List[Document]:
    text_splitter = RecursiveCharacterTextSplitter(
        separators=[
            "\n\n",
            "\n",
            "。",
        ],
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)


load_dotenv("./azure_chat_openai.env")

model = AzureChatOpenAI(
    api_version=os.getenv("api_version"),
    azure_endpoint=os.getenv("azure_endpoint"),
    azure_deployment=os.getenv("azure_deployment"),
    api_key=os.getenv("api_key"),
)

# To understand LCEL: https://www.youtube.com/watch?v=9M8x485j_lU
summarize_chain = (
    ChatPromptTemplate.from_template("以下のコンテンツを要約してください。\n---\n{content}")
    | model
    | StrOutputParser()
)
keyword_chain = (
    ChatPromptTemplate.from_template("以下のコンテンツにおける主要な名詞を 3 つ抽出してください。\n---\n{content}")
    | model
    | StrOutputParser()
)
parallel_chain = RunnableParallel(
    summary=summarize_chain,
    keywords=keyword_chain,
)

documents = load_documents(file_path="./data/test.pdf")
chunks = split_documents_to_chunks(documents=documents)

# TORIAEZU
content = chunks[0].page_content


response = parallel_chain.invoke({"content": content})

print(f"response: {response}, type: {type(response)}")

result = timeit.timeit(
    'parallel_chain.invoke({"content": content})',
    globals=globals(),
    number=1,
)
print(f"parallel_chain result: {result}")
result = timeit.timeit(
    'summarize_chain.invoke({"content": content})',
    globals=globals(),
    number=1,
)
print(f"summarize_chain result: {result}")
result = timeit.timeit(
    'keyword_chain.invoke({"content": content})',
    globals=globals(),
    number=1,
)
print(f"keyword_chain result: {result}")
