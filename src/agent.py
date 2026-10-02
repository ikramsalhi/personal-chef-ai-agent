from dotenv import load_dotenv
from tavily import TavilyClient

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

model = init_chat_model(
    model="gemini-3.1-flash-lite",
    model_provider="google_genai",
)

tavily = TavilyClient()


@tool
def web_search(query: str) -> str:
    """Search the web for useful cooking, ingredient, and recipe information."""
    result = tavily.search(query=query, max_results=5)
    rows = []
    for item in result.get("results", []):
        rows.append(
            f"Title: {item.get('title', '')}\n"
            f"URL: {item.get('url', '')}\n"
            f"Content: {item.get('content', '')}"
        )
    return "\n\n".join(rows) if rows else "No results found."


@tool
def servings_converter(
    ingredient_amount: float,
    original_servings: int,
    desired_servings: int,
) -> float:
    """Scale one ingredient amount from the original servings to the desired servings."""
    if original_servings <= 0 or desired_servings <= 0:
        raise ValueError("Servings must be greater than zero.")
    return ingredient_amount * desired_servings / original_servings


SYSTEM_PROMPT = """
You are Personal Chef, a practical cooking assistant.

Use tools when current information or calculations are useful.
Ask about dietary restrictions when they are relevant.
Do not invent exact nutrition or allergy claims.
Prefer clear, realistic recipes using ingredients the user actually has.
Keep answers concise unless the user asks for more detail.
"""

agent = create_agent(
    model=model,
    tools=[web_search, servings_converter],
    system_prompt=SYSTEM_PROMPT,
    checkpointer=InMemorySaver(),
)


def chat(message: str, thread_id: str = "chef-demo"):
    config = {"configurable": {"thread_id": thread_id}}
    return agent.invoke(
        {"messages": [{"role": "user", "content": message}]},
        config=config,
    )


if __name__ == "__main__":
    print("Personal Chef AI Agent")
    print("Type 'exit' to stop.\n")

    thread_id = "chef-cli"

    while True:
        user_text = input("You: ").strip()
        if user_text.lower() in {"exit", "quit"}:
            break

        response = chat(user_text, thread_id=thread_id)
        print("Chef:", response["messages"][-1].content)
