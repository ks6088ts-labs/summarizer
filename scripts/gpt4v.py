import base64
import os

import requests
import typer
from dotenv import load_dotenv

app = typer.Typer()

load_dotenv("./azure_chat_openai.env")


@app.command()
def inference(
    image_path: str = "./data/receipt.png",
):
    # Most of the code in this function is boilerplate code to make the request from Azure AI Studio # noqa: E501
    GPT4V_KEY = os.getenv("api_key")
    GPT4V_ENDPOINT = f"{os.getenv('azure_endpoint')}openai/deployments/gpt-4/extensions/chat/completions?api-version=2023-07-01-preview"  # noqa: E501

    encoded_image = base64.b64encode(open(image_path, "rb").read()).decode("ascii")
    headers = {
        "Content-Type": "application/json",
        "api-key": GPT4V_KEY,
    }

    # Payload for the request
    payload = {
        "enhancements": {"ocr": {"enabled": True}, "grounding": {"enabled": True}},
        "messages": [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "You are an AI assistant that helps people find information.",  # noqa: E501
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "合計いくらのお会計ですか？"},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"},
                    },
                ],
            },
        ],
        "temperature": 0.7,
        "top_p": 0.95,
        "max_tokens": 800,
    }

    # Send request
    try:
        response = requests.post(GPT4V_ENDPOINT, headers=headers, json=payload)
        # Will raise an HTTPError if the HTTP request returned an unsuccessful status code # noqa: E501
        response.raise_for_status()
    except requests.RequestException as e:
        raise SystemExit(f"Failed to make the request. Error: {e}")

    # Handle the response as needed (e.g., print or process)
    print(response.json())


if __name__ == "__main__":
    app()
