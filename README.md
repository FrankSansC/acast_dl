# acast_dl.py

The purpose of this script is to easily download podcast files from Acast for offline listening.

## Limitations

- this script is currently a wip and has been tested with only a very little set of podcast feeds
- this script only support `.mp3` files

## AI usage

Please note that part of this script has been written using [OpenAI](https://openai.com/) [ChatGPT](https://chatgpt.com/) (GPT-4o + GPT-5) as a teammate.

This project is an excuse to see how good AI is at helping to write small tools (I always have lots of ideas but don't have time to implement them).

# Dependencies

`acast_dl` relies on three dependencies :
- [`feedparser`](https://github.com/kurtmckee/feedparser) : for retrieving and parsing the RSS XML feed
- [`mutagen`](https://github.com/quodlibet/mutagen) : for updating ID3 MP3 tags
- [`tqdm`](https://github.com/tqdm/tqdm) : to show a progress bar when downloading the files

You can either install them with your favorite package manager or install [`uv`](https://docs.astral.sh/uv/) and launch `acast_dl.py` right away.

It makes use of [PEP-723](https://peps.python.org/pep-0723/) that allows to add metadata :

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "feedparser",
#     "mutagen",
#     "tqdm"
# ]
# ///
```

When launched the first time you'll see `uv` downloading and installing the dependencies :

```
TODO
```

I got the inspiration to use `uv` thanks to this blog post : [Fun with uv and PEP 723](https://www.cottongeeks.com/articles/2025-06-24-fun-with-uv-and-pep-723) (related [hn post](https://news.ycombinator.com/item?id=44369388)).

# Usage

```shell
TODO
```

# TODO

- [ ] Update this `README.md` file
- [ ] add arguments
  - [ ] `--override` : override any existing podcast file
  - [ ] `--no-tag` : don't update MP3 ID3 tags
  - [ ] `--ignore-rss-cache` : ignore ETag
  - [ ] `--rss-cache-file` : to override `.rss_cache.json` (not sure about the usefulness of this one)
  - [ ] `--max-download` : download only the latest / most recent X podcast episodes

# Similar projects

Here's a non-exhaustive list, in non-specific order, of similar projects to `acast_dl` :

- [acast-rss-downloader](https://github.com/duskmoon314/acast-rss-downloader)
- [gocast](https://github.com/philippdrebes/gocast)

# Legal Notice

This project is an independent tool and is **not affiliated with, endorsed by, or connected to Acast** in any way.
Acast is a registered trademark of its respective owner. All other trademarks and service marks are the property of their respective owners.

All podcasts, audio files, images, descriptions, and related metadata retrieved using this tool remain the sole property of their respective creators and copyright holders. This tool is intended for personal, non-commercial use only.

You are responsible for ensuring that your use of any downloaded content complies with applicable copyright laws and the terms of service of the source platform.

# License

The source code of this project is released under the [MIT License](./LICENSE).

This license applies **only** to the project’s code and does **not** extend to any media downloaded or processed with this tool.
