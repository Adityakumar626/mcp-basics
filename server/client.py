import asyncio
from langchain_groq import ChatGroq

from mcp_use import MCPAgent , MCPClient
import os 
from dotenv import load_dotenv

async def run_memory_chat():
    """Run a chat using MCPAgent's built-in conversation memory."""

    # Load enviornment variable for api keys 
    load_dotenv()
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

    # config file path - change this to your config file 
    config_file = "server/weather.json"

    print("Initializing chat...")

    # create MCP client and agent with memory enabled 
    client = MCPClient.from_config_file(config_file)
    llm = ChatGroq(model="openai/gpt-oss-120b")

    # create agent with memory_enabled=True
    agent = MCPAgent(
        llm=llm,
        client=client,
        max_steps=15,
        memory_enabled=True , # enables built-in convo memory
    )

    print("\n===== Interactive MCP Chat =====")
    print("Type 'exit' or 'quit' to end the conversation")
    print("Type 'clear' to clear conversation history")
    print("==================================\n")

    try:
        # Main chat loop 
        while True : 
            # get user input 
            user_input = input("\nYou:")

            # check for exit command 
            if user_input.lower() in ["exit" , "quit"]:
                print("ending Conversation")
                break

            # check for clear history command 
            if user_input.lower() == "clear":
                agent.clear_conversation_history()
                print("Conversation history cleared.")
                continue

            # get response from agent 
            # flush - stream output immediately 
            print("\nAssistant: ", end="", flush=True) # end - prevent chunks from new line

            try : 
                # Run the agent with user input (memory handling is automatic)
                response = await agent.run(user_input)
                print(response)

            except Exception as e  :
                print(f"\nError: {e}")

    finally:
        # Clean Up 
        if client and client.sessions : 
            await client.close_all_sessions()

if __name__ == "__main__":
    asyncio.run(run_memory_chat())