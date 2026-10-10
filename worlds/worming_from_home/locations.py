from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

from . import items

if TYPE_CHECKING:
    from .world import WormingFromHomeWorld

# Every location must have a unique integer ID associated with it.
# We will have a lookup from location name to ID here that, in world.py, we will import and bind to the world class.
# Even if a location doesn't exist on specific options, it must be present in this lookup.
LOCATION_NAME_TO_ID = {
    "Shop: Reading Nook": 1,
    "Shop: Worm Weights": 2,
    "Shop: Smartphone Charger": 3,
    "Shop: Stabilized Mouse": 4,
    "Shop: Slim Keyboard": 5,
    "Shop: L-Desk": 6,
    "Shop: Comfy Reading Nook": 7,
    "Shop: Worm Barbell": 8,
    "Shop: Monitor Extension": 9,
    "Shop: Cozy Reading Nook": 10,
    "Shop: Worm Squat Machine": 11,
    "Shop: Touch Keyboard": 12,
    "Shop: Wormgonomic Mouse": 13,
    "Shop: Water Cooler": 14,
    "Shop: Newton's Cradle": 15,
    "Shop: Coffee Machine": 16,
    "Shop: Printer": 17,
    "Shop: Cup of Pens": 18,
    "Shop: Worm Trampoline": 19,
    "Shop: Pile of Dirt": 20,
    "Shop: Webcam": 21,
    "Shop: Soundboard": 22,
    "Shop: Kevin": 23,

    # Interns
    "Shop: Intern 1": 101,
    "Shop: Intern 2": 102,
    "Shop: Intern 3": 103,
    "Shop: Intern 4": 104,
    "Shop: Intern 5": 105,
    "Shop: Intern 6": 106,
    "Shop: Intern 7": 107,
    "Shop: Intern 8": 108,
    "Shop: Intern 9": 109,
    "Shop: Intern 10": 110,
    "Shop: Intern 11": 111,
    "Shop: Intern 12": 112,
    "Shop: Intern 13": 113,
    "Shop: Intern 14": 114,
    "Shop: Intern 15": 115,
    "Shop: Intern 16": 116,
    "Shop: Intern 17": 117,
    "Shop: Intern 18": 118,
    "Shop: Intern 19": 119,
    "Shop: Intern 20": 120,
    "Shop: Intern 21": 121,
    "Shop: Intern 22": 122,
    "Shop: Intern 23": 123,
    "Shop: Intern 24": 124,
    "Shop: Intern 25": 125,
    "Shop: Intern 26": 126,
    "Shop: Intern 27": 127,
    "Shop: Intern 28": 128,
    "Shop: Intern 29": 129,
    "Shop: Intern 30": 130,
    "Shop: Intern 31": 131,
    "Shop: Intern 32": 132,
    "Shop: Intern 33": 133,
    "Shop: Intern 34": 134,
    "Shop: Intern 35": 135,
    "Shop: Intern 36": 136,
    "Shop: Intern 37": 137,
    "Shop: Intern 38": 138,
    "Shop: Intern 39": 139,
    "Shop: Intern 40": 140,
    "Shop: Intern 41": 141,
    "Shop: Intern 42": 142,
    "Shop: Intern 43": 143,
    "Shop: Intern 44": 144,
    "Shop: Intern 45": 145,
    "Shop: Intern 46": 146,
    "Shop: Intern 47": 147,
    "Shop: Intern 48": 148,
    "Shop: Intern 49": 149,
    "Shop: Intern 50": 150,
}

# Each Location instance must correctly report the "game" it belongs to.
# To make this simple, it is common practice to subclass the basic Location class and override the "game" field.
class WormingFromHomeLocation(Location):
    game = "Worming from Home"


# Let's make one more helper method before we begin actually creating locations.
# Later on in the code, we'll want specific subsections of LOCATION_NAME_TO_ID.
# To reduce the chance of copy-paste errors writing something like {"Chest": LOCATION_NAME_TO_ID["Chest"]},
# let's make a helper method that takes a list of location names and returns them as a dict with their IDs.
# Note: There is a minor typing quirk here. Some functions want location addresses to be an "int | None",
# so while our function here only ever returns dict[str, int], we annotate it as dict[str, int | None].
def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}


def create_all_locations(world: WormingFromHomeWorld) -> None:
    create_regular_locations(world)
    create_events(world)


def create_regular_locations(world: WormingFromHomeWorld) -> None:
    # Finally, we need to put the Locations ("checks") into their regions.
    # Once again, before we do anything, we can grab our regions we created by using world.get_region()
    overworld = world.get_region("Overworld")
    shop_tier_1 = world.get_region("Shop Tier 1")
    shop_tier_2 = world.get_region("Shop Tier 2")
    shop_tier_3 = world.get_region("Shop Tier 3")
    final_boss_room = world.get_region("Final Boss Room")

    # One way to create locations is by just creating them directly via their constructor.
    bottom_left_chest = WormingFromHomeLocation(
        world.player, "Bottom Left Chest", world.location_name_to_id["Bottom Left Chest"], overworld
    )

    # You can then add them to the region.
    overworld.locations.append(bottom_left_chest)

    # A simpler way to do this is by using the region.add_locations helper.
    # For this, you need to have a dict of location names to their IDs (i.e. a subset of location_name_to_id)
    # Aha! So that's why we made that "get_location_names_with_ids" helper method earlier.
    # You also need to pass your overridden Location class.
    shop_tier_1_locations = get_location_names_with_ids(
        ["Shop: Reading Nook", "Shop: Worm Weights", "Shop: Smartphone Charger", 
        "Shop: Stabilized Mouse", "Shop: Thin Keyboard", "Shop: L-Desk", 
        "Shop: Water Cooler", "Shop: Newton's Cradle"]
    )
    shop_tier_1.add_locations(shop_tier_1_locations, WormingFromHomeLocation)

    shop_tier_2_locations = get_location_names_with_ids(
        ["Shop: Comfy Reading Nook", "Shop: Worm Barbell", "Shop: Coffee Machine", 
        "Shop: Printer", "Shop: Cup of Pens"]
    )
    shop_tier_2.add_locations(shop_tier_2_locations, WormingFromHomeLocation)

    shop_tier_3_locations = get_location_names_with_ids(
        ["Shop: Monitor Extension", "Shop: Cozy Reading Nook", "Shop: Worm Squat Machine",
        "Shop: Touch Keyboard", "Shop: Wormgonomic Mouse", "Shop: Worm Trampoline", 
        "Shop: Pile of Dirt", "Shop: Webcam", "Shop: Soundboard", "Shop: Kevin"]
    )
    shop_tier_3.add_locations(shop_tier_3_locations, WormingFromHomeLocation)


def create_events(world: WormingFromHomeWorld) -> None:
    
    # Document signed event
    shop_tier_2 = world.get_region("Shop Tier 2")

    # One way to create an event is simply to use one of the normal methods of creating a location.
    sign_soul_away_location = WormingFromHomeLocation(world.player, "Event: Sign Contract", None, shop_tier_2)
    shop_tier_2.locations.append(sign_soul_away_location)

    # create event item for signing away soul and assign it to the event location
    sign_soul_away_item = items.WormingFromHomeItem("Signed Contract", ItemClassification.progression, None, world.player)
    sign_soul_away_location.place_locked_item(sign_soul_away_item)


    # Create Interview Success event
    final_boss_room = world.get_region("Final Boss Room")

    final_boss_room.add_event(
        "Event: Interview Succeeded", "Victory", location_type=WormingFromHomeLocation, item_type=items.WormingFromHomeItem
    )

