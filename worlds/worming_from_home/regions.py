from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region

if TYPE_CHECKING:
    from .world import WormingFromHomeWorld

# A region is a container for locations ("checks"), which connects to other regions via "Entrance" objects.
# Many games will model their Regions after physical in-game places, but you can also have more abstract regions.
# For a location to be in logic, its containing region must be reachable.
# The Entrances connecting regions can have rules - more on that in rules.py.
# This makes regions especially useful for traversal logic ("Can the player reach this part of the map?")

# Every location must be inside a region, and you must have at least one region.
# This is why we create regions first, and then later we create the locations (in locations.py).


def create_and_connect_regions(world: WormingFromHomeWorld) -> None:
    create_all_regions(world)
    connect_regions(world)


def create_all_regions(world: WormingFromHomeWorld) -> None:
    # Creating a region is as simple as calling the constructor of the Region class.
    overworld = Region("Overworld", world.player, world.multiworld)
    shop_tier_1 = Region("Shop Tier 1", world.player, world.multiworld)
    shop_tier_2 = Region("Shop Tier 2", world.player, world.multiworld)
    shop_tier_3 = Region("Shop Tier 3", world.player, world.multiworld)
    promotion_interview = Region("Promotion Interview", world.player, world.multiworld)

    # Let's put all these regions in a list.
    regions = [overworld, shop_tier_1, shop_tier_2, shop_tier_3, promotion_interview]

    # Some regions may only exist if the player enables certain options.
    # In our case, the Hammer locks the top middle chest in its own room if the hammer option is enabled.
    #if world.options.hammer:
    #    top_middle_room = Region("Top Middle Room", world.player, world.multiworld)
    #    regions.append(top_middle_room)

    # We now need to add these regions to multiworld.regions so that AP knows about their existence.
    world.multiworld.regions += regions


def connect_regions(world: WormingFromHomeWorld) -> None:
    # We have regions now, but still need to connect them to each other.
    # But wait, we no longer have access to the region variables we created in create_all_regions()!
    # Luckily, once you've submitted your regions to multiworld.regions,
    # you can get them at any time using world.get_region(...).
    overworld = world.get_region("Overworld")
    shop_tier_1 = world.get_region("Shop Tier 1")
    shop_tier_2 = world.get_region("Shop Tier 2")
    shop_tier_3 = world.get_region("Shop Tier 3")
    promotion_interview = world.get_region("Promotion Interview")
    #final_boss_room = world.get_region("Final Boss Room")


    #overworld_to_bottom_right_room = Entrance(world.player, "Overworld to Bottom Right Room", parent=overworld)

    # An even easier way is to use the region.connect helper.
    overworld.connect(shop_tier_1, "Overworld to Shop Tier 1")
    shop_tier_1.connect(shop_tier_2, "Shop Tier 1 to Shop Tier 2")
    shop_tier_2.connect(shop_tier_3, "Shop Tier 2 to Shop Tier 3")
    shop_tier_3.connect(promotion_interview, "Shop Tier 3 to Promotion Interview")
    #promotion_interview.connect(final_boss_room, "Promotion Interview to Final Boss Room")

    # The region.connect helper even allows adding a rule immediately.
    # We'll talk more about rule creation in the set_all_rules() function in rules.py.
    #overworld.connect(top_left_room, "Overworld to Top Left Room", lambda state: state.has("Key", world.player))

    # Some Entrances may only exist if the player enables certain options.
    # In our case, the Hammer locks the top middle chest in its own room if the hammer option is enabled.
    # In this case, we previously created an extra "Top Middle Room" region that we now need to connect to Overworld.
    #if world.options.hammer:
    #    top_middle_room = world.get_region("Top Middle Room")
    #    overworld.connect(top_middle_room, "Overworld to Top Middle Room")
