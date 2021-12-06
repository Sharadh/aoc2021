import click

from collections import Counter


@click.command()
@click.argument("input_file", type=click.File())
@click.argument("target_days", type=click.INT)
def main(input_file, target_days):
    timers = [int(t) for t in input_file.readline().strip().split(",")]
    counts = Counter(timers)

    click.echo("Start simulation...")
    # For timer = 1
    # 1 : 1
    # 2 : 0
    # 3 : 6 8 (2)
    # 4 : 5 7 (2)
    # 5 : 4 6 (2)
    # 6 : 3 5 (2)
    # 7 : 2 4 (2)
    # 8 : 1 3 (2)
    # 9 : 0 2 (2)
    # 10: 6 1 8 (3)
    # 11: 5 0 7 (3)
    # 12: 4 6 6 8 (4)
    # 13: 3 5 5 7 (4)
    # 14: 2 4 6 (3)
    # 15: 1 3 5 (3)
    # 16: 0 2 4 (3)
    # 17: 6 1 3 8 (4)
    # 18: 5 0 2 7 (4)
    # 19: 4 6 1 6 8 (5)
    # 20: 3 5 0 5 7 (5)
    # 21: 2 4 6 4 6 8 (6)
    result = {x: {} for x in range(1, 9)}
    for day in range(target_days + 1):
        for timer in range(1, 9):
            if timer >= day:
                result[timer][day] = 1
            else:
                prev = max(day - timer - 1, 0)
                result[timer][day] = result[6][prev] + result[8][prev]
        click.echo(f"Day {day}: {str([result[t][day] for t in range(1, 9)])}")
        # click.prompt("")

    click.echo(f"Input has following numbers of various timers: {counts}")
    click.prompt("continue?")

    sum_ = 0
    for timer, count in counts.items():
        contribution = result[timer][target_days] * count
        click.echo(f"f{timer} x {count} => {contribution}")
        sum_ += contribution

    click.secho(str(sum_), fg="green")


if __name__ == "__main__":
    main()
