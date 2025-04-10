# game.py

class Game:
    def __init__(self):
        self.red = {'x': 700, 'y': 300, 'health': 10}
        self.yellow = {'x': 100, 'y': 300, 'health': 10}
        self.red_bullets = []
        self.yellow_bullets = []

    def move_player(self, player, direction):
        """Updates player position based on input direction"""
        VEL = 5
        if player == "red":
            if direction == "left":
                self.red['x'] -= VEL
            elif direction == "right":
                self.red['x'] += VEL
            elif direction == "up":
                self.red['y'] -= VEL
            elif direction == "down":
                self.red['y'] += VEL
        elif player == "yellow":
            if direction == "left":
                self.yellow['x'] -= VEL
            elif direction == "right":
                self.yellow['x'] += VEL
            elif direction == "up":
                self.yellow['y'] -= VEL
            elif direction == "down":
                self.yellow['y'] += VEL

    def shoot(self, player):
        """Adds a new bullet from the player's spaceship"""
        if player == "red" and len(self.red_bullets) < 3:
            bullet = [self.red['x'], self.red['y'] + 20]
            self.red_bullets.append(bullet)
        elif player == "yellow" and len(self.yellow_bullets) < 3:
            bullet = [self.yellow['x'] + 55, self.yellow['y'] + 20]
            self.yellow_bullets.append(bullet)

    def update_bullets(self):
        """Move bullets and check for out-of-bounds"""
        for bullet in self.red_bullets[:]:
            bullet[0] -= 7
            if bullet[0] < 0:
                self.red_bullets.remove(bullet)

        for bullet in self.yellow_bullets[:]:
            bullet[0] += 7
            if bullet[0] > 900:
                self.yellow_bullets.remove(bullet)
