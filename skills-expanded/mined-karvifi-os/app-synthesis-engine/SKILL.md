---
name: app-synthesis-engine
description: Design and implement the App Synthesis Engine for the Software Synthesis OS — the system that turns a graph into a fully deployable, standalone application. Not just UI panels inside the OS shell, but complete applications that can be published as web apps, client portals, mobile PWAs, embeddable widgets, API endpoints, and white-label products. This is the mechanism that makes "all software humans ever built" achievable.
triggers: [app synthesis, deployable app, publish app, graph to app, standalone app, client portal generation, white-label, app publishing, generated app, app export, portal generator, app deployment, app synthesis engine, publish workspace, external app]
---

# SKILL: App Synthesis Engine

## Core Principle
The surface compiler generates UI *inside the OS shell*. The app synthesis engine generates software that lives *outside the shell* — standalone web apps, portals, APIs, widgets. A graph that represents a CRM should be able to publish itself as a working CRM application. This is the mechanism that turns the OS from a productivity tool into a software factory.

---

## 1. Synthesis Target Types

```typescript
// app-synthesis-service/types.ts

export type SynthesisTarget =
  | 'web_app'        // Full standalone web application (Next.js deployed to Coolify)
  | 'client_portal'  // External-facing simplified surface for clients
  | 'mobile_pwa'     // Progressive web app optimized for mobile
  | 'embed_widget'   // Embeddable iframe widget for third-party sites
  | 'api_endpoint'   // Public REST API generated from graph outputs
  | 'form_page'      // Standalone form page (data collection)
  | 'status_page'    // External status/progress page
  | 'white_label';   // Fully branded custom domain app

export interface SynthesisRequest {
  graphInstanceId: string;
  target: SynthesisTarget;
  branding: AppBranding;
  accessControl: SynthesisAccessControl;
  publishedRoutes?: PublishedRoute[];       // which graph paths are exposed
  customDomain?: string;
  workspaceId: string;
  requestedBy: string;
}

export interface AppBranding {
  appName: string;
  logoUrl?: string;
  primaryColor: string;
  accentColor?: string;
  fontFamily?: string;
  favicon?: string;
  customCss?: string;
}

export interface SynthesisAccessControl {
  visibility: 'public' | 'password' | 'invite_only' | 'sso';
  password?: string;               // hashed — never stored plain
  allowedEmails?: string[];        // for invite_only
  ssoProviderId?: string;          // for SSO
  requireEmailVerification: boolean;
}

export interface SynthesisResult {
  synthesisId: string;
  target: SynthesisTarget;
  status: 'building' | 'live' | 'failed' | 'paused';
  publishedUrl: string;
  customDomainStatus?: 'pending' | 'active' | 'failed';
  buildLogs?: string[];
  createdAt: string;
}
```

---

## 2. App Synthesis Pipeline

```typescript
// app-synthesis-service/pipeline.ts

export class AppSynthesisPipeline {
  
  async synthesize(req: SynthesisRequest): Promise<SynthesisResult> {
    // Step 1: Load and validate the graph
    const graph = await graphService.getGraph(req.graphInstanceId);
    const validation = graphValidator.validate(graph);
    if (!validation.valid) throw new SynthesisError('Invalid graph', validation.errors);

    // Step 2: Determine surface plan for target
    const surfacePlan = await this.planSurfaces(graph, req.target);

    // Step 3: Generate app scaffold code
    const appCode = await this.generateAppCode(graph, surfacePlan, req);

    // Step 4: Deploy to hosting
    const deploymentUrl = await this.deploy(appCode, req);

    // Step 5: Configure access control
    await this.configureAccessControl(deploymentUrl, req.accessControl);

    // Step 6: Register synthesis record
    const result = await db.synthesisDeployments.create({
      graphInstanceId: req.graphInstanceId,
      target: req.target,
      publishedUrl: deploymentUrl,
      brandingSnapshot: req.branding,
      accessControlConfig: req.accessControl,
      workspaceId: req.workspaceId,
      status: 'live',
    });

    // Step 7: Emit event
    await eventBus.publish('app.synthesized', {
      synthesisId: result.id,
      graphInstanceId: req.graphInstanceId,
      workspaceId: req.workspaceId,
      target: req.target,
      publishedUrl: deploymentUrl,
    });

    return result;
  }

  private async planSurfaces(
    graph: CanonicalGraph,
    target: SynthesisTarget,
  ): Promise<SynthesisSurfacePlan> {
    // Different targets get different surface plans
    const SURFACE_PLANS: Record<SynthesisTarget, SurfacePlanStrategy> = {
      web_app:        { includeCanvas: false, includeApprovalInbox: true,  showAllEngines: true,  layoutMode: 'operator' },
      client_portal:  { includeCanvas: false, includeApprovalInbox: false, showAllEngines: false, layoutMode: 'restricted_operator' },
      mobile_pwa:     { includeCanvas: false, includeApprovalInbox: true,  showAllEngines: true,  layoutMode: 'mobile_operator' },
      embed_widget:   { includeCanvas: false, includeApprovalInbox: false, showAllEngines: false, layoutMode: 'minimal' },
      api_endpoint:   { includeCanvas: false, includeApprovalInbox: false, showAllEngines: false, layoutMode: 'headless' },
      form_page:      { includeCanvas: false, includeApprovalInbox: false, showAllEngines: false, layoutMode: 'form_only' },
      status_page:    { includeCanvas: false, includeApprovalInbox: false, showAllEngines: false, layoutMode: 'status_only' },
      white_label:    { includeCanvas: false, includeApprovalInbox: true,  showAllEngines: true,  layoutMode: 'operator' },
    };

    return {
      strategy: SURFACE_PLANS[target],
      resolvedPanels: await surfaceCompiler.compile({
        graph,
        workspaceMode: 'operator',
        installedSurfaces: await packageRegistry.getSurfaceDefinitions(graph.packageRefs),
        activeArtifacts: await artifactService.listByGraph(graph.id),
        userId: 'synthesis_engine',
        userRoles: ['viewer'],
      }),
    };
  }

  private async generateAppCode(
    graph: CanonicalGraph,
    surfacePlan: SynthesisSurfacePlan,
    req: SynthesisRequest,
  ): Promise<AppCodeBundle> {
    // Generate a Next.js app bundle from the surface plan
    // This is a code generation step — produces real runnable code

    const routes = this.buildRoutes(surfacePlan, req.target);
    const components = this.buildComponents(surfacePlan, req);
    const apiRoutes = this.buildApiRoutes(graph, req.target);
    const configFiles = this.buildConfigFiles(req.branding, req.accessControl);

    return {
      routes,
      components,
      apiRoutes,
      configFiles,
      packageJson: this.buildPackageJson(graph),
      envTemplate: this.buildEnvTemplate(graph),
    };
  }
}
```

