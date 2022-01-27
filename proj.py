### IMPORT STATEMENTS
import pygame, pygame.math as pymaths, random, math as maths
from time import time as current_time


### GLOABL VARIABLES
player = None
screen_size = (0, 0)
target_group = None
bullet_image = None
laser_image = None
missile_image = None
play_shoot_noise = False


### SET UP
# the init function to get all the information I need from the other file
def init(_player, _screen_size, _missile_target_group, _bullet_image, _laser_image, _missile_image, _play_shoot_noise):
    global player, screen_size, target_group, bullet_image, laser_image, missile_image, play_shoot_noise
    player = _player
    screen_size = _screen_size
    target_group = _missile_target_group
    bullet_image = _bullet_image
    laser_image = _laser_image
    missile_image = _missile_image
    play_shoot_noise = _play_shoot_noise


### UTILITY FUNCTIONS
# round each element of a vector up
def round_vector(vector):
    # actually round the elements
    x = maths.ceil(vector.x)
    y = maths.ceil(vector.y)
    # make the new vector
    rounded_vector = pymaths.Vector2(x, y)
    # return it
    return rounded_vector


# function to find the rotation of a vector
def find_vector_angle(vector):
    # create a vector that is north facing
    north = pymaths.Vector2(0, 1)
    # find the difference between north and the given vector
    angle = north.angle_to(vector)
    # return the angle
    return angle


### OTHER FUNCTIONS
# function to create a projectile
def create_bullet(proj_type, gun):
    wait_time = 0.5
    if gun.last_fire >= wait_time:
        if proj_type == "bullet":
            projectile = Bullet()
            wait_time = 0.5
        elif proj_type == "laser":
            projectile = Laser()
            wait_time = 0.5
        else:
            projectile = HomingMissile()
            wait_time = 4


# play the noise when you fire
def shoot():
    sound_obj = pygame.mixer.Sound('shoot_noise.wav')
    sound_obj.play()


### CLASSES
# gun class
class Gun(pygame.sprite.Sprite):
    def __init__(self, _image, _player):
        pygame.sprite.Sprite.__init__(self)

        # get the image and the player as parameters
        self.image = _image
        self.parent = _player
        # set the rect and the center postition
        self.rect = self.image.get_rect(center=self.parent.rect.center)

        # 0 is not firing, 1 is firing bullets, 2 lasers and 3 missiles
        self.fire = 0

        # holds time when last projectile was fired so that there will be gaps in between shots
        self.last_fire = 0

    def update(self, _keys):
        global play_shoot_noise
        # update the position of the gun
        self.rect.center = self.parent.rect.center

        # if we need to fire
        if self.fire > 0:
            # sets the time a projectile was last fired to now
            self.last_fire = current_time()

            # depending on what we're firing, create projtype and give it a word that can be passed to where the proj
            # is created, so we know which type to create
            if self.fire == 2:
                projtype = "laser"
            elif self.fire == 3:
                projtype = "missile"
            else:
                projtype = "bullet"
            # actually create it
            createbullet(projtype, self)
            # play a sound if we really need to
            if play_shoot_noise:
                shoot_noise()

        # tkae keyboard input
        if keys[pygame.K_RETURN]:
            if self.parent.lasers:
                self.fire = 2
            else:
                self.fire = 1
        elif keys[pygame.K_RSHIFT]:
            self.fire = 3
        else:
            self.fire = 0

        # I removed joystick support to keep it simple for now, but I can re add it


# bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        global bullet_image, player, screen_size
        pygame.sprite.Sprite.__init__(self)

        # set the player, so we can have a look at its attributes
        self.player = player

        # set up the image and the rect
        self.image = bullet_image
        self.image = pygame.transform.rotate(self.image, self.player.angle)
        self.rect = self.image.get_rect(center=self.player.rect.center)

        # give it a vector
        self.unit = -player.velocity.normalize() * 32

        # get a tuple with the dimensions of the screen
        self.screen_size = screen_size

    def update(self):
        # slow it down gradually
        self.unit -= self.unit / 20

        # if off-screen or not moving
        if not self.rect.centerx in range(-100, self.screen_size[0] + 100) or \
            not self.rect.centery in range(-100, self.screen_size[1] + 100) or self.unit.magnitude < 1:
            # prevent itself from being updated or drawn
            self.kill()

        # move it by a whole number of pixels
        self.rect.move_ip(round(self.unit.x), round(self.unit.y))


