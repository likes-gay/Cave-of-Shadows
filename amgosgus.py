import json
from typing import TypedDict
from os import path
from inputs import get_valid_input, get_valid_arr_input, get_valid_bool_input
from datetime import datetime

game_word = {
	"Cave Entrance": {
		"description": "You stand at the entrance of the Cave of Shadows. The air is thick with the scent of damp earth and decay.",
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

	"Split Path": {
        "description": "The path ahead splits into two. One is narrow and winding, barely wide enough to squeeze through. The other is a wider, smoother path with a faint glow in the distance.",
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
		"description": "You crawl through the tight space, the lantern flickering as the walls close in around you.",
		"paths": [
			{
				"name": "Continue Forward",
				"next": "Escape Narrow Path"
			},
			{
				"name": "Turn Back",
				"next": "Split Path"
			}
		],
	},
	"Escape Narrow Path": {
		"description": "You spot a narrow ledge along the edge of the pit and manage to escape back to the fork in the path.",
		"options": [
			{
				"name": "Take the Narrow Path",
				"next": "Narrow Path"
			}
		],
		"items": []
	},
	"Wide Path": {
		"description": "You follow the wider path toward a faint glow ahead, leading into a cavernous room.",
		"options": [
			{
				"name": "Open the Chest",
				"next": "Treasure Room"
			},
			{
				"name": "Leave the Cave",
				"next": "Village"
			}
		]
	},
	"Treasure Room": {
		"description": "In the center of the room, a chest glows with an eerie light. Strange symbols cover the walls. A choice awaits.",
		"options": [
			{
				"name": "Open the Chest",
				"next": "Victory Ending"
			},
			{
				"name": "Leave the Chest",
				"next": "Neutral Ending"
			}
		]
	},
	"Village": {
		"description": "You return to the village, leaving the mysterious cave behind. Perhaps the treasure was never meant to be found.",
		"options": [],
		"items": []
	},
	"Bad Ending": {
		"description": "The darkness overwhelms you, and the Cave of Shadows claims another victim. You have perished.",
		"options": [],
		"items": []
	},

	"Neutral Ending": {
		"description": "You leave the cave without opening the chest, feeling relief but also a hint of regret.",
		"options": [],
		"items": []
	},
	"Tragic Ending": {
		"description": "The creature's attack is swift, and you are defeated. Darkness surrounds you as you fall.",
		"options": [],
		"items": []
	},
	"Victory Ending": {
		"description": "With the relic's light, you blind the creature and defeat it! You claim the treasure and return to the village as a hero.",
		"options": [],
		"items": [
			{
				"name": "Treasure",
				"next": "Village"
			}
		]
	}
}


print("""Welcome to...
   _____       .___                    __                           _________       _____  __   
  /  _  \\    __| _/__  __ ____   _____/  |_ __ _________   ____    /   _____/ _____/ ____\/  |_ 
 /  /_\\  \\  / __ |\\  \/ // __ \\ /    \\   __\\  |  \_  __ \_/ __ \\   \_____  \\ /  _ \\   __\\\   __\\
/    |    \/ /_/ | \\   /\\  ___/|   |  \\  | |  |  /|  | \/\\  ___/   /        (  <_> )  |   |  |  
\____|__  /\____ |  \_/  \___  >___|  /__| |____/ |__|    \___  > /_______  /\____/|__|   |__|  
        \/      \/           \/     \/                        \/          \/                    """)

class PlayerDataType(TypedDict):
	current_location: str
	inventory: list[str]
	game_name: str
	last_updated: int

class PlayerData():
	current_location: str = list(game_word.keys())[0]
	inventory: list[str] = []
	game_name: str
	last_updated: int

	def __init__(self):
		pass
	
	def play_game(self):
		location = game_word[self.current_location]
		print("You are at " + self.current_location)
		print(location["description"])

		if location["options"]:
			choice = get_valid_arr_input("What do you want to do next?: ", location["options"])
			self.current_location = location["options"][choice]
			self._save_game()
			return True
		return False


	def new_game(self):
		self.game_name = get_valid_input("What will you name this save? ")
		self._save_game()

	def load_game(self):
		file_exists = path.exists("saved_game.json")
		with open("saved_game.json", "r" if file_exists else "w") as f:
			all_player_datas: list[PlayerDataType] = json.load(f) if file_exists else []

		if all_player_datas:
			choicen_save_int = get_valid_arr_input("Choose a game: ", list(map(lambda x: f"{x['game_name']} - last updated: {datetime.fromtimestamp(x['last_updated']).strftime('%d-%m-%Y %H:%M:%S')}", all_player_datas)))
			loaded_save = all_player_datas[choicen_save_int]

			print(f"{loaded_save['game_name']} has been chosen.")
			self.__dict__ = loaded_save
			self._save_game()
			return
			
		print("No saved games found. So we'll start a new game.")
		self.new_game()

	def _save_game(self):
		file_exists = path.exists("saved_game.json")
		with open("saved_game.json", "r+" if file_exists else "w+") as f:
			all_player_datas: list[PlayerDataType] = json.load(f) if file_exists else []

			self.last_updated = datetime.now().timestamp()
			all_player_datas.append(self.__dict__)
			f.seek(0)
			json.dump(all_player_datas, f)



if __name__ == "__main__":
	choice = get_valid_arr_input("Choose an option: ", ["New Game", "Load Game", "Exit"])
	player = PlayerData()

	if choice == 0:
		player.new_game()
	elif choice == 1:
		player.load_game()
	else:
		exit()


		# 
	
	while True:
		if not player.play_game():
			break