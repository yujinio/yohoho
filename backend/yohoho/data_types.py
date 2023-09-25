from dataclasses import dataclass


@dataclass
class SearchOutput:
    movie_id: str
    movie_title: str


@dataclass
class IframesOutput:
    source_name: str
    iframe_url: str
    quality: str | None = None
