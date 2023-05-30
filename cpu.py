class CPU:
    def __init__(self, max_mem_cells):
        self.max_mem_cells = max_mem_cells
        self.state = [0] * max_mem_cells

    def execute(self, program):
        state = self.state.copy()
        swap = CPU.swap
        xor = CPU.xor
        for instruction in program:
            op = instruction[0]
            args = instruction[1]
            if op is swap or op is xor:
                op(self, state, args[0], args[1])
            else:
                op(self, state, args[0])
        return state

    def load(self, state, val):
        state[0] = val
    
    def swap(self, state, mem1, mem2):
        state[mem1], state[mem2] = state[mem2], state[mem1]
    
    def xor(self, state, mem1, mem2):
        state[mem1] = state[mem1] ^ state[mem2]
    
    def inc(self, state, mem):
        state[mem] += 1

    ops = {'LOAD': load, 'SWAP': swap, 'XOR': xor, 'INC': inc}
