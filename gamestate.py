#upgrades and events
class GameState:
    infinite_map_mode = False #False is Asteroids classic, True is infinite world
    upgrades = set()

    @classmethod
    def apply_upgrade(cls, upgrade_name):
        if upgrade_name in cls.upgrades:
            return
        
        cls.upgrades.add(upgrade_name)

        if upgrade_name == "infinite_map":
            cls.infinite_map_mode = True