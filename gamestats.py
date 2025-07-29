class GameStats:
    def __init__(self):
        self.asteroids_destroyed = 0
        self.upgrades_acquired = 0
        self.powerup_usage = {
            "invulnerability": 0,
            "acceleration": 0,
            "multishot": 0,
        }

    def increment_asteroid_destroyed(self):
        self.asteroids_destroyed += 1

    def increment_upgrades_acquired(self):
        self.upgrades_acquired += 1

    def increment_powerup_use(self, powerup_name):
        if powerup_name in self.powerup_usage:
            self.powerup_usage[powerup_name] += 1