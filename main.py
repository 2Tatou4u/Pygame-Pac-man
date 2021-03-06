#--------------------------------------------------------# TO DO #--------------------------------------------------------#
"""
- à retravailler : utilisation du système de réniatilisation Player | Ghost .initialisation() ET fonctionnement de Player | Ghost .initialisation()

# Pas important
- Améliorer death_display de la class Pac
- Minimiser l'utilisation de variable global comme score ou de niveau.
- Retravailler les collisions (mauvaises utilisation ainsi que mauvais équilibrage)
- La fonction mort des fantômes dépends du spawn du fantôme shadow (ce qui n'est pas bon) à modifier.
- Retravailler la class Maze
- Terminer la fonctionnaliter de création de niveau (sûrement créer une nouvelle class à la place d'utiliser Maze)
"""
#-------------------------------------------------------------------------------------------------------------------------#

import pygame, math, random, sys
from pygame.draw import circle, rect
# setup pygame functions
from pygame.locals import *
from pygame.sprite import collide_circle
pygame.init()

pygame.key.set_repeat()
clock = pygame.time.Clock()
# setup game functions
from functions import *

BLACK = pygame.Color("black")
WHITE = pygame.Color("white")
YELLOW = pygame.Color("yellow")
infoPC = pygame.display.Info()
# titre ----------------------------------------------------------------------------------------------------------------------------------- #
pygame.display.set_caption("PAC-MAN")
# icone ----------------------------------------------------------------------------------------------------------------------------------- #
pygame.display.set_icon(pygame.image.load("data/image/icone.png"))
# fenetre --------------------------------------------------------------------------------------------------------------------------------- #
window = pygame.display.set_mode((640, 640))
# paramètre démarrage --------------------------------------------------------------------------------------------------------------------- #
level = score = show_fps = 0
world = 1
# text ------------------------------------------------------------------------------------------------------------------------------------ #
# text font
font_10 = pygame.font.Font("data/emulogic.ttf", 13)
font_8 = pygame.font.Font("data/emulogic.ttf", 12)
font_13 = pygame.font.Font("data/emulogic.ttf", 13)
pacfont = pygame.font.Font("data/pac.ttf", 60)
# text assignement
text_pac_logo = pacfont.render("PAC.MAN", 0, WHITE)
# pause text
text_pause_replay = font_8.render("retry", 0, WHITE)
text_pause_menu = font_8.render("menu", 0, WHITE)
text_pause_quit = font_8.render("quit", 0, WHITE)

text_ready = font_10.render("ready!", 0, YELLOW)
# home text
text_home_1player = font_10.render("1 player", 0, WHITE)
text_home_HISCORE = font_10.render("hi-score", 0, WHITE)
text_home_edit = font_10.render("level editor", 0, WHITE)
text_home_option = font_10.render("option", 0, WHITE)
# option text
text_option_commands = font_10.render("commands", 0, WHITE)
text_commands_input = font_10.render("input", 0, WHITE)
# text function hiscore
text_hiscore_score = font_13.render("SCORE", 0, WHITE)
text_hiscore_name = font_13.render("NAME", 0, WHITE)
text_hiscore_round = font_13.render("STAGE", 0, WHITE)
text_hiscore_podium_list = []
text_hiscore_podium_list.append(font_13.render("1ST", 0, WHITE))
text_hiscore_podium_list.append(font_13.render("2ND", 0, WHITE))
text_hiscore_podium_list.append(font_13.render("3RD", 0, WHITE))
text_hiscore_podium_list.append(font_13.render("4TH", 0, WHITE))
text_hiscore_podium_list.append(font_13.render("5TH", 0, WHITE))
text_hiscore_podium_list.append(font_13.render("6TH", 0, WHITE))
text_hiscore_podium_list.append(font_13.render("7TH", 0, WHITE))
text_hiscore_podium_list.append(font_13.render("8TH", 0, WHITE))
text_hiscore_podium_list.append(font_13.render("9TH", 0, WHITE))

file_hiscore_score = hiscore_list()
# sound ----------------------------------------------------------------------------------------------------------------------------------- #
"""sound_game_start = pygame.mixer.Sound("data/sound/game_start.wav")"""
"""sound_pac_dot = pygame.mixer.Sound("data/sound/pacman_eat_dot.wav")"""
# level ----------------------------------------------------------------------------------------------------------------------------------- #
list_stage = []
#list_stage.append("data/map/ia")
list_stage.append("data/map/maze1")
list_stage.append("data/map/maze2")
#list_stage.append("data/map/map2_beta")
list_stage.append("data/map/maze3")
list_stage.append("data/map/maze4")
#list_stage.append("data/map/maze5")
# sprite ---------------------------------------------------------------------------------------------------------------------------------- #
# bonus
image_bonus = []
image_bonus.append(pygame.transform.scale(pygame.image.load("data/image/bonus/cherrys.png").convert_alpha(), (32, 32))) 		# cherrys
image_bonus.append(pygame.transform.scale(pygame.image.load("data/image/bonus/strawberry.png").convert_alpha(), (32, 32))) 		# strawberry
image_bonus.append(pygame.transform.scale(pygame.image.load("data/image/bonus/orange.png").convert_alpha(), (32, 32))) 			# orange
image_bonus.append(pygame.transform.scale(pygame.image.load("data/image/bonus/apple.png").convert_alpha(), (32, 32))) 			# apple
image_bonus.append(pygame.transform.scale(pygame.image.load("data/image/bonus/watermelon.png").convert_alpha(), (32, 32)))		# watermelon
image_bonus.append(pygame.transform.scale(pygame.image.load("data/image/bonus/key.png").convert_alpha(), (32, 32))) 			# key
# pac-man image animation
image_pac = []
image_pac.append(pygame.image.load("data/image/pac/pac0.png").convert_alpha())				# full
image_pac.append(pygame.image.load("data/image/pac/pac1.png").convert_alpha())				# walk 1
image_pac.append(pygame.image.load("data/image/pac/pac2.png").convert_alpha())				# walk 2
image_pac.append(pygame.image.load("data/image/pac/pac1.png").convert_alpha())				# walk 1
image_pac.append(pygame.image.load("data/image/pac/pac3.png").convert_alpha())				# end 1
image_pac.append(pygame.image.load("data/image/pac/pac4.png").convert_alpha())				# end 2
image_pac.append(pygame.image.load("data/image/pac/pac5.png").convert_alpha())				# end 3
image_pac.append(pygame.image.load("data/image/pac/pac6.png").convert_alpha())				# end 4
image_pac.append(pygame.image.load("data/image/pac/pac7.png").convert_alpha())				# end 5
image_pac.append(pygame.image.load("data/image/pac/pac8.png").convert_alpha())				# end 6
image_pac.append(pygame.image.load("data/image/pac/pac9.png").convert_alpha())				# end 7
image_pac.append(pygame.image.load("data/image/pac/pacA.png").convert_alpha())				# end 8
# list des yeux/animation des fantômes
list_gum_eye = []
list_gum_eye.append("data/image/ghost/ghost_gum_eye.png")
list_eye = []
list_eye.append("data/image/ghost/ghost_eye_right.png")
list_eye.append("data/image/ghost/ghost_eye_left.png")
list_eye.append("data/image/ghost/ghost_eye_up.png")
list_eye.append("data/image/ghost/ghost_eye_down.png")
list_animation = []
list_animation.append("data/image/ghost/ghost_moove0.png")
list_animation.append("data/image/ghost/ghost_moove1.png")
list_animation.append("data/image/ghost/ghost_moove2.png")
list_animation.append("data/image/ghost/ghost_moove3.png")
list_animation.append("data/image/ghost/ghost_moove4.png")
ghost_eye_right = pygame.transform.scale(pygame.image.load("data/image/ghost/ghost_eye_right.png").convert_alpha(), (32, 32))
ghost_eye_left = pygame.transform.scale(pygame.image.load("data/image/ghost/ghost_eye_left.png").convert_alpha(), (32, 32))
ghost_eye_up = pygame.transform.scale(pygame.image.load("data/image/ghost/ghost_eye_up.png").convert_alpha(), (32, 32))
ghost_eye_down = pygame.transform.scale(pygame.image.load("data/image/ghost/ghost_eye_down.png").convert_alpha(), (32, 32))
image_gum = ghost("data/image/ghost/ghost_body.png", list_gum_eye, list_animation, (255, 120, 233), pygame.Color("blue"), "data/image/ghost/ghost_gum_mouth.png")
list_gum_end = []
for image in image_gum:
	gum_end = palette_swap(image, pygame.Color("blue"), WHITE)
	gum_end = palette_swap(gum_end, (255, 192, 150), (255, 71, 71))
	list_gum_end.append(gum_end)
# gum
image_gum = ghost("data/image/ghost/ghost_body.png", list_gum_eye, list_animation, (255, 120, 233), (25, 25, 166), "data/image/ghost/ghost_gum_mouth.png")
# inky
image_inky = ghost("data/image/ghost/ghost_body.png", list_eye, list_animation, (255, 120, 233), pygame.Color("cyan"))
# clyde
image_clyde = ghost("data/image/ghost/ghost_body.png", list_eye, list_animation, (255, 120, 233), pygame.Color("darkorange"))
# shadow
image_shadow = ghost("data/image/ghost/ghost_body.png", list_eye, list_animation, (255, 120, 233), pygame.Color("red"))
# pinky
image_pinky = ghost("data/image/ghost/ghost_body.png", list_eye, list_animation, (255, 120, 233), pygame.Color("violet"))
# sprite groups
group_wall = pygame.sprite.RenderUpdates()
group_wall_spawn = pygame.sprite.RenderUpdates()
group_wall_spawn_special = pygame.sprite.RenderUpdates()
group_dot = pygame.sprite.RenderUpdates()
group_gum = pygame.sprite.RenderUpdates()
group_bonus = pygame.sprite.Group()
# commands
command_up = K_UP
command_down = K_DOWN
command_right = K_RIGHT
command_left = K_LEFT
command_return = K_SPACE
command_escape = K_ESCAPE

