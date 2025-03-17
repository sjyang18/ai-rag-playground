import os

from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient
from dotenv import load_dotenv

load_dotenv()

from azure.identity import get_bearer_token_provider

credential = DefaultAzureCredential()
token_provider = get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")

search_client = SearchClient(
    endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"), index_name=os.getenv("AZURE_AI_SEARCH_INDEX"), credential=credential
)

results = search_client.search(
    search_text="GCC service certificate rotation runbook with ADO pipeline",
    query_type="semantic",
    semantic_configuration_name=os.getenv("AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG"),
    top=10,
)

first_result = next(iter(results))
print("Available fields:", list(first_result.keys()))

for result in results:
    print("-------------------")
    print(result.get("chunk"))
    print(result.get("title"))
    print(result.get("@search.score"))
