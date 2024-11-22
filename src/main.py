import json, pathlib, shlex
from sys import exit # This is needed for PyInstaller
from io import TextIOWrapper
from typing import TypedDict
from datetime import datetime
from inputs import get_valid_input, get_valid_arr_input
from colorama import Fore, Style

RESOURCE_PATH = pathlib.Path(__file__).parent.resolve()
GAME_WORLD = {
    "Cave Entrance": {
        "description": (
            "You stand at the entrance of the Cave of Shadows. The air is thick with the scent of damp earth and decay.\n"
            "Faint whispers seem to call from within. Do you have the courage to step inside?"
        ),
        "options": [
            {"name": "Enter the Cave", "next": "Dark Tunnel"},
            {"name": "Turn Back", "next": "Village"}
        ],
        "items": []
    },

    "Village": {
        "description": (
            "You turn away from the dark cave, choosing to play it safe. The walk back to the village is quiet, and you reflect on your decision.\n"
            "The warmth of the tavern greets you as the night deepens. You've decided to relax and live another day."
        ),
        "options": [],
        "items": []
    },

    "Dark Tunnel": {
        "description": (
            "You step into the darkness. The light from your lantern flickers and dances as you walk deeper into the cave.\n"
            "It's eerily quiet except for the sound of your footsteps echoing against the stone walls. Suddenly, the path ahead splits into two."
        ),
        "options": [
            {"name": "Take the Narrow Path", "next": "Narrow Path"},
            {"name": "Take the Wide Path", "next": "Wide Path"}
        ],
        "items": []
    },

    "Narrow Path": {
        "description": (
            "You crawl through the tight space, your lantern flickering nervously as the walls close in on you.\n"
            "After a while, the ground suddenly gives way beneath you."
        ),
        "options": [
            {"name": "Try to Climb Out", "next": "Bad Ending - Fall to Doom"},
            {"name": "Stay Still", "next": "Pit Ledge Escape"}
        ],
        "items": []
    },

    "Bad Ending - Fall to Doom": {
        "description": (
            "You struggle to climb, but the walls are too slick. The pit seems endless. Darkness closes in as your strength fades.\n"
            "The cave claims another victim."
        ),
        "options": [],
        "items": []
    },

    "Pit Ledge Escape": {
        "description": (
            "You pause, letting your eyes adjust to the darkness. Eventually, you spot a narrow ledge along the edge of the pit.\n"
            "You carefully climb onto it and manage to escape. You find yourself back at the fork in the path, with two choices ahead."
        ),
        "options": [
            {"name": "Take the Wide Path", "next": "Wide Path"},
            {"name": "Leave the Cave", "next": "Leave Cave - Neutral Ending"}
        ],
        "items": []
    },

    "Wide Path": {
        "description": (
            "You follow the wider path toward a faint glow in the distance. Soon, you find yourself in a large cavernous room.\n"
            "A glowing chest sits in the center, with strange symbols carved into the walls."
        ),
        "options": [
            {"name": "Open the Chest", "next": "Treasure Room - Chest Opened"},
            {"name": "Leave the Chest", "next": "Leave Cave - Neutral Ending"}
        ],
        "items": []
    },

    "Treasure Room - Chest Opened": {
        "description": (
            "You open the chest and find a crystal relic pulsing with energy. As you grasp it, a monstrous creature emerges from the shadows.\n"
            "The battle is about to begin."
        ),
        "options": [
            {"name": "Use the Relic's Light to Blind the Creature", "next": "Victory - Success Ending"},
            {"name": "Use the Relic to Charge Your Sword with Power", "next": "Creature Attack - Tragic Ending"},
            {"name": "Throw the Relic as a Distraction and Attack", "next": "Creature Attack - Tragic Ending 2"},
            {"name": "Throw down all items and equipment and flee the caves", "next": "Escaping Treasure Room"}
        ],
        "items": ["Crystal Relic"]
    },

    "Escaping Treasure Room": {
        "description": (
            "You throw everything you have down and quickly remove all your armour, making you lighter and faster.\n"
            "While the Creature gobbles up your belongings, you sprint your way out of the cave and head back to village."
        ),
        "options": [
            {"name": "Inform the village Mayor about the Creature and prepare an army to defeat it", "next": "The Army Attacks"},
            {"name": "Head back to your room in the tavern and rest, hoping the Creature goes away", "next": "The Creature Hungers"}
        ],
        "items": []
    },
    
    "The Army Attacks": {
        "description": (
            "The Mayor orders an army to be built to defeat the Creature, and you are handed the finest sword in the land by the local blacksmith.\n"
            "Together you storm the cave, combining manpower and courage to take down the beast and save the village!"
        ),
        "options": [
            {"name": "Inform the village Mayor about the Creature and prepare an army to defeat it", "next": "The Army Attacks"},
            {"name": "Head back to your room in the tavern and rest, hoping the Creature goes away", "next": "The Creature Hungers"}
        ],
        "items": []
    },
    
    "Creature Attack - Tragic Ending": {
        "description": (
            "You fail to control the relic's power. The creature attacks swiftly, and in a heartbeat, your life is taken.\n"
            "The Cave of Shadows claims another soul."
        ),
        "options": [],
        "items": []
    },

    "Creature Attack - Tragic Ending 2": {
        "description": (
            "You attempt to throw the relic as a distraction, but the creature ignores it. It charges at you, striking swiftly,\n"
            "and your life fades in the darkness."
        ),
        "options": [],
        "items": []
    },

    "Victory - Success Ending": {
        "description": (
            "You raise the relic high, blinding the creature. Seizing the opportunity, you strike with your sword, killing it.\n"
            "The treasure is yours, and you return to the village as a hero."
        ),
        "options": [],
        "items": ["Crystal Relic", "Ancient Treasure"]
    },

    "Leave Cave - Neutral Ending": {
        "description": (
            "You decide that the dangers of the cave are too great. Retracing your steps, you carefully make your way back to the entrance.\n"
            "The cool night air greets you as you step outside. Though you leave the cave empty-handed, you feel relieved to be alive.\n"
            "The treasure, if it truly exists, will remain hidden — for now."
        ),
        "options": [],
        "items": []
    }
}

