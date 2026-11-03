#Just makes the smallest maze given the amount of drones you have and fills the maze
#Putting a drone on every tile and hence at the Treasure
#This is great for early game but Maze_spam is the fastest


clear()
largest_square = (max_drones()**0.5)//1

set_world_size(largest_square)

from move_to import move_to

amount = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)

def reset():
	harvest()
	plant(Entities.Bush)
	while can_harvest() == False:
		use_item(Items.Fertilizer)
		use_item(Items.Weird_Substance, amount)

def move_and_wait(index):
	for i in range(index):
		spawn_drone(move_and_wait,0)
		move(North)
	while True:
		if get_entity_type() == Entities.Treasure:
			use_item(Items.Weird_Substance, amount)
			if get_entity_type() == Entities.Treasure:
				reset()
				
for i in range(largest_square):
	spawn_drone(move_and_wait,largest_square-1)
	move(East)
do_a_flip()
	
plant(Entities.Bush)
while num_drones() < largest_square:
	do_a_flip()
	
while can_harvest() == False:
	use_item(Items.Fertilizer)
	use_item(Items.Weird_Substance, amount)

	
