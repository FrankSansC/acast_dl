#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "feedparser",
#     "mutagen",
#     "tqdm"
# ]
# ///

import os
import re
import feedparser
import urllib.request
from datetime import datetime
from tqdm import tqdm
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, COMM, TIT2, TPE1, TALB, TDRC, ID3NoHeaderError


class PodcastDownloader:
    def __init__(self, rss_url, output_dir="podcasts", max_episodes=None):
        self.rss_url = rss_url
        self.output_dir = output_dir
        self.max_episodes = max_episodes

    def sanitize_filename(self, name):
        return re.sub(r'[\\/*?:"<>|]', "", name)

    def set_metadata(self, mp3_path, metadata, image_url=None):
        print(f"Tagging: {mp3_path}")

        try:
            tags = ID3(mp3_path)
        except ID3NoHeaderError:
            tags = ID3()

        tags.add(TIT2(encoding=3, text=metadata.get("title", "")))
        tags.add(TPE1(encoding=3, text=metadata.get("author", "")))
        tags.add(TALB(encoding=3, text=metadata.get("album", "")))
        tags.add(TDRC(encoding=3, text=metadata.get("date", "")))

        if "description" in metadata:
            tags.add(COMM(encoding=3, lang='fra', desc='desc', text=metadata.get("description", "")))

        if image_url:
            try:
                image_data = urllib.request.urlopen(image_url).read()
                tags.add(APIC(
                    encoding=3,
                    mime='image/jpeg',  # or 'image/png'
                    type=3,  # cover (front)
                    desc='Cover',
                    data=image_data
                ))
            except Exception as e:
                print(f"Failed to download or embed image: {e}")

        tags.save(mp3_path)

    def get_audio_url(self, entry):
        for link in entry.links:
            if link.type == "audio/mpeg":
                return link.href
        return None

    def download_file(self, url, dest_path):
        print(f"Downloading: {url}")
        try:
            with urllib.request.urlopen(url) as response:
                total_size = int(response.getheader('Content-Length', 0))
                block_size = 8192
                with open(dest_path, 'wb') as out_file, tqdm(
                    total=total_size,
                    unit='B',
                    unit_scale=True,
                    unit_divisor=1024,
                    bar_format="{desc} |{bar}| {percentage:3.0f}% {n_fmt}/{total_fmt}",
                    initial=0
                ) as bar:
                    while True:
                        buffer = response.read(block_size)
                        if not buffer:
                            break
                        out_file.write(buffer)
                        bar.update(len(buffer))
        except Exception as e:
            print(f"Download failed: {e}")
            if os.path.exists(dest_path):
                os.remove(dest_path)

    def download(self):
        os.makedirs(self.output_dir, exist_ok=True)
        feed = feedparser.parse(self.rss_url)
        entries = feed.entries

        if self.max_episodes is not None:
            entries = entries[:self.max_episodes]

        os.makedirs(self.output_dir, exist_ok=True)

        for entry in entries:
            title = entry.title
            date = datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %Z')
            str_date = date.strftime('%Y%m%d')
            author = entry.get("author", feed.feed.get("author", ""))
            description = entry.get("summary", "")  # or "description"
            image_url = entry.get("image", {}).get("href", None)
            audio_url = self.get_audio_url(entry)

            if not audio_url:
                print(f"Skipping '{title}' (no MP3 link found)")
                continue

            filename = f"{self.sanitize_filename(date)} - {self.sanitize_filename(title)}.mp3"
            file_path = os.path.join(self.output_dir, filename)

            print(f"{filename}")

            if not os.path.exists(file_path):
                self.download_file(audio_url, file_path)

                metadata = {
                    "title": title,
                    "author": author,
                    "album": feed.feed.get("title", ""),
                    "date": date,
                }
                self.set_metadata(file_path, metadata)
            else:
                print(f"Already exists: {file_path}")


if __name__ == "__main__":
    rss_url = "https://feeds.acast.com/public/shows/encore-une-histoire"
    downloader = PodcastDownloader(rss_url, output_dir="podcasts", max_episodes=5)
    downloader.download()
