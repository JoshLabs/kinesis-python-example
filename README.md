# kinesis-python-example
Simple script to read data from kinesis using Python boto

# Setup
```bash
pip install boto3 
pip install click
```

# Usage
```bash
python kinesis_reader.py --help
```
```bash
python kinesis_reader.py <kinesis-stream_name> --limit=<limit>
```

## Using with AWS credentials
```bash
AWS_PROFILE=<profile_name> python kinesis_reader.py <kinesis-stream_name> --limit=<limit>
```
