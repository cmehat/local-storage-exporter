import logging
import time
import os

from prometheus_client import start_http_server

from local_storage_exporter.k8s import LocalStorageExporter
from local_storage_exporter import utils


def main():
    # Set up logging and create handler for info logs
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    _logger = logging.getLogger(__name__)
    _logger.setLevel(logging.INFO)
    _logger.addHandler(handler)

    try:
        # PVs that we want to monitor should have storage class name that is in the list
        # Expect comma separated list
        storage_class_names = os.environ.get("STORAGE_CLASS_NAMES")
        storage_class_names = (
            storage_class_names.split(",") if storage_class_names else []
        )
        if storage_class_names == []:
            _logger.error("No storage class names provided. Exiting...")
            exit(1)

        # Port to expose metrics
        port = int(os.environ.get("METRICS_PORT", 9100))

        # Update interval with ms, s, m, h suffixes, no suffix means seconds
        update_interval = os.environ.get("UPDATE_INTERVAL")
        if update_interval:
            update_interval = utils.convert_str_to_seconds(update_interval)
        else:
            update_interval = 30

        _logger.info(f"Storageclass names: {storage_class_names}")
        _logger.info(f"Metrics port: {port}")
        _logger.info(f"Update interval: {update_interval} seconds")

        lse = LocalStorageExporter(storage_class_names=storage_class_names)
        start_http_server(port)  # Metrics exporter server
        _logger.info(f"Started local storage exporter on port {port}")
        while True:
            lse.update_metrics()
            time.sleep(update_interval)
    except Exception as e:
        _logger.error(f"Caught exception in main: {e}")
        raise


if __name__ == "__main__":
    main()
