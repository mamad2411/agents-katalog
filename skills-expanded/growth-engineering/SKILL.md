---
name: growth-engineering
description: "Growth engineering - PLG, referral, viral loops, onboarding optimization."
---

# Growth Engineering

## PLG (Product-Led Growth) Implementation

### PLG Flywheel

```
User Signs Up (Free)
    |
    v
Experiences Value (Aha Moment)
    |
    v
Invites Team/Colleagues
    |
    v
Team Adopts Product
    |
    v
Usage Grows -> Hits Limits
    |
    v
Converts to Paid
    |
    v
Expands (More Seats/Features)
    |
    +---> Refers New Users (loop back)
```

### PLG Architecture

```typescript
interface PLGConfig {
  freeTier: {
    features: string[];
    limits: Record<string, number>;        // { projects: 3, members: 5, storage_gb: 1 }
    duration: "unlimited" | number;         // gun cinsinden veya sinirsiz
  };
  trialTier: {
    features: string[];
    duration_days: number;
    requires_cc: boolean;
  };
  paidTiers: Array<{
    name: string;
    price_monthly: number;
    price_annual: number;
    features: string[];
    limits: Record<string, number>;
  }>;
  gates: FeatureGate[];
}

interface FeatureGate {
  feature: string;
  gate_type: "hard" | "soft" | "usage";
  free_limit?: number;
  upgrade_prompt: string;
  cta: string;
}

// Feature gate middleware
function checkFeatureGate(feature: string) {
  return async (req: Request, res: Response, next: NextFunction) => {
    const user = req.user;
    const gate = gates.find(g => g.feature === feature);

    if (!gate) return next();

    const plan = await getUserPlan(user.id);
    const usage = await getFeatureUsage(user.id, feature);

    if (gate.gate_type === "hard" && plan.tier === "free") {
      return res.status(403).json({
        error: "UPGRADE_REQUIRED",
        message: gate.upgrade_prompt,
        cta: gate.cta,
        upgrade_url: `/billing/upgrade?feature=${feature}`,
      });
    }

    if (gate.gate_type === "usage" && gate.free_limit && usage >= gate.free_limit) {
      // Soft limit: izin ver ama uyar
      res.setHeader("X-Usage-Warning", gate.upgrade_prompt);
      await trackEvent(user.id, "feature_gate_hit", { feature, usage, limit: gate.free_limit });
    }

    next();
  };
}
```

### Aha Moment Definition

| Urun Tipi | Aha Moment Ornegi | Metrik |
|-----------|-------------------|--------|
| Project Management | Ilk task'i tamamlama | task_completed (first) |
| Analytics | Ilk dashboard olusturma | dashboard_created (first) |
| Communication | Ilk mesaj gonderme | message_sent (first) |
| Development Tool | Ilk basarili build | build_succeeded (first) |
| Design Tool | Ilk export/share | design_exported (first) |

```typescript
interface AhaMoment {
  event: string;
  conditions: Record<string, unknown>;
  time_window_hours: number;             // Bu sure icinde olursa "activated"
  activation_rate_target: number;        // %40-60 hedef
}

const ahaMoment: AhaMoment = {
  event: "project_created_with_members",
  conditions: { member_count: { gte: 2 }, tasks_added: { gte: 3 } },
  time_window_hours: 72,                 // Kayittan sonra 72 saat icinde
  activation_rate_target: 0.50,
};
```

## Referral System Design

### Referral Architecture

```typescript
interface ReferralProgram {
  id: string;
  name: string;
  reward_type: "two_sided" | "referrer_only" | "referee_only";
  referrer_reward: Reward;
  referee_reward: Reward;
  rules: ReferralRules;
}

interface Reward {
  type: "credit" | "discount" | "free_months" | "feature_unlock" | "cash";
  amount: number;
  currency?: string;
  description: string;
}

interface ReferralRules {
  max_referrals_per_user: number;        // spam onleme
  qualification_event: string;            // ne zaman odul verilir
  qualification_window_days: number;      // sure siniri
  anti_fraud: AntiFraudRules;
}

interface AntiFraudRules {
  same_ip_block: boolean;
  email_domain_block: string[];           // disposable email engelle
  min_activity_threshold: number;         // minimum kullanim
  cooldown_hours: number;                 // ayni kisi icin bekleme
}
```

