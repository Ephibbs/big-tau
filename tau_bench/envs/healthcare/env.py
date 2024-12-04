# Copyright Sierra

from tau_bench.envs.healthcare.data import load_data
from tau_bench.envs.healthcare.rules import RULES
from tau_bench.envs.healthcare.tools import ALL_TOOLS
from tau_bench.envs.healthcare.wiki import WIKI
from tau_bench.envs.base import Env
from typing import Optional, Union
from tau_bench.envs.user import UserStrategy


class MockHealthcareDomainEnv(Env):
    def __init__(
        self,
        user_strategy: Union[str, UserStrategy] = UserStrategy.LLM,
        user_model: str = "gpt-4o",
        user_provider: Optional[str] = None,
        task_split: str = "test",
        task_index: Optional[int] = None,
    ):
        match task_split:
            case "test":
                from tau_bench.envs.healthcare.tasks_test import TASKS as tasks
            case _:
                raise ValueError(f"Unknown task split: {task_split}")
        super().__init__(
            data_load_func=load_data,
            tools=ALL_TOOLS,
            tasks=tasks,
            wiki=WIKI,
            rules=RULES,
            user_strategy=user_strategy,
            user_model=user_model,
            user_provider=user_provider,
            task_index=task_index,
        )
        self.terminate_tools = ["transfer_to_human_agents"]
