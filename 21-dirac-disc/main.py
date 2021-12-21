import typing
from collections import Counter

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


def dirac_round(p1, p2):
    state = {"p1": (Counter(), "p2"), "p2": (Counter(), "p1")}
    state["p1"][0][(p1, 0)] = 1
    state["p2"][0][(p2, 0)] = 1
    outcomes = get_dirac_outcomes()
    click.confirm(f"{outcomes}")
    i, next_player, die = 0, "p1", 0
    wins = {
        "p1": 0, "p2": 0
    }
    while True:
        # Roll the die.
        i, player = i + 3, next_player

        positions, next_player = state[player]
        # Take every possible outcome on top of every possible position
        # calculated thus far; that gives us the new state of the multiverse.
        new_positions = Counter()
        for (pos, score), count in positions.items():
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
                    new_positions[(new_pos, new_score)] += new_count

        # If there are no more possibilities to continue, end the game.
        if not new_positions:
            wins[next_player] += sum(state[next_player][0].values())
            break

        # Store.
        state[player] = new_positions, next_player
        click.confirm(f"{player} after {i} throws: {positions} --> {state[player][0]}")

    click.echo(f"Wins: {wins} (simulated up to {i} throws)")
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
