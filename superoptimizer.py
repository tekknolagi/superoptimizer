from itertools import product
from cpu import CPU
import assembler

# Helper function that finds the optimal code given the assembly code.
def optimal_from_code(assembly, max_length, max_mem, max_val, debug=False):
    cpu = CPU(max_mem)
    program = assembler.parse(assembly)
    state = cpu.execute(program)
    print(f"***Source***{assembly}")
    optimal_from_state(state, max_length, max_val, debug)

# Helper function that finds the optimal code given the goal state.
def optimal_from_state(state, max_length, max_val, debug=False):
    max_mem = len(state)
    print(f"***State***\n{state}\n") 
    opt = Superoptimizer()
    shortest_program = opt.search(max_length, max_mem, max_val, state, debug) 
    disassembly = assembler.output(shortest_program)
    print(f"***Optimal***\n{disassembly}\n{'='*20}\n")

class Superoptimizer:
    def __init__(self):
        self.program_cache = {}

    # Generates all possible programs.
    def generate_programs(self, max_length, max_mem, max_val):
        load = CPU.load
        swap = CPU.swap
        xor = CPU.xor
        inc = CPU.inc
        ops_values = CPU.ops.values()
        load_arg_set = [(val,) for val in range(max_val + 1)]
        swap_arg_set = tuple(product(range(max_mem), repeat=2))
        inc_arg_set = [(val,) for val in range(max_mem)]
        arg_set_gen = {load: load_arg_set, swap: swap_arg_set, xor:
                       swap_arg_set, inc: inc_arg_set}
        for length in range(1, max_length + 1):
            for prog in product(ops_values, repeat=length):
                arg_sets = [arg_set_gen[op] for op in prog]
                for arg_set in product(*arg_sets):
                    program = (*zip(prog, arg_set),)
                    yield program

    # Tests all of the generated programs and returns the shortest.
    def search(self, max_length, max_mem, max_val, target_state, debug=False):
        count = 0
        cpu = CPU(max_mem)
        for program in self.generate_programs(max_length, max_mem, max_val):
            state = cpu.execute(program)
            if state == target_state:
                state = tuple(state) 
                if state not in self.program_cache or len(program) < len(self.program_cache[state]):
                    self.program_cache[state] = program
            
            # Debugging.
            if debug:
                count += 1
                if count % 1000000 == 0: print(f"Programs searched: {count:,}")
                if count % 10000000 == 0: 
                    solution = self.program_cache.get(tuple(target_state), None)
                    print(f"Best solution: {solution}")

        return self.program_cache.get(tuple(target_state), None)
