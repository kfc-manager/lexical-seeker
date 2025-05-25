import pika
from typing import Iterator


class Queue:
    def __init__(self, queue_host: str, queue_name: str):
        self.queue_name = queue_name
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(queue_host),
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(
            queue=queue_name,
            durable=True,
            exclusive=False,
        )

    def close(self):
        self.connection.close()

    def send(self, link: str):
        self.channel.basic_publish(
            exchange="",
            routing_key=self.queue_name,
            body=link,
            properties=pika.BasicProperties(delivery_mode=2),
        )

    def consume(self) -> Iterator[str]:
        while True:
            method_frame, header_frame, body = self.channel.basic_get(
                queue=self.queue_name, auto_ack=False
            )
            if method_frame:
                self.channel.basic_ack(method_frame.delivery_tag)
                yield body.decode("utf-8")
            else:
                break
