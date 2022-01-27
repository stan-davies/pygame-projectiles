# pygame-projectiles
some classes and utility functions to create projectiles in pygame

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
