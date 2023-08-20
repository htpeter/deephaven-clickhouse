import os

from src.polygon_config import equities, spawn_equity_trade_webhook_client, KafkaCallback

def main():
    # see docker_files/Dockerfile.cryptofeed where we set IS_DOCKER=True
    # by doing this here, we can also run this script locally
    # see https://www.confluent.io/blog/kafka-client-cannot-connect-to-broker-on-aws-on-docker-etc/#scenario-4
    kakfa_bootstrap = 'redpanda' if os.environ.get('IS_DOCKER') else 'localhost'
    kakfa_port = 29092 if os.environ.get('IS_DOCKER') else 9092

    kafka = KafkaCallback(
                bootstrap=kakfa_bootstrap, 
                port=kakfa_port,
                topic = 'polygon-trades'
                )

    spawn_equity_trade_webhook_client(
                equities = equities,
                handler = kafka.write
                )

if __name__ == '__main__':
    main()

