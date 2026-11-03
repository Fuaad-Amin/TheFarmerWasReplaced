from move_to import move_to

clear()
set_world_size(32)

def qr_xor(a, b):
	result = 0
	place = 1
	while a > 0 or b > 0:
		if a % 2 != b % 2:
			result = result + place
		a = a // 2
		b = b // 2
		place = place * 2
	return result


def qr_mul(a, b):
	result = 0
	while b > 0:
		if b % 2 == 1:
			result = qr_xor(result, a)
		b = b // 2
		a = a * 2
		if a >= 256:
			a = qr_xor(a - 256, 29)
	return result


def qr_bits(bits, number, count):
	for i in range(count - 1, -1, -1):
		bits.append((number // (2 ** i)) % 2)


def qr_set(matrix, reserved, x, y, dark):
	matrix[y][x] = dark
	reserved[y][x] = True


def qr_coordinates(message):
	length = len(message)

	if length <= 17:
		version = 1
		capacity = 19
		generator = [127, 122, 154, 164, 11, 68, 117]
	elif length <= 32:
		version = 2
		capacity = 34
		generator = [216, 194, 159, 111, 199, 94, 95, 113, 157, 193]
	elif length <= 53:
		version = 3
		capacity = 55
		generator = [29, 196, 111, 163, 112, 74, 10, 105, 105, 139, 132, 151, 32, 134, 26]
	else:
		return None
		
	alphabet = ' !"#$%&' + "'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~"

	bits = []
	qr_bits(bits, 4, 4)
	qr_bits(bits, length, 8)

	for i in range(length):
		code = -1
		for j in range(len(alphabet)):
			if alphabet[j] == message[i]:
				code = j + 32
				break
		if code == -1:
			return None
		qr_bits(bits, code, 8)

	for i in range(min(4, capacity * 8 - len(bits))):
		bits.append(0)

	while len(bits) % 8 != 0:
		bits.append(0)

	pad = 236
	while len(bits) < capacity * 8:
		qr_bits(bits, pad, 8)
		if pad == 236:
			pad = 17
		else:
			pad = 236

	data = []
	for i in range(0, len(bits), 8):
		value = 0
		for j in range(8):
			value = value * 2 + bits[i + j]
		data.append(value)

	ec_size = len(generator)
	ecc = []
	for i in range(ec_size):
		ecc.append(0)

	for value in data:
		factor = qr_xor(value, ecc[0])
		for j in range(ec_size - 1):
			ecc[j] = qr_xor(
				ecc[j + 1],
				qr_mul(generator[j], factor)
			)
		ecc[ec_size - 1] = qr_mul(
			generator[ec_size - 1], factor
		)

	codewords = data + ecc
	size = version * 4 + 17

	matrix = []
	reserved = []

	for y in range(size):
		row = []
		flags = []
		for x in range(size):
			row.append(False)
			flags.append(False)
		matrix.append(row)
		reserved.append(flags)

	# Timing patterns
	for i in range(size):
		qr_set(matrix, reserved, 6, i, i % 2 == 0)
		qr_set(matrix, reserved, i, 6, i % 2 == 0)

	# Finder patterns
	centers = [(3, 3), (size - 4, 3), (3, size - 4)]

	for center in centers:
		cx = center[0]
		cy = center[1]

		for dy in range(-4, 5):
			for dx in range(-4, 5):
				x = cx + dx
				y = cy + dy

				if 0 <= x and x < size and 0 <= y and y < size:
					distance = max(abs(dx), abs(dy))
					dark = distance != 2 and distance != 4
					qr_set(matrix, reserved, x, y, dark)

	# Alignment pattern
	if version >= 2:
		center = size - 7
		for dy in range(-2, 3):
			for dx in range(-2, 3):
				distance = max(abs(dx), abs(dy))
				qr_set(
					matrix, reserved,
					center + dx, center + dy,
					distance != 1
				)

	# Format information: correction level L, mask 0
	fmt = 30660

	for i in range(6):
		qr_set(matrix, reserved, 8, i, (fmt // (2 ** i)) % 2 == 1)

	qr_set(matrix, reserved, 8, 7, (fmt // 64) % 2 == 1)
	qr_set(matrix, reserved, 8, 8, (fmt // 128) % 2 == 1)
	qr_set(matrix, reserved, 7, 8, (fmt // 256) % 2 == 1)

	for i in range(9, 15):
		qr_set(matrix, reserved, 14 - i, 8, (fmt // (2 ** i)) % 2 == 1)

	for i in range(8):
		qr_set(matrix, reserved, size - 1 - i, 8, (fmt // (2 ** i)) % 2 == 1)

	for i in range(8, 15):
		qr_set(matrix, reserved, 8, size - 15 + i, (fmt // (2 ** i)) % 2 == 1)

	qr_set(matrix, reserved, 8, size - 8, True)

	# Place data and apply mask
	index = 0
	right = size - 1

	while right >= 1:
		if right == 6:
			right = 5

		upward = ((right + 1) // 2) % 2 == 0

		for v in range(size):
			if upward:
				y = size - 1 - v
			else:
				y = v

			for j in range(2):
				x = right - j

				if not reserved[y][x]:
					dark = False

					if index < len(codewords) * 8:
						value = codewords[index // 8]
						bit = 7 - index % 8
						dark = (value // (2 ** bit)) % 2 == 1
						index = index + 1

					if (x + y) % 2 == 0:
						dark = not dark

					matrix[y][x] = dark

		right = right - 2

	# Convert to 32x32 farm coordinates
	offset = (32 - size) // 2
	coordinates = []

	for y in range(size):
		for x in range(size):
			if matrix[y][x]:
				coordinates.append((x + offset, 31 - y - offset))
	return coordinates

clear()


black_squares = qr_coordinates("Your input goes here")
# Use QR sim to view your input faster

for i in black_squares:
	move_to(i)
	till()
move_to((0,0))
while True:
	pass

