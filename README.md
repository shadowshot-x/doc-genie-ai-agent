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

## Part 1 \[Blog Soon\]
1. What is Ollama?
2. What is Langchain?
3. How to provide tools to your Agent?
4. Run the Agent to get Interesting Insights.
5. Issues in the Current Flow

### How to Run
```
python3 app/backend/main.py
```

## Part 2
1. What is Langgraph?
2. Integrate Chatbot using Langgraph
3. Adding Additional Tools
4. Test the Flow and Visualize

## Part 3
1. More about Nodes and Edges
2. Create a Custom Node in Langgraph
3. How to Integrate Custom Node with Edges
4. Add Local Memory to Agent
5. Clean the Code