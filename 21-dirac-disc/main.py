import typing

import click


class Parts:
    PART_ONE = "part-one"
    PART_TWO = "part-two"


def roll(die):
    return die + 1 if die < 100 else 1


@click.command()
@click.argument("input_file", type=click.File())
@click.argument("part", type=click.Choice([Parts.PART_ONE, Parts.PART_TWO]))
def main(input_file, part):
    p1 = int(next(input_file).split(":")[1].strip())
    p2 = int(next(input_file).split(":")[1].strip())

    click.echo(f"Starting with {p1},{p2}")
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
    click.secho(f"Done!", fg="green")


if __name__ == "__main__":
    main()
