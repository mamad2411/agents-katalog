---
name: aws-iot-sitewise
description: "AWS IoT SiteWise API skill. Use when working with AWS IoT SiteWise for assets, timeseries, projects. Covers 84 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS IoT SiteWise
API version: 2019-12-02

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /configuration/account/encryption -- verify access
3. POST /assets/{assetId}/associate -- create first associate

## Endpoints

84 endpoints across 15 groups. See references/api-spec.lap for full details.

### assets
| Method | Path | Description |
|--------|------|-------------|
| POST | /assets/{assetId}/associate | Associates a child asset with the given parent asset through a hierarchy defined in the parent asset's model. For more information, see Associating assets in the IoT SiteWise User Guide. |
| POST | /assets | Creates an asset from an existing asset model. For more information, see Creating assets in the IoT SiteWise User Guide. |
| DELETE | /assets/{assetId} | Deletes an asset. This action can't be undone. For more information, see Deleting assets and models in the IoT SiteWise User Guide.  You can't delete an asset that's associated to another asset. For more information, see DisassociateAssets. |
| GET | /assets/{assetId} | Retrieves information about an asset. |
| GET | /assets/{assetId}/composite-models/{assetCompositeModelId} | Retrieves information about an asset composite model (also known as an asset component). An AssetCompositeModel is an instance of an AssetModelCompositeModel. If you want to see information about the model this is based on, call DescribeAssetModelCompositeModel. |
| GET | /assets/{assetId}/properties/{propertyId} | Retrieves information about an asset property.  When you call this operation for an attribute property, this response includes the default attribute value that you define in the asset model. If you update the default value in the model, this operation's response includes the new default value.  This operation doesn't return the value of the asset property. To get the value of an asset property, use GetAssetPropertyValue. |
| POST | /assets/{assetId}/disassociate | Disassociates a child asset from the given parent asset through a hierarchy defined in the parent asset's model. |
| GET | /assets/{assetId}/properties | Retrieves a paginated list of properties associated with an asset. If you update properties associated with the model before you finish listing all the properties, you need to start all over again. |
| GET | /assets/{assetId}/assetRelationships | Retrieves a paginated list of asset relationships for an asset. You can use this operation to identify an asset's root asset and all associated assets between that asset and its root. |
| GET | /assets | Retrieves a paginated list of asset summaries. You can use this operation to do the following:   List assets based on a specific asset model.   List top-level assets.   You can't use this operation to list all assets. To retrieve summaries for all of your assets, use ListAssetModels to get all of your asset model IDs. Then, use ListAssets to get all assets for each asset model. |
| GET | /assets/{assetId}/hierarchies | Retrieves a paginated list of associated assets. You can use this operation to do the following:    CHILD - List all child assets associated to the asset.    PARENT - List the asset's parent asset. |
| PUT | /assets/{assetId} | Updates an asset's name. For more information, see Updating assets and models in the IoT SiteWise User Guide. |
| PUT | /assets/{assetId}/properties/{propertyId} | Updates an asset property's alias and notification state.  This operation overwrites the property's existing alias and notification state. To keep your existing property's alias or notification state, you must include the existing values in the UpdateAssetProperty request. For more information, see DescribeAssetProperty. |

### timeseries
| Method | Path | Description |
|--------|------|-------------|
| POST | /timeseries/associate/ | Associates a time series (data stream) with an asset property. |
| POST | /timeseries/delete/ | Deletes a time series (data stream). If you delete a time series that's associated with an asset property, the asset property still exists, but the time series will no longer be associated with this asset property. To identify a time series, do one of the following:   If the time series isn't associated with an asset property, specify the alias of the time series.   If the time series is associated with an asset property, specify one of the following:    The alias of the time series.   The assetId and propertyId that identifies the asset property. |
| GET | /timeseries/describe/ | Retrieves information about a time series (data stream). To identify a time series, do one of the following:   If the time series isn't associated with an asset property, specify the alias of the time series.   If the time series is associated with an asset property, specify one of the following:    The alias of the time series.   The assetId and propertyId that identifies the asset property. |
| POST | /timeseries/disassociate/ | Disassociates a time series (data stream) from an asset property. |
| GET | /timeseries/ | Retrieves a paginated list of time series (data streams). |

