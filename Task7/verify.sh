#!/bin/bash

check() {
    echo "Checking insecure manifests:"

    echo

    find insecure-manifests -name '*.yaml' | sort | while read MANIFEST; do
        if minikube kubectl -- apply -f $MANIFEST; then
            echo "Applying $MANIFEST succeeded."
        else
            echo "Applying $MANIFEST failed (see error output)."
        fi

        echo
    done

    echo "Checking secure manifests:"

    echo

    find secure-manifests -name '*.yaml' | sort | while read MANIFEST; do
        if minikube kubectl -- apply -f $MANIFEST; then
            echo "Applying $MANIFEST succeeded."
        else
            echo "Applying $MANIFEST failed (see error output)."
        fi

        echo
    done

}

minikube kubectl -- create namespace audit-zone

echo

echo "* No restrictions"

echo

check

minikube kubectl -- delete namespace audit-zone

echo

echo "Setting up PSA"

echo

minikube kubectl -- apply -f ./01-create-namespace.yaml

echo

minikube kubectl -- get ns audit-zone --show-labels

echo

echo "* PSA restrictions"

echo

check

minikube kubectl -- delete namespace audit-zone

echo

echo "Setting up OPA"

echo

minikube kubectl -- create namespace audit-zone

curl https://raw.githubusercontent.com/open-policy-agent/gatekeeper/master/deploy/gatekeeper.yaml -o gatekeeper.yaml

minikube kubectl -- apply -f gatekeeper.yaml

find gatekeeper/constraint-templates/ -name '*.yaml' -exec minikube kubectl -- apply -f {} \;

until minikube kubectl -- get opahostpath,opaprivileged,opareadonlyrootfs,oparunasnonroot &>/dev/null; do
  sleep 1
done

find gatekeeper/constraints/ -name '*.yaml' -exec minikube kubectl -- apply -f {} \;

sleep 10

echo

echo "* OPA restrictions"

echo

check


