FROM debian
RUN apt update && apt install -y nginx libnginx-mod-rtmp

CMD ["nginx", "-g", "daemon off;"]