### projects
| Method | Path | Description |
|--------|------|-------------|
| POST | /projects/{projectId}/assets/associate | Associates a group (batch) of assets with an IoT SiteWise Monitor project. |
| POST | /projects/{projectId}/assets/disassociate | Disassociates a group (batch) of assets from an IoT SiteWise Monitor project. |
| POST | /projects | Creates a project in the specified portal.  Make sure that the project name and description don't contain confidential information. |
| DELETE | /projects/{projectId} | Deletes a project from IoT SiteWise Monitor. |
| GET | /projects/{projectId} | Retrieves information about a project. |
| GET | /projects/{projectId}/assets | Retrieves a paginated list of assets associated with an IoT SiteWise Monitor project. |
| GET | /projects | Retrieves a paginated list of projects for an IoT SiteWise Monitor portal. |
| PUT | /projects/{projectId} | Updates an IoT SiteWise Monitor project. |

### properties
| Method | Path | Description |
|--------|------|-------------|
| POST | /properties/batch/aggregates | Gets aggregated values (for example, average, minimum, and maximum) for one or more asset properties. For more information, see Querying aggregates in the IoT SiteWise User Guide. |
| POST | /properties/batch/latest | Gets the current value for one or more asset properties. For more information, see Querying current values in the IoT SiteWise User Guide. |
| POST | /properties/batch/history | Gets the historical values for one or more asset properties. For more information, see Querying historical values in the IoT SiteWise User Guide. |
| POST | /properties | Sends a list of asset property values to IoT SiteWise. Each value is a timestamp-quality-value (TQV) data point. For more information, see Ingesting data using the API in the IoT SiteWise User Guide. To identify an asset property, you must specify one of the following:   The assetId and propertyId of an asset property.   A propertyAlias, which is a data stream alias (for example, /company/windfarm/3/turbine/7/temperature). To define an asset property's alias, see UpdateAssetProperty.    With respect to Unix epoch time, IoT SiteWise accepts only TQVs that have a timestamp of no more than 7 days in the past and no more than 10 minutes in the future. IoT SiteWise rejects timestamps outside of the inclusive range of [-7 days, +10 minutes] and returns a TimestampOutOfRangeException error. For each asset property, IoT SiteWise overwrites TQVs with duplicate timestamps unless the newer TQV has a different quality. For example, if you store a TQV {T1, GOOD, V1}, then storing {T1, GOOD, V2} replaces the existing TQV.  IoT SiteWise authorizes access to each BatchPutAssetPropertyValue entry individually. For more information, see BatchPutAssetPropertyValue authorization in the IoT SiteWise User Guide. |
| GET | /properties/aggregates | Gets aggregated values for an asset property. For more information, see Querying aggregates in the IoT SiteWise User Guide. To identify an asset property, you must specify one of the following:   The assetId and propertyId of an asset property.   A propertyAlias, which is a data stream alias (for example, /company/windfarm/3/turbine/7/temperature). To define an asset property's alias, see UpdateAssetProperty. |
| GET | /properties/latest | Gets an asset property's current value. For more information, see Querying current values in the IoT SiteWise User Guide. To identify an asset property, you must specify one of the following:   The assetId and propertyId of an asset property.   A propertyAlias, which is a data stream alias (for example, /company/windfarm/3/turbine/7/temperature). To define an asset property's alias, see UpdateAssetProperty. |
| GET | /properties/history | Gets the history of an asset property's values. For more information, see Querying historical values in the IoT SiteWise User Guide. To identify an asset property, you must specify one of the following:   The assetId and propertyId of an asset property.   A propertyAlias, which is a data stream alias (for example, /company/windfarm/3/turbine/7/temperature). To define an asset property's alias, see UpdateAssetProperty. |
| GET | /properties/interpolated | Get interpolated values for an asset property for a specified time interval, during a period of time. If your time series is missing data points during the specified time interval, you can use interpolation to estimate the missing data. For example, you can use this operation to return the interpolated temperature values for a wind turbine every 24 hours over a duration of 7 days. To identify an asset property, you must specify one of the following:   The assetId and propertyId of an asset property.   A propertyAlias, which is a data stream alias (for example, /company/windfarm/3/turbine/7/temperature). To define an asset property's alias, see UpdateAssetProperty. |

