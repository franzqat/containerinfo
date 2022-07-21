## Contaninerinfo 
This application is used to collect and analyze metrics of containers that are running in a Kubernetes cluster and what are their resource requests and limits.

## Description
This application runs in Kubernetes and is able to query the resource requests and limits for all the containers of pods with labels specified by a query parameter from all namespaces.
The results is returned as json and is an array of records, containing the namespace, pod name, container name and the resources for each container of the matching pods.

## Installation

The installation is done using an Helm Chart.
### Requirements
- You need helm installed on your machine and access to the cluster. 
- To install the chart you need an account with cluster admin permissions, in order to create the appropriate RBAC rules for this application.
- You also need a pod with the `curl` command installed in order to try the application.

### Installation

To install the chart, download the `containerinfo-0.1.0.tgz` chart from the releases [PLACEHOLDER](LINK)

After, to install the chart you need to run the following command:

> `helm upgrade --install containerinfo /path/to/chart/containerinfo-0.1.0.tgz --create-namespace -n <NAMESPACE>`

Be sure to specify the namespace where the chart will be installed and the path where the chart is located.


In case you want to use different settings for the chart, you can change the values.yaml file inside the chart and run the following command:
> `helm upgrade --install containerinfo /path/to/chart/containerinfo-0.1.0.tgz --create-namespace -n <NAMESPACE> -f /path/to/values/values.yaml`

## Usage

To use this application, you need to call the exposed service from **inside** another pod of the cluster using the command:

> `curl "http://<SERVICE_NAME>.<NAMESPACE>.svc.cluster.local:5000/container-resources?pod-label=<LABEL_QUERY>"`

The LABEL_QUERY is a string that represents the label query to be used to filter the pods. It's a **mandatory** parameter, not providing it will return an error.

It should be in the format of: `key=value`
So if you want to filter the pods by the label `app: my-app`(from the yaml), you should use the query: `app=my-app`  


For example, to get the resources of all the containers of pods with the label `app=microservices` from all namespaces, considering that the app is installed in a namespace called `label-selector` you can use the following command:

> `curl "http://containerinfo.label-selector.svc.cluster.local:5000/container-resources?pod-label=app=microservices"`

The output is a json array of records, each record will be similar to this:

```json
[
  {
    "pod_name": "example-h7rvl",
    "namespace": "example-namespace",
    "container_name": "example-container",
    "mem_req": "100Mi",
    "mem_limit": "200Mi",
    "cpu_req": "100m",
    "cpu_limit": "200m"
  },
  ...
```

To access the pod, with an account with enough permissions, you need to connect to it using the `kubectl` command.
`kubectl exec -it <POD_NAME> -n <NAMESPACE> -- /bin/bash`

## Build
I used **podman** to build the image. 
To build the image, you need to run the following command:
```
podman build . -t container-resources
podman tag localhost/container-resources <YOURACCOUNT_NAME>/containerinfo:latest
podman push <YOURACCOUNT_NAME>/containerinfo:latest
```
If you prefer to use docker, just change `podman` into `docker`.

## Roadmap
It's possible to improve this application.
One of the first goals could be to remove the files generation inside /tmp/ folder and the input directly to the jq scripts.

## License
MIT license