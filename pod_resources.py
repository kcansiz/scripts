from kubernetes import client, config

def get_deployments_for_workers_with_label_selector(label_selector):
    config.load_kube_config()

    v1 = client.CoreV1Api()

    namespaces = v1.list_namespace().items
    # Filter namespaces based on the label selector (for rke2 projects)
    filtered_namespaces = [namespaces.metadata.name for namespaces in namespaces if namespaces.metadata.labels.get(label_selector) == "p-tkqjp"]

    for namespace in filtered_namespaces:
        ret = v1.list_namespaced_pod(namespace=namespace, watch=False)
        for pod in ret.items:
            name = pod.metadata.name
            try:
                req_cpu = pod.spec.containers[0].resources.requests['cpu'] if pod.spec.containers[0].resources.requests else "N/A"
                req_mem = pod.spec.containers[0].resources.requests['memory'] if pod.spec.containers[0].resources.requests else "N/A"
                lim_cpu = pod.spec.containers[0].resources.limits['cpu'] if pod.spec.containers[0].resources.limits else "N/A"
                lim_mem = pod.spec.containers[0].resources.limits['memory'] if pod.spec.containers[0].resources.limits else "N/A"
                print(f"{name}\t{namespace}\t{req_cpu}\t{req_mem}\t{lim_cpu}\t{lim_mem}")
            except:
                print(f"{name}\t{namespace}\tResource request or limit not found for the container.")

if __name__ == "__main__":
    label_selector = "field.cattle.io/projectId"
    get_deployments_for_workers_with_label_selector(label_selector)