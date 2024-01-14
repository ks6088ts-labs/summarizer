from fastapi import FastAPI
from langchain.prompts.chat import (
    ChatPromptTemplate,
)
from langchain.prompts.prompt import PromptTemplate
from langchain.schema import format_document
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langserve import add_routes

from server.routers import util

DEFAULT_DOCUMENT_PROMPT = PromptTemplate.from_template(template="{page_content}")


def _combine_documents(
    docs, document_prompt=DEFAULT_DOCUMENT_PROMPT, document_separator="\n\n"
):
    doc_strings = [format_document(doc, document_prompt) for doc in docs]
    return document_separator.join(doc_strings)


def add_router(app: FastAPI, path: str):
    # retriever
    azure_openai_embeddings = util.get_azure_openai_embeddings()
    azure_search_fields = util.get_azure_search_fields(
        embeddings=azure_openai_embeddings,
    )
    azure_search = util.get_azure_search(
        fields=azure_search_fields,
        embeddings=azure_openai_embeddings,
    )
    retriever = azure_search.as_retriever()

    # RAG prompt
    template = """Answer the question based only on the following context:
    {context}

    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)

    # LLM
    model = util.get_azure_chat_openai()

    add_routes(
        app,
        RunnableParallel(
            {
                "context": retriever | _combine_documents,
                "question": RunnablePassthrough(),
            }
        )
        | prompt
        | model,
        path=path,
    )
