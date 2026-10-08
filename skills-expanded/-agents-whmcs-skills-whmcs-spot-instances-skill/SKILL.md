---
name: whmcs-spot-instances
description: Spot instance handling for WHMCS cloud services
category: Provisioning & Cloud
version: 1.0.0
---

# WHMCS Spot Instance Handling Skill

## Overview
This skill provides patterns and implementations for managing spot instances in WHMCS, including bidding strategies, interruption handling, fallback mechanisms, and cost optimization.

## Implementation Patterns

### Spot Instance Manager
```php
<?php
/**
 * WHMCS Spot Instance Management
 * Handles spot/preemptible instance lifecycle
 */

namespace WHMCS\Module\Server\Spot;

class SpotInstanceManager {
    private $db;
    private $biddingEngine;
    private $interruptionHandler;

    public function __construct() {
        $this->db = \WHMCS\Database\Capsule::connection();
        $this->biddingEngine = new BiddingEngine();
        $this->interruptionHandler = new InterruptionHandler();
    }

    /**
     * Launch spot instance
     */
    public function launchSpot(array $params): array {
        $spotId = 'spot_' . bin2hex(random_bytes(12));

        $spotInstance = [
            'id' => $spotId,
            'service_id' => $params['service_id'] ?? null,
            'customer_id' => $params['customer_id'],
            'instance_type' => $params['instance_type'],
            'quantity' => $params['quantity'] ?? 1,
            'region' => $params['region'] ?? 'default',
            'max_bid_price' => $params['max_bid_price'],
            'bidding_strategy' => $params['strategy'] ?? 'optimal',
            'fallback_to_ondemand' => $params['fallback'] ?? true,
            'interrupt_grace_period' => $params['grace_period'] ?? 120,
            'status' => 'requesting',
            'created_at' => date('Y-m-d H:i:s')
        ];

        $this->db->insert('mod_spot_instances', $spotInstance);

        // Submit spot request to cloud provider
        $requestResult = $this->submitSpotRequest($spotInstance);

        if ($requestResult['success']) {
            $this->db->update('mod_spot_instances', [
                'request_id' => $requestResult['request_id'],
                'status' => 'open'
            ], ['id' => $spotId]);
        }

        return [
            'success' => true,
            'spot_id' => $spotId,
            'request_id' => $requestResult['request_id'] ?? null
        ];
    }

    /**
     * Get spot request status
     */
    public function getRequestStatus(string $spotId): array {
        $spot = $this->getSpotInstance($spotId);

        if (!$spot) {
            throw new \Exception("Spot instance not found: {$spotId}");
        }

        // Check with cloud provider
        $cloudStatus = $this->checkCloudRequestStatus($spot['request_id']);

        return [
            'spot_id' => $spotId,
            'request_id' => $spot['request_id'],
            'status' => $cloudStatus['status'],
            'current_price' => $cloudStatus['current_price'],
            'fulfilled_instances' => $cloudStatus['fulfilled'],
            'interruption_count' => $spot['interruption_count']
        ];
    }

    /**
     * Handle spot interruption
     */
    public function handleInterruption(array $interruptionData): array {
        $spotId = $interruptionData['spot_id'];
        $spot = $this->getSpotInstance($spotId);

        if (!$spot) {
            throw new \Exception("Spot instance not found: {$spotId}");
        }

        // Record interruption
        $this->db->insert('mod_spot_interruptions', [
            'spot_id' => $spotId,
            'instance_id' => $interruptionData['instance_id'],
            'interruption_time' => date('Y-m-d H:i:s'),
            'reason' => $interruptionData['reason'] ?? 'price_exceeded',
            'notice_received_at' => $interruptionData['notice_time'] ?? date('Y-m-d H:i:s')
        ]);

        // Update interruption count
        $this->db->update('mod_spot_instances', [
            'interruption_count' => $spot['interruption_count'] + 1
        ], ['id' => $spotId]);

        // Execute graceful shutdown
        $this->interruptionHandler->executeGracefulShutdown($spotId);

        // Check for fallback
        if ($spot['fallback_to_ondemand']) {
            $this->launchFallbackInstance($spotId);
        }

        return [
            'success' => true,
            'spot_id' => $spotId,
            'handled' => true,
            'fallback_launched' => $spot['fallback_to_ondemand']
        ];
    }

    /**
     * Calculate optimal bid price
     */
    public function calculateOptimalBid(string $instanceType, string $region): array {
        return $this->biddingEngine->calculateOptimalBid($instanceType, $region);
    }

    /**
     * Set up interruption monitoring
     */
    public function setupInterruptionMonitoring(string $spotId): array {
        $spot = $this->getSpotInstance($spotId);

        if (!$spot) {
            throw new \Exception("Spot instance not found: {$spotId}");
        }

        // Create scheduled task to check for interruptions
        $monitorConfig = [
            'spot_id' => $spotId,
            'check_interval' => 60,
            'grace_period' => $spot['interrupt_grace_period'],
            'notification_enabled' => true
        ];

        $this->db->update('mod_spot_instances', [
            'monitoring_config' => json_encode($monitorConfig)
        ], ['id' => $spotId]);

        return [
            'success' => true,
            'spot_id' => $spotId,
            'monitoring_enabled' => true
        ];
    }

    /**
     * List spot instances
     */
    public function listSpotInstances(array $filters = []): array {
        $query = "SELECT s.*, c.companyname as customer_name
                  FROM mod_spot_instances s
                  LEFT JOIN tblclients c ON s.customer_id = c.id
                  WHERE 1=1";

        $bindings = [];

        if (!empty($filters['status'])) {
            $query .= " AND s.status = ?";
            $bindings[] = $filters['status'];
        }

        if (!empty($filters['customer_id'])) {
            $query .= " AND s.customer_id = ?";
            $bindings[] = $filters['customer_id'];
        }

        $query .= " ORDER BY s.created_at DESC";

        $instances = $this->db->select($query, $bindings);

        return array_map(function($instance) {
            return [
                'id' => $instance->id,
                'customer_name' => $instance->customer_name,
                'instance_type' => $instance->instance_type,
                'status' => $instance->status,
                'max_bid_price' => $instance->max_bid_price,
                'interruption_count' => $instance->interruption_count,
                'created_at' => $instance->created_at
            ];
        }, $instances);
    }

    /**
     * Get savings report for spot usage
     */
    public function getSavingsReport(int $customerId, \DateTime $from, \DateTime $to): array {
        $spotUsage = $this->db->select(
            "SELECT SUM(uptime_hours) as total_hours,
                    SUM(on_demand_cost) as on_demand_cost,
                    SUM(spot_cost) as spot_cost
             FROM mod_spot_instances
             WHERE customer_id = ? AND created_at BETWEEN ? AND ?",
            [$customerId, $from->format('Y-m-d'), $to->format('Y-m-d')]
        )[0];

        $savings = $spotUsage->on_demand_cost - $spotUsage->spot_cost;
        $savingsPercent = $spotUsage->on_demand_cost > 0 ?
            ($savings / $spotUsage->on_demand_cost) * 100 : 0;

        return [
            'customer_id' => $customerId,
            'period' => ['from' => $from->format('Y-m-d'), 'to' => $to->format('Y-m-d')],
            'total_hours' => $spotUsage->total_hours,
            'on_demand_cost' => $spotUsage->on_demand_cost,
            'spot_cost' => $spotUsage->spot_cost,
            'total_savings' => $savings,
            'savings_percent' => round($savingsPercent, 2)
        ];
    }

    // Private helper methods

    private function submitSpotRequest(array $spotInstance): array {
        // Submit to cloud provider (AWS, GCP, Azure, etc.)
        // This is provider-specific implementation
        return ['success' => true, 'request_id' => 'spot-req-' . bin2hex(random_bytes(12))];
    }

    private function launchFallbackInstance(string $spotId): void {
        $spot = $this->getSpotInstance($spotId);

        // Launch on-demand instance as fallback
        $onDemandId = 'od_' . bin2hex(random_bytes(12));

        $this->db->insert('mod_ondemand_instances', [
            'id' => $onDemandId,
            'original_spot_id' => $spotId,
            'instance_type' => $spot['instance_type'],
            'region' => $spot['region'],
            'status' => 'launching'
        ]);

        // Trigger on-demand launch
    }
}

/**
 * Bidding Engine for Spot Instances
 */
class BiddingEngine {
    private $db;

    public function __construct() {
        $this->db = \WHMCS\Database\Capsule::connection();
    }

    public function calculateOptimalBid(string $instanceType, string $region): array {
        // Get historical prices
        $historicalPrices = $this->getHistoricalPrices($instanceType, $region);

        // Calculate statistics
        $avgPrice = array_sum($historicalPrices) / count($historicalPrices);
        $maxPrice = max($historicalPrices);
        $percentile70 = $this->calculatePercentile($historicalPrices, 70);
        $percentile90 = $this->calculatePercentile($historicalPrices, 90);

        // Determine optimal bid based on strategy
        $bidPrice = match($this->getStrategy()) {
            'low_cost' => $avgPrice * 0.8,
            'reliable' => $percentile70,
            'critical' => $percentile90,
            'optimal' => $avgPrice * 0.95,
            default => $avgPrice
        };

        return [
            'instance_type' => $instanceType,
            'region' => $region,
            'avg_price' => round($avgPrice, 4),
            'recommended_bid' => round($bidPrice, 4),
            'max_recommended' => round($maxPrice * 0.9, 4),
            'reliability_score' => $this->calculateReliabilityScore($historicalPrices)
        ];
    }

    private function getHistoricalPrices(string $instanceType, string $region): array {
        $prices = $this->db->select(
            "SELECT spot_price FROM mod_spot_price_history
             WHERE instance_type = ? AND region = ?
             AND recorded_at > DATE_SUB(NOW(), INTERVAL 30 DAY)
             ORDER BY recorded_at ASC",
            [$instanceType, $region]
        );

        return array_map(fn($p) => $p->spot_price, $prices);
    }

    private function calculatePercentile(array $values, int $percentile): float {
        sort($values);
        $index = ($percentile / 100) * (count($values) - 1);
        $floor = floor($index);
        $ceil = ceil($index);

        if ($floor == $ceil) {
            return $values[$floor];
        }

        return $values[$floor] * ($ceil - $index) + $values[$ceil] * ($index - $floor);
    }

    private function calculateReliabilityScore(array $prices): float {
        $interruptedHours = count(array_filter($prices, fn($p) => $p > 0.5));
        return round(100 - ($interruptedHours / count($prices)) * 100, 2);
    }
}

/**
 * Interruption Handler
 */
class InterruptionHandler {
    public function executeGracefulShutdown(string $spotId): void {
        $spot = $this->getSpotInstance($spotId);

        // Send SIGTERM to running processes
        $this->sendShutdownSignal($spot['instance_id']);

        // Wait for grace period
        sleep($spot['interrupt_grace_period']);

        // Create checkpoint if applicable
        $this->createCheckpoint($spotId);

        // Stop instance
        $this->stopInstance($spot['instance_id']);

        // Update status
        $this->db->update('mod_spot_instances', [
            'status' => 'interrupted',
            'last_interruption_at' => date('Y-m-d H:i:s')
        ], ['id' => $spotId]);
    }

    public function notifyCustomer(string $spotId): void {
        $spot = $this->getSpotInstance($spotId);

        // Send notification via WHMCS
        send_email($spot['customer_id'], 'spot-interruption', [
            'instance_type' => $spot['instance_type'],
            'interruption_time' => date('Y-m-d H:i:s')
        ]);
    }
}
```

