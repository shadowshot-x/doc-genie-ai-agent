from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage

class Prompts():
    router_prompt: str

    def __init__(self):
        all_prompts = ChatPromptTemplate.from_messages(
            [("system","Route the input to query_csv, query_file or normal_query based on the user's request. If user mentions a csv file in input, it will be query_csv. If user wants to understand something from text file it will be query_file. Else it will be normal_query")]
            [("genie","Describe this like a Genie. Keep answer short and precise : {humanMessage} \n{toolMessage}")]
        )

        all_prompt_messages = all_prompts.format_messages()
        self.router_prompt = all_prompt_messages[0]
