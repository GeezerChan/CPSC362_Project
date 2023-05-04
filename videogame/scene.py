# Andy Huynh
# CPSC 362
# ahuynh86@csu.fullerton.edu
# Project

"""Scene objects for making games with PyGame."""
import os
import pygame
import rgbcolors
from random import randint, uniform

# If you're interested in using abstract base classes, feel free to rewrite
# these classes.
# For more information about Python Abstract Base classes, see
# https://docs.python.org/3.8/library/abc.html

def random_position(max_width, max_height):
    return pygame.math.Vector2(randint(0, max_width-1), randint(0, max_height-1))

class SceneManager:
    def __init__(self):
        self._scene_dict = {}
        self._current_scene = None
        self._next_scene = None
        # This is a safety to ensure that calling
        # next() twice in a row without calling set_next_scene()
        # will raise StopIteration.
        self._reloaded = True

    def set_next_scene(self, key):
        self._next_scene = self._scene_dict[key]
        self._reloaded = True

    def add(self, scene_list):
        for (index, scene) in enumerate(scene_list):
            self._scene_dict[str(index)] = scene
        self._current_scene = self._scene_dict['0']

    def __iter__(self):
        return self

    def __next__(self):
        if self._next_scene and self._reloaded:
            self._reloaded = False
            return self._next_scene
        else:
            raise StopIteration

class Scene:
    """Base class for making PyGame Scenes."""

    def __init__(self, screen, background_color, soundtrack=None):
        """Scene initializer"""
        self._screen = screen
        self._background = pygame.Surface(self._screen.get_size())
        self._background.fill(background_color)
        self._frame_rate = 60
        self._is_valid = True
        self._soundtrack = soundtrack
        self._render_updates = None

    def draw(self):
        """Draw the scene."""
        self._screen.blit(self._background, (0, 0))

    def process_event(self, event):
        """Process a game event by the scene."""
        # This should be commented out or removed since it generates a lot of noise.
        # print(str(event))
        if event.type == pygame.QUIT:
            print("Good Bye!")
            self._is_valid = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            print("Bye bye!")
            self._is_valid = False
       
    def is_valid(self):
        """Is the scene valid? A valid scene can be used to play a scene."""
        return self._is_valid

    def render_updates(self):
        """Render all sprite updates."""

    def update_scene(self):
        """Update the scene state."""

    def start_scene(self):
        """Start the scene."""
        if self._soundtrack:
            try:
                pygame.mixer.music.load(self._soundtrack)
                pygame.mixer.music.set_volume(0.2)
            except pygame.error as pygame_error:
                print("Cannot open the mixer?")
                raise SystemExit("broken!!") from pygame_error
            pygame.mixer.music.play(-1)

    def end_scene(self):
        """End the scene."""
        if self._soundtrack and pygame.mixer.music.get_busy():
            # Fade music out so there isn't an audible pop
            pygame.mixer.music.fadeout(500)
            pygame.mixer.music.stop()

    def frame_rate(self):
        """Return the frame rate the scene desires."""
        return self._frame_rate


class PressAnyKeyToExitScene(Scene):
    """Empty scene where it will invalidate when a key is pressed."""

    def process_event(self, event):
        """Process game events."""
        super().process_event(event)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._is_valid = False


class PolygonTitleScene(PressAnyKeyToExitScene):
    """Scene with a title string and a polygon."""

    def __init__(
        self,
        screen,
        scene_manager,
        title,
        title_color=rgbcolors.magenta,
        title_size=72,
        background_color=rgbcolors.sky_blue,
        soundtrack=None,
    ):
        """Initialize the scene."""
        my_abs_path = os.path.abspath(__file__)
        self._main_dir = os.path.split(my_abs_path)[0]

        self._data_dir = os.path.join(self._main_dir, 'data')
        soundtrack = os.path.join(self._data_dir,
                                  'music-grid.wav')
        super().__init__(screen, background_color, soundtrack)

        title_font = pygame.font.SysFont(title, title_size)
        self._title = pygame.font.Font.render(title_font, title, True,
                                              title_color, background_color)
        eighteen = pygame.font.SysFont(title, 18)
        self._press_any_key = pygame.font.Font.render(eighteen, 'Press SPACE to continue.',
                                                      True, 'Black', background_color)
        self._press_esc_key = pygame.font.Font.render(eighteen, 'Press esc to exit.',
                                                      True, 'Black', background_color)
        self._scene_manager = scene_manager


    def draw(self):
        """Draw the scene."""
        super().draw()
        scene2 = self._screen
        pygame.Surface.blit(scene2, self._title, ((800/2)-160, (800/2)-50))
        pygame.Surface.blit(scene2, self._press_any_key, ((800/2)-90, 800-100))
        pygame.Surface.blit(scene2, self._press_esc_key, ((800/2)-60, 800-50))

    def process_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self._scene_manager.set_next_scene('1')
            self._is_valid = False
        else:
            super().process_event(event)

    def end_scene(self):
        super().end_scene()
        self._is_valid = True


