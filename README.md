# test1_repository

1. ubuntu/Linux 타겟 설정(TCP/RDMA)
2. ubuntu/Linux 호스트 설정(TCP/RDMA)
3. ubuntu/Linux 호스트 설정 해제(통합)
4. ubuntu/Linux 타겟 설정 해제(통합)

```
git stash
git pull
git stash pop
```

1. ubuntu/Linux 타겟 설정(TCP/RDMA)
- ubuntu/Linux 타겟 설정(TCP)
```
chmod +x script/target_tcp_setup.sh
sudo ./script/target_tcp_setup.sh
```
- ubuntu/Linux 타겟 설정(RDMA)
```
chmod +x script/target_rdma_setup.sh
sudo ./script/target_rdma_setup.sh
```
2. ubuntu/Linux 호스트 설정(TCP/RDMA)
- ubuntu/Linux 호스트 설정(TCP)
```
chmod +x script/host_tcp_setup.sh
sudo ./script/host_tcp_setup.sh
```
- ubuntu/Linux 호스트 설정(RDMA)
```
chmod +x script/host_rdma_setup.sh
sudo ./script/host_rdma_setup.sh
```
3. ubuntu/Linux 호스트 설정 해제(통합)
```
chmod +x script/host_teardown.sh
sudo ./script/host_teardown.sh
```
4. ubuntu/Linux 타겟 설정 해제(통합)
```
chmod +x script/target_teardown.sh
sudo ./script/target_teardown.sh
```


```
chmod +x setup_nvmeof_target.sh
sudo ./setup_nvmeof_target.sh

chmod +x test_nvmeof_connection.sh
sudo ./test_nvmeof_connection.sh

```

```
chmod +x install_and_run_wireshark.sh
sudo ./install_and_run_wireshark.sh

sudo wireshark
```

```
chmod +x install_nvme_cli.sh
sudo ./install_nvme_cli.sh
```

```
chmod +x mount_nvme.sh
sudo ./mount_nvme.sh
```