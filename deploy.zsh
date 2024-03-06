# Check if the .env file exists
if [[ ! -f .env ]]; then
  echo ".env file not found!"
  exit 1
fi

# Load the .env file using source
set -a
source .env
set +a

# Spin up a gunicorn server
gunicorn --bind ${HOST}:${PORT} --workers 1  TaskMan:app