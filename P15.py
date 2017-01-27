"""N-Queens problem"""

from search import *
import sys
import timeit

class P15(Problem) :
	"""Subclass of search.Problem"""

	def __init__(self, start_state, goal_state) :
		super(P15, self).__init__(start_state, goal_state)
		self.free_m = []
		for x in range(4):
			for y in range(4):
				self.free_m.append(self.actions(start_state))

	def actions(self, state) :
		row, col = search_coords(state, 0)
		action_list = []
		# find which pieces can move there
		if row > 0:
			action_list.append((row - 1, col))
		if col > 0:
			action_list.append((row, col - 1))
		if row < 3:
			action_list.append((row + 1, col))
		if col < 3:
			action_list.append((row, col + 1))
		return action_list
	
	def result(self, state, action) :
		row, col = search_coords(state, 0)
		list_of_tuples = list(state)
		list_of_lists = [list(elem) for elem in list_of_tuples]
		i = action[0]
		j = action[1]
		list_of_lists[row][col] = list_of_lists[i][j]
		list_of_lists[i][j] = 0
		list_of_tuples = (tuple(elem) for elem in list_of_lists)
		return tuple(list_of_tuples)


def search_coords(state, value) :
	""" returns coords of value """
	if value < 0 or value > 15:
		return -1, -1
	list_of_tuples = list(state)
	list_of_lists = [list(elem) for elem in list_of_tuples]
	for row in range(4):
		for col in range(4):
			if list_of_lists[row][col] == value:
				return row, col
		
def h1(n, goal_state) :
	misplaced_tiles = 0
	for i in range(4):
		for j in range(4):
			if n.state[i][j]!=0 and goal_state[i][j] != n.state[i][j]:
				misplaced_tiles += 1
	return misplaced_tiles

def h2(n, goal_state) :
	manhattan_distance = 0
	for i in range(4):
		for j in range(4):
			value = n.state[i][j]
			i_goal_state, j_goal_state = search_coords(goal_state, value)
			manhattan_distance += abs(i - i_goal_state) + abs(j - j_goal_state)
	return manhattan_distance

def h3(n, goal_state) :
	h = 0
	lot_current_state = list(n.state)
	current_state = [list(elem) for elem in lot_current_state]
	lot_goal_state = list(goal_state)
	lgoal_state = [list(elem) for elem in lot_goal_state]
	while (current_state != lgoal_state):
		blanki, blankj = search_coords(current_state, 0);
		if current_state[blanki][blankj] != lgoal_state[blanki][blankj]:
			righti, rightj = search_coords(current_state, lgoal_state[blanki][blankj])
			current_state[blanki][blankj] = lgoal_state[blanki][blankj]
			current_state[righti][rightj] = 0
		else:
			flag = False
			for i in range(4):
				for j in range(4):
					if current_state[i][j] != lgoal_state[i][j]:
						current_state[blanki][blankj] = current_state[i][j]
						current_state[i][j] = 0
						flag = True
						break
				if flag == True:
					break
		h += 1				
	return h

def h4(n, goal_state):
	wrong_line=0
	wrong_column=0
	for i in range(4):
		for j in range(4):
			if n.state[i][j]!=0 and goal_state[0][j] != n.state[i][j] and goal_state[1][j] != n.state[i][j] and goal_state[2][j] != n.state[i][j] and goal_state[i][j] != n.state[3][j] :
				wrong_line +=1
	for j in range(4):
		for i in range(4):
			if n.state[i][j]!=0 and goal_state[i][0] != n.state[i][j] and goal_state[i][1] != n.state[i][j] and goal_state[i][2] != n.state[i][j] and goal_state[i][j] != n.state[i][3] :
				wrong_column +=1
	wrong= wrong_line+wrong_column
	return wrong

print "TEST CASE 1"
print "Start State = ((1, 2, 3, 4), (5, 6, 7, 8), (0, 9, 10, 12), (13, 14, 11, 15))" 
print "Goal State = ((1, 2, 3, 4), (5, 6, 7, 8), (9, 10, 11, 12), (13, 14, 15, 0))"
print ""
p = P15(((1, 2, 3, 4), (5, 6, 7, 8), (9, 0, 10, 12), (13, 14, 11, 15)), ((1, 2, 3, 4), (5, 6, 7, 8), (9, 10, 11, 12), (13, 14, 15, 0)))
print "Heuristic 1 (misplaced tiles):"
print ""
start = timeit.default_timer()
solution = astar_search(p, lambda node : h1(node, p.goal))
print solution.path()
stop = timeit.default_timer()
print stop - start
print ""

print "Heuristic 2 (manhattan distance):"
print ""
start = timeit.default_timer()
solution = astar_search(p, lambda node : h2(node, p.goal))
print solution.path()
stop = timeit.default_timer()
print stop - start
print ""

