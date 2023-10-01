from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF, QObject
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtCore import QLineF, QPointF, QObject
elif PYQT_VER == 'PYQT6':
	from PyQt6.QtCore import QLineF, QPointF, QObject
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))



import time
import math

# Some global color constants that might be useful
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

# Global variable that controls the speed of the recursion automation, in seconds
PAUSE = 2

# A node is one point in a hull. It contains a QPointF object and pointers to the previous and next nodes.
class Node:
	def __init__(self, point):
		self.point = point
		self.prev = None
		self.next = None

# This stores the leftmost and rightmost nodes in a hull. Ultimately, the nodes are all connected together in a circular list
class Hull:
	def __init__(self, leftmost: Node, rightmost: Node):
		self.leftmost = leftmost
		self.rightmost = rightmost

#
# This is the class you have to complete.
#
class ConvexHullSolver(QObject):

# Class constructor
	def __init__( self):
		super().__init__()
		self.pause = False

# Some helper methods that make calls to the GUI, allowing us to send updates
# to be displayed.

	def showTangent(self, line, color):
		self.view.addLines(line,color)
		if self.pause:
			time.sleep(PAUSE)

	def eraseTangent(self, line):
		self.view.clearLines(line)

	def blinkTangent(self,line,color):
		self.showTangent(line,color)
		self.eraseTangent(line)

	def showHull(self, polygon, color):
		self.view.addLines(polygon,color)
		if self.pause:
			time.sleep(PAUSE)

	def eraseHull(self,polygon):
		self.view.clearLines(polygon)

	def showText(self,text):
		self.view.displayStatusText(text)


# This is the method that gets called by the GUI and actually executes
# the finding of the hull
	def compute_hull( self, points, pause, view):
		self.pause = pause
		self.view = view
		assert( type(points) == list and type(points[0]) == QPointF )

		t1 = time.time()
		# TODO: SORT THE POINTS BY INCREASING X-VALUE
		sorted_points = sorted(points, key=lambda x: x.x(), reverse=False)

		t2 = time.time()

		t3 = time.time()
		
		hull = self.solve(sorted_points)
		polygon = []
		
		curr_node = hull.leftmost
		while curr_node.next != hull.leftmost:
			polygon.append(QLineF(curr_node.point, curr_node.next.point))
			curr_node = curr_node.next
		
		polygon.append(QLineF(curr_node.point, curr_node.next.point))
		
		t4 = time.time()

		# when passing lines to the display, pass a list of QLineF objects.  Each QLineF
		# object can be created with two QPointF objects corresponding to the endpoints
		self.showHull(polygon,RED)
		self.showText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4-t3))

	def calculate_slope(self, left_node: Node, right_node: Node) -> float:
		rise = right_node.point.y() - left_node.point.y()
		run = right_node.point.x() - left_node.point.x()

		return rise / run
	
	def connectNodes(self, prevNode: Node, nextNode: Node) -> None:
		prevNode.next = nextNode
		nextNode.prev = prevNode
	
	def merge(self, left_hull: Hull, right_hull: Hull) -> Hull:
		left_upper = left_lower = left_hull.rightmost
		right_upper = right_lower = right_hull.leftmost

		slope = self.calculate_slope(left_upper, right_upper)
		slope_changed = True

		# finding upper tangent
		while slope_changed:
			slope_changed = False

			new_slope = self.calculate_slope(left_upper.prev, right_upper)
			if new_slope < slope:
				slope_changed = True
				left_upper = left_upper.prev
				slope = new_slope
		
			new_slope = self.calculate_slope(left_upper, right_upper.next)
			if new_slope > slope:
				slope_changed = True
				right_upper = right_upper.next
				slope = new_slope


		slope_decreased = True
		slope = self.calculate_slope(left_lower, right_lower)

		# finding lower tangent
		while slope_decreased:
			slope_decreased = False
			
			new_slope = self.calculate_slope(left_lower.next, right_lower)
			if new_slope > slope:
				slope_decreased = True
				left_lower = left_lower.next
				slope = new_slope
		
			new_slope = self.calculate_slope(left_lower, right_lower.prev)
			if new_slope < slope:
				slope_decreased = True
				right_lower = right_lower.prev
				slope = new_slope
			
		# connect tangent nodes
		self.connectNodes(left_upper, right_upper)
		self.connectNodes(right_lower, left_lower)

		return Hull(left_hull.leftmost, right_hull.rightmost)
	
	# recursive divide and conquer algorithm
	# returns convex hull of the current points
	def solve(self, points) -> Hull:
		# base case: len(points) = 2 or 3
		if len(points) == 2:
			node1 = Node(points[0])
			node2 = Node(points[1])
			self.connectNodes(node1, node2)
			self.connectNodes(node2, node1)
			return Hull(node1, node2)

		if len(points) == 3:
			node1 = Node(points[0])
			node2 = Node(points[1])
			node3 = Node(points[2])
				
			if self.calculate_slope(node1, node3) > self.calculate_slope(node1, node2):
				self.connectNodes(node1, node3)
				self.connectNodes(node3, node2)
				self.connectNodes(node2, node1)
			else:
				self.connectNodes(node1, node2)
				self.connectNodes(node2, node3)
				self.connectNodes(node3, node1)
			
			return Hull(node1, node3)

		# split into left and right halves
		split_index = math.ceil(len(points) / 2)
		left_hull = self.solve(points[:split_index])
		right_hull = self.solve(points[split_index:])
		
		return self.merge(left_hull, right_hull)


