import libtcodpy as libt
SCREEN_WIDTH = 112
SCREEN_HEIGHT = 51
libt.console_set_custom_font('terminal8x12_gs_tc.png', libt.FONT_TYPE_GREYSCALE | libt.FONT_LAYOUT_TCOD)
output = libt.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'Shootout!', False)
libt.console_set_default_background(0, libt.black)
libt.console_set_default_foreground(0, libt.lightest_grey)

GRID_ROWS = 8
GRID_COLS = 8
ROW_SIZE = 6
COL_SIZE = 14
activex = 0
activey = 0
grid = []
minionmode = False

class Unit:
	"""Grid node"""
	def __init__(self, active = False, name = None, minion = False, wind = None, ammo = None, size = 6):
		self.minion = minion
		self.name = name
		self.size = size
		self.wind = wind
		self.ammo = ammo
		self.active = active
		self.wounds = {'head': 0, 'guts': 0, 'lArm': 0, 'rArm': 0, 'lLeg': 0, 'rLeg': 0}
		self.stun = False
		
	def wound(self, location, damage):
		self.wounds[location] += damage // self.size
		if self.wounds[location] > 5:
			self.wounds[location] = 5
		elif self.wounds[location] < 0:
			self.wounds[location] = 0
		if not self.wind == None:
			self.lose_wind()
		
	def use_ammo(self):
		if self.ammo - 1 < 0:
			pass
		else: self.ammo -= 1
		
	def lose_wind(self):
		self.wind -= int(con_input("Wind damage"))
		
	def toggle_stun(self):
		self.stun = not self.stun
		
	def reload(self):
		self.ammo += 1
		
	def clear(self):
		self.active = False
		self.minion = False

def clear_all():
	global grid
	grid = [[Unit() for y in range(GRID_COLS)] for x in range(GRID_ROWS)]
	
# Process keyboard input
def act(key):
	global activex, activey
# Grid movement
	if libt.console_is_key_pressed(libt.KEY_UP):
		if grid[activex][activey - 1].minion == True or activey % 2 != 0:
			step = 1
		else:
			step = 2
		if activey - step >= 0:
			activey -= step
	elif libt.console_is_key_pressed(libt.KEY_DOWN):
		try:
			if grid[activex][activey + 1].minion == True or activey % 2 != 0:
				step = 1
			else:
				step = 2
			if activey + step <= GRID_ROWS - 1:
				activey += step
		except IndexError:
			pass
	elif libt.console_is_key_pressed(libt.KEY_LEFT):
		if grid[activex - 1][activey].minion == True or activey % 2 != 0:
			step = 1
		else:
			step = 2
		if activex - step >= 0:
			activex -= step
	elif libt.console_is_key_pressed(libt.KEY_RIGHT):
		try:
			if grid[activex + 1][activey].minion == True or activey % 2 != 0:
				step = 1
			else:
				step = 2
			if activex + step <= GRID_COLS - 1:
				activex += step
		except IndexError:
			pass
	if not grid[activex][activey].minion and not activex % 2 == 0:
		activex -= 1
	if not grid[activex][activey].minion and not activey % 2 == 0:
		activey -= 1
# Other commands	
	elif chr(key.c) == 'a':
		name = con_input("Name")
		if name == "":
			name = None
		wind = con_input("Wind")
		if wind == "":
			wind = None
		else: wind = int(wind)
		ammo = con_input("Ammo")
		if ammo == "":
			ammo = None
		else: ammo = int(ammo)
		size = con_input("Size")
		if size == "":
			size = 6
		else: size = int(size)
		grid[activex][activey] = Unit(True, name, False, wind, ammo, size)
	elif chr(key.c) == 'm':
		num = 0
		while num < 2 or num > 16:
			num = int(con_input("Number of minions"))
		add_minions(num)
	elif chr(key.c) == 's':
		if not grid[activex][activey].ammo == None:
			grid[activex][activey].use_ammo()
	elif chr(key.c) == 'r':
		if not grid[activex][activey].ammo == None:
			grid[activex][activey].reload()
	elif chr(key.c) == 'w':
		if grid[activex][activey].minion == False:
			loc = choose_loc()
		else: loc = "guts"
		dam = int(con_input("Damage"))
		grid[activex][activey].wound(loc, dam)
	elif chr(key.c) == 'i':
		if not grid[activex][activey].wind == None:
			grid[activex][activey].lose_wind()
	elif chr(key.c) == 'z':
		grid[activex][activey].toggle_stun()
	elif chr(key.c) == 'c':
		grid[activex][activey].clear()
	elif chr(key.c) == 'q':
		clear_all()
	
