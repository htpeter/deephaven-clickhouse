# Deephaven + Clickhouse
TLDR;
Deephaven Community doesn't provide a built-in persistent storage layer (as of Apr 2023), so let's use 
[Clickhouse](https://clickhouse.com/) to create one.<br><br>
This repo shows how to 
* leverage [Cryptofeed](https://github.com/bmoscon/cryptofeed) to subscribe to 24/7 real-time Crypto market data
* push the data onto Kafka to create live streams
* persist the streams via the Clickhouse Kafka Table Engine
* access real-time streams and historical data from the DH UI, plus some magic to stitch them together
* build a Deephaven app mode around it

## General Setup 
Everything should "just work", simply run this and wait until all 5 containers start up:<br>
```
docker-compose up -d
```
* Deephaven UI is running at http://localhost:10000/ide/
* ClickHouse Play is running at http://localhost:8123/play
  * CLICKHOUSE_USER: default
  * CLICKHOUSE_PASSWORD: password
* Redpanda Console is running at http://localhost:8080/overview

* Data is stored locally under the `/data/[deephaven|clickhouse]` folders which are mounted into the docker images

## Project structure
```
├── build                               <- Docker build and startup scripts 
│   ├── Dockerfile.cryptofeed               <- Dockerfile for Cryptofeed subscriptions
│   ├── Dockerfile.deephaven                <- Dockerfile for Deephaven server
│   ├── init_orderbooks.sql                 <- init script to create cryptfeed.trades* tables
│   ├── init_trades.sql                     <- init script to create cryptfeed.orderbooks* tables
│   └── wait-for-it.sh                      <- helper to wait for host:port service to be ready
│
├── data                                <- Project data
│   ├── clickhouse                          <- volume mount for the 'clickhouse' container
│   └── deephaven                           <- volume mount for the 'deephaven' container
│       ├── app.d                           <- Deephaven app mode config
│       ├── layouts                         <- Deephaven app layout 
│       └── notebooks                       <- Deephaven File Explorer 
│   
├── src                                 <- Python files
│   ├── script    
│   │   ├── cryptofeed_0_startup.sh         <- startup script for the 'cryptofeed' container
│   │   ├── cryptofeed_1_trades.py          <- script for trades subcriptions
│   │   └── cryptofeed_2_orderbooks.py      <- script for orderbook subcriptions
│   │ 
│   └── cryptofeed_tools.py             <- wrappers for Cryptofeed APIs
│
├── .gitignore                          <- List of files ignored by git
├── requirements.txt                    <- File for installing python dependencies
├── setup.py                            <- File for installing project as a package
└── README.md
```
## References
* ClickHouse + Kafka: https://clickhouse.com/docs/en/engines/table-engines/integrations/kafka
  * [Kafka to ClickHouse](https://clickhouse.com/docs/en/integrations/kafka#kafka-to-clickhouse)
  * [ClickHouse to Kafka](https://clickhouse.com/docs/en/integrations/kafka#clickhouse-to-kafka) [doable but we don't use it yet]

* ClickHouse + Redpanda: https://redpanda.com/blog/real-time-olap-database-clickhouse-redpanda
* [ClickHouse Server in 1 minute with Docker](https://dev.to/titronium/clickhouse-server-in-1-minute-with-docker-4gf2)
* [Clickhouse Kafka Engine Virtual Columns](https://clickhouse.com/docs/en/engines/table-engines/integrations/kafka#virtual-columns)
* Older version using QuestDB: https://github.com/kzk2000/deephaven-questdb
