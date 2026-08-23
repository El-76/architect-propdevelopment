### Настройка и тестирования сетевых политик

Запускаем mnikube:

```
minikube start --cni=calico
```

Создаём пространство имён:

```
minikube kubectl -- create namespace propdevelopment
```

Запускам поды приложений:

```
minikube kubectl -- apply -f front-end-app.yaml --namespace propdevelopment
minikube kubectl -- apply -f admin-back-end-api-app.yaml --namespace propdevelopment
minikube kubectl -- apply -f admin-front-end-app.yaml --namespace propdevelopment
minikube kubectl -- apply -f back-end-api-app.yaml --namespace propdevelopment
```

Проверяем:

```
minikube kubectl -- get pods --namespace propdevelopment
NAME                                      READY   STATUS    RESTARTS   AGE
admin-back-end-api-app-5f5d4694c7-rx4v7   1/1     Running   0          5m1s
admin-front-end-app-9c45dc9ff-qs2gh       1/1     Running   0          4m59s
back-end-api-app-5fdc8d84c7-d82j7         1/1     Running   0          4m58s
front-end-app-765596b8ff-g6f8m            1/1     Running   0          5m3s
```

"Залезаем" в каждый pod и пытаемся сделать запрос к соседям с помощью curl - все запросы проходят:

```
minikube kubectl -- get pods --namespace propdevelopment | tail -n +2 | cut -d ' ' -f1 | while read POD; do minikube kubectl -- exec $POD --namespace propdevelopment -- /bin/bash -c 'for APP in {admin-back-end-api-app,admin-front-end-app,back-end-api-app,front-end-app}; do echo -n '$POD' \-\> ${APP}; curl -s http://$APP --connect-timeout 1 >/dev/null 2>&1 && echo ": OK" || echo ": FAILED"; done'; done
admin-back-end-api-app-5f5d4694c7-rx4v7 -> admin-back-end-api-app: OK
admin-back-end-api-app-5f5d4694c7-rx4v7 -> admin-front-end-app: OK
admin-back-end-api-app-5f5d4694c7-rx4v7 -> back-end-api-app: OK
admin-back-end-api-app-5f5d4694c7-rx4v7 -> front-end-app: OK
admin-front-end-app-9c45dc9ff-qs2gh -> admin-back-end-api-app: OK
admin-front-end-app-9c45dc9ff-qs2gh -> admin-front-end-app: OK
admin-front-end-app-9c45dc9ff-qs2gh -> back-end-api-app: OK
admin-front-end-app-9c45dc9ff-qs2gh -> front-end-app: OK
back-end-api-app-5fdc8d84c7-d82j7 -> admin-back-end-api-app: OK
back-end-api-app-5fdc8d84c7-d82j7 -> admin-front-end-app: OK
back-end-api-app-5fdc8d84c7-d82j7 -> back-end-api-app: OK
back-end-api-app-5fdc8d84c7-d82j7 -> front-end-app: OK
front-end-app-765596b8ff-g6f8m -> admin-back-end-api-app: OK
front-end-app-765596b8ff-g6f8m -> admin-front-end-app: OK
front-end-app-765596b8ff-g6f8m -> back-end-api-app: OK
front-end-app-765596b8ff-g6f8m -> front-end-app: OK
```

"Наклеиваем" метку role на поды - она нужна для применения сетевых политик:

```
for SVC in {admin-back-end-api,admin-front-end,back-end-api,front-end}; do minikube kubectl -- label pods -l app=${SVC} role=${SVC} --namespace propdevelopment; done
pod/admin-back-end-api-app-5f5d4694c7-rx4v7 labeled
pod/admin-front-end-app-9c45dc9ff-qs2gh labeled
pod/back-end-api-app-5fdc8d84c7-d82j7 labeled
pod/front-end-app-765596b8ff-g6f8m labeled
```

Проверяем метки:

```
minikube kubectl -- get pods -L role --namespace propdevelopment
NAME                                      READY   STATUS    RESTARTS   AGE    ROLE
admin-back-end-api-app-5f5d4694c7-rx4v7   1/1     Running   0          6m4s   admin-back-end-api
admin-front-end-app-9c45dc9ff-qs2gh       1/1     Running   0          6m2s   admin-front-end
back-end-api-app-5fdc8d84c7-d82j7         1/1     Running   0          6m1s   back-end-api
front-end-app-765596b8ff-g6f8m            1/1     Running   0          6m6s   front-end
```

Опять проверяем - само по себе назначение метки не влияет на фильтрацию трафика - все запросы проходят:

