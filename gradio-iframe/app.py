import gradio as gr
from gradio_iframe import iFrame


example = iFrame().example_inputs()

with gr.Blocks() as demo:
    with gr.Row():
        iFrame(value=("""
        <iframe width="560" 
            height="315" 
            src="http://127.0.0.1:5000/"
            title="YouTube video player" 
            frameborder="0" 
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
            allowfullscreen>
        </iframe>"""), label="Populated"),  # populated component
        iFrame(label="Blank"),  # blank component


demo.launch()
