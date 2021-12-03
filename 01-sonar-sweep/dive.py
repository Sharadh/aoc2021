import click


def move_without_aim(x, y, _, direction, distance):
    if direction == "forward":
        x += distance
    elif direction == "down":
        y += distance
    elif direction == "up":
        y -= distance

    return x, y, _


def move_with_aim(x, y, aim, direction, distance):
    if direction == "forward":
        x += distance
        y += distance * aim
    elif direction == "down":
        aim += distance
    elif direction == "up":
        aim -= distance

    return x, y, aim


@click.command()
@click.argument("input_file", type=click.File())
@click.option("--use-aim/--no-use-aim", type=click.BOOL, default=False)
def main(input_file, use_aim):
    x, y, aim = 0, 0, 0

    for line in input_file:
        direction, distance = line.split()
        distance = int(distance)

        if use_aim:
            x, y, aim = move_with_aim(x, y, aim, direction, distance)
        else:
            x, y, aim = move_without_aim(x, y, aim, direction, distance)
        click.echo(f"{line} --> {x}, {y} (aim: {aim})")

    click.secho(f"{x}, {y} = {x * y}", fg="green")


if __name__ == "__main__":
    main()
