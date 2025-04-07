from fastapi import FastAPI, File, UploadFile, HTTPException
from PIL import Image
import io

from uvicorn.config import Config
from uvicorn.server import Server

from detector import detector

app = FastAPI()

d = detector()


ALLOWED_MIME_TYPES = [
    "image/jpeg",  # JPG
    "image/png",   # PNG
    "image/gif",   # GIF
    "image/bmp",   # BMP
    "image/tiff",  # TIFF
    "image/webp",  # WebP
]


@app.post("/detect")
async def upload_image(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400, detail="Only image files are allowed")
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        result = d.detect(image)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing image: {str(e)}")


def run_server():
    # log_config = {
    #     "version": 1,
    #     "disable_existing_loggers": False,
    #     "handlers": {
    #         "file_handler": {
    #             "class": "logging.FileHandler",
    #             "filename": "app.log",
    #             "mode": "a",
    #             "formatter": "default",
    #         },
    #     },
    #     "formatters": {
    #         "default": {
    #             "format": "%(asctime)s - %(levelname)s - %(message)s",
    #         },
    #     },
    #     "root": {
    #         "handlers": ["file_handler"],
    #         "level": "INFO",
    #     },
    # }
    # config = Config(app, host="0.0.0.0", port=7280, log_config=log_config)
    config = Config(app, host="0.0.0.0", port=7280)
    server = Server(config)
    server.run()

    server.should_exit = True
    server.force_exit = True


async def shutdown_event():
    await app.shutdown()


if __name__ == '__main__':
    run_server()
