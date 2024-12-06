import time
from colorama import Fore, Style
from platform import system

if system() == "Windows":
	from msvcrt import getch, kbhit
else: # Linux
	from getch import getch
	import sys, tty, termios

def ignore_input_time(seconds_to_ignore: float):
	if system() == "Windows":
		start_time = time.time()
		while time.time() - start_time < seconds_to_ignore:
			while kbhit():
				getch()
			time.sleep(0.1)
		return

	# Linux
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
		tty.setcbreak(sys.stdin.fileno())
		time.sleep(seconds_to_ignore)
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def get_valid_arr_input(
		prompt: str,
		options: list[str],
	) -> int:
	while True:
		for i, option in enumerate(options, start=1):
			print(f"{i}. {option}")
		
		choice = input(prompt)
		if not choice.isdigit():
			print(f"{Fore.RED}Invalid input.{Style.RESET_ALL} Please enter a number.")
			continue
		choice = int(choice)

		if choice < 1 or choice > len(options):
			print(f"{Fore.RED}Invalid input.{Style.RESET_ALL} Please choose a number from the range.")
			continue

		return choice - 1

def get_valid_bool_input(
		prompt: str,
	) -> bool:
	while True:
		choice = input(f"{prompt} (yes/no)").lower()
		if choice not in ["yes", "no", "y", "n"]:
			print(f"{Fore.RED}Invalid input.{Style.RESET_ALL} Please enter \"yes\"/\"y\" or \"no\"\"n\".")
			continue

		return choice in ["yes", "y"]

def get_valid_any_input(
		prompt: str,
	):
	print(prompt, end="", flush=True)
	getch()

def get_valid_input(
		prompt: str,
	) -> str:
	while True:
		choice = input(prompt)
		if not choice:
			print(f"{Fore.RED}Invalid input.{Style.RESET_ALL} Please enter a valid value.")
			continue

		return choice