class Maze:
	def __init__(self):
		# structure settings 
		self.maze_width = self.maze_length = 0
		self.dot = 0
		self.bonus_level = self.inky = self.shadow = self.pokey = self.pinky = False

	def maze_scale(self):
		self.maze_width = len(self.structure[0])
		self.maze_length = len(self.structure)
		
	def read_file(self, file):
		self.structure = []
		# open the file
		with open(file) as file:
			# on parcourt chaque lignes de textes
			for ligne in file:
				# création de la liste comportant une ligne du niveau
				ligne_niveau = []
				# on parcourt chaque caractères du textes de la ligne
				for sprite in ligne:
					# fait en sorte que la liste ne contient pas de saut de ligne
					if sprite != '\n':
						# ajouts des charactères dans chaque liste
						ligne_niveau.append(sprite)
				# on ajoute la ligne à la liste du niveau
				self.structure.append(ligne_niveau)
		self.maze_scale()

	def maze_editor(self, maze, window):
		self.structure = maze
		self.display_maze(window)

	def display_maze(self, window):
		global bonus

		# vide les groupes
		group_wall.empty()
		group_wall_spawn.empty()
		group_wall_spawn_special.empty()
		group_dot.empty()
		group_gum.empty()
		group_bonus.empty()
		self.dot = 0
		self.maze_width = len(self.structure[0])
		self.maze_length = len(self.structure)
		# parcourt la liste du niveau
		a = 0
		for ligne in self.structure:
			b = 0
			# parcour les listes de la structure
			for sprite in ligne:
				# calcul de la position
				x = b * 32
				y = a * 32
			# vérification de l'élément
				"""	m u d r q p l v i s a b y z
					g * bonus
					! ? % : + - ="""
				# wall
				if sprite == "m":
					
					wall = Sprite(x, y)

					if b != self.maze_width - 1 and b != 0 and a != self.maze_length-1 and a != 0:

						if self.structure[a][b + 1] == "m" and self.structure[a][b - 1] == "m" and self.structure[a - 1][b] == "m" and self.structure[a + 1][b] == "m":
							wall.create_sprite("wall_m")
						elif self.structure[a][b + 1] != "m" and self.structure[a][b - 1] != "m" and self.structure[a - 1][b] != "m" and self.structure[a + 1][b] != "m":	
							wall.create_sprite("wall_o")

						elif self.structure[a][b + 1] == "m" and self.structure[a][b - 1] == "m" and self.structure[a - 1][b] == "m":
							wall.create_sprite("wall_d")
						elif self.structure[a][b + 1] == "m" and self.structure[a][b - 1] == "m" and self.structure[a + 1][b] == "m":
							wall.create_sprite("wall_u")
						elif self.structure[a][b + 1] == "m" and self.structure[a - 1][b] == "m" and self.structure[a + 1][b] == "m":
							wall.create_sprite("wall_l")
						elif self.structure[a][b - 1] == "m" and self.structure[a - 1][b] == "m" and self.structure[a + 1][b] == "m":
							wall.create_sprite("wall_r")

						elif self.structure[a][b + 1] == "m" and self.structure[a][b - 1] == "m":
							wall.create_sprite("wall_v")
						elif self.structure[a][b + 1] == "m" and self.structure[a - 1][b] == "m":
							wall.create_sprite("wall_y")
						elif self.structure[a][b + 1] == "m" and self.structure[a + 1][b] == "m":
							wall.create_sprite("wall_a")
						elif self.structure[a][b - 1] == "m" and self.structure[a - 1][b] == "m":
							wall.create_sprite("wall_z")
						elif self.structure[a][b - 1] == "m" and self.structure[a + 1][b] == "m":
							wall.create_sprite("wall_b")
						elif self.structure[a - 1][b] == "m" and self.structure[a + 1][b] == "m":
							wall.create_sprite("wall_w")

						elif self.structure[a][b + 1] == "m":
							wall.create_sprite("wall_i")
						elif self.structure[a][b - 1] == "m":
							wall.create_sprite("wall_s")
						elif self.structure[a + 1][b] == "m":
							wall.create_sprite("wall_p")
						elif self.structure[a - 1][b] == "m":
							wall.create_sprite("wall_q")
					
					elif b == self.maze_width - 1 and a != 0 and a != self.maze_length - 1:

						if self.structure[a][b - 1] == "m" and self.structure[a - 1][b] == "m" and self.structure[a + 1][b] == "m":
							wall.create_sprite("wall_m")
						elif self.structure[a][b - 1] != "m" and self.structure[a + 1][b] != "m" and self.structure[a - 1][b] != "m":
							wall.create_sprite("wall_i")

						elif self.structure[a][b - 1] == "m" and self.structure[a - 1][b] == "m":
							wall.create_sprite("wall_d")
						elif self.structure[a][b - 1] == "m" and self.structure[a + 1][b] == "m":
							wall.create_sprite("wall_u")
						elif self.structure[a - 1][b] == "m" and self.structure[a + 1][b] == "m":
							wall.create_sprite("wall_l")

						elif self.structure[a][b - 1] == "m":
							wall.create_sprite("wall_v")
						elif self.structure[a + 1][b] == "m":
							wall.create_sprite("wall_a")
						elif self.structure[a - 1][b] == "m":
							wall.create_sprite("wall_y")

					elif b == 0 and a != 0 and a != self.maze_length - 1:
						if self.structure[a][b + 1] == "m" and self.structure[a - 1][b] == "m" and self.structure[a + 1][b] == "m":
							wall.create_sprite("wall_m")

						elif self.structure[a][b + 1] != "m" and self.structure[a + 1][b] != "m" and self.structure[a - 1][b] != "m":
							wall.create_sprite("wall_s")

						elif self.structure[a][b + 1] == "m" and self.structure[a - 1][b] == "m":
							wall.create_sprite("wall_d")
						elif self.structure[a][b + 1] == "m" and self.structure[a + 1][b] == "m":
							wall.create_sprite("wall_u")
						elif self.structure[a - 1][b] == "m" and self.structure[a + 1][b] == "m":
							wall.create_sprite("wall_r")

						elif self.structure[a][b + 1] == "m":
							wall.create_sprite("wall_v")
						elif self.structure[a + 1][b] == "m":
							wall.create_sprite("wall_b")
						elif self.structure[a - 1][b] == "m":
							wall.create_sprite("wall_z")

					elif a == 0 and b != 0 and b != self.maze_width - 1:
						if self.structure[a][b + 1] == "m" and self.structure[a][b - 1] == "m" and self.structure[a + 1][b] == "m":
							wall.create_sprite("wall_m")

						elif self.structure[a][b + 1] != "m" and self.structure[a][b - 1] != "m" and self.structure[a + 1][b] != "m":
							wall.create_sprite("wall_q")

						elif self.structure[a][b + 1] == "m" and self.structure[a + 1][b] == "m":
							wall.create_sprite("wall_l")
						elif self.structure[a][b - 1] == "m" and self.structure[a + 1][b] == "m":
							wall.create_sprite("wall_r")
						elif self.structure[a][b + 1] == "m" and self.structure[a][b - 1] == "m":
							wall.create_sprite("wall_d")
						
						elif self.structure[a][b + 1] == "m":
							wall.create_sprite("wall_y")
						elif self.structure[a + 1][b] == "m":
							wall.create_sprite("wall_w")
						elif self.structure[a][b - 1] == "m":
							wall.create_sprite("wall_z")

					elif a == self.maze_length - 1 and b != 0 and b != self.maze_width - 1:
						if self.structure[a][b + 1] == "m" and self.structure[a][b - 1] == "m" and self.structure[a - 1][b] == "m":
							wall.create_sprite("wall_m")

						elif self.structure[a][b + 1] != "m" and self.structure[a][b - 1] != "m" and self.structure[a - 1][b] != "m":
							wall.create_sprite("wall_p")

						elif self.structure[a][b + 1] == "m" and self.structure[a - 1][b] == "m":
							wall.create_sprite("wall_l")
						elif self.structure[a][b - 1] == "m" and self.structure[a - 1][b] == "m":
							wall.create_sprite("wall_r")
						elif self.structure[a][b + 1] == "m" and self.structure[a][b - 1] == "m":
							wall.create_sprite("wall_u")
						
						elif self.structure[a][b + 1] == "m":
							wall.create_sprite("wall_a")
						elif self.structure[a - 1][b] == "m":
							wall.create_sprite("wall_w")
						elif self.structure[a][b - 1] == "m":
							wall.create_sprite("wall_b")

					elif a == 0 and b == 0:
						if self.structure[a + 1][b] == "m" and self.structure[a][b + 1] == "m":
							wall.create_sprite("wall_m")
						elif self.structure[a + 1][b] != "m" and self.structure[a][b + 1] != "m":
							wall.create_sprite("wall_z")
						elif self.structure[a + 1][b] == "m" and self.structure[a][b + 1] != "m":
							wall.create_sprite("wall_r")
						elif self.structure[a + 1][b] != "m" and self.structure[a][b + 1] == "m":
							wall.create_sprite("wall_d")

					elif a == self.maze_length-1 and b == 0:
						if self.structure[a - 1][b] == "m" and self.structure[a][b + 1] == "m":
							wall.create_sprite("wall_m")
						elif self.structure[a - 1][b] != "m" and self.structure[a][b + 1] != "m":
							wall.create_sprite("wall_b")
						elif self.structure[a - 1][b] == "m" and self.structure[a][b + 1] != "m":
							wall.create_sprite("wall_r")
						elif self.structure[a - 1][b] != "m" and self.structure[a][b + 1] == "m":
							wall.create_sprite("wall_u")

					elif a == 0 and b == self.maze_width-1:
						if self.structure[a + 1][b] == "m" and self.structure[a][b - 1] == "m":
							wall.create_sprite("wall_m")
						elif self.structure[a + 1][b] != "m" and self.structure[a][b - 1] != "m":
							wall.create_sprite("wall_y")
						elif self.structure[a + 1][b] == "m" and self.structure[a][b - 1] != "m":
							wall.create_sprite("wall_l")
						elif self.structure[a + 1][b] != "m" and self.structure[a][b - 1] == "m":
							wall.create_sprite("wall_d")

					elif a == self.maze_length-1 and b == self.maze_width-1:
						if self.structure[a - 1][b] == "m" and self.structure[a][b - 1] == "m":
							wall.create_sprite("wall_m")
						elif self.structure[a - 1][b] != "m" and self.structure[a][b - 1] != "m":
							wall.create_sprite("wall_a")
						elif self.structure[a - 1][b] == "m" and self.structure[a][b - 1] != "m":
							wall.create_sprite("wall_l")
						elif self.structure[a - 1][b] != "m" and self.structure[a][b - 1] == "m":
							wall.create_sprite("wall_u")

					group_wall.add(wall)

				# ghost-spawn-wall
				elif sprite == "s":

					spawn_wall = Sprite(x, y)

					if self.structure[a][b + 1] == "s" and self.structure[a][b - 1] == "s" or\
						self.structure[a][b + 1] == "s" and self.structure[a][b - 1] == "=" or\
							self.structure[a][b + 1] == "=" and self.structure[a][b - 1] == "s" or\
								self.structure[a][b + 1] == "=" and self.structure[a][b - 1] == "=":
						spawn_wall.create_sprite("!")
					elif self.structure[a + 1][b] == "s" and self.structure[a - 1][b] == "s" or\
						self.structure[a + 1][b] == "s" and self.structure[a - 1][b] == "=" or\
							self.structure[a + 1][b] == "=" and self.structure[a - 1][b] == "s" or\
								self.structure[a + 1][b] == "=" and self.structure[a - 1][b] == "=":
						spawn_wall.create_sprite("?")
					elif self.structure[a + 1][b] == "s" and self.structure[a][b + 1] == "s" or\
						self.structure[a + 1][b] == "s" and self.structure[a][b + 1] == "=":
						spawn_wall.create_sprite("+")
					elif self.structure[a + 1][b] == "s" and self.structure[a][b - 1] == "s" or\
						self.structure[a + 1][b] == "s" and self.structure[a][b - 1] == "=":
						spawn_wall.create_sprite("-")
					elif self.structure[a - 1][b] == "s" and self.structure[a][b + 1] == "s" or\
						self.structure[a - 1][b] == "s" and self.structure[a][b + 1] == "=":
						spawn_wall.create_sprite(":")
					elif self.structure[a - 1][b] == "s" and self.structure[a][b - 1] == "s" or\
						self.structure[a - 1][b] == "s" and self.structure[a][b - 1] == "=":
						spawn_wall.create_sprite("%")

					group_wall_spawn.add(spawn_wall)
			
				# special-wall
				# pas fini (problème si on place ce sprite aux bordures du niveau)
				elif sprite == "=":
					special_spawn_wall = Sprite(x, y)

					special_spawn_wall.create_sprite("=")

					group_wall_spawn_special.add(special_spawn_wall)

				# dot/gum
				elif sprite == "*":
					dot = Sprite(x, y)
					dot.create_sprite("dot")
					group_dot.add(dot)
					# calcul du nombre de point
					self.dot += 1
					if b != self.maze_width - 1:
						if self.structure[a][b + 1] == "*" or self.structure[a][b + 1] == "g":
							dot = Sprite(x + 16, y)
							dot.create_sprite("dot")
							group_dot.add(dot)
							self.dot += 1
					if a != self.maze_length - 1:
						if self.structure[a + 1][b] == "*" or self.structure[a + 1][b] == "g":
							dot = Sprite(x, y + 16)
							dot.create_sprite("dot")
							group_dot.add(dot)
							self.dot += 1
					if a != 0:
						if self.structure[a - 1][b] == "g":
							dot = Sprite(x, y - 16)
							dot.create_sprite("dot")
							group_dot.add(dot)
							self.dot += 1
					if a != 0:
						if self.structure[a][b - 1] == "g":
							dot = Sprite(x - 16, y)
							dot.create_sprite("dot")
							group_dot.add(dot)
							self.dot += 1
					#print(self.dot * 10 + 3050 * 4 + 100 + 300 + 500 + 700 + 1000 + 2000)

				elif sprite == "g":
					gum = Sprite(x, y)
					gum.create_sprite("gum")
					group_gum.add(gum)

				elif sprite == "b":
					bonus = Bonus(window, x, y)
					self.bonus_level = True
				
				# définition du spawn des montres (pas fini)
				elif sprite == "1":
					pac.initialize(x, y, window)
				elif sprite == "4":
					shadow.initialize(x, y, window)
					self.shadow = True
				elif sprite == "3":
					pinky.initialize(x, y, window)
					self.pinky = True
				elif sprite == "5":
					pokey.initialize(x, y, window)
					self.pokey = True
				elif sprite == "2":
					inky.initialize(x, y, window)
					self.inky = True
				b += 1
			a += 1

	def moove_availablity(self):
		moove_right = moove_left = moove_down = moove_up = False
		a = 0
		for ligne in self.structure:
			b = 0
			for sprite in ligne:
				if sprite == "1":
					if self.structure[a][b+1] != "m" and self.structure[a][b+1] != "s" and self.structure[a][b+1] != "=":
						moove_right = True
					else:
						moove_right = False
					if self.structure[a][b-1] != "m" and self.structure[a][b-1] != "s" and self.structure[a][b-1] != "=":
						moove_left = True
					else:
						moove_left = False
					if self.structure[a+1][b] != "m" and self.structure[a+1][b] != "s" and self.structure[a+1][b] != "=":
						moove_down = True
					else:
						moove_down = False
					if self.structure[a-1][b] != "m" and self.structure[a-1][b] != "s" and self.structure[a-1][b] != "=":
						moove_up = True
					else:
						moove_up = False
				b += 1
			a += 1

		return moove_right, moove_left, moove_down, moove_up

