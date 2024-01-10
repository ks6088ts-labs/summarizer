from azure.search.documents.indexes.models import (
    SearchableField,
    SearchField,
    SearchFieldDataType,
    SimpleField,
)
from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai import AzureOpenAIEmbeddings
from langchain_openai.chat_models import AzureChatOpenAI
from langserve import add_routes

from server.settings import azure_ai_search as azure_ai_search_settings
from server.settings import azure_chat_openai as azure_chat_openai_settings
from server.settings import azure_embeddings_openai as azure_embeddings_openai_settings

app = FastAPI()

prompt = ChatPromptTemplate.from_template(
    "Please summarize the following sentences in three lines,\
    using the same language as the original text.\n```\n{topic}\n```"
)

chat_settings = azure_chat_openai_settings.AzureChatOpenAiSettings()

azure_chat_openai_model = AzureChatOpenAI(
    api_version=chat_settings.api_version,
    azure_endpoint=chat_settings.azure_endpoint,
    azure_deployment=chat_settings.azure_deployment,
    api_key=chat_settings.api_key,
)

embeddings_settings = azure_embeddings_openai_settings.AzureEmbeddingsOpenAiSettings()

azure_embeddings_openai_model = AzureOpenAIEmbeddings(
    api_version=embeddings_settings.api_version,
    azure_endpoint=embeddings_settings.azure_endpoint,
    azure_deployment=embeddings_settings.azure_deployment,
    api_key=embeddings_settings.api_key,
    chunk_size=1,
)

ai_search_settings = azure_ai_search_settings.AzureAiSearchSettings()

fields = [
    SimpleField(
        name="id",
        type=SearchFieldDataType.String,
        key=True,
        filterable=True,
    ),
    SearchableField(
        name="content",
        type=SearchFieldDataType.String,
        searchable=True,
    ),
    SearchField(
        name="content_vector",
        type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
        searchable=True,
        vector_search_dimensions=len(azure_embeddings_openai_model.embed_query("Text")),
        vector_search_configuration="default",
    ),
    SearchableField(
        name="metadata",
        type=SearchFieldDataType.String,
        searchable=True,
    ),
    SearchableField(
        name="tag",
        type=SearchFieldDataType.String,
        searchable=True,
        retrievable=False,
        sortable=True,
    ),
]

vector_store = AzureSearch(
    azure_search_endpoint=ai_search_settings.azure_search_endpoint,
    azure_search_key=ai_search_settings.azure_search_key,
    index_name=ai_search_settings.index_name,
    embedding_function=azure_embeddings_openai_model.embed_query,
    semantic_query_language="ja-jp",
    fields=fields,
)

add_routes(
    app,
    prompt | azure_chat_openai_model,
    path="/azure_openai",
)
