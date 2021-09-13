import importlib.metadata
import importlib.resources
import tarfile

__all__ = ["Pokedex"]
__version__ = importlib.metadata.version("pkmnhof")


class Pokedex:
    def __init__(self, gen=1):
        self.gen = gen
        self._tar = self._load_archive()
        self.frame = self._tar.extractfile("frame.png")

    def __getitem__(self, key):
        return self._tar.extractfile(f"{key:03d}.png")

    def _load_archive(self):
        m = {1: "rb"}

        pkg = importlib.resources.files("pkmnhof")
        archive = tarfile.open(pkg / "data" / f"{m[self.gen]}.tar.gz", mode="r:gz")

        return archive
