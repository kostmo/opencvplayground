#!/bin/bash

svn checkout http://pyblobs.googlecode.com/svn/trunk/ pyblobs
cd pyblobs
./make_swig_shadow.sh

ln -s pyblobs/blobs
