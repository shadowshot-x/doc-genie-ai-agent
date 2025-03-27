# Building AI Agents from scratch using LangGraph and Ollama: Part 1

Demystifying AI Agent Creation with LangGraph & Ollama: The First Phase of ‘Building AI Agents’ Series


## Introduction

### What are AI Agents?
AI agents are autonomous systems capable of executing tasks and decision-making based on predefined capabilities and local data sources, such as CSV files or 
documents. These agents utilize large language models (LLMs), like those provided by Ollama, to process and understand context-rich information.

### Project Description

This project aims to build an AI agent that interacts with your local datasets (CSV files and documents) via predefined query capabilities. Despite limited resources 
on Ubuntu 20.04 with 8GB RAM (no GPU), we demonstrate the feasibility of creating effective agents for information extraction from structured data.

### Required Tools

- **Ollama**
- **LangChain**
- **LangGraph**
- **Python**

## Use Case and Steps

### Step 1 : Use Case
DocGenie Agent simplifies local file interaction with users' queries:

1. Distinguishes generic from file-related questions.
2. Chooses appropriate tool for local data retrieval.
3. Summarizes and delivers results, streamlined by the ReAct Agent's pre-built logic.

![alt text](/figs/docgenie-basic-structure.jpg)

### Step 2 : Pull Ollama Model
```
ollama pull granite3.2:2b
```

### Step 3 : Understanding Code

A Tool is a Python function that has the following - 

- **Proper Name:** querycsv
- **Description in Triple Quotes**
- **Return Type**

This Pydantic formatted tool description enriches the model's understanding of how `querycsv` interacts with LLM by outlining its purpose, input type and output structure.

[CODE](https://github.com/shadowshot-x/doc-genie-ai-agent/blob/b049b79319fd54f8ed41b57306c5a3330e311f50/app/backend/main.py#L11)

Now, after tool is defined, we can import a prebuilt ReAct Agent. 

```python
agent_executor = create_react_agent(model, tools=tools)
```

This setup enables the AI system to dynamically respond to tasks without being constrained by a fixed flow. The `ReAct` agent acts as a reasoning and action 
decision-maker, enhancing flexibility in handling tasks based on contextual inputs.

[CODE](https://github.com/shadowshot-x/doc-genie-ai-agent/blob/b049b79319fd54f8ed41b57306c5a3330e311f50/app/backend/main.py#L29)

Call the messages using this :-
[CODE](https://github.com/shadowshot-x/doc-genie-ai-agent/blob/b049b79319fd54f8ed41b57306c5a3330e311f50/app/backend/main.py#L31-L37)

### Step 4 : Run the Flow

Run the Flow

```
python3 app/backend/main.py
```

1. **User Input:** Our AI system receives a query, unaware yet that it will trigger local data retrieval.
2. **LLM's Insight:** The Language Model (LLM) recognizes the need to interact with `querycsv`, our specialized tool for CSV file processing. It also decodes and 
generates an appropriate SQL command dynamically based on user queries—no predefined flow in sight!
3. **First Run - Misstep:** Initially, the generated SQL is incorrect, causing an error from `querycsv`. The LLM detects this mishap.
4. **Automated Correction:** Instead of manual intervention or a fresh start, our ReAct Agent springs into action:
   - Automatically re-evaluates and refines the SQL command for `querycsv` based on the current user query context.
   - Requests the tool to execute the corrected SQL command once more.
5. **Success:** With enhanced input this time, `querycsv` returns accurate data, fulfilling the request. The LLM receives the output without a hitch, marking the 
successful completion of our magic: an AI system that effortlessly comprehends user queries, intelligently decides on necessary actions, and executes them dynamically.

The combination of LangGraph's ReAct Agent and language models showcases this remarkable self-learning ability in handling unstructured inputs, exemplifying the power 
of dynamic decision-making and seamless automation in AI systems

## Problems with the Current Flow
1. **Low Accuracy and LLM Challenges:**
   - Our current agent struggles with errors, as seen repeatedly in screenshots, causing the Language Model (LLM) to fail in actionable comprehension.
   - Insufficient accuracy is a significant hurdle due to the model's inability to resolve issues consistently during query execution.

2. **Limitations of Pre-built ReAct Agent:**
   - The use of pre-built ReAct agents limits customization and debugging, hindering our ability to modify or fine-tune the flow for addressing identified problems 
effectively.

**Solution: Transition to LangGraph's Graph Architecture**

By adopting LangGraph’s graph architecture, we aim to overcome these limitations:

1. **Enhanced Accuracy:**
   - Leveraging more powerful LLMs integrated within this architecture improves accuracy significantly, minimizing errors and enabling the model to grasp and resolve 
issues with greater confidence.

2. **Full Control Over Flow:**
   - With the Graph Architecture, we gain complete control over every step of the request processing flow—from understanding user queries to executing actions through 
specialized tools like `querycsv`.
   - This granular control facilitates easier debugging and customization for tackling current challenges in real-time.

This shift promises a more robust, adaptable system, where each component can be precisely tuned according to our needs, delivering improved performance and user experience.





