#!/bin/bash

NAMESPACES='{client-mart-estate,client-mart,client-tour,client-crm,tenant-core}'

GROUPS_='{devops,support,client-flow-dev,client-crm-dev,tenant-core-dev}'

OPERATIONS=("patch resourcequotas" "create rolebindings" "create deployments" "patch configmaps" "patch deployments" "list pods")

for OPERATION in "${OPERATIONS[@]}"; do
    for GROUP in `eval echo $GROUPS_`; do
        for ENVIRONMENT in {'',-test}; do
            for NAMESPACE in `eval echo $NAMESPACES`; do 
                echo -n "can user from $GROUP $OPERATION in ${NAMESPACE}${ENVIRONMENT} namespace? "

                minikube kubectl -- auth can-i $OPERATION --as=noname --as-group=$GROUP -n ${NAMESPACE}${ENVIRONMENT}
            done
        done
    done
done

