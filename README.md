# tiny_crawler.exe 사용법

> 아직 베타 버전이라 MODE 1 밖에 안됨 뮤ㅠㅠ

## 동작 방식

1. list.txt에 링크들을 가져온다.
2. 링크들 마다 이미지를 몇 장씩 가져온다.
3. images 폴더에 저장한다.

## 설정 방법

1. config.ini 파일을 연다.
2. 한 명당 NUMBER_OF_IMAGES 수 만큼 가져온다.
3. NUMBER_OF_IMAGES를 2로 설정하면 2장 가져온다.(최대 6장)

## 사용 예시

1. list.txt에 원하는 사람 인스타 주소를 넣는다.(https://instagram.com/dev.gon.io/)
2. config.ini의 NUMBER_OF_IMAGES의 숫자를 원하는 만큼 수정
3. images에 잘 내려받는지 확인
4. 즐긴다.

## 주의사항

- 파일 해킹이나 폴더손상(images)가 발생하면 프로그램 종료
- 이 프로그램은 테스트용 크롬브라우저를 키고 로그인 후 사진을 다운로드함 놀라지 말 것.
