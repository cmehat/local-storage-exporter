from prometheus_client import Gauge


pv_used_bytes_gauge = Gauge(
    name="local_storage_pv_used_bytes",
    documentation="The amount of bytes used by local storage volume",
    labelnames=[
        "node_name",
        "pvc_name",
        "pvc_namespace",
        "pv_name",
        "storage_path",
        "pv_capacity",
        "storage_class_name",
    ],
)
pv_capacity_bytes_gauge = Gauge(
    name="local_storage_pv_capacity_bytes",
    documentation="The capacity of local storage volume",
    labelnames=[
        "node_name",
        "pvc_name",
        "pvc_namespace",
        "pv_name",
        "storage_path",
        "pv_capacity",
        "storage_class_name",
    ],
)

mounted_disk_used_gauge = Gauge(
    name="local_storage_mounted_disk_used_bytes",
    documentation="The amount of bytes used by mounted disk",
    labelnames=["node_name", "host_path", "volume_mount_path"],
)
mounted_disk_capacity_gauge = Gauge(
    name="local_storage_mounted_disk_capacity_bytes",
    documentation="The capacity of mounted disk",
    labelnames=["node_name", "host_path", "volume_mount_path"],
)
mounted_disk_available_gauge = Gauge(
    name="local_storage_mounted_disk_available_bytes",
    documentation="The amount of bytes available in mounted disk",
    labelnames=["node_name", "host_path", "volume_mount_path"],
)
