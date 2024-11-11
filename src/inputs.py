def get_valid_arr_input(
		prompt: str,
		options: list[str],
	) -> int:
	while True:
		for i, option in enumerate(options, start=1):
			print(f"{i}. {option}")
		
		choice = input(prompt)
		if not choice.isdigit():
			print("Invalid input. Please enter a number.")
			continue
		choice = int(choice)

		if choice < 1 or choice > len(options):
			print("Invalid input. Please choose a number from the range.")
			continue

		return choice - 1

def get_valid_bool_input(
		prompt: str,
	) -> bool:
	while True:
		choice = input(f"{prompt} (yes/no)").lower()
		if choice not in ["yes", "no", "y", "n"]:
			print("Invalid input. Please enter \"yes\" or \"no\".")
			continue

		return choice in ["yes", "y"]

def get_valid_input(
		prompt: str,
	) -> str:
	while True:
		choice = input(prompt)
		if not choice:
			print("Invalid input. Please enter a valid value.")
			continue

		return choice