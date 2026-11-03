# Function to infect the whole field
from move_to import move_to

def infect_row():
	for i in range(get_world_size()):
		use_item(Items.Fertilizer)
		move(East)

def infect_all():
	for i in range(get_world_size()):
		if not spawn_drone(infect_row):
			infect_row()
		move(North)
