import json, pathlib, shlex, sys, time
from io import TextIOWrapper
from typing import TypedDict
from datetime import datetime
from inputs import get_valid_input, get_valid_any_input, get_valid_arr_input, ignore_input_time
from colorama import Fore, Style, init, deinit

RESOURCE_PATH = pathlib.Path(__file__).parent.resolve()

if getattr(sys, "frozen", False):
	SAVE_FILE_PATH = pathlib.Path(sys.executable).parent / "saved_game.json"
else:
	SAVE_FILE_PATH = RESOURCE_PATH / "saved_game.json"

GAME_WORLD = {
	"Cave Entrance": {
		"description": (
			"You step into the darkness. The light from your lantern dances on the walls as you walk deeper into the cave.\n"
			"It's eerily quiet except for the sound of your footsteps echoing against the stone walls.\n"
			"Suddenly, the path ahead splits into two."
		),
		"options": [
			{"name": "Take the freightening narrow path", "next": "Narrow Path"},
			{"name": "Take the menacing wide path", "next": "Wide Path"}
		],
	},

	"Narrow Path": {
		"description": (
			"You crawl through the tight space, your lantern flickering nervously as the walls close in on you.\n"
			"The flame flickers and disappears in an instant, with just the moonlight to help you see.\n"
			"After a while, the ground suddenly starts to split beneath you."
		),
		"options": [
			{"name": "Attempt to climb out and escape", "next": "Tragic Ending 1 - Falling to your doom!"},
			{"name": "Shuffle along to the other side of the tight space", "next": "Pit Ledge Escape"}
		],
	},

	"Pit Ledge Escape": {
		"description": (
			"Being careful with your footing, you shuffle along and find a path on the other side.\n"
			"Feeling curious, you follow it and it leads you... back to where you started!\n" 
			"You should probably investigate those rumors, maybe the other path has some clues?"
		),
		"options": [
			{"name": "Take the wide path this time", "next": "Wide Path"},
			{"name": "Leave the cave, those rumors probably aren't true anyway", "next": "Neutral Ending - Safe and sound!"}
		],
	},

	"Wide Path": {
		"description": (
			"You follow the wider path toward a faint glow in the distance. Soon, you find yourself in a large cavernous room.\n"
			"A glowing chest sits in the centre, with strange symbols carved into the walls.\n"
			"Should you check it for rare treasures or leave it incase it's a trap?"
		),
		"options": [
			{"name": "Open the chest, maybe it has something powerful!", "next": "Treasure Room - Chest Opened"},
			{"name": "Leave the cave, it could be deadly...", "next": "Neutral Ending - Safe and sound!"}
		],
	},

	"Treasure Room - Chest Opened": {
		"description": (
			"You open the chest and find a crystal relic pulsing with energy. As you grasp it, a monstrous creature emerges from the shadows.\n"
			"Your heart quickens, your muscles tense up and you brace yourself, for the battle is about to begin.\n"
			"What will you do against the giant, villainous Creature??"
		),
		"options": [
			{"name": "Use the Relic's light to blind the Creature", "next": "Good Ending 2 - Blinded by the light!"},
			{"name": "Combine the Relic with your sword to greatly increase its power", "next": "Tragic Ending 2 - Snack for the Creature!"},
			{"name": "Throw the Relic as a distraction and attack", "next": "Tragic Ending 3 - Killed by the Creature!"},
			{"name": "Throw down all items and equipment and flee the caves", "next": "Escaping the Treasure Room"}
		],
	},

	"Escaping the Treasure Room": {
		"description": (
			"You throw everything you have down and quickly remove all your armour, making you lighter and faster.\n"
			"While the Creature gobbles up your belongings, you sprint your way out of the cave and head back to village.\n"
			"You could tell the Mayor about this, but would he believe you? Maybe you should just rest it off..."
		),
		"options": [
			{"name": "Inform the village Mayor about the Creature and prepare an army to defeat it", "next": "Good Ending 1 - Victory!"},
			{"name": "Head back to your room in the tavern and rest, hoping the Creature goes away", "next": "Neutral Ending - Safe and sound!"}
		],
	},
	
	"Good Ending 1 - Victory!": {
		"description": (
			"You and your grand army storm towards the cave, weapons drawn and battle cries filling you with determination.\n"
			"Swords slash into flesh, the Creature roars and your blood fills with fury!\n"
			"Together, you all charge the creature and strike it down, claiming an easy victory and 50 percent off your stay at the local tavern."
		),
		"options": []
	},

	"Good Ending 2 - Blinded by the light!": {
		"description": (
			"You raise the relic high, the moonlight reflecting off it and into the Creature's eyes, blinding it.\n"
			"Seizing the opportunity, you strike with your sword, killing it.\n"
			"Thanks to your heroic venture, the Creature shall be fed no more and the village is safe! (selling the Relic made you pretty rich too!)"
		), # Check teams for my final suggestions
		"options": []
	},

	"Tragic Ending 1 - Falling to your doom!": {
		"description": (
			"You struggle to climb, but the walls are covered in a mysterious ooze.\n"
			"As the floor becomes less and less, you have nothing to stand on and fall downwards.\n"
			"The cave claims another helpless victim, the rumors forever a mystery..."
		),
		"options": [],
	},
	
	"Tragic Ending 2 - Snack for the Creature!": {
		"description": (
			"You try combining the two but... it failed?\n"
			"Whilst you stand confused, the Creature seizes the opportunity and swallows you whole!\n"
			"With noone alive to tell about the Creature, the town reminds none the wiser about it lurking within the cave..."
		),
		"options": [],
	},

	"Tragic Ending 3 - Killed by the Creature!": {
		"description": (
			"You attempt to throw the relic as a distraction, but the creature ignores it.\n"
			"With your sword bouncing right off of its scaly skin, it defeats you in one fell swoop.\n"
			"So the rumor was true! Although I doubt you can tell anyone about it now..."
		),
		"options": [],
	},

	"Neutral Ending - Safe and sound!": {
		"description": (
			"You decide that the dangers of the cave are too great. Retracing your steps, you carefully make your way back to the entrance.\n"
			"The cool night air greets you as you step outside. Though you leave the cave empty-handed, you feel relieved to be alive.\n"
			"The rumors shall stay as just rumors - for now."
		),
		"options": []
	}
}


