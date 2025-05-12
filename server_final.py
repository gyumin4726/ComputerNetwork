# 랜덤 상황을 위한 랜덤 모듈 불러오기
import random

# http.server 모듈로부터 BaseHTTPRequestHandler와 HTTPServer 불러오기
from http.server import BaseHTTPRequestHandler, HTTPServer

# BaseHTTPRequestHandler를 상속받아 SimpleHTTPRequestHandler 클래스 정의
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    # 보안 토큰을 통한 인증 로직
    def check_auth(self):
        # HTTP 헤더에서 'Authorization' 항목을 가져오기
        auth_header = self.headers.get('Authorization')

        # 'Authorization' 항목이 없거나 값이 'Pass'가 아니면 401 Unauthorized 전송
        if auth_header is None or auth_header != 'Pass':
            self.send_response(401)
            self.end_headers()
            return False # 인증 실패
        return True # 인증 성공

    # GET 요청에 대한 응답 메서드
    def do_GET(self):

        # 요청 경로가 올바른 경로인 "www.get.com"인 경우
        if self.path == "www.get.com":

            # 요청 헤더에서 'computer-network' 항목 확인
            special_header = self.headers.get('computer-network')

            # 'computer-network' 항목이 없으면 400 Bad Request 전송
            if special_header is None:
                self.send_response(400)

            else:
                # 보안 인증 체크
                if not self.check_auth():
                    return

                # 서버 상태 랜덤 결정
                server_state = random.randrange(0,9)

                # 서버 상태에 따라 다른 HTTP 상태 코드 전송
                if server_state == 0:
                    self.send_response(500) # 500 Internal Server Error 전송
                elif server_state == 1:
                    self.send_response(501) # 501 Not Implemented 전송
                elif server_state == 2:
                    self.send_response(502) # 502 Bad Gateway 전송

                else:
                    # 30% 확률로 리다이렉트 수행
                    if random.random()<0.3:

                        # 리다이렉트 코드 랜덤 결정
                        redirect_code = random.choice([301,303,307,404])

                        # 선택된 코드를 응답으로 전송
                        self.send_response(redirect_code)

                        # 상태 코드에 따라 다른 위치로 리다이렉트
                        if redirect_code == 301:
                            self.send_header('Location', 'www.new-get.com/')
                            self.end_headers()
                        elif redirect_code == 303:
                            self.send_header('Location', 'www.see-other-get.com/')
                            self.end_headers()
                        elif redirect_code == 307:
                            self.send_header('Location', 'www.temporary-get.com/')
                            self.end_headers()
                        else:
                            self.send_header('Location', 'Unkown')
                            self.end_headers()

                    else:
                        # 리다이렉트를 수행하지 않는 경우, 200 OK 응답 전송
                        self.send_response(200)

        # 'www.new-get.com/', 'www.see-other-get.com/', 'www.temporary-get.com/' 경로로 들어온 요청을 처리
        elif self.path == "www.new-get.com/" or self.path =='www.see-other-get.com/' or self.path =='www.temporary-get.com/':

            # 요청 헤더에서 'computer-network' 항목 확인
            special_header = self.headers.get('computer-network')

            # 'computer-network' 항목이 없으면 400 Bad Request 응답 전송
            if special_header is None:
                self.send_response(400)

            else:
                # 보안 인증 체크
                if not self.check_auth():
                    return

                # 인증이 성공할 경우, 200 OK 응답 전송
                self.send_response(200,self.path)
                self.end_headers()

        # 위의 모든 경우에 해당하지 않는 잘못된 경로에 대해서는 404 Not Found 응답 전송
        else:
            self.send_response(404) 
        self.end_headers()

    # PUT 요청에 대한 응답 메서드
    def do_PUT(self):

        # 요청 경로가 올바른 경로인 "www.put.com"인 경우
        if self.path == "www.put.com":

            # 요청 헤더에서 'computer-network' 항목 확인
            special_header = self.headers.get('computer-network')

            # 'computer-network' 항목이 없으면 400 Bad Request 전송
            if special_header is None:
                self.send_response(400)

            else:
                # 'content_length'를 HTTP 헤더에서 불러들이기
                content_length = self.headers.get('Content-Length')
                
                # 'content_length'를 정수로 변환
                length = int(content_length)

                # 'length'에 해당하는 길이만큼 요청 본문 읽어들이기
                body = self.rfile.read(length)


                # 읽은 본문을 디코딩하고, 그 내용이 'right-body'와 일치하는지 확인
                if body.decode() != 'right-body':

                    # 본문 내용이 'right-body'와 일치하지 않으면 400 Bad Request 응답
                    self.send_response(400)

                else:
                    # 보안 인증 체크
                    if not self.check_auth(): 
                        return

                    # 서버 상태 랜덤 결정
                    server_state = random.randrange(0,9)

                    # 서버 상태에 따라 다른 HTTP 상태 코드 전송
                    if server_state == 0:
                        self.send_response(500) # 500 Internal Server Error 전송
                    elif server_state == 1:
                        self.send_response(501) # 501 Not Implemented 전송
                    elif server_state == 2:
                        self.send_response(502) # 502 Bad Gateway 전송

                    else:
                        # 30% 확률로 리다이렉트 수행
                        if random.random()<0.3:

                            # 리다이렉트 코드 랜덤 결정
                            redirect_code = random.choice([301,303,307,404])

                            # 선택된 코드를 응답으로 전송
                            self.send_response(redirect_code)

                            # 상태 코드에 따라 다른 위치로 리다이렉트
                            if redirect_code == 301:
                                self.send_header('Location', 'www.new-put.com/')
                                self.end_headers()
                            elif redirect_code == 303:
                                self.send_header('Location', 'www.see-other-put.com/')
                                self.end_headers()
                            elif redirect_code == 307:
                                self.send_header('Location', 'www.temporary-put.com/')
                                self.end_headers()
                            else:
                                self.send_header('Location', 'Unkown')
                                self.end_headers()

                        else:
                            # 리다이렉트를 수행하지 않는 경우, 200 OK 응답 전송
                            self.send_response(200)

        # 'www.new-get.com/', 'www.see-other-get.com/', 'www.temporary-get.com/' 경로로 들어온 요청을 처리
        elif self.path == "www.new-put.com/" or self.path =='www.see-other-put.com/' or self.path =='www.temporary-put.com/':

            # 요청 헤더에서 'computer-network' 항목 확인
            special_header = self.headers.get('computer-network')

            # 'computer-network' 항목이 없으면 400 Bad Request 응답 전송
            if special_header is None:
                self.send_response(400)

            else:
                # 보안 인증 체크
                if not self.check_auth(): 
                    return

                # 인증이 성공할 경우, 200 OK 응답 전송
                self.send_response(200,self.path)
                self.end_headers()

        # 위의 모든 경우에 해당하지 않는 잘못된 경로에 대해서는 404 Not Found 응답 전송
        else:
            self.send_response(404)
        self.end_headers()

    # HEAD 요청에 대한 응답 메서드
    def do_HEAD(self):

        # 요청 경로가 올바른 경로인 "www.head.com"인 경우
        if self.path == "www.head.com":

            # 보안 인증 체크
            if not self.check_auth():
                return

            # 서버 상태 랜덤 결정
            server_state = random.randrange(0,9)

            # 서버 상태에 따라 다른 HTTP 상태 코드 전송
            if server_state == 0:
                self.send_response(500) # 500 Internal Server Error 전송
            elif server_state == 1:
                self.send_response(501) # 501 Not Implemented 전송
            elif server_state == 2:
                self.send_response(502) # 502 Bad Gateway 전송

            else:
                # 30% 확률로 리다이렉트 수행  
                if random.random()<0.3:

                    # 리다이렉트 코드 랜덤 결정
                    redirect_code = random.choice([301,303,307,404])

                    # 선택된 코드를 응답으로 전송
                    self.send_response(redirect_code)

                    # 상태 코드에 따라 다른 위치로 리다이렉트
                    if redirect_code == 301:
                        self.send_header('Location', 'www.new-head.com/')
                        self.end_headers()
                    elif redirect_code == 303:
                        self.send_header('Location', 'www.see-other-head.com/')
                        self.end_headers()
                    elif redirect_code == 307:
                        self.send_header('Location', 'www.temporary-head.com/')
                        self.end_headers()
                    else:
                        self.send_header('Location', 'Unkown')
                        self.end_headers()

                else:
                    # 리다이렉트를 수행하지 않는 경우, 200 OK 응답 전송
                    self.send_response(200)

        # 'www.new-get.com/', 'www.see-other-get.com/', 'www.temporary-get.com/' 경로로 들어온 요청을 처리
        elif self.path == "www.new-head.com/" or self.path =='www.see-other-head.com/' or self.path =='www.temporary-head.com/':

            # 요청 헤더에서 'computer-network' 항목 확인
            special_header = self.headers.get('computer-network')

            # 'computer-network' 항목이 없으면 400 Bad Request 응답 전송
            if special_header is None:
                self.send_response(400)

            else:
                # 보안 인증 체크
                if not self.check_auth():  # 인증 체크
                    return
              
                # 인증이 성공할 경우, 200 OK 응답 전송
                self.send_response(200,self.path)
                self.end_headers()

        # 위의 모든 경우에 해당하지 않는 잘못된 경로에 대해서는 404 Not Found 응답 전송
        else:
            self.send_response(404)     
        self.end_headers()

    # POST 요청에 대한 응답 메서드
    def do_POST(self):

        # 요청 경로가 올바른 경로인 "www.post.com"인 경우
        if self.path == "www.post.com":

            # 요청 헤더에서 'computer-network' 항목 확인
            special_header = self.headers.get('computer-network')

            # 'computer-network' 항목이 없으면 400 Bad Request 전송
            if special_header is None:
                self.send_response(400)

            else:
                # 'content_length'를 HTTP 헤더에서 불러들이기
                content_length = self.headers.get('Content-Length')
                
                # 'content_length'를 정수로 변환
                length = int(content_length)

                # 'length'에 해당하는 길이만큼 요청 본문 읽어들이
                body = self.rfile.read(length)

                # 읽은 본문을 디코딩하고, 그 내용이 'right-body'와 일치하는지 확인
                if body.decode() != 'right-body':
                    # 본문 내용이 'right-body'와 일치하지 않으면 400 Bad Request 응답 전
                    self.send_response(400)

                else:
                    # 보안 인증 체크
                    if not self.check_auth():
                        return

                    # 서버 상태 랜덤 결정
                    server_state = random.randrange(0,9)

                    # 서버 상태에 따라 다른 HTTP 상태 코드 전송
                    if server_state == 0:
                        self.send_response(500) # 500 Internal Server Error 전송
                    elif server_state == 1:
                        self.send_response(501) # 501 Not Implemented 전송
                    elif server_state == 2: 
                        self.send_response(502) # 502 Bad Gateway 전송

                    else:

                        # 30% 확률로 리다이렉트 수행  
                        if random.random()<0.3:

                            # 리다이렉트 코드 랜덤 결정
                            redirect_code = random.choice([301,303,307,404])

                            # 선택된 코드를 응답으로 전송
                            self.send_response(redirect_code)

                            # 상태 코드에 따라 다른 위치로 리다이렉트
                            if redirect_code == 301:
                                self.send_header('Location', 'www.new-post.com/')
                                self.end_headers()
                            elif redirect_code == 303:
                                self.send_header('Location', 'www.see-other-post.com/')
                                self.end_headers()
                            elif redirect_code == 307:
                                self.send_header('Location', 'www.temporary-post.com/')
                                self.end_headers()
                            else:
                                self.send_header('Location', 'Unkown')
                                self.end_headers()
                        
                        else:
                            # 리다이렉트를 수행하지 않는 경우, 201 Created 응답 전송
                            self.send_response(201)

        # 'www.new-get.com/', 'www.see-other-get.com/', 'www.temporary-get.com/' 경로로 들어온 요청을 처리
        elif self.path == "www.new-post.com/" or self.path =='www.see-other-post.com/' or self.path =='www.temporary-post.com/':

            # 요청 헤더에서 'computer-network' 항목 확인
            special_header = self.headers.get('computer-network')

            # 'computer-network' 항목이 없으면 400 Bad Request 응답 전송
            if special_header is None:
                self.send_response(400)

            else:
                # 보안 인증 체크
                if not self.check_auth():
                    return

                # 인증이 성공할 경우, 201 Created 응답 전송
                self.send_response(201,self.path)
                self.end_headers()
        # 위의 모든 경우에 해당하지 않는 잘못된 경로에 대해서는 404 Not Found 응답 전송
        else:
            self.send_response(404) 
        self.end_headers()

# 서버를 실행는 메서드
def start_server():

    # 서버가 동작할 주소와 포트를 'localhost' 주소의 8088 포트로 설정
    server_address = ('localhost', 8088)

    # HTTPServer 객체를 생성, 요청을 처리할 핸들러로 'SimpleHTTPRequestHandler'를 사용
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)

    # 서버가 실행됨을 알리는 메시지를 출력
    print(f"Starting server on {server_address[0]}:{server_address[1]}")

    # 서버를 실행하고, 클라이언트로부터의 요청을 무한히 대기하며, 요청이 들어오면 처리
    httpd.serve_forever()

#'start_server' 함수를 호출하여 서버를 시작
if __name__ == "__main__":
    start_server()
