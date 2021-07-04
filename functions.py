import pygame, time
from pygame import constants
from pygame.locals import KEYDOWN, K_RETURN
clock = pygame.time.Clock()

def palette_swap(surface, old_color, new_color) -> pygame.Surface:
	"""Replace a color from an surface to another color.\
	Will not work with a sprite with black pixels, it will make them transparent."""
	img_copy = pygame.Surface((32, 32))
	# rempli l'image de la nouvelle couleur
	img_copy.fill(new_color)
	# supprime la couleur qu'on veut remplacer dans l'image
	surface.set_colorkey(old_color)
	# copy l'image sur le fond de la nouvelle couleur
	img_copy.blit(surface, (0, 0))
	# make all the black pixels of the surface transparent
	img_copy.set_colorkey(pygame.Color("black"))
	return img_copy

def outfile_read(file: str) -> str:
	"""open the output file and return the text in a string."""
	# open the output file for riding
	outfile = open(file, "r")
	# take the text of the output file
	text = outfile.read()
	# close the output file
	outfile.close()
	# return the text
	return text

def outfile_read_list(file: str):
	"""Open the output file and return the text in a list.\
	Each lines will be in a different list indice."""
	# open the output file for riding
	outfile = open(file, "r")
	# take lines of the output file in a list
	list_text = outfile.readlines()
	# close the output file
	outfile.close()
	# return the list
	return list_text

def return_commands() -> str:
	"""Return the name of the key you pressed as a string and as a pygame.key."""
	loop = True
	while loop:
		for event in pygame.event.get():
			if event.type == KEYDOWN and event.key != K_RETURN:
				return event.key, pygame.key.name(event.key)

def update_fps(font, color:str="Coral"):
	"""Get fps and render it in the font and color you want."""
	fps = str(int(clock.get_fps()))
	fps_text = font.render(fps, 1, pygame.Color(color))
	return fps_text

def dtime(fps:int, last_time: float):
	dt = time.time() - last_time
	dt *= fps
	last_time = time.time()
	return(dt, last_time)

def get_level(level:int, list_stage:list):
	file = list_stage[level]
	return file

def get_stage(world:int, level:int):
	if world == 1:
		stage = "A" + str(level)
		fps = 30
	elif world == 2:
		stage = "B" + str(level)
		fps = 33
	elif world == 3:
		stage = "C" + str(level)
		fps = 36
	elif world == 4:
		stage = "D" + str(level)
		fps = 40
	elif world == 5:
		stage = "E" + str(level)
		fps = 45
	elif world == 6:
		stage = "F" + str(level)
		fps = 50
	elif world == 7:
		stage = "G" + str(level)
		fps = 55
	else:
		stage = "PAC"

	if world >= 8:
		fps = 60
	return fps, stage

def level_up(world, level:int, list_stage:list):
	file = get_level(level, list_stage)
	fps, stage = get_stage(world, level+1)

	if level == len(list_stage)-1:
		level = 0
		world += 1
	else:
		level += 1
	return world, level, stage, file, fps

"""def render(text:str, font, color):
	return font.render(text, 0, color)"""

def ghost(body, eye:list, animation:list, old_color, new_color:constants, gum=0):
	list_image = []
	ghost = pygame.display.set_mode((16, 16))
	for eyes in eye:
		for animations in animation:
			ghost = pygame.image.load(body).convert()
			ghost.blit(pygame.image.load(eyes).convert_alpha(), (0, 0))
			ghost.blit(pygame.image.load(animations).convert_alpha(), (0, 0))
			if gum != 0:
				ghost.blit(pygame.image.load(gum).convert_alpha(), (0, 0))
			ghost = pygame.transform.scale(ghost, (32, 32))
			ghost = palette_swap(ghost, old_color, new_color)
			list_image.append(ghost)
	return list_image

def hiscore_list() -> list:
	"""Return a list of hight-score."""
	file_hiscore = outfile_read("data/HISCORE/HISCORE.txt")
	return [word for word in file_hiscore.split() if word.isdigit()]

def fps_display(show, window, font):
	if show == True:
		window.blit(update_fps(font), (0, 0))