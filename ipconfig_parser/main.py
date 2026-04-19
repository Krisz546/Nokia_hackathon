from pathlib import Path


def main():
    for path in sorted(Path(".").glob("*.txt")):
        print(path.name)


if __name__ == "__main__":
    main()
