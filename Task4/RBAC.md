Предположим сотрудники ровно такие как в описании задачи:

* Разработчики
* Инженеры по эксплуатации
* DevOps-инженеры

Но разработчики ещё делятся на команды (группы), которые разрабатывают:

1. client-flow-dev: client-mart-estate-app client-mart-app client-tour-app
1. client-crm-dev: client-crm-app
1. tenant-core-dev: tenant-core-app

(Предполагается, что разрабатываются своими силами и деплоятся в k8s только перечисленные выше сервисы, остальное - 3rd party).

Для них некоторые роли назначаются только для ресурсов своих сервисов, см. ниже.

Каждый сервис сконфигурирован в двух namespace - production (без суффикса) и test (с суффиксом -test).

| Роль  | Права роли | Группы пользователей |
| --- | --- | --- |
| devops | cluster-admin (например менять квоты ресурсов) для всех namespaces | DevOps-инженер |
| support | admin (например раздавать роли) для *-test namespaces, edit (например создавать deployments) - для production | инженеры по эксплуатации |
| *-dev | edit (например создавать deployments) для своих *-test namespaces, config-updater, pod-restarter, view - для всех *-test, view - для всех production, pod-restarter - для своих production | разработчики соответствующих модулей |


minikube start

find . -name '*.yaml' -exec fgrep namespace {} \; | sort -u | fgrep -v '#' | awk '{print $2;}' | while read N; do minikube kubectl -- create namespace ${N}; done
namespace/client-crm created
namespace/client-crm-test created
namespace/client-mart created
namespace/client-mart-estate created
namespace/client-mart-estate-test created
namespace/client-mart-test created
namespace/client-tour created
namespace/client-tour-test created
namespace/tenant-core created
namespace/tenant-core-test created

find . -name '*.yaml' -a -not -name 'rbac.yaml' -exec minikube kubectl -- apply -f {} \;
deployment.apps/client-crm-app created
service/client-crm-app created
deployment.apps/client-tour-app created
service/client-tour-app created
deployment.apps/client-crm-app created
service/client-crm-app created
deployment.apps/client-mart-app created
service/client-mart-app created
deployment.apps/client-mart-estate-app created
service/client-mart-estate-app created
deployment.apps/tenant-core-app created
service/tenant-core-app created
deployment.apps/client-mart-estate-app created
service/client-mart-estate-app created
deployment.apps/client-mart-app created
service/client-mart-app created
deployment.apps/client-tour-app created
service/client-tour-app created
deployment.apps/tenant-core-app created
service/tenant-core-app created

minikube kubectl -- get pods -A
NAMESPACE                 NAME                                     READY   STATUS    RESTARTS        AGE
client-crm-test           client-crm-app-575789496f-ccbxs          1/1     Running   0               70s
client-crm                client-crm-app-575789496f-6b2lm          1/1     Running   0               73s
client-mart-estate-test   client-mart-estate-app-f449589d7-dw8r5   1/1     Running   0               62s
client-mart-estate        client-mart-estate-app-f449589d7-c6x5d   1/1     Running   0               66s
client-mart-test          client-mart-app-6bc45d6787-cztt4         1/1     Running   0               68s
client-mart               client-mart-app-6bc45d6787-bslbr         1/1     Running   0               59s
client-tour-test          client-tour-app-549767d74c-gjgt7         1/1     Running   0               72s
client-tour               client-tour-app-549767d74c-9lshb         1/1     Running   0               57s
kube-system               coredns-7d764666f9-pdlwz                 1/1     Running   0               4m43s
kube-system               coredns-7d764666f9-rp2qn                 1/1     Running   0               4m43s
kube-system               etcd-minikube                            1/1     Running   0               4m50s
kube-system               kube-apiserver-minikube                  1/1     Running   0               4m49s
kube-system               kube-controller-manager-minikube         1/1     Running   0               4m49s
kube-system               kube-proxy-jmws5                         1/1     Running   0               4m44s
kube-system               kube-scheduler-minikube                  1/1     Running   0               4m54s
kube-system               storage-provisioner                      1/1     Running   1 (4m15s ago)   4m42s
tenant-core-test          tenant-core-app-7486f5f58c-gcvf9         1/1     Running   0               64s
tenant-core               tenant-core-app-7486f5f58c-cdp42         1/1     Running   0               55s


