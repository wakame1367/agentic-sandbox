"""Tiny runnable app so the `verify` job has something real to execute."""

from calc import add, divide


def main() -> int:
    print(f"2 + 3 = {add(2, 3)}")
    print(f"10 / 4 = {divide(10, 4)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
