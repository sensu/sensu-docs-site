---
title: "Scale Sensu Go with Enterprise datastore"
linkTitle: "Scale with Enterprise Datastore"
description: "Here’s how to scale your monitoring to thousands of events per second with Sensu."
weight: 90
version: "5.19"
product: "Sensu Go"
platformContent: false
menu:
  sensu-go-5.19:
    parent: deploy-sensu
---

**COMMERCIAL FEATURE**: Access the datastore feature in the packaged Sensu Go distribution.
For more information, see [Get started with commercial features][3].

Sensu Go's datastore feature enables scaling your monitoring to many thousands of events per second.

For each unique entity/check pair, Sensu records the latest event object in its datastore.
By default, Sensu uses the embedded etcd datastore for event storage.
The embedded etcd datastore helps you get started, but as the number of entities and checks in your Sensu implementation grows, so does the rate of events being written to the datastore.
In a clustered deployment of etcd, whether embedded or external to Sensu, each event received by a member of the cluster must be replicated to other members, increasing network and disk IO utilization.

Our team documented configuration and testing of Sensu running on bare metal infrastructure in the [sensu/sensu-perf][1] project.
This configuration comfortably handled 12,000 Sensu agent connections (and their keepalives) and processed more than 8,500 events per second.

This rate of events should be sufficient for many installations but assumes an ideal scenario where Sensu backend nodes use direct-attached, dedicated non-volatile memory express (NVMe) storage and are connected to a dedicated LAN.
Deployments on public cloud providers are not likely to achieve similar results due to sharing both disk and network bandwidth with other tenants.
Adhering to the cloud provider's recommended practices may also become a factor because many operators are inclined to deploy a cluster across multiple availability zones.
In such a deployment cluster, communication happens over shared WAN links, which are subject to uncontrolled variability in throughput and latency.

The Enterprise datastore can help operators achieve much higher rates of event processing and minimize the replication communication between etcd peers.
The `sensu-perf` test environment comfortably handles 40,000 Sensu agent connections (and their keepalives) and processes more than 36,000 events per second under ideal conditions.

## Prerequisites

* Database server running Postgres 9.5 or later
* Postgres database (or administrative access to create one)
* Postgres user with permissions to the database (or administrative access to create such a user)
* [Licensed Sensu Go backend][3]

## Configure Postgres

Before Sensu can start writing events to Postgres, you need a database and an account with permissions to write to that database.
To provide consistent event throughput, we recommend exclusively dedicating your Postgres instance to storage of Sensu events.

If you have administrative access to Postgres, you can create the database and user:

{{< code shell >}}
$ sudo -u postgres psql
postgres=# CREATE DATABASE sensu_events;
CREATE DATABASE
postgres=# CREATE USER sensu WITH ENCRYPTED PASSWORD 'mypass';
CREATE ROLE
postgres=# GRANT ALL PRIVILEGES ON DATABASE sensu_events TO sensu;
GRANT
postgres-# \q
{{< /code >}}

With this configuration complete, Postgres will have a `sensu_events` database for storing Sensu events and a `sensu` user with permissions to that database.

By default, the Postgres user you've just added will not be able to authenticate via password, so you'll also need to make a change to the `pg_hba.conf` file.
The required change will depend on how Sensu will connect to Postgres.
In this case, you'll configure Postgres to allow the `sensu` user to connect to the `sensu_events` database from any host using an [md5][5]-encrypted password:

{{< code shell >}}
# make a copy of the current pg_hba.conf
sudo cp /var/lib/pgsql/data/pg_hba.conf /var/tmp/pg_hba.conf.bak
# give sensu user permissions to connect to sensu_events database from any IP address
echo 'host sensu_events sensu 0.0.0.0/0 md5' | sudo tee -a /var/lib/pgsql/data/pg_hba.conf
# restart postgresql service to activate pg_hba.conf changes
sudo systemctl restart postgresql
{{< /code >}}

With this configuration complete, you can configure Sensu to store events in your Postgres database.

## Configure Sensu

If your Sensu backend is already licensed, the configuration for routing events to Postgres is relatively straightforward.
Create a `PostgresConfig` resource that describes the database connection as a data source name (DSN):

{{< language-toggle >}}

{{< code yml >}}
type: PostgresConfig
api_version: store/v1
metadata:
  name: postgres01
