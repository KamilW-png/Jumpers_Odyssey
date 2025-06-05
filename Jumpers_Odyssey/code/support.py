from settings import *
from os.path import join, dirname

def import_image(*path, format = 'png', alpha = True):
    base_dir = dirname(__file__)
    full_path = join(base_dir, *path) + f'.{format}'
    return pygame.image.load(full_path).convert_alpha() if alpha else pygame.image.load(full_path).convert()

def import_folder(*path):
    frames = []
    base_dir = dirname(__file__)
    folder_root = join(base_dir, *path)
    for folder_path, _, file_names in walk(folder_root):
        for file_name in sorted(file_names, key=lambda name: int(name.split('.')[0])):
            full_path = join(folder_path, file_name)
            frames.append(pygame.image.load(full_path).convert_alpha())
    return frames

def audio_importer(*path):
    audio_dict = {}
    base_dir = dirname(__file__)
    folder_root = join(base_dir, *path)
    for folder_path, _, file_names in walk(folder_root):
        for file_name in file_names:
            full_path = join(folder_path, file_name)
            key = file_name.rsplit('.', 1)[0]
            audio_dict[key] = pygame.mixer.Sound(full_path)
    return audio_dict
