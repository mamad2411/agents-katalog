---
description: Huzzology project-specific development rules for archetype mapping and visualization
globs: "client/**/*", "server/**/*", "shared/**/*"
alwaysApply: true
---

# Huzzology Project Development Rules

## **Project Overview**
- **Huzzology** is a real-time visual mapping application for women's pop culture archetypes, trends, and aesthetics
- **Core Mission**: Help users understand evolving cultural moments through interactive data visualization
- **Target Users**: People outside the cultural loop who want to understand trending archetypes

## **Architecture Principles**

### **Data Flow Architecture**
- **Ingestion Layer**: Scrape from TikTok, Twitter/X, Instagram, Reddit
- **Classification Engine**: Use LLMs/embeddings to cluster content into archetypes
- **Visualization Layer**: Interactive graph with ReactFlow + Dagre
- **Storage Layer**: MongoDB/PostgreSQL for archetype metadata and relationships

### **Component Structure**
```
src/
├── components/
│   ├── graph/           # ReactFlow components
│   ├── panels/          # Side panels for archetype details
│   ├── ui/              # Reusable UI components
│   └── moderation/      # Editor mode components
├── hooks/               # Custom React hooks
├── lib/                 # Utilities and configurations
├── scrapers/            # Data ingestion modules
├── types/               # TypeScript definitions
└── utils/               # Helper functions
```

## **Data Modeling Standards**

### **Archetype Node Structure**
```typescript
interface ArchetypeNode {
  id: string;                    // kebab-case: 'clean-girl'
  label: string;                 // Display name: 'Clean Girl'
  description: string;           // Brief explanation
  keywords: string[];            // Hashtags and terms
  influences: string[];          // Related archetype IDs
  examples: ContentExample[];    // Source content
  color: string;                 // Hex color for visualization
  metadata: {
    origin_date?: string;
    peak_popularity?: string;
    influence_score: number;     // 0-1 scale
    platforms: Platform[];
  };
}
```

### **Content Example Structure**
```typescript
interface ContentExample {
  platform: 'tiktok' | 'twitter' | 'instagram' | 'reddit';
  url: string;
  caption?: string;
  timestamp: string;
  engagement_metrics?: {
    likes: number;
    shares: number;
    comments: number;
  };
  creator?: {
    username: string;
    follower_count?: number;
  };
}
```

## **React Development Standards**

### **Component Naming & Organization**
- **Graph Components**: `ArchetypeGraph`, `NodeRenderer`, `EdgeRenderer`
- **Panel Components**: `ArchetypePanel`, `ExampleViewer`, `InfluenceMap`
- **Hook Naming**: `useArchetypeData`, `useGraphLayout`, `useContentScraper`

### **State Management with Zustand**
```typescript
// ✅ DO: Use Zustand for global state
interface ArchetypeStore {
  archetypes: ArchetypeNode[];
  selectedArchetype: string | null;
  timelineFilter: DateRange;
  searchQuery: string;
  // Actions
  setSelectedArchetype: (id: string | null) => void;
  updateArchetype: (id: string, updates: Partial<ArchetypeNode>) => void;
  addArchetype: (archetype: ArchetypeNode) => void;
}

// ❌ DON'T: Use complex Redux for this project
```

### **ReactFlow Integration**
```typescript
// ✅ DO: Use proper ReactFlow patterns
const ArchetypeGraph = () => {
  const { archetypes } = useArchetypeStore();
  const nodes = useMemo(() => 
    archetypes.map(archetype => ({
      id: archetype.id,
      data: archetype,
      type: 'archetypeNode',
      position: { x: 0, y: 0 } // Will be set by Dagre
    })), [archetypes]
  );

  return (
    <ReactFlow
      nodes={nodes}
      edges={edges}
      nodeTypes={{ archetypeNode: ArchetypeNodeComponent }}
    />
  );
};
```

## **Data Scraping Standards**

### **Scraper Architecture**
- **Use Puppeteer/Playwright** for headless browser automation
- **Implement rate limiting** to avoid being blocked
- **Use rotating proxies** for large-scale scraping
- **Store raw data** before processing for debugging

### **Content Classification**
```typescript
// ✅ DO: Use embeddings for semantic clustering
interface ContentClassifier {
  generateEmbedding(content: string): Promise<number[]>;
  clusterContent(embeddings: number[][]): Promise<ClusterResult[]>;
  labelCluster(cluster: ContentExample[]): Promise<string>;
}

// ✅ DO: Implement manual moderation interface
interface ModerationAction {
  type: 'approve' | 'reject' | 'merge' | 'split';
  target: string; // archetype ID
  reason?: string;
}
```

## **UI/UX Design Principles**

