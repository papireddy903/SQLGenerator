
from google import genai 
import os 
import json 
from google.genai import types 
from django.conf import settings 

def load_json_file(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

def get_sql_query_from_nl(user_input):
    """
    Given a natural language query, returns the generated SQL query as a string.
    """
    tables_file = os.path.join(settings.BASE_DIR, 'app', 'data', 'temp_tables.json')
    relationships_file = os.path.join(settings.BASE_DIR, 'app', 'data', 'temp_relationships.json')
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY", "AIzaSyDJF9xph8zBm-KHmDNdYw4vfixGzx-D8QA"))
    tables_info = load_json_file(tables_file)
    tables_relationships = load_json_file(relationships_file)

    instructions = (
        "You are the SQL query generator. Below is the metadata provided as two JSON files:\n"
        f"{json.dumps(tables_relationships)} has Tables and Join Conditions. Only use the Type of Join mentioned in the 'Type of Join' column.\n"
        f"{json.dumps(tables_info)} has Table name, Column Details and the Column Prefix you need to use.\n"
        "Only use columns mentioned in the column details. Do not assume anything.\n"
        "Generate a SQL Query based on the user question."
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            config=types.GenerateContentConfig(
                system_instruction=instructions
            ),
            contents=user_input,
        )
        return response.text.strip()
    except Exception as e:
        raise RuntimeError(f"Error generating SQL Query: {e}")

