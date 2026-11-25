---
name: amazon-elastic-kubernetes-service
description: "Amazon Elastic Kubernetes Service API skill. Use when working with Amazon Elastic Kubernetes Service for clusters, eks-anywhere-subscriptions, cluster-registrations. Covers 56 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon Elastic Kubernetes Service
API version: 2017-11-01

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /addons/configuration-schemas -- verify access
3. POST /clusters/{name}/access-entries/{principalArn}/access-policies -- create first access-policies

## Endpoints

56 endpoints across 6 groups. See references/api-spec.lap for full details.

### clusters
| Method | Path | Description |
|--------|------|-------------|
| POST | /clusters/{name}/access-entries/{principalArn}/access-policies | Associates an access policy and its scope to an access entry. For more information about associating access policies, see Associating and disassociating access policies to and from access entries in the Amazon EKS User Guide. |
| POST | /clusters/{name}/encryption-config/associate | Associates an encryption configuration to an existing cluster. Use this API to enable encryption on existing clusters that don't already have encryption enabled. This allows you to implement a defense-in-depth security strategy without migrating applications to new Amazon EKS clusters. |
| POST | /clusters/{name}/identity-provider-configs/associate | Associates an identity provider configuration to a cluster. If you want to authenticate identities using an identity provider, you can create an identity provider configuration and associate it to your cluster. After configuring authentication to your cluster you can create Kubernetes Role and ClusterRole objects, assign permissions to them, and then bind them to the identities using Kubernetes RoleBinding and ClusterRoleBinding objects. For more information see Using RBAC Authorization in the Kubernetes documentation. |
| POST | /clusters/{name}/access-entries | Creates an access entry. An access entry allows an IAM principal to access your cluster. Access entries can replace the need to maintain entries in the aws-auth ConfigMap for authentication. You have the following options for authorizing an IAM principal to access Kubernetes objects on your cluster: Kubernetes role-based access control (RBAC), Amazon EKS, or both. Kubernetes RBAC authorization requires you to create and manage Kubernetes Role, ClusterRole, RoleBinding, and ClusterRoleBinding objects, in addition to managing access entries. If you use Amazon EKS authorization exclusively, you don't need to create and manage Kubernetes Role, ClusterRole, RoleBinding, and ClusterRoleBinding objects. For more information about access entries, see Access entries in the Amazon EKS User Guide. |
| POST | /clusters/{name}/addons | Creates an Amazon EKS add-on. Amazon EKS add-ons help to automate the provisioning and lifecycle management of common operational software for Amazon EKS clusters. For more information, see Amazon EKS add-ons in the Amazon EKS User Guide. |
| POST | /clusters | Creates an Amazon EKS control plane. The Amazon EKS control plane consists of control plane instances that run the Kubernetes software, such as etcd and the API server. The control plane runs in an account managed by Amazon Web Services, and the Kubernetes API is exposed by the Amazon EKS API server endpoint. Each Amazon EKS cluster control plane is single tenant and unique. It runs on its own set of Amazon EC2 instances. The cluster control plane is provisioned across multiple Availability Zones and fronted by an Elastic Load Balancing Network Load Balancer. Amazon EKS also provisions elastic network interfaces in your VPC subnets to provide connectivity from the control plane instances to the nodes (for example, to support kubectl exec, logs, and proxy data flows). Amazon EKS nodes run in your Amazon Web Services account and connect to your cluster's control plane over the Kubernetes API server endpoint and a certificate file that is created for your cluster. You can use the endpointPublicAccess and endpointPrivateAccess parameters to enable or disable public and private access to your cluster's Kubernetes API server endpoint. By default, public access is enabled, and private access is disabled. For more information, see Amazon EKS Cluster Endpoint Access Control in the  Amazon EKS User Guide .  You can use the logging parameter to enable or disable exporting the Kubernetes control plane logs for your cluster to CloudWatch Logs. By default, cluster control plane logs aren't exported to CloudWatch Logs. For more information, see Amazon EKS Cluster Control Plane Logs in the  Amazon EKS User Guide .  CloudWatch Logs ingestion, archive storage, and data scanning rates apply to exported control plane logs. For more information, see CloudWatch Pricing.  In most cases, it takes several minutes to create a cluster. After you create an Amazon EKS cluster, you must configure your Kubernetes tooling to communicate with the API server and launch nodes into your cluster. For more information, see Allowing users to access your cluster and Launching Amazon EKS nodes in the Amazon EKS User Guide. |
| POST | /clusters/{name}/fargate-profiles | Creates an Fargate profile for your Amazon EKS cluster. You must have at least one Fargate profile in a cluster to be able to run pods on Fargate. The Fargate profile allows an administrator to declare which pods run on Fargate and specify which pods run on which Fargate profile. This declaration is done through the profile’s selectors. Each profile can have up to five selectors that contain a namespace and labels. A namespace is required for every selector. The label field consists of multiple optional key-value pairs. Pods that match the selectors are scheduled on Fargate. If a to-be-scheduled pod matches any of the selectors in the Fargate profile, then that pod is run on Fargate. When you create a Fargate profile, you must specify a pod execution role to use with the pods that are scheduled with the profile. This role is added to the cluster's Kubernetes Role Based Access Control (RBAC) for authorization so that the kubelet that is running on the Fargate infrastructure can register with your Amazon EKS cluster so that it can appear in your cluster as a node. The pod execution role also provides IAM permissions to the Fargate infrastructure to allow read access to Amazon ECR image repositories. For more information, see Pod Execution Role in the Amazon EKS User Guide. Fargate profiles are immutable. However, you can create a new updated profile to replace an existing profile and then delete the original after the updated profile has finished creating. If any Fargate profiles in a cluster are in the DELETING status, you must wait for that Fargate profile to finish deleting before you can create any other profiles in that cluster. For more information, see Fargate profile in the Amazon EKS User Guide. |
| POST | /clusters/{name}/node-groups | Creates a managed node group for an Amazon EKS cluster. You can only create a node group for your cluster that is equal to the current Kubernetes version for the cluster. All node groups are created with the latest AMI release version for the respective minor Kubernetes version of the cluster, unless you deploy a custom AMI using a launch template. For more information about using launch templates, see Customizing managed nodes with launch templates. An Amazon EKS managed node group is an Amazon EC2 Auto Scaling group and associated Amazon EC2 instances that are managed by Amazon Web Services for an Amazon EKS cluster. For more information, see Managed node groups in the Amazon EKS User Guide.  Windows AMI types are only supported for commercial Amazon Web Services Regions that support Windows on Amazon EKS. |
| POST | /clusters/{name}/pod-identity-associations | Creates an EKS Pod Identity association between a service account in an Amazon EKS cluster and an IAM role with EKS Pod Identity. Use EKS Pod Identity to give temporary IAM credentials to pods and the credentials are rotated automatically. Amazon EKS Pod Identity associations provide the ability to manage credentials for your applications, similar to the way that Amazon EC2 instance profiles provide credentials to Amazon EC2 instances. If a pod uses a service account that has an association, Amazon EKS sets environment variables in the containers of the pod. The environment variables configure the Amazon Web Services SDKs, including the Command Line Interface, to use the EKS Pod Identity credentials. Pod Identity is a simpler method than IAM roles for service accounts, as this method doesn't use OIDC identity providers. Additionally, you can configure a role for Pod Identity once, and reuse it across clusters. |
| DELETE | /clusters/{name}/access-entries/{principalArn} | Deletes an access entry. Deleting an access entry of a type other than Standard can cause your cluster to function improperly. If you delete an access entry in error, you can recreate it. |
| DELETE | /clusters/{name}/addons/{addonName} | Deletes an Amazon EKS add-on. When you remove an add-on, it's deleted from the cluster. You can always manually start an add-on on the cluster using the Kubernetes API. |
| DELETE | /clusters/{name} | Deletes an Amazon EKS cluster control plane. If you have active services in your cluster that are associated with a load balancer, you must delete those services before deleting the cluster so that the load balancers are deleted properly. Otherwise, you can have orphaned resources in your VPC that prevent you from being able to delete the VPC. For more information, see Deleting a cluster in the Amazon EKS User Guide. If you have managed node groups or Fargate profiles attached to the cluster, you must delete them first. For more information, see DeleteNodgroup and DeleteFargateProfile. |
| DELETE | /clusters/{name}/fargate-profiles/{fargateProfileName} | Deletes an Fargate profile. When you delete a Fargate profile, any Pod running on Fargate that was created with the profile is deleted. If the Pod matches another Fargate profile, then it is scheduled on Fargate with that profile. If it no longer matches any Fargate profiles, then it's not scheduled on Fargate and may remain in a pending state. Only one Fargate profile in a cluster can be in the DELETING status at a time. You must wait for a Fargate profile to finish deleting before you can delete any other profiles in that cluster. |
| DELETE | /clusters/{name}/node-groups/{nodegroupName} | Deletes a managed node group. |
| DELETE | /clusters/{name}/pod-identity-associations/{associationId} | Deletes a EKS Pod Identity association. The temporary Amazon Web Services credentials from the previous IAM role session might still be valid until the session expiry. If you need to immediately revoke the temporary session credentials, then go to the role in the IAM console. |
| GET | /clusters/{name}/access-entries/{principalArn} | Describes an access entry. |
| GET | /clusters/{name}/addons/{addonName} | Describes an Amazon EKS add-on. |
| GET | /clusters/{name} | Describes an Amazon EKS cluster. The API server endpoint and certificate authority data returned by this operation are required for kubelet and kubectl to communicate with your Kubernetes API server. For more information, see Creating or updating a kubeconfig file for an Amazon EKS cluster.  The API server endpoint and certificate authority data aren't available until the cluster reaches the ACTIVE state. |
| GET | /clusters/{name}/fargate-profiles/{fargateProfileName} | Describes an Fargate profile. |
| POST | /clusters/{name}/identity-provider-configs/describe | Describes an identity provider configuration. |
| GET | /clusters/{name}/insights/{id} | Returns details about an insight that you specify using its ID. |
| GET | /clusters/{name}/node-groups/{nodegroupName} | Describes a managed node group. |
| GET | /clusters/{name}/pod-identity-associations/{associationId} | Returns descriptive information about an EKS Pod Identity association. This action requires the ID of the association. You can get the ID from the response to the CreatePodIdentityAssocation for newly created associations. Or, you can list the IDs for associations with ListPodIdentityAssociations and filter the list by namespace or service account. |
| GET | /clusters/{name}/updates/{updateId} | Describes an update to an Amazon EKS resource. When the status of the update is Succeeded, the update is complete. If an update fails, the status is Failed, and an error detail explains the reason for the failure. |
| DELETE | /clusters/{name}/access-entries/{principalArn}/access-policies/{policyArn} | Disassociates an access policy from an access entry. |
| POST | /clusters/{name}/identity-provider-configs/disassociate | Disassociates an identity provider configuration from a cluster. If you disassociate an identity provider from your cluster, users included in the provider can no longer access the cluster. However, you can still access the cluster with IAM principals. |
| GET | /clusters/{name}/access-entries | Lists the access entries for your cluster. |
| GET | /clusters/{name}/addons | Lists the installed add-ons. |
| GET | /clusters/{name}/access-entries/{principalArn}/access-policies | Lists the access policies associated with an access entry. |
| GET | /clusters | Lists the Amazon EKS clusters in your Amazon Web Services account in the specified Amazon Web Services Region. |
| GET | /clusters/{name}/fargate-profiles | Lists the Fargate profiles associated with the specified cluster in your Amazon Web Services account in the specified Amazon Web Services Region. |
| GET | /clusters/{name}/identity-provider-configs | Lists the identity provider configurations for your cluster. |
| POST | /clusters/{name}/insights | Returns a list of all insights checked for against the specified cluster. You can filter which insights are returned by category, associated Kubernetes version, and status. |
| GET | /clusters/{name}/node-groups | Lists the managed node groups associated with the specified cluster in your Amazon Web Services account in the specified Amazon Web Services Region. Self-managed node groups aren't listed. |
| GET | /clusters/{name}/pod-identity-associations | List the EKS Pod Identity associations in a cluster. You can filter the list by the namespace that the association is in or the service account that the association uses. |
| GET | /clusters/{name}/updates | Lists the updates associated with an Amazon EKS resource in your Amazon Web Services account, in the specified Amazon Web Services Region. |
| POST | /clusters/{name}/access-entries/{principalArn} | Updates an access entry. |
| POST | /clusters/{name}/addons/{addonName}/update | Updates an Amazon EKS add-on. |
| POST | /clusters/{name}/update-config | Updates an Amazon EKS cluster configuration. Your cluster continues to function during the update. The response output includes an update ID that you can use to track the status of your cluster update with DescribeUpdate"/&gt;. You can use this API operation to enable or disable exporting the Kubernetes control plane logs for your cluster to CloudWatch Logs. By default, cluster control plane logs aren't exported to CloudWatch Logs. For more information, see Amazon EKS Cluster control plane logs in the  Amazon EKS User Guide .  CloudWatch Logs ingestion, archive storage, and data scanning rates apply to exported control plane logs. For more information, see CloudWatch Pricing.  You can also use this API operation to enable or disable public and private access to your cluster's Kubernetes API server endpoint. By default, public access is enabled, and private access is disabled. For more information, see Amazon EKS cluster endpoint access control in the  Amazon EKS User Guide . You can also use this API operation to choose different subnets and security groups for the cluster. You must specify at least two subnets that are in different Availability Zones. You can't change which VPC the subnets are from, the subnets must be in the same VPC as the subnets that the cluster was created with. For more information about the VPC requirements, see https://docs.aws.amazon.com/eks/latest/userguide/network_reqs.html in the  Amazon EKS User Guide . Cluster updates are asynchronous, and they should finish within a few minutes. During an update, the cluster status moves to UPDATING (this status transition is eventually consistent). When the update is complete (either Failed or Successful), the cluster status moves to Active. |
| POST | /clusters/{name}/updates | Updates an Amazon EKS cluster to the specified Kubernetes version. Your cluster continues to function during the update. The response output includes an update ID that you can use to track the status of your cluster update with the DescribeUpdate API operation. Cluster updates are asynchronous, and they should finish within a few minutes. During an update, the cluster status moves to UPDATING (this status transition is eventually consistent). When the update is complete (either Failed or Successful), the cluster status moves to Active. If your cluster has managed node groups attached to it, all of your node groups’ Kubernetes versions must match the cluster’s Kubernetes version in order to update the cluster to a new Kubernetes version. |
| POST | /clusters/{name}/node-groups/{nodegroupName}/update-config | Updates an Amazon EKS managed node group configuration. Your node group continues to function during the update. The response output includes an update ID that you can use to track the status of your node group update with the DescribeUpdate API operation. Currently you can update the Kubernetes labels for a node group or the scaling configuration. |
| POST | /clusters/{name}/node-groups/{nodegroupName}/update-version | Updates the Kubernetes version or AMI version of an Amazon EKS managed node group. You can update a node group using a launch template only if the node group was originally deployed with a launch template. If you need to update a custom AMI in a node group that was deployed with a launch template, then update your custom AMI, specify the new ID in a new version of the launch template, and then update the node group to the new version of the launch template. If you update without a launch template, then you can update to the latest available AMI version of a node group's current Kubernetes version by not specifying a Kubernetes version in the request. You can update to the latest AMI version of your cluster's current Kubernetes version by specifying your cluster's Kubernetes version in the request. For information about Linux versions, see Amazon EKS optimized Amazon Linux AMI versions in the Amazon EKS User Guide. For information about Windows versions, see Amazon EKS optimized Windows AMI versions in the Amazon EKS User Guide.  You cannot roll back a node group to an earlier Kubernetes version or AMI version. When a node in a managed node group is terminated due to a scaling action or update, every Pod on that node is drained first. Amazon EKS attempts to drain the nodes gracefully and will fail if it is unable to do so. You can force the update if Amazon EKS is unable to drain the nodes as a result of a Pod disruption budget issue. |
| POST | /clusters/{name}/pod-identity-associations/{associationId} | Updates a EKS Pod Identity association. Only the IAM role can be changed; an association can't be moved between clusters, namespaces, or service accounts. If you need to edit the namespace or service account, you need to delete the association and then create a new association with your desired settings. |

