import argparse
import logging
import sys

from dagorama import workflow_runnner


# Configure logging to write to standard output. 
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)  # Output to stdout instead of the default stderr
    ]
)


def main():
    parser = argparse.ArgumentParser(description="DAGorama: Tools for working with DAGs.")
    parser.add_argument('--run_workflows', action='store_true', help=".")
    
    args = parser.parse_args()
    
    if args.run_workflows:
        workflow_runnner.run_workflows()

if __name__ == "__main__":
    main()
