#!/bin/sh

action=$1
usage(){
    echo "$0 <action>"
    echo " action = startd | start | status | stop | logs | build"
}

start(){
   sudo docker-compose up
}

startd(){
   sudo docker-compose up -d
}

status(){
   sudo docker ps | grep q3 
}

stop(){
   sudo docker-compose down 
}

logs(){
   sudo docker ps | grep shortenurl | awk '{print $NF}' |xargs sudo docker logs -f
}

build(){
   sudo docker-compose build --no-cache
}


case ${action} in
  start)
    start ;;
  startd)
    startd ;;
  status)
    status ;;
  stop)
    stop ;;
  logs)
    logs ;;
  build)
    build ;;
  remove) 
    remove ;;
  *)
    usage ;;
esac
