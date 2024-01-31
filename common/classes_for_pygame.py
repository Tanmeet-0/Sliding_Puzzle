import pygame
from .movement import Vector, points_distance, point_angle_to_point

DEFAULT_FONT = "freesansbold.ttf"
DEFAULT_TEXT_SIZE = 20
DEFAULT_MOVE_SPEED = 1


class Box:
    def __init__(
        self,
        x: "int",
        y: "int",
        width: "int",
        height: "int",
        color: "tuple[int,int,int]",
        select_color: "tuple[int,int,int]",
        move_speed: "int" = DEFAULT_MOVE_SPEED,
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.default_color = color
        self.selected_color = select_color
        self.box_move_speed = move_speed
        self.box_destination = None
        self.selected = False
        self.can_be_selected = 1
        self.sound = None

    def draw(self, window: "pygame.Surface") -> "None":
        pygame.draw.rect(window, self.color, self.rect)

    def set_x(self, x: "int") -> "None":
        self.rect.x = x

    def set_y(self, y: "int") -> "None":
        self.rect.y = y

    def set_width(self, width: "int") -> "None":
        self.rect.width = width

    def set_height(self, height: "int") -> "None":
        self.rect.height = height

    def set_color(self, color: "tuple[int,int,int]") -> "None":
        self.default_color = color
        if not self.selected:
            self.color = self.default_color

    def set_select_color(self, color: "tuple[int,int,int]") -> "None":
        self.selected_color = color
        if self.selected:
            self.color = self.selected_color

    def set_move_speed(self, speed: "int") -> "None":
        self.box_move_speed = speed

    def get_x(self) -> "int":
        return self.rect.x

    def get_y(self) -> "int":
        return self.rect.y

    def get_width(self) -> "int":
        return self.rect.width

    def get_height(self) -> "int":
        return self.rect.height

    def get_rect(self) -> "pygame.Rect":
        return self.rect

    def get_color(self) -> "tuple[int,int,int]":
        return self.default_color

    def get_select_color(self) -> "tuple[int,int,int]":
        return self.selected_color

    def get_move_speed(self) -> "int":
        return self.box_move_speed

    def is_selected(self) -> "bool":
        return self.selected

    def select(self) -> "None":
        if self.can_be_selected == 1:
            if not self.selected:
                self.color = self.selected_color
                self.selected = True

    def deselect(self) -> "None":
        if self.can_be_selected == 1:
            if self.selected:
                self.color = self.default_color
                self.selected = False

    def allow_selection(self) -> "None":
        self.can_be_selected = 1

    def deny_selection(self) -> "None":
        self.can_be_selected = 0

    def collide_point(self, x: "int", y: "int") -> "bool":
        return self.rect.collidepoint(x, y)

    def exchange_position(self, other: "Box") -> "None":
        tx = self.get_x()
        ty = self.get_y()
        self.set_x(other.get_x())
        self.set_y(other.get_y())
        other.set_x(tx)
        other.set_y(ty)

    def set_destination(self, x: "int", y: "int") -> "None":
        self.box_destination = (x, y)

    def move_towards_destination(self) -> "None":
        # does nothing if there is no destination
        if self.box_destination != None:
            distance = points_distance(
                self.rect.x,
                self.rect.y,
                self.box_destination[0],
                self.box_destination[1],
            )
            if distance < self.box_move_speed:
                self.set_x(self.box_destination[0])
                self.set_y(self.box_destination[1])
                self.box_destination = None
                if self.sound != None:
                    self.sound.play()
            else:
                angle = point_angle_to_point(
                    self.rect.x,
                    self.rect.y,
                    self.box_destination[0],
                    self.box_destination[1],
                )
                diff = Vector(0, 0)
                diff.set_angle(angle)
                diff.set_length(self.box_move_speed)
                new_x = self.rect.x + int(diff.get_x())
                new_y = self.rect.y + int(diff.get_y())
                self.set_x(new_x)
                self.set_y(new_y)

    def destination_reached(self) -> "bool":
        return self.box_destination == None

    def set_sound(self, filename: "str"):
        self.sound = pygame.mixer.Sound(file=filename)

    def remove_sound(self):
        self.sound = None

    def set_sound_volume(self, value: "float"):
        if self.sound != None:
            self.sound.set_volume(value)


class Text:
    def __init__(
        self,
        center: "tuple[int,int]",
        text: "str",
        text_color: "tuple[int,int,int]",
        text_size: "int" = DEFAULT_TEXT_SIZE,
        font: "str" = DEFAULT_FONT,
        move_speed: "int" = DEFAULT_MOVE_SPEED,
    ):
        self.center = center
        self.text = str(text)  # for safety
        self.text_color = text_color
        self.text_size = text_size
        self.font = font
        self.text_move_speed = move_speed
        self.text_destination = None
        self.create_text()
        self.sound = None

    def create_text(self) -> "None":
        font = pygame.font.Font(self.font, self.text_size)
        self.text_surface = font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = self.center

    def draw(self, window: "pygame.Surface") -> "None":
        window.blit(self.text_surface, self.text_rect)

    def set_center(self, center: "tuple[int,int]") -> "None":
        self.center = center
        self.text_rect.center = self.center

    def set_text(self, text: "str") -> "None":
        self.text = str(text)  # For safety
        self.create_text()

    def set_text_color(self, text_color: "tuple[int,int,int]") -> "None":
        self.text_color = text_color
        self.create_text()

    def set_text_size(self, text_size: "int") -> "None":
        self.text_size = text_size
        self.create_text()

    def set_font(self, font: "str") -> "None":
        self.font = font
        self.create_text()

    def set_move_speed(self, speed: "int") -> "None":
        self.text_move_speed = speed

    def get_center(self) -> "tuple[int,int]":
        return self.center

    def get_text(self) -> "str":
        return self.text

    def get_text_color(self) -> "tuple[int,int,int]":
        return self.text_color

    def get_text_size(self) -> "int":
        return self.text_size

    def get_font(self) -> "str":
        return self.font

    def get_text_rect(self) -> "pygame.Rect":
        return self.text_rect

    def get_move_speed(self) -> "int":
        return self.text_move_speed

    def exchange_position(self, other: "Text"):
        t_center = self.get_center()
        self.set_center(other.get_center())
        other.set_center(t_center)

    def set_destination(self, x: "int", y: "int") -> "None":
        self.text_destination = (x, y)

    def move_towards_destination(self) -> "None":
        if self.text_destination != None:
            distance = points_distance(
                self.center[0],
                self.center[1],
                self.text_destination[0],
                self.text_destination[1],
            )
            if distance < self.text_move_speed:
                self.set_center(self.text_destination)
                self.text_destination = None
            else:
                angle = point_angle_to_point(
                    self.center[0],
                    self.center[1],
                    self.text_destination[0],
                    self.text_destination[1],
                )
                diff = Vector(0, 0)
                diff.set_angle(angle)
                diff.set_length(self.text_move_speed)
                new_x = self.center[0] + int(diff.get_x())
                new_y = self.center[1] + int(diff.get_y())
                new_center = (new_x, new_y)
                self.set_center(new_center)

    def destination_reached(self) -> "bool":
        return self.text_destination == None

    def set_sound(self, filename: "str"):
        self.sound = pygame.mixer.Sound(file=filename)

    def remove_sound(self):
        self.sound = None

    def set_sound_volume(self, value: "float"):
        if self.sound != None:
            self.sound.set_volume(value)


class Box_with_text(Box, Text):
    def __init__(
        self,
        text: "str",
        x: "int",
        y: "int",
        width: "int",
        height: "int",
        color: "tuple[int,int,int]",
        text_color: "tuple[int,int,int]",
        select_color: "tuple[int,int,int]",
        text_size: "int" = DEFAULT_TEXT_SIZE,
        font: "str" = DEFAULT_FONT,
        move_speed: "int" = DEFAULT_MOVE_SPEED,
    ):
        Box.__init__(
            self, x, y, width, height, color, select_color, move_speed=move_speed
        )
        Text.__init__(self, (0, 0), text, text_color, text_size, font)

    def draw(self, window: "pygame.Surface") -> "None":
        Text.set_center(self, self.rect.center)
        Box.draw(self, window)
        Text.draw(self, window)

    def exchange_position(self, other: "Box") -> "None":
        Box.exchange_position(self, other)

    def set_move_speed(self, speed: "int") -> "None":
        Box.set_move_speed(self, speed)

    def set_destination(self, x: "int", y: "int") -> "None":
        Box.set_destination(self, x, y)

    def move_towards_destination(self) -> "None":
        Box.move_towards_destination(self)

    def destination_reached(self) -> "bool":
        return Box.destination_reached(self)

    def set_sound(self, filename: "str"):
        Box.set_sound(self, filename)

    def remove_sound(self):
        Box.remove_sound(self)

    def set_sound_volume(self, value: "float"):
        Box.set_sound_volume(self, value)
