---
title: "Secure Sensu"
linkTitle: "Secure Sensu"
guide_title: "Secure Sensu"
type: "guide"
description: "As with all software, it’s important to minimize any attack surface exposed by the software. Sensu is no different. Learn about the components that need to be secured and how to secure them."
weight: 60
version: "6.2"
product: "Sensu Go"
platformContent: false
menu:
  sensu-go-6.2:
    parent: deploy-sensu
---

As with any piece of software, it is critical to minimize any attack surface the software exposes.
Sensu is no different.

This reference describes the components you need to secure to make Sensu production-ready, including etcd peer communication, the Sensu API and web UI, and Sensu agent-to-server communication.
It also describes agent mutual transport layer security (mTLS) authentication, which is required for [secrets management][1].

Before you can secure Sensu, you must [generate the certificates][12] you will need.
After you generate certificates, follow this reference to secure Sensu for production.

## Secure etcd peer communication

{{% notice warning %}}
**WARNING**: You must update the default configuration for Sensu's embedded etcd with an explicit, non-default configuration to secure etcd communication in transit.
If you do not properly configure secure etcd communication, your Sensu configuration will be vulnerable to unauthorized manipulation via etcd client connections.
{{% /notice %}}

To properly secure etcd communication, replace the default parameter values in your backend store configuration in `/etc/sensu/backend.yml` as follows:

1. Replace the placeholder with the path to your certificate and key for the `etcd-cert-file` and `etcd-key-file` to secure client communication:
{{< code yml >}}
etcd-cert-file: "/path/to/your/cert"
etcd-key-file: "/path/to/your/key"
{{< /code >}}

2. Replace the placeholder with the path to your certificate and key for the `etcd-peer-cert-file` and `etcd-peer-key-file` to secure cluster communication:
{{< code yml >}}
etcd-peer-cert-file: "/path/to/your/peer/cert"
etcd-peer-key-file: "/path/to/your/peer/key"
{{< /code >}}

3. Replace the placeholder with the path to your certificate and key for the `etcd-trusted-ca-file` and `etcd-peer-trusted-ca-file` to secure communication with the etcd client server and between etcd cluster members:
{{< code yml >}}
etcd-trusted-ca-file: "/path/to/your/ca/file"
etcd-peer-trusted-ca-file: "/path/to/your/peer/ca/file"
{{< /code >}}

4. Add non-default values for `etcd-listen-client-urls`, `etcd-listen-peer-urls`, and `etcd-initial-advertise-client-urls`:
{{< code yml >}}
etcd-listen-client-urls: "https://localhost:2379"
etcd-listen-peer-urls: "https://localhost:2380"
etcd-initial-advertise-peer-urls: "https://localhost:2380"
{{< /code >}}

    {{% notice note %}}
**NOTE**: If you are securing a [cluster](../cluster-sensu), use your backend node IP address instead of `localhost` in the non-default values for `etcd-listen-client-urls`, `etcd-listen-peer-urls`, and `etcd-initial-advertise-client-urls`.
{{% /notice %}}

5. Set `etcd-client-cert-auth` and `etcd-peer-client-cert-auth` to `true` to ensure that etcd only allows connections from clients and peers that present a valid, trusted certificate:
{{< code yml >}}
etcd-client-cert-auth: "true"
etcd-peer-client-cert-auth: "true"
{{< /code >}}

   Because etcd does not require authentication by default, you must set the `etcd-client-cert-auth` and `etcd-peer-client-cert-auth` parameters to `true` to secure Sensu's embedded etcd datastore against unauthorized access.

