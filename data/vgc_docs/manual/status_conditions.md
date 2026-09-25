# Status Conditions and How They Swing Games

Status conditions are persistent advantages that change the math for the rest of
the game. Recognizing how each one affects damage and speed is essential to
correct play.

Burn halves a physical attacker's damage output and chips 1/16 HP per turn. Burning
the opponent's physical win condition can neutralize it without a KO — a burned
Mega attacker may no longer threaten the KOs it was built for. Update every
physical damage calc for a burned attacker by halving it.

Paralysis halves Speed and gives a 25% chance the Pokémon cannot move that turn.
Spreading paralysis is partial speed control that does not expire: a paralyzed
sweeper may now be outsped by your whole team, flipping the speed tiers. Re-run
speed calcs the moment paralysis lands.

Sleep removes a Pokémon from the game for one to three turns and is among the most
powerful disruption tools (Spore is 100% accurate sleep). A slept Pokémon cannot
attack, redirect, or set up. Sleep Talk and certain abilities are the only ways
out. Putting the opposing redirector or setup sweeper to sleep can win the turn
outright.

Poison and badly-poisoned (toxic) deal increasing chip damage and pressure bulky,
passive Pokémon. They rarely change a single turn but win long games against stall.
Freeze is rare but game-ending while it lasts.

Safeguard and Misty Terrain protect a side from status; track `safeguard_turns`
and terrain when deciding whether a status move will land. When the opponent is
protected from status, hold your Spore or Thunder Wave for a turn when it can
actually connect.