### eks-anywhere-subscriptions
| Method | Path | Description |
|--------|------|-------------|
| POST | /eks-anywhere-subscriptions | Creates an EKS Anywhere subscription. When a subscription is created, it is a contract agreement for the length of the term specified in the request. Licenses that are used to validate support are provisioned in Amazon Web Services License Manager and the caller account is granted access to EKS Anywhere Curated Packages. |
| DELETE | /eks-anywhere-subscriptions/{id} | Deletes an expired or inactive subscription. Deleting inactive subscriptions removes them from the Amazon Web Services Management Console view and from list/describe API responses. Subscriptions can only be cancelled within 7 days of creation and are cancelled by creating a ticket in the Amazon Web Services Support Center. |
| GET | /eks-anywhere-subscriptions/{id} | Returns descriptive information about a subscription. |
| GET | /eks-anywhere-subscriptions | Displays the full description of the subscription. |
| POST | /eks-anywhere-subscriptions/{id} | Update an EKS Anywhere Subscription. Only auto renewal and tags can be updated after subscription creation. |

### cluster-registrations
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /cluster-registrations/{name} | Deregisters a connected cluster to remove it from the Amazon EKS control plane. A connected cluster is a Kubernetes cluster that you've connected to your control plane using the Amazon EKS Connector. |
| POST | /cluster-registrations | Connects a Kubernetes cluster to the Amazon EKS control plane.  Any Kubernetes cluster can be connected to the Amazon EKS control plane to view current information about the cluster and its nodes.  Cluster connection requires two steps. First, send a  RegisterClusterRequest  to add it to the Amazon EKS control plane. Second, a Manifest containing the activationID and activationCode must be applied to the Kubernetes cluster through it's native provider to provide visibility. After the manifest is updated and applied, the connected cluster is visible to the Amazon EKS control plane. If the manifest isn't applied within three days, the connected cluster will no longer be visible and must be deregistered using DeregisterCluster. |

