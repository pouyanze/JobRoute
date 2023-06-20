from django.shortcuts import render
from dotenv import load_dotenv
import os
import openai
import json

def job_transfer_view(request):
    if request.method == 'POST':

        user_job_title = request.POST.get('job_title')
        # Load environment variables from .env file
        load_dotenv()
        # Access the OpenAI API key from environment variable
        openai.api_key = os.getenv('OPENAI_API_KEY')

        # Call the Government of Canada's NOC API to retrieve the job data in JSON format
        prompt = f'Please provide a JSON format output based on the NOC code resulting from the user\'s job title input. The output should include the original job title, and a node called "similar_jobs" with sub-nodes containing "job_title", "noc_code", and "percent_similarity" for each of the 5 similar jobs. User job title: {user_job_title}'
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0,
            max_tokens=1284,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        # Extract the JSON content from the OpenAI API response
        response_text = response.choices[0].text.strip()
        response_json = json.loads(response_text)

        # Create the response JSON object
        response = {
            "original_job_title": user_job_title,
            "similar_jobs": response_json["similar_jobs"]
        }


        print(response)
        response_string = json.dumps(response, indent=4)
        print(response_string)

        return render(request, 'job_transfer.html', {'response': response})


    # If the request method is GET or the form has not been submitted yet
    return render(request, 'job_transfer.html')


def education_requirements_view(request):
    if request.method == 'POST':
        selected_job = request.POST.get('selected_job')
        job_title, noc_code = selected_job.split("|")
        
        # Load environment variables from .env file
        load_dotenv()
        # Access the OpenAI API key from environment variable
        openai.api_key = os.getenv('OPENAI_API_KEY')

        # Create a prompt for retrieving education requirements based on the selected NOC code and job title
        prompt = f'I am doing research on education requirements for jobs in Canada. My primary reference is the National Occupation Classification (NOC) developed by the Government of Canada. Based on NOC code{noc_code} and its job title {job_title}, I want you to provide a list of any degrees, diplomas, certificates, or designations required by the job.\n\nPlease provide a response in JSON format only for the given NOC code. Include a node called "education_requirements" with sub-nodes containing "type" (degree, diploma, certificate, designation), "institution" (name of the institution or establishment or whatever it is that is offering this programm), "description" (please specify the exact course or program name if possible), "length" (specify the length and the unit, e.g., 2 years, 4 years, 6 months, 2 weeks, etc.), and "link" (Please provide the link to the official homepage or index page of the institution, establishment, or program you are referring to. In case the page is not found (404 error), kindly provide the homepage address without any additional forward slashes, for instance i dont want https://www.utoronto.ca/computer-science i just need https://www.utoronto.ca/)'

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        # Extract the JSON content from the OpenAI API response
        response_text = response.choices[0].text.strip()
        response_json = json.loads(response_text)

        # Create the response JSON object
        response = {
            "selected_job": job_title,
            "education_requirements": response_json["education_requirements"]
        }

        print(response)
        response_string = json.dumps(response, indent=4)
        print(response_string)
        
        return render(request, 'education_requirements.html', {'response': response})

    elif request.method == 'GET':
        return render(request, 'job_transfer.html')