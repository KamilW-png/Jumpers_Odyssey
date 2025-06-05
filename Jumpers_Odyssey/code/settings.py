import pygame
from os import walk
from os.path import join
from pytmx.util_pygame import load_pygame

if not hasattr(pygame, 'FRect'):
    pygame.FRect = pygame.Rect

WINDOW_WIDTH, WINDOW_HEIGHT = 1920, 1080
# WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
TILE_SIZE = 64
FRAMERATE = 60
BG_COLOR = '#fcdfcd'

