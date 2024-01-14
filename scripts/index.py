import os
from enum import Enum

import typer
from azure.search.documents.indexes.models import (
    SearchableField,
    SearchField,
    SearchFieldDataType,
    SimpleField,
)
from dotenv import load_dotenv
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai import AzureOpenAIEmbeddings

app = typer.Typer()


# load environment variables
load_dotenv("./azure_embeddings_openai.env")
load_dotenv("./azure_ai_search.env")


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


def get_azure_search() -> AzureSearch:
    embeddings = get_embeddings()

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

    return AzureSearch(
        azure_search_endpoint=azure_search_endpoint,
        azure_search_key=azure_search_key,
        index_name=index_name,
        embedding_function=embeddings.embed_query,
        semantic_query_language="ja-jp",
        fields=fields,
    )


@app.command()
def create():
    azure_search = get_azure_search()

    loader = CSVLoader(
        file_path="./data/favorite_sports.csv",
        csv_args={"delimiter": ",", "quotechar": '"'},
        encoding="utf-8",
        # NOTE: metadata_columns is dependent on the csv file
        metadata_columns=["title", "name", "sports", "tag"],
    )
    documents = loader.load()
    print(f"---\nloaded documents\n---\n{documents}")

    response = azure_search.add_documents(documents=documents)
    print(f"---\add_documents response\n---\n{response}")


@app.command()
def search(query: str = "", filters: str = None):
    azure_search = get_azure_search()

    response = azure_search.similarity_search(
        query=query,
        k=3,
        search_type="hybrid",
        filters=filters,
    )
    print(f"similarity_search response(query={query}, filters={filters}): {response}")


if __name__ == "__main__":
    """
    # Help
    poetry run python scripts/index.py --help
    # Create Azure Search Index
    poetry run python scripts/index.py create
    # Search
    poetry run python scripts/index.py search \
        --query "河原町二郎" --filters "tag eq 'basic'"
    """
    app()