class Snake:
    speed = 0.5
    def __init__(self, position, speed, radius, color, name="None"):
        self._position = position
        self._original_position = pygame.math.Vector2(position)
        self._speed = speed
        self._radius = radius
        self._color = color
        self._name = name

    @property
    def radius(self):
        """Return the circle's radius"""
        return self._radius

    @property
    def position(self):
        """Return the circle's position."""
        return self._position

    @property
    def original_position(self):
        return self._original_position
    
    @property
    def speed(self):
        """Return the circle's speed."""
        return self._speed
    
    def move_ip(self, x, y):
        self._position = self._position + pygame.math.Vector2(x, y)

    @property
    def rect(self):
        """Return bounding rect."""
        left = self._position.x - self._radius
        top = self._position.y - self._radius
        width = 2 * self._radius
        return pygame.Rect(left, top, width, width)
    
    @property
    def height(self):
        """Return the height of the bounding box the circle is in."""
        return 2 * self._radius

    @property
    def width(self):
        """Return the width of the bounding box the circle is in."""
        return 2 * self._radius
    
    def draw(self, screen):
        """Draw the Snake to screen."""
        pygame.draw.circle(screen, self._color, self.position, self.radius)

    
class SnakeScene(PressAnyKeyToExitScene):
    """Scene for Snake Game"""

    def __init__(
            self,
            screen,
            scene_manager,
            background_color=rgbcolors.snow3,
            soundtrack=None,
        ):

        """Initialize the scene."""
        my_abs_path = os.path.abspath(__file__)
        self._main_dir = os.path.split(my_abs_path)[0]

        self._data_dir = os.path.join(self._main_dir, 'data')
        soundtrack = os.path.join(self._data_dir,
                                  '8bp051-06-random-happy_ending_after_all.mp3')

        super().__init__(screen, background_color, soundtrack)
        self._scene_manager = scene_manager
        self._snake = []
        self.drawSnake()
        self._next_key = '1'
    
    def drawSnake(self):
        (width, height) = self._screen.get_size()
        position = random_position(width-100, height-100)
        # c = Snake(position, 0.5, 5, rgbcolors.salmon1, 1)
        # self._snake.append(c)
        # startx = random.randint(5, 800-6)
        # starty = random.randint(5, 800-6)
        # snakeCoords = [{'x': startx, 'y': starty},
        #             {'x': startx - 1, 'y': starty},
        #             {'x': startx - 2, 'y': starty}]
        # for coord in snakeCoords:
        #     x = coord['x'] * 800
        #     y = coord['y'] * 800
        c = Snake(position, 0.5, 25, rgbcolors.salmon1, 1)
        self._snake.append(c)

    def process_event(self, event):
        direction = 'right'
        if event.type == pygame.QUIT:
            print("Good Bye!")
            self._is_valid = False
        elif event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_LEFT or event.key == pygame.K_a) \
                and direction != 'right':
                    direction = 'left'
            elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) \
                and direction != 'left':
                    direction = 'right'
            elif (event.key == pygame.K_UP or event.key == pygame.K_w) \
                and direction != 'down':
                    direction = 'up'
            elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) \
                and direction != 'up':
                    direction = 'down'
            # elif (event.key == pygame.K_DOWN or event.key == pygame.K_SPACE):
            #     self._snake = []
            #     self.drawSnake()
            elif event.key == pygame.K_ESCAPE:
                self._is_valid = False
        else:
            super().process_event(event)

        # move the snake by adding a segment in the direction it is moving
        # if direction == 'up':
        #     newHead = {'x': snakeCoords[0]['x'], 'y': snakeCoords[0]['y'] - 1}
        # elif direction == 'down':
        #     newHead = {'x': snakeCoords[0]['x'], 'y': snakeCoords[0]['y'] + 1}
        # elif direction == 'left':
        #     newHead = {'x': snakeCoords[0]['x'] - 1, 'y': snakeCoords[0]['y']}
        # elif direction == 'right':
        #     newHead = {'x': snakeCoords[0]['x'] + 1, 'y': snakeCoords[0]['y']}
        # snakeCoords.insert(0, newHead)
            

    def update_scene(self):
        super().update_scene()
        

    def render_updates(self):
        if self._render_updates:
            super().render_updates()
            # if self._render_updates:
            self._render_updates.clear(self._screen, self._background)
            self._render_updates.update()
            dirty = self._render_updates.draw(self._screen)

    def draw(self):
        """Draw the scene."""
        super().draw()
        for a in self._snake:
            a.draw(self._screen)
    
    def end_scene(self):
        super().end_scene()
        self._is_valid = True