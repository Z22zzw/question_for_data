#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd "$ROOT_DIR"

case "${1:-up}" in
  up|start)
    docker compose up -d --build
    docker compose ps
    ;;
  restart)
    docker compose down
    docker compose up -d --build
    docker compose ps
    ;;
  down|stop)
    docker compose down
    ;;
  status|ps)
    docker compose ps
    ;;
  logs)
    docker compose logs -f "${@:2}"
    ;;
  *)
    echo "Usage: $0 [up|start|restart|down|stop|status|ps|logs]" >&2
    exit 2
    ;;
esac