print "Heuristic 3 (gaschnig):"
print ""
start = timeit.default_timer()
solution = astar_search(p, lambda node : h3(node, p.goal))
print solution.path()
stop = timeit.default_timer()
print stop - start
print ""

print "Heuristic 4:"
print ""
start = timeit.default_timer()
solution = astar_search(p, lambda node : h4(node, p.goal))
print solution.path()
stop = timeit.default_timer()
print stop - start
print ""

print "TEST CASE 2"
print "Start State = ((5, 1, 7, 3), (9, 2, 11, 4), (13, 6, 15, 8), (0, 10, 14, 12))" 
print "Goal State = ((1, 2, 3, 4), (5, 6, 7, 8), (9, 10, 11, 12), (13, 14, 15, 0))"
print ""
p = P15(((5, 1, 7, 3), (9, 2, 11, 4), (13, 6, 15, 8), (0, 10, 14, 12)), ((1, 2, 3, 4), (5, 6, 7, 8), (9, 10, 11, 12), (13, 14, 15, 0)))
print "Heuristic 1 (misplaced tiles):"
print ""
start = timeit.default_timer()
solution = astar_search(p, lambda node : h1(node, p.goal))
print solution.path()
stop = timeit.default_timer()
print stop - start
print ""

print "Heuristic 2 (manhattan distance):"
print ""
start = timeit.default_timer()
solution = astar_search(p, lambda node : h2(node, p.goal))
print solution.path()
stop = timeit.default_timer()
print stop - start
print ""

print "Heuristic 3 (gaschnig):"
print ""
start = timeit.default_timer()
solution = astar_search(p, lambda node : h3(node, p.goal))
print solution.path()
stop = timeit.default_timer()
print stop - start
print ""

print "Heuristic 4:"
print ""
start = timeit.default_timer()
solution = astar_search(p, lambda node : h4(node, p.goal))
print solution.path()
stop = timeit.default_timer()
print stop - start
print ""

print "TEST CASE 3"
print "Start State = ((5, 1, 3, 4), (2, 6, 7, 8), (9, 10, 12, 0), (13, 14, 11, 15))" 
print "Goal State = ((1, 2, 3, 4), (5, 6, 7, 8), (9, 10, 11, 12), (13, 14, 15, 0))"
print ""
p = P15(((5, 1, 3, 4), (2, 6, 7, 8), (9, 10, 12, 0), (13, 14, 11, 15)), ((1, 2, 3, 4), (5, 6, 7, 8), (9, 10, 11, 12), (13, 14, 15, 0)))
print "Heuristic 1 (misplaced tiles):"
print ""
start = timeit.default_timer()
solution = astar_search(p, lambda node : h1(node, p.goal))
print solution.path()
stop = timeit.default_timer()
print stop - start
print ""

print "Heuristic 2 (manhattan distance):"
print ""
start = timeit.default_timer()
solution = astar_search(p, lambda node : h2(node, p.goal))
print solution.path()
stop = timeit.default_timer()
print stop - start
print ""

print "Heuristic 3 (gaschnig):"
print ""
start = timeit.default_timer()
solution = astar_search(p, lambda node : h3(node, p.goal))
print solution.path()
stop = timeit.default_timer()
print stop - start
print ""

print "Heuristic 4:"
print ""
start = timeit.default_timer()
solution = astar_search(p, lambda node : h4(node, p.goal))
print solution.path()
stop = timeit.default_timer()
print stop - start
print ""



print "TEST CASE 4"
print "Start State = ((1, 6, 4, 0), (5, 2, 3, 7), (9, 14, 10, 8), (13, 15, 11, 12))" 
print "Goal State = ((1, 2, 3, 4), (5, 6, 7, 8), (9, 10, 11, 12), (13, 14, 15, 0))"
print ""
p = P15(((1, 6, 4, 0), (5, 2, 3, 7), (9, 14, 10, 8), (13, 15, 11, 12)), ((1, 2, 3, 4), (5, 6, 7, 8), (9, 10, 11, 12), (13, 14, 15, 0)))
print "Heuristic 1 (misplaced tiles):"
print ""
start = timeit.default_timer()
solution = astar_search(p, lambda node : h1(node, p.goal))
print solution.path()
stop = timeit.default_timer()
print stop - start
print ""

print "Heuristic 2 (manhattan distance):"
print ""
start = timeit.default_timer()
solution = astar_search(p, lambda node : h2(node, p.goal))
print solution.path()
stop = timeit.default_timer()
print stop - start
print ""

print "Heuristic 3 (gaschnig):"
print ""
start = timeit.default_timer()
solution = astar_search(p, lambda node : h3(node, p.goal))
print solution.path()
stop = timeit.default_timer()
print stop - start
print ""

print "Heuristic 4:"
print ""
start = timeit.default_timer()
solution = astar_search(p, lambda node : h4(node, p.goal))
print solution.path()
stop = timeit.default_timer()
print stop - start
print ""