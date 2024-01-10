# https://python.langchain.com/docs/integrations/vectorstores/azuresearch
import os

from azure.search.documents.indexes.models import (
    SearchableField,
    SearchField,
    SearchFieldDataType,
    SimpleField,
)
from dotenv import load_dotenv
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai import AzureOpenAIEmbeddings

# azure_embeddings_openai
load_dotenv("./azure_embeddings_openai.env")
load_dotenv("./azure_ai_search.env")


def get_embeddings() -> AzureOpenAIEmbeddings:
    api_version = os.getenv("api_version")
    azure_endpoint = os.getenv("azure_endpoint")
    azure_deployment = os.getenv("azure_deployment")
    api_key = os.getenv("api_key")

    return AzureOpenAIEmbeddings(
        api_version=api_version,
        azure_endpoint=azure_endpoint,
        azure_deployment=azure_deployment,
        api_key=api_key,
        chunk_size=1,
    )


def get_azure_search(index_name: str, embeddings: AzureOpenAIEmbeddings) -> AzureSearch:
    azure_search_endpoint = os.getenv("azure_search_endpoint")
    azure_search_key = os.getenv("azure_search_key")

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
            vector_search_dimensions=len(embeddings.embed_query("Text")),
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

    return AzureSearch(
        azure_search_endpoint=azure_search_endpoint,
        azure_search_key=azure_search_key,
        index_name=index_name,
        embedding_function=embeddings.embed_query,
        semantic_query_language="ja-jp",
        fields=fields,
    )


embeddings = get_embeddings()
azure_search = get_azure_search(
    index_name="azure-ai-search",
    embeddings=embeddings,
)

azure_search.add_texts(
    ["Test 1", "Test 2", "Test 3"],
    [
        {"title": "Title 1", "source": "A", "random": "10290"},
        {"title": "Title 2", "source": "A", "random": "48392"},
        {"title": "Title 3", "source": "B", "random": "32893"},
    ],
)

res = azure_search.similarity_search(query="Test 3 source1", k=3, search_type="hybrid")

print(res)
