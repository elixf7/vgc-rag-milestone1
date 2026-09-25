# Item Theory in Doubles

Held items are a hidden layer of information at team preview. Reading the likely
item on an opposing Pokémon changes every damage and speed calculation, so update
your assumptions the moment an item is revealed.

Choice items (Choice Band, Choice Specs, Choice Scarf) lock the holder into the
first move it selects but grant a 1.5x boost to Attack, Special Attack, or Speed
respectively. A Choice Scarf is the single most important item to read for speed
control: a Scarf Garchomp jumps from a normal Speed tier to outrunning nearly the
entire field. When you see a Choice user lock a move, you gain a free turn to
switch in a Pokémon that walls that move.

Assault Vest raises Special Defense by 50% but forbids status moves, marking the
holder as a bulky attacker rather than a support piece. Life Orb adds 30% damage
at the cost of recoil and is the hallmark of an all-out attacker. Focus Sash
guarantees survival of one hit from full HP, a common pick on frail fast Pokémon
and on Trick Room setters that need to live a turn.

Berries change the calc mid-game. Sitrus Berry restores 25% HP when the holder
drops below half, so a Pokémon that looked like a guaranteed two-hit KO may now
survive. Type-resist berries (e.g. a berry that halves a super-effective hit) can
turn a KO into a survivable chip. Once consumed, set `item_consumed` and re-run
the calc, because the bulk it provided is gone for the rest of the game.

Defensive items such as Rocky Helmet, Leftovers, and Eviolite shift the long game.
Track them: a Leftovers user slowly out-sustains chip damage, and Rocky Helmet
punishes contact moves. The correct play against an unknown item is to assume the
most common one from usage stats, then immediately correct once the real item
shows itself.
