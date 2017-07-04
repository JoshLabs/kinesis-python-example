#!/usr/bin/env python
"""
Usage: %(scriptName)s --stream-name=STREAM_NAME --limit=LIMIT

This script pulls records from AWS kinesis stream for debugging purposes.
"""
import click
import boto3
import time
import json
import datetime
import time

@click.command()
@click.argument('stream_name', required=True)
@click.option('--limit', default=2, help="Number of records to pull from each available shard. Default is 2.")
@click.option('--timedelta', default=5, help="Number of minutes to look back in shard. Used with 'AT_TIMESTAMP'. Default is 5.")
def get_stream_data(stream_name, limit, timedelta):
    client = boto3.client('kinesis')

    if stream_name:
        stream = client.describe_stream(StreamName=stream_name)['StreamDescription']

        for shard in stream['Shards']:
            print "### %s - %s"%(stream_name, shard['ShardId'])
            shard_iterator = client.get_shard_iterator(
                StreamName=stream_name,
                ShardId=shard['ShardId'],
                ShardIteratorType='AT_TIMESTAMP',  #'TRIM_HORIZON'|'LATEST'
                Timestamp=datetime.datetime.utcnow() - datetime.timedelta(minutes=timedelta)
            )['ShardIterator']
            while True:
                out = client.get_records(ShardIterator=shard_iterator, Limit=limit)
                if out["Records"]:
                    for record in out["Records"]:
                        data = json.loads(record["Data"])
                        print data
                    break
                else:
                    print out
                    time.sleep(1)
    else:
        print "Need stream name !!!"

if __name__ == '__main__':
    get_stream_data()
