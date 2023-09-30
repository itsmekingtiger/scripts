import logging
import os
import re
import shutil
import time
from typing import List
from urllib.parse import urljoin

from utils import fs, hash, url as liburl
import m3u8dl.ffmpeg as ffmpeg
import m3u8dl.m3u8 as m3u8

import requests

DELAY_PER_SEGMENTS_RETRY = 5
DELAY_PER_SEGMENTS = 5
DELAY_PER_M3U8 = 10

M3U8_FILENAME = "index.m3u8"
TS_FILENAME = "out.ts"
TMP_DIR = "_tmp"


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(module)s/%(filename)s:%(lineno)d\t%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

log = logging.getLogger()
log.setLevel(logging.INFO)


def main():
    if not ffmpeg.is_ffmpeg_installed():
        raise Exception("ffmpeg가 설치되어 있지 않습니다")

    # If nessesary, add http header it sould be read from env or config file.
    header: dict[str, str] = {}

    fs.mkdir_if_not_exist(TMP_DIR)

    m3u8_list = open("m3u8_list.txt", "r").read()
    m3u8_urls = re.split(r"\r?\n", m3u8_list)
    for url in m3u8_urls:
        # skip comment line
        if url.startswith("#"):
            log.info(f"skipping comment: {url}")
            continue

        try:
            log.info(f"downloading {url}")

            # if not liburl.is_cloudflare(url):
            #     log.warning(f"{url} is not hosted on CloudFlare")
            #     continue

            download_from_m3u8(url, header)
        finally:
            time.sleep(DELAY_PER_M3U8)
            fs.clear_dir(TMP_DIR)


def download_from_m3u8(url: str, header: "dict[str, str]"):
    base_url, _ = liburl.extract_path_and_filename(url)

    try:
        # m3u8 다운로드
        m3u8_content = download(url, header)
        if not m3u8_content:
            raise Exception(f"Failed to download file: {url}.")

        m3u8_path = os.path.join(TMP_DIR, M3U8_FILENAME)

        fs.save(m3u8_path, m3u8_content)

        key_filename = m3u8.extract_key_from_m3u8(m3u8_path)
        if not isinstance(key_filename, str):
            raise Exception(f"{key_filename}는 문자열이 아닙니다.")

        key_filename = key_filename.lstrip("/")  # 절대 경로를 상대 경로로 수정

        m3u8.replace_key_in_m3u8(m3u8_path, key_filename)

        # key 다운로드
        key_url = urljoin(base_url, key_filename)
        key_path = os.path.join(TMP_DIR, key_filename)

        key_content = download(key_url, header)

        fs.save(key_path, key_content)

        # 세그먼트 다운로드
        segments = extract_segments(m3u8_content.decode())

        uid = liburl.extract_subdomain(base_url)
        playtime = m3u8.extract_playtime(m3u8_path)

        log.info(
            f"""
            정보일람: {uid}
            \t세그먼트: {len(segments)}
            \t재생 시간: {playtime}
            """
        )

        for i, segment in enumerate(segments):
            seg_url = urljoin(base_url, segment)
            seg_path = os.path.join(TMP_DIR, segment)
            seg_data = download(seg_url, headers=header)
            fs.save(seg_path, seg_data)

            seg_size_in_mb = len(seg_data) / 1024 / 1024
            log.info(f"다운로드 완료({i + 1}/{len(segments)}), {seg_size_in_mb:.3} MB")
            time.sleep(DELAY_PER_SEGMENTS)

        # ffmpeg
        # ffmpeg -allowed_extensions 'ALL' -protocol_whitelist 'crypto,file' -i index.m3u8 -c copy out.ts

        ffmpeg_command = [
            "ffmpeg",
            "-allowed_extensions",
            "ALL",
            "-protocol_whitelist",
            "crypto,file",
            "-i",
            M3U8_FILENAME,
            "-c",
            "copy",
            TS_FILENAME,
        ]

        proc = ffmpeg.run_command(ffmpeg_command, TMP_DIR)

        if proc.returncode != 0:
            print("Error:", proc.stderr)
        else:
            print("FFmpeg command executed successfully.")

    except Exception as e:
        log.error(f"something wrong: {e}")

    m3u8_path = os.path.join(TMP_DIR, TS_FILENAME)
    new_filename = f"{hash.calculate_sha256(m3u8_path).hex()}.ts"

    log.info(f"download complete {url} → {new_filename}")

    if os.path.exists(m3u8_path):
        shutil.move(m3u8_path, new_filename)


def extract_segments(content: str) -> List[str]:
    lines = re.split(r"\r?\n", content)
    return list(filter(containsSegmentNo, lines))


def containsSegmentNo(s: str) -> bool:
    return "segmentNo" in s


def download(url: str, headers: "dict[str, str]") -> bytes:
    resp = requests.get(url, headers=headers)
    if not resp.ok:
        raise Exception(f'다운로드 실패 "{url}": {resp.content.decode()}')
    return resp.content


if __name__ == "__main__":
    main()
