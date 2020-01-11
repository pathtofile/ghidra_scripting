# Count EntryPoints
# @author path/to/file
# @category Entrypoint
import json
# Import stubs so VSCode can do completion
# Get Stubs from: https://github.com/VDOO-Connected-Trust/ghidra-pyi-generator
try:
    import ghidra
    from ghidra_builtins import *
except:
    pass

# Pylint can't handle dynamic updated of globals, so for this script we'll just
# disable it for this script. We're running Jython, i.e. Python 2.7 anyway, so
# what's one more gross thing...
# pylint: disable=all
DUMMY_MONITOR = ghidra.util.task.DummyCancellableTaskMonitor()
RESULT = {
    "total_addresses": 0,
    "total_addresses_unique": 0,
    "total_functions": 1  # Entrypoint
}
UNIQ_FUNCS = list()

def check_func(level, func):
    global RESULT, UNIQ_FUNCS
    # Add to count of functions
    RESULT["total_functions"] += 1

    # Add length to running totals
    func_len = func.body.numAddresses
    if func not in UNIQ_FUNCS:
        UNIQ_FUNCS.append(func)
        RESULT["total_addresses_unique"] += func_len
    RESULT["total_addresses"] += func_len

    called_funcs = func.getCalledFunctions(DUMMY_MONITOR)
    for called_func in called_funcs:
        try:
            check_func(level+1, called_func)
        except RuntimeError:
            print("maximum recursion depth exceeded maybe?")
            return
def main():
    entry_symbol = getSymbol("entry", None)
    entry_func = getFunctionAt(entry_symbol.getAddress())
    if entry_func is None:
        print("failed to find entry...")
        return
    check_func(0, entry_func)
    print(json.dumps(RESULT, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
