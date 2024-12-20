import gradio as gr
import os
import google.generativeai as genai

# Set Google API key 
os.environ['GOOGLE_API_KEY'] = "your_google_api_key"
genai.configure(api_key = os.environ['GOOGLE_API_KEY'])

# Create the Model
txt_model = genai.GenerativeModel('gemini-pro')

# Function that generates Response and displays on Chat UI
def llm_response(history, text):
    if not text:
        return history
    
    # Prepare conversation history for context
    conversation_history = []
    for user_msg, ai_msg in history:
        if user_msg:
            conversation_history.append(f"{user_msg}")
        if ai_msg:
            conversation_history.append(f"{ai_msg}")
    
    # Add current user message to conversation history
    conversation_history.append(f"Human: {text}")
    
    # Combine history into a single context string
    context = "\n".join(conversation_history)
    
    # Generate response with full conversation context
    response = txt_model.generate_content(context)
    
    # Update history with new interaction
    history += [(text, response.text)]
    return history

# Function to clear chat history
def clear_chat():
    return []

# Interface Code
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

    # Submit message
    btn.click(llm_response, [chatbot, text_box], chatbot)
    
    # Clear chat history
    clear_btn.click(clear_chat, None, chatbot)

app.queue()
app.launch(debug=True)