# laser subclass of bullet
class Laser(Bullet):
    def __init__(self):
        global laser_image
        # actually initialise it
        super().__init__()

        # re-setting up the image for the laser so that not everything looks like a bullet
        self.image = laser_image
        self.image = pygame.transform.rotate(self.image, self.player.angle)
        self.rect = self.image.get_rect(center=self.player.rect.center)

        # make it a little faster
        # unnecessary note: I wanted to add "bit" after "little" but apparently it's better to "remove redundancy"
        # this also makes it go further because it takes longer to slow down
        self.unit *= 1.5


# homing missile class
class HomingMissile(pygame.sprite.Sprite):
    def __init__(self):
        global missile_image, player, target_group, screen_size
        pygame.sprite.Sprite.__init__(self)

        # get the player so we can use its attributes
        self.player = player

        # set the screen size so we can use it later
        self.screen_size = screen_size

        # set the og image (required to rotate it without crashing)
        self.og_image = image
        # flip the original image because otherwise it's the wrong way around
        self.og_image = pygame.transform.flip(self.og_image, False, True)
        # set the image we will actually blit and the rect
        self.image = self.og_image
        self.rect = self.image.get_rect(center=self.player.rect.center)

        # setting some more variables which will be used for rotating the image
        self.angle = self.player.angle
        self.change_angle = 0

        # get time of creation
        self.birthday = current_time()

        # get an array of all the targets it could follow
        self.viable_targets = [t for t in target_group if t.inRange]
        # choose one of the targets if there is some targets to choose from
        if self.viable_targets:
            # then select a target from the array
            self.target = self.viable_targets[random.randint(0, len(_target_group) - 1)]
            # and then find the relative vector between the missile and its target
            self.unit = round_vector((pymaths.Vector2(self.target.rect.center) - pymaths.Vector2(self.rect.center)).normalize() * 5)
        # otherwise
        else:
            # set the target to none so that we can delete it later, it can't be deleted in the init as it hasn't been added to group's yet
            self.target = None
            # set the vector to any old numbers, it doesn't matter as it will be deleted instantly, but it has to be set as it will get looked at once
            self.unit = pymath.Vector2(1, 1)

    def update(self):
        # find out how long it has been active
        lifetime = current_time() - self.birthday
        # if it has no target or has been around too long, remove it from all groups so that it can't be updated or drawn
        if not self.target or lifetime > 5:
            self.kill()
        # if it is on screen and doesn't meet above criteria
        elif self.target.rect.centerx in range(-100, self.screen_size[0] + 100) and self.target.rect.centery in range(-100, self.screen_size[1] + 100):
            # update its vector using the fancy function
            self.update_vector()

        # call the rotate function to get it nicely rotated
        self.rotate()

        # if it is off-screen then remove it from all gorups so that it can't be updated or drawn
        if not (self.rect.centerx in range(-100, self.screen_size[0] + 100) and self.rect.centery in range(-100, self.screen_size[1] + 100)):
            self.kill()

        # move it
        self.rect.center += self.unit

    def rotate(self):
        self.angle = -find_vector_angle(self.unit)
        self.image = pygame.transform.rotate(self.og_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update_vector(self):
        # an alternate pathfinding method which just gets the relative vector and then makes it smaller and then gets cracking
        # self.unit = (pygame.math.Vector2(self.target.rect.center) - pygame.math.Vector2(self.rect.center)) // 20

        # find the relative vector between the target the missile, this is where we want the missile to go
        rel_vec = pymaths.Vector2(self.target.rect.center) - pymaths.Vector2(self.rect.center)
        # find the difference in angle between the relative vector, the ideal path, and the cyrrent vector
        rel_ang = round(rel_vec.angle_to(self.unit))

        # if we need to turn clockwise
        if rel_ang > 4:
            # then turn clockwise, the negative does make it seem like it would be turning anit-clockwise but this is correct
            # the "ip" means in place, I don't really know what that means, but it is the only thing that works
            self.unit.rotate_ip(-5)
        # if we need to turn anti-clockwise
        elif rel_ang < -4:
            # then turn anti-clockwise
            self.unit.rotate_ip(5)
