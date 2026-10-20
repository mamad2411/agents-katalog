# Skill: Service Exposure via Private Link (`pl_service_exposure`)

Expose your own services privately to consumers in other VNets, subscriptions, tenants, or clouds using Azure Private Link Service, AWS PrivateLink, and GCP Private Service Connect.

---

## When to Use Service Exposure

| Scenario | Solution |
|---|---|
| SaaS provider sharing service with customers privately | Private Link Service / PrivateLink / PSC |
| Internal shared service consumed by multiple business units | Private Link Service across subscriptions |
| Cross-cloud private API access | Private Link + VPN/Interconnect |
| Partner integration without public internet | Cross-tenant Private Link |

---

## Azure Private Link Service

Azure Private Link Service allows you to expose a service behind a **Standard Load Balancer** so that consumers in other VNets/subscriptions/tenants can connect via private endpoints.

### Architecture

```
Producer VNet                          Consumer VNet
┌────────────────────────┐             ┌──────────────────────┐
│ Standard Load Balancer │             │                      │
│ ┌──────────────────┐   │             │  Private Endpoint    │
│ │ Backend Pool     │   │  NAT        │  (10.2.0.5)          │
│ │ (VMs / VMSS)     │◄──┼────────────◄┤                      │
│ └──────────────────┘   │             │  Consumer connects   │
│                        │             │  to 10.2.0.5         │
│ Private Link Service   │             └──────────────────────┘
│ (NAT to 10.1.0.0/24)  │
└────────────────────────┘
```

### Deployment

```bash
# Step 1: Create Standard Load Balancer with backend pool (skip if exists)
az network lb create \
  --resource-group myRG --name myLB --sku Standard \
  --frontend-ip-name myFrontend --backend-pool-name myBackend \
  --vnet-name producerVNet --subnet workloadSubnet

# Step 2: Create the Private Link Service
az network private-link-service create \
  --resource-group myRG \
  --name myPLS \
  --vnet-name producerVNet \
  --subnet natSubnet \
  --lb-name myLB \
  --lb-frontend-ip-configs myFrontend \
  --location eastus

# Step 3: Configure visibility and auto-approval
az network private-link-service update \
  --resource-group myRG \
  --name myPLS \
  --visibility "*" \
  --auto-approval "subscription-id-1" "subscription-id-2"
```

**Key requirements:**
- **Standard Load Balancer** is mandatory (Basic LB not supported).
- **NAT subnet**: A dedicated subnet for the PLS. The PLS NATs consumer PE IPs to IPs in this subnet.
- **Visibility**: Controls who can discover the PLS. Use `*` for any subscription or restrict to specific subscription IDs.
- **Auto-approval**: Subscriptions listed here can create PEs without manual approval.
- **TCP proxy protocol v2**: Optionally enable to pass the consumer's private endpoint IP to your backend (for logging, access control).

### Consumer Side (Creating PE to your PLS)

```bash
# Consumer creates PE pointing to the PLS resource ID
az network private-endpoint create \
  --resource-group consumerRG \
  --name myPEtoService \
  --vnet-name consumerVNet \
  --subnet peSubnet \
  --private-connection-resource-id /subscriptions/.../privateLinkServices/myPLS \
  --connection-name myConnection

# Alias-based connection (cross-tenant — consumer doesn't need resource ID)
az network private-endpoint create \
  --resource-group consumerRG \
  --name myPEtoService \
  --vnet-name consumerVNet \
  --subnet peSubnet \
  --private-connection-resource-id "myPLS.abc123.eastus.azure.privatelinkservice" \
  --connection-name myConnection
```

---

## AWS PrivateLink (Service Provider)

Expose your NLB-fronted service to consumers in other VPCs/accounts.

### Deployment

