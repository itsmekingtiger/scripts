# 개드립 첨부 파일 다운로더

이미지, 비디오 다운로더

## 기능

1. Download images and videos
2. Files will be renamed by order in place of page.

## 사전 요구사항

1. Python 3.10 이상
2. Poetry
3. Chrome, Chrome Driver

## 사용법

1. 크롬 버전에 맞는 크롬 드라이버를 프로젝트 루트에 위치
2. `lists.txt`에 포스트 URL 작성
3. 다음 스크립트 실행.
   ```powershell
   > .\run.ps1
   ```

## Backlog

- [ ] 텍스트도 추출하고 마크다운으로 출력하는 기능 추가
- [ ] 다운로드된 URL은 자동으로 제거하는 기능 추가
