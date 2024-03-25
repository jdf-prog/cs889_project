import fire
import regex as re
import gradio as gr
import socketio

from easy_openai import openai_completions
from typing import List, Tuple
from pathlib import Path
support_codes = ['python', 'markdown', 'json', 'html', 'css', 'javascript', 'typescript', 'yaml', 'dockerfile', 'shell', 'r', 'sql', 'sql-msSQL', 'sql-mySQL', 'sql-mariaDB', 'sql-sqlite', 'sql-cassandra', 'sql-plSQL', 'sql-hive', 'sql-pgSQL', 'sql-gql', 'sql-gpSQL', 'sql-sparkSQL', 'sql-esper']

MODEL_NAME = None
sio=None
# Function to send input to the pty
def send_pty_input(input_data):
    sio.emit('pty-input', {'input': input_data}, namespace='/pty')

def execute_commands_given_by_chatbot(code_block:str):
    send_pty_input(code_block + "\n")
        
def to_openai_chat_format(message:str, chat_history:List[Tuple[str, str]]):
    chat_messages = []
    for i, (user_message, bot_message) in enumerate(chat_history):
        chat_messages.append({"role": "user", "content": user_message})
        chat_messages.append({"role": "assistant", "content": bot_message})
    chat_messages.append({"role": "user", "content": message})
    return chat_messages
    
def detect_code_language(code:str):
    message = "What's the langauge of the following code block?\n\n```" + code + "```" + "\nOptions: " + ", ".join(support_codes) + "\nPlease output the language name in the following format: 'language: <name>'"
    results = openai_completions(
        prompts=[message],
        model_name=MODEL_NAME,
        max_tokens=2048,
        temperature=0.7,
        top_p=1.0,
    )
    completion = results['completions'][0]
    language = re.search(r"language: (.*)", completion).group(1)
    return language

def get_code_block_by_idx(code_blocks:List[str], idx:int):
    
    language = None
    if not code_blocks:
        code = "No code blocks found yet"
    if idx is None:
        code = "No code blocks selected yet"
    elif idx >= len(code_blocks):
        code = "No more next code block found, please click the 'Show Previous Code Block' button to see the last code block"
    elif idx <= -1:
        code = "No more previous code block found, please click the 'Show Next Code Block' button to see the first code block"
    else:
        code, language = code_blocks[idx]
    return code, language

def extract_codes_from_chat_history(previous_code_blocks:List[str], chat_history:List[Tuple[str, str]]):
    last_message = chat_history[-1][1]
    # detect whether there are code blocks in the last message
    all_code_blocks = re.findall(r"```(.*?)```", last_message, re.DOTALL)
    all_code_blocks = [code_block.strip(' \n') for code_block in all_code_blocks]
    
    all_code_blocks_language = [detect_code_language(code_block) for code_block in all_code_blocks]
    all_code_blocks = [(code_block, language) for code_block, language in zip(all_code_blocks, all_code_blocks_language)]
    
    lastest_code_block_idx = len(previous_code_blocks) if all_code_blocks else None
    
    all_code_blocks = previous_code_blocks + all_code_blocks
    code, language = get_code_block_by_idx(all_code_blocks, lastest_code_block_idx)
    return all_code_blocks, lastest_code_block_idx, gr.Code(code, language=language)

def increase_idx(code_blocks:List[str], idx:int):
    if idx < len(code_blocks):
        idx += 1
    code, language = get_code_block_by_idx(code_blocks, idx)
    return idx, gr.Code(code, language=language)

def decrease_idx(code_blocks:List[str], idx:int):
    if idx > -1:
        idx -= 1
    code, language = get_code_block_by_idx(code_blocks, idx)
    return idx, gr.Code(code, language=language)



def respond(message, chat_history):
    chat_messages = to_openai_chat_format(message, chat_history)
    
    results = openai_completions(
        prompts=[chat_messages],
        model_name=MODEL_NAME,
        max_tokens=2048,
        temperature=0.7,
        top_p=1.0,
    )
    completion = results['completions'][0]
    chat_history.append((message, completion))
    return "", chat_history

def clear_codes(code_blocks, idx, code_block):
    return [], None, gr.Code("No code blocks found yet")


def main(
    server_port:int=5000,
    root_path:str="",
    terminal_addr="http://localhost:5001",
    model_name="gpt-3.5-turbo",
):
    global sio
    # Create a Socket.IO client
    sio = socketio.Client()
    # Connect to the Flask-SocketIO server
    sio.connect(terminal_addr, namespaces=['/pty'])
    global MODEL_NAME
    MODEL_NAME = model_name
    

    with gr.Blocks() as demo:
        user_icon_path = Path(__file__).parent / "assets/user.jpeg"
        bot_icon_path = Path(__file__).parent / "assets/bot.jpeg"
        
        gr.Markdown("## Chatbot Terminal Copilot")
        chatbot = gr.Chatbot(
            show_copy_button=True, 
            avatar_images=[user_icon_path, bot_icon_path],
            render_markdown=True,
        )
        msg = gr.Textbox(label="Ask me anything!")
        with gr.Row():
            submit = gr.Button("Send")
            clear = gr.ClearButton([msg, chatbot])
        
        extracted_codes = gr.State([])
        current_code_idx = gr.State(None)
        
        gr.Markdown("## Extracted code blocks from the chat history")
        code_block = gr.Code(label="Current Code Block (you can edit the extracted code here and execute them with one click!)")
        
        with gr.Row():
            previous_code_block_button = gr.Button("Show Previous Code Block")
            next_code_block_button = gr.Button("Show Next Code Block")
            execute_command_button = gr.Button("Execute Code Block")

        msg.submit(respond, [msg, chatbot], [msg, chatbot]).success(extract_codes_from_chat_history, [extracted_codes, chatbot], [extracted_codes, current_code_idx, code_block])
        submit.click(respond, [msg, chatbot], [msg, chatbot]).success(extract_codes_from_chat_history, [extracted_codes, chatbot], [extracted_codes, current_code_idx, code_block])
        
        previous_code_block_button.click(decrease_idx, [extracted_codes, current_code_idx], [current_code_idx, code_block])
        next_code_block_button.click(increase_idx, [extracted_codes, current_code_idx], [current_code_idx, code_block])
        execute_command_button.click(execute_commands_given_by_chatbot, [code_block])
        clear.click(clear_codes, [extracted_codes, current_code_idx, code_block], [extracted_codes, current_code_idx, code_block])
        
        gr.Examples(
            ["How to change a folder's name in bash?", "How to print a colored text using in python?", 
             "How to create a new React component?", "How to send a GET request using Axios in JavaScript?", 
             "How to read a file line by line in Python?", "How to connect to a MySQL database using PHP?",
             "How to convert a string to a date in Java?", "How to create a table in SQLite using Python?",
             "How to list all files in a directory using Node.js?", "How to install a package using pip in Python?"],
            inputs=msg,
        )
        
        
    demo.launch(server_port=server_port, inline=True, width="50%", height=500, root_path=root_path)


if __name__ == "__main__":
    fire.Fire(main)