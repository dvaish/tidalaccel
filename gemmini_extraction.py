import re
from dataclasses import dataclass
from tqdm import tqdm
from tidalsim.tidalsim.util.spike_log import parse_spike_log

# RISC-V Base ISA custom opcode space
custom = {
    "CUSTOM_0": 0b00_010_11,
    "CUSTOM_1": 0b00_010_11,
    "CUSTOM_2": 0b10_110_11,
    "CUSTOM_3": 0b11_110_11,
}

# funct7 map from Gemmini.h
# These funct7 codes tell us which Gemmini instruction is being executed from the RoCC instruction
gemmini_funct7 = {
    0:   "k_CONFIG",
    1:   "k_MVIN2",
    2:   "k_MVIN",
    3:   "k_MVOUT",
    4:   "k_COMPUTE_PRELOADED",
    5:   "k_COMPUTE_ACCUMULATE",
    6:   "k_PRELOAD",
    7:   "k_FLUSH",
    8:   "k_LOOP_WS",
    9:   "k_LOOP_WS_CONFIG_BOUNDS",
    10:  "k_LOOP_WS_CONFIG_ADDRS_AB",
    11:  "k_LOOP_WS_CONFIG_ADDRS_DC",
    12:  "k_LOOP_WS_CONFIG_STRIDES_AB",
    13:  "k_LOOP_WS_CONFIG_STRIDES_DC",
    14:  "k_MVIN3",
    126: "k_COUNTER",
    15:  "k_LOOP_CONV_WS",
    16:  "k_LOOP_CONV_WS_CONFIG_1",
    17:  "k_LOOP_CONV_WS_CONFIG_2",
    18:  "k_LOOP_CONV_WS_CONFIG_3",
    19:  "k_LOOP_CONV_WS_CONFIG_4",
    20:  "k_LOOP_CONV_WS_CONFIG_5",
    21:  "k_LOOP_CONV_WS_CONFIG_6",
    23:  "k_MVOUT_SPAD"
}

class RoCCInstruction:
    def __init__(self, pc: int, inst: int):
        self.pc = pc
        self.inst = inst

        self.opcode = inst % (2 ** 7)           # inst[6:0]
        self.funct7 = (inst >> 25) % (2 ** 7)   # inst[31:25]

        self.xs1 = (inst >> 12) % 2             # inst[12]
        self.xs2 = (inst >> 13) % 2             # inst[13]
        self.xd  = (inst >> 14) % 2             # inst[14]

        self.rs1 = (inst >> 15) % (2 ** 5)      # inst[15:19]
        self.rs2 = (inst >> 20) % (2 ** 5)      # inst[20:24]
        self.rd = (inst >> 7)  % (2 ** 5)       # inst[7:11]


@dataclass
class GemminiInstruction(RoCCInstruction):

    def __init__(self, pc: int, inst: int):
        super().__init__(pc, inst)
        self.decoded_inst = gemmini_funct7[self.funct7]


tracefile = "log.log"

with open(tracefile) as f:
    lines = f.readlines()
    f.close()

spike_log = parse_spike_log(iter(lines), full_commit_log=False)

gemmini_instructions = []
for entry in tqdm(spike_log):
    if entry.decoded_inst == "unknown":
        gemmini_instruction = GemminiInstruction(entry.pc, entry.inst)
        gemmini_instructions.append(gemmini_instruction)

for inst in gemmini_instructions:
    print(f"{inst.decoded_inst} x{inst.rs1}, x{inst.rs2}, x{inst.rd} ({inst.xd}{inst.xs2}{inst.xs1})")