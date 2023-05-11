import os

class AppException(Exception):
    pass


class CanNotCreateTempDir(AppException):
    pass


def mkdir_if_not_exist(tmpdir: str):
    if os.path.exists(tmpdir):
        if not os.path.isdir(tmpdir):
            raise CanNotCreateTempDir(f'file "{tmpdir}" is alreay exists ant it is not dir')
    else:
        os.mkdir(tmpdir)

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

def save(file_name: str, content: bytes):
    open(file_name, "wb").write(content)