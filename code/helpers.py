import csv
import os
import pygame


def import_csv(path):
	data = []
	with open(path) as file:
		reader = csv.reader(file)
		for row in reader:
			data.append(row)

	return data


def import_level(path):
	map_data = {}
	for file in tuple(os.walk(path))[0][2]:
		key = file.lstrip("map_").rstrip(".csv")
		map_data[key] = import_csv(os.path.join(path, file))

	return map_data


def import_sprite_sheet(path, size_of_one_frame, scale=None):
	sheet = pygame.image.load(path).convert_alpha()
	width, height = sheet.get_size()
	w, h = size_of_one_frame
	rows = height//h
	cols = width//w
	frames = []
	for row in range(rows):
		for col in range(cols):
			frame = pygame.Surface(size_of_one_frame, pygame.SRCALPHA)
			crop_rect = pygame.Rect(col * w, row * h, w, h)
			frame.blit(sheet, (0, 0), crop_rect)
			if scale:
				transformed_scale = int(size_of_one_frame[0] * scale), int(size_of_one_frame[1] * scale)
				frame = pygame.transform.scale(frame, transformed_scale)
			frames.append(frame)

	return frames


def import_character(path, scale=1):
	anims = {}
	path = os.path.join(path, "SeparateAnim")
	for sheetname in list(os.walk(path))[0][2]:
		key = sheetname.replace(".png", "")
		parsed_sheet = import_sprite_sheet(os.path.join(path, sheetname), (16, 16), scale)
		if key in ["Attack", "Idle", "Jump"]:
			anims[key] = {}
			anims[key]["Down"] = parsed_sheet[0]
			anims[key]["Up"] = parsed_sheet[1]
			anims[key]["Left"] = parsed_sheet[2]
			anims[key]["Right"] = parsed_sheet[3]

		elif key in ["Dead", "Item", "Special1", "Special2"]:
			anims[key] = parsed_sheet

		else:
			anims[key] = {}
			anims[key]["Down"] = [parsed_sheet[0], parsed_sheet[4], parsed_sheet[8], parsed_sheet[12]]
			anims[key]["Up"] = [parsed_sheet[1], parsed_sheet[5], parsed_sheet[9], parsed_sheet[13]]
			anims[key]["Left"] = [parsed_sheet[2], parsed_sheet[6], parsed_sheet[10], parsed_sheet[14]]
			anims[key]["Right"] = [parsed_sheet[3], parsed_sheet[7], parsed_sheet[11], parsed_sheet[15]]

	anims["shadow"] = import_sprite_sheet("../assets/Actor/Characters/Shadow.png", (12, 7), scale)[0]

	return anims
