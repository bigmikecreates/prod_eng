
## LOAD BALANCERS

## CACHES

## API GATEWAYS

```
Infrastructure Components
└── Traffic Management
    └── API Gateway
        ├── Edge API Gateway
        ├── Internal API Gateway
        ├── Backend for Frontend
        ├── GraphQL Gateway
        ├── Event Gateway
        └── AI/LLM Gateway
```

### 2. INTERNAL API GATEWAY

This is a traffic management and policy-enforcement infrastructure component for private service-to-service communication. It often sits inside a VPC, Kubernetes cluster, private subnet, VPN, or service mesh. It primarily provides a controlled entry point for **east-west traffic** (traffic moving between internal services, as opposed to ***north-south traffic*** which is traffic entering/leaving the system).

```
External Client
      │
      ▼
Edge API Gateway
      │
      ▼
Private Network
      │
      ├── Internal API Gateway
      │       ├── Users Service
      │       ├── Orders Service
      │       └── Payments Service
      │
      └── Other internal systems
```

Its purposes are to:
1. Centralize control over how internal callers access backend services.
2. Forward traffic.

In such a system, the gateway abstracts the following details that the caller does not need to know:
- The current IP address of the user's service
- How many users-service instances exist
- Which instance is healthy
- Whether the service requires retries
- Whether the route has moved
- Which credentials the destination expects

It overlaps with the following categories:
1. Traffic Management
2. Security
3. Reliability 
4. Observability
5. Service Discovery
6. Configuration Management

#### ONTOLOGY

1. Gateway: The running infrastructure component that accepts and forwards requests.
2. Caller: THe internal workload initiating the request (e.g. orders-service, billing-worker, admin-api).
3. Service: A logical downstream application, which may be one process or a pool of instances (e.g. users, orders, payments, inventory)
4. Endpoint: A concrete network destination for a service (e.g. 10.0.2.14:8000, 10.0.2.15:8000, 10.0.2.16:8000).
5. Route: A rule mapping an incoming request to a downstream service (e.g. /internal/users/* -> users-service, /internal/orders/* -> orders-service).
6. Route Table: The collection of configured routes (e.g. RouteTable -> users route - orders route - payments route).
7. Policy: A rule controlling whether or how a request may proceed (e.g. AutenticationPolicy, AuthorizationPolicy, RetryPolicy, RateLimitPolicy, TimeoutPolicy, etc.)
8. Identity: The authenticated identity of the calling workload (e.g. service:orders-service, namespace:production, tenant:internal-platform).
9. Credential: Evidence used to prove identity (e.g. JWT, mTLS certificate, API key, workload identity token).
10. Request Context: Metadata propagated through the request lifecycle.
11. Upstream and Downstream: This is often defined by the developer themselves, however some proxy products often use "upstream" to mean the backend destination (i.e. Upstream caller -> Internal Gateway -> Downstream service).


An internal gateway's core operations include:

1. Route matching
2. Caller authentication
3. Authorization
4. Service discovery
5. Endpoint selection
6. Request forwarding
7. Context propagation
8. Response forwarding


#### SECURITY

Regardless of an API being private or public, a private API does not automatically mean it should be trusted as they may still contain:

1. Compromised workloads.
2. An incorrectly configured service.
3. Malicious insiders.
4. Lateral movement after a breach.
5. Accidental access from unrelated services.

It is therefore crucial to ensure that every workload is authenticated, every operation is authorized, and every connection should be encrypted where practical. Some authentication options include:

1. Static service token: This is a fixed shared secret used by one service to authenticate to another (e.g. X-Service-Token: shared-secret). The receiving service checks whether the token matches its configured secret. This is also the weakest authentication method.
2. Signed service JWT: This is a short-lived token containing claims about the calling service. The token is cryptographically signed. The receiver verifies the signature and checks claims such as i) `sub`: which service is calling, ii) `aud`: which service the token is intended for, iii) `scope`: what actions are allowed, and iv) `exp`: when the token expires.
3. mTLS: For this authentication method, both sides (caller and gateway) present certificates. The caller presents their certificate to the gateway, which validates the caller's identity. The gateway the presents its certificate to the caller to validate the gateway. The certificate may encode e.g. `spiffe://production/orders-service`.
4. Workload identity: These are cloud/cluster-issued identities (e.g. AWS IAM role, Azure Managed Identity, GCP Workload Identity, Kubernetes ServiceAccount, SPIFFE identity).