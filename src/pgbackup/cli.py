from argparse import Action, ArgumentParser

known_drivers = ["local", "s3"]

class DriverAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        driver, destination = values
        if driver.lower() not in known_drivers:
            parser.error(f"Unknown driver {driver}. Available drivers are: {known_drivers}")
        namespace.driver = driver.lower()
        namespace.destination = destination

def create_parser():
    parser = ArgumentParser()
    parser.add_argument("url", help="url of postgresql db to backup")
    parser.add_argument("--driver", "-d", 
            help="how and where to store the backup",
            nargs=2,
            metavar=("driver", "destination"),
            action=DriverAction,
            required=True
            )

    return parser

def main():
    import time
    import boto3
    from pgbackup import pgdump, storage

    args = create_parser().parse_args()
    dump = pgdump.dump(args.url)
    if args.driver == "s3":
        client = boto3.client("s3")
        timestamp = time.strftime("T%Y-%m-%d_%H:%M:%S", time.localtime())
        file_name = pgdump.dump_file_name(args.url, timestamp)
        print(f"Backing database up to {args.destination} in S3 as {file_name}.")
        storage.s3(client, dump.stdout, args.destination, 'example.sql')
    else:
        outfile = open(args.destination, "wb")
        print(f"Backing database up to {args.destination} locally as {file_name}.")
        storage.local(dump.stdout, outfile)