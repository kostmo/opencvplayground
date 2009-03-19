#!/usr/bin/python
from opencv import cv
from opencv import highgui

# =======================================================
def print_matrix(matrix, digits=None):

	if matrix.rows == 1 or matrix.cols == 1:
		quant = max(matrix.rows, matrix.cols)
		for i in range(quant):
			print (("%."+str(digits)+"f\t") % matrix[i]),
		print
	else:
		for i in range(matrix.rows):
			for j in range(matrix.cols):
				if not (digits is None):
					print (("%."+str(digits)+"f\t") % matrix[i][j]),
				else:
					print matrix[i][j], "\t",
			print

# =======================================================

class ChessboardDataContainer:

	def __init__(self, image_points, chessboard_inner_points):

		self.image_points = image_points
		self.object_points = []

		# Generate Checkboard Pattern
		square_unit = 1.0
		for i in range(chessboard_inner_points[0]):
			for j in range(chessboard_inner_points[1]):
				self.object_points.append( cv.cvPoint3D32f( (j+1)*square_unit, (chessboard_inner_points[1] - i)*square_unit, 0) )

# ===================================================

def try_calibration(chessboard_data_collection, corner_counts, frame_size):

	# Convert everything to matrices
	per_board_point_quantity = corner_counts[0]*corner_counts[1]

	corners_matrix = cv.cvCreateMat( len(chessboard_data_collection)*per_board_point_quantity, 2, cv.CV_32FC1 )
	object_points_matrix = cv.cvCreateMat( len(chessboard_data_collection)*per_board_point_quantity, 3, cv.CV_32FC1 )
#	point_counts_matrix = cv.cvCreateMat( len( chessboard_data_collection ), 1, cv.CV_32FC1 )
	point_counts_matrix = cv.cvCreateMat( len( chessboard_data_collection ), 1, cv.CV_32SC1 )	# This is the format that cvCalibrateCamera2 expects


	for i, chessdata in enumerate(chessboard_data_collection):

		for j, point in enumerate( chessdata.image_points ):
			cv.cvmSet(corners_matrix, i*per_board_point_quantity + j, 0, point.x)
			cv.cvmSet(corners_matrix, i*per_board_point_quantity + j, 1, point.y)

		for j, point in enumerate( chessdata.object_points ):
			cv.cvmSet(object_points_matrix, i*per_board_point_quantity + j, 0, point.x)
			cv.cvmSet(object_points_matrix, i*per_board_point_quantity + j, 1, point.y)
			cv.cvmSet(object_points_matrix, i*per_board_point_quantity + j, 2, point.z)

		# None of the following approaches are successful in converting to the correct integer value.
#		cv.cvmSet(point_counts_matrix, i, 0, per_board_point_quantity)
#		cv.cvmSet(point_counts_matrix, i, 0, int(per_board_point_quantity))
#		cv.cvmSet(point_counts_matrix, i, 0, cv.cvRound(per_board_point_quantity))

		# THIS ACTUALLY DOES WORK!
		point_counts_matrix[i] = per_board_point_quantity



	intrinsic, distortion = cv.cvCalibrateCamera2(
		object_points_matrix,	# Object points: a 3xN matrix, listing all the points in all the images
		corners_matrix,	# Image points: a 2xN matrix, listing all the 2D points in all the images
		point_counts_matrix,	# A vector (i.e. 1xM maxtrix) of point counts per image
		frame_size	# Image size
	)

	print "Intrinsic Parameters:"
	print_matrix(intrinsic)

# ===================================================

if __name__ == "__main__":

	chessboard_dimension = 4

	chessboard_inner_points = chessboard_dimension - 1
	chessboard_dim = cv.cvSize( chessboard_inner_points, chessboard_inner_points )

	chessboard_data_set = []
	img = None
	for i in range(4):
		img = highgui.cvLoadImage("images/cal%d.jpg"%i, highgui.CV_LOAD_IMAGE_COLOR)
		found_all, corners = cv.cvFindChessboardCorners( img, chessboard_dim )
		chessboard_data_set.append( ChessboardDataContainer(corners, [chessboard_inner_points, chessboard_inner_points]) )

	

	try_calibration(chessboard_data_set, [chessboard_inner_points, chessboard_inner_points], cv.cvGetSize(img))

	print "Done."

