# Doc Gini Agent

Tutorial on how to build an AI Agent from scratch.

The main usecase is to Query CSV Files and provide interesting observations based on user queries.

The Idea is to enable anyone build AI Agents Locally and make these Agents Production Grade

Tools
1. Ollama
2. Langgraph
3. Langchain

Platform Used to Build \[Platform is generic and can be used by any OS\]
```
Ubuntu 20.04. RAM - 8BG. No GPU
```

Python3.9+ is required

Starting Ollama
```
sudo systemctl start ollama
```

Model Used \[Tool Support Needed in LLM\]
1. `granite3.2:2b`

Stopping Ollama
```
sudo systemctl stop ollama
```

### How to Run
```
python3 app/backend/main.py
```

## Part 1 : [BLOG LINK](https://levelup.gitconnected.com/building-ai-agents-from-scratch-using-langgraph-and-ollama-part-1-3f91068d6dc3?gi=350f1ef173ea)
1. What is Ollama?
2. What is Langchain?
3. How to provide tools to your Agent?
4. Run the Agent to get Interesting Insights.
5. Issues in the Current Flow

![alt text](/figs/docgenie-basic-structure.jpg)

**For those who don't have medium membership, I have summarized the blog using AI. It can be found [HERE](docs/part1.md)**

## Part 2 [BLOG LINK](https://medium.com/gitconnected/building-ai-agents-from-scratch-using-langgraph-and-ollama-part-2-b62edbe23344)
1. What is Langgraph?
2. Integrate Chatbot using Langgraph
3. Adding Additional Tools
4. Test the Flow and Visualize

![alt text](/figs/part2.png)

## Part 3 [BLOG LINK](https://levelup.gitconnected.com/custom-nodes-and-state-in-langgraph-powered-by-ollama-ebecb4566adf)
1. More about Nodes and Edges
2. Create a Custom Node in Langgraph
3. How to Integrate Custom Node with Edges
4. Add Local Memory to Agent
5. Clean the Code

![alt text](/figs/part3.png)

## Part 4
1. Adding a Router Node
2. How to Utilize and Manipulate State
3. Building Text Agent
4. Add Conditional Routing Edges between multiple Agents
5. Understanding the Architecture

## Part 5
1. Understanding RAG
2. Setting up and Running ChromaDB
3. Ingesting Documents into ChromaDB
4. Integrating RAG with Agent
5. Understandint the Flow

```
docker run -d --rm --name chromadb -p 8000:8000 -v ./chroma:/chroma/chroma -e IS_PERSISTENT=TRUE -e ANONYMIZED_TELEMETRY=TRUE chromadb/chroma:0.6.3
```

## Part 6
1. Understanding MCP
2. Create STDIO MCP FastServer
3. Converting entire Call Stack to async
4. Understanding Request Flow from LangGraph to MCP
