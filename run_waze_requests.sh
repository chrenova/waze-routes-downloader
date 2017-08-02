#!/bin/bash

echo "1"
export WAZE_HOME=/home/mano/dev/waze/
echo $WAZE_HOME

rt=$1
echo $rt

cd $WAZE_HOME
source .venv/bin/activate

python -m waze_requests $rt