spec:
  dsn: "postgresql://sensu:mypass@10.0.2.15:5432/sensu_events?sslmode=disable"
  pool_size: 20
{{< /code >}}

{{< code json >}}
{
  "type": "PostgresConfig",
  "api_version": "store/v1",
  "metadata": {
    "name": "my-postgres"
  },
  "spec": {
    "dsn": "postgresql://sensu:mypass@10.0.2.15:5432/sensu_events",
    "pool_size": 20
  }
}
{{< /code >}}

{{< /language-toggle >}}

This configuration is written to disk as `my-postgres.yml`, and you can install it using `sensuctl`:

{{< code shell >}}
sensuctl create -f my-postgres.yml
{{< /code >}}

The Sensu backend is now configured to use Postgres for event storage!

In the web UI and in sensuctl, event history will appear incomplete.
When Postgres configuration is provided and the backend successfully connects to the database, etcd event history is not migrated.
New events will be written to Postgres as they are processed, with the Postgres datastore ultimately being brought up to date with the current state of your monitored infrastructure.

Aside from event history, which is not migrated from etcd, there's no observable difference when using Postgres as the event store, and neither interface supports displaying the PostgresConfig type.

To verify that the change was effective and your connection to Postgres was successful, look at the [sensu-backend log][4]:

{{< code shell >}}
{"component":"store","level":"warning","msg":"trying to enable external event store","time":"2019-10-02T23:31:38Z"}
{"component":"store","level":"warning","msg":"switched event store to postgres","time":"2019-10-02T23:31:38Z"}
{{< /code >}}

You can also use `psql` to verify that events are being written to the `sensu_events` database.
This code illustrates connecting to the `sensu_events` database, listing the tables in the database, and requesting a list of all entities reporting keepalives:

{{< code shell >}}
postgres=# \c sensu_events
You are now connected to database "sensu_events" as user "postgres".
sensu_events=# \dt
             List of relations
 Schema |       Name        | Type  | Owner 
--------+-------------------+-------+-------
 public | events            | table | sensu
 public | migration_version | table | sensu
(2 rows)
sensu_events=# select sensu_entity from events where sensu_check = 'keepalive';
 sensu_entity 
--------------
 i-414141
 i-424242
 i-434343
(3 rows)
{{< /code >}}

## Revert to the built-in datastore

If you want to revert to the default etcd event store, delete the PostgresConfig resource.
In this example, my-postgres.yml contains the same configuration you used to configure the Enterprise event store earlier in this guide:

{{< code shell >}}
sensuctl delete -f my-postgres.yml
{{< /code >}}

To verify that the change was effective, look for messages similar to these in the [sensu-backend log][4]:

{{< code shell >}}
{"component":"store","level":"warning","msg":"store configuration deleted","store":"/sensu.io/api/enterprise/store/v1/provider/postgres01","time":"2019-10-02T23:29:06Z"}
{"component":"store","level":"warning","msg":"switched event store to etcd","time":"2019-10-02T23:29:06Z"}
{{< /code >}}

Similar to enabling Postgres, switching back to the etcd datastore does not migrate current event data from one store to another.
You may see old events in the web UI or sensuctl output until the etcd datastore catches up with the current state of your monitored infrastructure.

## Configure Postgres streaming replication

Postgres supports an active standby by using [streaming replication][6].
All Sensu events written to the primary Postgres server will be replicated to the standby server.

{{% notice note %}}
**NOTE**: Paths and service names may vary based on your operating system.
{{% /notice %}}

This section describes how to configure PostgreSQL streaming replication in four steps.

### Step 1: Create and add the replication role

If you have administrative access to Postgres, you can create the replication role:

{{< code shell >}}
$ sudo -u postgres psql
postgres=# CREATE ROLE repl PASSWORD 'secret' LOGIN REPLICATION;
CREATE ROLE
postgres-# \q
{{< /code >}}

Then, you must add the replication role to `pg_hba.conf` using an [md5-encrypted password][5].
Make a copy of the current `pg_hba.conf`:

{{< code shell >}}
sudo cp /var/lib/pgsql/data/pg_hba.conf /var/tmp/pg_hba.conf.bak
{{< /code >}}

Next, give the repl user permissions to replicate from the standby host.
In the following command, replace `STANDBY_IP` with the IP address of your standby host:

