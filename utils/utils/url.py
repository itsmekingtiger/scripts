import os
from typing import Callable, Tuple
from urllib.parse import urljoin, urlparse


def base_url_of(url: str) -> str:
    """
    주어진 URL의 기본 URL을 반환하는 함수입니다.

    Args:
        url (str): 기본 URL을 추출할 URL 문자열입니다.

    Returns:
        str: 추출된 기본 URL입니다.

    Example:
        >>> base_url_of("https://www.example.com/path")
        "https://www.example.com"

        >>> base_url_of("http://sub.example.com/page")
        "http://sub.example.com"
    """

    # URL을 파싱합니다.
    parsed_url = urlparse(url)

    # 기본 URL을 구성하여 반환합니다.
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return base_url


def to_segment_url_map(base_url: str) -> Callable[[str], str]:
    return lambda segment: urljoin(base_url, segment)


def extract_path_and_filename(url: str) -> Tuple[str, str]:
    """
    주어진 URL에서 경로와 파일 이름을 추출하는 함수입니다.

    Args:
        url (str): 추출할 경로와 파일 이름을 포함하는 URL 문자열입니다.

    Returns:
        Tuple[str, str]: 추출된 경로와 파일 이름으로 이루어진 튜플입니다.

    Example:
        >>> extract_path_and_filename("https://my-site.com/2023/05/11/test_url.py")
        ("https://my-site.com/2023/05/11/", "test_url.py")

        >>> extract_path_and_filename("https://my-site.com/2023/05/11/")
        ("https://my-site.com/2023/05/11/", "")

        >>> extract_path_and_filename("https://subdomain.my-site.com/test_url.py")
        ("https://subdomain.my-site.com/", "test_url.py")

        >>> extract_path_and_filename("https://subdomain.my-site.com/")
        ("https://subdomain.my-site.com/", "")

        >>> extract_path_and_filename("/my/path/file.txt")
        ("/my/path", "file.txt")

        >>> extract_path_and_filename("/my/path/")
        ("/my/path", "")
    """

    # URL을 파싱합니다.
    parsed_url = urlparse(url)

    # 파일 이름을 추출합니다.
    filename = os.path.basename(parsed_url.path)

    return (url.replace(filename, ""), filename)


def pure_domain(url: str) -> str:
    parsed_url = urlparse(url)
    domain_parts = parsed_url.netloc.split(".")
    return ".".join(domain_parts[-2:])


def is_cloudflare(url: str) -> bool:
    return pure_domain(url) == "cf-ipfs.com"


def extract_subdomain(url: str) -> str:
    """
    주어진 URL에서 서브 도메인을 추출하는 함수입니다.

    Args:
        url (str): 서브 도메인을 추출할 URL 문자열입니다.

    Returns:
        str: 추출된 서브 도메인입니다. 서브 도메인이 없는 경우 빈 문자열을 반환합니다.

    Example:
        >>> extract_subdomain("https://sub.example.com/path")
        "sub"

        >>> extract_subdomain("https://example.com/path")
        ""
    """

    # URL을 파싱합니다.
    parsed_url = urlparse(url)

    # 도메인 부분을 점(.)으로 분리합니다.
    domain_parts = parsed_url.netloc.split(".")

    # 서브 도메인이 없는 경우 빈 문자열을 반환합니다.
    if len(domain_parts) < 3:
        return ""

    # 첫 번째 요소를 서브 도메인으로 반환합니다.
    return domain_parts[0]
