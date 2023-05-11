import os
from typing import Callable
from urllib.parse import urljoin, urlparse


def base_url_of(url: str) -> str:
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"


def to_segment_url_map(base_url: str) -> Callable[[str], str]:
    return lambda segment: to_segment_url(base_url, segment)


def to_segment_url(base_url: str, file_name: str) -> str:
    return urljoin(base_url, file_name)


def get_file_name(url: str) -> str:
    parsed_url = urlparse(url)
    return os.path.basename(parsed_url.path)


def pure_domain(url: str) -> str:
    parsed_url = urlparse(url)
    domain_parts = parsed_url.netloc.split(".")
    return ".".join(domain_parts[-2:])


def is_cloudflare(url: str) -> bool:
    return pure_domain(url) == "cf-ipfs.com"

def extract_subdomain(url: str) -> str:
    parsed_url = urlparse(url)
    domain_parts = parsed_url.netloc.split('.')

    if len(domain_parts) < 3:
        # 서브 도메인이 없는 경우 빈 문자열 반환
        return ""

    # 첫 번째 요소를 서브 도메인으로 반환
    return domain_parts[0]