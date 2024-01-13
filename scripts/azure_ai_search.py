import os
from enum import Enum

from azure.search.documents.indexes.models import (
    SearchableField,
    SearchField,
    SearchFieldDataType,
    SimpleField,
)
from dotenv import load_dotenv
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai import AzureOpenAIEmbeddings


class ResourceTag(Enum):
    BASIC = "basic"
    ADVANCED = "advanced"


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


def get_azure_search(embeddings: AzureOpenAIEmbeddings) -> AzureSearch:
    index_name = os.getenv("index_name")
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

    return AzureSearch(
        azure_search_endpoint=azure_search_endpoint,
        azure_search_key=azure_search_key,
        index_name=index_name,
        embedding_function=embeddings.embed_query,
        semantic_query_language="ja-jp",
        fields=fields,
    )


def main():
    # load environment variables
    load_dotenv("./azure_embeddings_openai.env")
    load_dotenv("./azure_ai_search.env")

    # instantiate AzureOpenAIEmbeddings
    embeddings = get_embeddings()

    # instantiate AzureSearch
    azure_search = get_azure_search(
        embeddings=embeddings,
    )

    # add mock documents into AzureSearch
    response = azure_search.add_texts(
        texts=["テスト 1", "テスト 2", "テスト 3"],
        metadatas=[
            {
                "title": "タイトル 1",
                "source": "A",
                "random": "10290",
                "tag": ResourceTag.BASIC.value,
            },
            {
                "title": "タイトル 2",
                "source": "A",
                "random": "48392",
                "tag": ResourceTag.ADVANCED.value,
            },
            {
                "title": "タイトル 3",
                "source": "B",
                "random": "32893",
                "tag": ResourceTag.BASIC.value,
            },
        ],
    )
    print(f"add_texts response: {response}")

    # Note: need to wait until the index is updated

    # query for similar documents with filters
    for tag in [ResourceTag.BASIC.value, ResourceTag.ADVANCED.value]:
        response = azure_search.similarity_search(
            query="テスト 3",
            k=3,
            search_type="hybrid",
            filters=f"tag eq '{tag}'",
        )
        print(f"tag: {tag}, response, {response}")


if __name__ == "__main__":
    main()
