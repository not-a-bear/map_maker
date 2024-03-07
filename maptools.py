import pygame
import random
pygame.init()

# colors
VOID = (0, 0, 0)
NEON = (15, 255, 80)
WATER = (115, 200, 255)
ISLAND = (153, 76, 0)
COAST = (247, 224, 170)
LOWLANDS = (169, 215, 91)
FOOTHILLS = (215, 190, 91)
HILLS = (144, 120, 91)
MOUNTAIN = (150, 150, 150)

# screen parameters
WIDTH, HEIGHT = 1280, 720
TILE_SIZE = 20
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE
FPS = 60

BG = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.SysFont("Arial", 10)

clock = pygame.time.Clock()

def adjust_grid(positions):
    all_neighbors = set()
    new_positions = set()

    for position in positions:
        neighbors = get_neighbors(position)
        all_neighbors.update(neighbors)

        neighbors = list(filter(lambda x: x in positions, neighbors))

        if len(neighbors) in [2, 5, 7, 8]:
            new_positions.add(position)
        elif len(neighbors) == 0:
            if random.randint(0,15) > 1:
                new_positions.add(position)
        

    for position in all_neighbors:
        neighbors = get_neighbors(position)
        neighbors = list(filter(lambda x: x in positions, neighbors))

        if len(neighbors) in [0, 3, 6, 7, 8]:
            new_positions.add(position)

    return new_positions


def get_neighbors(pos):
    x, y = pos
    neighbors = []
    for dx in [-1, 0, 1]:
        if x + dx < 0 or x + dx > GRID_WIDTH:
            continue
        for dy in [-1, 0, 1]:
            if y + dy < 0 or y + dy > GRID_HEIGHT:
                continue
            if dx == 0 and dy == 0:
                continue

            neighbors.append((x + dx, y + dy))

    return neighbors


def get_neighbors_neighbors(pos):
    x, y = pos
    neighbors_neighbors = []
    for dx in [-3, -2, -1, 0, 1, 2, 3]:
        if x + dx < 0 or x + dx > GRID_WIDTH:
            continue
        for dy in [-3, -2, -1, 0, 1, 2, 3]:
            if y + dy < 0 or y + dy > GRID_HEIGHT:
                continue
            if dx == 0 and dy == 0:
                continue

            neighbors_neighbors.append((x + dx, y + dy))

    return neighbors_neighbors


def fill_map(positions):
    BG.fill(WATER)

    for position in positions:
        col, row = position
        top_left = (col * TILE_SIZE, row * TILE_SIZE)
        neighbors = get_neighbors(position)
        neighbors = list(filter(lambda x: x in positions, neighbors))
        
        if len(neighbors) in [1, 2, 3]:
            pygame.draw.rect(BG, LOWLANDS, (*top_left, TILE_SIZE, TILE_SIZE))
        elif len(neighbors) in [4, 5, 6, 7]:
            pygame.draw.rect(BG, HILLS, (*top_left, TILE_SIZE, TILE_SIZE))
        elif len(neighbors) == 8:
            pygame.draw.rect(BG, MOUNTAIN, (*top_left, TILE_SIZE, TILE_SIZE))
        elif len(neighbors) == 0:
            pygame.draw.rect(BG, ISLAND, (*top_left, TILE_SIZE, TILE_SIZE))

        pygame.display.update()


# this is the version that returns numbers
def numbers_map(positions):
    mapped = True
    BG.fill(WATER)
    neighbors = set()
    neighbors_neighbors = set()
    # length = 0
    
    for position in positions:
        col, row = position
        # top_left = (col * TILE_SIZE, row * TILE_SIZE)
        neighbors = get_neighbors(position)
        neighbors = list(filter(lambda x: x in positions, neighbors))
        neighbors_neighbors = get_neighbors_neighbors(position)
        neighbors_neighbors = list(filter(lambda x: x in positions, neighbors_neighbors))
        neighbors_text = FONT.render(f'{len(neighbors_neighbors)}', 1, 'red')
        # if len(neighbors) < 7:
        #     pygame.draw.rect(BG, COAST, (*top_left, TILE_SIZE, TILE_SIZE))
        # else:
        BG.blit(neighbors_text, (col * TILE_SIZE, row * TILE_SIZE))
        pygame.display.update()

def numbers_file(positions, file_path):
    mapped = True
    neighbors = set()
    neighbors_neighbors = set()

    with open(file_path, "w") as text_file:
        for position in positions:
            col, row = position
            neighbors = get_neighbors(position)
            neighbors = list(filter(lambda x: x in positions, neighbors))
            neighbors_neighbors = get_neighbors_neighbors(position)
            neighbors_neighbors = list(filter(lambda x: x in positions, neighbors_neighbors))
            text_file.write(f'({col}, {row}) :{len(neighbors_neighbors)}; ')
            # BG.blit(neighbors_text, (col * TILE_SIZE, row * TILE_SIZE))

def map_dict(positions):
    mapped = True
    neighbors = set()
    neighbors_neighbors = set()
    map_dict = {}

    # with open(file_path, "w") as text_file:
    for position in positions:
        col, row = position
        neighbors = get_neighbors(position)
        neighbors = list(filter(lambda x: x in positions, neighbors))
        neighbors_neighbors = get_neighbors_neighbors(position)
        neighbors_neighbors = list(filter(lambda x: x in positions, neighbors_neighbors))
        key = (col, row)
        if len(neighbors) < 7:
            value = 'coast'
        else:
            length = len(neighbors_neighbors)
            if length == 48:
                value = 'mountain'
            elif length > 44:
                value = 'hills'
            elif length > 37:
                value = 'foothills'
            else:
                value = 'lowlands'
        map_dict[key] = value
        # text_file.write(f'({col}, {row}) :{len(neighbors_neighbors)}; ')

    return map_dict

def map_from_numbers(map_dict):
    mapped = True
    BG.fill(WATER)

    for key in map_dict.keys():
        col, row = key
        value = map_dict.get(key)
        top_left = (col * TILE_SIZE, row * TILE_SIZE)

        if value == 'mountain':
            pygame.draw.rect(BG, MOUNTAIN, (*top_left, TILE_SIZE, TILE_SIZE))
        elif value == 'hills':
            pygame.draw.rect(BG, HILLS, (*top_left, TILE_SIZE, TILE_SIZE))
        elif value == 'foothills':
            pygame.draw.rect(BG, FOOTHILLS, (*top_left, TILE_SIZE, TILE_SIZE))
        elif value == 'coast':
            pygame.draw.rect(BG, COAST, (*top_left, TILE_SIZE, TILE_SIZE))
        else:
            pygame.draw.rect(BG, LOWLANDS, (*top_left, TILE_SIZE, TILE_SIZE))

        pygame.display.update()

    