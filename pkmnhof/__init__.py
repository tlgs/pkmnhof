import argparse
import importlib.metadata
import importlib.resources
import tarfile

from PIL import Image, ImageShow

__version__ = importlib.metadata.version("pkmnhof")


class Pokedex:
    def __init__(self, gen):
        self.gen = gen
        self._tar = self._load_archive(gen)
        self.frame = self._tar.extractfile("frame.png")

    def __getitem__(self, key):
        return self._tar.extractfile(f"{key:03d}.png")

    def _load_archive(self, gen):
        m = {1: "rb"}

        pkg = importlib.resources.files("pkmnhof")
        archive = tarfile.open(pkg / "data" / f"{m[gen]}.tar.gz", mode="r:gz")

        return archive


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("numbers", nargs=6, type=int, metavar="N")
    parser.add_argument("-r", "--resize", default=1, type=float)
    parser.add_argument("-o", "--output")
    parser.add_argument(
        "--version", action="version", version=f"pkmnhof, version {__version__}"
    )
    args = parser.parse_args()

    if not all(0 < x < 152 for x in args.numbers):
        raise ValueError

    if args.resize is not None and not (1 <= args.resize <= 3):
        raise ValueError

    pokedex = Pokedex(1)

    pad = int(9 * args.resize)
    side = int(60 * args.resize)
    tmp = Image.new(mode="RGBA", size=(pad * 2 + side * 6, pad * 2 + side))
    for i, n in enumerate(args.numbers):
        tmp.paste(
            Image.open(pokedex[n]).resize((side, side)),
            box=(pad + side * i, pad),
        )

    background = (
        Image.open(pokedex.frame)
        .convert("RGBA")
        .resize((pad * 2 + side * 6, pad * 2 + side))
    )
    final = Image.alpha_composite(background, tmp)

    if args.output is not None:
        final.save(args.output)
    else:
        ImageShow.register(ImageShow.EogViewer, 0)  # prefer `eog` over `display`
        ImageShow.show(final)


if __name__ == "__main__":
    main()
