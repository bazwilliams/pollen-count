#!/bin/sh
rm -rf ./build/
mkdir build
cp *.py build
pip install -r requirements.txt -t build
cd build/
zip ../lambda.zip -r . *
