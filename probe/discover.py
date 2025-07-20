from kubernetes import client, config

def discover_endpoints(label_selector):
    config.load_incluster_config()
    svc = client.CoreV1Api().list_service_for_all_namespaces(label_selector=label_selector).items[0]
    ip = svc.spec.cluster_ip
    port = svc.spec.ports[0].port
    return f"{ip}:{port}"
