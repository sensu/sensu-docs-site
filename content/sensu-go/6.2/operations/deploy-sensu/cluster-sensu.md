---
title: "Run a Sensu cluster"
linkTitle: "Run a Sensu Cluster"
guide_title: "Run a Sensu cluster"
type: "guide"
description: "Clustering improves Sensu's availability, reliability, and durability. It can help you cope with the loss of a backend node, prevent data loss, and distribute the network load of agents. Read the guide to configure a Sensu cluster."
weight: 70
version: "6.2"
product: "Sensu Go"
platformContent: false
menu: 
  sensu-go-6.2:
    parent: deploy-sensu
---

To deploy Sensu for use outside of a local development environment, first decide whether you want to run a Sensu cluster.

A Sensu cluster is a group of at least three sensu-backend nodes, each connected to a shared database provided either by Sensu’s embedded etcd or an external etcd cluster.
Creating a Sensu cluster ultimately configures an [etcd cluster][2].

Clustering improves Sensu's availability, reliability, and durability.
It allows you to absorb the loss of a backend node, prevent data loss, and distribute the network load of agents.
If you have a healthy clustered backend, you only need to make [Sensu API][20] calls to any one of the cluster members.
The cluster protocol will replicate your changes to all cluster members.

Scaling a single backend to a cluster or migrating a cluster from cleartext HTTP to encrypted HTTPS without downtime can require [a number of tedious steps][14].
For this reason, we recommend that you **decide whether your deployment will require clustering as part of your initial planning effort**.

No matter whether you deploy a single backend or a clustered configuration, begin by securing Sensu with transport layer security (TLS).
The first step in setting up TLS is to [generate the certificates you need][13].
Then, follow our [Secure Sensu][16] guide to make Sensu production-ready.

After you've secured Sensu, continue reading this document to [set up][2] and [update][1] a clustered configuration.

{{% notice note %}}
**NOTE**: We recommend using a load balancer to evenly distribute agent connections across a cluster.
{{% /notice %}}

## Configure a cluster

The sensu-backend arguments for its store mirror the [etcd configuration flags][3], but the Sensu flags are prefixed with `etcd`.
For more detailed descriptions of the different arguments, see the [etcd documentation][4] or the [Sensu backend reference][15].

You can configure a Sensu cluster in a couple different ways &mdash; we'll show you a few below &mdash; but you should adhere to some etcd cluster guidelines as well:

> The recommended etcd cluster size is 3, 5 or 7, which is decided by the fault tolerance requirement. A 7-member cluster can provide enough fault tolerance in most cases. While a larger cluster provides better fault tolerance, the write performance reduces since data needs to be replicated to more machines. It is recommended to have an odd number of members in a cluster. Having an odd cluster size doesn't change the number needed for majority, but you gain a higher tolerance for failure by adding the extra member. *[etcd2 Admin Guide][18]*

