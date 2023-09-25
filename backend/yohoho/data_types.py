from dataclasses import dataclass


@dataclass
class SearchOutput:
    kinopoisk_id: int
    title: str


@dataclass
class IframesOutput:
    source_name: str
    iframe_url: str
    quality: str | None = None