### Referral Flow

```
Referrer                          Referee
   |                                |
   |-- Shares unique link --------> |
   |                                |-- Signs up
   |                                |-- Completes qualification
   |                                |     (first purchase / activation)
   |<-- Notification: Reward! ------|
   |-- Reward credited              |-- Reward credited
   |                                |
   v                                v
Track: referral_completed       Track: referred_user_activated
```

### Referral Schema

```sql
CREATE TABLE referrals (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  referrer_id UUID NOT NULL REFERENCES users(id),
  referee_id UUID REFERENCES users(id),
  referral_code VARCHAR(20) UNIQUE NOT NULL,
  referral_link TEXT NOT NULL,
  status VARCHAR(20) DEFAULT 'pending',  -- pending, signed_up, qualified, rewarded, expired
  channel VARCHAR(50),                    -- email, social, direct_link
  created_at TIMESTAMPTZ DEFAULT NOW(),
  signed_up_at TIMESTAMPTZ,
  qualified_at TIMESTAMPTZ,
  rewarded_at TIMESTAMPTZ,
  referrer_reward_amount DECIMAL,
  referee_reward_amount DECIMAL,
  metadata JSONB DEFAULT '{}'
);

CREATE INDEX idx_referrals_referrer ON referrals(referrer_id);
CREATE INDEX idx_referrals_code ON referrals(referral_code);
CREATE INDEX idx_referrals_status ON referrals(status);

-- Referral metrikleri
SELECT
  referrer_id,
  COUNT(*) AS total_referrals,
  COUNT(CASE WHEN status = 'signed_up' THEN 1 END) AS signups,
  COUNT(CASE WHEN status = 'qualified' THEN 1 END) AS qualified,
  COUNT(CASE WHEN status = 'rewarded' THEN 1 END) AS rewarded,
  ROUND(100.0 * COUNT(CASE WHEN status = 'qualified' THEN 1 END) /
    NULLIF(COUNT(CASE WHEN status = 'signed_up' THEN 1 END), 0), 1) AS conversion_rate
FROM referrals
GROUP BY referrer_id
ORDER BY qualified DESC;
```

## Viral Loops

### Viral Loop Types

| Tip | Mekanizma | Ornek | K-Factor Hedef |
|-----|-----------|-------|---------------|
| Word of Mouth | Organik tavsiye | Slack, Notion | 0.3-0.5 |
| Incentivized | Odul ile tavsiye | Dropbox (500MB) | 0.5-0.8 |
| Embedded | Urunde gorulme | "Made with X" | 0.2-0.4 |
| Collaborative | Birlikte kullanim | Google Docs invite | 0.6-1.0 |
| Social Proof | Paylasim/showcase | Spotify Wrapped | 0.3-0.6 |
| Content | Icerik uretimi | Canva, Figma links | 0.2-0.4 |

### K-Factor (Viral Coefficient)

```typescript
interface ViralMetrics {
  invites_per_user: number;       // ortalama gonderilen davet
  invite_conversion_rate: number; // davetin kabul orani
  cycle_time_days: number;        // bir loop'un suresi
}

function calculateKFactor(metrics: ViralMetrics): {
  kFactor: number;
  viral: boolean;
  doublingTimeDays: number | null;
} {
  // K = invites_per_user * conversion_rate
  const k = metrics.invites_per_user * metrics.invite_conversion_rate;

  return {
    kFactor: Math.round(k * 100) / 100,
    viral: k > 1,     // K > 1 = organik buyume
    doublingTimeDays: k > 1
      ? Math.round(metrics.cycle_time_days * Math.log(2) / Math.log(k))
      : null,
  };
}

// Ornek: 3 invite * %25 conversion = K=0.75 (viral degil ama katkisi var)
// Ornek: 5 invite * %30 conversion = K=1.5 (viral!)
```

### Viral Loop Implementation

```typescript
// "Made with [Product]" badge (embedded viral loop)
function generateShareableBadge(projectId: string, userId: string): string {
  const trackingUrl = `https://app.example.com/r/${encodeBase64(userId)}?ref=badge&project=${projectId}`;
  return `
    <a href="${trackingUrl}" target="_blank" rel="noopener">
      <img src="https://app.example.com/badge.svg" alt="Made with Example" width="120" height="28" />
    </a>
  `;
}

