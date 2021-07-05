#!/bin/bash
echo "Installing requirements"
pip3 install -r requirements.txt
echo "Downloading word vectors and saving them, this is a one off download"
python3 save_vectors.py
echo "Finished. Program can be run with 'python3 run.py'"