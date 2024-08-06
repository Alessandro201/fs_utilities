import os


def parse_args():
    import argparse

    parser = argparse.ArgumentParser(description="Remove empty directories recursively")

    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Write verbose output to STDERR"
    )
    parser.add_argument(
        "-d", "--dry-run", action="store_true", help="Do not delete any directory"
    )
    parser.add_argument(
        "DIRECTORIES",
        type=str,
        nargs="+",
        help="The directories to recursively search for empty directories",
    )

    args = parser.parse_args()
    return args


def remove_empty_dirs(path: str, verbose: bool = True, dry_run:bool = False):
    dirs_to_remove: set[str] = set()

    for root, dirs, files in os.walk(path, topdown=False):
        if files:
            continue

        if not dirs or all((os.path.join(root, dir) in dirs_to_remove for dir in dirs)):
            dirs_to_remove.add(root)

    for dir in reversed(list(dirs_to_remove)):
        if verbose:
            print(f"\t{dir}")
        
        if dry_run:
            continue

        os.system(f"rm -r {dir}")


def main():
    args = parse_args()

    inputs: list[str] = args.DIRECTORIES
    verbose: bool = args.verbose
    dry_run: bool = args.dry_run

    for path in inputs:
        if os.path.exists(path):
            if verbose:
                print(f"Finding empty directories in {path}")

            remove_empty_dirs(path, verbose=verbose, dry_run=dry_run)

            if verbose:
                print("\n")


if __name__ == "__main__":
    main()
