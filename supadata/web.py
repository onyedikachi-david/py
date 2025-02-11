"""Web-related operations for Supadata."""

from .types import Scrape, Map, CrawlJob, CrawlResponse, CrawlPage
from typing import Optional, List


class Web:
    """Web namespace for Supadata operations."""

    def __init__(self, request_handler):
        """Initialize Web namespace.
        
        Args:
            request_handler: Internal request handler from main client
        """
        self._request = request_handler

    def scrape(self, url: str) -> Scrape:
        """Scrape content from a web page.

        Args:
            url: URL to scrape

        Returns:
            Scrape object containing the extracted content

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        response = self._request("GET", "/web/scrape", params={"url": url})
        return Scrape(**response)

    def map(self, url: str) -> Map:
        """Generate a site map for a website.

        Args:
            url: Base URL to map

        Returns:
            Map object containing discovered URLs

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        response = self._request("GET", "/web/map", params={"url": url})
        return Map(**response)

    def crawl(self, url: str, limit: Optional[int] = None) -> CrawlJob:
        """Start a new crawl job.

        Args:
            url: URL to crawl
            limit: Optional maximum number of pages to crawl

        Returns:
            CrawlJob containing the job ID

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        data = {"url": url}
        if limit is not None:
            data["limit"] = limit # type: ignore
            
        response = self._request("POST", "/web/crawl", json=data)
        return CrawlJob(**response)

    def get_crawl_results(self, job_id: str) -> List[CrawlPage]:
        """Get the results of a crawl job.

        This method handles pagination automatically and returns all results.

        Args:
            job_id: ID of the crawl job

        Returns:
            List of CrawlPage objects containing the crawled content

        Raises:
            Exception: If the crawl job failed
            requests.exceptions.RequestException: If the API request fails
        """
        all_pages = []
        next_token = None

        while True:
            params = {}
            if next_token:
                params["next"] = next_token

            response = self._request("GET", f"/web/crawl/{job_id}", params=params)
            crawl_response = CrawlResponse(**response)

            # Check if the job failed
            if crawl_response.status == "failed":
                raise Exception("Crawl job failed")

            if crawl_response.pages:
                # Convert each page dict to a CrawlPage object
                page_objects = [CrawlPage(**page) for page in crawl_response.pages]
                all_pages.extend(page_objects)

            if not crawl_response.next:
                break
            next_token = crawl_response.next

        return all_pages 