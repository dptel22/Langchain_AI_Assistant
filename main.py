from dotenv import load_dotenv
import os
import gradio as gr

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

gemini_key = os.getenv("GEMINI_API_KEY")

system_prompt = """
You are the smartest person in the world. You possess limitless knowledge across every domain and can answer
any question with accuracy, clarity, and depth. Your role is to explain concepts in the
**most understandable, simple, and engaging way possible**, tailored to the background and level of the person asking.
Always break down complex ideas into clear steps, use examples or analogies where helpful,
and emphasize key points for better retention. You are not just providing answers; you are teaching, guiding,
and illuminating in the most effective way.

In addition, your tone should be witty, clever, and lightly humorous when appropriate—never dry or robotic.
You are real, authentic, and unbiased, presenting facts honestly while also adding a touch of personality.
You are Neil deGrasse Tyson in style: scientifically curious, thought-provoking, playfully insightful,
and always aiming to make people say, "Wow, I never thought of it that way before."

Keep responses **short, concise, and impactful**—no rambling, just sharp clarity with personality.
"""

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=gemini_key,
    temperature=0.5
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="history"),
    ("user", "{input}")
])

chain = prompt | llm | StrOutputParser()

print("Hi, I am Neil deGrasse Tyson, How can I help you?")


def chat(user_input, hist):
    langchain_history = []
    for item in hist:
        if item['role'] == 'user':
            langchain_history.append(HumanMessage(content=item['content']))
        elif item['role'] == 'assistant':
            langchain_history.append(AIMessage(content=item['content']))

    response = chain.invoke({"input": user_input, "history": langchain_history})

    return "", hist + [{'role': "user", 'content': user_input},
                       {'role': "assistant", 'content': response}]


page = gr.Blocks(
    title="Chat with Neil deGrasse Tyson",
    theme=gr.themes.Soft()
)

with page:
    gr.Markdown(
        """
        # Chat with Neil deGrasse Tyson
        Step into a conversation where science meets curiosity, sprinkled with wit and wonder. I'm here to explain 
        anything—from black holes to buttered toast—in the clearest, sharpest, and most thought-provoking way possible.
        Ask away, and let's make you say: "Wow, I never thought of it that way before."
        """
    )

    chatbot = gr.Chatbot(type='messages')

    msg = gr.Textbox()

    msg.submit(chat, [msg, chatbot], [msg, chatbot])

    clear = gr.Button("Clear Chat")
    clear.click(lambda: ([], ""), None, [chatbot, msg])

page.launch(share=True)