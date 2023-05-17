import logging
import os
import shutil
import time
from typing import Callable, Dict, Final, List, Tuple, TypedDict
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from utils import fs

TEMPORAL_BASE_PATH: Final = os.path.join(os.getcwd(), "tmp")
DOWNLOAD_BASE_PATH: Final = os.path.join(os.getcwd(), "downloads")

LIMIT: Final = 200


# https://stackoverflow.com/questions/7406102
def to_path_safe_string(s: str) -> str:
    """
    문자열을 파일 이름으로 쓰기 안전한 문자열로 변환
    """
    keepcharacters = (" ", ".", "_")
    return "".join(c for c in s if c.isalnum() or c in keepcharacters).rstrip()


def load_list_of_urls(url_list_file: str) -> List[str]:
    return open(url_list_file).readlines()


class Option(TypedDict):
    use_sequential_name: bool
    minimum_image_size: int


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(module)s/%(filename)s:%(lineno)d\t%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

log = logging.getLogger()
log.setLevel(logging.INFO)


class DogDripDownloader:
    def __init__(self) -> None:
        # Chrome 옵션 설정
        driver_options = Options()
        driver_options.add_argument("--disable-gpu")
        driver_options.add_experimental_option(
            "prefs",
            {
                "download.default_directory": TEMPORAL_BASE_PATH,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "plugins.always_open_pdf_externally": True,
                "safebrowsing.enabled": False,
                "safebrowsing.disable_download_protection": True,
            },
        )

        # Chrome 드라이버 설정 및 실행
        driver = webdriver.Chrome(options=driver_options)
        driver.command_executor._commands["send_command"] = (
            "POST",
            "/session/$sessionId/chromium/send_command",
        )

        # 다운로드 설정 적용
        params = {
            "cmd": "Page.setDownloadBehavior",
            "params": {"behavior": "allow", "downloadPath": TEMPORAL_BASE_PATH},
        }
        driver.execute("send_command", params)

        self.driver = driver

    def __del__(self):
        # 드라이버 종료
        self.driver.quit()

    def get_title(self) -> str:
        return to_path_safe_string(self.driver.title.rstrip("DogDrip.Net 개드립")).replace(
            ".", ""
        )

    def download(self, url: str):
        log.info(f"download page: {url}")

        # 지정된 URL로 이동
        self.driver.get(url)

        # 이미지/비디오 요소 추출
        element = self.driver.find_element(By.ID, "article_1")

        img_elems = self.extract_img_elems(element)
        video_elems = self.extract_video_elems(element)

        elems = img_elems + video_elems
        elems.sort(key=lambda e: e.location["y"])

        log.info(
            f"\thas {len(elems)} elements, {len(img_elems)} images and {len(video_elems)} videos"
        )

        def save_as_win32(driver, element, delay: float = 0.2):
            import win32com.client as comclt

            wsh = comclt.Dispatch("WScript.Shell")
            ActionChains(driver).move_to_element(element).context_click().perform()
            time.sleep(0.2)
            wsh.SendKeys("{v}")
            time.sleep(delay)

        # 단일 파일 다운로드
        if len(elems) == 1:
            self.download_element(save_as_win32, elems[0])
            time.sleep(1)

            origin_filename = os.listdir(TEMPORAL_BASE_PATH)[0]
            ext = origin_filename.split(".")[-1]
            new_filename = f"{self.get_title()}_.{ext}"

            shutil.move(
                os.path.join(TEMPORAL_BASE_PATH, origin_filename),
                os.path.join(DOWNLOAD_BASE_PATH, new_filename),
            )
        else:  # 여러 파일 다운로드
            # 페이지 폴더 생성
            page_download_path = os.path.join(DOWNLOAD_BASE_PATH, self.get_title())
            fs.mkdir_if_not_exist(page_download_path)

            # 엘리먼트 다운로드
            for index, elem in enumerate(elems):
                log.info(f"\tdownload element: {elem}")

                if src := self.get_source(elem):
                    log.info(f"source detected: {src}")
                else:
                    log.warn(f"can not specify source of elements: {elem}")

                origin_filename = self.download_element(save_as_win32, elem)

                ext = origin_filename.split(".")[-1]
                seq_filename = f"{elem.tag_name}_{index}.{ext}"

                shutil.move(
                    os.path.join(TEMPORAL_BASE_PATH, origin_filename),
                    os.path.join(page_download_path, seq_filename),
                )

    def filter_exclude_htm_file(self, files: list[str]) -> list[str]:
        return [f for f in files if not f.endswith(".htm")]

    def download_element(self, save_as_win32: Callable, elem: WebElement) -> str:
        def check_is_downloaded() -> Tuple[str, bool]:
            files = os.listdir(TEMPORAL_BASE_PATH)
            if not files:
                return ("", False)

            files = self.filter_exclude_htm_file(files)
            if len(files) != 1:
                raise Exception(f"file is not one: {files}")

            origin_filename = files[0]
            ext = origin_filename.split(".")[-1]

            log.info(f"{origin_filename} downloaded")

            if ext in ["crdownload", "html", "hml", "htm"]:
                raise Exception("downloaded wrong file")

            return (origin_filename, True)

        match elem.tag_name:
            case "img":
                save_as_win32(self.driver, elem)
            case "video":
                save_as_win32(self.driver, elem, 4)
            case _:
                raise Exception(f"알 수 없는 태그 네임: {elem.tag_name}")

        for i in range(10):
            time.sleep(1)
            name, ok = check_is_downloaded()
            if ok:
                return name
            print(f"download checking ({i+1}/{10})")
        raise Exception("download failed")

    def extract_video_elems(self, element: WebElement):
        video_elems = element.find_elements(By.TAG_NAME, "video")
        return video_elems

    def extract_img_elems(self, element: WebElement):
        img_elems = element.find_elements(By.TAG_NAME, "img")

        # 이미지는 가로와 세로가 최소 200 이상이어야 함
        img_elems = [
            elem
            for elem in img_elems
            if (elem.size["height"] > LIMIT and elem.size["width"] > LIMIT)
        ]

        return img_elems

    def get_source(self, elem: WebElement) -> str:
        """ """
        if s := elem.get_attribute("src"):
            return s
        elif s := elem.find_element(By.TAG_NAME, "source"):
            return s.get_attribute("src")
        return ""


fs.mkdir_if_not_exist(TEMPORAL_BASE_PATH)
fs.mkdir_if_not_exist(DOWNLOAD_BASE_PATH)

fs.clear_dir(TEMPORAL_BASE_PATH)


urls = load_list_of_urls("lists.txt")

ddd = DogDripDownloader()

for url in urls:
    ddd.download(url)
