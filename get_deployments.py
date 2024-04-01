from kubernetes import client, config

def get_deployments_for_workers_with_label_selector(label_selector):
    config.load_kube_config()

    v1 = client.AppsV1Api()

    v1_namespace = client.CoreV1Api()
    namespaces = v1_namespace.list_namespace().items

    # Filter namespaces based on the label selector (for rke2 projects)
    filtered_namespaces = [ns.metadata.name for ns in namespaces if ns.metadata.labels.get(label_selector) == "p-tkqjp"]

    for namespace in filtered_namespaces:
        deployments = v1.list_namespaced_deployment(namespace=namespace).items
        for deployment in deployments:
            name = deployment.metadata.name
            replicas = deployment.spec.replicas if deployment.spec.replicas is not None else 0
            available_replicas = deployment.status.available_replicas if deployment.status.available_replicas is not None else 0
            print(f"Deployment: {name} in Namespace: {namespace}")
            print(f"\tReplicas: {replicas} Available Replicas: {available_replicas}")

if __name__ == "__main__":
    label_selector = "field.cattle.io/projectId"
    get_deployments_for_workers_with_label_selector(label_selector)
