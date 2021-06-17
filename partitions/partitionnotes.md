# Build the partiton images

top-level: 
```shell
docker build -t ajymau/oltl-partitions:1 -f Dockerfile-OL-TLEx .; docker tag ajymau/oltl-partitions:1 ajymau/oltl-partitions:dev-last; docker push ajymau/oltl-partitions:dev-last
```

partition exec:
```shell
docker build -t ajymau/oltl-partitions:1 -f Dockerfile-OL-TLEx .; docker tag ajymau/oltl-partitions:1 ajymau/oltl-partitions:dev-last; docker push ajymau/oltl-partitions:dev-last
```

batch cli sidecar:
```shell
`docker build -t ajymau/batchcli:1 -f ./Dockerfile-BMgrCLI-Script .; docker tag ajymau/batchcli:1 ajymau/batchcli:dev-last; docker push ajymau/batchcli:dev-last
```

kube job create/delete:
```shell
kubectl create -f ./batchpartitionjob.yaml
kubectl delete -f ./batchpartitionjob.yaml
```