from chia.types.spend_bundle import SpendBundle
from chia.util.ints import uint32
from pathlib import Path

from tests.core.make_block_generator import make_block_generator
from chia.wallet.puzzles.load_clvm import load_clvm
from chia.types.blockchain_format.program import Program
from clvm import SExp
from clvm_tools import binutils
from chia.full_node.bundle_tools import best_solution_program

CGEN = load_clvm("cgen.clvm", package_or_requirement="src.wallet.puzzles")

def compress_spend_bundle(sb: SpendBundle):
    return compressed_solution_program(sb)


def compress_spend_bundle_program(sb: Program):
    #print(sb)
    compressed_cses = []
    for cse in sb.as_iter():
        a = cse.first()
        b = cse.rest().first().first()
        c = cse.rest().first().rest()
        s = b.rest().rest().first().rest().first().rest()
        p = SExp.to([a,[bytes(s),c.first()]])
        compressed_cses.append(p)
        #print(p)
    #return SExp.to([compressed_cses])
    return SExp.to(compressed_cses)

def compress_gen(g: Program):
    sb = Program.from_bytes(bytes(g)).rest()
    csb = compress_spend_bundle_program(sb)
    #print(csb)
    #cgen = SerializedProgram.from_bytes(SExp.to([binutils.assemble("#a"), CGEN, csb])).as_bin())
    #cgen = Program.to([binutils.assemble("#a"), quote(CGEN), quote([csb])])
    #cgen = binutils.assemble("(a 2 3)")
    cgen = CGEN.curry(csb)
    return cgen
    #return Program.from_bytes(b"\x80")

def gen(i):
    g = make_block_generator(i)
    genfile = Path(f"gen{i:04d}.clvm.hex")
    sb = Program.from_bytes(bytes(g)).rest()
    csb = compress_spend_bundle(sb)
    Path(f"compressed-cse{i:04d}.clvm.hex").write_text(str(csb))
    genfile.write_text(str(g))
    #compressed_genfile = Path(f"compressed-gen{i:04d}.clvm.hex")
    #compressed_genfile.write_text(str(compress_gen(g)))

#gen(2)

for i in range(10):
    gen(i)

for i in range(50, 2001, 50):
    gen(i)

