#!/usr/bin/env python
# Copyright 2019 AstroLab Software
# Author: Abhishek Chauhan
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""For verifying the working of the distribution pipeline.
Consume the distributed alerts from the Kafka Server.

1. Read from Kafka topic(s)
2. Deserialize the avro data using the pre-defined schema
3. Carry out operations on the obtained DataFrame
"""

import argparse

from fink_broker.parser import getargs
from fink_broker.sparkUtils import init_sparksession
from fink_broker.distributionUtils import decode_kafka_df
from pyspark.sql.functions import col

def main():
    parser = argparse.ArgumentParser(description = __doc__)
    args = getargs(parser)

    # Get or create a Spark Session
    spark = init_sparksession(
        name = "consume_distribution", shuffle_partitions = 2, log_level = "ERROR")

    # Topic to read from
    topic = "distribution_test"

    # Read from the Kafka topic
    df_kafka = spark \
        .read \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9093") \
        .option("value.deserializer", "ByteArrayDeserializer") \
        .option("subscribe", topic) \
        .load()

    # Decode df_kafka into a Spark DataFrame with StructType column
    df = decode_kafka_df(df_kafka, args.distribution_schema)


    print("\nprinting the schema of the decoded df\n")
    df.printSchema()

    print("\nPrint first three rows\n")
    df.show(3)

if __name__ == "__main__":
    main()
