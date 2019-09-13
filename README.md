```shell
docker run --rm -it --device /dev/gpiomem leastfixedpoint/fruit-pir-upload
```

```shell
fruit-cli container --filter /monitor/os/hostname = '"MYNODEHOSTNAME"' run \
  --device /dev/gpiomem \
  --name pir-upload-syndicate \
  leastfixedpoint/fruit-pir-upload
```
