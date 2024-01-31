from common.colors import *
import pygame, random
from common.classes_for_pygame import Text, Box_with_text


def main():
    pygame.init()
    WIDTH, HEIGHT = 1000, 500
    mouse_x, mouse_y = 0, 0
    mouse_pressed = 0
    PLAYING = "PLAYING"
    WIN = "WIN"
    WIN_ANIMATION = "WIN_ANIMATION"
    MOVING = "MOVING"
    state = PLAYING

    rows, columns = 5, 3
    assert rows * columns > 2, "Number Of Tiles Should Be Greater Than 2"
    box_color = Saddle_Brown
    box_text_color = White
    box_selected_color = Red
    x_margin = WIDTH * 10 // 100
    y_margin = HEIGHT * 10 // 100
    box_gap = 5
    speed = 15
    box_sound_filename = "slide_puzzle_sounds\\impactWood_light_001.ogg"
    grid, solved_grid = create_grid(
        WIDTH,
        HEIGHT,
        rows,
        columns,
        box_color,
        box_text_color,
        box_selected_color,
        x_margin,
        y_margin,
        box_gap,
        speed,
        box_sound_filename,
    )
    hidden_box = grid[rows - 1][columns - 1]
    moving_boxes = []
    randomize_gird(grid, rows, columns, hidden_box)

    BG = Blue_Voilet
    CLOCK = pygame.time.Clock()
    FPS = 60
    DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("SLIDE PUZZLE")
    start_alpha = 0
    active_alpha = start_alpha
    end_alpha = 220
    increment_alpha = 5
    trans_surface = pygame.Surface((WIDTH, HEIGHT))
    trans_surface.set_alpha(active_alpha)
    trans_surface.fill(Black)
    win_text = Text((WIDTH // 2, HEIGHT // 2), "YOU WIN!", Deep_Sky_Blue, text_size=100)
    play_again_box = Box_with_text(
        "Play Again!",
        WIDTH // 2 - (WIDTH * 20 // 100),
        HEIGHT // 2 + (HEIGHT * 10 // 100),
        WIDTH * 15 // 100,
        HEIGHT * 10 // 100,
        Orange_Red,
        Black,
        Green,
        25,
    )
    quit_game_box = Box_with_text(
        "Quit!",
        WIDTH // 2 + (WIDTH * 5 // 100),
        HEIGHT // 2 + (HEIGHT * 10 // 100),
        WIDTH * 15 // 100,
        HEIGHT * 10 // 100,
        Orange_Red,
        Black,
        Maroon,
        25,
    )

    while True:
        CLOCK.tick(FPS)
        DISPLAY.fill(BG)
        mouse_pressed = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit_game()
                if event.key == pygame.K_SPACE:
                    randomize_gird(grid, rows, columns, hidden_box)
            if event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pressed = 1

        # Collision Detection Loop
        if state == PLAYING:
            for r in range(rows):
                for c in range(columns):
                    box = grid[r][c]
                    if box != hidden_box:
                        if box.collide_point(mouse_x, mouse_y):
                            box.select()
                            if mouse_pressed:
                                mouse_pressed = 0
                                neighbours = get_neighbours(grid, c, r)
                                for diff, neighbour in neighbours.items():
                                    if neighbour == hidden_box:
                                        swap_box_with_box_in_grid(grid, c, r, diff)
                                        box.set_destination(
                                            hidden_box.get_x(), hidden_box.get_y()
                                        )
                                        hidden_box.set_destination(
                                            box.get_x(), box.get_y()
                                        )
                                        moving_boxes.append(box)
                                        moving_boxes.append(hidden_box)
                                        state = MOVING
                        else:
                            box.deselect()
        if state == PLAYING:
            if has_won(grid, rows, columns, solved_grid):
                state = WIN_ANIMATION
                for row in grid:
                    for box in row:
                        box.deselect()

        if state == MOVING:
            moving_boxes: "list[Box_with_text]"
            for box in moving_boxes:
                box.move_towards_destination()
            for box in moving_boxes:
                if not box.destination_reached():
                    break
            else:
                moving_boxes.clear()
                state = PLAYING

        # Draw Loop
        for grid_row in grid:
            for box in grid_row:
                if box != hidden_box:
                    box.draw(DISPLAY)

        if state == WIN_ANIMATION:
            if active_alpha >= end_alpha:
                state = WIN
            else:
                active_alpha += increment_alpha
                trans_surface.set_alpha(active_alpha)
                DISPLAY.blit(trans_surface, (0, 0))

        if state == WIN:
            if play_again_box.collide_point(mouse_x, mouse_y):
                play_again_box.select()
                if mouse_pressed:
                    randomize_gird(grid, rows, columns, hidden_box)
                    active_alpha = start_alpha
                    state = PLAYING
            else:
                play_again_box.deselect()
            if quit_game_box.collide_point(mouse_x, mouse_y):
                quit_game_box.select()
                if mouse_pressed:
                    quit_game()
            else:
                quit_game_box.deselect()

            DISPLAY.blit(trans_surface, (0, 0))
            win_text.draw(DISPLAY)
            play_again_box.draw(DISPLAY)
            quit_game_box.draw(DISPLAY)

        pygame.display.update()


def create_grid(
    WIDTH: "int",
    HEIGHT: "int",
    rows: "int",
    columns: "int",
    box_color: "tuple[int,int,int]",
    box_text_color: "tuple[int,int,int]",
    box_selected_color: "tuple[int,int,int]",
    x_margin: "int",
    y_margin: "int",
    box_gap: "int",
    speed: "int",
    sound_filename: "str"=None,
) -> "tuple[list[list[Box_with_text]],list[list[str]]]":
    box_width = (WIDTH - (x_margin * 2) - (box_gap * (columns - 1))) // columns
    # from total_width remove margin for both sides then remove the gaps between boxes
    # then divide the remaining by no of boxes in each row to get box_width
    box_height = (HEIGHT - (y_margin * 2) - (box_gap * (rows - 1))) // rows
    # from total_height remove margin for both sides then remove the gaps between boxes
    # then divide the remaining by no of boxes in each column to get box_height
    assert box_width > 0 and box_height > 0, "Box Width Or Height Less Than 1"
    grid = []
    grid_row = []
    solved_grid = []
    solved_row = []
    for r in range(rows):
        for c in range(columns):
            text = str(c + (r * columns) + 1)
            x = x_margin + (c * box_width) + (c * box_gap)
            y = y_margin + (r * box_height) + (r * box_gap)
            box = Box_with_text(
                text,
                x,
                y,
                box_width,
                box_height,
                box_color,
                box_text_color,
                box_selected_color,
                move_speed=speed,
            )
            if sound_filename != None:
                box.set_sound(sound_filename)
                box.set_sound_volume(0.3)
            grid_row.append(box)
            solved_row.append(text)
        grid.append(grid_row.copy())
        grid_row.clear()
        solved_grid.append(solved_row.copy())
        solved_row.clear()
    return (grid, solved_grid)


def get_neighbours(grid: "list[list]", x: "int", y: "int") -> "dict":
    neighbours = {(-1, 0): None, (1, 0): None, (0, -1): None, (0, 1): None}
    for diff in neighbours.keys():
        nx = x + diff[0]
        ny = y + diff[1]
        if (-1 < nx < len(grid[0])) and (-1 < ny < len(grid)):
            neighbours[diff] = grid[ny][nx]
    return neighbours


def swap_box_with_box_in_grid(
    grid: "list[list[Box_with_text]]",
    x: "int",
    y: "int",
    diff: "tuple[int,int]",
) -> "None":
    nx = x + diff[0]
    ny = y + diff[1]
    grid[y][x], grid[ny][nx] = grid[ny][nx], grid[y][x]


def has_won(
    grid: "list[list[Box_with_text]]",
    rows: "int",
    columns: "int",
    solved_grid: "list[list[str]]",
) -> "bool":
    for r in range(rows):
        for c in range(columns):
            box = grid[r][c]
            text = solved_grid[r][c]
            if box.get_text() != text:
                return False
    return True


def quit_game():
    pygame.quit()
    exit()


def randomize_gird(
    grid: "list[list[Box_with_text]]",
    rows: "int",
    columns: "int",
    hidden_box: "Box_with_text",
) -> "None":
    swaps = (rows * columns) ** 2
    if swaps > 200000:
        swaps = 200000
    for i in range(swaps):
        x, y = get_position_in_gird(grid, rows, columns, hidden_box)
        neighbours = get_neighbours(grid, x, y)
        diff = None
        neighbour = None
        while neighbour == None:
            diff = random.choice(tuple(neighbours.keys()))
            neighbour = neighbours[diff]
        hidden_box.exchange_position(neighbour)
        swap_box_with_box_in_grid(grid, x, y, diff)


def get_position_in_gird(
    grid: "list[list[Box_with_text]]", rows: "int", columns: "int", box: "Box_with_text"
) -> "tuple[int,int]":
    for r in range(rows):
        for c in range(columns):
            if grid[r][c] == box:
                return (c, r)
    assert 1 < 0, "Element Not In Grid"


if __name__ == "__main__":
    main()
