import os
from operator import itemgetter
from typing import List

import typer
from dotenv import load_dotenv
from langchain_community.document_loaders import YoutubeLoader
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
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


@app.command()
def summarize(
    url: str = "https://www.youtube.com/watch?v=ahnGLM-RC1Y",
):
    loader = YoutubeLoader.from_youtube_url(
        youtube_url=url,
        add_video_info=True,
        language=["en", "ja", "id"],
        translation="en",
    )
    documents: List[Document] = loader.load()
    assert len(documents) == 1, "Only one document should be loaded"
    context = documents[0].page_content

    template = """以下の文章を簡潔に 3 行の日本語で要約してください。:
    ---
    {context}
    """
    prompt = ChatPromptTemplate.from_template(template)

    # https://python.langchain.com/docs/expression_language/how_to/map
    chain = (
        {
            "context": itemgetter("context"),
        }
        | prompt
        | model
        | StrOutputParser()
    )

    response = chain.invoke(
        {
            "context": context,
        }
    )
    print(f"response: {response}")


if __name__ == "__main__":
    # poetry run python scripts/youtube_app.py --url "https://www.youtube.com/watch?v=ahnGLM-RC1Y"
    app()
