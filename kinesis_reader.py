#!/usr/bin/env python
"""
Usage: %(scriptName)s --stream-name=STREAM_NAME --limit=LIMIT

This script pulls records from AWS kinesis stream for debugging purposes.
"""
import optfunc
import boto3
import time
import json

@optfunc.run
def get_stream_data(stream_name=None, limit=2):
    client = boto3.client('kinesis')

    if stream_name:
        stream = client.describe_stream(StreamName=stream_name)['StreamDescription']

        for shard in stream['Shards']:
            print "### %s - %s"%(stream_name, shard['ShardId'])
            shard_iterator = client.get_shard_iterator(
                StreamName=stream_name,
                ShardId=shard['ShardId'],
                ShardIteratorType='TRIM_HORIZON'
            )['ShardIterator']
            out = client.get_records(ShardIterator=shard_iterator, Limit=limit)
            for record in out["Records"]:
                data = json.loads(record["Data"])
                print data
    else:
        print "Need stream name !!!"

