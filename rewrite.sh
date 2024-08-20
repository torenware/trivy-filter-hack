#! /usr/bin/env bash

#
# This script is a "front end" to the trivy binary. You'll
# typically install it as "trivy" in some directory that will
# be called before where the trivy binary is in the PATH.
#

# Edit this file to point to where you
# installed the trivy-wrapper.py script
WRAPPER_INSTALL_DIR=.

if [ "$1" != "image" ]; then
  exec trivy $@
else
  if CMD=$(python3 $WRAPPER_INSTALL_DIR/trivy-wrap.py $@); then
    echo "command: $CMD"
    exec $CMD
  else
    echo trivy command failed to parse
  fi

fi
