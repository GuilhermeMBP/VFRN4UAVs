# VFRN4UAVs

## Using Docker
### Building
```bash
docker build -t vfrn .
```
### Running
```bash
docker run -it --gpus=all --net=host --env DISPLAY=$DISPLAY vfrn
```

### Post-run
When using vscode dev-containers verify if the cpu is going to 100%, if so try this inside the container:
```bash
ps aux | grep @vs
```
and kill the process that appears in the list