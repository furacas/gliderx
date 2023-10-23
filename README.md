# Gliderx

Gliderx is an automation tool that can convert subscriptions into [glider](https://github.com/nadoo/glider) configurations and start the service.

## Usage

```
docker run -d --rm --name gliderx -p 7788:1080 -v $(pwd)/gliderx-config.yaml:/app/gliderx-config.yaml furacas/gliderx
```