---

## 3. Client Portal Generator (Most Common Target)

The client portal is the most common synthesis target — businesses want to give clients a clean external surface.

```typescript
// app-synthesis-service/targets/client-portal.ts

export class ClientPortalGenerator {
  
  async generate(
    graph: CanonicalGraph,
    req: SynthesisRequest,
  ): Promise<ClientPortalBundle> {
    // Determine what the client portal exposes
    const exposedNodes = graph.nodes.filter(n => 
      n.surface?.operatorVisible !== false &&
      CLIENT_PORTAL_ALLOWED_KINDS.has(n.kind)
    );

    // Generate portal pages from exposed nodes
    const pages: PortalPage[] = exposedNodes.map(node => ({
      slug: slugify(node.surface?.title ?? node.id),
      title: node.surface?.title ?? node.id,
      component: this.nodeToPortalComponent(node),
      accessLevel: this.resolveNodeAccessLevel(node, req.accessControl),
    }));

    // Generate client-facing navigation
    const nav = this.buildNav(pages, req.branding);

    // Generate authentication page if access control is set
    const authPage = req.accessControl.visibility !== 'public'
      ? this.buildAuthPage(req.accessControl, req.branding)
      : null;

    return { pages, nav, authPage, branding: req.branding };
  }

  private nodeToPortalComponent(node: GraphNode): PortalComponent {
    // Map node kinds to portal-appropriate React components
    const PORTAL_COMPONENT_MAP: Record<string, string> = {
      'engine.document':    'PortalDocumentViewer',   // read-only by default
      'engine.form':        'PortalForm',              // interactive form
      'ui.status':          'PortalStatusCard',        // status display
      'ui.progress':        'PortalProgressTracker',   // progress display
      'artifact.share':     'PortalDeliverables',      // download artifacts
      'engine.chat':        'PortalChat',              // messaging
      'engine.calendar':    'PortalBooking',           // appointment booking
    };

    const componentName = PORTAL_COMPONENT_MAP[node.kind] ?? 'PortalGenericCard';
    return {
      componentName,
      nodeId: node.id,
      props: this.extractPortalProps(node),
    };
  }
}

// Nodes allowed in client portals (no internal operations exposed)
const CLIENT_PORTAL_ALLOWED_KINDS = new Set([
  'engine.document',
  'engine.form',
  'engine.chat',
  'engine.calendar',
  'ui.status',
  'ui.progress',
  'ui.card',
  'ui.table',
  'artifact.share',
  'logic.gate',  // approval requests from clients
]);
```

---

## 4. API Endpoint Synthesis

