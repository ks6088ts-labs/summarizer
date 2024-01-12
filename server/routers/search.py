from azure.search.documents.indexes.models import (
    SearchableField,
    SearchField,
    SearchFieldDataType,
    SimpleField,
)
from fastapi import FastAPI
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai import AzureOpenAIEmbeddings
from langserve import add_routes

from server.settings import azure_ai_search as azure_ai_search_settings
from server.settings import azure_embeddings_openai as azure_embeddings_openai_settings


def add_router(app: FastAPI, path: str):
    embeddings_settings = (
        azure_embeddings_openai_settings.AzureEmbeddingsOpenAiSettings()
    )

    embeddings = AzureOpenAIEmbeddings(
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
        # Additional field to store the title
        SearchableField(
            name="title",
            type=SearchFieldDataType.String,
            searchable=True,
        ),
        # Additional field for filtering on document source
        SimpleField(
            name="source",
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

    vector_store = AzureSearch(
        azure_search_endpoint=ai_search_settings.azure_search_endpoint,
        azure_search_key=ai_search_settings.azure_search_key,
        index_name=ai_search_settings.index_name,
        embedding_function=embeddings.embed_query,
        semantic_query_language="ja-jp",
        fields=fields,
    )

    add_routes(
        app,
        vector_store.as_retriever(),
        path=path,
    )
