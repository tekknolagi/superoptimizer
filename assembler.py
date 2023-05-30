import re
from cpu import CPU

# Turns a string into a program.
def parse(assembly):
    lines = assembly.split('\n')
    program = []
    for line in lines:
        match = re.match(r'(\w+)\s+([-\d]+)(?:,\s*([-\d]+)(?:,\s*([-\d]+))?)?', line)
        if match:
            op_str, *args_str = match.groups()
            op = CPU.ops[op_str]
            args = [int(arg) for arg in args_str if arg is not None]
            program.append((op, args))
    return program

# Turns a program into a string.
def output(program):
    if len(program) == 0: return "\n"
    assembly = ""
    for instruction in program:
        op = instruction[0]
        args = instruction[1]
        if op.__name__ == CPU.load.__name__:
            assembly += f"LOAD {args[0]}\n"
        elif op.__name__ == CPU.swap.__name__:
            assembly += f"SWAP {args[0]}, {args[1]}\n"
        elif op.__name__ == CPU.xor.__name__:
            assembly += f"XOR {args[0]}, {args[1]}\n"
        elif op.__name__ == CPU.inc.__name__:
            assembly += f"INC {args[0]}\n"
    return assembly