{{% notice note %}}
**NOTE**: The [Sensu backend reference](../../../observability-pipeline/observe-schedule/backend/#datastore-and-cluster-configuration-flags) includes more information about each etcd store parameter.
{{% /notice %}}

## Secure the Sensu API and web UI

The Sensu Go Agent API, HTTP API, and web UI use a common stanza in `/etc/sensu/backend.yml` to provide the certificate, key, and CA file needed to provide secure communication.

{{% notice note %}}
**NOTE**: By changing these parameters, the server will communicate using transport layer security (TLS) and expect agents that connect to it to use the WebSocket secure protocol.
For communication to continue, you must complete the configuration in this section **and** in the [Sensu agent-to-server communication](#secure-sensu-agent-to-server-communication) section.
{{% /notice %}}

Configure the following backend secure sockets layer (SSL) attributes in `/etc/sensu/backend.yml`:

1. Replace the placeholders with the paths to your certificate and key files for the `cert-file`, `key-file`, and `trusted-ca-file` parameters:
{{< code yml >}}
cert-file: "/path/to/ssl/cert.pem"
key-file: "/path/to/ssl/key.pem"
trusted-ca-file: "/path/to/trusted-certificate-authorities.pem"
insecure-skip-tls-verify: false
{{< /code >}}

2. Set the `insecure-skip-tls-verify` parameter to `false`:
{{< code yml >}}
insecure-skip-tls-verify: false
{{< /code >}}

3. When you provide these cert-file and key-file parameters, the agent WebSocket API and HTTP API will serve requests over SSL/TLS (https).
For this reason, you must also specify `https://` schema for the `api-url` parameter for backend API configuration:
{{< code yml >}}
api-url: "https://localhost:8080"
{{< /code >}}

After you restart the `sensu-backend` service, the parameters will load and you will able to access the web UI at https://localhost:3000.
Configuring these attributes will also ensure that agents can communicate securely.

{{% notice note %}}
**NOTE**: The [Sensu backend reference](../../../observability-pipeline/observe-schedule/backend/#security-configuration-flags) includes more information about each API and web UI security configuration parameter.
{{% /notice %}}

### Specify separate web UI certificate and key

You can specify a certificate and key for the web UI separately from the API.
To do this, add the `dashboard-cert-file` and `dashboard-key-file` parameters for backend SSL configuration in `/etc/sensu/backend.yml`:

{{< code yml >}}
dashboard-cert-file: "/path/to/ssl/cert.pem"
dashboard-key-file: "/path/to/ssl/key.pem"
{{< /code >}}

{{% notice note %}}
**NOTE**: The [Sensu backend reference](../../../observability-pipeline/observe-schedule/backend/#web-ui-configuration-flags) includes more information about the `` and `` web UI configuration parameter.
{{% /notice %}}

## Secure Sensu agent-to-server communication

{{% notice note %}}
**NOTE**: If you change the agent configuration to communicate via WebSocket Secure protocol, the agent will no longer communicate over a plaintext connection.
For communication to continue, you must complete the steps in this section **and** [secure the Sensu API and web UI](#secure-the-sensu-api-and-web-ui).
{{% /notice %}}

By default, an agent uses the insecure `ws://` transport.
Here's an example for agent configuration in `/etc/sensu/agent.yml`:

{{< code yml >}}
backend-url:
  - "ws://127.0.0.1:8081"
{{< /code >}}

To use WebSocket over SSL/TLS (wss), change the `backend-url` value to the `wss://` schema in `/etc/sensu/agent.yml`:

{{< code yml >}}
backend-url:
  - "wss://127.0.0.1:8081"
{{< /code >}}

The agent will connect to Sensu backends over wss.
Remember, if you change the configuration to wss, plaintext communication will not be possible.

You can also provide a trusted CA as part of the agent configuration.
If you will start the agent via `sensu-agent start`, pass the `--trusted-ca-file` flag with the start command.
Otherwise, include the `trusted-ca-file` parameter in the agent configuration in `/etc/sensu/agent.yml`: 

{{< code yml>}}
trusted-ca-file: "/path/to/trusted-certificate-authorities.pem"
{{< /code >}}

{{% notice note %}}
**NOTE**: If you are creating a Sensu cluster, every cluster member needs to be present in the configuration.
See [Run a Sensu cluster](../cluster-sensu/) for more information about how to configure agents for a clustered configuration.
{{% /notice %}}

## Configure Sensu agent mTLS authentication

**COMMERCIAL FEATURE**: Access client mutual transport layer security (mTLS) authentication in the packaged Sensu Go distribution.
For more information, see [Get started with commercial features][5].

By default, Sensu agents require username and password authentication to communicate with Sensu backends.
For Sensu's [default user credentials][2] and details about configuring Sensu role-based access control (RBAC), see the [RBAC reference][3].

Alternatively, Sensu agents can use mTLS for authenticating to the backend websocket transport.
When agent mTLS authentication is enabled, agents do not need to send password credentials to backends when they connect.
To use [secrets management][1], Sensu agents must be secured with mTLS.
In addition, when using mTLS authentication, agents do not require an explicit user in Sensu.
Sensu agents default to authenticating as the [`agent` user][2] and using permissions granted to the `system:agents` group by the `system:agents` cluster role and cluster role binding.

You can still bind agents to a specific user when the `system:agents` group is problematic.
For this use case, create a user that matches the Common Name (CN) of the agent's certificate.

{{% notice note %}}
**NOTE**: Sensu agents need to be able to create events in the agent's namespace.
To ensure that agents with incorrect CN fields can't access the backend, remove the default `system:agents` group.
{{% /notice %}}

To view a certificate's CN with openssl, run:

{{< code bash >}}
openssl x509 -in client.pem -text -noout
{{< /code >}}

The response should be similar to this example:

{{< code bash >}}
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number:
            37:57:7b:04:1d:67:63:7b:ff:ae:39:19:5b:55:57:80:41:3c:ec:ff
        Signature Algorithm: sha256WithRSAEncryption
        Issuer: CN = CA
        Validity
            Not Before: Sep 26 18:58:00 2019 GMT
            Not After : Sep 24 18:58:00 2024 GMT
        Subject: CN = client
...
{{< /code >}}

The `Subject:` field indicates the certificate's CN is `client`, so to bind the agent to a particular user in Sensu, create a user called `client`.

To enable agent mTLS authentication:

1. Create and distribute new certificates and keys according to the [Generate certificates][12] guide.

2. With the TLS certificate and key are in place, [update the agent configuration using `cert-file` and `key-file` security configuration flags][7].

3. After you create backend and agent certificates, modify the backend configuration:
{{< code yml >}}
agent-auth-cert-file: "/path/to/backend-1.pem"
agent-auth-key-file: "/path/to/backend-1-key.pem"
agent-auth-trusted-ca-file: "/path/to/ca.pem"
{{< /code >}}

4. Modify the agent configuration:
{{< code yml >}}
cert-file: "/path/to/agent.pem"
key-file: "/path/to/agent-key.pem"
trusted-ca-file: "/path/to/ca.pem"
{{< /code >}}

You can use use certificates for authentication that are distinct from other communication channels used by Sensu, like etcd or the API.
However, deployments can also use the same certificates and keys for etcd peer and client communication, the HTTP API, and agent authentication without issues.

### Certificate revocation check

The Sensu backend checks certificate revocation list (CRL) and Online Certificate Status Protocol (OCSP) endpoints for agent mTLS, etcd client, and etcd peer connections whose remote sides present X.509 certificates that provide CRL and OCSP revocation information.

## Dynamic runtime asset paths and sudo

When check commands on Linux require enhanced permissions to run, you can use sudo to escalate the Sensu user’s privileges in a targeted fashion.
If you use dynamic runtime assets for check commands that use sudo, you'll need to adjust your default sudo configuration.

{{% notice warning %}}
**WARNING**: Before you adjust your sudo configuration, consider whether using dynamic runtime assets for privileged checks meets your security requirements.<br><br>
Using dynamic runtime assets with sudo has important security implications.
Rather than making a habit of using sudo for all check commands, carefully evaluate when its appropriate to escalate privileges in this way.
{{% /notice %}}

<a name="sudo-all-assets"></a>

To give Sensu access to use `sudo -E` for **all** assets installed under `var/cache/sensu/sensu-agent/`, add these lines to a file in your `/etc/sudoers.d/` directory:

{{< code shell >}}
sensu   ALL=(ALL)       NOPASSWD:SETENV: /var/cache/sensu/sensu-agent/**/bin/*
sensu   ALL=(ALL)       NOPASSWD:SETENV: /var/cache/sensu/sensu-agent/**/bin/*.*
{{< /code >}}

Both lines are necessary because `bin/*.*` won't match Go assets that do not end with file extension `.ext`.
The `**` is a [POSIX glob][8] that will match any subdirectory other than `.` and `..`.
`NOPASSWD:SETENV:` allows the Sensu user to run commands without a password and use `sudo -E` to preserve the Sensu user’s environment.

{{% notice warning %}}
**WARNING**: Use this example with the `**` POSIX glob as a pattern for testing in non-production environments.
If you include these lines in your sudo configuration, Sensu will run any script installed as an asset under sudo.
With the `sudo -E` prefix added to the check command, sudo will use the environment variables meant for the Sensu check environment.
**This opens all installed Sensu assets for privileged operation**.<br><br>
We recommend replacing the `**` glob with the sha512 sum for the specific build of the dynamic runtime asset to [target a specific dynamic runtime asset directory](#target-a-specific-dynamic-runtime-asset-directory).
In production, you should also replace the `bin/*.*` and `bin/*` globs in the sudo rule patterns with specific commands to further improve security.
{{% /notice %}}

With these changes, you can add `sudo -E` as the prefix for all asset-provided commands.
This will ensure that agent-provided environment variables are passed to the sudo environment and provide the expected sensu-agent operation using default agent configuration settings.

### Example check with privileged check command

This example check uses the `sudo -E` prefix to run a privileged check command provided by a dynamic runtime asset, [System Profile Linux][11].
The dynamic runtime asset named `sensu/system-profile-linux` is mapped into the environment variable `SENSU_SYSTEM_PROFILE_LINUX_PATH`.
Sensu will use the asset-specific path environment variable to prefix the check command instead of editing the sudo `secure_path`.

This check requires sudo rules that [allow Sensu to use `sudo -E` to run commands for all assets][14] installed under `var/cache/sensu/sensu-agent/`.
These rules allow Sensu to run **all** installed asset commands.

{{< language-toggle >}}

{{< code yml >}}
---
type: CheckConfig
api_version: core/v2
metadata:
  name: sudo_example
spec:
  check_hooks: null 
  command: sudo -E ${SENSU_SYSTEM_PROFILE_LINUX_PATH}/bin/system-profile-linux
  interval: 60
  publish: false
  runtime_assets:
  - sensu/system-profile-linux
  subscriptions:
  - test
{{< /code >}}

{{< code json >}}
{
  "type": "CheckConfig",
  "api_version": "core/v2",
  "metadata": {
    "name": "sudo_example"
  },
  "spec": {
    "check_hooks": null,
    "command": "sudo -E ${SENSU_SYSTEM_PROFILE_LINUX_PATH}/bin/system-profile-linux",
    "interval": 60,
    "publish": false,
    "runtime_assets": [
      "sensu/system-profile-linux"
    ],
    "subscriptions": [
      "test"
    ]
  }
}
{{< /code >}}

{{< /language-toggle >}}

<a name="asset-definition"></a>

The check requires the following definition for the [`system-profile-linux`][11] dynamic runtime asset:

{{< language-toggle >}}

{{< code yml >}}
---
type: Asset
api_version: core/v2
metadata:
  annotations:
    io.sensu.bonsai.api_url: https://bonsai.sensu.io/api/v1/assets/sensu/system-profile-linux
    io.sensu.bonsai.name: system-profile-linux
    io.sensu.bonsai.namespace: sensu
    io.sensu.bonsai.tags: ""
    io.sensu.bonsai.tier: Community
    io.sensu.bonsai.url: https://bonsai.sensu.io/assets/sensu/system-profile-linux
    io.sensu.bonsai.version: 0.10.1
  name: sensu/system-profile-linux
spec:
  builds:
  - filters:
    - entity.system.os == 'darwin'
    - entity.system.arch == '386'
    headers: null
    sha512: 523f4e3ac815969ffe8c085bfc61090655bc2978216396989d4b23de360b65ff696d746bc7acce42f888795a2fadd5f17ee47e98d9c18a1f0d7d9fd8771e228d
    url: https://assets.bonsai.sensu.io/7d72df2682c0134068abd21a65778c81e61d7afe/system-profile-linux_0.10.1_darwin_386.tar.gz
  - filters:
    - entity.system.os == 'darwin'
    - entity.system.arch == 'amd64'
    headers: null
    sha512: 00cbfbc9f39fb3a11915e848277586e21b1223ffdd85a5c1abf02bb31c0bb6cf1e37fa533a6b331ad684d6a815672b8823a215770584c1da10263bdedd924b1d
    url: https://assets.bonsai.sensu.io/7d72df2682c0134068abd21a65778c81e61d7afe/system-profile-linux_0.10.1_darwin_amd64.tar.gz
  - filters:
    - entity.system.os == 'linux'
    - entity.system.arch == 'armv7'
    headers: null
    sha512: f7ad60cfc4ba12ccfe623e2d86727a544b35c2fb165f6c9acae432f132762022ba542cf26d92e15ac445cc5d241feb6055c17286cb2f5a1e5c6be0723a003e91
    url: https://assets.bonsai.sensu.io/7d72df2682c0134068abd21a65778c81e61d7afe/system-profile-linux_0.10.1_linux_armv7.tar.gz
  - filters:
    - entity.system.os == 'linux'
    - entity.system.arch == 'arm64'
    headers: null
    sha512: 689def9af9116cdeaf8bca319b59012a83073bc05587e3e974aa5b9a5cd3a40fbab7ce386737d1d18c62d9d06b7393d3cdc26e35c8c697920cc1a9a9acb94ad9
    url: https://assets.bonsai.sensu.io/7d72df2682c0134068abd21a65778c81e61d7afe/system-profile-linux_0.10.1_linux_arm64.tar.gz
  - filters:
    - entity.system.os == 'linux'
    - entity.system.arch == '386'
    headers: null
    sha512: 7c5bf18b52f6c6b9d55f1fe882c4341949730d25abf31fc472d6779948d31bc3606887ceb7d160d706acd5abd660111e98ba0220815a87d1a5c351dd95b2eaf3
    url: https://assets.bonsai.sensu.io/7d72df2682c0134068abd21a65778c81e61d7afe/system-profile-linux_0.10.1_linux_386.tar.gz
  - filters:
    - entity.system.os == 'linux'
    - entity.system.arch == 'amd64'
    headers: null
    sha512: 29a6e1725f37e533cd9f6a8a17b40ef757ba5ea5dc27701c19a7fb9ac9c2bdf9f684d758d4440f278bb7fc669e52bf02efb3fc6758731f7f3e10617a2fe026cf
    url: https://assets.bonsai.sensu.io/7d72df2682c0134068abd21a65778c81e61d7afe/system-profile-linux_0.10.1_linux_amd64.tar.gz
  filters: null
  headers: null
{{< /code >}}

{{< code json >}}
{
  "type": "Asset",
  "api_version": "core/v2",
  "metadata": {
    "annotations": {
      "io.sensu.bonsai.api_url": "https://bonsai.sensu.io/api/v1/assets/sensu/system-profile-linux",
      "io.sensu.bonsai.name": "system-profile-linux",
      "io.sensu.bonsai.namespace": "sensu",
      "io.sensu.bonsai.tags": "",
      "io.sensu.bonsai.tier": "Community",
      "io.sensu.bonsai.url": "https://bonsai.sensu.io/assets/sensu/system-profile-linux",
      "io.sensu.bonsai.version": "0.10.1"
    },
    "name": "sensu/system-profile-linux"
  },
  "spec": {
    "builds": [
      {
        "filters": [
          "entity.system.os == 'darwin'",
          "entity.system.arch == '386'"
        ],
        "headers": null,
        "sha512": "523f4e3ac815969ffe8c085bfc61090655bc2978216396989d4b23de360b65ff696d746bc7acce42f888795a2fadd5f17ee47e98d9c18a1f0d7d9fd8771e228d",
        "url": "https://assets.bonsai.sensu.io/7d72df2682c0134068abd21a65778c81e61d7afe/system-profile-linux_0.10.1_darwin_386.tar.gz"
      },
      {
        "filters": [
          "entity.system.os == 'darwin'",
          "entity.system.arch == 'amd64'"
        ],
        "headers": null,
        "sha512": "00cbfbc9f39fb3a11915e848277586e21b1223ffdd85a5c1abf02bb31c0bb6cf1e37fa533a6b331ad684d6a815672b8823a215770584c1da10263bdedd924b1d",
        "url": "https://assets.bonsai.sensu.io/7d72df2682c0134068abd21a65778c81e61d7afe/system-profile-linux_0.10.1_darwin_amd64.tar.gz"
      },
      {
        "filters": [
          "entity.system.os == 'linux'",
          "entity.system.arch == 'armv7'"
        ],
        "headers": null,
        "sha512": "f7ad60cfc4ba12ccfe623e2d86727a544b35c2fb165f6c9acae432f132762022ba542cf26d92e15ac445cc5d241feb6055c17286cb2f5a1e5c6be0723a003e91",
        "url": "https://assets.bonsai.sensu.io/7d72df2682c0134068abd21a65778c81e61d7afe/system-profile-linux_0.10.1_linux_armv7.tar.gz"
      },
      {
        "filters": [
          "entity.system.os == 'linux'",
          "entity.system.arch == 'arm64'"
        ],
        "headers": null,
        "sha512": "689def9af9116cdeaf8bca319b59012a83073bc05587e3e974aa5b9a5cd3a40fbab7ce386737d1d18c62d9d06b7393d3cdc26e35c8c697920cc1a9a9acb94ad9",
        "url": "https://assets.bonsai.sensu.io/7d72df2682c0134068abd21a65778c81e61d7afe/system-profile-linux_0.10.1_linux_arm64.tar.gz"
      },
      {
        "filters": [
          "entity.system.os == 'linux'",
          "entity.system.arch == '386'"
        ],
        "headers": null,
        "sha512": "7c5bf18b52f6c6b9d55f1fe882c4341949730d25abf31fc472d6779948d31bc3606887ceb7d160d706acd5abd660111e98ba0220815a87d1a5c351dd95b2eaf3",
        "url": "https://assets.bonsai.sensu.io/7d72df2682c0134068abd21a65778c81e61d7afe/system-profile-linux_0.10.1_linux_386.tar.gz"
      },
      {
        "filters": [
          "entity.system.os == 'linux'",
          "entity.system.arch == 'amd64'"
        ],
        "headers": null,
        "sha512": "29a6e1725f37e533cd9f6a8a17b40ef757ba5ea5dc27701c19a7fb9ac9c2bdf9f684d758d4440f278bb7fc669e52bf02efb3fc6758731f7f3e10617a2fe026cf",
        "url": "https://assets.bonsai.sensu.io/7d72df2682c0134068abd21a65778c81e61d7afe/system-profile-linux_0.10.1_linux_amd64.tar.gz"
      }
    ],
    "filters": null,
    "headers": null
  }
}
{{< /code >}}

{{< /language-toggle >}}

### Target a specific dynamic runtime asset directory

To improve security, configure Sensu access to use `sudo -E` only for specific assets installed under `var/cache/sensu/sensu-agent/`, 
In your `/etc/sudoers.d/` file, in place of `**`, list the sha512 sum for the specific build of the dynamic runtime asset you are using.
This effectively whitelists the asset paths you want sudo to be able to use.
You can find the sha512 sum for the build you want to whitelist in the asset definition.

For example, the following rules would allow `sudo -E` access for only the [Linux amd64 build of the System Profile Linux][13] dynamic runtime asset:

{{< code shell >}}
sensu   ALL=(ALL)       NOPASSWD:SETENV: /var/cache/sensu/sensu-agent/29a6e1725f37e533cd9f6a8a17b40ef757ba5ea5dc27701c19a7fb9ac9c2bdf9f684d758d4440f278bb7fc669e52bf02efb3fc6758731f7f3e10617a2fe026cf/bin/*.*
sensu   ALL=(ALL)       NOPASSWD:SETENV: /var/cache/sensu/sensu-agent/29a6e1725f37e533cd9f6a8a17b40ef757ba5ea5dc27701c19a7fb9ac9c2bdf9f684d758d4440f278bb7fc669e52bf02efb3fc6758731f7f3e10617a2fe026cf/bin/*
{{< /code >}}

### Extend the sudo secure_path to include assets

If the sudo `secure_path` option is enabled, you can extend the path to include sensu-agent assets so that you do not have to explicitly use the full path to the asset binary in your sudo calls.
For example, this update allows you to call `sudo echo "hello world"` rather than `sudo /usr/bin/echo "hello world"`.
This is useful for checks that need to run on different hosts or that have different builds for different hosts.

Add this line to your `/etc/sudoers.d/` file:

{{< code shell >}}
Defaults    secure_path = /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/var/cache/sensu/sensu-agent/**/bin
{{< /code >}}

### Use sudo for diagnostic checks

To give Sensu access to use `sudo -E` for diagnostic purposes, add this line to your `/etc/sudoers.d/` file:

{{< code shell >}}
sensu   ALL=(ALL)       NOPASSWD:SETENV: /usr/bin/echo
{{< /code >}}

This allows you to create diagnostic check commands to ensure that dynamic runtime asset paths work as you expect.

For example, the event output for the following check should list both dynamic runtime asset paths prepended with an obvious asset directory under the configured sensu-agent cache directory:

{{< language-toggle >}}

{{< code yml >}}
---
type: CheckConfig
api_version: core/v2
metadata:
  name: sudo_test
spec:
  check_hooks: null
  command: sudo -E echo "PATH:$PATH \nLD:$LD_LIBRARY_PATH \n"
  env_vars: null
  handlers: []
  high_flap_threshold: 0
  interval: 10
  low_flap_threshold: 0
  output_metric_format: ""
  output_metric_handlers: null
  proxy_entity_name: ""
  publish: true
  round_robin: false
  runtime_assets:
  - sensu/system-profile-linux
  secrets: null
  stdin: false
  subdue: null
  subscriptions:
  - test
  timeout: 0
  ttl: 0
{{< /code >}}

{{< code json >}}
{
  "type": "CheckConfig",
  "api_version": "core/v2",
  "metadata": {
    "name": "sudo_test"
  },
  "spec": {
    "check_hooks": null,
    "command": "sudo -E echo \"PATH:$PATH \\nLD:$LD_LIBRARY_PATH \\n\"",
    "env_vars": null,
    "handlers": [],
    "high_flap_threshold": 0,
    "interval": 10,
    "low_flap_threshold": 0,
    "output_metric_format": "",
    "output_metric_handlers": null,
    "proxy_entity_name": "",
    "publish": true,
    "round_robin": false,
    "runtime_assets": [
      "sensu/system-profile-linux"
    ],
    "secrets": null,
    "stdin": false,
    "subdue": null,
    "subscriptions": [
      "test"
    ],
    "timeout": 0,
    "ttl": 0
  }
}
{{< /code >}}

{{< /language-toggle >}}

## Next step: Run a Sensu cluster

Well done!
Your Sensu installation should now be secured with TLS.
The last step before you deploy Sensu is to [set up a Sensu cluster][10].


[1]: ../../manage-secrets/secrets-management/
[2]: ../../control-access/rbac/#default-users
[3]: ../../control-access/rbac/
[5]: ../../../commercial/
[6]: https://etcd.io/docs/v3.3.13/op-guide/security/
[7]: ../../../observability-pipeline/observe-schedule/agent/#security-configuration-flags
[8]: https://en.wikipedia.org/wiki/Glob_%28programming%29
[9]: https://github.com/cloudflare/cfssl
[10]: ../cluster-sensu/
[11]: https://bonsai.sensu.io/assets/sensu/system-profile-linux
[12]: ../generate-certificates/
[13]: #asset-definition
[14]: #sudo-all-assets