class PlayerDataType(TypedDict):
    current_location: str
    inventory: list[str]
    game_name: str
    last_updated: int

def get_save_game_contents(file_pointer: TextIOWrapper | None = None) -> list[PlayerDataType]:
    try:
        if file_pointer is None:
            with open(f"{RESOURCE_PATH}/saved_game.json", "r") as file_pointer:
                return json.load(file_pointer)
        
        file_pointer.seek(0)
        return json.load(file_pointer)
    except (FileNotFoundError, json.JSONDecodeError):
        with open(f"{RESOURCE_PATH}/saved_game.json", "w") as file_pointer:
            json.dump([], file_pointer)
        return []

def get_game_name_syntax(
        game_data: list[PlayerDataType],
        exclude_last_update: bool | None = False
    ) -> list[str]:
    arr: list[str] = []
    for i, game in enumerate(game_data):
        name = shlex.quote(game["game_name"])
        last_updated = datetime.fromtimestamp(game["last_updated"]).strftime("%d-%m-%Y %H:%M:%S")
        if exclude_last_update:
            arr.append(name)
            continue
        arr.append(f"{name} - last updated: {last_updated}")
    return arr

class PlayerData():
    current_location: str
    inventory: list[str]
    game_name: str
    last_updated: int

    def __init__(self):
        self.current_location = list(GAME_WORLD.keys())[0]
        self.inventory = []

    def _print_section(self, title: str, content: str, color=Fore.GREEN):
        print(f"{color}{Style.BRIGHT}\n{'-' * 40}\n{title.upper()}\n{'-' * 40}\n{Style.RESET_ALL}{content}\n")
    
    def play_game(self):
        if self.current_location not in GAME_WORLD:
            print(f"{Fore.RED}Game Over: This location does not exist.{Style.RESET_ALL}")
            return False

        location = GAME_WORLD[self.current_location]
        self._print_section(f"Location: {self.current_location}", location["description"], Fore.YELLOW)

        if not location["options"]:
            print(f"{Fore.CYAN}This is the end of the path. Thank you for playing!{Style.RESET_ALL}")
            return False

        choice = get_valid_arr_input(
            f"{Fore.CYAN}What do you want to do next?{Style.RESET_ALL}\n",
            [f"{Fore.MAGENTA}{opt['name']}{Style.RESET_ALL}" for opt in location["options"]]
        )
        self.current_location = location["options"][choice]["next"]
        self._save_game()
        return True

    def delete_game(self):
        all_player_datas = get_save_game_contents()
        if all_player_datas:
            game_names = get_game_name_syntax(all_player_datas)
            game_names.append(f"{Fore.RED}Go back{Style.RESET_ALL}")
            choicen_save_int = get_valid_arr_input(f"{Fore.CYAN}Choose a game to delete: {Style.RESET_ALL}", game_names)
            if choicen_save_int == len(game_names) - 1:
                return
            all_player_datas.pop(choicen_save_int)
            self._save_game(override=all_player_datas)
            print(f"{Fore.GREEN}Game deleted successfully!{Style.RESET_ALL}")
            return
        print(f"{Fore.RED}No saved games found.{Style.RESET_ALL}")

    def new_game(self):
        all_game_names = list(map(lambda x: x.get("game_name"), get_save_game_contents()))
        
        while True:
            input_name = get_valid_input(f"{Fore.CYAN}What will you name this save? {Style.RESET_ALL}")
            if input_name in all_game_names:
                print(f"{Fore.RED}This name is already taken. Please enter another{Style.RESET_ALL}")
                continue
            self.game_name = input_name
            break

        self._save_game()
        print(f"{Fore.GREEN}New game '{self.game_name}' created!{Style.RESET_ALL}")

    def load_game(self):
        all_player_datas = get_save_game_contents()
        if all_player_datas:
            choicen_save_int = get_valid_arr_input(
                f"{Fore.CYAN}Choose a game to load:{Style.RESET_ALL}\n",
                [f"{Fore.YELLOW}{x['game_name']} - last updated: {datetime.fromtimestamp(x['last_updated']).strftime('%d-%m-%Y %H:%M:%S')}{Style.RESET_ALL}" for x in all_player_datas]
            )
            loaded_save = all_player_datas[choicen_save_int]

            print(f"{Fore.GREEN}Loaded game: {loaded_save['game_name']}{Style.RESET_ALL}")
            self.current_location = loaded_save["current_location"]
            self.inventory = loaded_save["inventory"]
            self.game_name = loaded_save["game_name"]
            self.last_updated = loaded_save["last_updated"]
            return True

        print(f"{Fore.RED}No saved games found.{Style.RESET_ALL}")
        return False

    def _save_game(self, override: list[PlayerDataType] | None = None):
        all_player_datas = get_save_game_contents() if override is None else override

        if override is None:
            self.last_updated = datetime.now().timestamp()
            game_found = False

            for i, player_data in enumerate(all_player_datas):
                if player_data["game_name"] == self.game_name:
                    all_player_datas[i] = self.__dict__
                    game_found = True
                    break

            if not game_found:
                all_player_datas.append(self.__dict__)

        with open(f"{RESOURCE_PATH}/saved_game.json", "w") as f:
            json.dump(all_player_datas, f)

if __name__ == "__main__":
    with open(f"{RESOURCE_PATH}/resources/AdventureSoft_logo.txt", "r") as f:
        print(f"{Fore.CYAN}Welcome to...\n{Style.BRIGHT}{f.read()}{Style.RESET_ALL}")

    while True:
        choice = get_valid_arr_input(
            f"{Fore.CYAN}Choose an option:{Style.RESET_ALL}\n",
            [f"{Fore.GREEN}New Game{Style.RESET_ALL}", f"{Fore.YELLOW}Load Game{Style.RESET_ALL}", f"{Fore.RED}Delete Games{Style.RESET_ALL}", f"{Fore.MAGENTA}Exit{Style.RESET_ALL}"]
        )
        player = PlayerData()

        if choice == 0:
            player.new_game()
        elif choice == 1 and not player.load_game():
            continue
        elif choice == 2:
            player.delete_game()
            continue
        elif choice == 3:
            print(f"{Fore.GREEN}Thanks for playing! Goodbye.{Style.RESET_ALL}")
            exit(1)

        while player.play_game():
            pass
