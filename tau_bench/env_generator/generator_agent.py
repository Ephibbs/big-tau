import os
import json
import yaml
import random
from faker import Faker
import openai
from typing import List, Dict, Any
import click
from pathlib import Path
import dotenv
dotenv.load_dotenv('../../.env')

fake = Faker()

envs_dir = "../envs"

# Helper to generate data via OpenAI
def generate_openai_completion(prompt, model="o1-mini", max_tokens=None, temperature=0.7):
    response = openai.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_completion_tokens=max_tokens,
        temperature=temperature
    )
    return response.choices[0].message.content.strip()

def generate_openai_object(prompt, schema, model="o1-mini", max_tokens=None, temperature=0.7):
    response = openai.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_schema", "json_schema": schema},
        max_completion_tokens=max_tokens,
        temperature=temperature
    )
    return json.loads(response.choices[0].message.content.strip())


# 1. Generate System Prompt (Agent Responsibilities and Policies)
def create_system_prompt(description: str, env_dir: str, model: str = "o1-mini") -> str:
    prompt = generate_openai_object(
        f"Write a detailed, formatted markdown document for an agent's responsibilities and policies in an environment fitting the following description:\n\n{description}\n\nInclude examples and guidelines. In addition, include a list of variables that should be supplied to the agent and will be appended to the agent's prompt(e.g. 'datetime', 'user_id', etc.). Only include variables that are necessary to support the task categories and system prompt. Only write what a text-based agent with function-calling capabilities could do, not what a human could do. Do not include function descriptions, just the general guidelines and responsibilities. Do not include a table of contents.",
        {
            "name": "wiki",
            "schema": {
                "type": "object",
                "properties": {
                    "content": {"type": "string"},
                    "variables": {
                        "type": "array",
                        "description": "A list of variables that should be supplied to the agent and will be appended to the agent's prompt.",
                        "items": {
                            "type": "string", "description": "The name of the variable."
                        },
                    }
                }
            },
            "required": ["content"]
        },
        model=model
    )
    with open(f"{env_dir}/wiki.md", "w") as file:
        file.write(prompt["content"])
    return prompt

# 2. Generate Task Categories
def create_task_categories(env_dir: str, num_categories: int = 50, model: str = "o1-mini") -> List[str]:
    system_prompt = open(f"{env_dir}/wiki.md", "r").read()
    task_prompt = f"List {num_categories} diverse task categories for the following agent, ensuring they are specific and relevant to the following system prompt:\n\n```\n{system_prompt}\n```\n\nCategories should be specific, start with a verb (such as 'schedule', 'update', 'verify', 'issue', 'escalate', 'get', 'delete', etc.), and be no more than 10 words."
    categories = generate_openai_object(task_prompt, {
            "name": "task_categories",
            "schema": {
                "type": "object",
                "properties": {
                    "categories": {
                    "type": "array",
                        "items": {"type": "string"},
                        "minItems": num_categories,
                        "maxItems": num_categories,
                        "uniqueItems": True
                    }
                },
                "required": ["categories"]
            }
        },
        model=model)
    with open(f"{env_dir}/task_categories.json", "w") as file:
        json.dump(categories['categories'], file, indent=4)
    return categories

# 4. Generate Functions and Schemas for Tasks
def create_functions(env_dir: str, model: str = "o1-mini") -> List[Dict[str, Any]]:
    task_categories = json.load(open(f"{env_dir}/task_categories.json", "r"))
    system_prompt = open(f"{env_dir}/wiki.md", "r").read()
    # Create a single prompt requesting all function schemas at once
    schema_prompt = f"""Based on the following system prompt and task categories, create a comprehensive list of function schemas that would be needed to handle all possible tasks. Each function schema should include:

1. A descriptive name
2. A detailed description of what the function does
3. Required input parameters with types and descriptions
4. Expected output format and description
5. Any constraints or validation rules

Think of CRUD operations, and other common operations that would be needed to handle the task categories. Try to reuse functions for similar tasks.

System prompt:
{system_prompt}

Task categories:
{"\n".join([f"- {category}" for category in task_categories])}

Return a list of complete function schemas in JSON Schema format."""

    # Get all function schemas in one call
    functions = generate_openai_object(schema_prompt, {
            "name": "function_schemas",
            "schema": {
                "type": "object",
                "properties": {
                    "functions": {
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
                    },
                },
                "required": ["functions"]
            }
        },
        model=model)

    with open(f"{env_dir}/functions_schemas.json", "w") as file:
        json.dump(functions['functions'], file, indent=4)
    return functions

# 3. Generate Function Response Schemas
def create_function_response_schemas(env_dir: str, model: str = "o1-mini") -> Dict[str, Any]:
    functions = json.load(open(f"{env_dir}/functions_schemas.json", "r"))
    system_prompt = open(f"{env_dir}/wiki.md", "r").read()
    db_prompt = "Design response schemas for a system supporting the following functions to call: " + ", ".join(functions) + " as well as the following system prompt: " + system_prompt + ". Provide schemas in JSON format. Create a schema for each function."
    db_schemas = generate_openai_object(db_prompt, {
        "name": "function_response_schemas",
        "schema": {
            "type": "object",
            "properties": {
                "tables": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "table_name": {"type": "string"},
                            "schema": {"type": "object"}
                        },
                        "required": ["table_name", "schema"]
                    }
                }
            },
            "required": ["tables"]
        }
    }, model=model)
    with open(f"{env_dir}/database_schemas.json", "w") as file:
        json.dump(db_schemas, file, indent=4)
    return db_schemas