{{< code shell >}}
export STANDBY_IP=192.168.52.10
echo "host replication repl ${STANDYB_IP}/32 md5" | sudo tee -a /var/lib/pgsql/data/pg_hba.conf
{{< /code >}}

Restart the PostgreSQL service to activate the `pg_hba.conf` changes:

{{< code shell >}}
sudo systemctl restart postgresql
{{< /code >}}

### Step 2: Set streaming replication configuration parameters

The next step is to set the streaming replication configuration parameters on the primary Postgres host.
Begin by making a copy of the `postgresql.conf`:

{{< code shell >}}
sudo cp -a /var/lib/pgsql/data/postgresql.conf /var/lib/pgsql/data/postgresql.conf.bak
{{< /code >}}

Next, append the necessary configuration options.

{{< code shell >}}
echo 'wal_level = hot_standby' | sudo tee -a /var/lib/pgsql/data/postgresql.conf
{{< /code >}}

Set the maximum number of concurrent connections from the standby servers:

{{< code shell >}}
echo 'max_wal_senders = 5' | sudo tee -a /var/lib/pgsql/data/postgresql.conf
{{< /code >}}

To prevent the primary server from removing the WAL segments required for the standby server before shipping them, set the minimum number of segments retained in the `pg_xlog` directory:

{{< code shell >}}
echo 'wal_keep_segments = 32' | sudo tee -a /var/lib/pgsql/data/postgresql.conf
{{< /code >}}

At minimum, the number of `wal_keep_segments` should be larger than the number of segments generated between the beginning of online backup and the startup of streaming replication.

{{% notice note %}}
**NOTE**: If you enable WAL archiving to an archive directory accessible from the standby, this may not be necessary.
{{% /notice %}}

Restart the PostgreSQL service to activate the `postgresql.conf` changes:

{{< code shell >}}
sudo systemctl restart postgresql
{{< /code >}}

### Step 3: Bootstrap the standby host

The standby host must be bootstrapped using the `pg_basebackup` command.
This process will copy all configuration files from the primary as well as databases.

If the standby host has ever run Postgres, you must empty the data directory:

{{< code shell >}}
sudo systemctl stop postgresql
sudo mv /var/lib/pgsql/data /var/lib/pgsql/data.bak
{{< /code >}}

Make the standby data directory:

{{< code shell >}}
sudo install -d -o postgres -g postgres -m 0700 /var/lib/pgsql/data
{{< /code >}}

And then bootstrap the standby data directory:

{{< code shell >}}
export PRIMARY_IP=192.168.52.11
sudo -u postgres pg_basebackup -h $PRIMARY_IP -D /var/lib/pgsql/data -P -U repl -R --xlog-method=stream
Password: 
30318/30318 kB (100%), 1/1 tablespace
{{< /code >}}

### Step 4: Confirm replication

To confirm your configuration is working properly, start by removing configurations that are only for the primary:

{{< code shell >}}
sudo sed -r -i.bak '/^(wal_level|max_wal_senders|wal_keep_segments).*/d' /var/lib/pgsql/data/postgresql.conf
{{< /code >}}

Start the PostgreSQL service:

{{< code shell >}}
sudo systemcl start postgresql
{{< /code >}}

To verify that the replication is taking place, check the commit log location on the primary and standby hosts:

{{< code shell >}}
# From master
sudo -u postgres psql -c "select pg_current_xlog_location()"
 pg_current_xlog_location 
--------------------------
 0/3000568
(1 row)
# From standby
sudo -u postgres psql -c "select pg_last_xlog_receive_location()"
 pg_last_xlog_receive_location 
-------------------------------
 0/3000568
(1 row)

# From standby
sudo -u postgres psql -c "select pg_last_xlog_replay_location()"
 pg_last_xlog_replay_location 
------------------------------
 0/3000568
(1 row)
{{< /code >}}

With this configuration complete, your Sensu events will be replicated to the standby host.


[1]: https://github.com/sensu/sensu-perf
[3]: ../../../commercial/
[4]: ../../maintain-sensu/troubleshoot/#log-file-locations
[5]: https://www.postgresql.org/docs/9.5/auth-methods.html#AUTH-PASSWORD
[6]: https://wiki.postgresql.org/wiki/Streaming_Replication
