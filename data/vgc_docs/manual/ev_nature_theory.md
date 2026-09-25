# EV Spreads and Natures

Effort Values (EVs) and Nature decide a Pokémon's final stats and therefore every
damage and speed calc. A Pokémon has 510 EVs to distribute, capped at 252 per
stat, and its Nature raises one stat by 10% while lowering another. When you do
not know an opponent's exact spread, assume the most common spread from usage
stats — but understand what each archetype implies.

Offensive spreads (e.g. 252 in the main attacking stat and 252 Speed with a
boosting Nature like Jolly or Timid) maximize damage and speed at the cost of
bulk. These Pokémon hit hard and move first but fall to neutral hits. Against an
offensive spread, you can often revenge-kill after it takes a single hit.

Bulky-offensive spreads invest enough Speed to outrun a key target, then dump the
rest into HP and a defense. They trade some power for the ability to survive a hit
and strike back. Trick Room spreads do the opposite: 0 Speed IVs and a
Speed-lowering Nature (Brave, Quiet, Relaxed, Sassy) so the Pokémon moves first
under Trick Room while maximizing bulk and power.

Defensive and support spreads load HP and both defenses, often with a Bold or
Calm Nature, to maximize how many hits the Pokémon eats. These spreads are common
on redirectors, Trick Room setters, and Intimidate pivots.

The practical takeaway for live play: the default assumed spread drives your calc,
but the moment you observe real damage (a move that did a specific percentage),
that observation overrides the assumption. A hit that did less than expected means
more bulk than assumed; a hit that did more means an offensive investment. Feed
every observed damage number back into your model.
