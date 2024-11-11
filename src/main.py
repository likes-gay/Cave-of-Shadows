import json
import pathlib
from io import TextIOWrapper
from typing import TypedDict
from inputs import get_valid_input, get_valid_arr_input, get_valid_bool_input
from datetime import datetime

game_word = {
	"Cave Entrance": {
		"description": "You stand at the entrance of the Cave of Shadows. The air is thick with the scent of damp earth and decay. Faint whispers seem to call from within.",
		"options": [
			{
				"name": "Enter the Cave",
				"next": "Dark Tunnel"
			},
			{
				"name": "Turn Back",
				"next": "Village"
			}
		],
		"items": []
	},

	"Village": {
		"description": "You turn away from the dark cave, choosing to play it safe. The walk back to the village is quiet, and you reflect on your decision. You feel the warmth of the tavern ahead as the night deepens.",
		"options": [],
		"items": []
	},

	"Dark Tunnel": {
		"description": "You step into the darkness. The light from your lantern flickers and dances as you walk deeper into the cave. Suddenly, the path ahead splits into two directions.",
		"options": [
			{
				"name": "Take the Narrow Path",
				"next": "Narrow Path"
			},
			{
				"name": "Take the Wide Path",
				"next": "Wide Path"
			}
		],
		"items": []
	},

	"Narrow Path": {
		"description": "You crawl through the tight space, the lantern flickering nervously as the walls close in. After a while, the ground suddenly gives way beneath you.",
		"options": [
			{
				"name": "Try to Climb Out",
				"next": "Bad Ending - Fall to Doom"
			},
			{
				"name": "Stay Still",
				"next": "Pit Ledge Escape"
			}
		],
		"items": []
	},

	"Bad Ending - Fall to Doom": {
		"description": "You struggle to climb, but the walls are too slick. The pit seems endless. Darkness closes in as your strength fades. The cave claims another victim.",
		"options": [],
		"items": []
	},

	"Pit Ledge Escape": {
		"description": "You pause, letting your eyes adjust to the darkness. Eventually, you spot a narrow ledge along the pit's edge. You climb onto it and manage to escape. You return to the fork in the path.",
		"options": [
			{
				"name": "Take the Wide Path",
				"next": "Wide Path"
			}
		],
		"items": []
	},

	"Wide Path": {
		"description": "You follow the wider path toward a faint glow in the distance. Soon, you find yourself in a large cavernous room. A glowing chest sits in the center, with strange symbols carved into the walls.",
		"options": [
			{
				"name": "Open the Chest",
				"next": "Treasure Room - Chest Opened"
			},
			{
				"name": "Leave the Chest",
				"next": "Leave Cave - Neutral Ending 1"
			}
		],
		"items": []
	},

	"Treasure Room - Chest Opened": {
		"description": "You open the chest and find a crystal relic pulsing with energy. As you grasp it, a monstrous creature emerges from the shadows. The battle is about to begin.",
		"options": [
			{
				"name": "Use the Relic's Light to Blind the Creature",
				"next": "Victory - Success Ending"
			},
			{
				"name": "Use the Relic to Charge Your Sword with Power",
				"next": "Creature Attack - Tragic Ending"
			},
			{
				"name": "Throw the Relic as a Distraction and Attack",
				"next": "Creature Attack - Tragic Ending"
			}
		],
		"items": ["Crystal Relic"]
	},
	
	"Creature Attack - Tragic Ending": {
		"description": "You fail to control the relic's power. The creature attacks swiftly, and in a heartbeat, your life is taken. The Cave of Shadows claims another soul.",
		"options": [],
		"items": []
	},

	"Creature Attack - Tragic Ending 2": {
		"description": "You attempt to throw the relic as a distraction, but the creature ignores it. It charges at you, striking swiftly, and your life fades in the darkness.",
		"options": [],
		"items": []
	},

	"Victory - Success Ending": {
		"description": "You raise the relic high, blinding the creature. Seizing the opportunity, you strike with your sword, killing it. The treasure is yours, and you return to the village as a hero.",
		"options": [],
		"items": ["Crystal Relic", "Ancient Treasure"]
	},

	"Leave Cave - Neutral Ending 1": {
		"description": "You decide that the chest isn't worth the risk. You leave the cave empty-handed but alive. The village is a welcome sight as you return, but something nags at you — the treasure remains lost.",
		"options": [],
		"items": []
	},

	"Leave Cave - Neutral Ending 2": {
		"description": "You leave the cave, walking away from the unknown dangers. The village feels safer as you return, but you can't help but wonder what the treasure could have meant.",
		"options": [],
		"items": []
	},

	"Leave Cave - Neutral Ending 3": {
		"description": "You exit the cave, choosing to live rather than risk everything for treasure. You return to the village and settle into a quiet life, but the mystery of the cave lingers in your thoughts.",
		"options": [],
		"items": []
	}
}

class PlayerDataType(TypedDict):
	current_location: str
	inventory: list[str]
	game_name: str
	last_updated: int

resource_location = pathlib.Path(__file__).parent.resolve()

def get_save_game_contents(file_pointer: TextIOWrapper | None = None) -> list[PlayerDataType]:
	try:
		if file_pointer is None:
			with open(f"{resource_location}/saved_game.json", "r") as file_pointer:
				return json.load(file_pointer)
		
		file_pointer.seek(0)
		return json.load(file_pointer)
	except (FileNotFoundError, json.JSONDecodeError):
		with open(f"{resource_location}/saved_game.json", "w") as file_pointer:
			json.dump([], file_pointer)
		return []

class PlayerData():
	current_location: str
	inventory: list[str]
	game_name: str
	last_updated: int

	def __init__(self):
		self.current_location = list(game_word.keys())[0]
		self.inventory = []
	
	def play_game(self):
		if self.current_location not in game_word:
			print("Game Over, this needs to be created")
			return False
		location = game_word[self.current_location]
		print("You are at " + self.current_location)
		print(location["description"])

		if not location["options"]:
			return False

		choice = get_valid_arr_input("What do you want to do next?: ", list(map(lambda x: x["name"], location["options"])))
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
		
		with open(f"{resource_location}/saved_game.json", "w") as f:
			json.dump(all_player_datas, f)



if __name__ == "__main__":
	with open(f"{resource_location}/resources/AdventureSoft_logo.txt", "r") as f:
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