// Collaborative viral loop
async function inviteToProject(
  inviterId: string,
  projectId: string,
  emails: string[]
): Promise<InviteResult[]> {
  const results: InviteResult[] = [];

  for (const email of emails) {
    // Rate limit: max 10 invite per project per day
    const todayInvites = await getInviteCount(inviterId, projectId, "today");
    if (todayInvites >= 10) {
      results.push({ email, status: "rate_limited" });
      continue;
    }

    const invite = await createInvite({ inviterId, projectId, email });
    await sendInviteEmail(email, invite);
    await trackEvent(inviterId, "invite_sent", {
      project_id: projectId,
      invite_id: invite.id,
      channel: "email",
    });
    results.push({ email, status: "sent", invite_id: invite.id });
  }

  return results;
}
```

## Onboarding Optimization

### Onboarding Checklist Pattern

```typescript
interface OnboardingStep {
  id: string;
  title: string;
  description: string;
  action_type: "auto" | "user_action" | "integration";
  completion_event: string;
  required: boolean;
  order: number;
  estimated_minutes: number;
  help_url?: string;
}

const onboardingSteps: OnboardingStep[] = [
  {
    id: "profile",
    title: "Profilini tamamla",
    description: "Adini ve rol bilgini ekle",
    action_type: "user_action",
    completion_event: "profile_completed",
    required: true,
    order: 1,
    estimated_minutes: 1,
  },
  {
    id: "first_project",
    title: "Ilk projeyi olustur",
    description: "Bir proje olusturup calismaya basla",
    action_type: "user_action",
    completion_event: "project_created",
    required: true,
    order: 2,
    estimated_minutes: 2,
  },
  {
    id: "invite_team",
    title: "Takimini davet et",
    description: "En az 1 takim arkadasi ekle",
    action_type: "user_action",
    completion_event: "team_member_invited",
    required: false,
    order: 3,
    estimated_minutes: 2,
  },
  {
    id: "integration",
    title: "Entegrasyon bagla",
    description: "GitHub, Slack veya Jira bagla",
    action_type: "integration",
    completion_event: "integration_connected",
    required: false,
    order: 4,
    estimated_minutes: 3,
  },
];

// Onboarding progress tracker
async function getOnboardingProgress(userId: string): Promise<{
  completed: string[];
  remaining: OnboardingStep[];
  percentage: number;
  nextStep: OnboardingStep | null;
}> {
  const completedEvents = await getUserEvents(userId, onboardingSteps.map(s => s.completion_event));
  const completed = onboardingSteps
    .filter(s => completedEvents.includes(s.completion_event))
    .map(s => s.id);
  const remaining = onboardingSteps.filter(s => !completed.includes(s.id));

  return {
    completed,
    remaining,
    percentage: Math.round((completed.length / onboardingSteps.length) * 100),
    nextStep: remaining[0] || null,
  };
}
```

### Onboarding Metrics

| Metrik | Formul | Hedef |
|--------|--------|-------|
| Completion Rate | completed_all_steps / started_onboarding | > %60 |
| Time to Complete | median(onboarding_end - signup) | < 10 dakika |
| Drop-off Point | En cok terk edilen adim | Her adim > %80 |
| Activation Rate | aha_moment_reached / signed_up | > %40 |
| Time to Value | signup -> first_value_event | < 5 dakika |

### Progressive Onboarding

```typescript
// Engagement-based onboarding (her seyi birden gosterme)
interface OnboardingTrigger {
  feature: string;
  show_after: string;           // event sonrasi goster
  delay_seconds: number;
  tooltip_position: "top" | "bottom" | "left" | "right";
  message: string;
  dismiss_event: string;
}

