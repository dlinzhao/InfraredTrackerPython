#!/bin/bash

# export LD_LIBRARY_PATH=./lib:./lib/opencv-3.2:$CUDA_ROOT/lib64:$LD_LIBRARY_PATH
# export PYTHONPATH=./python/packages:$PYTHONPATH
export QT_PLUGIN_PATH=./plugins:$QT_PLUGIN_PATH
export QML2_IMPORT_PATH=./qml:$QML2_IMPORT_PATH
export XKB_DEFAULT_RULES=base
# export QT_XKB_CONFIG_ROOT=./xkb:$QT_XKB_CONFIG_ROOT
export QT_XKB_CONFIG_ROOT=/usr/share/X11/xkb:$QT_XKB_CONFIG_ROOT
# export CUDA_VISIBLE_DEVICES=1
python3 ./bin/RunInfraredTracker.py
