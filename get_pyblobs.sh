#!/bin/bash

svn checkout http://pyblobs.googlecode.com/svn/trunk/ pyblobs
cd pyblobs
./make_swig_shadow.sh
cd ..
ln -s pyblobs/blobs
