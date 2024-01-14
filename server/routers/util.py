from azure.search.documents.indexes.models import (
    SearchableField,
    SearchField,
    SearchFieldDataType,
    SimpleField,
)
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai import AzureOpenAIEmbeddings
from langchain_openai.chat_models import AzureChatOpenAI

from server.settings import azure_ai_search as azure_ai_search_settings
from server.settings import azure_chat_openai as azure_chat_openai_settings
from server.settings import azure_embeddings_openai as azure_embeddings_openai_settings


def get_azure_chat_openai():
    chat_settings = azure_chat_openai_settings.AzureChatOpenAiSettings()
    return AzureChatOpenAI(
        api_version=chat_settings.api_version,
        azure_endpoint=chat_settings.azure_endpoint,
        azure_deployment=chat_settings.azure_deployment,
        api_key=chat_settings.api_key,
    )


def get_azure_openai_embeddings():
    embeddings_settings = (
        azure_embeddings_openai_settings.AzureEmbeddingsOpenAiSettings()
    )

    return AzureOpenAIEmbeddings(
        api_version=embeddings_settings.api_version,
        azure_endpoint=embeddings_settings.azure_endpoint,
        azure_deployment=embeddings_settings.azure_deployment,
        api_key=embeddings_settings.api_key,
        chunk_size=1,
    )


def get_azure_search(fields: list, embeddings: AzureOpenAIEmbeddings):
    ai_search_settings = azure_ai_search_settings.AzureAiSearchSettings()

    return AzureSearch(
        azure_search_endpoint=ai_search_settings.azure_search_endpoint,
        azure_search_key=ai_search_settings.azure_search_key,
        index_name=ai_search_settings.index_name,
        embedding_function=embeddings.embed_query,
        semantic_query_language="ja-jp",
        fields=fields,
    )


def get_azure_search_fields(embeddings: AzureOpenAIEmbeddings):
    return [
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
            analyzer_name="ja.lucene",
        ),
        SearchField(
            name="content_vector",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=len(embeddings.embed_query("Text")),
            vector_search_configuration="default",
        ),
        SearchableField(
            name="metadata",
            type=SearchFieldDataType.String,
            searchable=True,
        ),
        SearchableField(
            name="title",
            type=SearchFieldDataType.String,
            searchable=True,
        ),
        SearchableField(
            name="name",
            type=SearchFieldDataType.String,
            searchable=True,
        ),
        SimpleField(
            name="sports",
            type=SearchFieldDataType.String,
            filterable=True,
        ),
        SearchableField(
            name="tag",
            type=SearchFieldDataType.Collection(SearchFieldDataType.String),
            filterable=True,
            retrievable=False,
        ),
    ]
