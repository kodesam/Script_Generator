import openai
import random
import gradio as gr
import os

openai.api_key = os.environ["OpenAPI_Key"]

manual = r"""Input your variables in the fields on the left. The last one (Extra input...) is optional, you can use it to steer the prompt into a certain direction by adding more requirements.
"""

# Define the messages for step_1
SystemPrompt_10 = r""""You are a travelAI guide and prompt engineer to create itinarary. 

Make sure to include what sort of information the user needs to type into the prompt. 

When creating the script, please follow this structure: 
- Create Travel Itinirary 
- Duration of Stays
- List of all Top rated places
- List of all must visit places
- List of good Hotel 
- Best places to eats
- Exploration activities

Feel free to be creative."""
UserPrompt_10 = r""""Create a Travel Itinirary 
Additional instructions: At least 3 possible Itinirary """
AssistantPrompt_10 = r""""*HOOK*




# Function to make API call
def api_call(messages, temperature=0.9, model="gpt-4-1106-preview"):
    return openai.ChatCompletion.create( 
        messages=messages,
        temperature=temperature,
        model=model
    ).choices[0].message.content

# Function to be called by Gradio interface
def process_inputs(EPA_title, Department, Extra_input):
    # Check if EPA_title and/or Department are empty
    if not EPA_title and not Department:
        return manual
    if not Extra_input:
        stepOne = [
            {"role": "system", "content": SystemPrompt_10},
            {"role": "user", "content": UserPrompt_10},
            {"role": "assistant", "content": AssistantPrompt_10},
            {"role": "user", "content": f"""Create a Travel Itinirary: {EPA_title}
The target audience is: a tourist {Department} ."""}
        ]
    else:
        # Step 1: User input and first API call ~5secs
        stepOne = [
            {"role": "system", "content": SystemPrompt_10},
            {"role": "user", "content": UserPrompt_10},
            {"role": "assistant", "content": AssistantPrompt_10},
            {"role": "user", "content": f"""Create a Create a Travel Itinirary: {EPA_title}
The target audience is: a tourist in a {Department} . 
Additional instructions: {Extra_input}"""}
        ]
    
    Script_1 = api_call(stepOne, 0.7)
    return Script_1



# Create the Gradio interface 
iface = gr.Interface(
    fn=process_inputs, 
    inputs=[
        gr.Textbox(lines=2, label='Travel Itinirary... (use the phrasing: "How to do X with ChatGPT")'), 
        gr.Textbox(lines=2, label='Duration... (eg: days)'), 
        gr.Textbox(lines=2, label='type of itinary... (optional, put any extra requirements or relevant context)')
        ], 
    outputs=gr.Textbox(label="Script", show_copy_button=True)
)

iface.launch(share=True)
iface.launch()
