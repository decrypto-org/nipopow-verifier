"""
run with
$ python iszero
evm assembly with
solc --abi --bin --combined-json srcmap-runtime --overwrite --optimize -o . iszero.sol --asms
"""

import sys

sys.path.append("../../tools/interface/")
import contract_interface

sys.path.append("..")
from config import profiler


def deploy(constructor_arguments=[]):
    contract_path = "./iszero.sol"
    interface = contract_interface.ContractInterface(
        contract_path, backend="ganache", constructor_arguments=constructor_arguments
    )
    return interface


def finalize(interface):
    interface.end()


def print_debug_events(contract, receipt):
    try:
        debug_events = contract.events.debug().processReceipt(receipt)
    except Exception as ex:
        debug_events = {}
    if len(debug_events) > 0:
        for e in debug_events:
            log = dict(e)["args"]
            if isinstance(log["value"], bytes):
                value = log["value"].hex()
            else:
                value = log["value"]
            print(log["tag"], "\t", value)
    return debug_events


def call(interface, function_name, function_args=[]):
    """
    Runs a function with function_args
    """

    contract = interface.get_contract()
    from_address = interface.w3.eth.accounts[0]
    function = contract.get_function_by_name(function_name)(*function_args)
    res = function.call({"from": from_address})
    tx_hash = function.transact({"from": from_address})
    receipt = interface.w3.eth.waitForTransactionReceipt(tx_hash)
    interface.run_gas_profiler(profiler, tx_hash, function_name)
    print_debug_events(contract, receipt)
    return {"result": res, "gas": receipt["gasUsed"]}


interface = deploy()

result = call(interface, "compWithB0", function_args=[10])
print(result['gas'], result['result'])

result = call(interface, "compWithB1", function_args=[10])
print(result['gas'], result['result'])

result = call(interface, "compWith0", function_args=[10])
print(result['gas'], result['result'])

result = call(interface, "compWith1", function_args=[10])
print(result['gas'], result['result'])

finalize(interface)
