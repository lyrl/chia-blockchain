from enum import Enum


class ConditionCost(Enum):
    # Condition Costs
    AGG_SIG = 1151515  # the cost of one G1 subgroup check + aggregated signature validation
    CREATE_COIN = 1820552
    ASSERT_MY_COIN_ID = 0
    ASSERT_SECONDS_NOW_EXCEEDS = 0
    ASSERT_SECONDS_AGE_EXCEEDS = 0
    ASSERT_HEIGHT_NOW_EXCEEDS = 0
    ASSERT_HEIGHT_AGE_EXCEEDS = 0
    RESERVE_FEE = 0
    CREATE_ANNOUNCEMENT = 0
    ASSERT_ANNOUNCEMENT = 0