### access-policies
| Method | Path | Description |
|--------|------|-------------|
| POST | /access-policies | Creates an access policy that grants the specified identity (IAM Identity Center user, IAM Identity Center group, or IAM user) access to the specified IoT SiteWise Monitor portal or project resource. |
| DELETE | /access-policies/{accessPolicyId} | Deletes an access policy that grants the specified identity access to the specified IoT SiteWise Monitor resource. You can use this operation to revoke access to an IoT SiteWise Monitor resource. |
| GET | /access-policies/{accessPolicyId} | Describes an access policy, which specifies an identity's access to an IoT SiteWise Monitor portal or project. |
| GET | /access-policies | Retrieves a paginated list of access policies for an identity (an IAM Identity Center user, an IAM Identity Center group, or an IAM user) or an IoT SiteWise Monitor resource (a portal or project). |
| PUT | /access-policies/{accessPolicyId} | Updates an existing access policy that specifies an identity's access to an IoT SiteWise Monitor portal or project resource. |

### asset-models
| Method | Path | Description |
|--------|------|-------------|
| POST | /asset-models | Creates an asset model from specified property and hierarchy definitions. You create assets from asset models. With asset models, you can easily create assets of the same type that have standardized definitions. Each asset created from a model inherits the asset model's property and hierarchy definitions. For more information, see Defining asset models in the IoT SiteWise User Guide. You can create two types of asset models, ASSET_MODEL or COMPONENT_MODEL.    ASSET_MODEL – (default) An asset model that you can use to create assets. Can't be included as a component in another asset model.    COMPONENT_MODEL – A reusable component that you can include in the composite models of other asset models. You can't create assets directly from this type of asset model. |
| POST | /asset-models/{assetModelId}/composite-models | Creates a custom composite model from specified property and hierarchy definitions. There are two types of custom composite models, inline and component-model-based.  Use component-model-based custom composite models to define standard, reusable components. A component-model-based custom composite model consists of a name, a description, and the ID of the component model it references. A component-model-based custom composite model has no properties of its own; its referenced component model provides its associated properties to any created assets. For more information, see Custom composite models (Components) in the IoT SiteWise User Guide. Use inline custom composite models to organize the properties of an asset model. The properties of inline custom composite models are local to the asset model where they are included and can't be used to create multiple assets. To create a component-model-based model, specify the composedAssetModelId of an existing asset model with assetModelType of COMPONENT_MODEL. To create an inline model, specify the assetModelCompositeModelProperties and don't include an composedAssetModelId. |
| DELETE | /asset-models/{assetModelId} | Deletes an asset model. This action can't be undone. You must delete all assets created from an asset model before you can delete the model. Also, you can't delete an asset model if a parent asset model exists that contains a property formula expression that depends on the asset model that you want to delete. For more information, see Deleting assets and models in the IoT SiteWise User Guide. |
| DELETE | /asset-models/{assetModelId}/composite-models/{assetModelCompositeModelId} | Deletes a composite model. This action can't be undone. You must delete all assets created from a composite model before you can delete the model. Also, you can't delete a composite model if a parent asset model exists that contains a property formula expression that depends on the asset model that you want to delete. For more information, see Deleting assets and models in the IoT SiteWise User Guide. |
| GET | /asset-models/{assetModelId} | Retrieves information about an asset model. |
| GET | /asset-models/{assetModelId}/composite-models/{assetModelCompositeModelId} | Retrieves information about an asset model composite model (also known as an asset model component). For more information, see Custom composite models (Components) in the IoT SiteWise User Guide. |
| GET | /asset-models/{assetModelId}/composite-models | Retrieves a paginated list of composite models associated with the asset model |
| GET | /asset-models/{assetModelId}/properties | Retrieves a paginated list of properties associated with an asset model. If you update properties associated with the model before you finish listing all the properties, you need to start all over again. |
| GET | /asset-models | Retrieves a paginated list of summaries of all asset models. |
| GET | /asset-models/{assetModelId}/composition-relationships | Retrieves a paginated list of composition relationships for an asset model of type COMPONENT_MODEL. |
| PUT | /asset-models/{assetModelId} | Updates an asset model and all of the assets that were created from the model. Each asset created from the model inherits the updated asset model's property and hierarchy definitions. For more information, see Updating assets and models in the IoT SiteWise User Guide.  If you remove a property from an asset model, IoT SiteWise deletes all previous data for that property. You can’t change the type or data type of an existing property. To replace an existing asset model property with a new one with the same name, do the following:   Submit an UpdateAssetModel request with the entire existing property removed.   Submit a second UpdateAssetModel request that includes the new property. The new asset property will have the same name as the previous one and IoT SiteWise will generate a new unique id. |
| PUT | /asset-models/{assetModelId}/composite-models/{assetModelCompositeModelId} | Updates a composite model and all of the assets that were created from the model. Each asset created from the model inherits the updated asset model's property and hierarchy definitions. For more information, see Updating assets and models in the IoT SiteWise User Guide.  If you remove a property from a composite asset model, IoT SiteWise deletes all previous data for that property. You can’t change the type or data type of an existing property. To replace an existing composite asset model property with a new one with the same name, do the following:   Submit an UpdateAssetModelCompositeModel request with the entire existing property removed.   Submit a second UpdateAssetModelCompositeModel request that includes the new property. The new asset property will have the same name as the previous one and IoT SiteWise will generate a new unique id. |

