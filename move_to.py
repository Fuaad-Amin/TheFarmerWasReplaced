def move_to(tile):
  x, y = tile
	n = get_world_size()
	dx = (x - get_pos_x()) % n
	dy = (y - get_pos_y()) % n
	if dx <= n // 2:
		for i in range(dx):
			move(East)
	else:
		for i in range(n - dx):
			move(West)
	if dy <= n // 2:
		for i in range(dy):
			move(North)
	else:
		for i in range(n - dy):
			move(South)
