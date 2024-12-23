import gradio as gr
import os
import google.generativeai as genai

os.environ['GOOGLE_API_KEY'] = "your_google_api_key"
genai.configure(api_key = os.environ['GOOGLE_API_KEY'])

txt_model = genai.GenerativeModel('gemini-pro')

def llm_response(history, text):
    if not text:
        return history
    
    conversation_history = []
    for user_msg, ai_msg in history:
        if user_msg:
            conversation_history.append(f"{user_msg}")
        if ai_msg:
            conversation_history.append(f"{ai_msg}")
    
    conversation_history.append(f"Human: {text}")
    
    context = "\n".join(conversation_history)
    
    response = txt_model.generate_content(context)
    
    history += [(text, response.text)]
    return history

def clear_chat():
    return []

with gr.Blocks() as app:
    chatbot = gr.Chatbot(
        height=400
    )
    
    text_box = gr.Textbox(
        placeholder="Enter your message and press enter",
        container=False,
    )

    btn = gr.Button("Submit")
    clear_btn = gr.Button("Clear Chat")

    btn.click(llm_response, [chatbot, text_box], chatbot)
    
    clear_btn.click(clear_chat, None, chatbot)

app.queue()
app.launch(debug=True)
