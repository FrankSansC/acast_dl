import os
import re
import feedparser
import urllib.request
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3

class PodcastDownloader:
    def __init__(self, rss_url, output_dir="podcasts", max_episodes=None):
        self.rss_url = rss_url
        self.output_dir = output_dir
        self.max_episodes = max_episodes

    def sanitize_filename(self, name):
        return re.sub(r'[\\/*?:"<>|]', "", name)

    def download_file(self, url, dest_path):
        print(f"Downloading: {url}")
        urllib.request.urlretrieve(url, dest_path)

    def set_metadata(self, mp3_path, metadata):
        print(f"Tagging: {mp3_path}")
        audio = MP3(mp3_path, ID3=EasyID3)
        audio["title"] = metadata.get("title", "")
        audio["artist"] = metadata.get("author", "")
        audio["album"] = metadata.get("album", "")
        audio["date"] = metadata.get("date", "")
        audio.save()

    def get_audio_url(self, entry):
        for link in entry.links:
            if link.type == "audio/mpeg":
                return link.href
        return None

    def download(self):
        os.makedirs(self.output_dir, exist_ok=True)
        feed = feedparser.parse(self.rss_url)
        entries = feed.entries

        if self.max_episodes is not None:
            entries = entries[:self.max_episodes]

        for entry in entries:
            title = entry.title
            date = entry.get("published", "")[:10]
            author = entry.get("author", feed.feed.get("author", ""))
            audio_url = self.get_audio_url(entry)

            if not audio_url:
                print(f"Skipping '{title}' (no MP3 link found)")
                continue

            filename = f"{self.sanitize_filename(date)} - {self.sanitize_filename(title)}.mp3"
            file_path = os.path.join(self.output_dir, filename)

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