class Sprite(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.x = x
		self.y = y
		self.image = pygame.Surface([32, 32])
		self.rect = pygame.Rect(self.x, self.y, 32, 32)
		self.name = "False"
		self.timer = 0

	def create_sprite(self, name, update=False, full=0):
		if update == False:
			if level == 1:
				self.color_1 = pygame.Color("darkblue")
				self.color_2 = pygame.Color("lightgoldenrod1")
			elif level == 2:
				self.color_1 = pygame.Color("tan1")
				self.color_2 = pygame.Color("lightgoldenrod1")
			elif level == 3:
				self.color_1 = pygame.Color("olivedrab3")
				self.color_2 = pygame.Color("lightgoldenrod1")
			else:
				self.color_1 = pygame.Color("indianred1")
				self.color_2 = pygame.Color("lightgoldenrod1")
		else:
			self.color_1 = self.color_2 = self.color_update

		self.name = name

		if name == "wall_m":
			"window.fill((4, 2, 59), (0, 0, 32, 32))"
		# basic wall
		elif name == "wall_u":
			"window.fill((4, 2, 59), (0, 4, 32, 28))"
			self.image.fill(self.color_1, (0, 0, 32, 4))
		elif name == "wall_d":
			"self.image.fill((4, 2, 59), (0, 0, 32, 28))"
			self.image.fill(self.color_1, (0, 28, 32, 4))
		elif name == "wall_r":
			"self.image.fill((4, 2, 59), (0, 0, 28, 32))"
			self.image.fill(self.color_1, (28, 0, 4, 32))
		elif name == "wall_l":
			"self.image.fill((4, 2, 59), (4, 0, 28, 32))"
			self.image.fill(self.color_1, (0, 0, 4, 32))
		# double wall
		elif name == "wall_v":
			"self.image.fill((4, 2, 59), (0,  4, 32, 24))"
			self.image.fill(self.color_1, (0, 0, 32, 4))
			self.image.fill(self.color_1, (0, 28, 32, 4))
		elif name == "wall_w":
			"self.image.fill((4, 2, 59), (4, 0, 24, 32))"
			self.image.fill(self.color_1, (28, 0, 4, 32))
			self.image.fill(self.color_1, (0, 0, 4, 32))
		# mur diago
		elif name == "wall_a":
			"self.image.fill((4, 2, 59), (4, 4, 28, 28))"
			self.image.fill(self.color_1, (8, 0, 24, 4))
			self.image.fill(self.color_1, (0, 8, 4, 24))
			self.image.fill(self.color_1, (4, 4, 4, 4))
		elif name == "wall_b":
			"self.image.fill((4, 2, 59), (0, 4, 28, 28))"
			self.image.fill(self.color_1, (0, 0, 24, 4))
			self.image.fill(self.color_1, (28, 8, 4, 24))
			self.image.fill(self.color_1, (24, 4, 4, 4))
		elif name == "wall_y":
			"self.image.fill((4, 2, 59), (4, 0, 28, 28))"
			self.image.fill(self.color_1, (0, 0, 4, 24))
			self.image.fill(self.color_1, (8, 28, 24, 4))
			self.image.fill(self.color_1, (4, 24, 4, 4))
		elif name == "wall_z":
			"self.image.fill((4, 2, 59), (0, 0, 28, 28))"
			self.image.fill(self.color_1, (28, 0, 4, 24))
			self.image.fill(self.color_1, (0, 28, 24, 4))
			self.image.fill(self.color_1, (24, 24, 4, 4))
		# mur de fin (j'ai pas d'idée de nom)
		elif name == "wall_s":
			"self.image.fill((4, 2, 59), (0, 4, 28, 24))"
			self.image.fill(self.color_1, (0, 0, 24, 4))
			self.image.fill(self.color_1, (0, 28, 24, 4))
			self.image.fill(self.color_1, (24, 24, 4, 4))
			self.image.fill(self.color_1, (28, 8, 4, 16))
			self.image.fill(self.color_1, (24, 4, 4, 4))
		elif name == "wall_i":
			"self.image.fill((4, 2, 59), (4, 4, 28, 24))"
			self.image.fill(self.color_1, (8, 0, 24, 4))
			self.image.fill(self.color_1, (8, 28, 24, 4))
			self.image.fill(self.color_1, (4, 24, 4, 4))
			self.image.fill(self.color_1, (0, 8, 4, 16))
			self.image.fill(self.color_1, (4, 4, 4, 4))
		elif name == "wall_p":
			"self.image.fill((4, 2, 59), (4, 4, 24, 28))"
			self.image.fill(self.color_1, (28, 8, 4, 24))
			self.image.fill(self.color_1, (0, 8, 4, 24))
			self.image.fill(self.color_1, (8, 0, 16, 4))
			self.image.fill(self.color_1, (24, 4, 4, 4))
			self.image.fill(self.color_1, (4, 4, 4, 4))
		elif name == "wall_q":
			"self.image.fill((4, 2, 59), (4, 0, 24, 28))"
			self.image.fill(self.color_1, (28, 0, 4, 24))
			self.image.fill(self.color_1, (0, 0, 4, 24))
			self.image.fill(self.color_1, (8, 28, 16, 4))
			self.image.fill(self.color_1, (24, 24, 4, 4))
			self.image.fill(self.color_1, (4, 24, 4, 4))
		# mur solo :'(
		elif name == "wall_o":
			self.image.fill(self.color_1, (0, 8, 4, 16))
			self.image.fill(self.color_1, (8, 28, 16, 4))
			self.image.fill(self.color_1, (24, 24, 4, 4))
			self.image.fill(self.color_1, (4, 24, 4, 4))
			self.image.fill(self.color_1, (28, 8, 4, 16))
			self.image.fill(self.color_1, (8, 0, 16, 4))
			self.image.fill(self.color_1, (24, 4, 4, 4))
			self.image.fill(self.color_1, (4, 4, 4, 4))
		# mur spawn monstre
		elif name == "!":
			self.image.fill(self.color_1, (0, 20, 32, 4))
			self.image.fill(self.color_1, (0, 10, 32, 4))
		elif name == "?":
			self.image.fill(self.color_1, (20, 0, 4, 32))
			self.image.fill(self.color_1, (10, 0, 4, 32))
		elif name == "%":
			self.image.fill(self.color_1, (0, 20, 24, 4))
			self.image.fill(self.color_1, (0, 10, 14, 4))
			self.image.fill(self.color_1, (20, 0, 4, 20))
			self.image.fill(self.color_1, (10, 0, 4, 12))
		elif name == ":": 
			self.image.fill(self.color_1, (12, 20, 20, 4))
			self.image.fill(self.color_1, (20, 10, 12, 4))
			self.image.fill(self.color_1, (20, 0, 4, 14))
			self.image.fill(self.color_1, (10, 0, 4, 24))
		elif name == "+":
			self.image.fill(self.color_1, (20, 20, 12, 4))
			self.image.fill(self.color_1, (14, 10, 18, 4))
			self.image.fill(self.color_1, (20, 20, 4, 12))
			self.image.fill(self.color_1, (10, 10, 4, 22))
		elif name == "-":
			self.image.fill(self.color_1, (0, 20, 12, 4))
			self.image.fill(self.color_1, (0, 10, 24, 4))
			self.image.fill(self.color_1, (20, 14, 4, 18))
			self.image.fill(self.color_1, (10, 20, 4, 12))
		elif name == "=":
			self.image.fill(WHITE, (0, 14, 32, 6))
		# dot/gum
		elif name == "dot":
			self.image = pygame.Surface([4, 4])
			self.rect = pygame.Rect(self.x + 14, self.y + 14, 6, 6)
			self.image.fill(self.color_2, (0, 0, 4, 4))
		elif name == "gum":
			self.image.fill(self.color_2, (11, 11, 10, 10))
			self.image.fill(self.color_2, (10, 13, 12, 6))
			self.image.fill(self.color_2, (13, 10, 6, 12))
		# bonus
		elif name == "bonus":
			self.image.blit(image_bonus[bonus.sprite], (0, 0))
		
		self.image.set_colorkey(BLACK)

	def update(self, color):
		self.timer += 1
		self.color_update = color
		if self.timer == 20:
			self.timer = 0

		if self.timer < 10:
			self.create_sprite(self.name, False)
		else:
			self.create_sprite(self.name, True)

class Pac:
	def __init__(self, image_list, life=3, speed=4, necessary_point=15000):
		# image list
		self.image_list = image_list
		# image direction
		self.right = self.image_list[1]
		self.left = pygame.transform.rotate(self.right, 180)
		self.up = pygame.transform.rotate(self.right, 90)
		self.down = pygame.transform.rotate(self.right, 270)
		self.image = pygame.image.load("data/image/pac/pac1.png")
		# animation
		self.animation_timer = self.frame = 0
		# parametre
		self.score = 0
		self.speed = speed
		self.life = life
		self.life_earned = 0
		self.necessary_point = necessary_point

	
	def initialize_coordinates(self, x, y):
		self.screen_x = self.spawn_x = x
		self.screen_y = self.spawn_y = y
		self.collision = pygame.Rect(x, y, 32, 32)

	def initialize_window(self, window):
		self.window = window

	def initialize_moove(self):
		self.right = self.image_list[1]
		self.left = pygame.transform.rotate(self.right, 180)
		self.up = pygame.transform.rotate(self.right, 90)
		self.down = pygame.transform.rotate(self.right, 270)
		self.image = pygame.image.load("data/image/pac/pac1.png")
		self.animation_timer = self.frame = 0

	def initialize_life(self):
		self.life = 3
		self.life_earned = 0

	def initialize(self, x, y, window):
		self.initialize_window(window)
		self.initialize_coordinates(x, y)
		self.initialize_moove()

	def reset(self):
		self.initialize(self.spawn_x, self.spawn_y, self.window)
		self.image = self.image_list[1]
		
	def moove(self, direction):
		# moove right
		if direction == "right":
			if self.screen_x >= (niveau.maze_width - 1) * 32:
				self.rect = pygame.Rect(0, self.screen_y, 32, 32)
				if pygame.sprite.spritecollideany(self, group_wall) == pygame.sprite.spritecollideany(self, group_wall_spawn) == None:
					if self.screen_x >= niveau.maze_width * 32 - self.speed:
						self.screen_x = -32 + self.speed
					else:
						self.screen_x += self.speed
			else:		
				self.rect = pygame.Rect(self.screen_x + self.speed, self.screen_y, 32, 32)
				if pygame.sprite.spritecollideany(self, group_wall) == pygame.sprite.spritecollideany(self, group_wall_spawn) == None:
					self.screen_x += self.speed
			self.image = self.right

		# moove down
		elif direction == "down":
			if self.screen_y >= (niveau.maze_length - 1) * 32:
				self.rect = pygame.Rect(self.screen_x, 0, 32, 32)
				if pygame.sprite.spritecollideany(self, group_wall) == pygame.sprite.spritecollideany(self, group_wall_spawn) == None:
					if self.screen_y >= niveau.maze_length * 32  - self.speed:
						self.screen_y = -32 + self.speed
					else:
						self.screen_y += self.speed
			else:
				self.rect = pygame.Rect(self.screen_x, self.screen_y + self.speed, 32, 32)
				if pygame.sprite.spritecollideany(self, group_wall) == pygame.sprite.spritecollideany(self, group_wall_spawn) == None:
					self.screen_y += self.speed
			self.image = self.down
		
		# moove left
		elif direction == "left":
			if self.screen_x <= 0:
				self.rect = pygame.Rect((niveau.maze_width - 1) * 32, self.screen_y, 32, 32)
				if pygame.sprite.spritecollideany(self, group_wall) == pygame.sprite.spritecollideany(self, group_wall_spawn) == None:
					if self.screen_x <= -32 + self.speed:
						self.screen_x = niveau.maze_width * 32 - self.speed
					else:
						self.screen_x -= self.speed
			else:
				self.rect = pygame.Rect(self.screen_x - self.speed, self.screen_y, 32, 32)
				if pygame.sprite.spritecollideany(self, group_wall) == pygame.sprite.spritecollideany(self, group_wall_spawn) == None:
					self.screen_x -= self.speed
			self.image = self.left

		# moove up
		elif direction == "up":
			if self.screen_y <= 0:
				self.rect = pygame.Rect(self.screen_x, (niveau.maze_length - 1) * 32, 32, 32)
				if pygame.sprite.spritecollideany(self, group_wall) == pygame.sprite.spritecollideany(self, group_wall_spawn) == None:
					if self.screen_y <= -32 + self.speed:
						self.screen_y = niveau.maze_length * 32 - self.speed
					else:
						self.screen_y -= self.speed
			else:
				self.rect = pygame.Rect(self.screen_x, self.screen_y - self.speed, 32, 32)
				if pygame.sprite.spritecollideany(self, group_wall) == pygame.sprite.spritecollideany(self, group_wall_spawn) == None:
					self.screen_y -= self.speed
			self.image = self.up
		
		# pas d'autre solution que de rajouter ça ici à cause de la vérification collide
		if not (pygame.sprite.spritecollideany(self, group_wall) or pygame.sprite.spritecollideany(self, group_wall_spawn)) == None:
			self.frame = 0
			if self.animation_timer == 0:
				self.animation_timer = 1

	def death_display(self):
		self.image = self.up
		if self.frame < 999999:		# fait à la rache (si la partie fait + de 33 333 secondes le program ne marchera pas)
			self.frame = 1000001
			self.animation_timer = 3
		self.frame += 1
		if self.frame % 2 == 0:
			if self.animation_timer != 11:
				self.animation_timer += 1

		# image assignement
		self.right = self.image_list[self.animation_timer]
		self.left = pygame.transform.rotate(self.right, 180)
		self.up = pygame.transform.rotate(self.right, 90)
		self.down = pygame.transform.rotate(self.right, 270)

	def update_display(self):
		# timer verification
		if len(group_dot) == 0:
			self.image = self.image_list[0]
		else:
			self.frame += 1
			if self.frame % 2 == 0:
				self.animation_timer += 1
			if self.animation_timer >= 4:
				self.animation_timer = 0
		
		# image assignement
		self.right = self.image_list[self.animation_timer]
		self.left = pygame.transform.rotate(self.right, 180)
		self.up = pygame.transform.rotate(self.right, 90)
		self.down = pygame.transform.rotate(self.right, 270)

	"""def sound(self):
		global dt

		if self.oui == True:
			pygame.mixer.Sound.play(sound_pac_dot)
			self.non = True
		if self.non == True:
			self.truc += 1/30 * dt
			self.oui = False
			if self.truc >= self.mixer.Sound.get_length(sound_pac_dot):
				self.oui = True
				self.truc = 0"""

	def update_spritecollide(self):
		global score
		self.rect = pygame.Rect(self.screen_x + 12, self.screen_y + 12, 8, 8)
		if pygame.sprite.spritecollide(self, group_gum, True):
			score += 50
		if pygame.sprite.spritecollide(self, group_dot, True):
			score += 10

	def update_life(self):
		if score - (self.life_earned * self.necessary_point) >= self.necessary_point:
			self.life += 1
			self.life_earned += 1

	def update(self):
		self.update_life()
		self.update_display()
		self.update_spritecollide()

	def display_life(self):
		for life in range(0, self.life-1):
			self.window.blit(self.image_list[1], (0 + life * 32, (niveau.maze_length-1)*32+2))

	def display_character(self):
		self.window.blit(self.image, (self.screen_x, self.screen_y))

	def display(self):
		self.display_life()
		self.display_character()

class Ghost:
	def __init__(self, list_image, speed):
		# display variables
		self.list_image_right = [list_image[4], list_image[3], list_image[2], list_image[1], list_image[0]]
		self.list_image_left = [list_image[5], list_image[6], list_image[7], list_image[8], list_image[9]]
		self.list_image_up = [list_image[10], list_image[11], list_image[12], list_image[13], list_image[14]]
		self.list_image_down = [list_image[15], list_image[16], list_image[17], list_image[18], list_image[19]]
		self.frame = self.gumed_time = self.ia_timer = 0
		self.image = self.list_image_right[4]
		# invincibility
		self.invincibility = True
		# ia variables
		self.direction = "right"
		self.speed = speed
		self.death_animation = False
		self.right = self.left = self.up = self.down = True
		self.deadlock = None

	def initialize_coordinates(self, x, y):
		self.screen_x = self.spawn_x = x
		self.screen_y = self.spawn_y = y
		self.collision = pygame.Rect(self.screen_x + 12, self.screen_y + 12, 8, 8)
		self.rect = pygame.Rect(self.screen_x, self.screen_y, 32, 32)

	def initialize_window(self, window):
		self.window = window

	def initialize_moove(self):
		self.right = self.left = self.up = self.down = True
		self.direction = "right"
	
	def initialize_display(self):
		self.frame = self.gumed_time = self.ia_timer = 0
		self.image = self.list_image_right[4]

	def initialize(self, x, y, window):
		self.initialize_window(window)
		self.initialize_coordinates(x, y)
		self.initialize_display()
		self.state_alive()

	def reset(self):
		self.initialize(self.spawn_x, self.spawn_y, self.window)
		self.initialize_moove()

	def wall_collide(self):
		if self.screen_x % 32 != 0:
			up_wall = down_wall = True
			self.rect = pygame.Rect(self.screen_x + self.speed, self.screen_y, 32, 32)
			if pygame.sprite.spritecollideany(self, group_wall) == pygame.sprite.spritecollideany(self, group_wall_spawn) == None:
				right_wall = False
			else:
				right_wall = True
			self.rect = pygame.Rect(self.screen_x - self.speed, self.screen_y, 32, 32)
			if pygame.sprite.spritecollideany(self, group_wall) == pygame.sprite.spritecollideany(self, group_wall_spawn) == None:
				left_wall = False
			else:
				left_wall = True
		elif self.screen_y % 32 != 0:
			right_wall = left_wall = True
			self.rect = pygame.Rect(self.screen_x, self.screen_y + self.speed, 32, 32)
			if pygame.sprite.spritecollideany(self, group_wall) == pygame.sprite.spritecollideany(self, group_wall_spawn) == pygame.sprite.spritecollideany(self, group_wall_spawn_special) == None:
				down_wall = False
			else:
				down_wall = True
			self.rect = pygame.Rect(self.screen_x, self.screen_y - self.speed, 32, 32)
			if pygame.sprite.spritecollideany(self, group_wall) == pygame.sprite.spritecollideany(self, group_wall_spawn) == None:
				up_wall = False
			else:
				up_wall = True
		else:
			self.rect = pygame.Rect(self.screen_x + self.speed, self.screen_y, 32, 32)
			if pygame.sprite.spritecollideany(self, group_wall) == pygame.sprite.spritecollideany(self, group_wall_spawn) == None:
				right_wall = False
			else:
				right_wall = True
			self.rect = pygame.Rect(self.screen_x - self.speed, self.screen_y, 32, 32)
			if pygame.sprite.spritecollideany(self, group_wall) == pygame.sprite.spritecollideany(self, group_wall_spawn) == None:
				left_wall = False
			else:
				left_wall = True
			self.rect = pygame.Rect(self.screen_x, self.screen_y + self.speed, 32, 32)
			if pygame.sprite.spritecollideany(self, group_wall) == pygame.sprite.spritecollideany(self, group_wall_spawn) == pygame.sprite.spritecollideany(self, group_wall_spawn_special) == None:
				down_wall = False
			else:
				down_wall = True
			self.rect = pygame.Rect(self.screen_x, self.screen_y - self.speed, 32, 32)
			if pygame.sprite.spritecollideany(self, group_wall) == pygame.sprite.spritecollideany(self, group_wall_spawn) == None:
				up_wall = False
			else:
				up_wall = True

		# map border
		teleport = None
		if self.screen_x >= (niveau.maze_width - 1) * 32 and self.screen_y % 32 == 0:
			self.rect = pygame.Rect(0, self.screen_y, 32, 32)
			if pygame.sprite.spritecollideany(self, group_wall) == pygame.sprite.spritecollideany(self, group_wall_spawn) == None:
				teleport = "right"
			else:
				right_wall = True
		elif self.screen_x <= 0 and self.screen_y % 32 == 0:
			self.rect = pygame.Rect((niveau.maze_width - 1) * 32, self.screen_y, 32, 32)
			if pygame.sprite.spritecollideany(self, group_wall) == pygame.sprite.spritecollideany(self, group_wall_spawn) == None:
				teleport = "left"
			else:
				left_wall = True
		elif self.screen_y >= (niveau.maze_length - 1) * 32 and self.screen_x % 32 == 0:
			self.rect = pygame.Rect(self.screen_x, 0, 32, 32)
			if pygame.sprite.spritecollideany(self, group_wall) == pygame.sprite.spritecollideany(self, group_wall_spawn) == None:
				teleport = "down"
			else:
				down_wall = True
		elif self.screen_y <= 0 and self.screen_x % 32 == 0:
			self.rect = pygame.Rect(self.screen_x, (niveau.maze_length - 1) * 32, 32, 32)
			if pygame.sprite.spritecollideany(self, group_wall) == pygame.sprite.spritecollideany(self, group_wall_spawn) == None:
				teleport = "up"
			else:
				up_wall = True

		# dead_end
		if self.deadlock == "right" or self.deadlock == "left":
			if self.direction == "down" or self.direction == "up":
				self.deadlock = None
		elif self.deadlock == "down" or self.deadlock == "up":
			if self.direction == "right" or self.direction == "left":
				self.deadlock = None

		if right_wall == down_wall == up_wall == True and self.direction == "right":
			self.deadlock = "left"
		elif left_wall == down_wall == up_wall == True and self.direction == "left":
			self.deadlock = "right"
		elif right_wall == left_wall == up_wall == True and self.direction == "up":
			self.deadlock = "down"
		elif right_wall == left_wall == down_wall == True and self.direction == "down":
			self.deadlock = "up"

		return right_wall, left_wall, up_wall, down_wall, teleport

	def ai_moove_right(self, right_wall, left_wall, up_wall, down_wall, teleport):
		if teleport == "right":
			if self.screen_x >= (niveau.maze_width * 32) - self.speed:
				self.screen_x = -32 + self.speed
			else:
				self.screen_x += self.speed

			self.direction = "right"
			self.right = True
			self.down = self.up = self.left = False

		elif self.deadlock == "right" and up_wall == False or self.deadlock == "right" and down_wall == False:
			self.left = self.right = False
			self.up = True
			self.ai_moove_up(right_wall, left_wall, up_wall, down_wall, teleport)

		elif right_wall == False and self.right == True:
			self.screen_x += self.speed
			
			self.direction = "right"
			self.down = self.up = True
			self.left = False

		elif right_wall == True and up_wall == True and down_wall == True:
			self.left = True
			self.ai_moove_left(right_wall, left_wall, up_wall, down_wall, teleport)

		elif right_wall == True == left_wall == True and up_wall == True and down_wall == True:
			print("impossible")
			
		else:
			self.ai_moove_up(right_wall, left_wall, up_wall, down_wall, teleport)

	def ai_moove_left(self, right_wall, left_wall, up_wall, down_wall, teleport):
		if teleport == "left":
			if self.screen_x <= -32 + self.speed:
				self.screen_x = (niveau.maze_width * 32) - self.speed
			else:
				self.screen_x -= self.speed

			self.left = True
			self.down = self.up = self.right = False
			self.direction = "left"

		elif self.deadlock == "left" and up_wall == False or self.deadlock == "left" and down_wall == False:
			self.left = self.right = False
			self.down = True
			self.ai_moove_down(right_wall, left_wall, up_wall, down_wall, teleport)

		elif left_wall == False and self.left == True:
			self.screen_x -= self.speed
			
			self.down = self.up = True
			self.right = False
			self.direction = "left"

		elif left_wall == True and up_wall == True and down_wall == True and right_wall == False:
			self.right = True
			self.ai_moove_down(right_wall, left_wall, up_wall, down_wall, teleport)

		elif right_wall == True == left_wall == True and up_wall == True and down_wall == True:
			print("impossible")

		else:
			self.ai_moove_down(right_wall, left_wall, up_wall, down_wall, teleport)
	
	def ai_moove_down(self, right_wall, left_wall, up_wall, down_wall, teleport):
		if teleport == "down":
			if self.screen_y >= (niveau.maze_length * 32) - self.speed:
				self.screen_y = -32 + self.speed
			else:
				self.screen_y += self.speed

			self.direction = "down"
			self.down = True
			self.right = self.left = self.up = False
		
		elif self.deadlock == "down" and right_wall == False or self.deadlock == "down" and left_wall == False:
			self.up = self.down = False
			self.right = True
			self.ai_moove_right(right_wall, left_wall, up_wall, down_wall, teleport)

		elif down_wall == False and self.down == True:
			self.screen_y += self.speed
			
			self.direction = "down"
			self.right = self.left = True
			self.up = False

		elif down_wall == True and right_wall == True and left_wall == True:
			self.up = True
			self.ai_moove_up(right_wall, left_wall, up_wall, down_wall, teleport)

		elif right_wall == True == left_wall == True and up_wall == True and down_wall == True:
			print("impossible")

		else:
			self.ai_moove_right(right_wall, left_wall, up_wall, down_wall, teleport)
	
	def ai_moove_up(self, right_wall, left_wall, up_wall, down_wall, teleport):
		if teleport == "up":
			if self.screen_y <= -32 + self.speed:
				self.screen_y = (niveau.maze_length * 32) - self.speed
			else:
				self.screen_y -= self.speed

			self.up = True
			self.right = self.left = self.down = False
			self.direction = "up"
		
		elif self.deadlock == "up" and right_wall == False or self.deadlock == "up" and left_wall == False:
			self.up = self.down = False
			self.left = True
			self.ai_moove_left(right_wall, left_wall, up_wall, down_wall, teleport)

		elif up_wall == False and self.up == True:
			self.screen_y -= self.speed
			
			self.right = self.left = True
			self.down = False
			self.direction = "up"

		elif up_wall == True and right_wall == True and left_wall == True:
			self.down = True
			self.ai_moove_down(right_wall, left_wall, up_wall, down_wall, teleport)

		elif right_wall == True == left_wall == True and up_wall == True and down_wall == True:
			print("impossible")
			
		else:
			self.ai_moove_left(right_wall, left_wall, up_wall, down_wall, teleport)

	def ai_prediction(self, x, y):
		right_wall, left_wall, up_wall, down_wall, teleport = self.wall_collide()

		if self.death_animation == True:
			self.ia_death()

		else:
			if self.screen_x > x:
				target_x = "left"
			elif self.screen_x < x:
				target_x = "right"
			elif random.randint(0, 1) == 0:
				target_x = "left"
			else:
				target_x = "right"

			if self.screen_y > y:
				target_y = "up"
			elif self.screen_y < y:
				target_y = "down"
			elif random.randint(0, 1) == 0:
				target_y = "up"
			else:
				target_y = "down"

			if (self.screen_x - x)**2 > (self.screen_y - y)**2:
				priority = "x"
			elif (self.screen_x - x)**2 < (self.screen_y - y)**2:
				priority = "y"
			elif random.randint(0, 1) == 0:
				priority = "x"
			else:
				priority = "y"

			# RIGHT
			if self.direction == "right":
				if up_wall == False and right_wall == False or down_wall == False and right_wall == False:
					self.left = self.up = self.down = True

				# pas de choix possible
				if right_wall == up_wall == True or \
						right_wall == down_wall == True or \
							up_wall == down_wall == True:
					self.ai_moove_right(right_wall, left_wall, up_wall, down_wall, teleport)

				# haut, bas et droite possible
				elif up_wall == False and down_wall == False and right_wall == False:
					if priority == "x" and target_x == "right":
						self.ai_moove_right(right_wall, left_wall, up_wall, down_wall, teleport)
					elif target_y == "up":
						self.ai_moove_up(right_wall, left_wall, up_wall, down_wall, teleport)
					else:
						self.ai_moove_down(right_wall, left_wall, up_wall, down_wall, teleport)

				# droite et bas possible
				elif right_wall == down_wall == False:
					if target_x == "left" and priority == "x" or priority == "y" and target_y == "down":
						self.ai_moove_down(right_wall, left_wall, up_wall, down_wall, teleport)
					else:
						self.ai_moove_right(right_wall, left_wall, up_wall, down_wall, teleport)

				# droite ou haut possible
				elif right_wall == up_wall == False:
					if target_x == "left" and priority == "x" or priority == "y" and target_y == "up":
						self.ai_moove_up(right_wall, left_wall, up_wall, down_wall, teleport)
					else:
						self.ai_moove_right(right_wall, left_wall, up_wall, down_wall, teleport)

				# haut ou bas possible
				elif up_wall == down_wall == False:
					if target_y == "up":
						self.ai_moove_up(right_wall, left_wall, up_wall, down_wall, teleport)
					else:
						self.ai_moove_down(right_wall, left_wall, up_wall, down_wall, teleport)

			# LEFT
			elif self.direction == "left":
				if up_wall == False and left_wall == False or down_wall == False and left_wall == False:
					self.right = self.up = self.down = True

				# pas de choix possible
				if left_wall == up_wall == True or \
						left_wall == down_wall == True or \
							up_wall == down_wall == True:
					self.ai_moove_left(right_wall, left_wall, up_wall, down_wall, teleport)

				# haut, bas et droite possible
				elif up_wall == False and down_wall == False and left_wall == False:
					if priority == "x" and target_x == "left":
						self.ai_moove_left(right_wall, left_wall, up_wall, down_wall, teleport)
					elif target_y == "up":
						self.ai_moove_up(right_wall, left_wall, up_wall, down_wall, teleport)
					else:
						self.ai_moove_down(right_wall, left_wall, up_wall, down_wall, teleport)

				# droite et bas possible
				elif left_wall == down_wall == False:
					if target_x == "right" and priority == "x" or priority == "y" and target_y == "down":
						self.ai_moove_down(right_wall, left_wall, up_wall, down_wall, teleport)
					else:
						self.ai_moove_left(right_wall, left_wall, up_wall, down_wall, teleport)

				# droite ou haut possible
				elif left_wall == up_wall == False:
					if target_x == "right" and priority == "x" or priority == "y" and target_y == "up":
						self.ai_moove_up(right_wall, left_wall, up_wall, down_wall, teleport)
					else:
						self.ai_moove_left(right_wall, left_wall, up_wall, down_wall, teleport)

				# haut ou bas possible
				elif up_wall == down_wall == False:
					if target_y == "up":
						self.ai_moove_up(right_wall, left_wall, up_wall, down_wall, teleport)
					else:
						self.ai_moove_down(right_wall, left_wall, up_wall, down_wall, teleport)

			# DOWN
			elif self.direction == "down":
				if right_wall == False and down_wall == False or left_wall == False and down_wall == False:
					self.right = self.left = self.up = True

				# pas de choix possible
				if down_wall == right_wall == True or \
						down_wall == left_wall == True or \
							right_wall == left_wall == True:
					self.ai_moove_down(right_wall, left_wall, up_wall, down_wall, teleport)
	
				# haut, bas et droit possible
				elif right_wall == left_wall == down_wall == False:
					if priority == "y" and target_y == "down":
						self.ai_moove_down(right_wall, left_wall, up_wall, down_wall, teleport)
					elif target_x == "right":
						self.ai_moove_right(right_wall, left_wall, up_wall, down_wall, teleport)
					else:
						self.ai_moove_left(right_wall, left_wall, up_wall, down_wall, teleport)

				# droite et bas possible
				elif down_wall == right_wall == False:
					if target_y == "up" and priority == "y" or priority == "x" and target_x == "right":
						self.ai_moove_right(right_wall, left_wall, up_wall, down_wall, teleport)
					else:
						self.ai_moove_down(right_wall, left_wall, up_wall, down_wall, teleport)

				elif down_wall == left_wall == False:
					if target_y == "up" and priority == "y" or priority == "x" and target_x == "left":
						self.ai_moove_left(right_wall, left_wall, up_wall, down_wall, teleport)
					else:
						self.ai_moove_down(right_wall, left_wall, up_wall, down_wall, teleport)

				elif right_wall == left_wall == False:
					if target_x == "right":
						self.ai_moove_right(right_wall, left_wall, up_wall, down_wall, teleport)
					else:
						self.ai_moove_left(right_wall, left_wall, up_wall, down_wall, teleport)

			# UP
			elif self.direction == "up":
				if right_wall == False and up_wall == False or left_wall == False and up_wall == False:
					self.right = self.left = self.down = True

				# pas de choix possible
				if up_wall == right_wall == True or \
						up_wall == left_wall == True or \
							right_wall == left_wall == True:
					self.ai_moove_up(right_wall, left_wall, up_wall, down_wall, teleport)
	
				# haut, bas et droit possible
				elif right_wall == left_wall == up_wall == False:
					if priority == "y" and target_y == "up":
						self.ai_moove_up(right_wall, left_wall, up_wall, down_wall, teleport)
					elif target_x == "right":
						self.ai_moove_right(right_wall, left_wall, up_wall, down_wall, teleport)
					else:
						self.ai_moove_left(right_wall, left_wall, up_wall, down_wall, teleport)

				# droite et bas possible
				elif up_wall == right_wall == False:
					if target_y == "down" and priority == "y" or priority == "x" and target_x == "right":
						self.ai_moove_right(right_wall, left_wall, up_wall, down_wall, teleport)
					else:
						self.ai_moove_up(right_wall, left_wall, up_wall, down_wall, teleport)

				elif up_wall == left_wall == False:
					if target_y == "down" and priority == "y" or priority == "x" and target_x == "left":
						self.ai_moove_left(right_wall, left_wall, up_wall, down_wall, teleport)
					else:
						self.ai_moove_up(right_wall, left_wall, up_wall, down_wall, teleport)

				elif right_wall == left_wall == False:
					if target_x == "right":
						self.ai_moove_right(right_wall, left_wall, up_wall, down_wall, teleport)
					else:
						self.ai_moove_left(right_wall, left_wall, up_wall, down_wall, teleport)


	def ai_frightened(self):
		right_wall, left_wall, up_wall, down_wall, teleport = self.wall_collide()

		# RIGHT
		if self.direction == "right":
			if up_wall == False and right_wall == False or down_wall == False and right_wall == False:
				self.left = self.up = self.down = True
			
			# pas de choix possible
			if right_wall == up_wall == True or \
					right_wall == down_wall == True or \
						up_wall == down_wall == True:
				self.ai_moove_right(right_wall, left_wall, up_wall, down_wall, teleport)

			# haut, bas et droite possible
			elif up_wall == False and down_wall == False and right_wall == False:
				path = random.randint(0, 2)
				if path == 0:
					self.ai_moove_right(right_wall, left_wall, up_wall, down_wall, teleport)
				elif path == 1:
					self.ai_moove_up(right_wall, left_wall, up_wall, down_wall, teleport)
				else:
					self.ai_moove_down(right_wall, left_wall, up_wall, down_wall, teleport)

			# droite et bas possible
			elif right_wall == down_wall == False:
				if random.randint(0, 1) == 0:
					self.ai_moove_right(right_wall, left_wall, up_wall, down_wall, teleport)
				else:
					self.ai_moove_down(right_wall, left_wall, up_wall, down_wall, teleport)
			
			# droite ou haut possible
			elif right_wall == up_wall == False:
				if random.randint(0, 1) == 0:
					self.ai_moove_right(right_wall, left_wall, up_wall, down_wall, teleport)
				else:
					self.ai_moove_up(right_wall, left_wall, up_wall, down_wall, teleport)
			
			# haut ou bas possible
			elif up_wall == down_wall == False:
				if random.randint(0, 1) == 0:
					self.ai_moove_up(right_wall, left_wall, up_wall, down_wall, teleport)
				else:
					self.ai_moove_down(right_wall, left_wall, up_wall, down_wall, teleport)

		# LEFT
		elif self.direction == "left":
			if up_wall == False and left_wall == False or down_wall == False and left_wall == False:
				self.right = self.up = self.down = True
			
			# pas de choix possible
			if left_wall == up_wall == True or \
					left_wall == down_wall == True or \
						up_wall == down_wall == True:
				self.ai_moove_left(right_wall, left_wall, up_wall, down_wall, teleport)

			# haut, bas et droit possible
			elif up_wall == False and down_wall == False and left_wall == False:
				path = random.randint(0, 2)
				if path == 0:
					self.ai_moove_left(right_wall, left_wall, up_wall, down_wall, teleport)
				elif path == 1:
					self.ai_moove_up(right_wall, left_wall, up_wall, down_wall, teleport)
				else:
					self.ai_moove_down(right_wall, left_wall, up_wall, down_wall, teleport)

			# droite et bas possible
			elif left_wall == down_wall == False:
				if random.randint(0, 1) == 0:
					self.ai_moove_left(right_wall, left_wall, up_wall, down_wall, teleport)
				else:
					self.ai_moove_down(right_wall, left_wall, up_wall, down_wall, teleport)
			
			elif left_wall == up_wall == False:
				if random.randint(0, 1) == 0:
					self.ai_moove_left(right_wall, left_wall, up_wall, down_wall, teleport)
				else:
					self.ai_moove_up(right_wall, left_wall, up_wall, down_wall, teleport)
				
			elif up_wall == down_wall == False:
				if random.randint(0, 1) == 0:
					self.ai_moove_up(right_wall, left_wall, up_wall, down_wall, teleport)
				else:
					self.ai_moove_down(right_wall, left_wall, up_wall, down_wall, teleport)

		# DOWN
		elif self.direction == "down":
			if right_wall == False and down_wall == False or left_wall == False and down_wall == False:
				self.right = self.left = self.up = True
			
			# pas de choix possible
			if down_wall == right_wall == True or \
					down_wall == left_wall == True or \
						right_wall == left_wall == True:
				self.ai_moove_down(right_wall, left_wall, up_wall, down_wall, teleport)
 
			# haut, bas et droit possible
			elif right_wall == left_wall == down_wall == False:
				path = random.randint(0, 2)
				if path == 0:
					self.ai_moove_down(right_wall, left_wall, up_wall, down_wall, teleport)
				elif path == 1:
					self.ai_moove_right(right_wall, left_wall, up_wall, down_wall, teleport)
				else:
					self.ai_moove_left(right_wall, left_wall, up_wall, down_wall, teleport)

			# droite et bas possible
			elif down_wall == right_wall == False:
				if random.randint(0, 1) == 0:
					self.ai_moove_down(right_wall, left_wall, up_wall, down_wall, teleport)
				else:
					self.ai_moove_right(right_wall, left_wall, up_wall, down_wall, teleport)
			
			elif down_wall == left_wall == False:
				if random.randint(0, 1) == 0:
					self.ai_moove_down(right_wall, left_wall, up_wall, down_wall, teleport)
				else:
					self.ai_moove_left(right_wall, left_wall, up_wall, down_wall, teleport)
				
			elif right_wall == left_wall == False:
				if random.randint(0, 1) == 0:
					self.ai_moove_right(right_wall, left_wall, up_wall, down_wall, teleport)
				else:
					self.ai_moove_left(right_wall, left_wall, up_wall, down_wall, teleport)
		
		# UP
		elif self.direction == "up":
			if right_wall == False and up_wall == False or left_wall == False and up_wall == False:
				self.right = self.left = self.down = True
			
			# pas de choix possible
			if up_wall == right_wall == True or \
					up_wall == left_wall == True or \
						right_wall == left_wall == True:
				self.ai_moove_up(right_wall, left_wall, up_wall, down_wall, teleport)
 
			# haut, bas et droit possible
			elif right_wall == left_wall == up_wall == False:
				path = random.randint(0, 2)
				if path == 0:
					self.ai_moove_up(right_wall, left_wall, up_wall, down_wall, teleport)
				elif path == 1:
					self.ai_moove_right(right_wall, left_wall, up_wall, down_wall, teleport)
				else:
					self.ai_moove_left(right_wall, left_wall, up_wall, down_wall, teleport)

			# droite et bas possible
			elif up_wall == right_wall == False:
				if random.randint(0, 1) == 0:
					self.ai_moove_up(right_wall, left_wall, up_wall, down_wall, teleport)
				else:
					self.ai_moove_right(right_wall, left_wall, up_wall, down_wall, teleport)
			
			elif up_wall == left_wall == False:
				if random.randint(0, 1) == 0:
					self.ai_moove_up(right_wall, left_wall, up_wall, down_wall, teleport)
				else:
					self.ai_moove_left(right_wall, left_wall, up_wall, down_wall, teleport)
				
			elif right_wall == left_wall == False:
				if random.randint(0, 1) == 0:
					self.ai_moove_right(right_wall, left_wall, up_wall, down_wall, teleport)
				else:
					self.ai_moove_left(right_wall, left_wall, up_wall, down_wall, teleport)

	def ia_death(self):
		if shadow.spawn_y > self.screen_y:
			self.screen_y += self.speed
			self.direction = "down"
		elif shadow.spawn_y < self.screen_y:
			self.screen_y -= self.speed
			self.direction = "up"
		elif shadow.spawn_x > self.screen_x:
			self.screen_x += self.speed
			self.direction = "right"
		elif shadow.spawn_x < self.screen_x:
			self.screen_x -= self.speed
			self.direction = "left"
		else:
			self.initialize_moove()
			self.state_alive()

	def state_alive(self):
		self.speed = 4
		self.gumed_time = 0
		self.check_screen_coordinate(self.speed)
		self.invincibility = True
		self.death_animation = False

	def state_gumed(self):
		self.speed = 2
		self.invincibility = False
		self.gumed_time = 6 * 30

	def state_death(self):
		self.speed = 8
		self.check_screen_coordinate(self.speed)
		self.death_animation = True
		self.gumed_time = 0

	def state_touched(self):
		if self.invincibility == True:
			death()
		elif self.invincibility == False and self.death_animation == False:
			pac.ghost_score *= 2
			self.animation_touched()
			self.state_death()
	
	def animation_touched(self):
		global score
		score += pac.ghost_score
		self.image = font_8.render(str(pac.ghost_score), 0, (34, 255, 255))

		window.fill(BLACK)
		group_wall.draw(window)
		group_wall_spawn.draw(window)
		group_wall_spawn_special.draw(window)
		group_dot.draw(window)
		group_gum.draw(window)
		group_bonus.draw(window)
		self.display()

		pygame.display.flip()
		pygame.time.wait(650) # 0.65 sec

	def check_screen_coordinate(self, speed):
		"""Make the ghost coordinate a multiple of 32, by erasing what they have in excess."""
		self.screen_x -= self.screen_x % speed
		self.screen_y -= self.screen_y % speed

	def ia_update(self, chase_x, chase_y, scatter_x, scatter_y, radius=0):
		self.ia_timer += 1/30 * dt
		distance = math.hypot(pac.screen_x - self.screen_x, pac.screen_y - self.screen_y)

		if self.gumed_time != 0:
			self.ai_frightened()
		elif self.ia_timer >= 10 and not distance <= radius:
			self.ai_prediction(chase_x, chase_y)
		else:
			self.ai_prediction(scatter_x, scatter_y)

		if self.ia_timer >= 30:
			self.ia_timer = 0

	def update_display(self):
		self.frame += 1
		if self.frame % 5 == 0:
			self.frame -= 5

		if self.death_animation == True:
			if self.direction == "right":
				self.image = ghost_eye_right
			elif self.direction == "left":
				self.image = ghost_eye_left
			elif self.direction == "up":
				self.image = ghost_eye_up
			elif self.direction == "down":
				self.image = self.image = ghost_eye_down
		elif self.invincibility == True:
			if self.direction == "right":
				self.image = self.list_image_right[self.frame]
			elif self.direction == "left":
				self.image = self.list_image_left[self.frame]
			elif self.direction == "up":
				self.image = self.list_image_up[self.frame]
			elif self.direction == "down":
				self.image = self.list_image_down[self.frame]
		elif self.invincibility == False:
			self.gumed_time -= 1
			if self.gumed_time == 0:
				self.state_alive()
			elif self.gumed_time < 48 and self.gumed_time > 40 or self.gumed_time < 32 and self.gumed_time > 24 or self.gumed_time < 16 and self.gumed_time > 8:
				self.image = list_gum_end[self.frame]
			else:
				self.image = image_gum[self.frame]

	def update(self):
		self.collision = pygame.Rect(self.screen_x + 8, self.screen_y + 8, 16, 16)
		pac.rect = pygame.Rect(pac.screen_x + 8, pac.screen_y + 8, 16, 16)

		if pac.rect.colliderect(self.collision):
			self.state_touched()
			
		pac.rect = pygame.Rect(pac.screen_x + 12, pac.screen_y + 12, 8, 8)
		if pygame.sprite.spritecollide(pac, group_gum, False) and self.death_animation == False:
			pac.ghost_score = 100
			self.state_gumed()

		self.update_display()

	def display(self):
		self.window.blit(self.image, (self.screen_x, self.screen_y))

	def play(self):
		self.update()
		self.display()

class Bonus:
	def __init__(self, window, x, y):
		self.bonus = False
		self.x = x
		self.y = y
		self.timer = self.timer_display = 0
		self.wait = 240
		self.list_image = image_bonus
		self.fruit_text = font_13.render("", 0, (34, 255, 255))
		self.window = window
		self.sprite = 0
		self.point = 100

	def create(self):
		bonus = Sprite(self.x, self.y)
		bonus.create_sprite("bonus")
		group_bonus.add(bonus)
		self.bonus = True

	def delete(self):
		group_bonus.empty()
		self.bonus = False

	def hit_fruit(self):
		self.timer_display += 1

		if self.timer_display != 56:
			if self.timer_display % 10 == 0:
				self.fruit_text = font_8.render(str(self.point), 0, (34, 255, 255))
			elif self.timer_display % 5 == 0:
				self.fruit_text = font_8.render("", 0, (34, 255, 255))
		else:
			self.timer_display = 0

	def update_score(self):
		if self.sprite == 1:
			self.point = 300
		elif self.sprite == 2:
			self.point = 500
		elif self.sprite == 3:
			self.point = 700
		elif self.sprite == 4:
			self.point = 1000
		elif self.sprite == 5:
			self.point = 2000
		else:
			# reset au cas où 6 bonus s'affiche dans un niveau
			# après avoir utiliser tout les bonus
			self.sprite = 0
			self.point = 100
		# si on récupère tout les bonus on gagne 4600 points en un stage

	def update_timer(self):
		if self.sprite < 6:
			self.timer += 1 * dt
			if self.timer >= self.wait and self.bonus == False:
				self.create()
				self.update_score()
				self.sprite += 1
				self.timer = 0
				self.wait *= 1.25
		if self.timer >= 300 and self.bonus == True: # 300 frame ~= 10s
			self.delete()
			self.sprite -= 1
			self.timer = 1
			self.wait /= 1.25

		if self.timer >= self.wait and self.bonus == False:
			self.timer = 1
			print("truc impossible vient de se réaliser")

	def update_collide(self):
		global score
		if pygame.sprite.spritecollide(pac, group_bonus, False):
			self.delete()
			score += self.point
			self.timer = 0
			return True

	def update(self):
		self.update_timer()

		if self.update_collide() == True or self.timer_display != 0:
			self.hit_fruit()

	def display(self):
		if len(group_bonus) == 0:
			self.window.blit(self.fruit_text, (self.x, self.y + 5))

# pas fini et pas encore bien assez réfléchi
# quelques bug sont à fixer
# les nombres ne sont pas encore implémenter
# si implémenter peut être ajouter dans maze_editor pour définir le nombre de case en x, y
def new_hiscore(max_letters):
	input = ''
	number_letters = 0
	list_key_letters = [pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d, pygame.K_e, pygame.K_f, pygame.K_g,
	pygame.K_h, pygame.K_i, pygame.K_j, pygame.K_k, pygame.K_l, pygame.K_m, pygame.K_n, pygame.K_o, pygame.K_p, 
	pygame.K_q, pygame.K_r, pygame.K_s, pygame.K_t, pygame.K_u, pygame.K_v, pygame.K_w, pygame.K_x, pygame.K_y, pygame.K_z]

	text_score = outfile_read_list("data/HISCORE/HISCORE.txt")
	text_score = [s.replace("\n", "") for s in text_score]

	loop = True
	while loop:
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == command_escape:
					loop = False
					if number_letters > 0:
						return input
					elif number_letters <= 0:
						return "xxx"

				if number_letters != max_letters:
					if event.key in list_key_letters:
						input += pygame.key.name(event.key)
						number_letters += 1

				if number_letters != 0:
					if event.key == pygame.K_BACKSPACE:
						number_letters -= 1
						list1 = list(input)
						list1 = list1[:-1]
						input = ""
						for i in list1:
							input += i

				if event.key == command_return:
					loop = False
					if number_letters > 0:
						return input
					elif number_letters <= 0:
						return "xxx"

		name = font_13.render(input, 0, WHITE)

		window.fill(BLACK)
		window.blit(name, (window.get_rect().width / 2 - (len(input)*8), window.get_rect().height / 2 - 16))
		pygame.display.flip()

def set_HISCORE(score, stage):
	text_score = outfile_read("data/HISCORE/HISCORE.txt")
	file_hiscore_score = [int(word) for word in text_score.split() if word.isdigit()]
	text_score = [str(word) for word in text_score.split() if not word.isdigit()]

	txt_stage = outfile_read("data/HISCORE/STAGE.txt")
	text_stage = [str(word) for word in txt_stage.split()]

	name = new_hiscore(3)
	for n, i in enumerate(file_hiscore_score):
		if score > i:

			old_score = file_hiscore_score[n]
			old_name = text_score[n]
			old_stage = text_stage[n]

			file_hiscore_score[n] = score
			text_score[n] = name
			text_stage[n] = stage

			score = old_score
			name = old_name
			stage = old_stage

	"""	30010 	B1	enz <- moi car je suis trop fort
		28360 	A3	vio <- record de la personne qui m'a aidé à équilibrer le jeu
		25000 	B1	pac
		20000 	A2	pok
		15000 	A3	spe				hight-score de base
		7000 	A1	ink
		5000 	A1	shw
		0 		A1	xxx				note à moi-même : ajoute un système de reset avec ces scores
		0 		A1	xxx"""

	outfile = open("data/HISCORE/HISCORE.txt", "w")
	# save the datas into the file
	for n, i in enumerate(file_hiscore_score):
		outfile.write(str(file_hiscore_score[n]) + " " + text_score[n] + "\n")
	outfile.close()

	outfile = open("data/HISCORE/STAGE.txt", "w")
	# save the datas into the file
	for n, i in enumerate(text_stage):
		outfile.write(text_stage[n] + "\n")
	outfile.close()

def menu_home():
	window = pygame.display.set_mode((640, 640))
	y = 273

	loop = True
	while loop:
		for event in pygame.event.get():
			if event.type == QUIT or event.type == KEYDOWN and event.key == command_escape:
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == command_down:
					if y == 423:
						y = 273
					else:
						y += 50
				elif event.key == command_up:
					if y == 273:
						y = 423
					else:
						y -= 50
				elif event.key == command_return:
					if y == 273:
						loop = False
						level_start()
						break
					elif y == 323:
						display_HISCORE()
						window = pygame.display.set_mode((640, 640))
						pygame.display.flip()
						break
					elif y == 373:
						level_editor()
						window = pygame.display.set_mode((640, 640))
						pygame.display.flip()
						break
					elif y == 423:
						menu_option()
			# display --------------------------------------------------------------------------------------------------------------------------- #
			window.fill(BLACK)
			window.blit(text_pac_logo, (window.get_width() / 2 - 348 / 2, 70))
			window.blit(text_home_1player, (window.get_width() / 2 - 80, 270))
			window.blit(text_home_HISCORE, (window.get_width() / 2 - 80, 320))
			window.blit(text_home_edit, (window.get_width() / 2 - 80, 370))
			window.blit(text_home_option, (window.get_width() / 2 - 80, 420))
			pygame.draw.polygon(window, WHITE, ((window.get_width() / 2 - 105, y), (window.get_width() / 2 - 105, y + 10), (window.get_width() / 2 - 90, y + 5)))
			# flip
			pygame.display.flip()

		pygame.time.Clock().tick(15)

def display_HISCORE():
	"512, 640"
	window = pygame.display.set_mode((512, 640))

	text_score = outfile_read("data/HISCORE/HISCORE.txt")
	number_score = [str(word) for word in text_score.split() if word.isdigit()]
	name_score = [str(word) for word in text_score.split() if not word.isdigit()]
	txt_stage = outfile_read("data/HISCORE/STAGE.txt")
	name_stage = [str(word) for word in txt_stage.split()]
	
	place_x = window.get_width() / 2 - 373 / 2
	hiscore = []
	name = []
	stage = []
	name_x = []
	hiscore_x = []
	stage_x = []
	for i in range(0, len(number_score)):
		hiscore.append(font_13.render(number_score[i], 0, WHITE))
		hiscore_x.append((place_x + 175 - (len(number_score[i]) * 13) + 3, 200 + (i+1) * 30))
		stage.append(font_13.render(name_stage[i], 0, WHITE))
		stage_x.append((place_x + 260, 200 + (i+1) * 30))
		name.append(font_13.render(name_score[i], 0, WHITE))
		name_x.append((place_x + 375 - (len(name_score[i]) * 13) - 2, 200 + (i+1) * 30))

	# display --------------------------------------------------------------------------------------------------------------------------- #
	window.fill(BLACK)

	window.blit(text_pac_logo, (window.get_width() // 2 - 348 // 2, 70))

	window.blit(text_hiscore_score, (place_x + 112, 200))
	window.blit(text_hiscore_round, (place_x + 220, 200))
	window.blit(text_hiscore_name, (place_x + 320, 200))

	for i in range (0, len(hiscore)):
		window.blit(text_hiscore_podium_list[i], (place_x, 230 + 30*i))
		window.blit(hiscore[i], hiscore_x[i])
		window.blit(stage[i], stage_x[i])
		window.blit(name[i], name_x[i])

	pygame.display.flip()
		
	loop = True
	while loop:
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit()
			elif event.type == KEYDOWN:
				if event.key == command_escape:
					loop = False
					break

		pygame.time.Clock().tick(15)

def level_start():
	global level, niveau, p, text_score, dt, stage, world, last_time
	# choix du niveau
	world, level, stage, level_file, fps = level_up(world, level, list_stage)
	# génération du niveau
	niveau = Maze()
	niveau.read_file(level_file)
	# ouverture de la fenêtre Pygame
	window = pygame.display.set_mode((niveau.maze_width * 32, niveau.maze_length * 32))
	niveau.display_maze(window)
	# text hiscore
	text_game_HISCORE = font_8.render("high-score " + file_hiscore_score[0], 0, WHITE)
	text_stage = font_8.render("stage " + stage, 0, WHITE)
	# variable touche mouvement
	d = u = l = r = 0

	level_before()

	last_time = time.time()
	temps = 0
	loop = True
	while loop:
		# fps --------------------------------------------------------------------------------------------------------------------------------- #
		# augmentation de la vitesse du jeu chaque seconde de 0.0005 image par seconde
		# pour créer une dynamique
		# utilisation de Dtime pour l'augmentation (peut-être qu'il y a mieux)
		dt, last_time = dtime(fps, last_time)
		temps += dt * (1/fps)
		# touche ------------------------------------------------------------------------------------------------------------------------------ #
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit()
			# bouton pause
			elif event.type == KEYDOWN:
				if event.key == command_escape:
					menu_pause()
					last_time = time.time()
					break
				elif event.key == K_g:
					level_start()
					loop = False
					break
		# mouvement ----------------------------------------------------------------------------------------------------------------------- #
		" touche pac ---------------------------------------------------------------------------------------------------------------------- "
		keys = pygame.key.get_pressed()
		if keys[command_up] or u == True:
			u = True
			d = r = l = False
			pac.rect = pygame.Rect(pac.screen_x, pac.screen_y - pac.speed, 32, 32)
			if pac.screen_x % 32 == 0 and pygame.sprite.spritecollideany(pac, group_wall) == pygame.sprite.spritecollideany(pac, group_wall_spawn) == None:
				p = "up"
		if keys[command_down] or d == True:
			d = True
			u = l = r = False
			pac.rect = pygame.Rect(pac.screen_x, pac.screen_y + pac.speed, 32, 32)
			if pac.screen_x % 32 == 0 and pygame.sprite.spritecollideany(pac, group_wall) == pygame.sprite.spritecollideany(pac, group_wall_spawn) == None:
				p = "down"
		if keys[command_right] or r == True:
			r = True
			u = d = l = False
			pac.rect = pygame.Rect(pac.screen_x + pac.speed, pac.screen_y, 32, 32)
			if pac.screen_y % 32 == 0 and pygame.sprite.spritecollideany(pac, group_wall) == pygame.sprite.spritecollideany(pac, group_wall_spawn) == None:
				p = "right"
		if keys[command_left] or l == True:
			l = True
			r = u = d = False
			pac.rect = pygame.Rect(pac.screen_x - pac.speed, pac.screen_y, 32, 32)
			if pac.screen_y % 32 == 0 and pygame.sprite.spritecollideany(pac, group_wall) == pygame.sprite.spritecollideany(pac, group_wall_spawn) == None:
				p = "left"

		# mouvements -------------------------------------------------------------------------------------------------------------------------- #
		pac.moove(p)
			 
		if p == "right":
			pinky.ia_update(pac.screen_x + 64, pac.screen_y, 0, 0)
			inky.ia_update((pac.screen_x + 64) * 2 - shadow.screen_x, pac.screen_y * 2 - shadow.screen_y, (niveau.maze_width-1) * 32, (niveau.maze_length-1) * 32)
		elif p == "left":
			pinky.ia_update(pac.screen_x - 64, pac.screen_y, 0, 0)
			inky.ia_update((pac.screen_x - 64) * 2 - shadow.screen_x, pac.screen_y * 2 - shadow.screen_y, (niveau.maze_width-1) * 32, (niveau.maze_length-1) * 32)
		elif p == "up":
			pinky.ia_update(pac.screen_x - 64, pac.screen_y - 64, 0, 0)
			inky.ia_update((pac.screen_x - 64)* 2 - shadow.screen_x, (pac.screen_y - 64)* 2 - shadow.screen_y, (niveau.maze_width-1) * 32, (niveau.maze_length-1) * 32)
		elif p == "down":
			pinky.ia_update(pac.screen_x, pac.screen_y + 64, 0, 0)
			inky.ia_update(pac.screen_x * 2 - shadow.screen_x, (pac.screen_y + 64)*2 - shadow.screen_y, (niveau.maze_width-1) * 32, (niveau.maze_length-1) * 32)
		
		pokey.ia_update(pac.screen_x, pac.screen_y, 0, (niveau.maze_length-1) * 32, 128)
		shadow.ia_update(pac.screen_x, pac.screen_y, (niveau.maze_width-1) * 32, 0)
		
		if len(group_dot) == 0:
			pac.update()
			level_end()
			level_start()
			loop = False
			break

		# DISPLAY ----------------------------------------------------------------------------------------------------------------------------- #
		if len(group_gum) != 0:
			group_gum.update(BLACK)
		text_score = font_8.render("score " + str(score), 0, WHITE)

		if int(file_hiscore_score[0]) < score:
			text_game_HISCORE = font_8.render("high-score " + str(score), 0, YELLOW)
		""" structure ------------------------------------------------------------------------------------------------------------------- """
		window.fill(BLACK)														# fond
		group_wall.draw(window)													# wall
		group_wall_spawn.draw(window)											# spawn-wall
		group_wall_spawn_special.draw(window)									# special-wall
		group_dot.draw(window)													# dot
		group_gum.draw(window)													# gum
		group_bonus.draw(window)												# bonus
		""" text ------------------------------------------------------------------------------------------------------------------------ """
		window.blit(text_score, (64, 2))										# text_score
		window.blit(text_game_HISCORE, (window.get_rect().width/2 - 82, 2))		# text_hight-score
		window.blit(text_stage, (window.get_rect().width - 150, 2))				# text_stage
		bonus.display()
		""" personnage ------------------------------------------------------------------------------------------------------------------ """
		if niveau.bonus_level == True:
			bonus.update()
		if niveau.inky == True:
			inky.play()
		if niveau.shadow == True:
			shadow.play()
		if niveau.pokey == True:
			pokey.play()
		if niveau.pinky == True:
			pinky.play()
		pac.update()
		pac.display()															# player
		fps_display(show_fps, window, font_8)									# fps

		pygame.display.flip()
		clock.tick(fps)

def level_before():
	global p, last_time
	timer = 19
	
	right, left, down, up = niveau.moove_availablity()
	if right == True:
		p = "right"
	elif down == True:
		p = "down"
	elif left == True:
		p = "left"
	else:
		p = "up"

	loop = True
	timer_loop = 60
	while loop == True:
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit()
			elif event.type == KEYDOWN:
				if event.key == command_right and right == True:
					p = "right"
				elif event.key == command_left and left == True:
					p = "left"
				elif event.key == command_down and down == True:
					p = "down"
				elif event.key == command_up and up == True:
					p = "up"

		if timer_loop == 0:
			loop = False

		timer += 1
		timer_loop -= 1
		if timer >=10:
			window.blit(text_ready, (bonus.x - 26 + 3, bonus.y))
			pygame.display.flip()

		if timer == 20:
			window.fill(BLACK)
			group_wall.draw(window)
			group_wall_spawn.draw(window)
			group_wall_spawn_special.draw(window)
			group_dot.draw(window)
			group_gum.draw(window)
			inky.display()
			shadow.display()
			pinky.display()
			pokey.display()
			pac.display()
			timer = 0

		pygame.display.flip()
		pygame.time.Clock().tick(15)

	last_time = time.time()

def level_over():
	global level, world, score, file_hiscore_score

	window = pygame.display.set_mode((640, 640))
	if int(file_hiscore_score[8]) < score:
		set_HISCORE(score, stage)
		file_hiscore_score = hiscore_list()

	loop = True
	while loop:
		for event in pygame.event.get():
			if event.type == QUIT or event.type == KEYDOWN and event.key == command_escape:
				sys.exit()
			elif event.type == KEYDOWN and event.key == command_return:
				level = score = 0
				world = 1
				loop = False
				menu_home()
				break
		
		window.fill(BLACK)
		window.blit((text_score), (320, 320))
		pygame.display.flip()
		pygame.time.Clock().tick(30)

def death():
	for _ in range(0, 45):
		pygame.event.get()
		# DISPLAY ------------------------------------------------------------------------------------------------------------------------- #
		# draw
		window.fill((0, 0, 0))
		group_wall.draw(window)
		group_wall_spawn.draw(window)
		group_wall_spawn_special.draw(window)
		""" personnage ------------------------------------------------------------------------------------------------------------------ """
		pac.death_display()
		pac.display()

		pygame.display.update()
		pygame.time.Clock().tick(30)

	pac.life -= 1
	reset()
	if pac.life <= 0:
		pac.initialize_life()
		level_over()
	else:
		level_before()

def level_end():
	timer = 0

	loop = True
	while loop:
		# TIMER #
		timer += 1
		if timer == 60:
			loop = False
			break
		
		# DISPLAY ------------------------------------------------------------------------------------------------------------------------- #
		# update
		group_wall_spawn.update(WHITE)
		group_wall_spawn_special.update(WHITE)
		# draw
		window.fill(BLACK)
		group_wall.draw(window)
		group_wall.update(WHITE)
		group_wall_spawn.draw(window)
		group_wall_spawn_special.draw(window)
		""" personnage ------------------------------------------------------------------------------------------------------------------ """
		pac.display()
		
		pygame.display.update()
		pygame.time.Clock().tick(30)
	reset()

def menu_pause():
	global level, score, world
	pause_button = 1
	half_width = window.get_rect().width / 2
	half_heigth = window.get_rect().height / 2
	pause_button_color_1 = YELLOW
	pause_button_color_2 = pause_button_color_3 = WHITE

	window.fill(WHITE, (half_width - 96, half_heigth - 160, 192, 320))
	window.fill(BLACK, (half_width - 96 + 5, half_heigth - 160 + 5, 182, 310))
	pygame.display.update((half_width - 96, half_heigth - 160, 192, 320))

	loop = True
	while loop:
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit()
			elif event.type == KEYDOWN:
				if event.key == command_escape:
					loop = False
				elif event.key == command_down:
					if pause_button == 3:
						pause_button = 1
					else:
						pause_button += 1
				elif event.key == command_up:
					if pause_button == 1:
						pause_button = 3
					else:
						pause_button -=1
				elif event.key == command_return:
					if pause_button == 1:
						loop = level = score = 0
						world = 1
						pac.initialize_life()
						reset()
						level_start()
						break
					elif pause_button == 2:
						level = 0
						world = 1
						pac.initialize_life()
						reset()
						menu_home()
						break
					elif pause_button == 3:
						sys.exit()

				if pause_button == 1:
					pause_button_color_1 = YELLOW
					pause_button_color_2 = WHITE
					pause_button_color_3 = WHITE
				elif pause_button == 2:
					pause_button_color_1 = WHITE
					pause_button_color_2 = YELLOW
					pause_button_color_3 = WHITE
				elif pause_button == 3:
					pause_button_color_1 = WHITE
					pause_button_color_2 = WHITE
					pause_button_color_3 = YELLOW

			# DRAW BUTTON ------------------------------------------------------------------------------------------------------------------ #
			window.fill(pause_button_color_1, (half_width - 96 + 20, half_heigth - 160 + 192 / 3, 152, 40))
			window.fill(BLACK, (half_width - 96 + 25, half_heigth - 160 + 192 / 3 + 5, 142, 30))					# button_1
			window.blit((text_pause_replay), (half_width - 96 + 37, half_heigth - 160 + 192 / 3 + 12))	

			window.fill(pause_button_color_2, (half_width - 96 + 20, half_heigth - 160 + 2 *(192 / 3), 152, 40))
			window.fill(BLACK, (half_width - 96 + 25, half_heigth - 160 + 2 *(192 / 3) + 5, 142, 30))				# button_2
			window.blit((text_pause_menu), (half_width - 96 + 73, half_heigth - 160 + 2 *(192 / 3) + 12))

			window.fill(pause_button_color_3, (half_width - 96 + 20, half_heigth - 160 + 192, 152, 40))
			window.fill(BLACK, (half_width - 96 + 25, half_heigth - 160 + 192 + 5, 142, 30))						# button_3
			window.blit((text_pause_quit), (half_width - 96 + 58, half_heigth - 160 + 192 + 12))

			pygame.display.update((half_width - 96, half_heigth - 160, 192, 320))
			
		pygame.time.Clock().tick(15)

# pas fini genre vraiment
def level_editor(x=40, y=40):
	window = pygame.display.set_mode((x * 32, y * 32))
	wall = "0"
	maze = []
	while y:
		y -= 1
		z = x
		ligne = []
		while z:
			z -= 1
			ligne.append("0")
		maze.append(ligne)
	niveau = Maze()

	loop = True
	while loop:
			
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit()

			if event.type == KEYDOWN:
				if event.key == command_escape:
					loop = False
				
				# beaucoup de vérification sont à faire
				# comme dans le class Maze par exemple

				# "=" n'est pas 100% fonctionnel pour le
				# map editing, il faut que j'écris toutes
				# les combinaisons possible de murs avec "="

				# 1, 2, 3, 4 et 5 n'ont aucune visualisation
				# dans l'éditeur de niveau, c'est impossible
				# de savoir où ils sont
				# de + on peut poser plusieurs 1, 2.. ce qui
				# ne pause pas de problème au code, mais
				# peut rendre confu les joueurs

				# toutes les possibilités d'éléments ne sont pas
				# encore implémenter dans l'éditeur
				# il manque "b", "g", "1", "2", "3"

				# rajouter une interface pour savoir quel objet
				# nous tenons sur la souris
				# pouvoir sélectioner les objets depuis l'interface
				# si on prend l'objet pour les murs "m" on peut
				# afficher une sorte de "mur solo" transparent
				# pour "m" sur la souris par exemple
				elif event.key == K_a:
					wall = "m"
				elif event.key == K_q:
					wall = "*"
				elif event.key == K_z:
					wall = "s"
				elif event.key == K_e:
					wall = "="
				elif event.key == K_s:
					wall = "g"
				elif event.key == K_SPACE:
					# faire en sorte que la map soit sauvegarder
					# surement dans un fichier spécial avec toutes les maps
					# il faudrait qu'on puisse après ouvrir chaque map
					# les prévisualiser ou même pouvoir les modifier
					"level(maze)"
					loop = False
					break

		if pygame.mouse.get_pressed()[0]:
			maze[y][x] = wall
		elif pygame.mouse.get_pressed()[2]:
			maze[y][x] = " "
		
		window.fill(BLACK)
		if pygame.mouse.get_focused():
			x, y = pygame.mouse.get_pos()
			x = int(x / 32)
			y = int(y / 32)
			window.fill((30, 30, 30), (x * 32, y * 32, 32, 32))
		niveau.maze_editor(maze, window)
		group_wall.draw(window)
		group_wall_spawn.draw(window)
		group_wall_spawn_special.draw(window)
		group_dot.draw(window)

		pygame.display.flip()

def menu_option():
	global show_fps
	window = pygame.display.set_mode((640, 640))
	y = 273
	loop = True
	while loop:
		for event in pygame.event.get():
			if event.type == QUIT or event.type == KEYDOWN and event.key == command_escape:
				loop = False
				break
			if event.type == KEYDOWN:
				if event.key == command_down:
					if y == 423:
						y = 273
					else:
						y += 50
				elif event.key == command_up:
					if y == 273:
						y = 423
					else:
						y -= 50
				elif event.key == command_return:
					if y == 273:
						menu_option_commands()
					elif y == 323:
						if show_fps == False:
							show_fps = True
						else:
							show_fps = False
					elif y == 373:
						pass
					elif y == 423:
						pass
			# display
			window.fill(BLACK)
			window.blit(text_pac_logo, (window.get_width() / 2 - 348 / 2, 70))
			window.blit(text_option_commands, (window.get_width() / 2 - 80, 270))
			pygame.draw.polygon(window, WHITE, ((window.get_width() / 2 - 105, y), (window.get_width() / 2 - 105, y + 10), (window.get_width() / 2 - 90, y + 5)))

			pygame.display.flip()
		pygame.time.Clock().tick(15)

def menu_option_commands():
	global command_return, command_down, command_left, command_right, command_up

	window = pygame.display.set_mode((640, 640))
	y = 273
	width = window.get_width() / 2 - 348 / 2
	width_input = window.get_width() / 2 + 150

	text_input_up = font_10.render(pygame.key.name(command_up), 0, WHITE)
	text_input_down = font_10.render(pygame.key.name(command_down), 0, WHITE)
	text_input_right = font_10.render(pygame.key.name(command_right), 0, WHITE)
	text_input_left = font_10.render(pygame.key.name(command_left), 0, WHITE)

	text_commands_up = font_10.render("up", 0, WHITE)
	text_commands_down = font_10.render("down", 0, WHITE)
	text_commands_right = font_10.render("right", 0, WHITE)
	text_commands_left = font_10.render("left", 0, WHITE)

	loop = True
	while loop:
		pygame.time.Clock().tick(30)
	
		for event in pygame.event.get():
			if event.type == QUIT or event.type == KEYDOWN and event.key == command_escape:
				loop = False
				break
			if event.type == KEYDOWN:
				if event.key == command_down:
					if y == 423:
						y = 273
					else:
						y += 50
				elif event.key == command_up:
					if y == 273:
						y = 423
					else:
						y -= 50
				elif event.key == command_return:
					if y == 273:
						text_commands_up = font_10.render("up", 0, YELLOW)
						text_input_up = font_10.render(pygame.key.name(command_up), 0, YELLOW)
						window.blit(text_input_up, (width_input, 270))
						window.blit(text_commands_up, (width, 270))
						pygame.display.flip()
						command_up, command_up_text = return_commands()
						text_input_up = font_10.render(command_up_text, 0, WHITE)
						text_commands_up = font_10.render("up", 0, WHITE)
					elif y == 323:
						text_commands_down = font_10.render("down", 0, YELLOW)
						text_input_down = font_10.render(pygame.key.name(command_down), 0, YELLOW)
						window.blit(text_input_down, (width_input, 320))
						window.blit(text_commands_down, (width, 320))
						pygame.display.flip()
						command_down, command_down_text = return_commands()
						text_input_down = font_10.render(command_down_text, 0, WHITE)
						text_commands_down = font_10.render("down", 0, WHITE)
					elif y == 373:
						text_commands_right = font_10.render("right", 0, YELLOW)
						text_input_right = font_10.render(pygame.key.name(command_right), 0, YELLOW)
						window.blit(text_input_right, (width_input, 370))
						window.blit(text_commands_right, (width, 370))
						pygame.display.flip()
						command_right, command_right_text = return_commands()
						text_input_right = font_10.render(command_right_text, 0, WHITE)
						text_commands_right = font_10.render("right", 0, WHITE)
					elif y == 423:
						text_commands_left = font_10.render("left", 0, YELLOW)
						text_input_left = font_10.render(pygame.key.name(command_left), 0, YELLOW)
						window.blit(text_commands_left, (width, 420))
						window.blit(text_input_left, (width_input, 420))
						pygame.display.flip()
						command_left, command_left_text = return_commands()
						text_input_left = font_10.render(command_left_text, 0, WHITE)
						text_commands_left = font_10.render("left", 0, WHITE)
		# display
		window.fill(BLACK)
		window.blit(text_pac_logo, (width, 70))
		window.blit(text_option_commands, (width, 240)) 
		window.blit(text_commands_input, (width_input - 50, 240)) 
		window.blit(text_commands_up, (width, 270)) 
		window.blit(text_input_up, (width_input, 270))
		window.blit(text_commands_down, (width, 320))
		window.blit(text_input_down, (width_input, 320))
		window.blit(text_commands_right, (width, 370))
		window.blit(text_input_right, (width_input, 370))
		window.blit(text_commands_left, (width, 420))
		window.blit(text_input_left, (width_input, 420))
		pygame.draw.polygon(window, WHITE, ((window.get_width() / 2 - 373 / 2, y), (window.get_width() / 2 - 373 / 2, y + 10), (window.get_width() / 2 - 358 / 2, y + 5)))

		pygame.display.flip()

def reset():
	pac.reset()
	shadow.reset()
	pinky.reset()
	pokey.reset()
	inky.reset()

# MAIN ------------------------------------------------------------------------------------------------------------------------------------ #
if __name__ == "__main__":
	pac = Pac(image_pac, 3, 4)
	shadow = Ghost(image_shadow, 4)
	pinky = Ghost(image_pinky, 4)
	pokey = Ghost(image_clyde, 4)
	inky = Ghost(image_inky, 4)
	menu_home()