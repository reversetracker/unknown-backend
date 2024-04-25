# 기본 서버 설정
workers = 1  # 동시에 처리할 작업자(프로세스) 수. 일반적으로 CPU 코어 수 * 2 + 1 권장
worker_class = "uvicorn.workers.UvicornWorker"  # 비동기 처리를 위한 Uvicorn 워커 클래스
bind = "0.0.0.0:80"  # 서버가 바인딩될 호스트와 포트
keep_alive = 2  # 클라이언트가 지속 연결을 유지하는 시간(초)
timeout = 10  # 워커가 응답하는 데까지 허용되는 최대 시간(초)
accesslog = "-"  # 접근 로그 경로, "-"는 표준 출력을 의미
errorlog = "-"  # 에러 로그 경로, "-"는 표준 출력을 의미

# 로깅 설정
loglevel = "info"  # 로깅 레벨 (debug, info, warning, error, critical)
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# 보안 설정
limit_request_line = 4094  # 허용되는 최대 HTTP 요청 라인 크기(바이트)
limit_request_fields = 100  # 요청당 허용되는 최대 헤더 필드 수

# 성능 최적화
threads = 1  # 각 워커당 스레드 수 (gthread 워커 클래스를 사용하는 경우)
worker_connections = (
    1000  # 최대 클라이언트 동시 연결 수 (eventlet, gevent 워커 클래스를 사용하는 경우)
)
max_requests = 1000  # 워커를 재시작하기 전에 처리할 최대 요청 수
max_requests_jitter = 50  # 워커 재시작 간 최대 요청 수에 추가되는 임의의 변동 값

# 프로세스 이름 설정
proc_name = "gunicorn-proc"  # 프로세스 이름 지정

# 그레이스풀 셧다운 타임
graceful_timeout = 30  # 재시작 시 워커가 종료되기를 기다리는 최대 시간(초)

# 기타
reload = False  # 개발 중 코드 변경시 자동 리로드 활성화, 배포 환경에서는 사용하지 않는 것이 좋음
preload_app = False  # 시작 시 애플리케이션을 사전 로드할지 여부, 메모리 사용량 감소와 애플리케이션 시작 시간 단축 효과
