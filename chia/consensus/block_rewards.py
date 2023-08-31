from __future__ import annotations

from chia.util.ints import uint32, uint64
from chia.types.blockchain_format.execution_payload import WithdrawalV1
from chia.consensus.block_record import BlockRecord
from chia.consensus.blockchain_interface import BlockchainInterface
from chia.consensus.constants import ConsensusConstants

# 1 Cryptomines coin = 1,000,000,000,000 = 1 trillion mojo.
_mojo_per_chia = 1000000000000
_bpx_to_gwei = 1000000000
_blocks_per_year = 1681920  # 32 * 6 * 24 * 365


def calculate_pool_reward(height: uint32) -> uint64:
    """
    Returns the pool reward at a certain block height. The pool earns 7/8 of the reward in each block. If the farmer
    is solo farming, they act as the pool, and therefore earn the entire block reward.
    These halving events will not be hit at the exact times
    (3 years, etc), due to fluctuations in difficulty. They will likely come early, if the network space and VDF
    rates increase continuously.
    """

    if height == 0:
        return uint64(int((7 / 8) * 2500000 * _mojo_per_chia))
    elif height < 2 * _blocks_per_year:
        return uint64(int((7 / 8) * 1 * _mojo_per_chia))
    elif height < 5 * _blocks_per_year:
        return uint64(int((7 / 8) * 0.5 * _mojo_per_chia))
    elif height < 8 * _blocks_per_year:
        return uint64(int((7 / 8) * 0.25 * _mojo_per_chia))
    elif height < 11 * _blocks_per_year:
        return uint64(int((7 / 8) * 0.125 * _mojo_per_chia))
    else:
        return uint64(int((7 / 8) * 0.0625 * _mojo_per_chia))


def calculate_base_farmer_reward(height: uint32) -> uint64:
    """
    Returns the base farmer reward at a certain block height.
    The base fee reward is 1/8 of total block reward

    Returns the coinbase reward at a certain block height. These halving events will not be hit at the exact times
    (3 years, etc), due to fluctuations in difficulty. They will likely come early, if the network space and VDF
    rates increase continuously.
    """
    if height == 0:
        return uint64(int((1 / 8) * 2500000 * _mojo_per_chia))
    elif height < 2 * _blocks_per_year:
        return uint64(int((1 / 8) * 1 * _mojo_per_chia))
    elif height < 5 * _blocks_per_year:
        return uint64(int((1 / 8) * 0.5 * _mojo_per_chia))
    elif height < 8 * _blocks_per_year:
        return uint64(int((1 / 8) * 0.25 * _mojo_per_chia))
    elif height < 11 * _blocks_per_year:
        return uint64(int((1 / 8) * 0.125 * _mojo_per_chia))
    else:
        return uint64(int((1 / 8) * 0.0625 * _mojo_per_chia))


def create_withdrawals(
    constants: ConsensusConstants,
    prev_tx_block: BlockRecord,
    blocks: BlockchainInterface,
) -> List[WithdrawalV1]:
    withdrawals: List[WithdrawalV1] = []
    
    next_wd_index: uint64
    if prev_tx_block.last_withdrawal_index is None:
        next_wd_index = 0
    else:
        next_wd_index = prev_tx_block.last_withdrawal_index + 1
    
    # Add block rewards
    curr: BlockRecord = prev_tx_block
    while True:
        withdrawals.append(
            WithdrawalV1(
                next_wd_index,
                uint64(1),
                curr.coinbase,
                _calculate_v3_reward(curr.height + 1),
            )
        )
        next_wd_index += 1
        
        if curr.prev_hash == constants.GENESIS_CHALLENGE:
            break
        curr = blocks.block_record(curr.prev_hash)
        if curr.is_transaction_block:
            break
    
    return withdrawals

def _calculate_v3_reward(
    v3_height: uint64 
) -> uint64:
    if v3_height < 2 * _blocks_per_year:
        return uint64(1 * _mojo_per_chia)
    elif v3_height < 5 * _blocks_per_year:
        return uint64(0.5 * _mojo_per_chia)
    elif v3_height < 8 * _blocks_per_year:
        return uint64(0.25 * _mojo_per_chia)
    elif v3_height < 11 * _blocks_per_year:
        return uint64(0.125 * _mojo_per_chia)
    else:
        return uint64(0.0625 * _mojo_per_chia)