```typescript
// app-synthesis-service/targets/api-endpoint.ts

export class ApiEndpointSynthesizer {
  
  async generate(
    graph: CanonicalGraph,
    req: SynthesisRequest,
  ): Promise<OpenApiSpec> {
    // Generate a REST API from the graph's exposed input/output ports
    const inputNodes = graph.nodes.filter(n => n.kind === 'data.input' || n.kind === 'ui.form');
    const outputNodes = graph.nodes.filter(n => n.kind === 'artifact.export' || n.kind === 'artifact.share');
    const triggerNodes = graph.nodes.filter(n => n.kind === 'logic.trigger');

    const paths: Record<string, PathItem> = {};

    // Each trigger node becomes an API endpoint
    for (const trigger of triggerNodes) {
      const route = `/${slugify(trigger.id)}`;
      paths[route] = {
        post: {
          operationId: trigger.id,
          summary: trigger.ui?.label ?? trigger.id,
          requestBody: {
            content: {
              'application/json': {
                schema: trigger.inputSchema,
              },
            },
          },
          responses: {
            '200': {
              description: 'Graph execution queued',
              content: {
                'application/json': {
                  schema: { type: 'object', properties: { runId: { type: 'string' } } },
                },
              },
            },
          },
          security: [{ BearerAuth: [] }],
        },
      };
    }

    return {
      openapi: '3.0.0',
      info: {
        title: req.branding.appName,
        version: '1.0.0',
      },
      paths,
      components: {
        securitySchemes: {
          BearerAuth: { type: 'http', scheme: 'bearer' },
        },
      },
    };
  }
}
```

---

## 5. Synthesis Deployment Model

```typescript
// app-synthesis-service/deployment/SynthesisDeployer.ts

export class SynthesisDeployer {
  
  async deploy(
    bundle: AppCodeBundle,
    req: SynthesisRequest,
  ): Promise<string> {
    switch (req.target) {
      case 'web_app':
      case 'white_label':
      case 'client_portal':
      case 'mobile_pwa':
        return this.deployNextjsApp(bundle, req);

      case 'embed_widget':
        return this.deployStaticWidget(bundle, req);

      case 'api_endpoint':
        return this.deployApiServer(bundle, req);

      case 'form_page':
      case 'status_page':
        return this.deployStaticPage(bundle, req);

      default:
        throw new Error(`Unknown synthesis target: ${req.target}`);
    }
  }

  private async deployNextjsApp(bundle: AppCodeBundle, req: SynthesisRequest): Promise<string> {
    // Deploy via Coolify API (from coollabsio/coolify)
    const deployment = await coolifyClient.createApp({
      name: slugify(req.branding.appName),
      type: 'nextjs',
      source: 'inline',
      code: bundle,
      envVars: {
        OS_API_URL: process.env.OS_API_GATEWAY_URL,
        OS_WORKSPACE_ID: req.workspaceId,
        OS_SYNTHESIS_ID: req.synthesisId,
        OS_ACCESS_CONTROL: JSON.stringify(req.accessControl),
      },
    });

    await deployment.waitForReady();

    // Custom domain if specified
    if (req.customDomain) {
      await coolifyClient.setCustomDomain(deployment.id, req.customDomain);
    }

    return deployment.url;
  }

  private async deployStaticWidget(bundle: AppCodeBundle, req: SynthesisRequest): Promise<string> {
    // Build a single JS file that mounts as a widget
    const widgetJs = await buildWidgetBundle(bundle);
    const blobUrl = await blobStorage.upload(
      `synthesis/${req.synthesisId}/widget.js`,
      widgetJs,
      'application/javascript',
    );
    return `${process.env.CDN_BASE_URL}/synthesis/${req.synthesisId}/widget.js`;
  }
}
```

---

## 6. Synthesis Registry (Track All Published Apps)

```sql
-- migrations/synthesis_deployments.sql

create table synthesis_deployments (
  id uuid primary key,
  graph_instance_id uuid not null references graph_instances(id) on delete cascade,
  workspace_id uuid not null references workspaces(id) on delete cascade,
  target text not null,
  status text not null default 'building',
  published_url text,
  custom_domain text,
  custom_domain_status text,
  branding_snapshot jsonb not null,
  access_control_config jsonb not null,
  graph_version_at_synthesis integer not null,
  created_by uuid references users(id),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

-- Track visits to synthesized apps
create table synthesis_visits (
  id uuid primary key,
  synthesis_id uuid not null references synthesis_deployments(id) on delete cascade,
  visitor_id text,          -- anonymous or authenticated visitor
  path text,
  visited_at timestamptz not null default now()
);
```

---

## 7. Checklist

- [ ] All 8 synthesis targets are implemented and deployable
- [ ] Client portal generator filters nodes by allowed kinds (no internal ops exposed)
- [ ] API endpoint synthesis produces a valid OpenAPI 3.0 spec
- [ ] Synthesis deployments are tracked in `synthesis_deployments` table
- [ ] Custom domain support via Coolify API
- [ ] Access control (public / password / invite / SSO) implemented for all targets
- [ ] Graph changes can trigger re-synthesis (or manual re-deploy)
- [ ] Synthesis visits are tracked for analytics
- [ ] Synthesized apps connect back to the OS API (not standalone data silos)
- [ ] White-label target supports full custom CSS and branding injection
- [ ] Widget embed target produces a single JS file with mount instructions
