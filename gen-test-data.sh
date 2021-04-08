
#
python make_sample_generators.py 
#

#brun -x gen0002.clvm > g2
#brun -x compressed-gen0002.clvm > cg2
#diff g2 cg2

#brun -x gen0002.clvm > g2
for f in compressed-cse??00.clvm.hex; do
  ./make-cgen $f  
done

for g in gen??00.clvm.hex; do
  cp $g generators/
  opd $g > generators/$(basename $g .hex) &
done

