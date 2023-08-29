from kubernetes import client, config

def get_db_ip_address(service_name, namespace):
    config.load_incluster_config()

    api_client = client.CoreV1Api()

    services = api_client.list_namespaced_service(namespace).items

    for service in services:
        if service.metadata.name == service_name:
            for port in service.spec.ports:
                service_port = f'{port.port}'

            print(f"{service.spec.cluster_ip}:{service_port}")
            service_address = f"{service.spec.cluster_ip}:{service_port}"
            return service_address
    
    return None