```bash
# Step 1: Create NLB with target group (skip if exists)
aws elbv2 create-load-balancer \
  --name my-nlb --type network \
  --subnets subnet-aaa subnet-bbb

# Step 2: Create VPC endpoint service
aws ec2 create-vpc-endpoint-service-configuration \
  --network-load-balancer-arns arn:aws:elasticloadbalancing:...:loadbalancer/net/my-nlb/... \
  --acceptance-required

# Step 3: Allow specific accounts to create endpoints
aws ec2 modify-vpc-endpoint-service-permissions \
  --service-id vpce-svc-0123456789abcdef0 \
  --add-allowed-principals "arn:aws:iam::123456789012:root" "arn:aws:iam::987654321098:root"

# Step 4: Accept consumer endpoint connection
aws ec2 accept-vpc-endpoint-connections \
  --service-id vpce-svc-0123456789abcdef0 \
  --vpc-endpoint-ids vpce-0123456789abcdef0
```

**Key points:**
- **NLB only** — ALB and GLB cannot be PrivateLink providers.
- **Cross-region**: Prefer same-region consumers for latency and data-transfer predictability, but AWS PrivateLink supports cross-Region endpoint service access when the provider enables allowed Regions and permissions such as `vpce:AllowMultiRegion`. Verify the current workflow before publishing: https://docs.aws.amazon.com/vpc/latest/privatelink/privatelink-share-your-services.html.
- **IP address type**: Endpoint services and consumers can use IPv4, IPv6, or dualstack where the service, NLB, target groups, and client VPC subnets support it. Validate address-type support end-to-end before advertising IPv6 or dualstack access.
- **Private DNS name**: Register a custom DNS name (e.g., `api.myservice.com`) and verify domain ownership. Consumers can then use this name instead of the `vpce-*` DNS name.

---

## GCP Private Service Connect (Producer)

Expose your Internal Load Balancer-backed service via a service attachment.

```bash
# Step 1: Create internal LB with backend service (skip if exists)

# Step 2: Create a separate subnet for PSC NAT
gcloud compute networks subnets create psc-nat-subnet \
  --network=my-vpc --region=us-central1 \
  --range=10.5.0.0/24 --purpose=PRIVATE_SERVICE_CONNECT

# Step 3: Create service attachment
gcloud compute service-attachments create my-service \
  --region=us-central1 \
  --producer-forwarding-rule=my-ilb-forwarding-rule \
  --nat-subnets=psc-nat-subnet \
  --connection-preference=ACCEPT_MANUAL \
  --consumer-accept-list=consumer-project-id=10

# Step 4: Share the service attachment URI with consumers
# projects/my-project/regions/us-central1/serviceAttachments/my-service
```

**Key points:**
- **Internal LB only** — external LBs cannot be PSC producers.
- **NAT subnet**: A dedicated subnet with `purpose=PRIVATE_SERVICE_CONNECT` for NAT.
- **Consumer limit**: Set max connections per consumer project via the accept list.
- **Domain names**: Optionally configure a DNS domain for the service.

---

## Cross-Cloud Service Exposure

To expose a service from one cloud to consumers in another:

1. Deploy the service behind a private link/endpoint service in the producer cloud.
2. Establish cross-cloud connectivity (VPN, ExpressRoute, Interconnect).
3. Create a private endpoint in the consumer cloud's VNet/VPC.
4. Configure DNS forwarding so consumers resolve the service FQDN to the private IP.

**Example: Azure PLS consumed from AWS:**
- Producer: Azure PLS behind Standard LB.
- Network: Site-to-site VPN between Azure VNet and AWS VPC.
- Consumer: Route traffic from AWS to the Azure PE IP via VPN.
- DNS: AWS Route 53 private hosted zone with A record pointing to the PE IP.

---

## Common Service Exposure Mistakes

1. **Using Basic LB (Azure)** — PLS requires Standard LB. Basic LB is not supported and is being retired.
2. **Forgetting NAT subnet** — both Azure PLS and GCP PSC need a dedicated NAT subnet.
3. **No approval workflow for production** — auto-approval is convenient but risky for cross-tenant scenarios. Use manual approval with notification.
4. **Not enabling TCP proxy v2 (Azure)** — without it, the backend sees NAT IPs instead of consumer IPs. Enable if you need consumer identification.
5. **Single-region deployment** — Private Link is regional. For multi-region consumers, deploy the service in multiple regions.

**Analysis only — verify against vendor documentation before applying.**
