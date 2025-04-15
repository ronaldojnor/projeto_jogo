class Shop:
    def __init__(self):
        self.upgrades = {
            "double_shot": {"active": False, "cost": 10},
            "fast_shot": {"active": False, "cost": 10},
            "extra_health": {"active": False, "cost": 10},
            "damage_up": {"active": True, "cost": 10}  # sempre disponível
        }

    def apply_upgrade(self, player, choice, xp_system):
        upgrade = self.upgrades[choice]
        if xp_system.coins >= upgrade["cost"]:
            xp_system.coins -= upgrade["cost"]
            upgrade["cost"] = int(upgrade["cost"] * 1.5)

            # upgrades únicos
            if choice == "double_shot":
                upgrade["active"] = True
                player.double_shot = True
            elif choice == "fast_shot":
                upgrade["active"] = True
                player.shot_interval = max(100, player.shot_interval - 150)
            elif choice == "extra_health":
                upgrade["active"] = True
                player.health += 50
            elif choice == "damage_up":
                player.damage += 5  # novo upgrade de dano!

            return True
        return False

    def get_options(self):
        return [
            k for k, v in self.upgrades.items()
            if k != "double_shot" or not v["active"]
        ]

    def get_cost(self, upgrade_name):
        return self.upgrades[upgrade_name]["cost"]
