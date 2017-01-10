import random

from flaky import flaky

from web3.utils.encoding import decode_hex
from web3.utils import async


@flaky(max_runs=3)
def test_miner_setExtra(web3_empty, wait_for_block):
    web3 = web3_empty

    initial_extra = decode_hex(web3.eth.getBlock(web3.eth.blockNumber)['extraData'])

    new_extra_data = b'-this-is-32-bytes-of-extra-data-'

    # sanity
    assert initial_extra != new_extra_data

    web3.miner.setExtra(new_extra_data)

    with async.Timeout(60) as timeout:
        while True:
            extra_data = decode_hex(web3.eth.getBlock(web3.eth.blockNumber)['extraData'])
            if extra_data == new_extra_data:
                break
            async.sleep(random.random())
            timeout.check()

    after_extra = decode_hex(web3.eth.getBlock(web3.eth.blockNumber)['extraData'])

    assert after_extra == new_extra_data
