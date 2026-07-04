# Session Affinity (Sticky Sessions)

## Overview

**Session affinity** (also known as **sticky sessions**) is a load balancing strategy where a client is consistently routed to the **same backend server** for the duration of a session.

Without session affinity, every request is treated independently by the load balancer.

---

## Without Session Affinity

Imagine an application with three backend servers.

```text
          Client
             │
             ▼
     Load Balancer
      ┌─────┼─────┐
      │     │     │
      ▼     ▼     ▼
 Server A Server B Server C
```

Requests from a single client might be distributed like this:

```text
Request 1 → Server A
Request 2 → Server C
Request 3 → Server B
Request 4 → Server A
```

This approach works well when backend servers are **stateless**, meaning they do not store client-specific information in memory.

---

## With Session Affinity

With session affinity enabled, the load balancer remembers which server initially handled a client and continues routing subsequent requests to that same server.

Client 123:

```text
Request 1 → Server B
Request 2 → Server B
Request 3 → Server B
Request 4 → Server B
```

A different client may be assigned elsewhere.

Client 456:

```text
Request 1 → Server C
Request 2 → Server C
Request 3 → Server C
```

Each client remains "sticky" to its assigned backend server.

---

## Why Is Session Affinity Needed?

Suppose your application stores user session data directly in server memory.

Server A:

```text
User: Mike

Shopping Cart
├── Shoes
└── Laptop
```

The user's next request arrives.

If the load balancer instead routes the request to **Server B**:

```text
Shopping Cart
└── (empty)
```

From the user's perspective, their shopping cart has disappeared because Server B has no knowledge of the session stored on Server A.

Session affinity prevents this by ensuring Mike continues communicating with **Server A** throughout the session.

---

# Common Implementation Methods

## 1. Cookie-Based Affinity (Most Common)

The load balancer stores the assigned server inside a cookie.

Response:

```http
Set-Cookie: SERVER_ID=A
```

Future requests automatically include:

```http
Cookie: SERVER_ID=A
```

The load balancer reads the cookie and forwards the request back to **Server A**.

---

## 2. Client IP Hashing

The load balancer computes a hash using the client's IP address.

```python
server = hash(client_ip) % number_of_servers
```

Example:

```text
192.168.1.10
      │
      ▼
  hash(IP)
      │
      ▼
  Server B
```

Every request from that IP address is routed to **Server B**.

### Drawbacks

- Multiple users may share the same public IP (NAT).
- Mobile devices frequently change IP addresses.
- IPv6 privacy addresses may rotate automatically.

---

## 3. Session ID Hashing

Instead of hashing the client's IP, the load balancer hashes a session identifier.

```text
 Session ID
      │
      ▼
     Hash
      │
      ▼
 Assigned Server
```

This generally provides more reliable affinity than client IP hashing.

---

# Disadvantages

## Uneven Load Distribution

Suppose the current user distribution looks like:

```text
Server A → 500 users
Server B → 120 users
Server C →  90 users
```

Even if Server A becomes overloaded, all existing sticky sessions continue being routed there.

---

## Server Failure

Suppose Server A crashes.

```text
 User
  │
  ▼
Server A ❌
```

If session data exists only in Server A's memory:

- Users may be logged out.
- Shopping carts may disappear.
- Session state is lost.

---

## Harder to Scale

Initially:

```text
Server A
Server B
Server C
```

After adding another server:

```text
Server A
Server B
Server C
Server D
```

Existing sticky sessions continue communicating with their originally assigned servers until those sessions expire.

As a result, Server D initially receives relatively little traffic.

---

# Modern Approach: Stateless Applications

Modern distributed systems typically avoid sticky sessions by making application servers **stateless**.

Instead of storing session information locally, servers retrieve it from shared infrastructure such as:

- Redis
- Distributed caches
- Shared databases
- Signed JWTs

Architecture:

```text
                 Client
                    │
                    ▼
            Load Balancer
         ┌──────┼──────┐
         ▼      ▼      ▼
     Server A Server B Server C
         │      │      │
         └──────┼──────┘
                │
                ▼
              Redis
```

Because every server has access to the shared session store, any healthy server can process any request.

---

# When Should You Use Session Affinity?

Session affinity is appropriate when:

- Legacy applications store session state in memory.
- Session state is expensive to reconstruct.
- Migrating to a stateless architecture is impractical.

---

# When Should You Avoid It?

For modern cloud-native systems, prefer designing services to be **stateless** whenever possible.

Benefits include:

- Better horizontal scalability
- Improved fault tolerance
- Easier autoscaling
- Better load balancing
- Greater resilience during server failures

---

# Summary

- **Session affinity** (sticky sessions) ensures a client consistently communicates with the same backend server.
- It is primarily used by stateful applications that store session data in server memory.
- Common implementations include:
  - Cookie-based affinity
  - Client IP hashing
  - Session ID hashing
- Sticky sessions simplify stateful applications but reduce load balancing flexibility.
- Modern architectures instead favor **stateless application servers** backed by shared session stores such as Redis or JWT-based authentication.