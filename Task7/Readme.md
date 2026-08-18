maaaah@debian:~/architect-propdevelopment/Task7$ minikube kubectl -- apply -f 01-create-namespace.yaml
namespace/audit-zone created

maaaah@debian:~/architect-propdevelopment/Task7$ minikube kubectl -- get namespaces
NAME              STATUS   AGE
audit-zone        Active   3s
default           Active   2m7s
kube-node-lease   Active   2m7s
kube-public       Active   2m7s
kube-system       Active   2m7s

minikube kubectl -- apply -f insecure-manifests/01-privileged-pod.yaml
Error from server (Forbidden): error when creating "insecure-manifests/01-privileged-pod.yaml": pods "privileged-pod" is forbidden: violates PodSecurity "restricted:latest": privileged (container "privileged-pod-nginx" must not set securityContext.privileged=true), allowPrivilegeEscalation != false (container "privileged-pod-nginx" must set securityContext.allowPrivilegeEscalation=false)

minikube kubectl -- apply -f insecure-manifests/02-hostpath-pod.yaml
Error from server (Forbidden): error when creating "insecure-manifests/02-hostpath-pod.yaml": pods "hostpath-pod" is forbidden: violates PodSecurity "restricted:latest": restricted volume types (volume "host-logs" uses restricted volume type "hostPath")

minikube kubectl -- apply -f insecure-manifests/03-root-user-pod.yaml
Error from server (Forbidden): error when creating "insecure-manifests/03-root-user-pod.yaml": pods "privileged-pod" is forbidden: violates PodSecurity "restricted:latest": allowPrivilegeEscalation != false (container "privileged-pod-nginx" must set securityContext.allowPrivilegeEscalation=false), runAsNonRoot != true (container "privileged-pod-nginx" must not set securityContext.runAsNonRoot=false), runAsUser=0 (container "privileged-pod-nginx" must not set runAsUser=0)

minikube kubectl -- delete namespace audit-zone

minikube kubectl -- create namespace audit-zone

curl https://raw.githubusercontent.com/open-policy-agent/gatekeeper/master/deploy/gatekeeper.yaml -o gatekeeper.yaml

minikube kubectl -- apply -f gatekeeper.yaml

find gatekeeper/constraint-templates/ -name '*.yaml' -exec minikube kubectl -- apply -f {} \;

find gatekeeper/constraints/ -name '*.yaml' -exec minikube kubectl -- apply -f {} \;

minikube kubectl -- apply -f insecure-manifests/01-privileged-pod.yaml
Error from server (Forbidden): error when creating "insecure-manifests/01-privileged-pod.yaml": admission webhook "validation.gatekeeper.sh" denied the request: [privileged] Security Violation: Container 'privileged-pod-nginx' is privileged. This is forbidden.

minikube kubectl -- apply -f insecure-manifests/02-hostpath-pod.yaml
Error from server (Forbidden): error when creating "insecure-manifests/02-hostpath-pod.yaml": admission webhook "validation.gatekeeper.sh" denied the request: [hostpath] Security Violation: Volume 'host-logs' uses hostPath, which is strictly forbidden.

minikube kubectl -- apply -f insecure-manifests/03-root-user-pod.yaml
Error from server (Forbidden): error when creating "insecure-manifests/03-root-user-pod.yaml": admission webhook "validation.gatekeeper.sh" denied the request: [runasnonroot] Security Violation: Container 'root-user-pod-nginx' or Pod Spec must explicitly set runAsNonRoot to true.
