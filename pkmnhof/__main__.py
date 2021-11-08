import re

import click
from PIL import Image, ImageShow

from pkmnhof import Pokedex, __version__


def validate_nums(ctx, param, value):
    r"""Validate the NUMS argument - accepted values are any positive integer or '_'.

    The pattern ^d*[1-9]\d*$ exclusively matches positive integers.
    """
    for x in value:
        if re.fullmatch(r"^(\d*[1-9]\d*|_)$", x) is None:
            raise click.BadParameter(f"'{x}' should be a positive integer or '_'.")

    return value


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option(
    "-o",
    "--output",
    type=click.Path(dir_okay=False),
    help="Save image to a file instead of displaying it.",
)
@click.option(
    "-r",
    "--resize",
    type=click.FloatRange(1, 3),
    default=1,
    help="Resize original image (mainting its aspect ratio).",
)
@click.option("--no-frame", is_flag=True, help="Create image without a frame.")
@click.version_option(version=__version__)
@click.argument("nums", nargs=6, callback=validate_nums)
def main(output, resize, no_frame, nums):
    """Display an image containing a Pokémon team.

    NUMS represent each Pokémon's National Pokédex number.
    Optionally use '_' for an empty slot.
    """
    pokedex = Pokedex()

    pad = int(9 * resize)
    side = int(60 * resize)
    tmp = Image.new(mode="RGBA", size=(pad * 2 + side * 6, pad * 2 + side))
    for i, n in enumerate(nums):
        if n == "_":
            continue

        tmp.paste(
            im=Image.open(pokedex[int(n)]).resize((side, side)),
            box=(pad + side * i, pad),
        )

    if no_frame:
        background = Image.new(
            mode="RGBA",
            size=(pad * 2 + side * 6, pad * 2 + side),
            color="#ffffff",
        )
    else:
        background = (
            Image.open(pokedex.frame)
            .convert("RGBA")
            .resize((pad * 2 + side * 6, pad * 2 + side))
        )

    final = Image.alpha_composite(background, tmp)

    if output is not None:
        final.save(output)
    else:
        ImageShow.register(ImageShow.EogViewer, 0)  # prefer `eog` over `display`
        ImageShow.show(final)


if __name__ == "__main__":
    main()
