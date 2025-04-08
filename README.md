# Supadata Python SDK

[![PyPI version](https://badge.fury.io/py/supadata.svg)](https://badge.fury.io/py/supadata)
[![MIT license](https://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat)](http://opensource.org/licenses/MIT)

The official Python SDK for Supadata.

Get your free API key at [supadata.ai](https://supadata.ai) and start scraping data in minutes.

## Installation

```bash
pip install supadata
```

## Usage

```python
from supadata import Supadata, SupadataError

# Initialize the client
supadata = Supadata(api_key="YOUR_API_KEY")

# Get YouTube transcript with Spanish language preference
transcript = supadata.youtube.transcript(video_id="dQw4w9WgXcQ", lang="es")
print(f"Got transcript {transcript.content}")

# Translate YouTube transcript to Spanish
translated = supadata.youtube.translate(
    video_id="dQw4w9WgXcQ",
    lang="es"
)
print(f"Got translated transcript in {translated.lang}")

# Get plain text transcript
text_transcript = supadata.youtube.transcript(
    video_id="dQw4w9WgXcQ",
    text=True
)
print(text_transcript.content)

# Scrape web content
web_content = supadata.web.scrape("https://supadata.ai")
print(f"Page title: {web_content.name}")
print(f"Page content: {web_content.content}")

# Map website URLs
site_map = supadata.web.map("https://supadata.ai")
print(f"Found {len(site_map.urls)} URLs")

# Start a crawl job
crawl_job = supadata.web.crawl(
    url="https://supadata.ai",
    limit=100  # Optional: limit the number of pages to crawl
)
print(f"Started crawl job: {crawl_job.job_id}")

# Get crawl results
# This automatically handles pagination and returns all pages
try:
    pages = supadata.web.get_crawl_results(job_id=crawl_job.job_id)
    for page in pages:
        print(f"Crawled page: {page.url}")
        print(f"Page title: {page.name}")
        print(f"Content: {page.content}")
except SupadataError as e:
    print(f"Crawl job failed: {e}")

# Get Video Metadata
video = supadata.youtube.video(id="https://youtu.be/dQw4w9WgXcQ") # can be url or video id
print(f"Video: {video}")

# Get Channel Metadata
channel = supadata.youtube.channel(id="https://youtube.com/@RickAstleyVEVO") # can be url, channel id, handle
print(f"Channel: {channel}")

# Get video IDs from a YouTube channel
channel_videos = supadata.youtube.channel.videos(
    id="RickAstleyVEVO",  # can be url, channel id, or handle
    type="all",  # 'all', 'video', or 'short'
    limit=50
)
print(f"Regular videos: {channel_videos.video_ids}")
print(f"Shorts: {channel_videos.short_ids}")

# Get Playlist metadata
playlist = supadata.youtube.playlist(id="PLlaN88a7y2_plecYoJxvRFTLHVbIVAOoc") # can be url or playlist id
print(f"Playlist: {playlist}")

# Get video IDs from a YouTube playlist
playlist_videos = supadata.youtube.playlist.videos(
    id="https://www.youtube.com/playlist?list=PLlaN88a7y2_plecYoJxvRFTLHVbIVAOoc",  # can be url or playlist id
    limit=50
)
print(f"Regular videos: {playlist_videos.video_ids}")
print(f"Shorts: {playlist_videos.short_ids}")

# --- Batch Operations ---

# Start a batch job to get transcripts for multiple videos
# You can provide video IDs, a playlist ID, or a channel ID
transcript_batch_job = supadata.youtube.transcript.batch(
    video_ids=["dQw4w9WgXcQ", "xvFZjo5PgG0"],
    # playlist_id="PLlaN88a7y2_plecYoJxvRFTLHVbIVAOoc", # alternatively
    # channel_id="UC_9-kyTW8ZkZNDHQJ6FgpwQ", # alternatively
    lang="en",  # Optional: specify preferred transcript language
    limit=100   # Optional: limit for playlist/channel
)
print(f"Started transcript batch job: {transcript_batch_job.job_id}")

# Start a batch job to get video metadata for a playlist
video_batch_job = supadata.youtube.video.batch(
    playlist_id="PLlaN88a7y2_plecYoJxvRFTLHVbIVAOoc",
    limit=50
)
print(f"Started video metadata batch job: {video_batch_job.job_id}")

# Get the results of a batch job (poll until status is 'completed' or 'failed')
import time

job_id = transcript_batch_job.job_id # or video_batch_job.job_id

while True:
    try:
        batch_results = supadata.youtube.batch.get_batch_results(job_id=job_id)
        print(f"Job {job_id} status: {batch_results.status}")

        if batch_results.status == "completed":
            print(f"Job completed at: {batch_results.completed_at}")
            print(f"Stats: Total={batch_results.stats.total}, Succeeded={batch_results.stats.succeeded}, Failed={batch_results.stats.failed}")
            for item in batch_results.results:
                if item.error_code:
                    print(f"  Video {item.video_id} failed with error: {item.error_code}")
                elif item.transcript:
                    print(f"  Video {item.video_id} transcript ({item.transcript.lang}): {len(item.transcript.content)} chunks/chars")
                elif item.video:
                     print(f"  Video {item.video_id} metadata: Title='{item.video.title}'")
            break
        elif batch_results.status == "failed":
            print(f"Job {job_id} failed.")
            # You might want to add more error details if available in a real scenario
            break
        elif batch_results.status in ["queued", "active"]:
            print("Waiting for job to complete...")
            time.sleep(5) # Poll every 5 seconds
        else:
            print(f"Unknown job status: {batch_results.status}")
            break
    except SupadataError as e:
        print(f"Error fetching batch results for job {job_id}: {e}")
        break

## Error Handling

The SDK uses custom `SupadataError` exceptions that provide structured error information:

```python
from supadata.errors import SupadataError

try:
    transcript = supadata.youtube.transcript(video_id="INVALID_ID")
except SupadataError as error:
    print(f"Error code: {error.error}")
    print(f"Error message: {error.message}")
    print(f"Error details: {error.details}")
    if error.documentation_url:
        print(f"Documentation: {error.documentation_url}")
```

## API Reference

See the [Documentation](https://supadata.ai/documentation) for more details on all possible parameters and options.

## License

MIT
