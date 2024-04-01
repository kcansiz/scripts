from kubernetes import client, config

def delete_evicted_pods_in_default_namespace():
    config.load_kube_config()

    v1 = client.CoreV1Api()
    # namespaces to clean all pods
    namespaces = ["",""]

    for namespace in namespaces:
        pods = v1.list_namespaced_pod(namespace=namespace).items

        for pod in pods:
            if pod.status.phase == "Failed" and pod.status.reason == "Evicted":
                pod_name = pod.metadata.name
                v1.delete_namespaced_pod(name=pod_name, namespace=namespace, body=client.V1DeleteOptions())
                print(f"Deleted evicted pod: {pod_name} in namespace: {namespace}")

if __name__ == "__main__":
    delete_evicted_pods_in_default_namespace()
