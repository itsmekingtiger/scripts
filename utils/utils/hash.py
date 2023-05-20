import hashlib
from typing import Final

_BLOCK_SIZE: Final = 4096


def calculate_sha256(file_path: str) -> bytes:
    """
    주어진 파일 경로의 파일을 읽어 SHA-256 해시 값을 계산합니다.

    Args:
        file_path (str): 해시 값을 계산할 파일 경로.

    Returns:
        bytes: 계산된 SHA-256 해시 값을 bytes로 반환합니다.

    """
    sha256_hash = hashlib.sha256()

    with open(file_path, "rb") as file:
        # 파일을 작은 청크로 나누어 해시 계산
        for chunk in iter(lambda: file.read(_BLOCK_SIZE), b""):
            sha256_hash.update(chunk)

    # 해시 값을 bytes로 반환
    return sha256_hash.digest()


def calculate_md5(file_path: str) -> bytes:
    """
    주어진 파일 경로의 파일을 읽어 MD5 해시 값을 계산합니다.

    Args:
        file_path (str): 해시 값을 계산할 파일 경로.

    Returns:
        bytes: 계산된 MD5 해시 값을 bytes로 반환합니다.

    """
    md5_hash = hashlib.md5()

    with open(file_path, "rb") as file:
        # 파일을 작은 청크로 나누어 해시 계산
        for chunk in iter(lambda: file.read(_BLOCK_SIZE), b""):
            md5_hash.update(chunk)

    # 해시 값을 bytes로 반환
    return md5_hash.digest()
