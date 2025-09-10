# langchain_utils.py

from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage, AIMessage
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate

import pyttsx3

# --- 1. MEMORY SETUP ---
memory = ConversationBufferMemory(return_messages=True)


def add_to_memory(user_input, ai_response):
    memory.chat_memory.add_user_message(user_input)
    memory.chat_memory.add_ai_message(ai_response)


def get_memory_messages():
    return memory.load_memory_variables({})['history']


# --- 2. TEXT-TO-SPEECH ---
def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


# --- 3. INCLUSIVITY EXPLANATION PROMPT ---
def get_inclusivity_prompt(job_text):
    prompt = f"""
You are a DEI-focused assistant. Given the job description below, explain why this job appears inclusive or not, based on language and accommodations:

Job Description:
{job_text}

Provide a short explanation in 2-3 sentences.
"""
    return prompt


# --- 4. OUTPUT PARSER EXAMPLE (OPTIONAL STRUCTURED FORMAT) ---
response_schemas = [
    ResponseSchema(name="reason", description="Explanation of inclusivity."),
    ResponseSchema(name="score", description="Numeric inclusivity score from 1 to 10")
]

parser = StructuredOutputParser.from_response_schemas(response_schemas)

output_format_instructions = parser.get_format_instructions()

structured_prompt_template = PromptTemplate(
    template="""
Given the following job description:

{job_desc}

Please explain why it's inclusive and provide a numeric score.

{format_instructions}
""",
    input_variables=["job_desc"],
    partial_variables={"format_instructions": output_format_instructions}
)

def get_structured_prompt(job_desc):
    return structured_prompt_template.format(job_desc=job_desc)

def parse_structured_response(response_text):
    return parser.parse(response_text)