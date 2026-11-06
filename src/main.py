import argparse
from music_playlist.app import MusicPlaylistApp

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Play categorized music with hotkeys.")
    parser.add_argument(
        "-obs",
        "--obs-text",
        "--obs_text",
        action="store_true",
        help="display the currently played song in OBS",
    )
    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()
    MusicPlaylistApp(show_obs_text=arguments.obs_text).run()


if __name__ == "__main__":
    main()