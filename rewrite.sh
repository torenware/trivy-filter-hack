#! /usr/bin/env bash

if [ "$1" != "image" ]; then
  exec trivy $@
else
  if CMD=$(python3 trivy-wrap.py $@); then
    echo "command: $CMD"
    exec $CMD
  else
    echo trivy command failed to parse
  fi

fi