class PlayerDataType(TypedDict):
	current_location: str
	game_name: str
	last_updated: int

def get_save_game_contents(file_pointer: TextIOWrapper | None = None) -> list[PlayerDataType]:
	try:
		if file_pointer is None:
			with open(SAVE_FILE_PATH, "r") as f:
				return json.load(f)
		 
		file_pointer.seek(0)
		return json.load(file_pointer)
	except (FileNotFoundError, json.JSONDecodeError):
		with open(SAVE_FILE_PATH, "w") as f:
			json.dump([], f)
		return []

def get_game_name_syntax(
		game_data: list[PlayerDataType],
		exclude_last_update: bool | None = False
	) -> list[str]:
	arr: list[str] = []
	for game in game_data:
		name = shlex.quote(game["game_name"])
		last_updated = datetime.fromtimestamp(game["last_updated"]).strftime("%d-%m-%Y %H:%M:%S")
		if exclude_last_update:
			arr.append(name)
			continue
		arr.append(f"{name} - last updated: {last_updated}")
	return arr

class PlayerData():
	current_location: str
	game_name: str
	last_updated: int

	def __init__(self):
		self.current_location = list(GAME_WORLD.keys())[0]

	def _print_section(self, title: str, content: str, color=Fore.GREEN):
		print(f"{color}{Style.BRIGHT}\n{'-' * 40}\n{title.upper()}\n{'-' * 40}\n{Style.RESET_ALL}{content}\n")
	
	def play_game(self):
		location = GAME_WORLD[self.current_location]
		
		if not location["options"]:
			self._print_section(f"Ending: {self.current_location}", location["description"], Fore.CYAN)
			print(f"{Fore.BLUE}This is the end of the game. Thank you for playing!{Style.RESET_ALL}")
			return False
		
		self._print_section(f"Location: {self.current_location}", location["description"], Fore.YELLOW)
		
		if len(location["options"]) == 1 and "name" not in location["options"][0]:
			self.current_location = location["options"][0]["next"]
			self._save_game()

			get_valid_any_input(f"{Fore.CYAN}Press any key to continue...{Style.RESET_ALL}")
			return True

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
			choicen_save_int = get_valid_arr_input(f"{Fore.CYAN}Choose a save to delete: {Style.RESET_ALL}", game_names)
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
				print(f"{Fore.RED}This name is already taken, please enter another.{Style.RESET_ALL}")
				continue
			self.game_name = input_name
			break

		self._save_game()
		print(f"{Fore.GREEN}New game '{shlex.quote(self.game_name)}' created!{Style.RESET_ALL}")

	def load_game(self):
		all_player_datas = get_save_game_contents()
		if all_player_datas:
			choicen_save_int = get_valid_arr_input(
				f"{Fore.CYAN}Choose a game to load:{Style.RESET_ALL}\n",
				[f"{Fore.YELLOW}{x['game_name']} - last updated: {datetime.fromtimestamp(x['last_updated']).strftime('%d-%m-%Y %H:%M:%S')}{Style.RESET_ALL}" for x in all_player_datas]
			)
			loaded_save = all_player_datas[choicen_save_int]

			self.current_location = loaded_save["current_location"]
			self.game_name = loaded_save["game_name"]
			self.last_updated = loaded_save["last_updated"]
			print(f"{Fore.GREEN}Loaded game: {shlex.quote(self.game_name)}{Style.RESET_ALL}")
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

		with open(SAVE_FILE_PATH, "w") as f:
			json.dump(all_player_datas, f)

def slow_print(text: str, delay: float = .1):
	for char in text.split("\n"):
		print(char, flush=True)
		ignore_input_time(delay)
	print()

if __name__ == "__main__":
	init()
	with open(RESOURCE_PATH / "resources/AdventureSoft_presents.txt", "r") as f:
		slow_print(f"{Fore.CYAN}{Style.BRIGHT}{f.read()}{Style.RESET_ALL}", delay=.25)

	with open(RESOURCE_PATH / "resources/CaveofShadows_logo.txt", "r") as f:
		slow_print(f"{Fore.MAGENTA}{f.read()}{Style.RESET_ALL}")

	while True:
		choice = get_valid_arr_input(
			f"{Fore.CYAN}Please choose an option:{Style.RESET_ALL}\n",
			[f"{Fore.GREEN}Start a new game{Style.RESET_ALL}", f"{Fore.YELLOW}Load a saved game{Style.RESET_ALL}", f"{Fore.RED}Delete a saved game{Style.RESET_ALL}", f"{Fore.MAGENTA}Exit the game{Style.RESET_ALL}"]
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
			print(f"{Fore.GREEN}Thank your for playing Cave of Shadows! Goodbye.{Style.RESET_ALL}")
			WAITING_TIME = 1
			for i in range(WAITING_TIME):
				print(f"{Fore.RED}Exiting in {WAITING_TIME - i}s...{Style.RESET_ALL}", end="\r")
				ignore_input_time(1)
			deinit()
			break

		while player.play_game():
			pass