# 5. Generate Edge Cases for Tasks
def create_edge_cases(env_dir: str, model: str = "o1-mini", num_edge_cases: int = 12) -> Dict[str, List[Dict[str, Any]]]:
    task_categories = json.load(open(f"{env_dir}/task_categories.json", "r"))
    edge_cases = {}
    for category in task_categories:
        cases = []
        # Generate a mix of normal and edge cases
        edge_prompt = f"""Generate {num_edge_cases} test cases for the task category '{category}'. 
        Include a mix of:
        - Normal cases (everything works as expected)
        - Edge cases (unusual but valid situations)
        - Error cases (invalid or problematic situations)
        
        For example, if the category is 'register_new_patient', cases could include:
        - Normal: Patient with valid insurance and complete information
        - Edge: Patient with no insurance
        - Edge: Patient who is reluctant to provide information and must be asked multiple times
        - Error: Patient with missing required documentation
        
        For each case, provide a description of the case.
        
        Format as JSON."""
        
        cases_response = json.loads(generate_openai_completion(edge_prompt, max_tokens=800, model=model))
        cases.extend(cases_response)
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

@click.group()
def cli():
    """Generate test environments for tau_bench."""
    pass

@cli.command()
@click.argument('name')
@click.option('--description', '-d', prompt=True, help='Description of the environment')
@click.option('--num-tasks', '-t', default=500, show_default=True, 
              help='Number of tasks to generate')
@click.option('--num-categories', '-c', default=50, show_default=True,
              help='Number of task categories to generate')
@click.option('--output-dir', '-o', default=envs_dir, show_default=True,
              help='Base directory for environments')
@click.option('--stop-after', '-s', type=int, 
              help='Stop after specified step (1-6). Steps:\n1: System Prompt\n2: Task Categories\n3: Database Schemas\n4: Functions\n5: Edge Cases\n6: Users and Tasks')
@click.option('--only-step', '-os', type=int,
              help='Only generate the specified step (1-6).')
@click.option('--model', '-m', default="gpt-4o", show_default=True,
              help='OpenAI model to use for generation')
@click.option('--test-suite-params', '-ts',
              help='YAML file containing test suite parameters')
def create(name: str, description: str, num_tasks: int, num_categories: int, output_dir: str, stop_after: int, only_step: int, model: str, test_suite_params: str):
    """Create a new environment with the specified configuration."""
    if test_suite_params:
        test_suite_params = yaml.safe_load(open(test_suite_params, "r"))
        name = test_suite_params["name"]
        description = test_suite_params["description"]
        num_tasks = test_suite_params["num_tasks"]
        num_categories = test_suite_params["num_categories"]
        output_dir = test_suite_params["output_dir"]
        stop_after = test_suite_params["stop_after"]
        only_step = test_suite_params["only_step"]
        model = test_suite_params["model"]
        test_suite_params = test_suite_params["test_suite_params"]
    if stop_after and not 1 <= stop_after <= 6:
        click.echo(click.style(f"Error: --stop-after must be between 1 and 6", fg='red'))
        return

    env_dir = Path(output_dir) / name
    
    click.echo(f"Creating environment '{name}' using model '{model}'...")
    
    # Create environment directory
    env_dir.mkdir(parents=True, exist_ok=True)
    generate_environment_wiki(env_dir)
    click.echo(f"✓ Environment Wiki saved to {env_dir}/wiki.py")

    steps = [
        ('System Prompt', lambda: create_system_prompt(description, env_dir, model=model)),
        ('Task Categories', lambda: create_task_categories(env_dir, num_categories, model=model)),
        ('Functions', lambda: create_functions(env_dir, model=model)),
        ('Database Schemas', lambda: create_function_response_schemas(env_dir, model=model)),
        ('Edge Cases', lambda: create_edge_cases(env_dir, model=model)),
        ('Users and Tasks', lambda: create_users_and_tasks(env_dir, num_tasks))
    ]
    
    if only_step:
        steps = [steps[only_step - 1]]

    with click.progressbar(length=len(steps), label='Generating environment components') as bar:
        for i, (step_name, step_func) in enumerate(steps, 1):
            click.echo(f"\nExecuting Step {i}: {step_name}")
            step_func()
                
            bar.update(1)
            
            if stop_after and i >= stop_after:
                click.echo(click.style(f"\n✓ Stopped after step {i} as requested", fg='yellow'))
                break

    click.echo(click.style("\n✓ Environment created successfully!", fg='green'))
    click.echo(f"\nGenerated files in {env_dir}:")
    for file in env_dir.glob('*'):
        click.echo(f"  - {file.name}")

@cli.command()
@click.argument('name')
@click.option('--output-dir', '-o', default=envs_dir, show_default=True,
              help='Base directory for environments')
def delete(name: str, output_dir: str):
    """Delete an existing environment."""
    env_dir = Path(output_dir) / name
    if not env_dir.exists():
        click.echo(click.style(f"Error: Environment '{name}' not found", fg='red'))
        return
    
    if click.confirm(f"Are you sure you want to delete environment '{name}'?"):
        import shutil
        shutil.rmtree(env_dir)
        click.echo(click.style(f"✓ Environment '{name}' deleted", fg='green'))

@cli.command()
@click.option('--output-dir', '-o', default=envs_dir, show_default=True,
              help='Base directory for environments')
def list(output_dir: str):
    """List all existing environments."""
    env_path = Path(output_dir)
    environments = [d.name for d in env_path.iterdir() if d.is_dir()]
    
    if not environments:
        click.echo("No environments found.")
        return
        
    click.echo("Available environments:")
    for env in environments:
        click.echo(f"  - {env}")

if __name__ == '__main__':
    cli()
