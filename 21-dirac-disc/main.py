import typing
from collections import Counter
from dataclasses import dataclass, replace

import click


class Parts:
    PART_ONE = "part-one"
    PART_TWO = "part-two"


def training_round(p1, p2):
    state = {"p1": (p1, 0, "p2"), "p2": (p2, 0, "p1")}
    i, next_player, die = 0, "p1", 0
    while True:
        # Roll the die.
        i, player = i + 3, next_player

        die_total = 0
        for _ in range(3):
            die = roll(die)
            die_total += die

        pos, score, next_player = state[player]
        pos = (pos + die_total) % 10
        if pos == 0:
            pos = 10
        score += pos
        # Store.
        state[player] = pos, score, next_player
        # click.confirm(f"Round {i}: {die_total} --> {state[player]}")

        # Next turn, or done?
        if score >= 1000:
            break

    click.echo(f"Winner: {player} after {i} rounds with final state {state}")
    click.echo(f"Answer: {state[next_player][1] * i}")


def get_dirac_outcomes():
    """Returns a dictionary of possible 3-die totals and times
    that can happen."""
    c = Counter()
    for i in range(1, 4):
        for j in range(1, 4):
            for k in range(1, 4):
                c[i + j + k] += 1
    return c


@dataclass(frozen=True)
class DiracState:
    p1_pos: int
    p1_score: int
    p2_pos: int
    p2_score: int

    def position(self, player):
        return getattr(self, f"{player}_pos")

    def score(self, player):
        return getattr(self, f"{player}_score")

    def copy_with(self, player, pos, score):
        return replace(self, **{f"{player}_pos": pos, f"{player}_score": score})


def next_player(player):
    return "p1" if player == "p2" else "p2"


def dirac_round(p1, p2):
    # This indicates the number of universes that result with various 3-throw die-totals.
    outcomes = get_dirac_outcomes()
    click.confirm(f"{outcomes} (total of {sum(outcomes.values())})")

    states: typing.Counter[DiracState] = Counter()
    states[DiracState(p1, 0, p2, 0)] += 1

    i, player = 0, "p2"
    wins = {
        "p1": 0, "p2": 0
    }
    # While there are active states of the game, continue playing.
    while states:
        # Roll the die.
        player = next_player(player)

        # Take every possible outcome on top of every possible position
        # calculated thus far; that gives us the new state of the multiverse.
        new_states = Counter()
        for state, count in states.items():
            pos = state.position(player)
            score = state.score(player)
            for die_total, freq in outcomes.items():
                new_pos = (pos + die_total) % 10
                if new_pos == 0:
                    new_pos = 10
                new_score = score + new_pos
                new_count = count * freq
                # click.confirm(f"{pos},{score} ({count} times) + {die_total} ({freq} times) -> {new_pos},{new_score} ({new_count} times)")
                if new_score >= 21:
                    # Count the win, but end the game (don't carry forward)
                    wins[player] += new_count
                else:
                    new_state = state.copy_with(player, new_pos, new_score)
                    new_states[new_state] += new_count

        click.confirm(f"{player} after {i} throws: {len(states)} --> {len(new_states)}")
        states = new_states

    click.echo(f"Wins: {wins} (simulated up to {i} throws)")
    winner = "p1" if wins["p1"] > wins["p2"] else "p2"
    click.echo(f"{winner} wins more, in {wins[winner]} universes!")
    # click.echo(f"Answer: {state[next_player][1] * i}")


def roll(die):
    return die + 1 if die < 100 else 1


@click.command()
@click.argument("input_file", type=click.File())
@click.argument("part", type=click.Choice([Parts.PART_ONE, Parts.PART_TWO]))
def main(input_file, part):
    p1 = int(next(input_file).split(":")[1].strip())
    p2 = int(next(input_file).split(":")[1].strip())

    click.echo(f"Starting with {p1},{p2}")
    if part == Parts.PART_ONE:
        training_round(p1, p2)
    if part == Parts.PART_TWO:
        dirac_round(p1, p2)

    click.secho(f"Done!", fg="green")


if __name__ == "__main__":
    main()