### jobs
| Method | Path | Description |
|--------|------|-------------|
| POST | /jobs | Defines a job to ingest data to IoT SiteWise from Amazon S3. For more information, see Create a bulk import job (CLI) in the Amazon Simple Storage Service User Guide.  Before you create a bulk import job, you must enable IoT SiteWise warm tier or IoT SiteWise cold tier. For more information about how to configure storage settings, see PutStorageConfiguration. Bulk import is designed to store historical data to IoT SiteWise. It does not trigger computations or notifications on IoT SiteWise warm or cold tier storage. |
| GET | /jobs/{jobId} | Retrieves information about a bulk import job request. For more information, see Describe a bulk import job (CLI) in the Amazon Simple Storage Service User Guide. |
| GET | /jobs | Retrieves a paginated list of bulk import job requests. For more information, see List bulk import jobs (CLI) in the IoT SiteWise User Guide. |

### dashboards
| Method | Path | Description |
|--------|------|-------------|
| POST | /dashboards | Creates a dashboard in an IoT SiteWise Monitor project. |
| DELETE | /dashboards/{dashboardId} | Deletes a dashboard from IoT SiteWise Monitor. |
| GET | /dashboards/{dashboardId} | Retrieves information about a dashboard. |
| GET | /dashboards | Retrieves a paginated list of dashboards for an IoT SiteWise Monitor project. |
| PUT | /dashboards/{dashboardId} | Updates an IoT SiteWise Monitor dashboard. |

### 20200301
| Method | Path | Description |
|--------|------|-------------|
| POST | /20200301/gateways | Creates a gateway, which is a virtual or edge device that delivers industrial data streams from local servers to IoT SiteWise. For more information, see Ingesting data using a gateway in the IoT SiteWise User Guide. |
| DELETE | /20200301/gateways/{gatewayId} | Deletes a gateway from IoT SiteWise. When you delete a gateway, some of the gateway's files remain in your gateway's file system. |
| GET | /20200301/gateways/{gatewayId} | Retrieves information about a gateway. |
| GET | /20200301/gateways/{gatewayId}/capability/{capabilityNamespace} | Retrieves information about a gateway capability configuration. Each gateway capability defines data sources for a gateway. A capability configuration can contain multiple data source configurations. If you define OPC-UA sources for a gateway in the IoT SiteWise console, all of your OPC-UA sources are stored in one capability configuration. To list all capability configurations for a gateway, use DescribeGateway. |
| GET | /20200301/gateways | Retrieves a paginated list of gateways. |
| PUT | /20200301/gateways/{gatewayId} | Updates a gateway's name. |
| POST | /20200301/gateways/{gatewayId}/capability | Updates a gateway capability configuration or defines a new capability configuration. Each gateway capability defines data sources for a gateway. A capability configuration can contain multiple data source configurations. If you define OPC-UA sources for a gateway in the IoT SiteWise console, all of your OPC-UA sources are stored in one capability configuration. To list all capability configurations for a gateway, use DescribeGateway. |

