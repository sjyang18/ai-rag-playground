import os

from autogen import AssistantAgent, UserProxyAgent, register_function
from autogen.cache import Cache
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from azure.search.documents import SearchClient
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()


credential = DefaultAzureCredential()
token_provider = get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")
llm_config = {
    "config_list": [
        {
            "model": "gpt-4o-deployment",  # replace with your model deployment name
            "base_url": os.getenv("AZURE_OPENAI_ENDPOINT"),
            "api_type": "azure",
            "api_version": "2024-05-01-preview",
            "max_tokens": 1000,
            "azure_ad_token_provider": token_provider,
        }
    ],
    "cache_seed": 42,
    "temperature": 0,
    "timeout": 120,
}


search_client = SearchClient(
    endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"), index_name=os.getenv("AZURE_AI_SEARCH_INDEX"), credential=credential
)

openai_client = AzureOpenAI(
    azure_ad_token_provider=token_provider,
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version="2024-05-01-preview",
)


def search(query: str):
    print("Searching for:", query)
    embeddings = openai_client.embeddings.create(model="text-embedding-3-small-deployment", input=[query])
    vector_embedding = embeddings.data[0].embedding
    results = search_client.search(
        search_text=query,
        vector_queries=[
            {
                "kind": "vector",
                "vector": vector_embedding,
                "fields": "text_vector",  # replace with your vector field name in the index
                "k": 10,
            }
        ],
        query_type="semantic",
        semantic_configuration_name=os.getenv("AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG"),
        top=10,
    )

    output = []
    for result in results:
        result.pop("text_vector")
        output.append(result)

    return output


cog_search = AssistantAgent(
    name="COGSearch",
    system_message="You are a helpful AI assistant that uses Azure Cognitive Search to find relevant information. "
    "For each user query, use the search function to find information, then summarize the results in a helpful way. "
    "Cite specific documents when providing information. Be concise but thorough."
    "Return 'TERMINATE' when the task is done.",
    llm_config=llm_config,
)

user_proxy = UserProxyAgent(
    name="User",
    llm_config=False,
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    human_input_mode="TERMINATE",
)

register_function(
    search,
    caller=cog_search,
    executor=user_proxy,
    name="search",
    description="A tool for searching the Cognitive Search index",
)

if __name__ == "__main__":
    import asyncio

    async def main():
        print("Welcome to the Cognitive Search Chatbot!")
        print("Type your questions and press Enter. Type 'exit' to end the conversation.")

        with Cache.disk() as cache:
            while True:
                user_question = input("\nYour question: ")
                if user_question.lower() == "exit":
                    print("Goodbye!")
                    break

                # Start a new conversation
                await user_proxy.a_initiate_chat(
                    cog_search,
                    message=user_question,
                    cache=cache,
                )

    asyncio.run(main())