## Database Schema
```sql
CREATE TABLE `mod_spot_instances` (
  `id` VARCHAR(50) PRIMARY KEY,
  `service_id` INT,
  `customer_id` INT NOT NULL,
  `request_id` VARCHAR(100),
  `instance_type` VARCHAR(100) NOT NULL,
  `quantity` INT DEFAULT 1,
  `region` VARCHAR(50) DEFAULT 'default',
  `max_bid_price` DECIMAL(10,4) NOT NULL,
  `bidding_strategy` VARCHAR(50) DEFAULT 'optimal',
  `fallback_to_ondemand` TINYINT(1) DEFAULT 1,
  `interrupt_grace_period` INT DEFAULT 120,
  `monitoring_config` TEXT,
  `status` ENUM('requesting', 'open', 'active', 'interrupted', 'cancelled', 'closed') DEFAULT 'requesting',
  `interruption_count` INT DEFAULT 0,
  `uptime_hours` DECIMAL(10,2) DEFAULT 0,
  `on_demand_cost` DECIMAL(10,2) DEFAULT 0,
  `spot_cost` DECIMAL(10,2) DEFAULT 0,
  `last_interruption_at` DATETIME,
  `created_at` DATETIME NOT NULL
);

CREATE TABLE `mod_spot_interruptions` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `spot_id` VARCHAR(50) NOT NULL,
  `instance_id` VARCHAR(100),
  `interruption_time` DATETIME NOT NULL,
  `reason` VARCHAR(100),
  `notice_received_at` DATETIME,
  FOREIGN KEY (`spot_id`) REFERENCES `mod_spot_instances`(`id`)
);

CREATE TABLE `mod_spot_price_history` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `instance_type` VARCHAR(100) NOT NULL,
  `region` VARCHAR(50) NOT NULL,
  `spot_price` DECIMAL(10,6) NOT NULL,
  `on_demand_price` DECIMAL(10,6) NOT NULL,
  `recorded_at` DATETIME NOT NULL,
  INDEX `idx_instance_region` (`instance_type`, `region`)
);
```

## Bidding Strategies

| Strategy | Bid % of On-Demand | Reliability | Best For |
|----------|-------------------|-------------|----------|
| Low Cost | 60-70% | Medium | Batch processing |
| Optimal | 90-95% | High | General workloads |
| Reliable | 70-80% | Very High | Production apps |
| Critical | 100%+ | Highest | Mission critical |

## Best Practices

1. **Graceful Handling**: Implement proper shutdown procedures
2. **Cost Monitoring**: Track savings vs on-demand
3. **Fallback Plans**: Always have on-demand fallback
4. **Bid Strategy**: Use historical data for optimal bidding
5. **Interruption Recovery**: Implement checkpoint mechanisms

## Related Skills

- whmcs-reserved-instances
- whmcs-cost-tracking
- whmcs-auto-scaling
- whmcs-billing-dimensions