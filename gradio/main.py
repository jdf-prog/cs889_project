import gradio as gr
from gradio_iframe import iFrame

def flip_text(x):
    return x[::-1]

with gr.Blocks() as demo:
    gr.Markdown("CS889: DigitalDreamers Terminal Copilot")
    with gr.Row():
        iFrame(value=("""
        <iframe width="1000" 
            height="800"
            src="http://127.0.0.1:5000/"
            title="Terminal" 
            frameborder="0" 
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
            allowfullscreen>
        </iframe>"""), label="Populated"),
        with gr.Column():
            text_input = gr.Textbox()
            text_output = gr.Textbox()
            text_button = gr.Button("Flip")

    text_button.click(flip_text, inputs=text_input, outputs=text_output)


if __name__ == "__main__":
    demo.launch()
