---
name: below-is-the-full-codex-ready-build-spec
description: Below is the full Codex-ready build spec
---

# Below is the full Codex-ready build spec

This skill defines the autonomous behavior, system prompt, and capabilities for the agent **Below is the full Codex-ready build spec**.

## Source Location
Originally discovered in Rick's Downloads at: `/Users/kalivibecoding/Downloads/Below is the full Codex-ready build spec.md`

## 🧠 Master Agent Prompt & Capabilities

Below is the full Codex-ready build spec for the game layer on top of MyFreeScoreNow.

Use this as the master prompt inside Codex.

You are building CreditQuest AI, a Cloudflare-first gamified credit intelligence platform on top of the MyFreeScoreNow 3-bureau credit report API.

Build a production-ready full-stack system with:

Frontend:
Next.js App Router
React
TypeScript
Tailwind CSS
Framer Motion
Phaser 3 for the game world
Optional PixiJS v8 for lightweight animation scenes
Zustand for client game state
TanStack Query for API fetching

Backend:
Cloudflare Workers
Cloudflare D1
Cloudflare R2
Cloudflare Queues
Cloudflare Durable Objects
Cloudflare Workflows
Cloudflare KV
Cloudflare Vectorize-ready abstraction

Integrations:
MyFreeScoreNow API
Twilio-ready notifications
SendGrid/Resend-ready email notices
Stripe-ready subscription gating
AI provider abstraction for OpenAI, Gemini, Claude, OpenRouter

Important:
Never expose MyFreeScoreNow API credentials to the browser.
Never store raw credit reports unencrypted.
Never present score changes as guaranteed.
Always label projections as estimates.
Never give legal advice inside the game UI.
Use educational language, consumer-rights language, and approval-readiness language.

Cloudflare is the correct base because Workers supports bindings to storage and platform services such as Durable Objects, D1, KV, Queues, and related primitives, and Cloudflare’s Next.js guide supports deploying Next.js apps to Workers through the OpenNext adapter.

Phaser is the right game engine for this because it is built for HTML5 games using Canvas/WebGL, and Phaser has an official React/TypeScript integration template.

PixiJS can be used for animated dashboards, map layers, cards, and overlays because PixiJS React v8 is designed for interactive graphics inside React.

Product Name
CreditQuest AI
The Credit Report Game Engine
Core User Experience
User connects MyFreeScoreNow
System pulls 3B report
System normalizes report
System builds player profile
System generates personalized game world
User sees credit report as a game
User gets missions, quests, bosses, lessons, simulations, and roadmaps
User stays active because every report refresh creates new levels and new outcomes
Main Game Worlds
1. Credit Kingdom
Main credit score, bureau score comparison, score factors, account health.

2. Debt Dungeon
Collections, charge-offs, high balances, past-due accounts, settlement education, validation education.

3. Utilization Arena
Credit card balances, limits, payoff simulations, utilization thresholds.

4. Mortgage Mountain
FHA, VA, USDA, conventional readiness, DTI, score threshold, down payment roadmap.

5. Auto Loan City
Auto approval readiness, estimated APR tiers, down payment targets, installment history.

6. Business Credit Empire
EIN, DUNS, business bank, vendor tiers, business tradelines, no-PG roadmap.

7. Student Loan Temple
Student loan status, payment plan awareness, delinquency recovery, payoff strategy.

8. Approval Castle
The final goal world where users pick what they want approved for.
Repository Structure
creditquest-ai/
  apps/
    web/
      app/
        (auth)/
        dashboard/
        game/
        roadmaps/
        simulations/
        reports/
        api/
      components/
        game/
        dashboard/
        credit/
        roadmaps/
        ui/
      lib/
        api/
        game/
        mfsn/
        simulations/
        scoring/
        auth/
      public/
        game-assets/
          maps/
          characters/
          bosses/
          icons/
          music/
    worker/
      src/
        index.ts
        routes/
          auth.routes.ts
          mfsn.routes.ts
          report.routes.ts
          game.routes.ts
          simulation.routes.ts
          roadmap.routes.ts
        services/
          mfsn.service.ts
          report-normalizer.service.ts
          game-engine.service.ts
          simulation-engine.service.ts
          roadmap-engine.service.ts
          encryption.service.ts
          ai.service.ts
        durable-objects/
          game-session.object.ts
        workflows/
          report-ingestion.workflow.ts
        queues/
          report-analysis.consumer.ts
        db/
          schema.sql
          migrations/
        types/
          mfsn.types.ts
          credit.types.ts
          game.types.ts
          roadmap.types.ts
  packages/
    shared/
      src/
        types/
        constants/
        game-rules/
        credit-rules/
  wrangler.jsonc
  package.json
  pnpm-workspace.yaml
  README.md
Environment Variables
MFSN_API_BASE_URL=https://api.myfreescorenow.com
MFSN_API_EMAIL=
MFSN_API_PASSWORD=

JWT_SECRET=
ENCRYPTION_KEY=

OPENAI_API_KEY=
GEMINI_API_KEY=
ANTHROPIC_API_KEY=
OPENROUTER_API_KEY=

TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=

STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
Database Schema
CREATE TABLE users (
  id TEXT PRIMARY KEY,
  email TEXT NOT NULL UNIQUE,
  full_name TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE mfsn_connections (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  member_email TEXT NOT NULL,
  encrypted_client_token TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'active',
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE credit_reports (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  source TEXT NOT NULL DEFAULT 'MFSN',
  raw_r2_key TEXT NOT NULL,
  report_generated_at TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE bureau_scores (
  id TEXT PRIMARY KEY,
  report_id TEXT NOT NULL,
  provider TEXT NOT NULL,
  score INTEGER,
  score_band TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (report_id) REFERENCES credit_reports(id)
);

CREATE TABLE credit_accounts (
  id TEXT PRIMARY KEY,
  report_id TEXT NOT NULL,
  provider TEXT NOT NULL,
  account_name TEXT,
  account_number_masked TEXT,
  account_type TEXT,
  account_status TEXT,
  account_rating TEXT,
  account_open INTEGER,
  balance_amount REAL,
  credit_limit_amount REAL,
  monthly_payment REAL,
  past_due_amount REAL,
  date_opened TEXT,
  reported_date TEXT,
  first_delinquency_date TEXT,
  is_negative INTEGER DEFAULT 0,
  is_delinquent INTEGER DEFAULT 0,
  dispute_flag INTEGER DEFAULT 0,
  late30_count INTEGER DEFAULT 0,
  late60_count INTEGER DEFAULT 0,
  late90_count INTEGER DEFAULT 0,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (report_id) REFERENCES credit_reports(id)
);

CREATE TABLE credit_collections (
  id TEXT PRIMARY KEY,
  report_id TEXT NOT NULL,
  provider TEXT NOT NULL,
  agency_client TEXT,
  original_creditor TEXT,
  balance_amount REAL,
  original_amount REAL,
  status TEXT,
  assigned_date TEXT,
  reported_date TEXT,
  account_number_masked TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (report_id) REFERENCES credit_reports(id)
);

CREATE TABLE credit_inquiries (
  id TEXT PRIMARY KEY,
  report_id TEXT NOT NULL,
  provider TEXT NOT NULL,
  inquiry_type TEXT,
  inquiry_name TEXT,
  reported_date TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (report_id) REFERENCES credit_reports(id)
);

CREATE TABLE score_reasons (
  id TEXT PRIMARY KEY,
  report_id TEXT NOT NULL,
  provider TEXT NOT NULL,
  code TEXT,
  description TEXT,
  effect TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (report_id) REFERENCES credit_reports(id)
);

CREATE TABLE game_profiles (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  report_id TEXT NOT NULL,
  player_level INTEGER NOT NULL,
  credit_power INTEGER NOT NULL,
  xp INTEGER NOT NULL DEFAULT 0,
  coins INTEGER NOT NULL DEFAULT 0,
  current_world TEXT NOT NULL DEFAULT 'credit_kingdom',
  avatar_class TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (report_id) REFERENCES credit_reports(id)
);

CREATE TABLE game_quests (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  report_id TEXT NOT NULL,
  quest_type TEXT NOT NULL,
  world TEXT NOT NULL,
  title TEXT NOT NULL,
  description TEXT NOT NULL,
  target_metric TEXT NOT NULL,
  current_value REAL,
  target_value REAL,
  xp_reward INTEGER NOT NULL,
  coin_reward INTEGER NOT NULL,
  difficulty TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'active',
  estimated_score_impact_min INTEGER DEFAULT 0,
  estimated_score_impact_max INTEGER DEFAULT 0,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  completed_at TEXT,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (report_id) REFERENCES credit_reports(id)
);

CREATE TABLE game_bosses (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  report_id TEXT NOT NULL,
  boss_type TEXT NOT NULL,
  world TEXT NOT NULL,
  title TEXT NOT NULL,
  source_entity_id TEXT,
  health INTEGER NOT NULL,
  severity TEXT NOT NULL,
  weakness TEXT NOT NULL,
  reward_xp INTEGER NOT NULL,
  reward_coins INTEGER NOT NULL,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  defeated_at TEXT
);

CREATE TABLE approval_roadmaps (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  report_id TEXT NOT NULL,
  roadmap_type TEXT NOT NULL,
  current_readiness_score INTEGER NOT NULL,
  target_readiness_score INTEGER NOT NULL,
  approval_stage TEXT NOT NULL,
  projected_score_gain_min INTEGER DEFAULT 0,
  projected_score_gain_max INTEGER DEFAULT 0,
  estimated_days_min INTEGER DEFAULT 0,
  estimated_days_max INTEGER DEFAULT 0,
  roadmap_json TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE credit_simulations (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  report_id TEXT NOT NULL,
  simulation_type TEXT NOT NULL,
  input_json TEXT NOT NULL,
  output_json TEXT NOT NULL,
  disclaimer TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
Shared TypeScript Types
export type BureauProvider = "EFX" | "EXP" | "TU" | "UNKNOWN";

export type GameWorld =
  | "credit_kingdom"
  | "debt_dungeon"
  | "utilization_arena"
  | "mortgage_mountain"
  | "auto_loan_city"
  | "business_credit_empire"
  | "student_loan_temple"
  | "approval_castle";

export type BossType =
  | "collection_golem"
  | "chargeoff_beast"
  | "late_payment_wraith"
  | "utilization_dragon"
  | "inquiry_swarm"
  | "public_record_titan"
  | "thin_file_shadow";

export type QuestDifficulty = "easy" | "medium" | "hard" | "boss";

export type ApprovalRoadmapType =
  | "mortgage"
  | "auto_loan"
  | "business_credit"
  | "debt_freedom"
  | "student_loan"
  | "apartment"
  | "personal_loan"
  | "credit_card";

export type GameProfile = {
  id: string;
  userId: string;
  reportId: string;
  playerLevel: number;
  creditPower: number;
  xp: number;
  coins: number;
  currentWorld: GameWorld;
  avatarClass: string;
};

export type GameQuest = {
  id: string;
  questType: string;
  world: GameWorld;
  title: string;
  description: string;
  targetMetric: string;
  currentValue: number;
  targetValue: number;
  xpReward: number;
  coinReward: number;
  difficulty: QuestDifficulty;
  estimatedScoreImpactMin: number;
  estimatedScoreImpactMax: number;
};

export type GameBoss = {
  id: string;
  bossType: BossType;
  world: GameWorld;
  title: string;
  sourceEntityId?: string;
  health: number;
  severity: "low" | "medium" | "high" | "critical";
  weakness: string;
  rewardXp: number;
  rewardCoins: number;
};

export type ApprovalRoadmap = {
  type: ApprovalRoadmapType;
  currentReadinessScore: number;
  targetReadinessScore: number;
  approvalStage: string;
  projectedScoreGainMin: number;
  projectedScoreGainMax: number;
  estimatedDaysMin: number;
  estimatedDaysMax: number;
  steps: RoadmapStep[];
};

export type RoadmapStep = {
  id: string;
  title: string;
  description: string;
  actionType:
    | "pay_down_balance"
    | "resolve_collection"
    | "fix_late_payment"
    | "age_accounts"
    | "reduce_inquiries"
    | "build_positive_history"
    | "business_credit_setup"
    | "student_loan_review";
  priority: number;
  required: boolean;
  estimatedImpactMin: number;
  estimatedImpactMax: number;
};
Game Rules Engine

Create:

packages/shared/src/game-rules/credit-game-rules.ts
export function scoreToPlayerLevel(score: number): number {
  if (!score || score < 300) return 1;
  return Math.max(1, Math.min(100, Math.floor((score - 300) / 5.5)));
}

export function scoreToCreditPower(score: number): number {
  if (!score) return 0;
  return Math.max(0, Math.min(999, Math.round(((score - 300) / 550) * 999)));
}

export function scoreBand(score: number): string {
  if (score >= 800) return "Legendary";
  if (score >= 740) return "Elite";
  if (score >= 700) return "Strong";
  if (score >= 660) return "Building";
  if (score >= 620) return "Challenged";
  if (score >= 580) return "High Risk";
  return "Critical";
}

export function utilizationSeverity(ratio: number): "low" | "medium" | "high" | "critical" {
  if (ratio >= 0.9) return "critical";
  if (ratio >= 0.7) return "high";
  if (ratio >= 0.3) return "medium";
  return "low";
}

export function negativeCountSeverity(count: number): "low" | "medium" | "high" | "critical" {
  if (count >= 8) return "critical";
  if (count >= 4) return "high";
  if (count >= 1) return "medium";
  return "low";
}
MFSN Connector Service
export class MfsnService {
  constructor(private env: Env) {}

  async login(): Promise<{ accessToken: string; sessionId: string }> {
    const form = new FormData();
    form.append("email", this.env.MFSN_API_EMAIL);
    form.append("password", this.env.MFSN_API_PASSWORD);

    const res = await fetch(`${this.env.MFSN_API_BASE_URL}/api/auth/login`, {
      method: "POST",
      body: form
    });

    if (!res.ok) {
      throw new Error(`MFSN login failed: ${res.status}`);
    }

    const json: any = await res.json();

    if (!json.success || !json.data?.accessToken) {
      throw new Error(json.message || "MFSN login failed");
    }

    return {
      accessToken: json.data.accessToken,
      sessionId: json.data.sessionId
    };
  }

  async fetch3BReport(input: {
    memberEmail: string;
    clientToken: string;
    accessToken: string;
  }): Promise<any> {
    const form = new FormData();
    form.append("email", input.memberEmail);
    form.append("client_token", input.clientToken);

    const res = await fetch(`${this.env.MFSN_API_BASE_URL}/api/auth/fetch-3B-json`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${input.accessToken}`
      },
      body: form
    });

    const json: any = await res.json();

    if (!res.ok || !json.success) {
      throw new Error(json.message || `MFSN fetch failed: ${res.status}`);
    }

    return json.data;
  }

  async logout(accessToken: string): Promise<void> {
    await fetch(`${this.env.MFSN_API_BASE_URL}/api/auth/logout`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${accessToken}`
      }
    });
  }
}
Report Normalizer
export class ReportNormalizerService {
  normalize(raw: any) {
    const providerViews = raw?.providerViews ?? [];

    const scores = providerViews.map((view: any) => ({
      provider: view.provider,
      score: view.summary?.creditScore?.score ?? null,
      reasons: view.summary?.creditScore?.scoreReasons ?? []
    }));

    const accounts = providerViews.flatMap((view: any) => {
      const provider = view.provider;

      return [
        ...(view.revolvingAccounts ?? []),
        ...(view.mortgageAccounts ?? []),
        ...(view.installmentAccounts ?? []),
        ...(view.otherAccounts ?? [])
      ].map((account: any) => ({
        provider,
        accountName: account.accountName,
        accountNumberMasked: maskAccountNumber(account.accountNumber),
        accountType: account.accountType,
        accountStatus: account.accountStatus,
        accountRating: account.accountRating,
        accountOpen: Boolean(account.accountOpen),
        balanceAmount: account.balanceAmount?.amount ?? 0,
        creditLimitAmount: account.creditLimitAmount?.amount ?? 0,
        monthlyPayment: account.monthlyPayment?.amount ?? 0,
        pastDueAmount: account.pastDueAmount?.amount ?? 0,
        dateOpened: account.dateOpened,
        reportedDate: account.reportedDate,
        firstDelinquencyDate: account.firstDelinquencyDate,
        isNegative: Boolean(account.isNegative),
        isDelinquent: Boolean(account.isDelinquent),
        disputeFlag: Boolean(account.disputeFlag),
        late30Count: account.late30Count ?? 0,
        late60Count: account.late60Count ?? 0,
        late90Count: account.late90Count ?? 0
      }));
    });

    const collections = providerViews.flatMap((view: any) =>
      (view.collections ?? []).map((item: any) => ({
        provider: view.provider,
        agencyClient: item.agencyClient,
        originalCreditor: item.originalCreditor,
        balanceAmount: item.amount?.amount ?? 0,
        originalAmount: item.orginalAmountOwed?.amount ?? 0,
        status: item.status,
        assignedDate: item.assignedDate,
        reportedDate: item.reportedDate,
        accountNumberMasked: maskAccountNumber(item.accountNumber)
      }))
    );

    const inquiries = providerViews.flatMap((view: any) =>
      (view.inquiries ?? []).map((item: any) => ({
        provider: view.provider,
        inquiryType: item.type,
        inquiryName: item.contactInformation?.contactName,
        reportedDate: item.reportedDate
      }))
    );

    const summaries = providerViews.map((view: any) => ({
      provider: view.provider,
      totalNegativeAccounts: view.summary?.totalNegativeAccounts ?? 0,
      totalCollections: view.summary?.totalCollections ?? 0,
      totalInquiries: view.summary?.totalInquires ?? 0,
      averageAccountAgeMonths: view.summary?.averageAccountAgeMonths ?? 0,
      lengthOfCreditHistoryMonths: view.summary?.lengthOfCreditHistoryMonths ?? 0,
      revolvingDebtToCreditRatio:
        view.summary?.revolvingAccounts?.debtToCreditRatio ?? 0,
      revolvingBalance:
        view.summary?.revolvingAccounts?.balance?.amount ?? 0,
      revolvingLimit:
        view.summary?.revolvingAccounts?.creditLimit?.amount ?? 0
    }));

    return {
      scores,
      accounts,
      collections,
      inquiries,
      summaries
    };
  }
}

function maskAccountNumber(value?: string) {
  if (!value) return null;
  const last4 = value.slice(-4);
  return `****${last4}`;
}
Game Engine Service
import {
  scoreToPlayerLevel,
  scoreToCreditPower,
  utilizationSeverity,
  negativeCountSeverity
} from "@creditquest/shared/game-rules/credit-game-rules";

export class GameEngineService {
  generateGameProfile(input: {
    userId: string;
    reportId: string;
    normalized: any;
  }) {
    const validScores = input.normalized.scores
      .map((s: any) => s.score)
      .filter(Boolean);

    const avgScore =
      validScores.length > 0
        ? Math.round(validScores.reduce((a: number, b: number) => a + b, 0) / validScores.length)
        : 0;

    return {
      userId: input.userId,
      reportId: input.reportId,
      playerLevel: scoreToPlayerLevel(avgScore),
      creditPower: scoreToCreditPower(avgScore),
      xp: 0,
      coins: 0,
      currentWorld: "credit_kingdom",
      avatarClass: this.pickAvatarClass(avgScore)
    };
  }

  generateBosses(input: { userId: string; reportId: string; normalized: any }) {
    const bosses: any[] = [];

    for (const collection of input.normalized.collections) {
      bosses.push({
        userId: input.userId,
        reportId: input.reportId,
        bossType: "collection_golem",
        world: "debt_dungeon",
        title: `${collection.agencyClient || "Collection"} Golem`,
        sourceEntityId: collection.accountNumberMasked,
        health: Math.min(100, Math.max(25, Math.round((collection.balanceAmount || 100) / 25))),
        severity: collection.balanceAmount >= 2500 ? "critical" : collection.balanceAmount >= 1000 ? "high" : "medium",
        weakness: "Review validation, accuracy, reporting dates, ownership, balance, and dispute rights.",
        rewardXp: 150,
        rewardCoins: 75
      });
    }

    const highUtilization = input.normalized.summaries.find(
      (s: any) => s.revolvingDebtToCreditRatio >= 0.3
    );

    if (highUtilization) {
      bosses.push({
        userId: input.userId,
        reportId: input.reportId,
        bossType: "utilization_dragon",
        world: "utilization_arena",
        title: "Utilization Dragon",
        health: Math.round(highUtilization.revolvingDebtToCreditRatio * 100),
        severity: utilizationSeverity(highUtilization.revolvingDebtToCreditRatio),
        weakness: "Lower revolving balances below 29%, then below 9%, while maintaining on-time payments.",
        rewardXp: 200,
        rewardCoins: 100
      });
    }

    const negativeCount = Math.max(
      ...input.normalized.summaries.map((s: any) => s.totalNegativeAccounts ?? 0),
      0
    );

    if (negativeCount > 0) {
      bosses.push({
        userId: input.userId,
        reportId: input.reportId,
        bossType: "late_payment_wraith",
        world: "credit_kingdom",
        title: "Negative History Wraith",
        health: negativeCount * 20,
        severity: negativeCountSeverity(negativeCount),
        weakness: "Audit account accuracy, payment history, dates, status, and consumer dispute rights.",
        rewardXp: 250,
        rewardCoins: 125
      });
    }

    return bosses;
  }

  generateQuests(input: { userId: string; reportId: string; normalized: any }) {
    const quests: any[] = [];

    const revolvingSummary = input.normalized.summaries.find(
      (s: any) => s.revolvingLimit > 0
    );

    if (revolvingSummary?.revolvingDebtToCreditRatio > 0.09) {
      const targetBalance9 = Math.floor(revolvingSummary.revolvingLimit * 0.09);
      const paydownNeeded = Math.max(0, revolvingSummary.revolvingBalance - targetBalance9);

      quests.push({
        userId: input.userId,
        reportId: input.reportId,
        questType: "pay_down_utilization",
        world: "utilization_arena",
        title: "Lower the Utilization Shield",
        description: `Reduce revolving balances by approximately $${Math.round(paydownNeeded)} to target the 9% utilization zone.`,
        targetMetric: "revolving_balance",
        currentValue: revolvingSummary.revolvingBalance,
        targetValue: targetBalance9,
        xpReward: 300,
        coinReward: 150,
        difficulty: paydownNeeded > 3000 ? "hard" : "medium",
        estimatedScoreImpactMin: 10,
        estimatedScoreImpactMax: 55
      });
    }

    const collectionsCount = input.normalized.collections.length;

    if (collectionsCount > 0) {
      quests.push({
        userId: input.userId,
        reportId: input.reportId,
        questType: "collection_review",
        world: "debt_dungeon",
        title: "Audit Collection Monsters",
        description: `Review ${collectionsCount} collection item(s) for ownership, balance accuracy, date accuracy, and validation support.`,
        targetMetric: "collections_reviewed",
        currentValue: 0,
        targetValue: collectionsCount,
        xpReward: 250,
        coinReward: 100,
        difficulty: collectionsCount >= 4 ? "hard" : "medium",
        estimatedScoreImpactMin: 0,
        estimatedScoreImpactMax: 40
      });
    }

    const hardInquiries = input.normalized.inquiries.filter(
      (i: any) => i.inquiryType === "HARD"
    );

    if (hardInquiries.length > 2) {
      quests.push({
        userId: input.userId,
        reportId: input.reportId,
        questType: "inquiry_cooldown",
        world: "approval_castle",
        title: "Stop the Inquiry Swarm",
        description: "Avoid unnecessary new applications while preparing for approval goals.",
        targetMetric: "new_inquiries",
        currentValue: hardInquiries.length,
        targetValue: 0,
        xpReward: 100,
        coinReward: 50,
        difficulty: "easy",
        estimatedScoreImpactMin: 0,
        estimatedScoreImpactMax: 15
      });
    }

    return quests;
  }

  private pickAvatarClass(avgScore: number) {
    if (avgScore >= 740) return "Approval Knight";
    if (avgScore >= 680) return "Credit Ranger";
    if (avgScore >= 620) return "Rebuild Warrior";
    return "Fresh Start Fighter";
  }
}
Simulation Engine
export class SimulationEngineService {
  simulatePaydown(input: {
    currentScore: number;
    currentRevolvingBalance: number;
    currentRevolvingLimit: number;
    paydownAmount: number;
  }) {
    const beforeRatio = input.currentRevolvingLimit > 0
      ? input.currentRevolvingBalance / input.currentRevolvingLimit
      : 0;

    const afterBalance = Math.max(0, input.currentRevolvingBalance - input.paydownAmount);

    const afterRatio = input.currentRevolvingLimit > 0
      ? afterBalance / input.currentRevolvingLimit
      : 0;

    const estimatedGain = estimateUtilizationGain(beforeRatio, afterRatio, input.currentScore);

    return {
      before: {
        balance: input.currentRevolvingBalance,
        utilization: beforeRatio,
        score: input.currentScore
      },
      after: {
        balance: afterBalance,
        utilization: afterRatio,
        estimatedScoreMin: input.currentScore + estimatedGain.min,
        estimatedScoreMax: input.currentScore + estimatedGain.max
      },
      disclaimer:
        "This is an educational estimate, not a guaranteed credit score result. Actual score changes depend on bureau data, scoring model, timing, reporting updates, and full credit profile."
    };
  }

  simulateCollectionResolution(input: {
    currentScore: number;
    collectionCount: number;
    collectionBalance: number;
    resolutionType: "deleted" | "paid" | "settled" | "validated";
  }) {
    let min = 0;
    let max = 0;

    if (input.resolutionType === "deleted") {
      min = input.currentScore < 620 ? 10 : 0;
      max = input.currentScore < 620 ? 60 : 25;
    }

    if (input.resolutionType === "paid" || input.resolutionType === "settled") {
      min = 0;
      max = 20;
    }

    return {
      estimatedScoreMin: input.currentScore + min,
      estimatedScoreMax: input.currentScore + max,
      approvalImpact:
        input.resolutionType === "deleted"
          ? "May improve approval profile if the collection is removed from one or more bureaus."
          : "May improve manual underwriting and lender perception even when score impact is limited.",
      disclaimer:
        "Collection outcomes are estimates. Deletion, updating, settlement, or payment can affect each scoring model differently."
    };
  }
}

function estimateUtilizationGain(before: number, after: number, score: number) {
  let min = 0;
  let max = 0;

  if (before > 0.9 && after <= 0.3) {
    min = 20;
    max = 75;
  } else if (before > 0.7 && after <= 0.3) {
    min = 15;
    max = 55;
  } else if (before > 0.3 && after <= 0.09) {
    min = 10;
    max = 40;
  } else if (before > 0.09 && after <= 0.09) {
    min = 3;
    max = 20;
  }

  if (score >= 740) {
    max = Math.min(max, 25);
  }

  return { min, max };
}
Roadmap Engine
export class RoadmapEngineService {
  buildMortgageRoadmap(normalized: any) {
    const avgScore = averageScore(normalized);
    const utilization = maxUtilization(normalized);
    const negatives = maxNegativeAccounts(normalized);
    const collections = normalized.collections.length;

    let readiness = 0;

    if (avgScore >= 580) readiness += 20;
    if (avgScore >= 620) readiness += 15;
    if (avgScore >= 680) readiness += 20;
    if (utilization <= 0.29) readiness += 15;
    if (utilization <= 0.09) readiness += 10;
    if (negatives === 0) readiness += 15;
    if (collections === 0) readiness += 5;

    const steps = [];

    if (avgScore < 580) {
      steps.push(step("raise_score_580", "Reach FHA Minimum Score Zone", "Build toward at least the 580 score zone for stronger FHA readiness.", "build_positive_history", 1, true, 20, 80));
    }

    if (avgScore < 640) {
      steps.push(step("raise_score_640", "Reach Stronger Mortgage Review Zone", "Improve score strength to make lender review easier.", "build_positive_history", 2, true, 10, 70));
    }

    if (utilization > 0.29) {
      steps.push(step("lower_utilization_29", "Lower Revolving Utilization Below 29%", "Pay down revolving balances to reduce credit risk signals.", "pay_down_balance", 3, true, 10, 55));
    }

    if (collections > 0) {
      steps.push(step("review_collections", "Review Collection Accounts", "Review collections for accuracy, ownership, balance, status, and reporting dates.", "resolve_collection", 4, true, 0, 50));
    }

    return {
      type: "mortgage",
      currentReadinessScore: Math.min(100, readiness),
      targetReadinessScore: 85,
      approvalStage: readiness >= 85 ? "Mortgage Ready" : readiness >= 60 ? "Almost Ready" : "Needs Work",
      projectedScoreGainMin: steps.reduce((sum, s) => sum + s.estimatedImpactMin, 0),
      projectedScoreGainMax: steps.reduce((sum, s) => sum + s.estimatedImpactMax, 0),
      estimatedDaysMin: 30,
      estimatedDaysMax: 180,
      steps
    };
  }

  buildAutoLoanRoadmap(normalized: any) {
    const avgScore = averageScore(normalized);
    const negatives = maxNegativeAccounts(normalized);
    const utilization = maxUtilization(normalized);

    const readiness =
      (avgScore >= 620 ? 30 : 10) +
      (avgScore >= 680 ? 25 : 0) +
      (utilization <= 0.29 ? 20 : 5) +
      (negatives === 0 ? 20 : 5);

    const steps = [];

    if (avgScore < 660) {
      steps.push(step("score_660_auto", "Reach Better Auto Loan Tier", "Build toward a stronger score tier before applying.", "build_positive_history", 1, true, 10, 60));
    }

    if (utilization > 0.29) {
      steps.push(step("auto_utilization", "Lower Card Balances Before Auto Application", "Reduce revolving debt to improve approval and APR position.", "pay_down_balance", 2, true, 10, 55));
    }

    return {
      type: "auto_loan",
      currentReadinessScore: Math.min(100, readiness),
      targetReadinessScore: 80,
      approvalStage: readiness >= 80 ? "Auto Ready" : readiness >= 55 ? "Close" : "Needs Work",
      projectedScoreGainMin: steps.reduce((sum, s) => sum + s.estimatedImpactMin, 0),
      projectedScoreGainMax: steps.reduce((sum, s) => sum + s.estimatedImpactMax, 0),
      estimatedDaysMin: 15,
      estimatedDaysMax: 120,
      steps
    };
  }

  buildBusinessCreditRoadmap(normalized: any) {
    return {
      type: "business_credit",
      currentReadinessScore: 25,
      targetReadinessScore: 90,
      approvalStage: "Business Foundation Needed",
      projectedScoreGainMin: 0,
      projectedScoreGainMax: 0,
      estimatedDaysMin: 30,
      estimatedDaysMax: 180,
      steps: [
        step("ein", "Confirm EIN and Business Entity", "Set up legal business foundation.", "business_credit_setup", 1, true, 0, 0),
        step("business_bank", "Open Business Bank Account", "Separate business and personal finances.", "business_credit_setup", 2, true, 0, 0),
        step("duns", "Create or Confirm DUNS Profile", "Prepare for vendor reporting and business identity.", "business_credit_setup", 3, true, 0, 0),
        step("tier1", "Start Tier 1 Vendor Accounts", "Build business credit reporting history.", "business_credit_setup", 4, true, 0, 0)
      ]
    };
  }
}

function averageScore(normalized: any) {
  const scores = normalized.scores.map((s: any) => s.score).filter(Boolean);
  return scores.length ? Math.round(scores.reduce((a: number, b: number) => a + b, 0) / scores.length) : 0;
}

function maxUtilization(normalized: any) {
  return Math.max(...normalized.summaries.map((s: any) => s.revolvingDebtToCreditRatio ?? 0), 0);
}

function maxNegativeAccounts(normalized: any) {
  return Math.max(...normalized.summaries.map((s: any) => s.totalNegativeAccounts ?? 0), 0);
}

function step(
  id: string,
  title: string,
  description: string,
  actionType: string,
  priority: number,
  required: boolean,
  estimatedImpactMin: number,
  estimatedImpactMax: number
) {
  return {
    id,
    title,
    description,
    actionType,
    priority,
    required,
    estimatedImpactMin,
    estimatedImpactMax
  };
}
Game UI Pages
/game
Main playable map

/game/worlds/credit-kingdom
Score and account health

/game/worlds/debt-dungeon
Collections, charge-offs, past-due accounts

/game/worlds/utilization-arena
Paydown simulator

/game/worlds/mortgage-mountain
Mortgage roadmap

/game/worlds/auto-loan-city
Auto loan roadmap

/game/worlds/business-credit-empire
Business credit builder

/game/simulations
What-if simulator

/game/rewards
XP, coins, badges, unlocks

/game/story
AI-generated personalized financial journey
Phaser Game Shell
"use client";

import { useEffect, useRef } from "react";
import Phaser from "phaser";
import { CreditQuestMapScene } from "./scenes/CreditQuestMapScene";

export function CreditQuestGameCanvas() {
  const parentRef = useRef<HTMLDivElement | null>(null);
  const gameRef = useRef<Phaser.Game | null>(null);

  useEffect(() => {
    if (!parentRef.current || gameRef.current) return;

    gameRef.current = new Phaser.Game({
      type: Phaser.AUTO,
      parent: parentRef.current,
      width: 1280,
      height: 720,
      backgroundColor: "#111827",
      physics: {
        default: "arcade"
      },
      scene: [CreditQuestMapScene],
      scale: {
        mode: Phaser.Scale.FIT,
        autoCenter: Phaser.Scale.CENTER_BOTH
      }
    });

    return () => {
      gameRef.current?.destroy(true);
      gameRef.current = null;
    };
  }, []);

  return <div ref={parentRef} className="h-full w-full overflow-hidden rounded-2xl" />;
}
Phaser Map Scene
import Phaser from "phaser";

export class CreditQuestMapScene extends Phaser.Scene {
  constructor() {
    super("CreditQuestMapScene");
  }

  preload() {
    this.load.image("map", "/game-assets/maps/creditquest-map.png");
    this.load.image("hero", "/game-assets/characters/hero.png");
    this.load.image("debtBoss", "/game-assets/bosses/collection-golem.png");
  }

  create() {
    this.add.image(640, 360, "map").setScale(1);

    const hero = this.physics.add.sprite(180, 520, "hero").setScale(0.6);

    const worlds = [
      { x: 220, y: 460, label: "Credit Kingdom" },
      { x: 440, y: 500, label: "Debt Dungeon" },
      { x: 650, y: 420, label: "Utilization Arena" },
      { x: 840, y: 300, label: "Mortgage Mountain" },
      { x: 1010, y: 450, label: "Business Empire" }
    ];

    worlds.forEach((world) => {
      const zone = this.add.circle(world.x, world.y, 36, 0xffffff, 0.25).setInteractive();
      this.add.text(world.x - 70, world.y + 45, world.label, {
        fontSize: "18px",
        color: "#ffffff"
      });

      zone.on("pointerdown", () => {
        window.dispatchEvent(
          new CustomEvent("creditquest:world-selected", {
            detail: { label: world.label }
          })
        );
      });
    });

    this.add.text(32, 32, "CreditQuest AI", {
      fontSize: "32px",
      color: "#ffffff",
      fontStyle: "bold"
    });
  }
}
API Routes
POST /api/mfsn/connect
Stores member email and encrypted client token.

POST /api/reports/fetch
Fetches latest MFSN 3B report.

GET /api/reports/latest
Returns normalized latest report.

POST /api/game/generate
Generates profile, quests, bosses, and roadmaps.

GET /api/game/state
Returns current game state.

POST /api/simulations/paydown
Runs paydown simulator.

POST /api/simulations/collection-resolution
Runs collection simulator.

GET /api/roadmaps/mortgage
Returns mortgage roadmap.

GET /api/roadmaps/auto-loan
Returns auto roadmap.

GET /api/roadmaps/business-credit
Returns business credit roadmap.
Worker Route Example
import { Hono } from "hono";
import { MfsnService } from "../services/mfsn.service";
import { ReportNormalizerService } from "../services/report-normalizer.service";
import { GameEngineService } from "../services/game-engine.service";
import { RoadmapEngineService } from "../services/roadmap-engine.service";

export const reportRoutes = new Hono<{ Bindings: Env }>();

reportRoutes.post("/fetch", async (c) => {
  const user = c.get("user");
  const body = await c.req.json();

  const mfsn = new MfsnService(c.env);
  const normalizer = new ReportNormalizerService();
  const gameEngine = new GameEngineService();
  const roadmapEngine = new RoadmapEngineService();

  const login = await mfsn.login();

  try {
    const rawReport = await mfsn.fetch3BReport({
      memberEmail: body.memberEmail,
      clientToken: body.clientToken,
      accessToken: login.accessToken
    });

    const reportId = crypto.randomUUID();
    const rawKey = `reports/${user.id}/${reportId}.json`;

    await c.env.RAW_REPORTS.put(rawKey, JSON.stringify(rawReport), {
      httpMetadata: {
        contentType: "application/json"
      }
    });

    const normalized = normalizer.normalize(rawReport);

    const profile = gameEngine.generateGameProfile({
      userId: user.id,
      reportId,
      normalized
    });

    const bosses = gameEngine.generateBosses({
      userId: user.id,
      reportId,
      normalized
    });

    const quests = gameEngine.generateQuests({
      userId: user.id,
      reportId,
      normalized
    });

    const roadmaps = {
      mortgage: roadmapEngine.buildMortgageRoadmap(normalized),
      autoLoan: roadmapEngine.buildAutoLoanRoadmap(normalized),
      businessCredit: roadmapEngine.buildBusinessCreditRoadmap(normalized)
    };

    return c.json({
      success: true,
      reportId,
      profile,
      bosses,
      quests,
      roadmaps
    });
  } finally {
    await mfsn.logout(login.accessToken);
  }
});
Main Dashboard Layout
export default function GameDashboardPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-white">
      <section className="grid grid-cols-12 gap-6 p-6">
        <aside className="col-span-3 rounded-2xl bg-slate-900 p-5">
          <h2 className="text-xl font-bold">Player Profile</h2>
          <div className="mt-4">
            <p>Level 18 Rebuild Warrior</p>
            <p>Credit Power: 621</p>
            <p>XP: 2,450</p>
            <p>Coins: 800</p>
          </div>
        </aside>

        <section className="col-span-6 rounded-2xl bg-slate-900 p-4">
          <div className="h-[520px]">
            <CreditQuestGameCanvas />
          </div>
        </section>

        <aside className="col-span-3 rounded-2xl bg-slate-900 p-5">
          <h2 className="text-xl font-bold">Active Quests</h2>
          <div className="mt-4 space-y-3">
            <QuestCard title="Lower Utilization Shield" reward="+300 XP" />
            <QuestCard title="Audit Collection Monsters" reward="+250 XP" />
            <QuestCard title="Stop Inquiry Swarm" reward="+100 XP" />
          </div>
        </aside>
      </section>
    </main>
  );
}

function QuestCard({ title, reward }: { title: string; reward: string }) {
  return (
    <div className="rounded-xl border border-slate-700 bg-slate-800 p-4">
      <h3 className="font-semibold">{title}</h3>
      <p className="text-sm text-slate-300">{reward}</p>
    </div>
  );
}
AI Story Prompt
You are the CreditQuest AI story engine.

Turn the user's normalized credit report into a motivational, game-like journey.

Rules:
Do not promise guaranteed score increases.
Do not provide legal advice.
Do not shame the user.
Do not mention sensitive PII.
Use plain English.
Make it fun, empowering, and specific to their report.
Tie every story element to an actual credit factor.

Input:
Average score
Bureau score spread
Utilization
Collections count
Negative account count
Late payment count
Inquiry count
Approval goal
Roadmap steps

Output JSON:
{
  "storyTitle": "",
  "playerClass": "",
  "openingScene": "",
  "mainVillains": [],
  "currentMission": "",
  "nextUnlock": "",
  "encouragement": ""
}
Required Game Mechanics
XP:
Earned from education, report refreshes, completed tasks, simulator use, roadmap progress.

Coins:
Earned from completing quests.
Used to unlock lessons, premium tools, badges, consult discounts, templates.

Levels:
Based on average credit score plus completed financial education.

Bosses:
Generated from report problems.

Quests:
Generated from report action items.

Worlds:
Unlocked by goals and report needs.

Roadmaps:
Mortgage, auto, business credit, debt freedom, student loan, apartment approval.

Simulations:
Paydown, collection resolution, inquiry cooldown, account aging, new secured card, business credit tiering.

Badges:
Utilization Slayer
Debt Dungeon Survivor
Mortgage Mountain Climber
Auto Approval Ready
Business Credit Builder
On-Time Streak Master
Report Refresh Champion
Compliance Rules
Every projected score result must say:
Estimated. Not guaranteed.

Every dispute-related quest must say:
Review for accuracy and consumer-rights education.

Never say:
This will delete.
This guarantees approval.
This raises your score by X.
This is legal advice.

Use:
May help.
Estimated impact.
Potential effect.
Approval readiness.
Educational review.
Accuracy review.
Codex Task List
1. Create monorepo structure.
2. Build shared TypeScript types.
3. Build D1 schema and migrations.
4. Build MFSN connector service.
5. Build encryption service.
6. Build report normalizer.
7. Build game rules engine.
8. Build game profile generator.
9. Build boss generator.
10. Build quest generator.
11. Build roadmap generator.
12. Build simulation engine.
13. Build Cloudflare Worker API routes.
14. Build Phaser game canvas.
15. Build React dashboard.
16. Build world pages.
17. Build simulation UI.
18. Build roadmap UI.
19. Build report refresh workflow.
20. Build queue consumer for background report analysis.
21. Build AI story generator abstraction.
22. Build Twilio notification abstraction.
23. Build Stripe gating abstraction.
24. Add tests for normalizer, game rules, simulations, and roadmaps.
25. Add README with setup, deploy, and security instructions.
Final System Behavior
When a user connects MyFreeScoreNow:

1. Fetch the report.
2. Store raw report securely.
3. Normalize all credit data.
4. Calculate credit power.
5. Generate player level.
6. Generate worlds.
7. Generate bosses from derogatory items.
8. Generate quests from utilization, negatives, collections, inquiries, thin file, and payment history.
9. Generate approval roadmaps.
10. Generate simulations.
11. Generate personalized story.
12. Display the report as a playable financial game.

This gives Codex the full game-layer system to finalize into a real repo.
