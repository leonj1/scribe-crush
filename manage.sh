#!/bin/bash

case "$1" in
  start)
    echo "Starting all services..."
    docker-compose up -d
    ;;
  stop)
    echo "Stopping all services..."
    docker-compose down
    ;;
  restart)
    echo "Restarting all services..."
    docker-compose restart
    ;;
  logs)
    docker-compose logs -f
    ;;
  status)
    docker-compose ps
    ;;
  *)
    echo "Usage: $0 {start|stop|restart|logs|status}"
    exit 1
    ;;
esac
