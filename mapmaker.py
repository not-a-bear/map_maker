import sys, random
import pygame
import maptools
pygame.init()

# colors
VOID = (0, 0, 0)
NEON = (15, 255, 80)
WATER = (115, 200, 255)
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

clock = pygame.time.Clock()

FONT = pygame.font.SysFont("Arial", 10)


def gen(num):
    return set([(random.randrange(0, GRID_WIDTH), random.randrange(0, GRID_HEIGHT)) for _ in range(num)])


def draw_grid(positions):
    for position in positions:
        col, row = position
        top_left = (col * TILE_SIZE, row * TILE_SIZE)
        pygame.draw.rect(BG, NEON, (*top_left, TILE_SIZE, TILE_SIZE))

    for row in range(GRID_HEIGHT):
        pygame.draw.line(BG, VOID, (0, row * TILE_SIZE), (WIDTH, row * TILE_SIZE))

    for col in range(GRID_WIDTH):
        pygame.draw.line(BG, VOID, (col * TILE_SIZE, 0), (col * TILE_SIZE, HEIGHT))


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
    neighbors = set()
    neighbors_neighbors = set()
    length = 0
    
    for position in positions:
        col, row = position
        top_left = (col * TILE_SIZE, row * TILE_SIZE)
        neighbors = get_neighbors(position)
        neighbors = list(filter(lambda x: x in positions, neighbors))
        neighbors_neighbors = get_neighbors_neighbors(position)
        neighbors_neighbors = list(filter(lambda x: x in positions, neighbors_neighbors))

        if len(neighbors) < 7:
            pygame.draw.rect(BG, COAST, (*top_left, TILE_SIZE, TILE_SIZE))
        else:
            length = len(neighbors_neighbors)
            if length == 48:
                pygame.draw.rect(BG, MOUNTAIN, (*top_left, TILE_SIZE, TILE_SIZE))
            elif length > 44:
                pygame.draw.rect(BG, HILLS, (*top_left, TILE_SIZE, TILE_SIZE))
            elif length > 37:
                pygame.draw.rect(BG, FOOTHILLS, (*top_left, TILE_SIZE, TILE_SIZE))
            else:
                pygame.draw.rect(BG, LOWLANDS, (*top_left, TILE_SIZE, TILE_SIZE))

        pygame.display.update()


def main():
    run = True
    playing = False
    mapped = False
    count = 0
    update_frequency = 20
    
    positions = set()

    while run:
        clock.tick(FPS)

        if playing:
            count += 1

        if count >= update_frequency:
            count = 0
            positions = adjust_grid(positions)

        pygame.display.set_caption("Playing" if playing else "Paused")

        if mapped == False:

            BG.fill(VOID)
            draw_grid(positions)
            pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // TILE_SIZE
                row = y // TILE_SIZE
                pos = (col, row)

                if pos in positions:
                    positions.remove(pos)
                else:
                    positions.add(pos)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:

                    if playing == False:
                        mapped = False
                    
                    playing = not playing
                    
                if event.key == pygame.K_c:
                    positions = set()
                    playing = False
                    mapped = False
                    count = 0

                if event.key == pygame.K_g:
                    positions = gen(random.randrange(5, 6) * GRID_WIDTH)

                if event.key == pygame.K_m:
                    fill_map(positions)
                    mapped = True

                if event.key == pygame.K_a:
                    mapped = True
                    positions = gen(random.randrange(5, 6) * GRID_WIDTH)

                    for _ in range(18):
                        positions = adjust_grid(positions)
                    
                    fill_map(positions)

                if event.key == pygame.K_p:
                    maptools.numbers_map(positions)

                if event.key == pygame.K_f:
                    maptools.numbers_file(positions, 'MapMaker/test.tx')

                if event.key == pygame.K_s:
                    map_dict = maptools.map_dict(positions)
                
                if event.key == pygame.K_r:
                    maptools.map_from_numbers(map_dict)

      
    pygame.quit()


if __name__ == "__main__":
    main()



