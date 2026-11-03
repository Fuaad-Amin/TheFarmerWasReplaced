clear()

#Wall Hugging algorithm as well as a maze maker

def make_maze(size):
	plant(Entities.Bush)
	while can_harvest() == False:
		use_item(Items.Fertilizer)
		use_item(Items.Weird_Substance, size * 2**(num_unlocked(Unlocks.Mazes) - 1))

def clockwise(direction):
	if direction == East:
		return(South)
	if direction == South:
		return(West)
	if direction == West:
		return(North)
	if direction == North:
		return(East)
			
def counter_clockwise(direction):
	if direction == East:
		return(North)
	if direction == South:
		return(East)
	if direction == West:
		return(South)
	if direction == North:
		return(West)

def solve():
	Facing = North
	while get_entity_type() != Entities.Treasure:
		if can_move(counter_clockwise(Facing)):
			Facing = counter_clockwise(Facing)
			move(Facing)
		elif can_move(Facing):
			move(Facing)
		else:
			Facing = clockwise(Facing)
	use_item(Items.Weird_Substance, get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1))

