import json
import asyncio
import datetime as dt
from typing import List

import pandas as pd
from polygon import WebSocketClient
from aiokafka import AIOKafkaProducer
from polygon.websocket.models import WebSocketMessage

# Historic days lookback 
lookback_days = 1

# Equities we should maintain data about
equities = ["COIN"]

class KafkaCallback:
    def __init__(self, bootstrap='127.0.0.1', port=9092, topic=None, numeric_type=float, none_to=None,
                 **kwargs):  # working locally
        """
        bootstrap: str, list
            if a list, should be a list of strings in the format: ip/host:port, i.e.
                192.1.1.1:9092
                192.1.1.2:9092
                etc
            if a string, should be ip/port only
        """
        self.bootstrap = bootstrap
        self.port = port
        self.producer = None
        self.topic = topic if topic else self.default_topic
        self.numeric_type = numeric_type
        self.none_to = none_to

    async def __connect(self):
        if not self.producer:
            loop = asyncio.get_event_loop()
            self.producer = AIOKafkaProducer(acks=0,
                                             loop=loop,
                                             bootstrap_servers=f'{self.bootstrap}:{self.port}' if isinstance(
                                                 self.bootstrap, str) else self.bootstrap,
                                             client_id='polygon')
            await self.producer.start()

    async def write(self, data: dict):
        await self._connect()
        for i in data:
            await self.producer.send_and_wait(
                        self.topic, 
                        json.dumps(i).encode('utf-8')
                        )

def print_handler(msgs: List[WebSocketMessage]):
    for m in msgs:
        print(m)

def last_n_weekdays(start_date: pd.Timestamp, n: int):
    date_range = pd.date_range(end=start_date, periods=n*5)  # Generate a range of dates including weekends
    weekdays = date_range[date_range.weekday < 5]  # Filter out weekends (0=Monday, 4=Friday)
    return weekdays[-n:]  # Return the last N weekdays

def spawn_equity_trade_webhook_client(equities = equities, handler = print_handler):
    client = WebSocketClient()
    args = [f"T.{i}" for i in equities]
    client.subscribe(*args)
    return client.run(handler)

