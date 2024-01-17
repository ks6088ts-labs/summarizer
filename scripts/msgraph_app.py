import os

import typer
from dotenv import load_dotenv

load_dotenv("./ms_app.env")
app = typer.Typer()


@app.command()
def run_msal():
    # PythonからSharePointにファイルアップロードしたいッッ！: https://zenn.dev/dencyu/articles/7c018ae166e278
    import msal
    import requests

    # Get an app
    app = msal.ConfidentialClientApplication(
        client_id=os.getenv("client_id"),
        client_credential=os.getenv("client_credential"),
        authority=f"https://login.microsoftonline.com/{os.getenv('tenant_id')}",
    )

    # Get an access token
    scope = os.getenv("scope")
    token = app.acquire_token_silent([scope], account=None)

    if not token:
        print("No suitable token exists in cache. Let's get a new one from AAD.")
        token = app.acquire_token_for_client(scopes=[scope])
    print(f"got token={token}")

    graph_data = requests.get(
        "https://graph.microsoft.com/v1.0/sites",
        headers={"Authorization": "Bearer " + token["access_token"]},
    ).json()
    print(graph_data)


@app.command()
def run_msgraphsdk():
    # msgraph-sdk-python: https://github.com/microsoftgraph/msgraph-sdk-python?tab=readme-ov-file#3-make-requests-against-the-service
    import asyncio

    from azure.identity.aio import ClientSecretCredential
    from msgraph import GraphServiceClient
    from msgraph.generated.models.entity_type import EntityType
    from msgraph.generated.models.search_query import SearchQuery
    from msgraph.generated.models.search_request import SearchRequest
    from msgraph.generated.models.search_response import SearchResponse
    from msgraph.generated.search.query.query_post_request_body import (
        QueryPostRequestBody,
    )

    credential = ClientSecretCredential(
        client_id=os.getenv("client_id"),
        client_secret=os.getenv("client_credential"),
        tenant_id=os.getenv("tenant_id"),
    )
    client = GraphServiceClient(
        credentials=credential,
        scopes=[os.getenv("scope")],
    )

    # GET /users/{id | userPrincipalName}
    async def get_user():
        # update the user_principal_name to the user you want to get
        user_principal_name = "USER@CONTOSO.onmicrosoft.com"
        user = await client.users.by_user_id(user_principal_name).get()
        if user:
            print(user.display_name)

    # https://github.com/microsoftgraph/msgraph-sdk-python/blob/main/docs/drives_samples.md#1-list-all-drives-get-drives
    async def get_drives():
        drives = await client.drives.get()
        if drives and drives.value:
            for drive in drives.value:
                print(
                    drive.id,
                    drive.drive_type,
                    drive.name,
                    drive.description,
                    drive.web_url,
                )

    async def search():
        results = await client.search.query.post(
            body=QueryPostRequestBody(
                requests=[
                    SearchRequest(
                        entity_types=[EntityType.ListItem],
                        query=SearchQuery(
                            query_string="contoso",
                        ),
                        size=1,
                        region="NAM",
                    )
                ],
            )
        )
        if results and results.value:
            for i, result in enumerate(results.value):
                response: SearchResponse = result
                print(f"{i}: {response}")

    # asyncio.run(get_user())
    # asyncio.run(get_drives())
    asyncio.run(search())


if __name__ == "__main__":
    app()
