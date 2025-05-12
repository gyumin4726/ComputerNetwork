# HTTP 클라이언트-서버 통신 프로젝트

이 프로젝트는 Python을 사용하여 HTTP 클라이언트-서버 통신을 구현한 것입니다.

## 프로젝트 구조

- `client_final.py`: HTTP 클라이언트 구현 (GUI 인터페이스 포함)
- `server_final.py`: HTTP 서버 구현
- `Report.md`: 프로젝트 상세 보고서

## 주요 기능

- HTTP 메서드 지원 (GET, PUT, HEAD, POST)
- 토큰 기반 인증 시스템
- 리다이렉트 처리
- 다양한 HTTP 상태 코드 처리
- 사용자 친화적인 GUI 인터페이스

## 실행 방법

1. 서버 실행:
   ```bash
   python server_final.py
   ```

2. 클라이언트 실행:
   ```bash
   python client_final.py
   ```

## 사용 방법

### 기본 요구사항
- 모든 요청에 대해 토큰에 'Pass'를 입력해야 합니다
- 각 HTTP 메서드별로 정확한 경로를 입력해야 합니다

### HTTP 메서드별 사용법

#### 1. GET 요청
- 경로: `www.get.com`
- 본문: 비워두기
- 토큰: `Pass`
- 가능한 응답:
  - 200 OK: 정상 응답
  - 400 Bad Request: 'computer-network' 헤더 누락
  - 401 Unauthorized: 잘못된 토큰
  - 404 Not Found: 잘못된 경로
  - 500 Internal Server Error: 서버 내부 오류
  - 501 Not Implemented: 구현되지 않은 기능
  - 502 Bad Gateway: 게이트웨이 오류
  - 301/303/307: 리다이렉트 응답

#### 2. PUT 요청
- 경로: `www.put.com`
- 본문: `right-body` (정확히 이 값이어야 함)
- 토큰: `Pass`
- 가능한 응답:
  - 200 OK: 정상 응답
  - 400 Bad Request: 
    - 'computer-network' 헤더 누락
    - 본문이 'right-body'가 아님
  - 401 Unauthorized: 잘못된 토큰
  - 404 Not Found: 잘못된 경로
  - 500/501/502: 서버 오류
  - 301/303/307: 리다이렉트 응답

#### 3. HEAD 요청
- 경로: `www.head.com`
- 본문: 비워두기
- 토큰: `Pass`
- 가능한 응답:
  - 200 OK: 정상 응답
  - 400 Bad Request: 'computer-network' 헤더 누락
  - 401 Unauthorized: 잘못된 토큰
  - 404 Not Found: 잘못된 경로
  - 500/501/502: 서버 오류
  - 301/303/307: 리다이렉트 응답

#### 4. POST 요청
- 경로: `www.post.com`
- 본문: `right-body` (정확히 이 값이어야 함)
- 토큰: `Pass`
- 가능한 응답:
  - 200 OK: 정상 응답
  - 400 Bad Request: 
    - 'computer-network' 헤더 누락
    - 본문이 'right-body'가 아님
  - 401 Unauthorized: 잘못된 토큰
  - 404 Not Found: 잘못된 경로
  - 500/501/502: 서버 오류
  - 301/303/307: 리다이렉트 응답

### 리다이렉트 응답 처리
- 301/303/307 응답을 받으면 자동으로 새로운 위치로 재요청됩니다
- 리다이렉트된 경로:
  - GET: `www.new-get.com/`, `www.see-other-get.com/`, `www.temporary-get.com/`
  - PUT: `www.new-put.com/`, `www.see-other-put.com/`, `www.temporary-put.com/`
  - HEAD: `www.new-head.com/`, `www.see-other-head.com/`, `www.temporary-head.com/`
  - POST: `www.new-post.com/`, `www.see-other-post.com/`, `www.temporary-post.com/`

## 요구사항

- Python 3.x
- tkinter (GUI 구현용)

## 주의사항

- 서버가 먼저 실행되어 있어야 클라이언트가 연결 가능
- 인증을 위해서는 반드시 토큰에 'Pass' 입력 필요
- 서버와 클라이언트는 별도의 터미널에서 실행해야 함
- 경로는 정확히 입력해야 하며, 앞뒤 공백이 없어야 함
- PUT과 POST 요청의 본문은 정확히 'right-body'여야 함
- 서버는 랜덤하게 오류를 발생시킬 수 있음 (500, 501, 502)
- 30% 확률로 리다이렉트 응답이 발생할 수 있음

## HTTP 응답 코드 설명

### 200 OK
- 정상적인 요청이 성공적으로 처리된 경우
- 모든 조건이 만족될 때 발생:
  - 올바른 경로 사용
  - 올바른 토큰('Pass') 입력
  - PUT/POST 요청의 경우 올바른 본문('right-body') 입력
  - 'computer-network' 헤더 존재

### 400 Bad Request
- 요청이 잘못된 경우 발생:
  - 'computer-network' 헤더가 없는 경우
  - PUT/POST 요청에서 본문이 'right-body'가 아닌 경우
  - 본문의 형식이 잘못된 경우

### 401 Unauthorized
- 인증에 실패한 경우 발생:
  - 토큰이 'Pass'가 아닌 경우
  - 토큰이 입력되지 않은 경우
  - Authorization 헤더가 없는 경우

### 404 Not Found
- 요청한 리소스를 찾을 수 없는 경우 발생:
  - 잘못된 경로 입력
  - 존재하지 않는 경로 요청
  - 경로에 오타가 있는 경우

### 500 Internal Server Error
- 서버 내부 오류 발생:
  - 서버의 랜덤 상태에 의해 발생 (약 11% 확률)
  - 서버의 예기치 않은 오류

### 501 Not Implemented
- 서버가 요청한 기능을 지원하지 않는 경우:
  - 서버의 랜덤 상태에 의해 발생 (약 11% 확률)
  - 구현되지 않은 HTTP 메서드 요청

### 502 Bad Gateway
- 게이트웨이 오류 발생:
  - 서버의 랜덤 상태에 의해 발생 (약 11% 확률)
  - 서버의 통신 오류

### 301/303/307 리다이렉트
- 리다이렉트가 필요한 경우 발생:
  - 서버의 랜덤 상태에 의해 발생 (30% 확률)
  - 301: 영구 리다이렉트
  - 303: See Other
  - 307: 임시 리다이렉트

## 응답 코드 발생 확률
- 200 OK: 약 47% (정상 요청 시)
- 500/501/502: 각각 약 11% (서버 상태에 따라)
- 301/303/307: 총 30% (리다이렉트)
- 400/401/404: 요청 오류 시 100% (해당 조건 만족 시) 