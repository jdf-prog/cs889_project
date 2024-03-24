# cs886_project

## Installation
* pip install flask flask_cors gradio
* pip install -r pyxtermjs/requirements.txt
* go to gradio-iframe/src and run `pip install -e .`
## Running
* Run terminal webpage: python pyxtermjs/pyxtermjs/app.py (make sure flask is listing on localhost:5000, otherwise change the url in gradio/main.py)
* Run gradio: python gradio/main.py