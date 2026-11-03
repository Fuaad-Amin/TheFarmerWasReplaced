
from move_to import move_to
from infect_all import infect_all

# Also included an infection toggle to farm Weird_substance as infected cactus gives a lot
infect = False

def back_prop_row():
	sorted = False
	while sorted == False:
		if measure() < measure(West) and measure(West) != None:
			swap(West)
			move(West)
			sorted = False
		else:
			sorted = True
	
def insertion_sort_row():
	for i in range(get_world_size() - 1):
		move_to((i + 1,get_pos_y()))
		back_prop_row()

def back_prop_rank():
	sorted = False
	while sorted == False:
		if measure() < measure(South) and measure(South) != None:
			swap(South)
			move(South)
			sorted = False
		else:
			sorted = True
	
def insertion_sort_rank():
	for i in range(get_world_size() - 1):
		move_to((get_pos_x(),i + 1))
		back_prop_rank()


def reset_row():
	for i in range(get_world_size()):
		if get_entity_type() != Entities.Cactus:
			harvest()
		if get_ground_type() != Grounds.Soil:
			till()
		plant(Entities.Cactus)
		move(East)

clear()

while num_items(Items.Cactus) < 335544320:
	for i in range(get_world_size()):
		if not spawn_drone(reset_row):
			reset_row()
		move(North)
	while num_drones() > 1:
		pass
	move_to((0,0))
	if infect == True:
		infect_all()
	for i in range(get_world_size()):
		if not spawn_drone(insertion_sort_row):
			insertion_sort_row()
		move(North)
	while num_drones() > 1:
		pass
	for i in range(get_world_size()):
		if not spawn_drone(insertion_sort_rank):
			insertion_sort_rank()
		move(East)
	while num_drones() > 1:
		pass
	while not can_harvest():
		pass
	harvest()
