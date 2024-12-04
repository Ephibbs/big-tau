# Copyright Sierra

from .calculate import Calculate
from .get_user_details import GetUserDetails
from .think import Think
from .transfer_to_human_agents import TransferToHumanAgents


ALL_TOOLS = [
    Calculate,
    GetUserDetails,
    Think,
    TransferToHumanAgents,
]