```
minikube kubectl -- get pods --namespace propdevelopment | tail -n +2 | cut -d ' ' -f1 | while read POD; do minikube kubectl -- exec $POD --namespace propdevelopment -- /bin/bash -c 'for APP in {admin-back-end-api-app,admin-front-end-app,back-end-api-app,front-end-app}; do echo -n '$POD' \-\> ${APP}; curl -s http://$APP --connect-timeout 1 >/dev/null 2>&1 && echo ": OK" || echo ": FAILED"; done'; done
admin-back-end-api-app-5f5d4694c7-rx4v7 -> admin-back-end-api-app: OK
admin-back-end-api-app-5f5d4694c7-rx4v7 -> admin-front-end-app: OK
admin-back-end-api-app-5f5d4694c7-rx4v7 -> back-end-api-app: OK
admin-back-end-api-app-5f5d4694c7-rx4v7 -> front-end-app: OK
admin-front-end-app-9c45dc9ff-qs2gh -> admin-back-end-api-app: OK
admin-front-end-app-9c45dc9ff-qs2gh -> admin-front-end-app: OK
admin-front-end-app-9c45dc9ff-qs2gh -> back-end-api-app: OK
admin-front-end-app-9c45dc9ff-qs2gh -> front-end-app: OK
back-end-api-app-5fdc8d84c7-d82j7 -> admin-back-end-api-app: OK
back-end-api-app-5fdc8d84c7-d82j7 -> admin-front-end-app: OK
back-end-api-app-5fdc8d84c7-d82j7 -> back-end-api-app: OK
back-end-api-app-5fdc8d84c7-d82j7 -> front-end-app: OK
front-end-app-765596b8ff-g6f8m -> admin-back-end-api-app: OK
front-end-app-765596b8ff-g6f8m -> admin-front-end-app: OK
front-end-app-765596b8ff-g6f8m -> back-end-api-app: OK
front-end-app-765596b8ff-g6f8m -> front-end-app: OK
```

Применяем сетевые политики:

```
minikube kubectl -- apply -f non-admin-api-allow.yaml --namespace propdevelopment
networkpolicy.networking.k8s.io/allow-frontend-to-backend created
networkpolicy.networking.k8s.io/allow-backend-to-frontend created
networkpolicy.networking.k8s.io/allow-admin-frontend-to-admin-backend created
networkpolicy.networking.k8s.io/allow-admin-backend-to-admin-frontend created
```

"Залезаем" в каждый pod и пытаемся сделать запрос к соседям с помощью curl - некоторые запросы "отваливаются" по таймауту в соответствие с настроенными политиками:

```
minikube kubectl -- get pods --namespace propdevelopment | tail -n +2 | cut -d ' ' -f1 | while read POD; do minikube kubectl -- exec $POD --namespace propdevelopment -- /bin/bash -c 'for APP in {admin-back-end-api-app,admin-front-end-app,back-end-api-app,front-end-app}; do echo -n '$POD' \-\> ${APP}; curl -s http://$APP --connect-timeout 1 >/dev/null 2>&1 && echo ": OK" || echo ": FAILED"; done'; done
admin-back-end-api-app-5f5d4694c7-rx4v7 -> admin-back-end-api-app: FAILED
admin-back-end-api-app-5f5d4694c7-rx4v7 -> admin-front-end-app: OK
admin-back-end-api-app-5f5d4694c7-rx4v7 -> back-end-api-app: FAILED
admin-back-end-api-app-5f5d4694c7-rx4v7 -> front-end-app: FAILED
admin-front-end-app-9c45dc9ff-qs2gh -> admin-back-end-api-app: OK
admin-front-end-app-9c45dc9ff-qs2gh -> admin-front-end-app: FAILED
admin-front-end-app-9c45dc9ff-qs2gh -> back-end-api-app: FAILED
admin-front-end-app-9c45dc9ff-qs2gh -> front-end-app: FAILED
back-end-api-app-5fdc8d84c7-d82j7 -> admin-back-end-api-app: FAILED
back-end-api-app-5fdc8d84c7-d82j7 -> admin-front-end-app: FAILED
back-end-api-app-5fdc8d84c7-d82j7 -> back-end-api-app: FAILED
back-end-api-app-5fdc8d84c7-d82j7 -> front-end-app: OK
front-end-app-765596b8ff-g6f8m -> admin-back-end-api-app: FAILED
front-end-app-765596b8ff-g6f8m -> admin-front-end-app: FAILED
front-end-app-765596b8ff-g6f8m -> back-end-api-app: OK
front-end-app-765596b8ff-g6f8m -> front-end-app: FAILED
```
