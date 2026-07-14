<div align="center">

# Load Balancers

Implementations of common load balancing algorithms from first principles.

</div>

---

# Overview

Load balancing is the process of distributing incoming requests across multiple backend servers to improve performance, scalability, availability, and fault tolerance.

Different routing algorithms make different trade-offs. Some prioritize simplicity, others prioritize fairness, latency, session affinity, or cluster scalability. There is no universally "best" algorithm—the appropriate choice depends on the workload and system architecture.

This module implements the following routing algorithms from scratch:

- Round Robin
- Weighted Round Robin
- Random Routing
- Weighted Random Routing
- Least Connections
- Weighted Least Connections
- Least Response Time
- IP Hash (Client Hash)
- Consistent Hashing

---

# Objectives

- Understand the intuition behind each routing algorithm
- Implement every algorithm from first principles
- Compare the strengths and weaknesses of each approach
- Explore where each algorithm is used in production
- Build an understanding of how modern load balancers make routing decisions

---

# Implemented Algorithms

| Algorithm | Status |
|-----------|:------:|
| Round Robin | ✅ |
| Weighted Round Robin | ✅ |
| Random Routing | ✅ |
| Weighted Random Routing | ✅ |
| Least Connections | ✅ |
| Weighted Least Connections | ✅ |
| Least Response Time | ✅ |
| IP Hash (Client Hash) | ✅ |
| Consistent Hashing | ✅ |

---

# Routing Algorithms

## 1. Round Robin

Routes requests sequentially across all available backend servers.

```
Request 1 → Server A
Request 2 → Server B
Request 3 → Server C
Request 4 → Server A
```

### Advantages

- Extremely simple
- Constant-time routing
- Even request distribution
- No runtime metrics required

### Trade-offs

- Assumes all backend servers are identical
- Ignores CPU, memory and current load
- Performs poorly when requests vary significantly in execution time

### Common Use Cases

- Stateless HTTP APIs
- Small backend clusters
- Homogeneous infrastructure

---

## 2. Weighted Round Robin

Extends Round Robin by assigning each server a weight representing its relative capacity.

Servers with higher weights receive proportionally more requests.

```
Weight 1 → A
Weight 2 → B
Weight 4 → C

Distribution

A
B
B
C
C
C
C
```

### Advantages

- Supports heterogeneous hardware
- Predictable traffic distribution
- Easy to configure

### Trade-offs

- Weights are static
- Does not react to changing backend load
- Fast servers can still become overloaded

### Common Use Cases

- Mixed hardware clusters
- Cloud deployments with different instance sizes

---

## 3. Random Routing

Each request is routed to a randomly selected backend server.

```
Request 1 → Server C
Request 2 → Server A
Request 3 → Server B
Request 4 → Server C
```

### Advantages

- Extremely simple
- Stateless
- Naturally distributes requests over time

### Trade-offs

- Uneven short-term distribution
- No awareness of server capacity
- No awareness of runtime load

### Common Use Cases

- Small deployments
- Simulations
- Demonstrations
- Lightweight routing layers

---

## 4. Weighted Random Routing

Randomly selects a backend while respecting configured server weights.

Servers with larger weights have a higher probability of being selected.

### Advantages

- Supports heterogeneous infrastructure
- Simple implementation
- Naturally randomized distribution

### Trade-offs

- Still ignores runtime metrics
- Distribution is probabilistic rather than deterministic
- Temporary imbalance is expected

### Common Use Cases

- Mixed-capacity clusters
- Traffic sampling
- Canary deployments

---

## 5. Least Connections

Routes requests to the backend with the fewest active connections.

### Advantages

- Adapts to current backend load
- Excellent for long-lived connections
- Better distribution when request durations vary

### Trade-offs

- Assumes identical server capacity
- Requires connection tracking
- Active connections are not always proportional to actual workload

### Common Use Cases

- TCP load balancing
- WebSockets
- Streaming services
- Long-running HTTP requests

---

## 6. Weighted Least Connections

Extends Least Connections by incorporating server capacity through configurable weights.

Instead of minimizing:

```
connections
```

it minimizes:

```
connections / weight
```

### Advantages

- Load aware
- Capacity aware
- Excellent for heterogeneous clusters
- Common production routing strategy

### Trade-offs

- Requires accurate server weights
- More computational overhead than simple algorithms
- Connection count may still not reflect true resource consumption

### Common Use Cases

- Production API gateways
- Reverse proxies
- Enterprise load balancers

---

## 7. Least Response Time

Routes requests to the backend with the lowest observed response latency.

### Advantages

- Adapts to backend performance
- Optimizes end-user latency
- Automatically avoids slower servers

### Trade-offs