### portals
| Method | Path | Description |
|--------|------|-------------|
| POST | /portals | Creates a portal, which can contain projects and dashboards. IoT SiteWise Monitor uses IAM Identity Center or IAM to authenticate portal users and manage user permissions.  Before you can sign in to a new portal, you must add at least one identity to that portal. For more information, see Adding or removing portal administrators in the IoT SiteWise User Guide. |
| DELETE | /portals/{portalId} | Deletes a portal from IoT SiteWise Monitor. |
| GET | /portals/{portalId} | Retrieves information about a portal. |
| GET | /portals | Retrieves a paginated list of IoT SiteWise Monitor portals. |
| PUT | /portals/{portalId} | Updates an IoT SiteWise Monitor portal. |

### actions
| Method | Path | Description |
|--------|------|-------------|
| GET | /actions/{actionId} | Retrieves information about an action. |
| POST | /actions | Executes an action on a target resource. |
| GET | /actions | Retrieves a paginated list of actions for a specific target resource. |

### configuration
| Method | Path | Description |
|--------|------|-------------|
| GET | /configuration/account/encryption | Retrieves information about the default encryption configuration for the Amazon Web Services account in the default or specified Region. For more information, see Key management in the IoT SiteWise User Guide. |
| GET | /configuration/account/storage | Retrieves information about the storage configuration for IoT SiteWise. |
| POST | /configuration/account/encryption | Sets the default encryption configuration for the Amazon Web Services account. For more information, see Key management in the IoT SiteWise User Guide. |
| POST | /configuration/account/storage | Configures storage settings for IoT SiteWise. |

### logging
| Method | Path | Description |
|--------|------|-------------|
| GET | /logging | Retrieves the current IoT SiteWise logging options. |
| PUT | /logging | Sets logging options for IoT SiteWise. |

