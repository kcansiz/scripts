import pandas as pd
from kubernetes import client, config

def get_deployments_for_workers_with_label_selector(label_selector):
    config.load_kube_config()

    v1 = client.CoreV1Api()

    namespaces = v1.list_namespace().items
    # Filter namespaces based on the label selector (for rke2 projects)
    filtered_namespaces = [namespaces.metadata.name for namespaces in namespaces if namespaces.metadata.labels.get(label_selector) == "p-tkqjp"]

    data = []
    for namespace in filtered_namespaces:
        ret = v1.list_namespaced_pod(namespace=namespace, watch=False)
        for pod in ret.items:
            name = pod.metadata.name
            try:
                req_cpu = pod.spec.containers[0].resources.requests['cpu'] if pod.spec.containers[0].resources.requests else "N/A"
                req_mem = pod.spec.containers[0].resources.requests['memory'] if pod.spec.containers[0].resources.requests else "N/A"
                lim_cpu = pod.spec.containers[0].resources.limits['cpu'] if pod.spec.containers[0].resources.limits else "N/A"
                lim_mem = pod.spec.containers[0].resources.limits['memory'] if pod.spec.containers[0].resources.limits else "N/A"
                data.append([name, namespace, req_cpu, req_mem, lim_cpu, lim_mem])
            except:
                data.append([name, namespace, "Not Found", "Not Found", "Not Found", "Not Found"])

    df = pd.DataFrame(data, columns=["Name", "Namespace", "Request CPU", "Request Memory", "Limit CPU", "Limit Memory"])
    df.to_excel("dev_quotas.xlsx", index=False)

if __name__ == "__main__":
    label_selector = "field.cattle.io/projectId"
    get_deployments_for_workers_with_label_selector(label_selector)
