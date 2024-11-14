import json, pathlib
from io import TextIOWrapper
from typing import TypedDict
from inputs import get_valid_input, get_valid_arr_input
from datetime import datetime

RESOURCE_PATH = pathlib.Path(__file__).parent.resolve()
GAME_WORLD = {
    "Cave Entrance": {
        "description": (
            "You stand at the entrance of the Cave of Shadows. The air is thick with the scent of damp earth and decay. "
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
            "You turn away from the dark cave, choosing to play it safe. The walk back to the village is quiet, and you reflect on your decision. "
            "The warmth of the tavern greets you as the night deepens. You've decided to relax and live another day."
        ),
        "options": [],
        "items": []
    },

    "Dark Tunnel": {
        "description": (
            "You step into the darkness. The light from your lantern flickers and dances as you walk deeper into the cave. "
            "It’s eerily quiet except for the sound of your footsteps echoing against the stone walls. Suddenly, the path ahead splits into two."
        ),
        "options": [
            {"name": "Take the Narrow Path", "next": "Narrow Path"},
            {"name": "Take the Wide Path", "next": "Wide Path"}
        ],
        "items": []
    },

    "Narrow Path": {
        "description": (
            "You crawl through the tight space, your lantern flickering nervously as the walls close in on you. "
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
            "You struggle to climb, but the walls are too slick. The pit seems endless. Darkness closes in as your strength fades. "
            "The cave claims another victim."
        ),
        "options": [],
        "items": []
    },

	"Pit Ledge Escape": {
    	"description": (
        	"You pause, letting your eyes adjust to the darkness. Eventually, you spot a narrow ledge along the edge of the pit. "
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
            "You follow the wider path toward a faint glow in the distance. Soon, you find yourself in a large cavernous room. "
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
            "You open the chest and find a crystal relic pulsing with energy. As you grasp it, a monstrous creature emerges from the shadows. "
            "The battle is about to begin."
        ),
        "options": [
            {"name": "Use the Relic’s Light to Blind the Creature", "next": "Victory - Success Ending"},
            {"name": "Use the Relic to Charge Your Sword with Power", "next": "Creature Attack - Tragic Ending"},
            {"name": "Throw the Relic as a Distraction and Attack", "next": "Creature Attack - Tragic Ending 2"}
        ],
        "items": ["Crystal Relic"]
    },

    "Creature Attack - Tragic Ending": {
        "description": (
            "You fail to control the relic's power. The creature attacks swiftly, and in a heartbeat, your life is taken. "
            "The Cave of Shadows claims another soul."
        ),
        "options": [],
        "items": []
    },

    "Creature Attack - Tragic Ending 2": {
        "description": (
            "You attempt to throw the relic as a distraction, but the creature ignores it. It charges at you, striking swiftly, "
            "and your life fades in the darkness."
        ),
        "options": [],
        "items": []
    },

    "Victory - Success Ending": {
        "description": (
            "You raise the relic high, blinding the creature. Seizing the opportunity, you strike with your sword, killing it. "
            "The treasure is yours, and you return to the village as a hero."
        ),
        "options": [],
        "items": ["Crystal Relic", "Ancient Treasure"]
    },

	"Leave Cave - Neutral Ending": {
    	"description": (
        	"You decide that the dangers of the cave are too great. Retracing your steps, you carefully make your way back to the entrance. "
        	"The cool night air greets you as you step outside. Though you leave the cave empty-handed, you feel relieved to be alive. "
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

class PlayerData():
	current_location: str
	inventory: list[str]
	game_name: str
	last_updated: int

	def __init__(self):
		self.current_location = list(GAME_WORLD.keys())[0]
		self.inventory = []
	
	def play_game(self):
		if self.current_location not in GAME_WORLD:
			print("Game Over, this needs to be created")
			return False
		location = GAME_WORLD[self.current_location]
		print("You are at the " + self.current_location)
		print(location["description"])

		if not location["options"]:
			return False

		choice = get_valid_arr_input("\nWhat do you want to do next?: ", list(map(lambda x: x["name"], location["options"])))
		self.current_location = location["options"][choice]["next"]
		self._save_game()
		return True

	def delete_game(self):
		all_player_datas = get_save_game_contents()
		
		if all_player_datas:
			game_names = list(map(lambda x: f"{x.get('game_name')} - last updated: {datetime.fromtimestamp(x['last_updated']).strftime('%d-%m-%Y %H:%M:%S')}", all_player_datas))
			game_names.append("Go back")
			choicen_save_int = get_valid_arr_input("Choose a game: ", game_names)
			if choicen_save_int == len(game_names) - 1:
				return
			all_player_datas.pop(choicen_save_int)
			self._save_game(override=all_player_datas)
			return
		
		print("No saved games found.")

	def new_game(self):
		self.game_name = get_valid_input("What will you name this save? ")
		self._save_game()

	def load_game(self):
		all_player_datas = get_save_game_contents()

		if all_player_datas:
			choicen_save_int = get_valid_arr_input("Choose a game: ", list(map(lambda x: f"{x['game_name']} - last updated: {datetime.fromtimestamp(x['last_updated']).strftime('%d-%m-%Y %H:%M:%S')}", all_player_datas)))
			loaded_save = all_player_datas[choicen_save_int]

			print(f"{loaded_save['game_name']} has been chosen.")
			self.current_location = loaded_save["current_location"]
			self.inventory = loaded_save["inventory"]
			self.game_name = loaded_save["game_name"]
			self.last_updated = loaded_save["last_updated"]
			return True
		
		print("No saved games found.")
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
		print(f"Welcome to...\n{f.read()}")
	
	while True:
		choice = get_valid_arr_input("Choose an option: ", ["New Game", "Load Game", "Delete Games", "Exit"])
		player = PlayerData()

		if choice == 0:
			player.new_game()
		elif choice == 1 and not player.load_game():
			continue
		elif choice == 2:
			player.delete_game()
			continue
		elif choice == 3:
			exit()
			
		while True:
			if not player.play_game():
				break