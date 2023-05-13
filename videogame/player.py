"""Player objects for the scenes."""

import math
from random import randint
import pygame
import rgbcolors
import assets


# Taken from the pygame examples
def load_image(filename, colorkey=None, scale=1):
    image = pygame.image.load(filename)
    image = image.convert()

    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pygame.transform.scale(image, size)

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image, image.get_rect()


class Player(pygame.sprite.Sprite):
    """Class representing player with a bounding rect."""

    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(assets.get('dragon'), -1)
        self._position = position
        self.rect.center = self._position
        self._radius = 25
        self._color = rgbcolors.purple2
        self._velocity = pygame.math.Vector2(0, 0)

    def update(self):
        "Updates"
        newv = self._position.x + self._velocity.x
        if newv > 0 and newv < 800:
            self._position += self._velocity
        self.rect.center = self._position

    @property
    def position(self):
        """Returns position"""
        return self._position

    def stop(self):
        """Stops movement"""
        self._velocity = pygame.math.Vector2(0, 0)

    def move_left(self):
        """Moves left"""
        self._velocity = pygame.math.Vector2(-10, 0)

    def move_right(self):
        """Moves right"""
        self._velocity = pygame.math.Vector2(10, 0)

    def draw(self, screen):
        """Draw the Player to screen."""
        pygame.draw.circle(screen, self._color, self._position, self._radius)


class Bullet:
    """Class for Player's bullets"""
    def __init__(self, position, target_position, speed):
        self._position = pygame.math.Vector2(position)
        self._target_position = pygame.math.Vector2(target_position)
        self._speed = speed
        self._color = rgbcolors.mult_color(self._speed, rgbcolors.blue)
        self._radius = 10

    @property
    def rect(self):
        """Return bounding rect."""
        left = self._position.x - self._radius
        top = self._position.y - self._radius
        width = 2 * self._radius
        return pygame.Rect(left, top, width, width)

    def should_die(self):
        """If bullet should disappear"""
        squared_distance = (self._position -
                            self._target_position).length_squared()
        return math.isclose(squared_distance, 0.0, rel_tol=1e-01)

    def update(self, delta_time):
        """Updates bullet postion"""
        self._position.move_towards_ip(self._target_position,
                                       self._speed * delta_time)

    def draw(self, screen):
        """Draw the circle to screen."""
        pygame.draw.circle(screen, self._color, self._position, self._radius)


class Alien(pygame.sprite.Sprite):
    """Class representing an alien ship with a bounding rect."""

    def __init__(self, center_x, center_y, radius, color, name="None"):
        self._center_x = center_x
        self._center_y = center_y
        self._radius = radius
        self._color = color
        self._name = name
        self._is_exploding = False

    @property
    def radius(self):
        """Return the circle's radius"""
        return self._radius

    @property
    def center(self):
        """Return the circle's center."""
        return pygame.Vector2(self._center_x, self._center_y)

    @property
    def rect(self):
        """Return bounding rect."""
        left = self._center_x - self._radius
        top = self._center_y - self._radius
        width = 2 * self._radius
        return pygame.Rect(left, top, width, width)

    @property
    def width(self):
        """Return the width of the bounding box the circle is in."""
        return 2 * self._radius

    @property
    def height(self):
        """Return the height of the bounding box the circle is in."""
        return 2 * self._radius

    @property
    def is_exploding(self):
        """If explodes"""
        return self._is_exploding

    @is_exploding.setter
    def is_exploding(self, val):
        self._is_exploding = val

    def draw(self, screen):
        """Draw the circle to screen."""
        pygame.draw.circle(screen, self._color, self.center, self._radius)

    def __repr__(self):
        """Circle stringify."""
        return f'Circle({self._center_x}, {self._center_y},\
        {self._radius}, {self._color}, "{self._name}")'


class AlienBullet:
    """Class for Alien's bullets"""
    def __init__(self, position, target_position, speed):
        self._position = pygame.math.Vector2(position)
        self._target_position = pygame.math.Vector2(target_position)
        self._speed = speed
        self._color = rgbcolors.mult_color(self._speed, rgbcolors.red)
        self._radius = 10

    @property
    def rect(self):
        """Return bounding rect."""
        left = self._position.x - self._radius
        top = self._position.y - self._radius
        width = 2 * self._radius
        return pygame.Rect(left, top, width, width)

    def should_die(self):
        """If bullet should disappear"""
        squared_distance = (self._position -
                            self._target_position).length_squared()
        return math.isclose(squared_distance, 0.0, rel_tol=1e-01)

    def update(self, delta_time):
        """Update alien bullet position"""
        self._position.move_towards_ip(self._target_position,
                                       self._speed * delta_time)

    def draw(self, screen):
        """Draw the circle to screen."""
        pygame.draw.circle(screen, self._color, self._position, self._radius)


class Shield:
    """Class representing player with a bounding rect."""

    def __init__(self, position):
        self._position = position
        self._radius = 25
        self._color = rgbcolors.purple2
        self._velocity = pygame.math.Vector2(0, 0)

    @property
    def radius(self):
        """Return the circle's radius"""
        return self._radius

    @property
    def position(self):
        """Returns position"""
        return self._position

    def draw(self, screen):
        """Draw the Player to screen."""
        pygame.draw.rect(screen, self._color,
                         pygame.Rect(200, 600, 50, 25))
        pygame.draw.rect(screen, self._color,
                         pygame.Rect(375, 600, 50, 25))
        pygame.draw.rect(screen, self._color,
                         pygame.Rect(550, 600, 50, 25))
