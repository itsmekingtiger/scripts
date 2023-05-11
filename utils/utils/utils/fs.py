
import os


def clear_dir(path: str):
    if not os.path.exists(path):
        raise Exception(f'디렉토리 비우기 실패: "{path}" is not exists')

    if not os.path.isdir(path):
        raise Exception(f'디렉토리 비우기 실패: "{path}" is not directory')

    for file_name in os.listdir(path):
        file_path = os.path.join(path, file_name)

        # 파일이면 삭제
        if os.path.isfile(file_path):
            os.remove(file_path)

        # 디렉터리이면 재귀적으로 삭제
        elif os.path.isdir(file_path):
            clear_dir(file_path)
            os.rmdir(file_path)