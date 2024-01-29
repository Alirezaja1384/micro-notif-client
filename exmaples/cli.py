import asyncio
from micro_notif import v1 as micro_notif

RMQ_CONN_STR = "amqp://guest:guest@localhost:5672"
RMQ_EXCHANGE_NAME = "micro_notif"


async def main():
    client = micro_notif.MicroNotifRabbitMQClient(
        conn_str=RMQ_CONN_STR, exchange_name=RMQ_EXCHANGE_NAME, durable=True
    )

    phone_number = input("Phone number: ")
    message = input("Message: ")

    await client.connect()
    await client.send_sms(message={"to": phone_number, "message": message})
    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
