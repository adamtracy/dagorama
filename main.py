import argparse
import logging
import sys

from app import workflow_runnner
from app import io

# Configure logging to write to standard output.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(
            sys.stdout
        ),
        logging.FileHandler("app.log")
    ],
)


def main():
    parser = argparse.ArgumentParser(
        description="DAGorama: Tools for working with DAGs."
    )
    parser.add_argument("--run_workflows", action="store_true", help="run the workflows in ./tests/data")
    parser.add_argument("--viz_graphs", action="store_true", help="create visualizations of the graphs in ./output")

    args = parser.parse_args()

    if args.run_workflows:
        workflow_runnner.run_workflows()
    elif args.viz_graphs:
        io.viz_graphs()

if __name__ == "__main__":
    main()
