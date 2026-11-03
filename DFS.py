from Solve_maze import make_maze
from move_to import move_to
		
def solve_dfs(size):
		
	def g(pos):
		x,y=pos
		array = []
		if can_move(North):
			array.append((x,y+1))
		if can_move(South):
			array.append((x,y-1))
		if can_move(East):
			array.append((x+1,y))
		if can_move(West):
			array.append((x-1,y))
		return array
		

	seen = set()

	def dfs(tile):
		if get_entity_type() == Entities.Treasure:
			return True

		seen.add(tile)

		for w in g(tile):
			if w not in seen:
				move_to(w)
				if dfs(w):
					return True
				move_to(tile)

		return False

	if dfs((get_pos_x(), get_pos_y())):
		use_item(Items.Weird_Substance, size * 2**(num_unlocked(Unlocks.Mazes) - 1))