### queries
| Method | Path | Description |
|--------|------|-------------|
| POST | /queries/execution | Run SQL queries to retrieve metadata and time-series data from asset models, assets, measurements, metrics, transforms, and aggregates. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags | Retrieves the list of tags for an IoT SiteWise resource. |
| POST | /tags | Adds tags to an IoT SiteWise resource. If a tag already exists for the resource, this operation updates the tag's value. |
| DELETE | /tags | Removes a tag from an IoT SiteWise resource. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a associate?" -> POST /assets/{assetId}/associate
- "Create a associate?" -> POST /timeseries/associate/
- "Create a associate?" -> POST /projects/{projectId}/assets/associate
- "Create a disassociate?" -> POST /projects/{projectId}/assets/disassociate
- "Create a aggregate?" -> POST /properties/batch/aggregates
- "Create a latest?" -> POST /properties/batch/latest
- "Create a history?" -> POST /properties/batch/history
- "Create a property?" -> POST /properties
- "Create a access-policy?" -> POST /access-policies
- "Create a asset?" -> POST /assets
- "Create a asset-model?" -> POST /asset-models
- "Create a composite-model?" -> POST /asset-models/{assetModelId}/composite-models
- "Create a job?" -> POST /jobs
- "Create a dashboard?" -> POST /dashboards
- "Create a gateway?" -> POST /20200301/gateways
- "Create a portal?" -> POST /portals
- "Create a project?" -> POST /projects
- "Delete a access-policy?" -> DELETE /access-policies/{accessPolicyId}
- "Delete a asset?" -> DELETE /assets/{assetId}
- "Delete a asset-model?" -> DELETE /asset-models/{assetModelId}
- "Delete a composite-model?" -> DELETE /asset-models/{assetModelId}/composite-models/{assetModelCompositeModelId}
- "Delete a dashboard?" -> DELETE /dashboards/{dashboardId}
- "Delete a gateway?" -> DELETE /20200301/gateways/{gatewayId}
- "Delete a portal?" -> DELETE /portals/{portalId}
- "Delete a project?" -> DELETE /projects/{projectId}
- "Create a delete?" -> POST /timeseries/delete/
- "Get access-policy details?" -> GET /access-policies/{accessPolicyId}
- "Get action details?" -> GET /actions/{actionId}
- "Get asset details?" -> GET /assets/{assetId}
- "Get composite-model details?" -> GET /assets/{assetId}/composite-models/{assetCompositeModelId}
- "Get asset-model details?" -> GET /asset-models/{assetModelId}
- "Get composite-model details?" -> GET /asset-models/{assetModelId}/composite-models/{assetModelCompositeModelId}
- "Get property details?" -> GET /assets/{assetId}/properties/{propertyId}
- "Get job details?" -> GET /jobs/{jobId}
- "Get dashboard details?" -> GET /dashboards/{dashboardId}
- "List all encryption?" -> GET /configuration/account/encryption
- "Get gateway details?" -> GET /20200301/gateways/{gatewayId}
- "Get capability details?" -> GET /20200301/gateways/{gatewayId}/capability/{capabilityNamespace}
- "List all logging?" -> GET /logging
- "Get portal details?" -> GET /portals/{portalId}
- "Get project details?" -> GET /projects/{projectId}
- "List all storage?" -> GET /configuration/account/storage
- "List all describe?" -> GET /timeseries/describe/
- "Create a disassociate?" -> POST /assets/{assetId}/disassociate
- "Create a disassociate?" -> POST /timeseries/disassociate/
- "Create a action?" -> POST /actions
- "Create a execution?" -> POST /queries/execution
- "List all aggregates?" -> GET /properties/aggregates
- "List all latest?" -> GET /properties/latest
- "List all history?" -> GET /properties/history
- "List all interpolated?" -> GET /properties/interpolated
- "List all access-policies?" -> GET /access-policies
- "List all actions?" -> GET /actions
- "List all composite-models?" -> GET /asset-models/{assetModelId}/composite-models
- "List all properties?" -> GET /asset-models/{assetModelId}/properties
- "List all asset-models?" -> GET /asset-models
- "List all properties?" -> GET /assets/{assetId}/properties
- "List all assetRelationships?" -> GET /assets/{assetId}/assetRelationships
- "List all assets?" -> GET /assets
- "List all hierarchies?" -> GET /assets/{assetId}/hierarchies
- "List all jobs?" -> GET /jobs
- "List all composition-relationships?" -> GET /asset-models/{assetModelId}/composition-relationships
- "List all dashboards?" -> GET /dashboards
- "List all gateways?" -> GET /20200301/gateways
- "List all portals?" -> GET /portals
- "List all assets?" -> GET /projects/{projectId}/assets
- "List all projects?" -> GET /projects
- "List all tags?" -> GET /tags
- "List all timeseries?" -> GET /timeseries/
- "Create a encryption?" -> POST /configuration/account/encryption
- "Create a storage?" -> POST /configuration/account/storage
- "Create a tag?" -> POST /tags
- "Update a access-policy?" -> PUT /access-policies/{accessPolicyId}
- "Update a asset?" -> PUT /assets/{assetId}
- "Update a asset-model?" -> PUT /asset-models/{assetModelId}
- "Update a composite-model?" -> PUT /asset-models/{assetModelId}/composite-models/{assetModelCompositeModelId}
- "Update a property?" -> PUT /assets/{assetId}/properties/{propertyId}
- "Update a dashboard?" -> PUT /dashboards/{dashboardId}
- "Update a gateway?" -> PUT /20200301/gateways/{gatewayId}
- "Create a capability?" -> POST /20200301/gateways/{gatewayId}/capability
- "Update a portal?" -> PUT /portals/{portalId}
- "Update a project?" -> PUT /projects/{projectId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