minikube kubectl -- apply -f rbac.yaml
clusterrole.rbac.authorization.k8s.io/pod-restarter created
clusterrole.rbac.authorization.k8s.io/config-updater created
clusterrolebinding.rbac.authorization.k8s.io/devops-global-cluster-admin created
rolebinding.rbac.authorization.k8s.io/support-client-mart-estate-edit created
rolebinding.rbac.authorization.k8s.io/support-client-mart-estate-test-admin created
rolebinding.rbac.authorization.k8s.io/support-client-mart-edit created
rolebinding.rbac.authorization.k8s.io/support-client-mart-test-admin created
rolebinding.rbac.authorization.k8s.io/support-client-tour-edit created
rolebinding.rbac.authorization.k8s.io/support-client-tour-test-admin created
rolebinding.rbac.authorization.k8s.io/support-client-crm-edit created
rolebinding.rbac.authorization.k8s.io/support-client-crm-test-admin created
rolebinding.rbac.authorization.k8s.io/support-tenant-core-edit created
rolebinding.rbac.authorization.k8s.io/support-tenant-core-test-admin created
rolebinding.rbac.authorization.k8s.io/client-flow-dev-client-mart-estate-test-edit created
rolebinding.rbac.authorization.k8s.io/client-flow-dev-client-mart-test-edit created
rolebinding.rbac.authorization.k8s.io/client-flow-dev-client-tour-test-edit created
rolebinding.rbac.authorization.k8s.io/client-crm-dev-client-crm-test-edit created
rolebinding.rbac.authorization.k8s.io/tenant-core-dev-tenant-core-test-edit created
rolebinding.rbac.authorization.k8s.io/client-flow-dev-client-mart-estate-test-config-updater created
rolebinding.rbac.authorization.k8s.io/client-flow-dev-client-mart-estate-test-pod-restarter created
rolebinding.rbac.authorization.k8s.io/client-flow-dev-client-mart-estate-test-view created
rolebinding.rbac.authorization.k8s.io/client-crm-dev-client-mart-estate-test-config-updater created
rolebinding.rbac.authorization.k8s.io/client-crm-dev-client-mart-estate-test-pod-restarter created
rolebinding.rbac.authorization.k8s.io/client-crm-dev-client-mart-estate-test-view created
rolebinding.rbac.authorization.k8s.io/tenant-core-dev-client-mart-estate-test-config-updater created
rolebinding.rbac.authorization.k8s.io/tenant-core-dev-client-mart-estate-test-pod-restarter created
rolebinding.rbac.authorization.k8s.io/tenant-core-dev-client-mart-estate-test-view created
rolebinding.rbac.authorization.k8s.io/client-flow-dev-client-mart-test-config-updater created
rolebinding.rbac.authorization.k8s.io/client-flow-dev-client-mart-test-pod-restarter created
rolebinding.rbac.authorization.k8s.io/client-flow-dev-client-mart-test-view created
rolebinding.rbac.authorization.k8s.io/client-crm-dev-client-mart-test-config-updater created
rolebinding.rbac.authorization.k8s.io/client-crm-dev-client-mart-test-pod-restarter created
rolebinding.rbac.authorization.k8s.io/client-crm-dev-client-mart-test-view created
rolebinding.rbac.authorization.k8s.io/tenant-core-dev-client-mart-test-config-updater created
rolebinding.rbac.authorization.k8s.io/tenant-core-dev-client-mart-test-pod-restarter created
rolebinding.rbac.authorization.k8s.io/tenant-core-dev-client-mart-test-view created
rolebinding.rbac.authorization.k8s.io/client-flow-dev-client-tour-test-config-updater created
rolebinding.rbac.authorization.k8s.io/client-flow-dev-client-tour-test-pod-restarter created
rolebinding.rbac.authorization.k8s.io/client-flow-dev-client-tour-test-view created
rolebinding.rbac.authorization.k8s.io/client-crm-dev-client-tour-test-config-updater created
rolebinding.rbac.authorization.k8s.io/client-crm-dev-client-tour-test-pod-restarter created
rolebinding.rbac.authorization.k8s.io/client-crm-dev-client-tour-test-view created
rolebinding.rbac.authorization.k8s.io/tenant-core-dev-client-tour-test-config-updater created
rolebinding.rbac.authorization.k8s.io/tenant-core-dev-client-tour-test-pod-restarter created
rolebinding.rbac.authorization.k8s.io/tenant-core-dev-client-tour-test-view created
rolebinding.rbac.authorization.k8s.io/client-flow-dev-client-crm-test-config-updater created
rolebinding.rbac.authorization.k8s.io/client-flow-dev-client-crm-test-pod-restarter created
rolebinding.rbac.authorization.k8s.io/client-flow-dev-client-crm-test-view created
rolebinding.rbac.authorization.k8s.io/client-crm-dev-client-crm-test-config-updater created
rolebinding.rbac.authorization.k8s.io/client-crm-dev-client-crm-test-pod-restarter created
rolebinding.rbac.authorization.k8s.io/client-crm-dev-client-crm-test-view created
rolebinding.rbac.authorization.k8s.io/tenant-core-dev-client-crm-test-config-updater created
rolebinding.rbac.authorization.k8s.io/tenant-core-dev-client-crm-test-pod-restarter created
rolebinding.rbac.authorization.k8s.io/tenant-core-dev-client-crm-test-view created
rolebinding.rbac.authorization.k8s.io/client-flow-dev-tenant-core-test-config-updater created
rolebinding.rbac.authorization.k8s.io/client-flow-dev-tenant-core-test-pod-restarter created
rolebinding.rbac.authorization.k8s.io/client-flow-dev-tenant-core-test-view created
rolebinding.rbac.authorization.k8s.io/client-crm-dev-tenant-core-test-config-updater created
rolebinding.rbac.authorization.k8s.io/client-crm-dev-tenant-core-test-pod-restarter created
rolebinding.rbac.authorization.k8s.io/client-crm-dev-tenant-core-test-view created
rolebinding.rbac.authorization.k8s.io/tenant-core-dev-tenant-core-test-config-updater created
rolebinding.rbac.authorization.k8s.io/tenant-core-dev-tenant-core-test-pod-restarter created
rolebinding.rbac.authorization.k8s.io/tenant-core-dev-tenant-core-test-view created
rolebinding.rbac.authorization.k8s.io/client-flow-dev-client-mart-estate-view created
rolebinding.rbac.authorization.k8s.io/client-flow-dev-client-mart-view created
rolebinding.rbac.authorization.k8s.io/client-flow-dev-client-tour-view created
rolebinding.rbac.authorization.k8s.io/client-crm-dev-client-crm-view created
rolebinding.rbac.authorization.k8s.io/tenant-core-dev-tenant-core-view created
rolebinding.rbac.authorization.k8s.io/client-flow-dev-client-mart-estate-pod-restarter created
rolebinding.rbac.authorization.k8s.io/client-flow-dev-client-mart-pod-restarter created
rolebinding.rbac.authorization.k8s.io/client-flow-dev-client-tour-pod-restarter created
rolebinding.rbac.authorization.k8s.io/client-crm-dev-client-crm-pod-restarter created
rolebinding.rbac.authorization.k8s.io/tenant-core-dev-tenant-core-pod-restarter created

