from easy_openai import openai_completions
prompts = ["Respond with one digit: 1+1=", "Respond with one digit: 2+2="]
chatmls = [[{"role":"system","content":"You are an AI assistant that helps people find information."},
            {"role":"user","content": prompt}] for prompt in prompts]
openai_completions(chatmls, model_name="ChatGPT", max_tokens=50) # change model_name to your desired model