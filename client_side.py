# import asyncio
# from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
# from langgraph.prebuilt import create_react_agent
# from langchain_mcp_adapters.client import MultiServerMCPClient
# from langchain_openai import AzureChatOpenAI
# from dotenv import load_dotenv
    
# load_dotenv()

# async def main():
#     model = AzureChatOpenAI(temperature=0.3, model="gpt-4o")

#     async with MultiServerMCPClient(
#         {
#             # "crypto": {
#             #     "url": "http://localhost:8001/sse",
#             #     "transport": "sse",
#             # },
#             # "weather": {
#             #     "url": "http://localhost:8000/sse",
#             #     "transport": "sse",
#             # },
#             "search": {
#                 "url": "http://localhost:8000/sse",  # Assuming port 8010
#                 "transport": "sse",
#             }
#         }
#     ) as client:
#         agent = create_react_agent(model, client.get_tools())
#         # agent_response = await agent.ainvoke({"messages": "Get price of sui crpto coin?"})
#         # agent_response = await agent.ainvoke({"messages": "what is the weather in nyc?"})
#         agent_response = await agent.ainvoke({"messages": "What are the key features of Revolut app?"})

#         for response in agent_response["messages"]:
#             user = ""
#             if isinstance(response, HumanMessage):
#                 user = "User"
#             elif isinstance(response, ToolMessage):
#                 user = "Tool"
#             elif isinstance(response, AIMessage):
#                 user = "AI"

#             if isinstance(response.content, list):
#                 print(f'{user}: {response.content[0].get("text", "")}')
#                 continue
#             print(f"{user}: {response.content}")

# # Run the async function
# asyncio.run(main())






import asyncio
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
    
load_dotenv()

async def run_query(agent, query):
    print(f"\nQuery: {query}")
    agent_response = await agent.ainvoke({"messages": query})
    
    for response in agent_response["messages"]:
        user = ""
        if isinstance(response, HumanMessage):
            user = "User"
        elif isinstance(response, ToolMessage):
            user = "Tool"
        elif isinstance(response, AIMessage):
            user = "AI"

        if isinstance(response.content, list):
            content = response.content[0].get("text", "")
        else:
            content = response.content
        
        if user:  # Only print non-empty messages
            print(f"{user}: {content}")

async def main():
    model = AzureChatOpenAI(temperature=0.3, model="gpt-4o")

    async with MultiServerMCPClient(
        {
            "weather": {
                "url": "http://localhost:8000/sse",
                "transport": "sse",
            }
        }
    ) as client:
        agent = create_react_agent(model, client.get_tools())
        
        # US Examples
        await run_query(agent, "What are the current weather alerts for Atlanta?")
        # await run_query(agent, "What's the forecast for New York City? (provide coordinates 40.7128,-74.0060)")
        
        # # UK Examples
        # await run_query(agent, "What's the weather forecast for London, UK?")
        
        # # India Examples
        # await run_query(agent, "What's the current temperature in Kolkata, India?")
        # await run_query(agent, "Get weather update for Mumbai, India")

# Run the async function
asyncio.run(main())