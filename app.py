import openai
import random
import gradio as gr
import os

openai.api_key = os.environ["OpenAPI_Key"]

manual = r"""Input your variables in the fields on the left. The last one (Extra input...) is optional, you can use it to steer the prompt into a certain direction by adding more requirements.
"""

# Define the messages for step_1
SystemPrompt_10 = r""""You are a script writer and prompt engineer creating engaging YouTube tutorial scripts on how to use ChatGPT for various tasks in a corporate environment. 

Make sure to include what sort of information the user needs to type into the prompt. 

When creating the script, please follow this structure: 
- Hook
- Title
- Introduction
- Learning Objectives Summary
- Learning Objective 1
- Learning Objective 2
- Conclusion

Feel free to be creative."""
UserPrompt_10 = r""""Create a script for teaching an employee: How to create a Job Ad with ChatGPT.
Additional instructions: Use digital marketing manager as an example role."""
AssistantPrompt_10 = r""""*HOOK*
If you want your job ads to be found by the right candidates, you have to incorporate the right SEO-friendly keywords.

But how do you accomplish this without a lot of experience in Search Engine Optimization? 

Well, with ChatGPT. 

*TITLE*
Create a Job Ad with ChatGPT

*INTRO*
In this digital age, getting your job ad to stand out amongst the rest is crucial to finding the best candidates.

Today, we'll show you how to use ChatGPT to create a job ad that not only resonates with your ideal candidates, but also ranks high with SEO-friendly keywords. 

*LEARNING OBJECTIVES SUMMARY*
You will learn how to:

- Create an ideal job description

- Extract SEO Friendly Keywords 

- Craft a Job Ad 

Let's dive right in!

*LEARNING OBJECTIVE 1*
You can't create the perfect job ad without first creating the job description. 

Creating a comprehensive job description is critical for attracting the right candidates, setting expectations, and ensuring both the employee and employer understand the role's responsibilities.   

To create a basic job description, you would at least need to define the job title, the overview of the role, and the role's key responsibilities.

 It's also preferable to already identify any other details about the role, like qualifications and skills, experience level, salary and benefits, reporting structure, and working hours.    

Let's say you've been tasked to recruit a 'Digital Marketing Manager'.

Gather as much information as you can on the specifics of this job from the person that made the request. 

For this tutorial, we'll be using the following sample information.


The job title is "Digital marketing manager."

The overview of the role is "The digital marketing manager is responsible for managing the overall digital marketing strategy of xpedite.ai. He/she is also responsible for:
-	overseeing online marketing campaigns and other digital projects to optimize online brand presence and boost revenue.
-	manageing a team of 3 digital marketers." 

The key responsibilities of the role are "propose and execute digital marketing strategies, manage and oversee digital channels, monitor and measure ROI and KPIs of online campaigns."

Now, we're ready to write our prompt. 

Type: "You are a recruiter. Create a job description for a digital marketing manager.


Here are some additional details to consider when writing the job description:"

Then, paste the details you gathered previously.

Then press the send button.

ChatGPT wrote some basic details, the overview of the role, and key responsibilities of the role. 

It also included [basic and preferred qualifications], [what's in it for the applicant], and [more instructions].


Make sure to review and revise this job description so it effectively communicates your expectations. 

*LEARNING OBJECTIVE 2*
With this description, we can proceed to extract keywords which potential candidates might use when searching for this job.

Keywords are important because they make your job ad discoverable. The best keywords should resonate with the job seekers' search behavior.

Let's get keywords from ChatGPT. 

Type "Provide keywords related to the role of Digital Marketing Manager based on the description you've provided me."

Then, press the send message button. 

ChatGPT came up with a couple of keywords that we can use when posting our final job ad. 

We can also incorporate these keywords into the job ad itself.

With our description and keywords in hand, let's craft a job ad that integrates them both seamlessly.  

Type:

"Using the job description and the keywords you've provided, draft a job ad for a Digital Marketing Manager."

 Then, press the send button.   

Here's the response. 


ChatGPT drafted a job ad that contains specific details about the job description and incorporates keywords so that it's easier to find on the internet. 

Make sure to review and revise the ad and verify that all information is accurate before posting it online. 

*CONCLUSION*
That's it!

By leveraging the power of ChatGPT-4, HR professionals can create job advertisements that stand out and attract top talent.

Remember, in the digital age of recruitment, your job ad is your first impression. So make it count!"""


# Function to make API call
def api_call(messages, temperature=0.9, model="gpt-4"):
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
            {"role": "user", "content": f"""Create a script for teaching an employee: {EPA_title}
The target audience is: a professional in a {Department} team."""}
        ]
    else:
        # Step 1: User input and first API call ~5secs
        stepOne = [
            {"role": "system", "content": SystemPrompt_10},
            {"role": "user", "content": UserPrompt_10},
            {"role": "assistant", "content": AssistantPrompt_10},
            {"role": "user", "content": f"""Create a script for teaching an employee: {EPA_title}
The target audience is: a professional in a {Department} team. 
Additional instructions: {Extra_input}"""}
        ]
    
    Script_1 = api_call(stepOne, 0.7)
    return Script_1



# Create the Gradio interface 
iface = gr.Interface(
    fn=process_inputs, 
    inputs=[
        gr.Textbox(lines=2, label='EPA title Here... (use the phrasing: "How to do X with ChatGPT")'), 
        gr.Textbox(lines=2, label='Department Here... (eg: Product Management)'), 
        gr.Textbox(lines=2, label='Extra input Here... (optional, put any extra requirements or relevant context)')
        ], 
    outputs=gr.Textbox(label="Script", show_copy_button=True)
)

iface.launch(share=True)
iface.launch()