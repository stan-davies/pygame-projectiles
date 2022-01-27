# pygame-projectiles
some classes and utility functions to create projectiles in pygame

## init
use `proj.init()` to init projectiles. you need to give these arguments in this order:
 1. player, this is used quite a lot, you need to give a pygame sprite which is the player you want to shoot projectiles
 2. screen size, give a tuple of ints that contains the width and height of your window
 3. missile target group, a pygame spritegroup which contains the objects you want the tracking missiles to follow
 4. bullet image, the image you want a standard bullet to have, scaled to whatever size you want it
 5. laser image, same as above but for the laser subclass
 6. missile image, the same again but this time for the missile class
 7. play shoot noise, True if you want a sound to be played when you fire, False if not

## classes
 - gun, takes inputs and creates necessary projectiles
 - bullet, a standard bullet, shoots in the direction of the player, bullets slow over time
 - laser a subclass of bullet, faster and travles further
 - homing missile, takes a pygame spritegroup and then tracks a target from that group that has an attribute called inRange set to True

## utility functions
the main purpose of adding these was so that i could use them in the class but you can use them too if you want
 - round vector, ceil rounds each element of a pygame Vector2
 - find vector angle, returns the rotation of a pygame Vector2 in degrees
there are a few other functions but they have no use outside of this, they wouldn't even work
