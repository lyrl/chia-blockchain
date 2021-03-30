from dataclasses import dataclass
from typing import List, Any, Optional

from src.consensus.condition_costs import ConditionCost
from src.types.blockchain_format.program import SerializedProgram
from src.types.condition_opcodes import ConditionOpcode
from src.types.name_puzzle_condition import NPC
from src.util.ints import uint64, uint16
from src.util.streamable import Streamable, streamable


@dataclass(frozen=True)
@streamable
class NPCResult(Streamable):
    error: Optional[uint16]
    npc_list: List[NPC]
    clvm_cost: uint64  # CLVM cost only, cost of conditions and tx size is not included


def calculate_cost_of_program(
    program: SerializedProgram, npc_result: NPCResult, clvm_cost_ratio_constant: int
) -> uint64:
    """
    This function calculates the total cost of either a block or a spendbundle
    """
    total_clvm_cost = 0
    total_clvm_cost += npc_result.clvm_cost
    npc_list = npc_result.npc_list
    # Add cost of conditions
    npc: NPC
    total_vbyte_cost = 0
    for npc in npc_list:
        for condition, cvp_list in npc.condition_dict.items():
            if condition is ConditionOpcode.AGG_SIG or condition is ConditionOpcode.AGG_SIG_ME:
                total_vbyte_cost += len(cvp_list) * ConditionCost.AGG_SIG.value
            elif condition is ConditionOpcode.CREATE_COIN:
                total_vbyte_cost += len(cvp_list) * ConditionCost.CREATE_COIN.value
            elif condition is ConditionOpcode.ASSERT_SECONDS_NOW_EXCEEDS:
                total_vbyte_cost += len(cvp_list) * ConditionCost.ASSERT_SECONDS_NOW_EXCEEDS.value
            elif condition is ConditionOpcode.ASSERT_HEIGHT_AGE_EXCEEDS:
                total_vbyte_cost += len(cvp_list) * ConditionCost.ASSERT_HEIGHT_AGE_EXCEEDS.value
            elif condition is ConditionOpcode.ASSERT_HEIGHT_NOW_EXCEEDS:
                total_vbyte_cost += len(cvp_list) * ConditionCost.ASSERT_HEIGHT_NOW_EXCEEDS.value
            elif condition is ConditionOpcode.ASSERT_MY_COIN_ID:
                total_vbyte_cost += len(cvp_list) * ConditionCost.ASSERT_MY_COIN_ID.value
            elif condition is ConditionOpcode.RESERVE_FEE:
                total_vbyte_cost += len(cvp_list) * ConditionCost.RESERVE_FEE.value
            elif condition is ConditionOpcode.CREATE_ANNOUNCEMENT:
                total_vbyte_cost += len(cvp_list) * ConditionCost.CREATE_ANNOUNCEMENT.value
            elif condition is ConditionOpcode.ASSERT_ANNOUNCEMENT:
                total_vbyte_cost += len(cvp_list) * ConditionCost.ASSERT_ANNOUNCEMENT.value
            else:
                # We ignore unknown conditions in order to allow for future soft forks
                pass

    # Add raw size of the program
    total_vbyte_cost += len(bytes(program))

    total_clvm_cost += total_vbyte_cost * clvm_cost_ratio_constant

    return uint64(total_clvm_cost)