### **Visual Design**
- **Bright, modern interface** with soft gradients
- **Each archetype has unique color palette** derived from its aesthetic
- **Use emoji and keyword tags** for fun, accessible exploration
- **Responsive design** for mobile and desktop

### **Interaction Patterns**
```typescript
// ✅ DO: Implement smooth transitions
const ArchetypeNode = ({ data }: { data: ArchetypeNode }) => {
  return (
    <motion.div
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      style={{ backgroundColor: data.color }}
      className="archetype-node"
    >
      <span className="archetype-emoji">{getArchetypeEmoji(data.id)}</span>
      <h3>{data.label}</h3>
    </motion.div>
  );
};
```

### **Onboarding Flow**
- **"Start with a vibe"** → Show 3 trending archetypes
- **Progressive disclosure** of features
- **Contextual tooltips** for graph interactions

## **Performance Optimization**

### **Data Loading**
- **Implement virtual scrolling** for large content lists
- **Use React.memo** for expensive graph components
- **Lazy load** archetype details and examples
- **Cache embeddings** and classification results

### **Graph Rendering**
```typescript
// ✅ DO: Optimize ReactFlow performance
const MemoizedArchetypeNode = memo(ArchetypeNodeComponent);

const useGraphLayout = (nodes: Node[], edges: Edge[]) => {
  return useMemo(() => {
    return getLayoutedElements(nodes, edges, 'TB');
  }, [nodes, edges]);
};
```

## **Content Moderation & Safety**

### **Content Filtering**
- **Filter explicit content** before classification
- **Implement user reporting** for inappropriate archetypes
- **Age-appropriate content** warnings where needed
- **Respect platform terms of service** in scraping

### **Cultural Sensitivity**
- **Avoid stereotyping** in archetype descriptions
- **Include diverse representation** in examples
- **Allow community input** on archetype definitions
- **Regular review** of potentially harmful content

## **API Design Standards**

### **RESTful Endpoints**
```typescript
// ✅ DO: Use clear, RESTful API design
GET    /api/archetypes              // List all archetypes
GET    /api/archetypes/:id          // Get specific archetype
POST   /api/archetypes              // Create new archetype
PUT    /api/archetypes/:id          // Update archetype
DELETE /api/archetypes/:id          // Delete archetype

GET    /api/archetypes/:id/examples // Get content examples
POST   /api/scrape/platform/:name  // Trigger scraping
GET    /api/trends/timeline         // Get trending data
```

### **Error Handling**
```typescript
// ✅ DO: Implement comprehensive error handling
interface ApiError {
  code: string;
  message: string;
  details?: any;
  timestamp: string;
}

// Common error codes
const ERROR_CODES = {
  ARCHETYPE_NOT_FOUND: 'ARCHETYPE_NOT_FOUND',
  SCRAPING_RATE_LIMITED: 'SCRAPING_RATE_LIMITED',
  CLASSIFICATION_FAILED: 'CLASSIFICATION_FAILED',
  INVALID_CONTENT: 'INVALID_CONTENT'
} as const;
```

## **Testing Strategy**

### **Component Testing**
- **Test graph interactions** with React Testing Library
- **Mock ReactFlow** for unit tests
- **Test archetype panel** content rendering
- **Verify search and filter** functionality

### **Integration Testing**
- **Test scraper modules** with mock data
- **Verify classification pipeline** end-to-end
- **Test API endpoints** with real database
- **Performance testing** for large datasets

### **E2E Testing**
- **User journey testing** from onboarding to exploration
- **Cross-browser compatibility** testing
- **Mobile responsiveness** testing
- **Accessibility compliance** testing

## **Deployment & Monitoring**

### **Environment Configuration**
```typescript
// ✅ DO: Use environment-specific configs
interface Config {
  NODE_ENV: 'development' | 'staging' | 'production';
  DATABASE_URL: string;
  SCRAPING_RATE_LIMIT: number;
  OPENAI_API_KEY: string;
  REDIS_URL?: string; // For caching
}
```

### **Monitoring & Analytics**
- **Track archetype popularity** over time
- **Monitor scraping success rates** and errors
- **User engagement metrics** on graph interactions
- **Performance monitoring** for graph rendering

## **Future Feature Considerations**

### **Planned Enhancements**
- **Archetype comparison tool** ("Mob Wife vs Clean Girl")
- **Trend forecasting** with ML predictions
- **User-generated content** submissions
- **Newsletter generation** from trending data
- **Mobile app** with simplified interface

### **Scalability Planning**
- **Microservices architecture** for scraping modules
- **CDN integration** for media content
- **Database sharding** for large archetype datasets
- **Real-time updates** with WebSocket connections

---

**Remember**: Huzzology is about making cultural trends accessible and fun to explore. Every feature should serve the goal of helping users understand and navigate the evolving landscape of women's pop culture archetypes.
