Modular, PyGTK-based environment for prototyping image/video processing pipelines and experimentation with OpenCV.

## Design: ##
  * Stages of the pipeline illustrated in video, and separated by the "Right Arrow" stock icon.

## Pipeline stages implemented: ##
  * Thresholding
  * Blob filtering (via [pyblobs](http://pyblobs.googlecode.com/))

## Expected features: ##
  * Have "collapse" option to show or hide video
  * Drag and drop these functions, selectable from a menu
  * Have a treetable that shows pipeline stages and their execution times

## Separate tools ##
  * Point correspondence tool
  * Camera calibration tool
  * Hand-segmentation tool (TODO)

![http://opencvplayground.googlecode.com/svn/screenshots/slow_children.png](http://opencvplayground.googlecode.com/svn/screenshots/slow_children.png)