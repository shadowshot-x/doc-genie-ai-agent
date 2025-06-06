import asyncio
from graph import graph

async def main():
    from graph import graph
    graph = await graph.init_graph()

    async def stream_graph_updates(user_input: str):
        async for event in graph.astream({"messages": [{"role": "user", "content": user_input}]}):
            for value in event.values():
                print("Assistant:", value["messages"][-1].content)

    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break

            await stream_graph_updates(user_input)
        except Exception as e:
            print(e)
            # fallback if input() is not available
            break

if __name__ == "__main__":
    asyncio.run(main())