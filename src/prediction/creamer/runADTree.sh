#!/bin/bash
# 1st arg - path to the place where the data is held
# 2nd arg - stem:
#	- stem.spec
#	- stem.train
#	- stem.test

export JBOOST_DIR="/Users/User/Dropbox/Code/boosting/jboost-2.2" 
export CLASSPATH="$CLASSPATH:$JBOOST_DIR/dist/jboost.jar:$JBOOST_DIR/lib/jfreechart-1.0.10.jar:$JBOOST_DIR/lib/jcommon-1.0.8.jar"


cd $1
java jboost.controller.Controller -b LogLossBoost -numRounds 50 -S $2 -P $2predict.py -n spec.spec

#python ./error.py --info=$2.info

#perl ./atree2dot2ps.pl  --info $2.info --tree $2.output.tree --threshold 10 

exit