const progressiveHints: OnboardingTrigger[] = [
  {
    feature: "keyboard_shortcuts",
    show_after: "third_task_created",
    delay_seconds: 2,
    tooltip_position: "bottom",
    message: "Pro tip: Ctrl+K ile hizli komut menusunu acabilirsin",
    dismiss_event: "shortcut_hint_dismissed",
  },
  {
    feature: "automation",
    show_after: "tenth_task_completed",
    delay_seconds: 5,
    tooltip_position: "right",
    message: "Bu tekrarlayan gorevi otomatiklestirmek ister misin?",
    dismiss_event: "automation_hint_dismissed",
  },
];
```

## Activation Metrics

### Activation Funnel

```
Signup --> Setup --> Aha Moment --> Habit
  |         |          |            |
  v         v          v            v
100%      ~70%       ~40%         ~20%
```

### Activation Definition Framework

```typescript
interface ActivationCriteria {
  name: string;
  events: Array<{
    event: string;
    count: number;             // minimum kac kez
    within_days: number;       // kac gun icinde
  }>;
  logic: "AND" | "OR";        // tum kriterler mi, herhangi biri mi
}

const activationDefinitions: ActivationCriteria[] = [
  {
    name: "basic_activation",
    events: [
      { event: "project_created", count: 1, within_days: 3 },
      { event: "task_created", count: 3, within_days: 7 },
    ],
    logic: "AND",
  },
  {
    name: "team_activation",
    events: [
      { event: "team_member_invited", count: 1, within_days: 7 },
      { event: "collaborative_action", count: 5, within_days: 14 },
    ],
    logic: "AND",
  },
];

// Hangi activation definition en iyi retention ile korelasyon gosteriyor?
// -> A/B test et, D30 retention ile karsilastir
```

## Freemium Model Design

### Freemium Strategies

| Strateji | Sinir Tipi | Ornek |
|----------|-----------|-------|
| Feature-limited | Bazi ozellikler locked | Slack (mesaj gecmisi), GitHub (private repo) |
| Usage-limited | Kullanim siniri | Dropbox (2GB), Vercel (100GB bandwidth) |
| Seat-limited | Kullanici sayisi | Notion (10 guest), Linear (10 members) |
| Time-limited (trial) | Sure siniri | 14 gun full access |
| Support-limited | Destek seviyesi | Community vs Priority support |

### Pricing Page Optimization

```typescript
interface PricingExperiment {
  name: string;
  hypothesis: string;
  variants: Array<{
    id: string;
    change: string;
    expected_impact: string;
  }>;
  primary_metric: string;
}

const pricingExperiments: PricingExperiment[] = [
  {
    name: "anchor_pricing",
    hypothesis: "Enterprise plani one koymak, Pro plan conversion'i %15 arttirir",
    variants: [
      { id: "control", change: "Free -> Pro -> Enterprise", expected_impact: "baseline" },
      { id: "treatment", change: "Enterprise -> Pro -> Free (reverse)", expected_impact: "+15% Pro conversion" },
    ],
    primary_metric: "plan_upgrade_rate",
  },
  {
    name: "annual_discount",
    hypothesis: "%20 yerine 2 ay bedava demek, annual conversion'i %10 arttirir",
    variants: [
      { id: "control", change: "Save 20%", expected_impact: "baseline" },
      { id: "treatment", change: "2 months free", expected_impact: "+10% annual" },
    ],
    primary_metric: "annual_plan_rate",
  },
];
```

## Growth Experiments Framework

### Experiment Lifecycle

```
Idea -> Prioritize (ICE) -> Design -> Implement -> Run -> Analyze -> Learn
```

### ICE Scoring

```typescript
interface GrowthExperiment {
  id: string;
  name: string;
  hypothesis: string;
  impact: number;              // 1-10: basarili olursa ne kadar etki
  confidence: number;          // 1-10: basarili olma ihtimali
  ease: number;                // 1-10: ne kadar kolay implement
  ice_score: number;           // (impact + confidence + ease) / 3
  primary_metric: string;
  status: "backlog" | "designing" | "running" | "analyzing" | "completed";
  results?: ExperimentResult;
}