# Hit Location list
def choose_loc():
	libt.console_print_frame(0, SCREEN_WIDTH // 2 - 10, SCREEN_HEIGHT // 2 - 8, 20, 17)
	libt.console_print_frame(0, SCREEN_WIDTH // 2 - 9, SCREEN_HEIGHT // 2 - 7, 18, 15)
	libt.console_hline(0, SCREEN_WIDTH // 2 - 6, SCREEN_HEIGHT // 2 - 8, 10, libt.BKGND_SET)
	libt.console_hline(0, SCREEN_WIDTH // 2 - 6, SCREEN_HEIGHT // 2 - 7, 10, libt.BKGND_SET)
	libt.console_print(0, SCREEN_WIDTH // 2 - 7, SCREEN_HEIGHT // 2 - 5, "1. Head")
	libt.console_print(0, SCREEN_WIDTH // 2 - 7, SCREEN_HEIGHT // 2 - 3, "2. Guts")
	libt.console_print(0, SCREEN_WIDTH // 2 - 7, SCREEN_HEIGHT // 2 - 1, "3. Left arm")
	libt.console_print(0, SCREEN_WIDTH // 2 - 7, SCREEN_HEIGHT // 2 + 1, "4. Right arm")
	libt.console_print(0, SCREEN_WIDTH // 2 - 7, SCREEN_HEIGHT // 2 + 3, "5. Left leg")
	libt.console_print(0, SCREEN_WIDTH // 2 - 7, SCREEN_HEIGHT // 2 + 5, "6. Right leg")

	libt.console_flush()
	command = libt.console_wait_for_keypress(True)
	while not command.vk == libt.KEY_ENTER:
		if command.vk == libt.KEY_1:
			return "head"
		elif command.vk == libt.KEY_2:
			return "guts"
		elif command.vk == libt.KEY_3:
			return "lArm"
		elif command.vk == libt.KEY_4:
			return "rArm"
		elif command.vk == libt.KEY_5:
			return "lLeg"
		elif command.vk == libt.KEY_6:
			return "rLeg"
		command = libt.console_wait_for_keypress(True)

# Define offscreen consoles
frame = libt.console_new(27,11)
libt.console_set_default_background(frame, libt.black)
libt.console_set_default_foreground(frame, libt.yellow)
libt.console_clear(frame)
libt.console_set_char(frame, 1, 1, libt.CHAR_DNW)
libt.console_set_char(frame, 25, 1, libt.CHAR_DNE)
libt.console_set_char(frame, 1, 10, libt.CHAR_DSW)
libt.console_set_char(frame, 25, 10, libt.CHAR_DSE)
libt.console_set_char(frame, 2, 1, libt.CHAR_HLINE)
libt.console_set_char(frame, 1, 2, libt.CHAR_VLINE)
libt.console_set_char(frame, 24, 1, libt.CHAR_HLINE)
libt.console_set_char(frame, 25, 2, libt.CHAR_VLINE)
libt.console_set_char(frame, 2, 10, libt.CHAR_HLINE)
libt.console_set_char(frame, 1, 9, libt.CHAR_VLINE)
libt.console_set_char(frame, 24, 10, libt.CHAR_HLINE)
libt.console_set_char(frame, 25, 9, libt.CHAR_VLINE)

minionframe = libt.console_new(14,6)
libt.console_set_default_background(minionframe, libt.black)
libt.console_set_default_foreground(minionframe, libt.yellow)
libt.console_clear(minionframe)
libt.console_set_char(minionframe, 2, 1, libt.CHAR_NW)
libt.console_set_char(minionframe, 13, 1, libt.CHAR_NE)
libt.console_set_char(minionframe, 2, 5, libt.CHAR_SW)
libt.console_set_char(minionframe, 13, 5, libt.CHAR_SE)

unitcon = libt.console_new(28,12)
libt.console_set_default_background(unitcon, libt.black)
libt.console_set_default_foreground(unitcon, libt.lightest_grey)
libt.console_clear(unitcon)
libt.console_print_frame(unitcon, 2, 2, 23, 8)
libt.console_hline(unitcon, 4, 2, 19, libt.BKGND_SET)
libt.console_print(unitcon, 4, 4, "Head:    O  Guts:")
libt.console_print(unitcon, 4, 5, "LArm:   / \ RArm:")
libt.console_print(unitcon, 4, 6, "LLeg:   / \ RLeg:")
libt.console_print(unitcon, 4, 8, "Wind:       Ammo:")
libt.console_set_char(unitcon, 13, 5, libt.CHAR_CHECKBOX_UNSET)

minioncon = libt.console_new(14,6)
libt.console_set_default_background(minioncon, libt.black)
libt.console_set_default_foreground(minioncon, libt.lightest_grey)
libt.console_clear(minioncon)
libt.console_print(minioncon, 3, 2, "Guts:")
libt.console_print(minioncon, 3, 3, "Wind:")
libt.console_print(minioncon, 3, 4, "Ammo:")

stunmarker = libt.console_new(27,11)
libt.console_set_default_background(stunmarker, libt.purple)
libt.console_set_default_foreground(stunmarker, libt.white)
libt.console_set_key_color(stunmarker, libt.purple)
libt.console_clear(stunmarker)
libt.console_set_default_background(stunmarker, libt.dark_red)
libt.console_rect(stunmarker, 3, 7, 21, 1, False, libt.BKGND_SET)
libt.console_print(stunmarker, 11, 7, "STUN")

def update_consoles():
	libt.console_clear(0)
	if not minionmode:
		if not grid[activex][activey].minion and not grid[activex + 1][activey].minion and not grid[activex][activey + 1].minion and not grid[activex + 1][activey + 1].minion:
			libt.console_blit(frame, 0, 0, 0, 0, 0, activex * COL_SIZE, activey * ROW_SIZE, 1.0, 0.0)
		else:
			libt.console_blit(minionframe, 0, 0, 0, 0, 0, activex * COL_SIZE, activey * ROW_SIZE)
	for y in range(GRID_COLS):
		for x in range(GRID_COLS):
			if grid[x][y].active:
				if not grid[x][y].minion:
				# Unit
					libt.console_blit(unitcon, 0, 0, 0, 0, 0, x * COL_SIZE, y * ROW_SIZE, 1.0, 0)
					if not grid[x][y].name == None:
						libt.console_print_ex(0, x * COL_SIZE + 13, y * ROW_SIZE + 2, libt.BKGND_NONE, libt.CENTER, " " + grid[x][y].name[:17] + " ")
					libt.console_print(0, x * COL_SIZE + 11, y * ROW_SIZE + 9, " (" + str(grid[x][y].size) + ") ")
				# Wound numbers
					libt.console_set_char(0, x * COL_SIZE + 10, y * ROW_SIZE + 4, str(grid[x][y].wounds['head']))
					libt.console_set_char(0, x * COL_SIZE + 10, y * ROW_SIZE + 5, str(grid[x][y].wounds['lArm']))
					libt.console_set_char(0, x * COL_SIZE + 10, y * ROW_SIZE + 6, str(grid[x][y].wounds['lLeg']))
					libt.console_set_char(0, x * COL_SIZE + 22, y * ROW_SIZE + 4, str(grid[x][y].wounds['guts']))
					libt.console_set_char(0, x * COL_SIZE + 22, y * ROW_SIZE + 5, str(grid[x][y].wounds['rArm']))
					libt.console_set_char(0, x * COL_SIZE + 22, y * ROW_SIZE + 6, str(grid[x][y].wounds['rLeg']))
				# Wind & Ammo
					if not grid[x][y].wind == None:
						libt.console_print(0, x * COL_SIZE + 10, y * ROW_SIZE + 8, str(grid[x][y].wind))
					else:
						libt.console_print(0, x * COL_SIZE + 10, y * ROW_SIZE + 8, str('-'))
					if not grid[x][y].ammo == None:
						libt.console_print(0, x * COL_SIZE + 22, y * ROW_SIZE + 8, str(grid[x][y].ammo))
					else:
						libt.console_print(0, x * COL_SIZE + 22, y * ROW_SIZE + 8, str('-'))
				# Wound colors
					colors = [libt.lightest_grey, libt.yellow, libt.orange, libt.dark_flame, libt.darker_red, libt.darkest_grey]
					libt.console_set_char_foreground(0, x * COL_SIZE + 13, y * ROW_SIZE + 4, colors[grid[x][y].wounds['head']])
					libt.console_set_char_foreground(0, x * COL_SIZE + 12, y * ROW_SIZE + 5, colors[grid[x][y].wounds['lArm']])
					libt.console_set_char_foreground(0, x * COL_SIZE + 12, y * ROW_SIZE + 6, colors[grid[x][y].wounds['lLeg']])
					libt.console_set_char_foreground(0, x * COL_SIZE + 13, y * ROW_SIZE + 5, colors[grid[x][y].wounds['guts']])
					libt.console_set_char_foreground(0, x * COL_SIZE + 14, y * ROW_SIZE + 5, colors[grid[x][y].wounds['rArm']])
					libt.console_set_char_foreground(0, x * COL_SIZE + 14, y * ROW_SIZE + 6, colors[grid[x][y].wounds['rLeg']])
				# Stun
					if grid[x][y].stun:
						libt.console_blit(stunmarker, 0, 0, 0, 0, 0, x * COL_SIZE, y * ROW_SIZE)
				else:
				# Minion
					libt.console_blit(minioncon, 0, 0, 0, 0, 0, x * COL_SIZE, y * ROW_SIZE, 1.0, 0)
					libt.console_print_ex(0, x * COL_SIZE + 8, y * ROW_SIZE + 1, libt.BKGND_NONE, libt.CENTER, grid[x][y].name)
					libt.console_print(0, x * COL_SIZE + 7, y * ROW_SIZE + 5, "(" + str(grid[x][y].size) + ")")
					if not grid[x][y].wind == None:
						libt.console_print(0, x * COL_SIZE + 10, y * ROW_SIZE + 3, str(grid[x][y].wind))
					else:
						libt.console_print(0, x * COL_SIZE + 10, y * ROW_SIZE + 3, str('-'))
					if not grid[x][y].ammo == None:
						libt.console_print(0, x * COL_SIZE + 10, y * ROW_SIZE + 4, str(grid[x][y].ammo))
					else:
						libt.console_print(0, x * COL_SIZE + 10, y * ROW_SIZE + 4, str('-'))
					colors = [libt.lightest_grey, libt.yellow, libt.orange, libt.dark_flame, libt.darker_red, libt.darkest_grey]
					libt.console_put_char_ex(0, x * COL_SIZE + 10, y * ROW_SIZE + 2, str(grid[x][y].wounds['guts']), colors[grid[x][y].wounds['guts']], libt.black)
					if grid[x][y].stun:
						libt.console_blit(stunmarker, 10, 7, 6, 1, 0, x * COL_SIZE + 5, y * ROW_SIZE + 5)
	libt.console_print_ex(0, SCREEN_WIDTH // 2, 49, libt.BKGND_NONE, libt.CENTER, 'a: Add Unit  m: Add Minions  s: Shoot  r: Reload  w: Wound  i: Wind Damage  z: Stun  c: Clear  q: Clear All')
	libt.console_flush()
	
# Input line on console
def con_input(query):
	string = ""
	update_consoles()
	libt.console_set_default_background(0, libt.black)
	libt.console_set_default_foreground(0, libt.white)
	libt.console_print_frame(0, 46 - len(query), SCREEN_HEIGHT // 2 - 3, 32, 7, True, libt.BKGND_SET, None)
	libt.console_print_frame(0, 47 - len(query), SCREEN_HEIGHT // 2 - 2, 30, 5, True, libt.BKGND_NONE, None)
	libt.console_print_ex(0, 50, SCREEN_HEIGHT // 2, libt.BKGND_NONE, libt.RIGHT, query + ":")
	libt.console_flush()
	command = libt.console_wait_for_keypress(True)
	while not command.vk == libt.KEY_ENTER:
		if len(string) > 15 or libt.console_is_key_pressed(libt.KEY_BACKSPACE):
			string = string[:-1]
		if libt.console_is_key_pressed(libt.KEY_BACKSPACE):
			libt.console_set_char(0, len(string) + 53, SCREEN_HEIGHT // 2, " ")
		elif libt.console_is_key_pressed(libt.KEY_CHAR) or libt.console_is_key_pressed(libt.KEY_0) or libt.console_is_key_pressed(libt.KEY_1) or libt.console_is_key_pressed(libt.KEY_2) or libt.console_is_key_pressed(libt.KEY_3) or libt.console_is_key_pressed(libt.KEY_4) or libt.console_is_key_pressed(libt.KEY_5) or libt.console_is_key_pressed(libt.KEY_6) or libt.console_is_key_pressed(libt.KEY_7) or libt.console_is_key_pressed(libt.KEY_8) or libt.console_is_key_pressed(libt.KEY_9):
			if libt.console_is_key_pressed(libt.KEY_SHIFT):
				letter = chr(command.c - 32)
			else:
				letter = chr(command.c)
			libt.console_set_char(0, len(string) + 53, SCREEN_HEIGHT // 2, letter)
			libt.console_set_char_foreground(0, len(string) + 53, SCREEN_HEIGHT // 2, libt.lightest_grey)
			string += letter
		libt.console_flush()
		command = libt.console_wait_for_keypress(True)
	libt.console_set_default_background(0, libt.black)
	libt.console_set_default_foreground(0, libt.lightest_grey)
	return string
	
def add_minions(num):
	global minionmode
	minionmode = True
	minionrow = 0
	minioncol = 0
	update_consoles()
	libt.console_put_char_ex(0, minioncol * COL_SIZE * 4, minionrow * ROW_SIZE + 3, ">", libt.yellow, libt.black)
	libt.console_flush()
	command = libt.console_wait_for_keypress(True)
	while not command.vk == libt.KEY_ENTER and not command.vk == libt.KEY_ESCAPE:
		if num <= 4:
			if command.vk == libt.KEY_UP:
				minionrow -= 1
			elif command.vk == libt.KEY_DOWN:
				minionrow += 1
			if minionrow > GRID_ROWS - 1:
				minionrow = GRID_ROWS - 1
		else:
			if command.vk == libt.KEY_UP:
				minionrow -= 2
			elif command.vk == libt.KEY_DOWN:
				minionrow += 2
			if minionrow > GRID_ROWS - 2:
				minionrow = GRID_ROWS - 2
		if minionrow < 0:
			minionrow = 0
		if num <= 8:
			if command.vk == libt.KEY_LEFT:
				minioncol -= 1
			elif command.vk == libt.KEY_RIGHT:
				minioncol += 1
			if minioncol < 0:
				minioncol = 0
			elif minioncol > GRID_COLS // 4 - 1:
				minioncol = GRID_COLS // 4 - 1
		update_consoles()
		libt.console_put_char_ex(0, minioncol * COL_SIZE * 4, minionrow * ROW_SIZE + 3, ">", libt.yellow, libt.black)
		libt.console_flush()
		command = libt.console_wait_for_keypress(True)
	if command.vk == libt.KEY_ENTER:
		name = con_input("Name")
		#if name == "":
		#	name = None
		wind = con_input("Wind")
		if wind == "":
			wind = None
		else: wind = int(wind)
		ammo = con_input("Ammo")
		if ammo == "":
			ammo = None
		else: ammo = int(ammo)
		size = con_input("Size")
		if size == "":
			size = 6
		else: size = int(size)
		if num <= 4:
			for n in range(num):
				grid[minioncol * 4 + n][minionrow] = Unit(True, name[:6] + str(n + 1), True, wind, ammo, size)
		elif num <= 8:
			for n in range(4):
				grid[minioncol * 4 + n][minionrow] = Unit(True, name[:6] + str(n + 1), True, wind, ammo, size)
			for n in range(num - 4):
				grid[minioncol * 4 + n][minionrow + 1] = Unit(True, name[:6] + str(n + 5), True, wind, ammo, size)
		else:
			for n in range(8):
				grid[n][minionrow] = Unit(True, name[:6] + str(n + 1), True, wind, ammo, size)
			for n in range(num - 8):
				grid[n][minionrow + 1] = Unit(True, name[:6] + str(n + 9), True, wind, ammo, size)
	minionmode = False
	
clear_all()
libt.console_print_ex(0, 50, SCREEN_WIDTH // 2, libt.BKGND_NONE, libt.CENTER, 'a: Add Unit  r: Reload  s: Shoot  m: Add Minions  w: Wound  i: Wind Damage  z: Stun')
# Main loop		
while not libt.console_is_window_closed():
	update_consoles()
	command = libt.console_wait_for_keypress(True)
	if command.vk == libt.KEY_ESCAPE:
		break
	act(command)