import os

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

# Initialize Azure OpenAI client with DefaultAzureCredential
credential = DefaultAzureCredential()

token_provider = get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")

# Create token provider for Azure AI Search and get a token
search_scope = "https://search.azure.com/.default"
# Get an actual access token for search
search_token = credential.get_token(search_scope).token

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    azure_ad_token_provider=token_provider,
    api_version="2024-05-01-preview",
)

completion = client.chat.completions.create(
    model=os.getenv("AZURE_OPENAI_MODEL_DEPLOYMENT_NAME"),
    messages=[
        {
            "role": "system",
            "content": "You are an AI assistant that helps people find information from my data and citations you get from my data.",
        },
        {"role": "user", "content": "service certificate rotation in gcc?"},
    ],
    max_tokens=800,
    temperature=0,
    top_p=0,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None,
    extra_body={
        "data_sources": [
            {
                "type": "azure_search",
                "parameters": {
                    "endpoint": os.environ["AZURE_SEARCH_ENDPOINT"],
                    "index_name": os.environ["AZURE_AI_SEARCH_INDEX"],
                    "authentication": {"type": "access_token", "access_token": search_token},
                },
            }
        ]
    },
)

print(completion.model_dump_json(indent=2))
