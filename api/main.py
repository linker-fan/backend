import os
import uvicorn

#HOST = os.getenv("SERVER_HOST")
#PORT = os.getenv("SERVER_PORT")
HOST="0.0.0.0"
PORT=8000

if __name__ == "__main__":
    uvicorn.run('server.app:app', host=HOST, port=PORT, reload=True)