I wanted to try hyperswitch, but their hyperswitch-web image was only built for arm64.. so I made a new workflow that builds it for both arm64 and amd64.. then I found their gh repo dockerfile doesn't set the sdkVersion in the tagged releases so I made this script automatically set it just before it builds the images.. This allows the hyperswitch-helm scripts to work if I change the following helm values (works with argocd too)

```
hyperswitch-web:
  autoBuild:
    buildImage: ghcr.io/centerionware/hyperswitch-web-autobuild/hyperswitch-web
```

It's all automated based on the gitVersion found in the hyperswitch-helm chart for the hyperswitch-web. It will build a new set of images every morning at 2am IF a new tag is found.

This is for kubernetes and docker.
