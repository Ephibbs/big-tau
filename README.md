# τ++-bench: A Benchmark for Tool-Agent-User Interaction in Many Real-World Domains

## Inspired by τ-bench by Sierra Research

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

## Domains

1. **Airline**  
   Manage schedules, handle customer inquiries, oversee logistics, and track service requests.

2. **Retail**  
   Handle stock updates, process orders, assist customer interactions, and manage returns and exchanges.

3. **Healthcare**  
   Coordinate appointments, manage health records, provide information, and assist with insurance processing.

4. **Legal**  
   Support document creation, assist with research, provide review services, and give access to relevant references.

5. **Events**  
   Coordinate attendee management, oversee venue options, plan schedules, and manage event-related communications.

6. **Real Estate**  
   Schedule property tours, provide property details, support documentation, and facilitate communications.

7. **Finance**  
   Conduct financial modeling, analyze market trends, generate performance reports, assess risk factors, and provide data-driven insights to support investment and business decisions.

8. **Fitness**  
   Track activities, suggest routines, provide wellness information, and monitor progress.

9. **Logistics**  
   Track deliveries, optimize routes, update inventory, and log incident reports.

10. **HR**  
    Post opportunities, manage schedules, oversee employee data, and support inquiries.

11. **Insurance**  
    Submit claims, verify policy details, confirm coverage, and track claim statuses.

12. **Space**  
    Track assets, monitor data, forecast conditions, and coordinate schedules.

13. **Pharmaceuticals**  
    Track participants, ensure compliance, coordinate testing, and generate reports.

14. **Manufacturing**  
    Monitor production data, manage operations, assure quality, and report on efficiency.

15. **Cybersecurity**  
    Track security concerns, manage incident responses, conduct assessments, and provide audit reports.

16. **Hospitality**  
    Handle reservations, manage preferences, oversee requests, and follow up on feedback.

17. **Banking**  
    Assist with account inquiries, provide transaction data, manage alerts, and offer guidance.

18. **Engineering**  
    Manage code repositories, review and merge pull requests, track project issues, automate testing, and document technical processes, write unit tests, install dependencies, code across files.

19. **Loans**  
    Process applications, verify criteria, answer inquiries, and manage payments.

20. **Construction**  
    Track project timelines, verify credentials, assist with permits, and manage communications.

21. **Agriculture**  
    Track performance, monitor conditions, manage resources, and assist with analytics.

22. **Advertising**  
    Track performance, conduct tests, analyze metrics, and adjust targeting.

23. **Sales**  
    Track engagement, provide follow-ups, update records, and monitor progress.

24. **Education**  
    Track progress, manage materials, coordinate sessions, and provide learning support.

25. **Accounting**
    Manage financial records, reconcile accounts, prepare financial statements, handle budgeting, process invoices, and ensure compliance with tax regulations.

26. **Data Science**
    Perform data cleaning and preprocessing, run statistical analyses, create visualizations, develop predictive models, and generate insights for decision-making.
    
28. **Web Automation**
    Automate repetitive web tasks, extract data from websites, fill out and submit online forms, manage web scraping, schedule automated workflows, and monitor web activities for changes or updates.


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

## License

See `./LICENSE`.
