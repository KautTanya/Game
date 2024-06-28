"""Game"""
import random
import pickle


class Person:
    """Main class"""
    def __init__(self, name, attack, defense, health, crit_chance, damage_percentage):
        self.name = name    # імʼя
        self._attack = attack   # атака
        self._defense = defense   # захист
        self._health = health  # здоровʼя
        self.base_attack = attack
        self.base_defense = defense
        self.base_health = health
        self.crit_chance = crit_chance  # вірогідність критичного удару
        self.damage_percentage = damage_percentage   # відсоток критичного урону,
        self.inventory = []  # інвентарь
        self.equipped = {}   # вдягнуті речі
        self.experience = 0  # досвід
        self.level = 1    # рівень

    @property
    def attack(self):
        """attack"""
        return self._attack

    @attack.setter
    def attack(self, value):
        if value < 0:
            raise ValueError("Attack cannot be negative")
        self._attack = value

    @property
    def defense(self):
        """defense"""
        return self._defense

    @defense.setter
    def defense(self, value):
        if value < 0:
            raise ValueError("Defense cannot be negative")
        self._defense = value

    @property
    def health(self):
        """health"""
        return self._health

    @health.setter
    def health(self, value):
        if value < 0:
            self._health = 0
        else:
            self._health = value

    def __str__(self):
        return (f"{self.name} (Level: {self.level}) - Health: {self._health}, "
                f"Attack: {self._attack}, Defense: {self._defense}, "
                f"XP: {self.experience}")

    def add_item_to_inventory(self, item):
        """add item to inventory"""
        self.inventory.append(item)
        print(f"{item.name} added to inventory.")

    def equip_item(self, item):
        """equip item"""
        if item.item_type in self.equipped:
            self.unequip_item(item.item_type)
        self.equipped[item.item_type] = item
        self._recalculate_stats()
        print(f"Equipped {item.name}.")

    def unequip_item(self, item_type):
        """nequip item"""
        if item_type in self.equipped:
            print(f"Unequipped {self.equipped[item_type].name}.")
            del self.equipped[item_type]
            self._recalculate_stats()

    def _recalculate_stats(self):
        self._attack = self.base_attack + sum(item.attack_boost for item in self.equipped.values())
        self._defense = self.base_defense + sum(item.defense_boost for item in self.equipped.values())
        self._health = self.base_health + sum(item.health_boost for item in self.equipped.values())
        print("Stats recalculated.")


class Warrior(Person):
    base_attack = 120
    base_defense = 100
    base_health = 150

    def __init__(self, name):
        super().__init__(name, self.base_attack, self.base_defense, self.base_health, crit_chance=0.15,
                         damage_percentage=1.8)


class Mage(Person):
    base_attack = 150
    base_defense = 80
    base_health = 100

    def __init__(self, name):
        super().__init__(name, self.base_attack, self.base_defense, self.base_health, crit_chance=0.25,
                         damage_percentage=2.5)


class Rogue(Person):
    base_attack = 130
    base_defense = 90
    base_health = 110

    def __init__(self, name):
        super().__init__(name, self.base_attack, self.base_defense, self.base_health, crit_chance=0.30,
                         damage_percentage=2.0)


class Paladin(Person):
    base_attack = 110
    base_defense = 120
    base_health = 140

    def __init__(self, name):
        super().__init__(name, self.base_attack, self.base_defense, self.base_health, crit_chance=0.10,
                         damage_percentage=1.5)


class Bot(Person):
    def __init__(self, level):
        name = f"Bot_{random.randint(1000, 9999)}"
        attack = random.randint(5, 10) + level * 3
        defense = random.randint(3, 8) + level * 2
        health = random.randint(20, 40) + level * 10
        super().__init__(name, attack, defense, health, crit_chance=0.1, damage_percentage=1.5)


class Item:
    """Item"""
    def __init__(self, name, item_type, attack_boost=0, defense_boost=0, health_boost=0):
        self.name = name
        self.item_type = item_type
        self.attack_boost = attack_boost
        self.defense_boost = defense_boost
        self.health_boost = health_boost

    def __str__(self):
        return f"{self.name} (+{self.attack_boost} Attack, +{self.defense_boost} Defense, +{self.health_boost} Health)"


class Game:
    """All game"""
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    @staticmethod
    def generate_bot(player_level):
        """generate bot"""
        return Bot(player_level)

    @staticmethod
    def fight(player1, player2):
        """fight"""
        # Визначення класу переваги
        class_advantage = {
            'Warrior': {'Mage': 1.15, 'Rogue': 1.0, 'Paladin': 1.0, 'Bot': 1.0},
            'Mage': {'Rogue': 1.15, 'Paladin': 1.0, 'Warrior': 1.0, 'Bot': 1.0},
            'Rogue': {'Paladin': 1.15, 'Warrior': 1.0, 'Mage': 1.0, 'Bot': 1.0},
            'Paladin': {'Warrior': 1.15, 'Mage': 1.0, 'Rogue': 1.0, 'Bot': 1.0},
            'Bot': {'Warrior': 1.0, 'Mage': 1.0, 'Rogue': 1.0, 'Paladin': 1.0}
        }

        turn = 0
        while player1.health > 0 and player2.health > 0:
            attacker = player1 if turn % 2 == 0 else player2
            defender = player2 if turn % 2 == 0 else player1

            damage = attacker.attack * class_advantage[type(attacker).__name__][type(defender).__name__]
            defender.health -= damage
            print(f"{attacker.name} attacks {defender.name} for {damage:.2f} damage.")

            if defender.health <= 0:
                print(f"{attacker.name} wins!")
                attacker.experience += 50
                break

            turn += 1

    def go_to_forest(self, player):
        """go to forest"""
        print("You have entered the forest. Type 'stop' to return.")
        while True:
            bot = self.generate_bot(player.level)
            print(f"A wild {bot.name} appears!")
            self.fight(player, bot)
            if player.health <= 0:
                print("You have been defeated! Returning to safety...")
                break
            command = input("Continue fighting? (yes/stop): ")
            if command == "stop":
                print("Returning from the forest...")
                break


def save_game(filename, game_state):
    """save game"""
    with open(filename, 'wb') as file:
        pickle.dump(game_state, file)
        print("Game saved successfully!")


def load_game(filename):
    """load game"""
    with open(filename, 'rb') as file:
        game_state = pickle.load(file)
        print("Game loaded successfully!")
        return game_state


player1 = Warrior("Arthur")
player2 = Mage("Merlin")
player3 = Rogue("Robin")
player4 = Paladin("Lancelot")

# Створення бота
bot = Game.generate_bot(5)  # для рівня гравця – 5

sword = Item("Excalibur", "weapon", attack_boost=15)
shield = Item("Dragon Shield", "armor", defense_boost=10)
potion = Item("Healing Potion", "potion", health_boost=50)

player1.add_item_to_inventory(sword)
player1.add_item_to_inventory(shield)
player1.equip_item(sword)
player1.equip_item(shield)

player2.add_item_to_inventory(potion)
player2.equip_item(potion)

game = Game(player1, player2)
game.fight(player1, player2)

save_game("game_state.pkl", game)
loaded_game = load_game("game_state.pkl")

game.go_to_forest(player1)