### addons
| Method | Path | Description |
|--------|------|-------------|
| GET | /addons/configuration-schemas | Returns configuration options. |
| GET | /addons/supported-versions | Describes the versions for an add-on. Information such as the Kubernetes versions that you can use the add-on with, the owner, publisher, and the type of the add-on are returned. |

### access-policies
| Method | Path | Description |
|--------|------|-------------|
| GET | /access-policies | Lists the available access policies. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{resourceArn} | List the tags for an Amazon EKS resource. |
| POST | /tags/{resourceArn} | Associates the specified tags to an Amazon EKS resource with the specified resourceArn. If existing tags on a resource are not specified in the request parameters, they aren't changed. When a resource is deleted, the tags associated with that resource are also deleted. Tags that you create for Amazon EKS resources don't propagate to any other resources associated with the cluster. For example, if you tag a cluster with this operation, that tag doesn't automatically propagate to the subnets and nodes associated with the cluster. |
| DELETE | /tags/{resourceArn} | Deletes specified tags from an Amazon EKS resource. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a access-policy?" -> POST /clusters/{name}/access-entries/{principalArn}/access-policies
- "Create a associate?" -> POST /clusters/{name}/encryption-config/associate
- "Create a associate?" -> POST /clusters/{name}/identity-provider-configs/associate
- "Create a access-entry?" -> POST /clusters/{name}/access-entries
- "Create a addon?" -> POST /clusters/{name}/addons
- "Create a cluster?" -> POST /clusters
- "Create a eks-anywhere-subscription?" -> POST /eks-anywhere-subscriptions
- "Create a fargate-profile?" -> POST /clusters/{name}/fargate-profiles
- "Create a node-group?" -> POST /clusters/{name}/node-groups
- "Create a pod-identity-association?" -> POST /clusters/{name}/pod-identity-associations
- "Delete a access-entry?" -> DELETE /clusters/{name}/access-entries/{principalArn}
- "Delete a addon?" -> DELETE /clusters/{name}/addons/{addonName}
- "Delete a cluster?" -> DELETE /clusters/{name}
- "Delete a eks-anywhere-subscription?" -> DELETE /eks-anywhere-subscriptions/{id}
- "Delete a fargate-profile?" -> DELETE /clusters/{name}/fargate-profiles/{fargateProfileName}
- "Delete a node-group?" -> DELETE /clusters/{name}/node-groups/{nodegroupName}
- "Delete a pod-identity-association?" -> DELETE /clusters/{name}/pod-identity-associations/{associationId}
- "Delete a cluster-registration?" -> DELETE /cluster-registrations/{name}
- "Get access-entry details?" -> GET /clusters/{name}/access-entries/{principalArn}
- "Get addon details?" -> GET /clusters/{name}/addons/{addonName}
- "List all configuration-schemas?" -> GET /addons/configuration-schemas
- "List all supported-versions?" -> GET /addons/supported-versions
- "Get cluster details?" -> GET /clusters/{name}
- "Get eks-anywhere-subscription details?" -> GET /eks-anywhere-subscriptions/{id}
- "Get fargate-profile details?" -> GET /clusters/{name}/fargate-profiles/{fargateProfileName}
- "Create a describe?" -> POST /clusters/{name}/identity-provider-configs/describe
- "Get insight details?" -> GET /clusters/{name}/insights/{id}
- "Get node-group details?" -> GET /clusters/{name}/node-groups/{nodegroupName}
- "Get pod-identity-association details?" -> GET /clusters/{name}/pod-identity-associations/{associationId}
- "Get update details?" -> GET /clusters/{name}/updates/{updateId}
- "Delete a access-policy?" -> DELETE /clusters/{name}/access-entries/{principalArn}/access-policies/{policyArn}
- "Create a disassociate?" -> POST /clusters/{name}/identity-provider-configs/disassociate
- "List all access-entries?" -> GET /clusters/{name}/access-entries
- "List all access-policies?" -> GET /access-policies
- "List all addons?" -> GET /clusters/{name}/addons
- "List all access-policies?" -> GET /clusters/{name}/access-entries/{principalArn}/access-policies
- "List all clusters?" -> GET /clusters
- "List all eks-anywhere-subscriptions?" -> GET /eks-anywhere-subscriptions
- "List all fargate-profiles?" -> GET /clusters/{name}/fargate-profiles
- "List all identity-provider-configs?" -> GET /clusters/{name}/identity-provider-configs
- "Create a insight?" -> POST /clusters/{name}/insights
- "List all node-groups?" -> GET /clusters/{name}/node-groups
- "List all pod-identity-associations?" -> GET /clusters/{name}/pod-identity-associations
- "Get tag details?" -> GET /tags/{resourceArn}
- "List all updates?" -> GET /clusters/{name}/updates
- "Create a cluster-registration?" -> POST /cluster-registrations
- "Delete a tag?" -> DELETE /tags/{resourceArn}
- "Create a update?" -> POST /clusters/{name}/addons/{addonName}/update
- "Create a update-config?" -> POST /clusters/{name}/update-config
- "Create a update?" -> POST /clusters/{name}/updates
- "Create a update-config?" -> POST /clusters/{name}/node-groups/{nodegroupName}/update-config
- "Create a update-version?" -> POST /clusters/{name}/node-groups/{nodegroupName}/update-version
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
