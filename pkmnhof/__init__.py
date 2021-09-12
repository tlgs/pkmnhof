import argparse
import importlib.resources
import tarfile

from PIL import Image, ImageShow


class Pokedex:
    def __init__(self, gen):
        self.gen = gen
        self.tar = self._load_archive(gen)

    def __getitem__(self, key):
        return self.tar.extractfile(f"{key:03d}.png")

    def _load_archive(self, gen):
        m = {1: "rb"}

        pkg = importlib.resources.files("pkmnhof")
        archive = tarfile.open(pkg / "data" / f"{m[gen]}.tar.gz", mode="r:gz")

        return archive


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("numbers", nargs=6, type=int, metavar="N")
    parser.add_argument("-r", "--resize", type=float)
    parser.add_argument("-c", "--columns", default=6, type=int, choices=[6, 3, 2, 1])
    args = parser.parse_args()

    if not all(0 < x < 152 for x in args.numbers):
        raise ValueError

    if args.resize is not None and not (1 <= args.resize <= 3):
        raise ValueError

    # default size should probably not be hardcoded
    side = 60 if args.resize is None else int(60 * args.resize)

    pokedex = Pokedex(1)

    images = [Image.open(pokedex[n]).resize(size=(side, side)) for n in args.numbers]

    tmp = Image.new(mode="RGBA", size=(side * args.columns, side * (6 // args.columns)))
    for i in range(6):
        x = i % args.columns
        y = i // args.columns
        tmp.paste(images[i], (side * x, side * y))

    final = Image.new(
        mode="RGBA",
        size=(side * args.columns, side * (6 // args.columns)),
        color="#ffffff",
    )
    final.alpha_composite(tmp)

    ImageShow.register(ImageShow.EogViewer, 0)  # prefer `eog` over `display`
    ImageShow.show(final)


if __name__ == "__main__":
    main()