- Requires continuous latency measurements
- Sensitive to temporary latency spikes
- Historical measurements may become stale
- Response time alone does not always reflect server health

### Common Use Cases

- Latency-sensitive APIs
- Microservices
- User-facing web applications

---

## 8. IP Hash (Client Hash)

Hashes the client IP address to consistently route requests to the same backend.

```
hash(client_ip) % number_of_servers
```

### Advantages

- Provides sticky sessions
- Simple implementation
- No server-side session lookup required

### Trade-offs

- Cluster changes cause widespread client remapping
- Poor scalability
- Uneven distribution when client IPs are skewed
- Clients behind NAT may overload a single backend

### Common Use Cases

- Legacy session-based applications
- Stateful web applications
- Applications without shared session storage

---

## 9. Consistent Hashing

Maps both servers and clients onto a hash ring.

Requests are routed to the first server encountered when moving clockwise around the ring.

Unlike traditional hashing, adding or removing a server only remaps a small subset of clients.

### Advantages

- Minimal request redistribution
- Excellent horizontal scalability
- Supports virtual nodes
- Widely used in distributed systems

### Trade-offs

- More complex implementation
- Requires virtual nodes for even distribution
- More difficult to reason about than traditional algorithms

### Common Use Cases

- Distributed caches
- Distributed databases
- Sharded storage systems
- Content delivery networks (CDNs)
- Service meshes

---

# Learning Progression

The algorithms naturally build upon one another, introducing increasingly sophisticated routing strategies.

```
Round Robin
        │
        ▼
Weighted Round Robin
        │
        ▼
Random Routing
        │
        ▼
Weighted Random Routing
        │
        ▼
Least Connections
        │
        ▼
Weighted Least Connections
        │
        ▼
Least Response Time
        │
        ▼
IP Hash
        │
        ▼
Consistent Hashing
```

The progression introduces increasingly advanced concepts:

- Deterministic scheduling
- Weighted routing
- Probabilistic routing
- Runtime load awareness
- Capacity awareness
- Latency-aware routing
- Session affinity
- Distributed hashing
- Horizontal scalability

---

# Comparison

| Algorithm | Load Aware | Capacity Aware | Session Affinity | Cluster Scaling | Runtime Metrics | Complexity | Typical Use Cases |
|-----------|:----------:|:--------------:|:----------------:|:---------------:|:---------------:|:----------:|-------------------|
| Round Robin | ❌ | ❌ | ❌ | ✅ | ❌ | Very Low | Stateless APIs |
| Weighted Round Robin | ❌ | ✅ | ❌ | ✅ | ❌ | Low | Mixed-capacity servers |
| Random Routing | ❌ | ❌ | ❌ | ✅ | ❌ | Very Low | Simple routing, testing |
| Weighted Random Routing | ❌ | ✅ | ❌ | ✅ | ❌ | Low | Canary deployments, weighted traffic |
| Least Connections | ✅ | ❌ | ❌ | ✅ | Active Connections | Medium | TCP, WebSockets |
| Weighted Least Connections | ✅ | ✅ | ❌ | ✅ | Active Connections | Medium | Production load balancers |
| Least Response Time | ✅ | Partial | ❌ | ✅ | Response Latency | High | Latency-sensitive services |
| IP Hash | ❌ | ❌ | ✅ | ❌ | ❌ | Low | Sticky sessions |
| Consistent Hashing | ❌ | Via Virtual Nodes | ✅ | ⭐ Excellent | ❌ | High | Distributed systems, sharding |

---

# Choosing the Right Algorithm

| If your priority is... | Recommended Algorithm |
|------------------------|-----------------------|
| Simplicity | Round Robin |
| Different server capacities | Weighted Round Robin |
| Randomized request distribution | Random Routing |
| Weighted randomized distribution | Weighted Random Routing |
| Long-lived connections | Least Connections |
| Production load balancing | Weighted Least Connections |
| Lowest response latency | Least Response Time |
| Sticky sessions | IP Hash |
| Distributed caching or sharding | Consistent Hashing |

---

# Production Examples

| Technology | Routing Algorithm(s) |
|------------|----------------------|
| NGINX | Round Robin, Weighted Round Robin, Least Connections, IP Hash |
| HAProxy | Round Robin, Least Connections, Least Response Time, Consistent Hashing |
| Envoy Proxy | Round Robin, Least Request, Ring Hash (Consistent Hashing) |
| Traefik | Round Robin, Weighted Round Robin |
| Kubernetes Services | Round Robin (IPVS), Session Affinity |
| Redis Cluster | Consistent Hashing concepts |
| Apache Cassandra | Consistent Hashing with Virtual Nodes |
| Amazon Dynamo | Consistent Hashing |
| Memcached Clients | Consistent Hashing |