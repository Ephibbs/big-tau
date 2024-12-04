import os
import json
import random
from faker import Faker
import openai
from typing import List, Dict, Any

fake = Faker()

# Replace with your OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

envs_dir = "tau_bench/envs"

# Helper to generate data via OpenAI
def generate_openai_completion(prompt, model="o1-mini", max_tokens=None, temperature=0.7):
    response = openai.Completion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=temperature
    )
    return response["choices"][0]["text"].strip()

def generate_openai_object(prompt, schema, model="o1-mini", max_tokens=None, temperature=0.7):
    response = openai.Completion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_schema", "schema": schema, "name": "response"},
        max_tokens=max_tokens,
        temperature=temperature
    )
    return json.loads(response["choices"][0]["message"]["content"].strip())

# 1. Generate System Prompt (Agent Responsibilities and Policies)
def create_system_prompt(description: str, env_dir: str) -> str:
    prompt = generate_openai_completion(
        f"Write a detailed, formatted markdown document for an agent's responsibilities and policies in an environment fitting the following description:\n\n{description}\n\nInclude examples and guidelines."
    )
    with open(f"{envs_dir}/wiki.md", "w") as file:
        file.write(prompt)
    return prompt

# 2. Generate Task Categories
def create_task_categories(system_prompt: str, env_dir: str, num_categories: int = 50) -> List[str]:
    task_prompt = f"List {num_categories} diverse task categories for the following agent, ensuring they are specific and actionable:\n\n```\n{system_prompt}\n```"
    categories = generate_openai_object(task_prompt, {
        "type": "array",
        "items": {"type": "string"},
        "additionalProperties": False
    })
    with open(f"{env_dir}/task_categories.json", "w") as file:
        json.dump(categories, file, indent=4)
    return categories

# 3. Generate Functions and Schemas for Tasks
def create_functions(system_prompt: str, task_categories: List[str], env_dir: str) -> List[Dict[str, Any]]:
    # Create a single prompt requesting all function schemas at once
    schema_prompt = f"""Based on the following system prompt and task categories, create a comprehensive list of function schemas that would be needed to handle all possible tasks. Each function schema should include:

1. A descriptive name
2. A detailed description of what the function does
3. Required input parameters with types and descriptions
4. Expected output format and description
5. Any constraints or validation rules

System prompt:
{system_prompt}

Task categories:
{"\n".join([f"- {category}" for category in task_categories])}

Return a list of complete function schemas in JSON Schema format."""

    # Get all function schemas in one call
    functions = generate_openai_object(schema_prompt, {
        "type": "array",
        "items": {
            "type": "object",
            "required": ["name", "description", "parameters"],
            "properties": {
                "name": {"type": "string"},
                "description": {"type": "string"},
                "parameters": {"type": "object"}
            }
        }
    })

    with open(f"{env_dir}/functions_schemas.json", "w") as file:
        json.dump(functions, file, indent=4)
    return functions

# 4. Generate Database Schemas
def create_mock_databases(env_dir: str) -> Dict[str, Any]:
    db_prompt = "Design database schemas for a system supporting 50 diverse task categories. Include tables for users, tasks, logs, and other necessary entities. Provide schemas in JSON format."
    db_schemas = generate_openai_object(db_prompt, {
        "type": "object",
        "properties": {}
    })
    with open(f"{env_dir}/database_schemas.json", "w") as file:
        json.dump(db_schemas, file, indent=4)
    return db_schemas

# 5. Generate Edge Cases for Tasks
def create_edge_cases(task_categories: List[str], env_dir: str) -> Dict[str, List[Dict[str, Any]]]:
    edge_cases = {}
    for category in task_categories:
        cases = []
        for i in range(12):
            edge_prompt = f"Create a detailed edge case for task category '{category}', case #{i+1}. Include input data, expected output, and a description of why this is an edge case."
            case = json.loads(generate_openai_completion(edge_prompt, max_tokens=200))
            cases.append(case)
        edge_cases[category] = cases
    with open(f"{env_dir}/edge_cases.json", "w") as file:
        json.dump(edge_cases, file, indent=4)
    return edge_cases

# 6. Generate Users and Related Database Entries
def create_users_and_tasks(task_categories: List[str], env_dir: str, num_tasks: int = 500) -> None:
    users = {}
    tasks = []
    for _ in range(num_tasks):  # Create 500 users
        user_id = fake.uuid4()
        user = {
            "id": user_id,
            "name": {"first_name": fake.first_name(), "last_name": fake.last_name()},
            "address": {
                "address1": fake.street_address(),
                "address2": fake.secondary_address(),
                "city": fake.city(),
                "country": fake.country(),
                "province": fake.state_abbr(),
                "zip": fake.zipcode()
            },
            "email": fake.email(),
            "dob": fake.date_of_birth().isoformat(),
            "payment_methods": {
                f"credit_card_{random.randint(1000000, 9999999)}": {
                    "source": "credit_card",
                    "brand": random.choice(["visa", "mastercard", "amex"]),
                    "last_four": str(random.randint(1000, 9999)),
                    "id": f"credit_card_{random.randint(1000000, 9999999)}"
                }
            }
        }
        users[user_id] = user

        # Create associated tasks
        task_id = fake.uuid4()
        task = {
            "id": task_id,
            "user_id": user_id,
            "category": random.choice(task_categories),
            "description": fake.sentence(),
            "status": random.choice(["pending", "completed", "failed"]),
            "created_at": fake.date_time_this_year().isoformat()
        }
        tasks.append(task)

    # Save to JSON files
    with open("users.json", "w") as file:
        json.dump(users, file, indent=4)
    with open("tasks.json", "w") as file:
        json.dump(tasks, file, indent=4)

def generate_environment_wiki(env_dir: str) -> None:
    WIKI = """import os

FOLDER_PATH = os.path.dirname(__file__)

with open(os.path.join(FOLDER_PATH, "wiki.md"), "r") as f:
    WIKI = f.read()
"""
    with open(f"{env_dir}/wiki.py", "w") as file:
        file.write(WIKI)

# Main Execution
if __name__ == "__main__":
    name = input("Enter a name for the environment: ")
    description = input("Enter a description for the environment: ")
    num_tasks = int(input("Enter the number of tasks: "))
    num_categories = int(input("Enter the number of task categories: "))
    env_dir = f"{envs_dir}/{name}"

    # Step 0: Create Environment Directory
    os.makedirs(env_dir, exist_ok=True)
    generate_environment_wiki(env_dir)
    print(f"Environment Wiki saved to {env_dir}/wiki.py")


    # Step 1: System Prompt
    system_prompt = create_system_prompt(description, env_dir)
    print(f"System Prompt saved.")
    
    # Step 2: Task Categories
    categories = create_task_categories(system_prompt, env_dir, num_categories)
    print("Task Categories generated.")

    # Step 3: Database Schemas
    db_schemas = create_mock_databases(env_dir)
    print("Database Schemas generated.")
    
    # Step 4: Functions
    functions = create_functions(system_prompt, categories, env_dir)
    print("Functions generated.")
    
    # Step 5: Edge Cases
    edge_cases = create_edge_cases(categories, env_dir)
    print("Edge Cases generated.")
    
    # Step 5: Users and Tasks
    create_users_and_tasks(categories, env_dir, num_tasks)
    print("Users and Tasks generated.")