function prioritizeExperiments(experiments: GrowthExperiment[]): GrowthExperiment[] {
  return experiments
    .map(e => ({
      ...e,
      ice_score: (e.impact + e.confidence + e.ease) / 3,
    }))
    .sort((a, b) => b.ice_score - a.ice_score);
}
```

### Experiment Tracking Template

```typescript
interface ExperimentResult {
  experiment_id: string;
  start_date: string;
  end_date: string;
  sample_size: { control: number; treatment: number };
  primary_metric: {
    control_value: number;
    treatment_value: number;
    lift: number;                        // %
    p_value: number;
    significant: boolean;
  };
  secondary_metrics: Array<{
    name: string;
    lift: number;
    significant: boolean;
  }>;
  decision: "ship" | "iterate" | "kill";
  learnings: string[];
}
```

## Notification Strategies

### Notification Framework

```typescript
interface NotificationConfig {
  type: "push" | "email" | "in_app" | "sms";
  trigger: string;                       // event name
  template: string;
  delay_minutes: number;
  frequency_cap: {
    max_per_day: number;
    max_per_week: number;
  };
  segment: string;                       // user segment
  priority: "critical" | "high" | "medium" | "low";
}

const notificationSchedule: NotificationConfig[] = [
  // Onboarding sequence
  {
    type: "email",
    trigger: "user_signed_up",
    template: "welcome_email",
    delay_minutes: 0,
    frequency_cap: { max_per_day: 1, max_per_week: 3 },
    segment: "new_users",
    priority: "high",
  },
  {
    type: "email",
    trigger: "onboarding_incomplete_24h",
    template: "complete_setup_nudge",
    delay_minutes: 24 * 60,
    frequency_cap: { max_per_day: 1, max_per_week: 2 },
    segment: "incomplete_onboarding",
    priority: "medium",
  },
  // Re-engagement
  {
    type: "email",
    trigger: "inactive_7_days",
    template: "we_miss_you",
    delay_minutes: 0,
    frequency_cap: { max_per_day: 1, max_per_week: 1 },
    segment: "churning",
    priority: "medium",
  },
  // Expansion
  {
    type: "in_app",
    trigger: "usage_limit_80_percent",
    template: "upgrade_nudge",
    delay_minutes: 0,
    frequency_cap: { max_per_day: 1, max_per_week: 2 },
    segment: "high_usage_free",
    priority: "high",
  },
];
```

## User Engagement Hooks

### Engagement Loop Patterns

| Pattern | Mekanizma | Ornek |
|---------|-----------|-------|
| Variable Reward | Beklenmedik oduller | LinkedIn: "X viewed your profile" |
| Investment | Kullanici emek harcayor | Pinterest: pin boards |
| Social Proof | Baskalari kullaniyor | "1000+ team already uses..." |
| Progress | Ilerleme gosterimi | Duolingo streak |
| Commitment | Kucuk adimlar -> buyuk adimlar | Free trial -> paid |
| Loss Aversion | Kaybetme korkusu | "Your streak will reset!" |
| FOMO | Kacirma korkusu | "Limited time offer" |

### Streak System

```typescript
interface StreakConfig {
  activity_event: string;
  period: "daily" | "weekly";
  milestones: Array<{
    days: number;
    reward: string;
    badge?: string;
  }>;
  grace_period_hours: number;     // streak kurtarma suresi
  freeze_available: boolean;       // streak dondurma hakki
}

const streakConfig: StreakConfig = {
  activity_event: "daily_active",
  period: "daily",
  milestones: [
    { days: 3, reward: "Nice start!", badge: "streak_3" },
    { days: 7, reward: "1 week streak!", badge: "streak_7" },
    { days: 30, reward: "Monthly warrior!", badge: "streak_30" },
    { days: 100, reward: "Centurion!", badge: "streak_100" },
  ],
  grace_period_hours: 12,
  freeze_available: true,
};
```

## Anti-Patterns

| Anti-Pattern | Dogru Yol |
|-------------|-----------|
| Feature gating cok agresif | Deger gorsun, sonra gate koy |
| Spam notification | Frequency cap + unsubscribe kolay |
| Karisik onboarding | Max 5 adim, progressive disclosure |
| Referral odulunu geciktirmek | Aninda ver, sonra qualify et |
| K-Factor'u ignore etmek | Her feature'da viral loop dusun |
| Tek seferlik onboarding | Devam eden egitim (progressive) |
| Agresif upgrade prompt | Deger gordukleri anda goster |
| Tum kullanicilara ayni deneyim | Segment-based kisiselllestirme |
