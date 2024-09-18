### Tomato Agent Server MSA Architecture
## 간단 소개
    - 기존 tomatoAgent에서 백엔드 부분을 더 보완한 프로젝트입니다.(https://github.com/Oldentomato/tomato_agent)  
    - 더 유연한 커스터마이징을 위해 기존의 langchain을 사용하지 않고 openAI로만 구성되었습니다.  
    - 여러 유저들이 한번에 요청할 때를 고려하고, 빠른 속도로 처리하도록 구성했습니다. 
    - 기능 확장과 유지보수를 위하여 MSA구조로 설계하였습니다.  
## 사용된 기술
    - FastAPI
    - Redis
    - MongoDB
    - MongoDB Express (dev)
    - gunicorn
    - Docker
    - Docker Compose (dev)
    - Portainer (dev)
    - Docker Swarm
    - traefik
    - openAI
## 구조  
![img](https://github.com/Oldentomato/TomatoAgentServer/blob/main/gitImg/img1.png)
    - docker swarm을 이용하여 해당 서비스 스택을 deploy함  
    - traefik을 이용하여 80번포트로 들어오는 요청으로 로드밸런싱을 진행  
    - 현재는 모든 서버가 하나의 db를 바라보도록 했지만 추후에 db를 수평확장할 예정  
    - 각 서버 컨테이너 내부는 gunicorn으로 데이터를 주고받음  
    - traefik도 오류로 다운될 가능성을 대비해 replica를 하나 생성해둠
## 왜 traefik인가
    - 역방향 프록시 서버는 처음에는 nginx를 사용하려 했다. 하지만 docker swarm처럼 orchestrator에는 사용이 적합하지 않다는 내용을 보게 되었다. 컨테이너를 인식하는 기능자체가 없어 대부분 헬퍼툴을 사용한다는데, 비용이나 부실한 내용 등 사용에 어려움이 많다고 하는데, traefik은 기본적으로 헬퍼 툴로 구현되어 있다고 한다. 게다가 문서도 잘 정리되어 있고, 최신 툴 답게 서드파티 모듈을 사용할 필요가 없도록 구성되어있어 몇몇 기업은 nginx 대신 traefik을 사용한다고 한다.
## 왜 Docker Swarm인가
    - MSA를 구성을 할때는 대부분 Kubernetes를 사용한다. 안정적이면서 다양한 기능이 있고, 거대한 커뮤니티가 활성화 되어있어 수많은 기업에서 많이 사용한다.
    하지만 Kubernetes 자체가 기능이 많은 만큼 무겁고 느리다. 심지어 세팅을 할 때도 많은 작업이 필요하기 때문에 대규모 프로젝트에 적합하다.
    이 프로젝트는 그만큼 큰 프로젝트는 아니기 때문에, Kubernetes와 목적은 같지만 좀 더 가볍고 사용하기 편한 Docker Swarm을 사용하게 되었다. Kubernetes만큼 기능이 많지는 않지만 기본적인 구성을 갖출 수 있고, docker compose에서 변형하여 사용할 수 있어 손쉽게 접근이 가능하다.

## 왜 Redis인가
    - 각 요청이 들어올 때마다 유저별 클래스 객체를 인스턴스하고, db에서 유저의 정보를 가져온 다음, 소스코드를 실행하게 된다. 채팅을 보낼 때마다 이러한 작업들이 이루어지면 쓸데없는 반복작업이 이루어지기 때문에 속도가 빠르지 않다.
    그러기에, 미리 데이터를 유저별로 메모리상에 저장해두고 요청할 때마다 디스크가 아닌 메모리에서 데이터를 가져오게 한다면 더 빠르게 처리할 수 있을 것이다.

## 블로그 
[블로그 이동하기](https://wsportfolio.vercel.app/blog/post_1)  