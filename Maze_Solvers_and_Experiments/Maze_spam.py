# Literally the fastest way to farm a ton of gold in the game provided you had Weird_Substance to burn

clear()

from move_to import move_to
from Solve_maze import make_maze, solve
from DFS import solve_dfs

def tiny_solver(a,b):
	do_a_flip()
	while num_items(Items.Gold) < 9863168000:
		move_to((a,b))
		make_maze(4)
		solve_dfs(4)
		use_item(Items.Weird_Substance, 4 * 2**(num_unlocked(Unlocks.Mazes) - 1))
		if get_entity_type() == Entities.Treasure:
			harvest()

for x in range(8):
	for y in range(4):
		move_to((4*x+2,4*y+2))
		if not spawn_drone(tiny_solver,4*x+2,4*y+2):
			tiny_solver(4*x+2,4*y+2)
