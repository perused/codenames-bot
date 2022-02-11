#!/bin/bash
echo "Installing requirements"
pip3 install -r setup/requirements.txt
echo "Downloading word vectors and saving them, this is a one off download"
python3 setup/setup_vectors.py
echo "Finished. Program can be run with 'python3 run.py'"