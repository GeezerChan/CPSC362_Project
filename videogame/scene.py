# Andy Huynh
# CPSC 386-02
# 2023-04-20
# ahuynh86@csu.fullerton.edu
# @GeezerChan
#
# Lab 00-04
#
# M4: Invader
#

"""Scene objects for making games with PyGame."""

import random
import pygame
import assets
import player
import rgbcolors
import animation

# If you're interested in using abstract base classes, feel free to rewrite
# these classes.
# For more information about Python Abstract Base classes, see
# https://docs.python.org/3.8/library/abc.html

class SceneManager:
    """Class to manage multiple scenes"""

    def __init__(self):
        self._scene_dict = {}
        self._current_scene = None
        self._next_scene = None
        # This is a safety to ensure that calling
        # next() twice in a row without calling set_next_scene()
        # will raise StopIteration.
        self._reloaded = True

    def set_next_scene(self, key):
        """Sets next scene"""
        self._next_scene = self._scene_dict[key]
        self._reloaded = True

    def add(self, scene_list):
        """Adds new scene to list"""
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
                print('\n'.join(pygame_error.args))
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
        elif event.type == pygame.KEYDOWN:
            self._is_valid = True


class PolygonTitleScene(PressAnyKeyToExitScene):
    """Main Menu Scene"""

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
        super().__init__(screen, background_color, assets.get('music-grid'))
        self._scene_manager = scene_manager
        title_font = pygame.font.SysFont(title, title_size)
        self._title = pygame.font.Font.render(title_font, title, True,
                                              title_color, background_color)
        eighteen = pygame.font.SysFont(title, 20)
        self._conditions = pygame.font.Font.render(eighteen,
                                        'Win by: Shooting and getting rid of all aliens.',
                                                      True, 'Black', background_color)
        self._conditions1 = pygame.font.Font.render(eighteen,
                                        'Lose by: Getting shot 3 times. OR aliens reach you.',
                                                      True, 'Black', background_color)
        self._how_to_play = pygame.font.Font.render(eighteen, 'How to Play:',
                                                      True, 'Black', background_color)
        self._how_to_play1 = pygame.font.Font.render(eighteen,
                                                     'Arrow keys: <-(move left), ->(move right)',
                                                      True, 'Black', background_color)
        self._how_to_play2 = pygame.font.Font.render(eighteen,
                                                     'Spacebar to shoot',
                                                      True, 'Black', background_color)
        self._press_any_key = pygame.font.Font.render(eighteen, 'Press TAB to continue.',
                                                      True, rgbcolors.dark_red, background_color)
        self._press_esc_key = pygame.font.Font.render(eighteen, 'Press ESC any time to exit.',
                                                      True, rgbcolors.dark_red, background_color)

    def draw(self):
        """Draw the scene."""
        super().draw()
        scene2 = self._screen
        pygame.Surface.blit(scene2, self._title, ((800/2)-190, 200))
        pygame.Surface.blit(scene2, self._conditions, (270, 350))
        pygame.Surface.blit(scene2, self._conditions1, (260, 380))
        pygame.Surface.blit(scene2, self._how_to_play, ((800/2)-40, 800-300))
        pygame.Surface.blit(scene2, self._how_to_play1, ((800/2)-115, 800-275))
        pygame.Surface.blit(scene2, self._how_to_play2, ((800/2)-55, 800-250))
        pygame.Surface.blit(scene2, self._press_any_key, ((800/2)-62, 800-100))
        pygame.Surface.blit(scene2, self._press_esc_key, ((800/2)-70, 800-50))

    def process_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
            self._scene_manager.set_next_scene('1')
            self._is_valid = False
        else:
            super().process_event(event)

    def end_scene(self):
        super().end_scene()
        self._is_valid = True


