from config import SUMMARY_PATH
from simulator import Simulator
from storage import FileStorage


def main():
    storage = FileStorage(SUMMARY_PATH)
    sim = Simulator(storage)
    sim.run_forever()


if __name__ == "__main__":
    main()