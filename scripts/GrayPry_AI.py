import json
from dotenv import load_dotenv
import os

def convert_to_json(form_data):
    # Convert form data to dictionary
    data_dict = {key: form_data[key] for key in form_data.keys()}

    # Convert the dictionary to JSON
    data_json = json.dumps(data_dict)
    return data_json

import openai

def create_diagnosis_question(vehicle_info):
    question = f"I have a {vehicle_info['year']}  {vehicle_info['make']}  {vehicle_info['model']}"
    
    details = []

    if vehicle_info.get('mileage') and vehicle_info['mileage'].strip():
        details.append(f"with {vehicle_info['mileage']} miles")
    if vehicle_info.get('noise') and vehicle_info['noise'].strip():
        details.append(f"is experiencing {vehicle_info['noise']}")
    if vehicle_info.get('warningLights') and vehicle_info['warningLights'].strip():
        details.append(f"a {vehicle_info['warningLights']} is on")
    if vehicle_info.get('performanceIssues') and vehicle_info['performanceIssues'].strip():
        details.append(f"and there is {vehicle_info['performanceIssues']}")
    if vehicle_info.get('drivingFeel') and vehicle_info['drivingFeel'].strip():
        details.append(f"with {vehicle_info['drivingFeel']}")
    if vehicle_info.get('heatingCooling') and vehicle_info['heatingCooling'].strip():
        details.append(f"The {vehicle_info['heatingCooling']} is also an issue")
    if vehicle_info.get('suspension') and vehicle_info['suspension'].strip():
        details.append(f"and the {vehicle_info['suspension']} is slightly worn")

    question += ", ".join(details)

    return question

# Set your API key
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

ENGINE="text-davinci-003",  # You can use other engines like "text-curie-003"
DEF_PROMPT = """
<QUESTION>

Can you Provide me 3 - 5 common reasons I could be haveing issues?

I'd like this to be in the form of an JSON file

Follow this schema:
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "user_vehicle_info": {
      "type": "object",
      "properties": {
        "year": { "type": "integer" },
        "make": { "type": "string" },
        "model": { "type": "string" },
        "mileage": { "type": "integer" }
      },
      "required": ["year", "make", "model", "mileage"]
    },
    "num_reasons_requested": { "type": "integer" },
    "parts_link": { "type": "string", "format": "uri", "description": "Use rock auto at: https://www.rockauto.com/en/catalog/make,year,model but replace make,year,model with the info in question" },
    "car_manuals_link": { "type": "string", "format": "uri", "description": "Use carmanuals at: https://www.carmanuals.org/?s=year+model but replace year,model with the info in question" },
    "suggested_reasons": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "reason": { "type": "string" },
          "explanation": { "type": "string" },
          "helpful_links": {
            "type": "object",
            "properties": {
              "YouTube_Search": { "type": "string", "format": "uri" },
              "Google_Search": { "type": "string", "format": "uri" }
            },
            "required": ["YouTube_Search", "Google_Search"]
          }
        },
        "required": ["reason", "explanation", "helpful_links"]
      }
    }
  },
  "required": ["user_vehicle_info", "num_reasons_requested", "parts_link", "car_manuals_link", "suggested_reasons"]
}

"""

def get_diagnosis_reasons(question):
    try:
        prompt = DEF_PROMPT.replace("<QUESTION>", question)
        print(prompt)
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1999
        )

        # Accessing the 'text' key properly
        text_response = response['choices'][0]['text']
        print(text_response)
        print()

        # Parsing the text response into a JSON object
        json_response = json.loads(text_response)
        return json_response
    except KeyError:
        print("An error occurred while accessing the response. Please check the response structure.")
        return None
    except json.JSONDecodeError:
        print("An error occurred while parsing the JSON response.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None