class GameOverScene(PressAnyKeyToExitScene):
    """Game Over Scene"""

    def __init__(
        self,
        screen,
        scene_manager,
        title,
        title_color=rgbcolors.dark_red,
        title_size=72,
        background_color=rgbcolors.indian_red,
        soundtrack=None,
    ):
        """Initialize the scene."""
        super().__init__(screen, background_color, assets.get('music-grid.BJ'))
        self._scene_manager = scene_manager
        title_font = pygame.font.SysFont(title, title_size)
        self._title = pygame.font.Font.render(title_font, title, True,
                                              title_color, background_color)
        eighteen = pygame.font.SysFont(title, 20)
        twenty = pygame.font.SysFont(title, 50)
        self._press_any_key = pygame.font.Font.render(eighteen, 'Press TAB to try again.',
                                                      True, rgbcolors.dark_red, background_color)
        self._press_esc_key = pygame.font.Font.render(eighteen, 'Press ESC any time to exit.',
                                                      True, rgbcolors.dark_red, background_color)
        self._you_lose = pygame.font.Font.render(twenty, 'You lose.',
                                                      True, rgbcolors.dark_red, background_color)

    def draw(self):
        """Draw the scene."""
        super().draw()
        scene2 = self._screen
        pygame.Surface.blit(scene2, self._title, ((800/2)-190, 200))
        pygame.Surface.blit(scene2, self._you_lose, ((800/2)-70, 400))
        pygame.Surface.blit(scene2, self._press_any_key, ((800/2)-62, 800-100))
        pygame.Surface.blit(scene2, self._press_esc_key, ((800/2)-70, 800-50))

    def process_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
            self._scene_manager.set_next_scene('3')
            self._is_valid = False
        else:
            super().process_event(event)

    def end_scene(self):
        super().end_scene()
        self._is_valid = True


class GameOver2Scene(PressAnyKeyToExitScene):
    """Game Over2 Scene"""

    def __init__(
        self,
        screen,
        scene_manager,
        title,
        title_color=rgbcolors.white,
        title_size=72,
        background_color=rgbcolors.black,
        soundtrack=None,
    ):
        """Initialize the scene."""
        super().__init__(screen, background_color, assets.get('goofy_ahh'))
        self._scene_manager = scene_manager
        title_font = pygame.font.SysFont(title, title_size)
        self._title = pygame.font.Font.render(title_font, title, True,
                                              title_color, background_color)
        eighteen = pygame.font.SysFont(title, 20)
        twenty = pygame.font.SysFont(title, 50)
        self._press_esc_key = pygame.font.Font.render(eighteen, 'Press ESC any time to exit.',
                                                      True, rgbcolors.dark_red, background_color)
        self._you_lost = pygame.font.Font.render(twenty,
                                                'This world is taken over by aliens.',
                                                True, rgbcolors.dark_red, background_color)
        self._you_lost2 = pygame.font.Font.render(twenty,
                                                'No more coming back.',
                                                True, rgbcolors.dark_red, background_color)

    def draw(self):
        """Draw the scene."""
        super().draw()
        scene2 = self._screen
        pygame.Surface.blit(scene2, self._title, ((800/2)-190, 200))
        pygame.Surface.blit(scene2, self._you_lost, ((800/2)-280, 400))
        pygame.Surface.blit(scene2, self._you_lost2, ((800/2)-190, 450))
        pygame.Surface.blit(scene2, self._press_esc_key, ((800/2)-70, 800-50))

    def process_event(self, event):
        super().process_event(event)

    def end_scene(self):
        super().end_scene()
        self._is_valid = True


class GameWinScene(PressAnyKeyToExitScene):
    """Game Win Scene"""

    def __init__(
        self,
        screen,
        scene_manager,
        title,
        title_color=rgbcolors.blue3,
        title_size=72,
        background_color=rgbcolors.snow3,
        soundtrack=None,
    ):
        """Initialize the scene."""
        super().__init__(screen, background_color, assets.get('music-grid'))
        self._scene_manager = scene_manager
        title_font = pygame.font.SysFont(title, title_size)
        self._title = pygame.font.Font.render(title_font, title, True,
                                              title_color, background_color)
        eighteen = pygame.font.SysFont(title, 20)
        twenty = pygame.font.SysFont(title, 50)
        self._press_esc_key = pygame.font.Font.render(eighteen, 'Press ESC any time to exit.',
                                                      True, rgbcolors.dark_red, background_color)
        self._you_won = pygame.font.Font.render(twenty,
                                                'This world is protected from the aliens.',
                                                True, rgbcolors.dark_red, background_color)
        self._you_won2 = pygame.font.Font.render(twenty,
                                                'You did it!',
                                                True, rgbcolors.dark_red, background_color)

    def draw(self):
        """Draw the scene."""
        super().draw()
        scene2 = self._screen
        pygame.Surface.blit(scene2, self._title, ((800/2)-190, 200))
        pygame.Surface.blit(scene2, self._you_won, ((800/2)-280, 400))
        pygame.Surface.blit(scene2, self._you_won2, ((800/2)-80, 450))
        pygame.Surface.blit(scene2, self._press_esc_key, ((800/2)-70, 800-50))

    def process_event(self, event):
        super().process_event(event)

    def end_scene(self):
        super().end_scene()
        self._is_valid = True