./check-rbac.sh
can user from devops patch resourcequotas in client-mart-estate namespace? yes
can user from devops patch resourcequotas in client-mart namespace? yes
can user from devops patch resourcequotas in client-tour namespace? yes
can user from devops patch resourcequotas in client-crm namespace? yes
can user from devops patch resourcequotas in tenant-core namespace? yes
can user from devops patch resourcequotas in client-mart-estate-test namespace? yes
can user from devops patch resourcequotas in client-mart-test namespace? yes
can user from devops patch resourcequotas in client-tour-test namespace? yes
can user from devops patch resourcequotas in client-crm-test namespace? yes
can user from devops patch resourcequotas in tenant-core-test namespace? yes
can user from support patch resourcequotas in client-mart-estate namespace? no
can user from support patch resourcequotas in client-mart namespace? no
can user from support patch resourcequotas in client-tour namespace? no
can user from support patch resourcequotas in client-crm namespace? no
can user from support patch resourcequotas in tenant-core namespace? no
can user from support patch resourcequotas in client-mart-estate-test namespace? no
can user from support patch resourcequotas in client-mart-test namespace? no
can user from support patch resourcequotas in client-tour-test namespace? no
can user from support patch resourcequotas in client-crm-test namespace? no
can user from support patch resourcequotas in tenant-core-test namespace? no
can user from client-flow-dev patch resourcequotas in client-mart-estate namespace? no
can user from client-flow-dev patch resourcequotas in client-mart namespace? no
can user from client-flow-dev patch resourcequotas in client-tour namespace? no
can user from client-flow-dev patch resourcequotas in client-crm namespace? no
can user from client-flow-dev patch resourcequotas in tenant-core namespace? no
can user from client-flow-dev patch resourcequotas in client-mart-estate-test namespace? no
can user from client-flow-dev patch resourcequotas in client-mart-test namespace? no
can user from client-flow-dev patch resourcequotas in client-tour-test namespace? no
can user from client-flow-dev patch resourcequotas in client-crm-test namespace? no
can user from client-flow-dev patch resourcequotas in tenant-core-test namespace? no
can user from client-crm-dev patch resourcequotas in client-mart-estate namespace? no
can user from client-crm-dev patch resourcequotas in client-mart namespace? no
can user from client-crm-dev patch resourcequotas in client-tour namespace? no
can user from client-crm-dev patch resourcequotas in client-crm namespace? no
can user from client-crm-dev patch resourcequotas in tenant-core namespace? no
can user from client-crm-dev patch resourcequotas in client-mart-estate-test namespace? no
can user from client-crm-dev patch resourcequotas in client-mart-test namespace? no
can user from client-crm-dev patch resourcequotas in client-tour-test namespace? no
can user from client-crm-dev patch resourcequotas in client-crm-test namespace? no
can user from client-crm-dev patch resourcequotas in tenant-core-test namespace? no
can user from tenant-core-dev patch resourcequotas in client-mart-estate namespace? no
can user from tenant-core-dev patch resourcequotas in client-mart namespace? no
can user from tenant-core-dev patch resourcequotas in client-tour namespace? no
can user from tenant-core-dev patch resourcequotas in client-crm namespace? no
can user from tenant-core-dev patch resourcequotas in tenant-core namespace? no
can user from tenant-core-dev patch resourcequotas in client-mart-estate-test namespace? no
can user from tenant-core-dev patch resourcequotas in client-mart-test namespace? no
can user from tenant-core-dev patch resourcequotas in client-tour-test namespace? no
can user from tenant-core-dev patch resourcequotas in client-crm-test namespace? no
can user from tenant-core-dev patch resourcequotas in tenant-core-test namespace? no
can user from devops create rolebindings in client-mart-estate namespace? yes
can user from devops create rolebindings in client-mart namespace? yes
can user from devops create rolebindings in client-tour namespace? yes
can user from devops create rolebindings in client-crm namespace? yes
can user from devops create rolebindings in tenant-core namespace? yes
can user from devops create rolebindings in client-mart-estate-test namespace? yes
can user from devops create rolebindings in client-mart-test namespace? yes
can user from devops create rolebindings in client-tour-test namespace? yes
can user from devops create rolebindings in client-crm-test namespace? yes
can user from devops create rolebindings in tenant-core-test namespace? yes
can user from support create rolebindings in client-mart-estate namespace? no
can user from support create rolebindings in client-mart namespace? no
can user from support create rolebindings in client-tour namespace? no
can user from support create rolebindings in client-crm namespace? no
can user from support create rolebindings in tenant-core namespace? no
can user from support create rolebindings in client-mart-estate-test namespace? yes
can user from support create rolebindings in client-mart-test namespace? yes
can user from support create rolebindings in client-tour-test namespace? yes
can user from support create rolebindings in client-crm-test namespace? yes
can user from support create rolebindings in tenant-core-test namespace? yes
can user from client-flow-dev create rolebindings in client-mart-estate namespace? no
can user from client-flow-dev create rolebindings in client-mart namespace? no
can user from client-flow-dev create rolebindings in client-tour namespace? no
can user from client-flow-dev create rolebindings in client-crm namespace? no
can user from client-flow-dev create rolebindings in tenant-core namespace? no
can user from client-flow-dev create rolebindings in client-mart-estate-test namespace? no
can user from client-flow-dev create rolebindings in client-mart-test namespace? no
can user from client-flow-dev create rolebindings in client-tour-test namespace? no
can user from client-flow-dev create rolebindings in client-crm-test namespace? no
can user from client-flow-dev create rolebindings in tenant-core-test namespace? no
can user from client-crm-dev create rolebindings in client-mart-estate namespace? no
can user from client-crm-dev create rolebindings in client-mart namespace? no
can user from client-crm-dev create rolebindings in client-tour namespace? no
can user from client-crm-dev create rolebindings in client-crm namespace? no
can user from client-crm-dev create rolebindings in tenant-core namespace? no
can user from client-crm-dev create rolebindings in client-mart-estate-test namespace? no
can user from client-crm-dev create rolebindings in client-mart-test namespace? no
can user from client-crm-dev create rolebindings in client-tour-test namespace? no
can user from client-crm-dev create rolebindings in client-crm-test namespace? no
can user from client-crm-dev create rolebindings in tenant-core-test namespace? no
can user from tenant-core-dev create rolebindings in client-mart-estate namespace? no
can user from tenant-core-dev create rolebindings in client-mart namespace? no
can user from tenant-core-dev create rolebindings in client-tour namespace? no
can user from tenant-core-dev create rolebindings in client-crm namespace? no
can user from tenant-core-dev create rolebindings in tenant-core namespace? no
can user from tenant-core-dev create rolebindings in client-mart-estate-test namespace? no
can user from tenant-core-dev create rolebindings in client-mart-test namespace? no
can user from tenant-core-dev create rolebindings in client-tour-test namespace? no
can user from tenant-core-dev create rolebindings in client-crm-test namespace? no
can user from tenant-core-dev create rolebindings in tenant-core-test namespace? no
can user from devops create deployments in client-mart-estate namespace? yes
can user from devops create deployments in client-mart namespace? yes
can user from devops create deployments in client-tour namespace? yes
can user from devops create deployments in client-crm namespace? yes
can user from devops create deployments in tenant-core namespace? yes
can user from devops create deployments in client-mart-estate-test namespace? yes
can user from devops create deployments in client-mart-test namespace? yes
can user from devops create deployments in client-tour-test namespace? yes
can user from devops create deployments in client-crm-test namespace? yes
can user from devops create deployments in tenant-core-test namespace? yes
can user from support create deployments in client-mart-estate namespace? yes
can user from support create deployments in client-mart namespace? yes
can user from support create deployments in client-tour namespace? yes
can user from support create deployments in client-crm namespace? yes
can user from support create deployments in tenant-core namespace? yes
can user from support create deployments in client-mart-estate-test namespace? yes
can user from support create deployments in client-mart-test namespace? yes
can user from support create deployments in client-tour-test namespace? yes
can user from support create deployments in client-crm-test namespace? yes
can user from support create deployments in tenant-core-test namespace? yes
can user from client-flow-dev create deployments in client-mart-estate namespace? no
can user from client-flow-dev create deployments in client-mart namespace? no
can user from client-flow-dev create deployments in client-tour namespace? no
can user from client-flow-dev create deployments in client-crm namespace? no
can user from client-flow-dev create deployments in tenant-core namespace? no
can user from client-flow-dev create deployments in client-mart-estate-test namespace? yes
can user from client-flow-dev create deployments in client-mart-test namespace? yes
can user from client-flow-dev create deployments in client-tour-test namespace? yes
can user from client-flow-dev create deployments in client-crm-test namespace? no
can user from client-flow-dev create deployments in tenant-core-test namespace? no
can user from client-crm-dev create deployments in client-mart-estate namespace? no
can user from client-crm-dev create deployments in client-mart namespace? no
can user from client-crm-dev create deployments in client-tour namespace? no
can user from client-crm-dev create deployments in client-crm namespace? no
can user from client-crm-dev create deployments in tenant-core namespace? no
can user from client-crm-dev create deployments in client-mart-estate-test namespace? no
can user from client-crm-dev create deployments in client-mart-test namespace? no
can user from client-crm-dev create deployments in client-tour-test namespace? no
can user from client-crm-dev create deployments in client-crm-test namespace? yes
can user from client-crm-dev create deployments in tenant-core-test namespace? no
can user from tenant-core-dev create deployments in client-mart-estate namespace? no
can user from tenant-core-dev create deployments in client-mart namespace? no
can user from tenant-core-dev create deployments in client-tour namespace? no
can user from tenant-core-dev create deployments in client-crm namespace? no
can user from tenant-core-dev create deployments in tenant-core namespace? no
can user from tenant-core-dev create deployments in client-mart-estate-test namespace? no
can user from tenant-core-dev create deployments in client-mart-test namespace? no
can user from tenant-core-dev create deployments in client-tour-test namespace? no
can user from tenant-core-dev create deployments in client-crm-test namespace? no
can user from tenant-core-dev create deployments in tenant-core-test namespace? yes
can user from devops patch configmaps in client-mart-estate namespace? yes
can user from devops patch configmaps in client-mart namespace? yes
can user from devops patch configmaps in client-tour namespace? yes
can user from devops patch configmaps in client-crm namespace? yes
can user from devops patch configmaps in tenant-core namespace? yes
can user from devops patch configmaps in client-mart-estate-test namespace? yes
can user from devops patch configmaps in client-mart-test namespace? yes
can user from devops patch configmaps in client-tour-test namespace? yes
can user from devops patch configmaps in client-crm-test namespace? yes
can user from devops patch configmaps in tenant-core-test namespace? yes
can user from support patch configmaps in client-mart-estate namespace? yes
can user from support patch configmaps in client-mart namespace? yes
can user from support patch configmaps in client-tour namespace? yes
can user from support patch configmaps in client-crm namespace? yes
can user from support patch configmaps in tenant-core namespace? yes
can user from support patch configmaps in client-mart-estate-test namespace? yes
can user from support patch configmaps in client-mart-test namespace? yes
can user from support patch configmaps in client-tour-test namespace? yes
can user from support patch configmaps in client-crm-test namespace? yes
can user from support patch configmaps in tenant-core-test namespace? yes
can user from client-flow-dev patch configmaps in client-mart-estate namespace? no
can user from client-flow-dev patch configmaps in client-mart namespace? no
can user from client-flow-dev patch configmaps in client-tour namespace? no
can user from client-flow-dev patch configmaps in client-crm namespace? no
can user from client-flow-dev patch configmaps in tenant-core namespace? no
can user from client-flow-dev patch configmaps in client-mart-estate-test namespace? yes
can user from client-flow-dev patch configmaps in client-mart-test namespace? yes
can user from client-flow-dev patch configmaps in client-tour-test namespace? yes
can user from client-flow-dev patch configmaps in client-crm-test namespace? yes
can user from client-flow-dev patch configmaps in tenant-core-test namespace? yes
can user from client-crm-dev patch configmaps in client-mart-estate namespace? no
can user from client-crm-dev patch configmaps in client-mart namespace? no
can user from client-crm-dev patch configmaps in client-tour namespace? no
can user from client-crm-dev patch configmaps in client-crm namespace? no
can user from client-crm-dev patch configmaps in tenant-core namespace? no
can user from client-crm-dev patch configmaps in client-mart-estate-test namespace? yes
can user from client-crm-dev patch configmaps in client-mart-test namespace? yes
can user from client-crm-dev patch configmaps in client-tour-test namespace? yes
can user from client-crm-dev patch configmaps in client-crm-test namespace? yes
can user from client-crm-dev patch configmaps in tenant-core-test namespace? yes
can user from tenant-core-dev patch configmaps in client-mart-estate namespace? no
can user from tenant-core-dev patch configmaps in client-mart namespace? no
can user from tenant-core-dev patch configmaps in client-tour namespace? no
can user from tenant-core-dev patch configmaps in client-crm namespace? no
can user from tenant-core-dev patch configmaps in tenant-core namespace? no
can user from tenant-core-dev patch configmaps in client-mart-estate-test namespace? yes
can user from tenant-core-dev patch configmaps in client-mart-test namespace? yes
can user from tenant-core-dev patch configmaps in client-tour-test namespace? yes
can user from tenant-core-dev patch configmaps in client-crm-test namespace? yes
can user from tenant-core-dev patch configmaps in tenant-core-test namespace? yes
can user from devops patch deployments in client-mart-estate namespace? yes
can user from devops patch deployments in client-mart namespace? yes
can user from devops patch deployments in client-tour namespace? yes
can user from devops patch deployments in client-crm namespace? yes
can user from devops patch deployments in tenant-core namespace? yes
can user from devops patch deployments in client-mart-estate-test namespace? yes
can user from devops patch deployments in client-mart-test namespace? yes
can user from devops patch deployments in client-tour-test namespace? yes
can user from devops patch deployments in client-crm-test namespace? yes
can user from devops patch deployments in tenant-core-test namespace? yes
can user from support patch deployments in client-mart-estate namespace? yes
can user from support patch deployments in client-mart namespace? yes
can user from support patch deployments in client-tour namespace? yes
can user from support patch deployments in client-crm namespace? yes
can user from support patch deployments in tenant-core namespace? yes
can user from support patch deployments in client-mart-estate-test namespace? yes
can user from support patch deployments in client-mart-test namespace? yes
can user from support patch deployments in client-tour-test namespace? yes
can user from support patch deployments in client-crm-test namespace? yes
can user from support patch deployments in tenant-core-test namespace? yes
can user from client-flow-dev patch deployments in client-mart-estate namespace? yes
can user from client-flow-dev patch deployments in client-mart namespace? yes
can user from client-flow-dev patch deployments in client-tour namespace? yes
can user from client-flow-dev patch deployments in client-crm namespace? no
can user from client-flow-dev patch deployments in tenant-core namespace? no
can user from client-flow-dev patch deployments in client-mart-estate-test namespace? yes
can user from client-flow-dev patch deployments in client-mart-test namespace? yes
can user from client-flow-dev patch deployments in client-tour-test namespace? yes
can user from client-flow-dev patch deployments in client-crm-test namespace? yes
can user from client-flow-dev patch deployments in tenant-core-test namespace? yes
can user from client-crm-dev patch deployments in client-mart-estate namespace? no
can user from client-crm-dev patch deployments in client-mart namespace? no
can user from client-crm-dev patch deployments in client-tour namespace? no
can user from client-crm-dev patch deployments in client-crm namespace? yes
can user from client-crm-dev patch deployments in tenant-core namespace? no
can user from client-crm-dev patch deployments in client-mart-estate-test namespace? yes
can user from client-crm-dev patch deployments in client-mart-test namespace? yes
can user from client-crm-dev patch deployments in client-tour-test namespace? yes
can user from client-crm-dev patch deployments in client-crm-test namespace? yes
can user from client-crm-dev patch deployments in tenant-core-test namespace? yes
can user from tenant-core-dev patch deployments in client-mart-estate namespace? no
can user from tenant-core-dev patch deployments in client-mart namespace? no
can user from tenant-core-dev patch deployments in client-tour namespace? no
can user from tenant-core-dev patch deployments in client-crm namespace? no
can user from tenant-core-dev patch deployments in tenant-core namespace? yes
can user from tenant-core-dev patch deployments in client-mart-estate-test namespace? yes
can user from tenant-core-dev patch deployments in client-mart-test namespace? yes
can user from tenant-core-dev patch deployments in client-tour-test namespace? yes
can user from tenant-core-dev patch deployments in client-crm-test namespace? yes
can user from tenant-core-dev patch deployments in tenant-core-test namespace? yes
can user from devops list pods in client-mart-estate namespace? yes
can user from devops list pods in client-mart namespace? yes
can user from devops list pods in client-tour namespace? yes
can user from devops list pods in client-crm namespace? yes
can user from devops list pods in tenant-core namespace? yes
can user from devops list pods in client-mart-estate-test namespace? yes
can user from devops list pods in client-mart-test namespace? yes
can user from devops list pods in client-tour-test namespace? yes
can user from devops list pods in client-crm-test namespace? yes
can user from devops list pods in tenant-core-test namespace? yes
can user from support list pods in client-mart-estate namespace? yes
can user from support list pods in client-mart namespace? yes
can user from support list pods in client-tour namespace? yes
can user from support list pods in client-crm namespace? yes
can user from support list pods in tenant-core namespace? yes
can user from support list pods in client-mart-estate-test namespace? yes
can user from support list pods in client-mart-test namespace? yes
can user from support list pods in client-tour-test namespace? yes
can user from support list pods in client-crm-test namespace? yes
can user from support list pods in tenant-core-test namespace? yes
can user from client-flow-dev list pods in client-mart-estate namespace? yes
can user from client-flow-dev list pods in client-mart namespace? yes
can user from client-flow-dev list pods in client-tour namespace? yes
can user from client-flow-dev list pods in client-crm namespace? yes
can user from client-flow-dev list pods in tenant-core namespace? yes
can user from client-flow-dev list pods in client-mart-estate-test namespace? yes
can user from client-flow-dev list pods in client-mart-test namespace? yes
can user from client-flow-dev list pods in client-tour-test namespace? yes
can user from client-flow-dev list pods in client-crm-test namespace? yes
can user from client-flow-dev list pods in tenant-core-test namespace? yes
can user from client-crm-dev list pods in client-mart-estate namespace? yes
can user from client-crm-dev list pods in client-mart namespace? yes
can user from client-crm-dev list pods in client-tour namespace? yes
can user from client-crm-dev list pods in client-crm namespace? yes
can user from client-crm-dev list pods in tenant-core namespace? yes
can user from client-crm-dev list pods in client-mart-estate-test namespace? yes
can user from client-crm-dev list pods in client-mart-test namespace? yes
can user from client-crm-dev list pods in client-tour-test namespace? yes
can user from client-crm-dev list pods in client-crm-test namespace? yes
can user from client-crm-dev list pods in tenant-core-test namespace? yes
can user from tenant-core-dev list pods in client-mart-estate namespace? yes
can user from tenant-core-dev list pods in client-mart namespace? yes
can user from tenant-core-dev list pods in client-tour namespace? yes
can user from tenant-core-dev list pods in client-crm namespace? yes
can user from tenant-core-dev list pods in tenant-core namespace? yes
can user from tenant-core-dev list pods in client-mart-estate-test namespace? yes
can user from tenant-core-dev list pods in client-mart-test namespace? yes
can user from tenant-core-dev list pods in client-tour-test namespace? yes
can user from tenant-core-dev list pods in client-crm-test namespace? yes
can user from tenant-core-dev list pods in tenant-core-test namespace? yes
