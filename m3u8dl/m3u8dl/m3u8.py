import re
from dataclasses import dataclass
from datetime import timedelta
from enum import Enum
from typing import Optional


class EncryptionMethod(Enum):
    """
    > The methods defined are: NONE, AES-128, and SAMPLE-AES.
    """

    NONE = "None"
    AES = "AES-128"
    SAMPLE = "SAMPLE-AES"


@dataclass
class ExtXKeyInfo:
    method: EncryptionMethod
    uri: str
    iv: str


def parse_ext_x_key_info(string: str) -> Optional[ExtXKeyInfo]:
    """
    주어진 문자열에서 '#EXT-X-KEY' 형식의 정보를 추출하여 데이터 클래스로 반환합니다.

    Args:
        string (str): '#EXT-X-KEY' 형식의 문자열.

    Returns:
        ExtXKeyInfo or None: 추출된 정보를 담은 ExtXKeyInfo 데이터 클래스 객체 또는 None.
    """

    pattern = r'#EXT-X-KEY:METHOD=(\w+),URI="([^"]+)",IV=([^\s,]+)'

    if match := re.match(pattern, string):
        method = match.group(1)
        uri = match.group(2)
        iv = match.group(3)

        return ExtXKeyInfo(method=EncryptionMethod(method), uri=uri, iv=iv)
    else:
        return None


def is_encrypted(file_path: str) -> bool:
    """
    주어진 파일에 암호화 정보가 있는지 확인하고, 파일이 암호화되었는지 여부를 반환합니다.

    Args:
        file_path (str): 암호화 정보를 확인할 파일 경로.

    Returns:
        bool: 파일이 암호화되었으면 True, 그렇지 않으면 False.
    """

    with open(file_path, "r") as file:
        lines = file.readlines()

    for line in lines:
        if line.startswith("#EXT-X-KEY"):
            if info := parse_ext_x_key_info(line):
                return info.method != EncryptionMethod.NONE

    return False


def extract_key_from_m3u8(file_path: str):
    """
    주어진 M3U8 파일에서 키 정보를 추출합니다.

    Args:
        file_path (str): 키 정보를 추출할 M3U8 파일의 경로.

    Returns:
        str or None: 추출된 키 정보의 URI 값 또는 None.
    """

    key_pattern = r'#EXT-X-KEY:METHOD=AES-128,URI="(.+?)",IV=0x\d+'

    with open(file_path, "r") as file:
        content = file.read()
        match = re.search(key_pattern, content)

        if match:
            return match.group(1)
        else:
            return None


def replace_key_in_m3u8(file_path: str, new_key: str):
    key_pattern = r'(#EXT-X-KEY:METHOD=AES-128,URI=")(.+?)(",IV=0x\d+)'

    with open(file_path, "r") as file:
        content = file.read()

    content = re.sub(key_pattern, rf"\1{new_key}\3", content)

    with open(file_path, "w") as file:
        file.write(content)


def extract_playtime(file_path: str) -> timedelta:
    """
    주어진 파일에서 재생 시간 정보를 추출하여 총 재생 시간을 timedelta 형식으로 반환합니다.

    Args:
        file_path (str): 재생 시간 정보를 추출할 파일의 경로.

    Returns:
        timedelta: 총 재생 시간을 표현하는 timedelta 객체.
    """

    total_duration = 0

    with open(file_path, "r") as file:
        lines = file.readlines()

    for line in lines:
        if line.startswith("#EXTINF:"):
            # 재생 시간 정보를 추출하고 float로 변환하여 총 재생 시간에 더함
            duration = float(line.split(":")[1].split(",")[0])
            total_duration += duration

    return timedelta(seconds=int(total_duration))
