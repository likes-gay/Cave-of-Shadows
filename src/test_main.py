from main import GAME_WORLD

def test_no_invalid_nexts():
	for location, value in GAME_WORLD.items():
		for option in value["options"]:
			assert option["next"] in GAME_WORLD, f"Invalid \"next\" reference in location \"{location}\": {option['next']}"

def test_no_unused_locations():
	locations = set(GAME_WORLD.keys())
	
	visited = set()
	to_visit = {next(iter(GAME_WORLD.keys()))}

	while to_visit:
		current_location = to_visit.pop()
		if current_location in visited:
			continue
		visited.add(current_location)
		locations.discard(current_location)
		for option in GAME_WORLD[current_location]["options"]:
			to_visit.add(option["next"])

	assert len(locations) == 0, f"Unused locations found: \"{', '.join(locations)}\""