
# τaurus Commands

Run models:

Llama-3.3-70B-Instruct:
```
python run.py --agent-strategy tool-calling --env retail --model deepinfra/meta-llama/Llama-3.3-70B-Instruct --model-provider deepinfra --user-model deepinfra/meta-llama/Llama-3.3-70B-Instruct --user-model-provider deepinfra --user-strategy llm --max-concurrency 1
```

GPT-4o:
```
python run.py --agent-strategy tool-calling --env retail --model gpt-4o --model-provider openai --user-model gpt-4o --user-model-provider openai --user-strategy llm --max-concurrency 1
```

Llama-3.1-8B-Instruct:
```
python run.py --agent-strategy tool-calling --env retail --model deepinfra/meta-llama/Meta-Llama-3.1-8B-Instruct --model-provider together_ai --user-model deepinfra/meta-llama/Meta-Llama-3.1-8B-Instruct --user-model-provider together_ai --user-strategy llm --max-concurrency 20
```

Team-ACE/ToolACE-8B:
```
python run.py --agent-strategy tool-calling --env retail --model Team-ACE/ToolACE-8B --model-provider together_ai --user-model Team-ACE/ToolACE-8B --user-model-provider together_ai --user-strategy llm --max-concurrency 1
```

RunPod:
```
python run.py --agent-strategy tool-calling --env retail --model runpod/fs6nm1iy1wadmu/sk-IrR7Bwxtin0haWagUnPrBgq5PurnUz86/Team-ACE/ToolACE-8B --user-model openai/gpt-4o --user-model-provider together_ai --user-strategy llm --max-concurrency 1
```

## RunPod VLLM *Pod* Settings for Llama 3.1

Add the following to the end of your RunPod Pod's command:
```
 --enable-auto-tool-choice --tool-call-parser llama3_json --chat-template examples/tool_chat_template_llama3.1_json.jinja
```

## RunPod VLLM *Serverless* Settings

Can't figure it out.


## Historical trajectories

τ-bench might be expensive to run. We have provided a set of historical trajectories for the airline and retail environments in `./historical_trajectories`.

If you would like to contribute your historical trajectories to this benchmark, please submit a PR!

### Tool-ACE Trajectory Example
Running task 0
User: {'role': 'user', 'content': "Hi there! I recently received an order and I'd like to exchange a couple of items from it."}

Assistant: {'content': None, 'refusal': None, 'role': 'assistant', 'audio': None, 'function_call': None, 'tool_calls': [{'id': 'chatcmpl-tool-6424f758e9474fd49fd48e1a789cf629', 'function': {'arguments': '{"order_id": "#W0000000"}', 'name': 'get_order_details'}, 'type': 'function'}]}

User: {'role': 'tool', 'tool_call_id': 'chatcmpl-tool-6424f758e9474fd49fd48e1a789cf629', 'name': 'get_order_details', 'content': 'Error: order not found'}

Assistant: {'content': 'The order with the given order id (#W0000000r) was not found. Please provide the correct order id to proceed with the exchange.', 'refusal': None, 'role': 'assistant', 'audio': None, 'function_call': None, 'tool_calls': []}

User: {'role': 'user', 'content': "I don't have the order ID handy right now, but I can describe the items I'd like to exchange if that helps."}

Assistant: {'content': None, 'refusal': None, 'role': 'assistant', 'audio': None, 'function_call': None, 'tool_calls': [{'id': 'chatcmpl-tool-0c6210bb51e84f90926e2ac106bf082a', 'function': {'arguments': '{"order_id": "#W0000000"}', 'name': 'get_order_details'}, 'type': 'function'}]}

User: {'role': 'tool', 'tool_call_id': 'chatcmpl-tool-0c6210bb51e84f90926e2ac106bf082a', 'name': 'get_order_details', 'content': 'Error: order not found'}

Assistant: {'content': None, 'refusal': None, 'role': 'assistant', 'audio': None, 'function_call': None, 'tool_calls': [{'id': 'chatcmpl-tool-2884461e64434429a24c89abdda7b981', 'function': {'arguments': '{"first_name": "John", "last_name": "Doe", "zip": "12345"}', 'name': 'find_user_id_by_name_zip'}, 'type': 'function'}]}

User: {'role': 'tool', 'tool_call_id': 'chatcmpl-tool-2884461e64434429a24c89abdda7b981', 'name': 'find_user_id_by_name_zip', 'content': 'Error: user not found'}

Assistant: {'content': '[find_user_id_by_email(email=johndoe@example.comr)]', 'refusal': None, 'role': 'assistant', 'audio': None, 'function_call': None, 'tool_calls': []}

User: {'role': 'user', 'content': "I apologize, but I don't think my email is set up with your system. Can we proceed with the exchange details instead?"}

Assistant: {'content': '[find_user_id_by_name_zip(first_name=Johnr, last_name=Doer, zip=12345r)]', 'refusal': None, 'role': 'assistant', 'audio': None, 'function_call': None, 'tool_calls': []}

User: {'role': 'user', 'content': "It looks like there might be a mix-up with the name. I'm Yusuf Rossi, and my ZIP code is 19122."}

Assistant: {'content': '[find_user_id_by_name_zip(first_name=Yusufr, last_name=Rossir, zip=19122r)]', 'refusal': None, 'role': 'assistant', 'audio': None, 'function_call': None, 'tool_calls': []}