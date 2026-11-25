clear()

from move_to import move_to

start_red = [(1 + 10,0 + 10), (1+ 10,1+ 10), (1+ 10,2+ 10), (2+ 10,2+ 10), (0+ 10,1+ 10)]

def build_initial():
	row = []
	for i in range(get_world_size()):
		if (get_pos_x(),get_pos_y()) in start_red:
			place(Grounds.Block_Red)
		else:
			place(Grounds.Block_Blue)
		if get_ground_type() == Grounds.Block_Blue:
			row.append(0)
		elif get_ground_type() == Grounds.Block_Red:
			row.append(1)
		move(North)
	return row

move_to((0,0))
jobs = []
cache = []
grid = []

for i in range(get_world_size()):
	drone = spawn_drone(build_initial)
	if drone == None:
		jobs.append((False, build_initial()))
	else:
		jobs.append((True, drone))
	move(East)
for is_drone, result in jobs:
	if is_drone:
		grid.append(wait_for(result))
	else:
		grid.append(result)

def around(point):
	x, y = point
	rows = len(grid)
	cols = len(grid[0])
	total = 0
	for dx in (-1, 0, 1):
		for dy in (-1, 0, 1):
			if dx == 0 and dy == 0:
				continue
			total += grid[(x + dx) % rows][(y + dy) % cols]
	return total
	
def step(point):
	x, y = point
	Alive = grid[x][y] == 1
	neighbors = around((x,y))

	if Alive == True and neighbors in (0,1):
		return 0
	elif Alive == True and neighbors in (2,3):
		return 1
	elif Alive == True and neighbors in (4,5,6,7,8):
		return 0
	elif Alive == False and neighbors == 3:
		return 1
	else:
		return 0

def fix_row():
	row = []

	for i in range(get_world_size()):
		state = step((get_pos_x(),get_pos_y()))
		row.append(state)

		if get_ground_type() == Grounds.Block_Blue and state == 1:
			dig()
			place(Grounds.Block_Red)

		elif get_ground_type() == Grounds.Block_Red and state == 0:
			dig()
			place(Grounds.Block_Blue)

		move(North)

	return row
while True:
	jobs = []
	cache = []

	for i in range(get_world_size()):
		drone = spawn_drone(fix_row)

		if drone == None:
			jobs.append((False, fix_row()))
		else:
			jobs.append((True, drone))

		move(East)

	for is_drone, result in jobs:
		if is_drone:
			cache.append(wait_for(result))
		else:
			cache.append(result)

	grid = cache