We also recommend using stable platforms to support your etcd instances (see [etcd's supported platforms][5]).

{{% notice note %}}
**NOTE**: If a cluster member is started before it is configured to join a cluster, the member will persist its prior configuration to disk.
For this reason, you must remove any previously started member's etcd data by stopping sensu-backend and deleting the contents of `/var/lib/sensu/sensu-backend/etcd` before proceeding with cluster configuration.
{{% /notice %}}

### Docker

If you prefer to stand up your Sensu cluster within Docker containers, check out the Sensu Go [Docker configuration][7].
This configuration defines three sensu-backend containers and three sensu-agent containers.

### Traditional computer instance

{{% notice note %}}
**NOTE**: The remainder of this guide describes on-disk configuration.
If you are using an ephemeral computer instance, you can use `sensu-backend start --help` to see examples of etcd command line flags.
The configuration file entries in the rest of this guide translate to `sensu-backend` flags.
{{% /notice %}}

#### Sensu backend configuration

{{% notice warning %}}
**WARNING**: You must update the default configuration for Sensu's embedded etcd with an explicit, non-default configuration to secure etcd communication in transit.
If you do not properly configure secure etcd communication, your Sensu configuration will be vulnerable to unauthorized manipulation via etcd client connections.
{{% /notice %}}

The examples in this section are configuration snippets from `/etc/sensu/backend.yml` using a three-node cluster.
The nodes are named `backend-1`, `backend-2` and `backend-3` with IP addresses `10.0.0.1`, `10.0.0.2` and `10.0.0.3`, respectively.

{{% notice note %}}
**NOTE**: This backend configuration assumes you have set up and installed the sensu-backend on all the nodes used in your cluster.
Follow the [Install Sensu](../install-sensu/) guide if you have not already done this.
{{% /notice %}}

**Store configuration for backend-1/10.0.0.1**

{{< code yml >}}
etcd-advertise-client-urls: "http://10.0.0.1:2379"
etcd-listen-client-urls: "http://10.0.0.1:2379"
etcd-listen-peer-urls: "http://0.0.0.0:2380"
etcd-initial-cluster: "backend-1=http://10.0.0.1:2380,backend-2=http://10.0.0.2:2380,backend-3=http://10.0.0.3:2380"
etcd-initial-advertise-peer-urls: "http://10.0.0.1:2380"
etcd-initial-cluster-state: "new"
etcd-initial-cluster-token: "unique_token_for_this_cluster"
etcd-name: "backend-1"
{{< /code >}}

**Store configuration for backend-2/10.0.0.2**

{{< code yml >}}
etcd-advertise-client-urls: "http://10.0.0.2:2379"
etcd-listen-client-urls: "http://10.0.0.2:2379"
etcd-listen-peer-urls: "http://0.0.0.0:2380"
etcd-initial-cluster: "backend-1=http://10.0.0.1:2380,backend-2=http://10.0.0.2:2380,backend-3=http://10.0.0.3:2380"
etcd-initial-advertise-peer-urls: "http://10.0.0.2:2380"
etcd-initial-cluster-state: "new"
etcd-initial-cluster-token: "unique_token_for_this_cluster"
etcd-name: "backend-2"
{{< /code >}}

**Store configuration for backend-3/10.0.0.3**

{{< code yml >}}
etcd-advertise-client-urls: "http://10.0.0.3:2379"
etcd-listen-client-urls: "http://10.0.0.3:2379"
etcd-listen-peer-urls: "http://0.0.0.0:2380"
etcd-initial-cluster: "backend-1=http://10.0.0.1:2380,backend-2=http://10.0.0.2:2380,backend-3=http://10.0.0.3:2380"
etcd-initial-advertise-peer-urls: "http://10.0.0.3:2380"
etcd-initial-cluster-state: "new"
etcd-initial-cluster-token: "unique_token_for_this_cluster"
etcd-name: "backend-3"
{{< /code >}}

{{% notice warning %}}
**WARNING**: To properly secure etcd communication, replace the default URLs for `etcd-advertise-client-urls`, `etcd-listen-client-urls`, `etcd-listen-peer-urls`, and `etcd-initial-cluster` in the store configurations for your backends with non-default values.<br><br>
Specify the same `etcd-initial-cluster-token` value for all three backends.
This allows etcd to generate unique cluster IDs and member IDs even for clusters that have otherwise identical configurations and prevents cross-cluster-interaction.
{{% /notice %}}

After you configure each node as described in these examples, start each sensu-backend:

{{< code shell >}}
sudo systemctl start sensu-backend
{{< /code >}}

##### Add Sensu agents to clusters

Each Sensu agent should have the following entries in `/etc/sensu/agent.yml` to ensure the agent is aware of all cluster members.
This allows the agent to reconnect to a working backend if the backend it is currently connected to goes into an unhealthy state.

Here is an example backend-url configuration for all agents connecting to the cluster over WebSocket:

{{< code yml >}}
backend-url:
  - "ws://10.0.0.1:8081"
  - "ws://10.0.0.2:8081"
  - "ws://10.0.0.3:8081"
{{< /code >}}

You should now have a highly available Sensu cluster!
Confirm cluster health and try other cluster management commands with [sensuctl][6].

## Manage and monitor clusters with sensuctl

[Sensuctl][17] includes several commands to help you manage and monitor your cluster.
Run `sensuctl cluster -h` for additional help information.

### Get cluster health status

Get cluster health status and etcd alarm information:

{{< code shell >}}
sensuctl cluster health
{{< /code >}}

The cluster health response will list the health status for each cluster member, similar to this example:

{{< code shell >}}
       ID            Name                          Error                           Healthy  
────────────────── ─────────── ─────────────────────────────────────────────────── ─────────
a32e8f613b529ad4   backend-1                                                        true
c3d9f4b8d0dd1ac9   backend-2  dial tcp 10.0.0.2:2379: connect: connection refused   false
c8f63ae435a5e6bf   backend-3                                                        true
{{< /code >}}

### Add a cluster member

To add a new member node to an existing cluster:

1. Configure the new node's store in its `/etc/sensu/backend.yml` configuration file.
For the new node `backend-4` with IP address `10.0.0.4`:

   {{< code yml >}}
etcd-advertise-client-urls: "http://10.0.0.4:2379"
etcd-listen-client-urls: "http://10.0.0.4:2379"
etcd-listen-peer-urls: "http://0.0.0.0:2380"
etcd-initial-cluster: "backend-1=http://10.0.0.1:2380,backend-2=http://10.0.0.2:2380,backend-3=http://10.0.0.3:2380,backend-4=http://10.0.0.4:2380"
etcd-initial-advertise-peer-urls: "http://10.0.0.4:2380"
etcd-initial-cluster-state: "existing"
etcd-initial-cluster-token: "unique_token_for_this_cluster"
etcd-name: "backend-4"
{{< /code >}}

   {{% notice note %}}
**NOTE**: To make sure the new member is added to the correct cluster, specify the same `etcd-initial-cluster-token` value that you used for the other members in the cluster.

Also, when you are adding a cluster member, make sure the `etcd-initial-cluster-state` value is `existing`, **not** `new`.
{{% /notice %}}

2. Run the sensuctl command to add the new cluster member:

   {{< code shell >}}
sensuctl cluster member-add backend-4 http://10.0.0.4:2380
{{< /code >}}

   You will receive a sensuctl response to confirm that the new member was added:

   {{< code shell >}}
added member 2f7ae42c315f8c2d to cluster
{{< /code >}}

3. Start the new backend:

   {{< code shell >}}
sudo systemctl start sensu-backend
{{< /code >}}

4. Add the new cluster member's WebSocket backend-url in `/etc/sensu/agent.yml` for all agents that connect to the cluster over WebSocket:

   {{< code yml >}}
backend-url:
  - "ws://10.0.0.1:8081"
  - "ws://10.0.0.2:8081"
  - "ws://10.0.0.3:8081"
  - "ws://10.0.0.4:8081"
{{< /code >}}

### List cluster members

List the ID, name, peer URLs, and client URLs of all nodes in a cluster:

{{< code shell >}}
sensuctl cluster member-list
{{< /code >}}

You will receive a sensuctl response that lists all cluster members:

{{< code shell >}}
       ID            Name             Peer URLs                Client URLs
────────────────── ─────────── ───────────────────────── ─────────────────────────
a32e8f613b529ad4   backend-1    http://10.0.0.1:2380      http://10.0.0.1:2379  
c3d9f4b8d0dd1ac9   backend-2    http://10.0.0.2:2380      http://10.0.0.2:2379
c8f63ae435a5e6bf   backend-3    http://10.0.0.3:2380      http://10.0.0.3:2379
2f7ae42c315f8c2d   backend-4    http://10.0.0.4:2380      http://10.0.0.4:2379
{{< /code >}}

### Remove a cluster member

Remove a faulty or decommissioned member node from a cluster:

{{< code shell >}}
sensuctl cluster member-remove 2f7ae42c315f8c2d
{{< /code >}}

You will receive a sensuctl response to confirm that the cluster member was removed:

{{< code shell >}}
Removed member 2f7ae42c315f8c2d from cluster
{{< /code >}}

### Replace a faulty cluster member

To replace a faulty cluster member to restore a cluster's health:

1. Get cluster health status and etcd alarm information:
{{< code shell >}}
sensuctl cluster health
{{< /code >}}

    In the response, for a faulty cluster member, the Error column will include an error message and the Healthy column will list `false`.
    In this example, the response indicates that cluster member `backend-4` is faulty:
{{< code shell >}}
       ID            Name                          Error                           Healthy  
────────────────── ─────────── ─────────────────────────────────────────────────── ─────────
a32e8f613b529ad4   backend-1                                                        true
c3d9f4b8d0dd1ac9   backend-2                                                        true
c8f63ae435a5e6bf   backend-3                                                        true
2f7ae42c315f8c2d   backend-4  dial tcp 10.0.0.4:2379: connect: connection refused   false

{{< /code >}}

2. Remove the faulty cluster member &mdash; in this example, `backend-4` &mdash; using its ID.
Removing the faulty cluster member prevents the cluster size from growing.
{{< code shell >}}
sensuctl cluster member-remove 2f7ae42c315f8c2d
{{< /code >}}

    The response should indicate that the cluster member was removed:
{{< code shell >}}
Removed member 2f7ae42c315f8c2d from cluster
{{< /code >}}

3. Follow the steps in [Add a cluster member][22] to configure the replacement cluster member.
{{% notice note %}}
**NOTE**: You can use the same name and IP address as the removed faulty member for the replacement cluster member.
When updating the replacement member's backend configuration file, make sure the `etcd-initial-cluster-state` value is `existing`, **not** `new`.
{{% /notice %}}

If replacing the faulty cluster member does not resolve the problem, see the [etcd operations guide][12] for more information.

### Update a cluster member

Update the peer URLs of a member in a cluster:

{{< code shell >}}
sensuctl cluster member-update c8f63ae435a5e6bf http://10.0.0.4:2380
{{< /code >}}

You will receive a sensuctl response to confirm that the cluster member was updated:

{{< code shell >}}
Updated member with ID c8f63ae435a5e6bf in cluster
{{< /code >}}

## Cluster security

See [Secure Sensu][16] for information about cluster security.

## Use an external etcd cluster

{{% notice warning %}}
**WARNING**: You must update the example configuration for external etcd with an explicit, non-default configuration to secure etcd communication in transit.
If you do not properly configure secure etcd communication, your Sensu configuration will be vulnerable to unauthorized manipulation via etcd client connections.
{{% /notice %}}

To use Sensu with an external etcd cluster, you must have etcd 3.3.2 or newer.
To stand up an external etcd cluster, follow etcd's [clustering guide][2] using the same store configuration.
Do not configure external etcd in Sensu via backend command line flags or the backend configuration file (`/etc/sensu/backend.yml`).

### Configure key space access

Follow these steps to configure read and write access to the `/sensu.io/` key space for your users so you can initialize a backend that uses etcd authentication.

1. Add the `sensu` user:
{{< highlight shell >}}
etcdctl user add sensu
{{< /highlight >}}

2. Enter the `sensu` user password when prompted.

3. Create the `sensu_readwrite` role:
{{< highlight shell >}}
etcdctl role add sensu_readwrite
{{< /highlight >}}

4. Grant read/write permissions to the `sensu_readwrite` role under the `/sensu.io/` key space:
{{< highlight shell >}}
etcdctl role grant-permission sensu_readwrite readwrite --from-key '/sensu.io/'
{{< /highlight >}}

5. Grant the `sensu_readwrite` role to the `sensu` user:
{{< highlight shell >}}
etcdctl user grant-role sensu sensu_readwrite
{{< /highlight >}}

6. Confirm that the grant is configured correctly:
{{< highlight shell >}}
/opt/etcd/etcdctl user get USERNAME --detail
{{< /highlight >}}
    
    You should see the following output:
{{< highlight shell >}}
User: USERNAME

Role sensu_readwrite
KV Read:
  [/sensu.io/, <open ended>
KV Write:
  [/sensu.io/, <open ended>
{{< /highlight >}}

Etcd does not enable authentication by default, so additional configuration may be needed before etcd will enforce these controls.
See the [etcd operators documentation][12] for details.

### Start etcd

To start etcd for `backend-1` based on the [three-node configuration example][19]:

{{< code shell >}}
etcd \
--listen-client-urls "https://10.0.0.1:2379" \
--advertise-client-urls "https://10.0.0.1:2379" \
--listen-peer-urls "https://10.0.0.1:2380" \
--initial-cluster "backend-1=https://10.0.0.1:2380,backend-2=https://10.0.0.2:2380,backend-3=https://10.0.0.3:2380" \
--initial-advertise-peer-urls "https://10.0.0.1:2380" \
--initial-cluster-state "new" \
--name "backend-1" \
--trusted-ca-file=./ca.pem \
--cert-file=./backend-1.pem \
--key-file=./backend-1-key.pem \
--client-cert-auth \
--peer-trusted-ca-file=./ca.pem \
--peer-cert-file=./backend-1.pem \
--peer-key-file=./backend-1-key.pem \
--peer-client-cert-auth \
--auto-compaction-mode revision \
--auto-compaction-retention 2
{{< /code >}}

{{% notice note %}}
**NOTE**: Without the `auto-compaction-mode` and `auto-compaction-retention` flags, your database may quickly reach etcd's maximum database size limit.
{{% /notice %}}

Tell Sensu to use this external etcd data source by adding the `sensu-backend` flag `--no-embed-etcd` to the original configuration and the path to a client certificate created using your CA:

{{< code shell >}}
sensu-backend start \
--etcd-trusted-ca-file=./ca.pem \
--etcd-cert-file=./backend-1.pem \
--etcd-key-file=./backend-1-key.pem \
--etcd-client-urls=https://10.0.0.1:2379,https://10.0.0.2:2379,https://10.0.0.3:2379 \
--no-embed-etcd
{{< /code >}}

{{% notice note %}}
**NOTE**: The `etcd-client-urls` value must be a space-delimited list or a YAML array.
{{% /notice %}}

## Migrate from embedded etcd to external etcd

To migrate from embedded etcd to external etcd, first decide whether you need to migrate all of your etcd data or just your Sensu configurations.

If you need to migrate all etcd data, you must create an [etcd snapshot][9].
Use the snapshot to [restore][25] your entire cluster after setting up the new external cluster.

If you need to migrate only your Sensu configuration, you can use [sensuctl dump][24] to create a backup and use [sensuctl create][26] to import your configuration to the new external cluster.

{{% notice note %}}
**NOTE**: The sensuctl dump command does not export user passwords, and sensuctl create does not restore API keys from a sensuctl dump backup.
For this reason, you must use the [etcd snapshot and restore process](https://etcd.io/docs/latest/op-guide/recovery/) to migrate your entire embedded cluster to external etcd.
{{% /notice %}}

After you create the backups you need, follow [Use an external etcd cluster][27] to configure Sensu to use the external cluster as your datastore.

## Troubleshoot clusters

### Failure modes

See the [etcd failure modes documentation][8] for information about cluster failure modes.

### Disaster recovery

See the [etcd recovery guide][9] for disaster recovery information.

### Redeploy a cluster

To redeploy a cluster due to an issue like loss of quorum among cluster members, etcd corruption, or hardware failure, read [Remove and redeploy a cluster][23].


[1]: https://etcd.io/docs/latest/op-guide/runtime-configuration/
[2]: https://etcd.io/docs/latest/op-guide/clustering/
[3]: https://etcd.io/docs/latest/op-guide/configuration/
[4]: https://etcd.io/docs/latest/
[5]: https://etcd.io/docs/latest/platforms/
[6]: #manage-and-monitor-clusters-with-sensuctl
[7]: https://github.com/sensu/sensu-go/blob/main/docker-compose.yaml
[8]: https://etcd.io/docs/latest/op-guide/failures/
[9]: https://etcd.io/docs/latest/op-guide/recovery/
[10]: https://github.com/cloudflare/cfssl
[11]: https://etcd.io/docs/latest/op-guide/clustering/#self-signed-certificates
[12]: https://etcd.io/docs/latest/op-guide/
[13]: ../generate-certificates/
[14]: https://etcd.io/docs/latest/op-guide/runtime-configuration/
[15]: ../../../observability-pipeline/observe-schedule/backend/
[16]: ../secure-sensu/
[17]: ../../../sensuctl/
[18]: https://etcd.io/docs/current/dev-internal/discovery_protocol/#specifying-the-expected-cluster-size
[19]: #sensu-backend-configuration
[20]: ../../../api/
[21]: ../install-sensu/
[22]: #add-a-cluster-member
[23]: ../../maintain-sensu/troubleshoot/#remove-and-redeploy-a-cluster
[24]: ../../../sensuctl/back-up-recover/
[25]: https://etcd.io/docs/v3.5/op-guide/recovery/#restoring-a-cluster
[26]: ../../../sensuctl/back-up-recover/#restore-resources-from-backup
[27]: #use-an-external-etcd-cluster
