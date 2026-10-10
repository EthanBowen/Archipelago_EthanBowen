from __future__ import annotations

from typing import TYPE_CHECKING

from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAll, Rule

from .options import HardMode

if TYPE_CHECKING:
    from .world import WormingFromHomeWorld

HAS_KEY = Has("Key")  # Hmm, what could this be? A little foreshadowing perhaps? :) You'll find out if you keep reading!


def set_all_rules(world: WormingFromHomeWorld) -> None:
    # In order for AP to generate an item layout that is actually possible for the player to complete,
    # we need to define rules for our Entrances and Locations.
    # Note: Regions do not have rules, the Entrances connecting them do!
    # We'll do entrances first, then locations, and then finally we set our victory condition.

    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)


def set_all_entrance_rules(world: WormingFromHomeWorld) -> None:

    # Grab entrances
    overworld_to_shop_tier_1 = world.get_entrance("Overworld to Shop Tier 1")
    shop_tier_1_to_shop_tier_2 = world.get_entrance("Shop Tier 1 to Shop Tier 2")
    shop_tier_2_to_shop_tier_3 = world.get_entrance("Shop Tier 2 to Shop Tier 3")
    shop_tier_3_to_final_boss_room = world.get_entrance("Shop Tier 3 to Final Boss Room")

    # Set up entrance rules
    #   world.set_rule(overworld_to_top_left_room, lambda state: state.has("Key", world.player))

    # Player must have L-Desk to advance pass phase 1
    ready_for_printer = Has("L-Desk")
    world.set_rule(shop_tier_1_to_shop_tier_2, ready_for_printer)

    # End game opens up after signing contract
    ready_for_interview_prep = Has("Signed Soul Away")
    world.set_rule(shop_tier_2_to_shop_tier_3, ready_for_interview_prep)

    # Game can be finished after signing contract and having webcam, soundboard, and worm trampoline
    ready_for_interview = HasAll("Signed Soul Away", "Webcam", "Soundboard", "Worm Trampoline")
    world.set_rule(shop_tier_3_to_final_boss_room, ready_for_interview)


    # Rule Builder also allows the core AP code to do a lot of under-the-hood optimizations.
    # Rule Builder is quite comprehensive, and even if you have really esoteric rules,
    # you can make custom rules by subclassing CustomRule.

def set_all_location_rules(world: WormingFromHomeWorld) -> None:
    # Location rules work no differently from Entrance rules.
    # Most of our locations are chests that can simply be opened by walking up to them.
    # Thus, their logical requirements are covered by the Entrance rules of the Entrances that were required to
    # reach the region that the chest sits in.
    # However, our two enemies work differently.
    # Entering the room with the enemy is not enough, you also need to have enough combat items to be able to defeat it.
    # So, we need to set requirements on the Locations themselves.
    # Since combat is a bit more complicated, we'll use this chance to cover some advanced access rule concepts.

    # In "set_all_entrance_rules", we had a rule for a location that doesn't always exist.
    # In this case, we had to check for its existence (by checking the player's chosen options) before setting the rule.
    # Other times, you may have a situation where a location can have two different rules depending on the options.
    # In our case, the enemy in the right room has more health if hard mode is selected,
    # so ontop of the Sword, the player will either need one more health or a Shield in hard mode.
    # First, let's make our sword condition.
    can_sign_contract: Rule = HasAll("Printer", "Cup of Pens")

    sign_away_soul = world.get_location("Event: Sign Contract")
    world.set_rule(sign_away_soul, can_sign_contract)

    # In hard mode, the player also needs both Health Upgrades to survive long enough to defeat the boss.
    # For this, we can use the optional "count" parameter for "Has".
    has_interview_materials = HasAll("Webcam", "Soundboard", "Worm Trampoline")

    # Previously, we used an "if world.options.hard_mode" condition to check if we should apply the extra requirement.
    # However, if you're comfortable with boolean logic, there is another way.
    # OptionFilter is a rule component which isn't a "Rule" on its own, but when used in a boolean expression with
    # rules, it acts like True if the option has the specified value, and acts like False otherwise.
    hard_mode_is_off = OptionFilter(HardMode, False)

    can_successfully_interview = has_interview_materials
    
    # Promotion aquired win condition
    interview_succeeded = world.get_location("Event: Interview Succeeded")
    world.set_rule(interview_succeeded, can_successfully_interview)


def set_completion_condition(world: WormingFromHomeWorld) -> None:
    # Finally, we need to set a completion condition for our world, defining what the player needs to win the game.
    # For this, we can use world.set_completion_rule.
    # You can just set a completion condition directly like any other condition, referencing items the player receives:
    world.set_completion_rule(HasAll("Sword", "Shield"))

    # In our case, we went for the Victory event design pattern (see create_events() in locations.py).
    # So lets undo what we just did, and instead set the completion condition to:
    world.set_completion_rule(Has("Victory"))


# One final comment about rules:
# If your world exclusively uses Rule Builder rules (like WormingFromHome), it's worth trying CachedRuleBuilderWorld.
# CachedRuleBuilderWorld is a subclass of World that has a bunch of caching magic to make rules faster.
# Just have your world class subclass CachedRuleBuilderWorld instead of World:
#   class WormingFromHomeWorld(CachedRuleBuilderWorld): ...
# This may speed up your world, or it may make it slower.
# The exact factors are complex and not well understood, but there is no harm in trying it.
# Generate a few seeds and see if there is a noticeable difference!
# If you're wondering, author has checked: WormingFromHome is too simple to see any benefits, so we'll stick with "World".
