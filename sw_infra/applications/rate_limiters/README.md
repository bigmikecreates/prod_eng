<div align="center">

# Rate Limiters

Implementations of common rate limiting algorithms from first principles.

This module forms part of a larger production engineering project focused on implementing the core algorithms and components used throughout backend engineering, distributed systems, API gateways, reverse proxies, and cloud infrastructure.

</div>

---

# Overview

Rate limiting is the process of controlling how many requests a client, user, or service may perform over a period of time.

It is a fundamental component of production systems and is commonly used to:

- Protect backend services from overload
- Prevent abuse and denial-of-service attacks
- Enforce API quotas
- Ensure fair resource allocation
- Smooth traffic spikes
- Improve overall system stability

Different rate limiting algorithms make different trade-offs between accuracy, memory usage, burst tolerance, fairness, and computational complexity. There is no universally "best" algorithm—the appropriate choice depends on the workload and system requirements.

---

# Objectives

- Understand the intuition behind common rate limiting algorithms
- Implement each algorithm from first principles
- Compare the trade-offs between different approaches
- Explore where each algorithm is used in production systems
- Build an understanding of how modern APIs and gateways enforce request limits

---

# Implemented Algorithms

| Algorithm | Status |
|-----------|:------:|
| Fixed Window Counter | ✅ |
| Sliding Window Log | ✅ |
| Sliding Window Counter | ✅ |
| Token Bucket | ✅ |
| Leaky Bucket | ✅ |

---

# Algorithms

## 1. Fixed Window Counter

Counts requests within a fixed time interval.

```
Window: 12:00 → 12:01

Maximum Requests = 100
```

When the next window begins, the counter resets.

### Advantages

- Extremely simple
- Constant-time operations
- Very low memory usage
- Easy to distribute using Redis

### Trade-offs

- Boundary problem allows burst traffic
- Requests at the end and beginning of adjacent windows may effectively double the configured limit
- Lowest accuracy of the common algorithms

### Common Use Cases

- Internal APIs
- Low-traffic services
- Basic request throttling

---

## 2. Sliding Window Log

Stores the timestamp of every request.

Before processing a request, timestamps outside the configured time window are removed.

### Advantages

- Very accurate
- True rolling time window
- Fair request distribution

### Trade-offs

- High memory usage
- Cleanup cost increases with request volume
- Does not scale well for extremely high traffic

### Common Use Cases

- Authentication endpoints
- Security-sensitive APIs
- Administrative interfaces

---

## 3. Sliding Window Counter

Approximates a rolling window by combining counters from the current and previous windows.

Rather than storing every request, only two counters are maintained.

### Advantages

- Low memory usage
- Near-sliding-window accuracy
- Constant-time operations
- Suitable for high throughput

### Trade-offs

- Slight approximation error
- More complex than Fixed Window Counter
- Less accurate than Sliding Window Log

### Common Use Cases

- Public APIs
- High-volume services
- Distributed rate limiting

---

## 4. Token Bucket

Tokens are added to a bucket at a constant rate.

Each request consumes one token.

Requests are rejected once the bucket becomes empty.

```
Bucket Capacity = 100

Refill Rate = 10 tokens/sec
```

### Advantages

- Supports controlled bursts
- Excellent throughput
- Constant-time operations
- Widely used in production

### Trade-offs

- Requires refill calculations
- Slightly more complex implementation
- Requires synchronized timing in distributed environments

### Common Use Cases

- Public APIs
- Cloud providers
- API gateways
- Client SDKs

---

## 5. Leaky Bucket

Incoming requests enter a queue.

Requests leave the queue at a fixed rate.

```
Incoming Requests

██████████

↓

Queue

██████████

↓

Outgoing Requests

█
█
█
█
```

### Advantages

- Smooth traffic
- Predictable request rate
- Protects downstream services
- Constant-time operations

### Trade-offs

- Rejects legitimate bursts
- Queue introduces latency
- Less flexible than Token Bucket

### Common Use Cases

- Reverse proxies
- Network routers
- Traffic shaping
- Load regulation

---

# Learning Progression

The algorithms naturally evolve toward increasingly sophisticated traffic control strategies.

```
Fixed Window Counter
          │
          ▼
Sliding Window Log
          │
          ▼
Sliding Window Counter
          │
          ▼
Token Bucket
          │
          ▼
Leaky Bucket
```

The progression introduces increasingly advanced concepts:

- Request counting
- Rolling time windows
- Memory optimization
- Burst tolerance
- Traffic shaping
- Constant-rate processing

---

# Comparison

| Algorithm | Burst Support | Memory Usage | Accuracy | Runtime Complexity | Typical Use Cases |
|------------|:-------------:|:------------:|:--------:|:------------------:|-------------------|
| Fixed Window Counter | ⭐ High | ⭐ Very Low | Low | O(1) | Simple APIs |
| Sliding Window Log | Medium | High | ⭐ Excellent | O(n) Cleanup | Security-sensitive APIs |
| Sliding Window Counter | Medium | Low | High | O(1) | High-throughput APIs |
| Token Bucket | ⭐ Excellent | Low | High | O(1) | API Gateways, Cloud Services |
| Leaky Bucket | None | Low | High | O(1) | Traffic Shaping, Networking |

---

# Trade-offs

| Algorithm | Primary Strength | Primary Weakness |
|------------|-----------------|------------------|
| Fixed Window Counter | Extremely simple | Boundary bursts |
| Sliding Window Log | Highest accuracy | High memory usage |
| Sliding Window Counter | Good accuracy with low memory | Approximation error |
| Token Bucket | Supports burst traffic | Requires refill calculations |
| Leaky Bucket | Produces smooth traffic | Rejects legitimate bursts |

---

# Choosing the Right Algorithm

| If your priority is... | Recommended Algorithm |
|------------------------|-----------------------|
| Simplest implementation | Fixed Window Counter |
| Highest accuracy | Sliding Window Log |
| Memory efficiency | Sliding Window Counter |
| Burst-friendly APIs | Token Bucket |
| Constant request throughput | Leaky Bucket |

---

# Production Examples

| Technology | Algorithm(s) |
|------------|--------------|
| NGINX | Leaky Bucket |
| Envoy Proxy | Token Bucket |
| Kong Gateway | Fixed Window, Sliding Window |
| Cloudflare | Token Bucket, Sliding Window |
| AWS API Gateway | Token Bucket |
| Google Cloud Endpoints | Token Bucket |
| GitHub API | Token Bucket |
| Stripe API | Token Bucket |
| Redis-based Rate Limiters | Fixed Window, Sliding Window |

---

# Production Engineering Perspective

The evolution of rate limiting algorithms reflects increasingly sophisticated approaches to controlling request throughput.

```
Request Counting
        │
        ▼
Moving Time Windows
        │
        ▼
Memory Optimization
        │
        ▼
Burst Control
        │
        ▼
Traffic Shaping
```

Each algorithm solves a different production problem rather than replacing the previous one.

For example:

- **Fixed Window Counter** prioritizes simplicity.
- **Sliding Window Log** prioritizes accuracy.
- **Sliding Window Counter** balances accuracy and memory efficiency.
- **Token Bucket** prioritizes burst tolerance.
- **Leaky Bucket** prioritizes smooth, predictable traffic.
