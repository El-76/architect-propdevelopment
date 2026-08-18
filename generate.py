groups_to_namespaces = {
    'client-flow-dev': ['client-mart-estate', 'client-mart', 'client-tour'],
    'client-crm-dev': ['client-crm'],
    'tenant-core-dev': ['tenant-core']
}

namespaces = [v for vs in groups_to_namespaces.values() for v in vs]

print('# support')

print()

print('# admin для *-test namespaces, edit - для production')

print()

for namespace in namespaces:
    for environment, role in {'': 'edit', '-test': 'admin'}.items():
        print('apiVersion: rbac.authorization.k8s.io/v1')
        print('kind: RoleBinding')
        print('metadata:')
        print(f'  name: support-{namespace}{environment}-{role}')
        print(f'  namespace: {namespace}{environment}')
        print('subjects:')
        print('  - kind: Group')
        print(f'    name: support')
        print('    apiGroup: rbac.authorization.k8s.io')
        print('roleRef:')
        print('  kind: ClusterRole')
        print(f'  name: {role}')
        print('  apiGroup: rbac.authorization.k8s.io')
        print('---')
        print()

print()

print('# *-dev')

print()

print('# edit для своих *-test namespaces')

print()

for group in groups_to_namespaces:
    for namespace in groups_to_namespaces[group]:
        print('apiVersion: rbac.authorization.k8s.io/v1')
        print('kind: RoleBinding')
        print('metadata:')
        print(f'  name: {group}-{namespace}-test-edit')
        print(f'  namespace: {namespace}-test')
        print('subjects:')
        print('  - kind: Group')
        print(f'    name: {group}')
        print('    apiGroup: rbac.authorization.k8s.io')
        print('roleRef:')
        print('  kind: ClusterRole')
        print('  name: edit')
        print('  apiGroup: rbac.authorization.k8s.io')
        print('---')
        print()

print()

print('# config-updater, pod-restarter, view - для всех *-test')

print()

for namespace in namespaces:
    for group in groups_to_namespaces: 
        for role in ['config-updater', 'pod-restarter', 'view']:
            print('apiVersion: rbac.authorization.k8s.io/v1')
            print('kind: RoleBinding')
            print('metadata:')
            print(f'  name: {group}-{namespace}-test-{role}')
            print(f'  namespace: {namespace}-test')
            print('subjects:')
            print('  - kind: Group')
            print(f'    name: {group}')
            print('    apiGroup: rbac.authorization.k8s.io')
            print('roleRef:')
            print('  kind: ClusterRole')
            print(f'  name: {role}')
            print('  apiGroup: rbac.authorization.k8s.io')
            print('---')
            print()

print()

print('# view - для production')

print()

for namespace in namespaces:
    for group in groups_to_namespaces:
        print('apiVersion: rbac.authorization.k8s.io/v1')
        print('kind: RoleBinding')
        print('metadata:')
        print(f'  name: {group}-{namespace}-view')
        print(f'  namespace: {namespace}')
        print('subjects:')
        print('  - kind: Group')
        print(f'    name: {group}')
        print('    apiGroup: rbac.authorization.k8s.io')
        print('roleRef:')
        print('  kind: ClusterRole')
        print('  name: view')
        print('  apiGroup: rbac.authorization.k8s.io')
        print('---')
        print()

print()

print('# pod-restarter - для своих production')

print()

for group in groups_to_namespaces:
    for namespace in groups_to_namespaces[group]:
        print('apiVersion: rbac.authorization.k8s.io/v1')
        print('kind: RoleBinding')
        print('metadata:')
        print(f'  name: {group}-{namespace}-pod-restarter')
        print(f'  namespace: {namespace}')
        print('subjects:')
        print('  - kind: Group')
        print(f'    name: {group}')
        print('    apiGroup: rbac.authorization.k8s.io')
        print('roleRef:')
        print('  kind: ClusterRole')
        print('  name: pod-restarter')
        print('  apiGroup: rbac.authorization.k8s.io')
        print('---')
        print()
