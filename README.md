# Swiss Army Knife for Cloud

## Tools List

```
├── dlv
│   └── amd64
│       ├── dlv-1.3.0
│       └── dlv-1.7.0
├── kubectl-exec
│   ├── kubectl-exec
│   ├── LICENSE
│   └── README.md
└── README.md
```

- dlv. [A GDB for Go.](https://github.com/go-delve/delve)
- kubectl-exec. [Bash script to attach alpine container to K8S node](https://github.com/mohatb/kubectl-exec)

## How to attach a Go process in a K8S pod

1. Run `kubectl describe pod [POD NAME] | grep Node` to get which node that K8S pod runs in.
1. Run `kubectl-exec`.
1. To find the PID of the container process, run `docker ps -q | xargs docker inspect --format '{{.State.Pid}}, {{.Name}}'  | grep process-name`.
1. Once insider alpine container, run `./dlv attach [pid]`.

See [Github issue.](https://github.com/MicrosoftDocs/azure-docs/issues/79825)