class AlienScene(PressAnyKeyToExitScene):
    """Scene for Alien Invasion"""

    def __init__(self, screen, scene_manager):
        super().__init__(screen, rgbcolors.black, assets.get('soundtrack'))
        self._explosion_sound = pygame.mixer.Sound(assets.get('soundfx'))
        self._scene_manager = scene_manager
        self.delta_time = 0
        self._aliens = []
        self.make_aliens()
        (width, height) = self._screen.get_size()
        self._player = player.Player(pygame.math.Vector2(width//2, height - 100))
        self._bullets = []
        self._alien_bullets = []
        self._render_updates = pygame.sprite.RenderUpdates()
        animation.Explosion.containers = self._render_updates
        eighteen = pygame.font.SysFont('title', 20)
        self._press_esc_key = pygame.font.Font.render(eighteen, 'Press ESC any time to exit.',
                                                      True, rgbcolors.dark_red, rgbcolors.black)

    def make_aliens(self):
        """Makes the alien models."""
        alien_width = 40
        alien_radius = alien_width // 2
        buffer_between = alien_width // 4
        (width, height) = (600, 250)
        x_step = buffer_between + alien_width
        y_step = buffer_between + alien_width
        aliens_per_row = (width // x_step) - 1
        num_rows = (height // y_step) - 1
        self._aliens = [
            player.Alien(
                x_step + (j * x_step),
                y_step + (i * y_step),
                alien_radius,
                rgbcolors.red,
                f"{i+1}, {j+1}",
            )
            for i in range(num_rows)
            for j in range(aliens_per_row)
        ]

    def update_scene(self):
        super().update_scene()
        self._player.update()
        (width, height) = self._screen.get_size()
        for move in self._aliens:
            if move._center_x != width - 30:
                move._center_y += .5
            #elif move._center_x == width - 25:
            #    move._center_x -= 1
            #else:
            #    move._center_y += 1
            if move._center_y == 650:
                self._scene_manager.set_next_scene('2')
                self._is_valid = False

        for bullet in self._bullets:
            bullet.update(self.delta_time)
            if bullet.should_die():
                self._bullets.remove(bullet)
            else:
                index = bullet.rect.collidelist([c.rect for c in self._aliens])
                if index > -1:
                    animation.Explosion(self._aliens[index])
                    self._aliens[index].is_exploding = True
                    self._aliens.remove(self._aliens[index])
                    self._explosion_sound.play()
                    self._bullets.remove(bullet)
                if not self._aliens:
                    self._scene_manager.set_next_scene('4')
                    self._is_valid = False

        for alienbullet in self._alien_bullets:
            alienbullet.update(self.delta_time)
            if alienbullet.should_die():
                self._alien_bullets.remove(alienbullet)
                #if alienbullet.rect.collideobjects(): # If collides with player
                #self._scene_manager.set_next_scene('2')
                #self._is_valid = False

        if random.randint(0,100) == random.randint(0,100):
            (width, height) = self._screen.get_size()
            rand_posi = random.randint(100, 700)
            bullet_target = pygame.math.Vector2(rand_posi, height)
            velocity = .2
            self._alien_bullets.append(
                player.AlienBullet(pygame.math.Vector2(rand_posi, 250),
                                    bullet_target, velocity))

    def process_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            (width, height) = self._screen.get_size()
            bullet_target = self._player.position - pygame.math.Vector2(0, height)
            velocity = 1
            self._bullets.append(player.Bullet(self._player.position, bullet_target, velocity))
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            self._player.move_left()
        elif event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
            self._player.stop()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            self._player.move_right()
        elif event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
            self._player.stop()
        else:
            super().process_event(event)

    def render_updates(self):
        super().render_updates()
        self._render_updates.clear(self._screen, self._background)
        self._render_updates.update()
        dirty = self._render_updates.draw(self._screen)

    def draw(self):
        super().draw()
        for aliens in self._aliens:
            aliens.draw(self._screen)
        for bullet in self._bullets:
            bullet.draw(self._screen)
        for alienbullets in self._alien_bullets:
            alienbullets.draw(self._screen)
        self._player.draw(self._screen)
        scene2 = self._screen
        pygame.Surface.blit(scene2, self._press_esc_key, ((800/2)-70, 800-50))