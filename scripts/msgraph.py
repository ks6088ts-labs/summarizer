import logging
import os

import requests
import typer
from dotenv import load_dotenv

load_dotenv("./ms_app.env")
app = typer.Typer()


@app.command()
def run_msal():
    # PythonからSharePointにファイルアップロードしたいッッ！: https://zenn.dev/dencyu/articles/7c018ae166e278
    import msal

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
        logging.info("No suitable token exists in cache. Let's get a new one from AAD.")
        token = app.acquire_token_for_client(scopes=[scope])
    print(f"got token={token}")

    graph_data = requests.get(
        "https://graph.microsoft.com/v1.0/sites",
        headers={"Authorization": "Bearer " + token["access_token"]},
    ).json()
    print(graph_data)


if __name__ == "__main__":
    app()
