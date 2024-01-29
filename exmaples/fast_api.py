from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import Depends, FastAPI
from pydantic import BaseModel, Field
from micro_notif import v1 as micro_notif

_client = micro_notif.MicroNotifRabbitMQClient(
    conn_str="amqp://guest:guest@localhost:5672",
    exchange_name="micro_notif",
    durable=True,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await _client.connect()
    yield
    await _client.disconnect()


app = FastAPI(docs_url="/docs", lifespan=lifespan)


def get_client():
    return _client


class SendSMSModel(BaseModel):
    to: str = Field(pattern=r"09[0-9]{9}")
    message: str = Field(min_length=1)


@app.post("/send_sms")
async def send_sms(
    body: SendSMSModel,
    client: Annotated[
        micro_notif.MicroNotifRabbitMQClient, Depends(get_client)
    ],
):
    await client.send_sms(message={"to": body.to, "message": body.message})
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
