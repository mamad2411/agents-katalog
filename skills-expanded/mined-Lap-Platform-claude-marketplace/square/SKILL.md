---
name: square
description: "Square API skill. Use when working with Square for mobile, oauth2, {location_id}. Covers 327 endpoints."
version: 1.0.0
generator: lapsh
---

# Square
API version: 2.0

## Auth
OAuth2 | ApiKey Authorization in header

## Base URL
https://connect.squareup.com

## Setup
1. Set your API key in the appropriate header
2. GET /v2/bank-accounts -- verify access
3. POST /mobile/authorization-code -- create first authorization-code

## Endpoints

327 endpoints across 34 groups. See references/api-spec.lap for full details.

### mobile
| Method | Path | Description |
|--------|------|-------------|
| POST | /mobile/authorization-code | CreateMobileAuthorizationCode |

### oauth2
| Method | Path | Description |
|--------|------|-------------|
| POST | /oauth2/revoke | RevokeToken |
| POST | /oauth2/token | ObtainToken |
| POST | /oauth2/token/status | RetrieveTokenStatus |

### {location_id}
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/{location_id}/orders | V1ListOrders |
| GET | /v1/{location_id}/orders/{order_id} | V1RetrieveOrder |
| PUT | /v1/{location_id}/orders/{order_id} | V1UpdateOrder |

### apple-pay
| Method | Path | Description |
|--------|------|-------------|
| POST | /v2/apple-pay/domains | RegisterDomain |

### bank-accounts
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/bank-accounts | ListBankAccounts |
| GET | /v2/bank-accounts/by-v1-id/{v1_bank_account_id} | GetBankAccountByV1Id |
| GET | /v2/bank-accounts/{bank_account_id} | GetBankAccount |

### bookings
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/bookings | ListBookings |
| POST | /v2/bookings | CreateBooking |
| POST | /v2/bookings/availability/search | SearchAvailability |
| POST | /v2/bookings/bulk-retrieve | BulkRetrieveBookings |
| GET | /v2/bookings/business-booking-profile | RetrieveBusinessBookingProfile |
| GET | /v2/bookings/custom-attribute-definitions | ListBookingCustomAttributeDefinitions |
| POST | /v2/bookings/custom-attribute-definitions | CreateBookingCustomAttributeDefinition |
| DELETE | /v2/bookings/custom-attribute-definitions/{key} | DeleteBookingCustomAttributeDefinition |
| GET | /v2/bookings/custom-attribute-definitions/{key} | RetrieveBookingCustomAttributeDefinition |
| PUT | /v2/bookings/custom-attribute-definitions/{key} | UpdateBookingCustomAttributeDefinition |
| POST | /v2/bookings/custom-attributes/bulk-delete | BulkDeleteBookingCustomAttributes |
| POST | /v2/bookings/custom-attributes/bulk-upsert | BulkUpsertBookingCustomAttributes |
| GET | /v2/bookings/location-booking-profiles | ListLocationBookingProfiles |
| GET | /v2/bookings/location-booking-profiles/{location_id} | RetrieveLocationBookingProfile |
| GET | /v2/bookings/team-member-booking-profiles | ListTeamMemberBookingProfiles |
| POST | /v2/bookings/team-member-booking-profiles/bulk-retrieve | BulkRetrieveTeamMemberBookingProfiles |
| GET | /v2/bookings/team-member-booking-profiles/{team_member_id} | RetrieveTeamMemberBookingProfile |
| GET | /v2/bookings/{booking_id} | RetrieveBooking |
| PUT | /v2/bookings/{booking_id} | UpdateBooking |
| POST | /v2/bookings/{booking_id}/cancel | CancelBooking |
| GET | /v2/bookings/{booking_id}/custom-attributes | ListBookingCustomAttributes |
| DELETE | /v2/bookings/{booking_id}/custom-attributes/{key} | DeleteBookingCustomAttribute |
| GET | /v2/bookings/{booking_id}/custom-attributes/{key} | RetrieveBookingCustomAttribute |
| PUT | /v2/bookings/{booking_id}/custom-attributes/{key} | UpsertBookingCustomAttribute |

### cards
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/cards | ListCards |
| POST | /v2/cards | CreateCard |
| GET | /v2/cards/{card_id} | RetrieveCard |
| POST | /v2/cards/{card_id}/disable | DisableCard |

### cash-drawers
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/cash-drawers/shifts | ListCashDrawerShifts |
| GET | /v2/cash-drawers/shifts/{shift_id} | RetrieveCashDrawerShift |
| GET | /v2/cash-drawers/shifts/{shift_id}/events | ListCashDrawerShiftEvents |

### catalog
| Method | Path | Description |
|--------|------|-------------|
| POST | /v2/catalog/batch-delete | BatchDeleteCatalogObjects |
| POST | /v2/catalog/batch-retrieve | BatchRetrieveCatalogObjects |
| POST | /v2/catalog/batch-upsert | BatchUpsertCatalogObjects |
| POST | /v2/catalog/images | CreateCatalogImage |
| PUT | /v2/catalog/images/{image_id} | UpdateCatalogImage |
| GET | /v2/catalog/info | CatalogInfo |
| GET | /v2/catalog/list | ListCatalog |
| POST | /v2/catalog/object | UpsertCatalogObject |
| DELETE | /v2/catalog/object/{object_id} | DeleteCatalogObject |
| GET | /v2/catalog/object/{object_id} | RetrieveCatalogObject |
| POST | /v2/catalog/search | SearchCatalogObjects |
| POST | /v2/catalog/search-catalog-items | SearchCatalogItems |
| POST | /v2/catalog/update-item-modifier-lists | UpdateItemModifierLists |
| POST | /v2/catalog/update-item-taxes | UpdateItemTaxes |

### channels
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/channels | ListChannels |
| POST | /v2/channels/bulk-retrieve | BulkRetrieveChannels |
| GET | /v2/channels/{channel_id} | RetrieveChannel |

### customers
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/customers | ListCustomers |
| POST | /v2/customers | CreateCustomer |
| POST | /v2/customers/bulk-create | BulkCreateCustomers |
| POST | /v2/customers/bulk-delete | BulkDeleteCustomers |
| POST | /v2/customers/bulk-retrieve | BulkRetrieveCustomers |
| POST | /v2/customers/bulk-update | BulkUpdateCustomers |
| GET | /v2/customers/custom-attribute-definitions | ListCustomerCustomAttributeDefinitions |
| POST | /v2/customers/custom-attribute-definitions | CreateCustomerCustomAttributeDefinition |
| DELETE | /v2/customers/custom-attribute-definitions/{key} | DeleteCustomerCustomAttributeDefinition |
| GET | /v2/customers/custom-attribute-definitions/{key} | RetrieveCustomerCustomAttributeDefinition |
| PUT | /v2/customers/custom-attribute-definitions/{key} | UpdateCustomerCustomAttributeDefinition |
| POST | /v2/customers/custom-attributes/bulk-upsert | BulkUpsertCustomerCustomAttributes |
| GET | /v2/customers/groups | ListCustomerGroups |
| POST | /v2/customers/groups | CreateCustomerGroup |
| DELETE | /v2/customers/groups/{group_id} | DeleteCustomerGroup |
| GET | /v2/customers/groups/{group_id} | RetrieveCustomerGroup |
| PUT | /v2/customers/groups/{group_id} | UpdateCustomerGroup |
| POST | /v2/customers/search | SearchCustomers |
| GET | /v2/customers/segments | ListCustomerSegments |
| GET | /v2/customers/segments/{segment_id} | RetrieveCustomerSegment |
| DELETE | /v2/customers/{customer_id} | DeleteCustomer |
| GET | /v2/customers/{customer_id} | RetrieveCustomer |
| PUT | /v2/customers/{customer_id} | UpdateCustomer |
| POST | /v2/customers/{customer_id}/cards | CreateCustomerCard |
| DELETE | /v2/customers/{customer_id}/cards/{card_id} | DeleteCustomerCard |
| GET | /v2/customers/{customer_id}/custom-attributes | ListCustomerCustomAttributes |
| DELETE | /v2/customers/{customer_id}/custom-attributes/{key} | DeleteCustomerCustomAttribute |
| GET | /v2/customers/{customer_id}/custom-attributes/{key} | RetrieveCustomerCustomAttribute |
| POST | /v2/customers/{customer_id}/custom-attributes/{key} | UpsertCustomerCustomAttribute |
| DELETE | /v2/customers/{customer_id}/groups/{group_id} | RemoveGroupFromCustomer |
| PUT | /v2/customers/{customer_id}/groups/{group_id} | AddGroupToCustomer |

### devices
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/devices | ListDevices |
| GET | /v2/devices/codes | ListDeviceCodes |
| POST | /v2/devices/codes | CreateDeviceCode |
| GET | /v2/devices/codes/{id} | GetDeviceCode |
| GET | /v2/devices/{device_id} | GetDevice |

### disputes
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/disputes | ListDisputes |
| GET | /v2/disputes/{dispute_id} | RetrieveDispute |
| POST | /v2/disputes/{dispute_id}/accept | AcceptDispute |
| GET | /v2/disputes/{dispute_id}/evidence | ListDisputeEvidence |
| POST | /v2/disputes/{dispute_id}/evidence-files | CreateDisputeEvidenceFile |
| POST | /v2/disputes/{dispute_id}/evidence-text | CreateDisputeEvidenceText |
| DELETE | /v2/disputes/{dispute_id}/evidence/{evidence_id} | DeleteDisputeEvidence |
| GET | /v2/disputes/{dispute_id}/evidence/{evidence_id} | RetrieveDisputeEvidence |
| POST | /v2/disputes/{dispute_id}/submit-evidence | SubmitEvidence |

### employees
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/employees | ListEmployees |
| GET | /v2/employees/{id} | RetrieveEmployee |

### events
| Method | Path | Description |
|--------|------|-------------|
| POST | /v2/events | SearchEvents |
| PUT | /v2/events/disable | DisableEvents |
| PUT | /v2/events/enable | EnableEvents |
| GET | /v2/events/types | ListEventTypes |

### gift-cards
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/gift-cards | ListGiftCards |
| POST | /v2/gift-cards | CreateGiftCard |
| GET | /v2/gift-cards/activities | ListGiftCardActivities |
| POST | /v2/gift-cards/activities | CreateGiftCardActivity |
| POST | /v2/gift-cards/from-gan | RetrieveGiftCardFromGAN |
| POST | /v2/gift-cards/from-nonce | RetrieveGiftCardFromNonce |
| POST | /v2/gift-cards/{gift_card_id}/link-customer | LinkCustomerToGiftCard |
| POST | /v2/gift-cards/{gift_card_id}/unlink-customer | UnlinkCustomerFromGiftCard |
| GET | /v2/gift-cards/{id} | RetrieveGiftCard |

### inventory
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/inventory/adjustment/{adjustment_id} | DeprecatedRetrieveInventoryAdjustment |
| GET | /v2/inventory/adjustments/{adjustment_id} | RetrieveInventoryAdjustment |
| POST | /v2/inventory/batch-change | DeprecatedBatchChangeInventory |
| POST | /v2/inventory/batch-retrieve-changes | DeprecatedBatchRetrieveInventoryChanges |
| POST | /v2/inventory/batch-retrieve-counts | DeprecatedBatchRetrieveInventoryCounts |
| POST | /v2/inventory/changes/batch-create | BatchChangeInventory |
| POST | /v2/inventory/changes/batch-retrieve | BatchRetrieveInventoryChanges |
| POST | /v2/inventory/counts/batch-retrieve | BatchRetrieveInventoryCounts |
| GET | /v2/inventory/physical-count/{physical_count_id} | DeprecatedRetrieveInventoryPhysicalCount |
| GET | /v2/inventory/physical-counts/{physical_count_id} | RetrieveInventoryPhysicalCount |
| GET | /v2/inventory/transfers/{transfer_id} | RetrieveInventoryTransfer |
| GET | /v2/inventory/{catalog_object_id} | RetrieveInventoryCount |
| GET | /v2/inventory/{catalog_object_id}/changes | RetrieveInventoryChanges |

### invoices
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/invoices | ListInvoices |
| POST | /v2/invoices | CreateInvoice |
| POST | /v2/invoices/search | SearchInvoices |
| DELETE | /v2/invoices/{invoice_id} | DeleteInvoice |
| GET | /v2/invoices/{invoice_id} | GetInvoice |
| PUT | /v2/invoices/{invoice_id} | UpdateInvoice |
| POST | /v2/invoices/{invoice_id}/attachments | CreateInvoiceAttachment |
| DELETE | /v2/invoices/{invoice_id}/attachments/{attachment_id} | DeleteInvoiceAttachment |
| POST | /v2/invoices/{invoice_id}/cancel | CancelInvoice |
| POST | /v2/invoices/{invoice_id}/publish | PublishInvoice |

### labor
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/labor/break-types | ListBreakTypes |
| POST | /v2/labor/break-types | CreateBreakType |
| DELETE | /v2/labor/break-types/{id} | DeleteBreakType |
| GET | /v2/labor/break-types/{id} | GetBreakType |
| PUT | /v2/labor/break-types/{id} | UpdateBreakType |
| GET | /v2/labor/employee-wages | ListEmployeeWages |
| GET | /v2/labor/employee-wages/{id} | GetEmployeeWage |
| POST | /v2/labor/scheduled-shifts | CreateScheduledShift |
| POST | /v2/labor/scheduled-shifts/bulk-publish | BulkPublishScheduledShifts |
| POST | /v2/labor/scheduled-shifts/search | SearchScheduledShifts |
| GET | /v2/labor/scheduled-shifts/{id} | RetrieveScheduledShift |
| PUT | /v2/labor/scheduled-shifts/{id} | UpdateScheduledShift |
| POST | /v2/labor/scheduled-shifts/{id}/publish | PublishScheduledShift |
| POST | /v2/labor/shifts | CreateShift |
| POST | /v2/labor/shifts/search | SearchShifts |
| DELETE | /v2/labor/shifts/{id} | DeleteShift |
| GET | /v2/labor/shifts/{id} | GetShift |
| PUT | /v2/labor/shifts/{id} | UpdateShift |
| GET | /v2/labor/team-member-wages | ListTeamMemberWages |
| GET | /v2/labor/team-member-wages/{id} | GetTeamMemberWage |
| POST | /v2/labor/timecards | CreateTimecard |
| POST | /v2/labor/timecards/search | SearchTimecards |
| DELETE | /v2/labor/timecards/{id} | DeleteTimecard |
| GET | /v2/labor/timecards/{id} | RetrieveTimecard |
| PUT | /v2/labor/timecards/{id} | UpdateTimecard |
| GET | /v2/labor/workweek-configs | ListWorkweekConfigs |
| PUT | /v2/labor/workweek-configs/{id} | UpdateWorkweekConfig |

### locations
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/locations | ListLocations |
| POST | /v2/locations | CreateLocation |
| GET | /v2/locations/custom-attribute-definitions | ListLocationCustomAttributeDefinitions |
| POST | /v2/locations/custom-attribute-definitions | CreateLocationCustomAttributeDefinition |
| DELETE | /v2/locations/custom-attribute-definitions/{key} | DeleteLocationCustomAttributeDefinition |
| GET | /v2/locations/custom-attribute-definitions/{key} | RetrieveLocationCustomAttributeDefinition |
| PUT | /v2/locations/custom-attribute-definitions/{key} | UpdateLocationCustomAttributeDefinition |
| POST | /v2/locations/custom-attributes/bulk-delete | BulkDeleteLocationCustomAttributes |
| POST | /v2/locations/custom-attributes/bulk-upsert | BulkUpsertLocationCustomAttributes |
| GET | /v2/locations/{location_id} | RetrieveLocation |
| PUT | /v2/locations/{location_id} | UpdateLocation |
| POST | /v2/locations/{location_id}/checkouts | CreateCheckout |
| GET | /v2/locations/{location_id}/custom-attributes | ListLocationCustomAttributes |
| DELETE | /v2/locations/{location_id}/custom-attributes/{key} | DeleteLocationCustomAttribute |
| GET | /v2/locations/{location_id}/custom-attributes/{key} | RetrieveLocationCustomAttribute |
| POST | /v2/locations/{location_id}/custom-attributes/{key} | UpsertLocationCustomAttribute |
| GET | /v2/locations/{location_id}/transactions | ListTransactions |
| GET | /v2/locations/{location_id}/transactions/{transaction_id} | RetrieveTransaction |
| POST | /v2/locations/{location_id}/transactions/{transaction_id}/capture | CaptureTransaction |
| POST | /v2/locations/{location_id}/transactions/{transaction_id}/void | VoidTransaction |

### loyalty
| Method | Path | Description |
|--------|------|-------------|
| POST | /v2/loyalty/accounts | CreateLoyaltyAccount |
| POST | /v2/loyalty/accounts/search | SearchLoyaltyAccounts |
| GET | /v2/loyalty/accounts/{account_id} | RetrieveLoyaltyAccount |
| POST | /v2/loyalty/accounts/{account_id}/accumulate | AccumulateLoyaltyPoints |
| POST | /v2/loyalty/accounts/{account_id}/adjust | AdjustLoyaltyPoints |
| POST | /v2/loyalty/events/search | SearchLoyaltyEvents |
| GET | /v2/loyalty/programs | ListLoyaltyPrograms |
| GET | /v2/loyalty/programs/{program_id} | RetrieveLoyaltyProgram |
| POST | /v2/loyalty/programs/{program_id}/calculate | CalculateLoyaltyPoints |
| GET | /v2/loyalty/programs/{program_id}/promotions | ListLoyaltyPromotions |
| POST | /v2/loyalty/programs/{program_id}/promotions | CreateLoyaltyPromotion |
| GET | /v2/loyalty/programs/{program_id}/promotions/{promotion_id} | RetrieveLoyaltyPromotion |
| POST | /v2/loyalty/programs/{program_id}/promotions/{promotion_id}/cancel | CancelLoyaltyPromotion |
| POST | /v2/loyalty/rewards | CreateLoyaltyReward |
| POST | /v2/loyalty/rewards/search | SearchLoyaltyRewards |
| DELETE | /v2/loyalty/rewards/{reward_id} | DeleteLoyaltyReward |
| GET | /v2/loyalty/rewards/{reward_id} | RetrieveLoyaltyReward |
| POST | /v2/loyalty/rewards/{reward_id}/redeem | RedeemLoyaltyReward |

### merchants
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/merchants | ListMerchants |
| GET | /v2/merchants/custom-attribute-definitions | ListMerchantCustomAttributeDefinitions |
| POST | /v2/merchants/custom-attribute-definitions | CreateMerchantCustomAttributeDefinition |
| DELETE | /v2/merchants/custom-attribute-definitions/{key} | DeleteMerchantCustomAttributeDefinition |
| GET | /v2/merchants/custom-attribute-definitions/{key} | RetrieveMerchantCustomAttributeDefinition |
| PUT | /v2/merchants/custom-attribute-definitions/{key} | UpdateMerchantCustomAttributeDefinition |
| POST | /v2/merchants/custom-attributes/bulk-delete | BulkDeleteMerchantCustomAttributes |
| POST | /v2/merchants/custom-attributes/bulk-upsert | BulkUpsertMerchantCustomAttributes |
| GET | /v2/merchants/{merchant_id} | RetrieveMerchant |
| GET | /v2/merchants/{merchant_id}/custom-attributes | ListMerchantCustomAttributes |
| DELETE | /v2/merchants/{merchant_id}/custom-attributes/{key} | DeleteMerchantCustomAttribute |
| GET | /v2/merchants/{merchant_id}/custom-attributes/{key} | RetrieveMerchantCustomAttribute |
| POST | /v2/merchants/{merchant_id}/custom-attributes/{key} | UpsertMerchantCustomAttribute |

### online-checkout
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/online-checkout/location-settings/{location_id} | RetrieveLocationSettings |
| PUT | /v2/online-checkout/location-settings/{location_id} | UpdateLocationSettings |
| GET | /v2/online-checkout/merchant-settings | RetrieveMerchantSettings |
| PUT | /v2/online-checkout/merchant-settings | UpdateMerchantSettings |
| GET | /v2/online-checkout/payment-links | ListPaymentLinks |
| POST | /v2/online-checkout/payment-links | CreatePaymentLink |
| DELETE | /v2/online-checkout/payment-links/{id} | DeletePaymentLink |
| GET | /v2/online-checkout/payment-links/{id} | RetrievePaymentLink |
| PUT | /v2/online-checkout/payment-links/{id} | UpdatePaymentLink |

### orders
| Method | Path | Description |
|--------|------|-------------|
| POST | /v2/orders | CreateOrder |
| POST | /v2/orders/batch-retrieve | BatchRetrieveOrders |
| POST | /v2/orders/calculate | CalculateOrder |
| POST | /v2/orders/clone | CloneOrder |
| GET | /v2/orders/custom-attribute-definitions | ListOrderCustomAttributeDefinitions |
| POST | /v2/orders/custom-attribute-definitions | CreateOrderCustomAttributeDefinition |
| DELETE | /v2/orders/custom-attribute-definitions/{key} | DeleteOrderCustomAttributeDefinition |
| GET | /v2/orders/custom-attribute-definitions/{key} | RetrieveOrderCustomAttributeDefinition |
| PUT | /v2/orders/custom-attribute-definitions/{key} | UpdateOrderCustomAttributeDefinition |
| POST | /v2/orders/custom-attributes/bulk-delete | BulkDeleteOrderCustomAttributes |
| POST | /v2/orders/custom-attributes/bulk-upsert | BulkUpsertOrderCustomAttributes |
| POST | /v2/orders/search | SearchOrders |
| GET | /v2/orders/{order_id} | RetrieveOrder |
| PUT | /v2/orders/{order_id} | UpdateOrder |
| GET | /v2/orders/{order_id}/custom-attributes | ListOrderCustomAttributes |
| DELETE | /v2/orders/{order_id}/custom-attributes/{custom_attribute_key} | DeleteOrderCustomAttribute |
| GET | /v2/orders/{order_id}/custom-attributes/{custom_attribute_key} | RetrieveOrderCustomAttribute |
| POST | /v2/orders/{order_id}/custom-attributes/{custom_attribute_key} | UpsertOrderCustomAttribute |
| POST | /v2/orders/{order_id}/pay | PayOrder |

### payments
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/payments | ListPayments |
| POST | /v2/payments | CreatePayment |
| POST | /v2/payments/cancel | CancelPaymentByIdempotencyKey |
| GET | /v2/payments/{payment_id} | GetPayment |
| PUT | /v2/payments/{payment_id} | UpdatePayment |
| POST | /v2/payments/{payment_id}/cancel | CancelPayment |
| POST | /v2/payments/{payment_id}/complete | CompletePayment |

### payouts
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/payouts | ListPayouts |
| GET | /v2/payouts/{payout_id} | GetPayout |
| GET | /v2/payouts/{payout_id}/payout-entries | ListPayoutEntries |

### refunds
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/refunds | ListPaymentRefunds |
| POST | /v2/refunds | RefundPayment |
| GET | /v2/refunds/{refund_id} | GetPaymentRefund |

### sites
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/sites | ListSites |
| DELETE | /v2/sites/{site_id}/snippet | DeleteSnippet |
| GET | /v2/sites/{site_id}/snippet | RetrieveSnippet |
| POST | /v2/sites/{site_id}/snippet | UpsertSnippet |

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| POST | /v2/subscriptions | CreateSubscription |
| POST | /v2/subscriptions/bulk-swap-plan | BulkSwapPlan |
| POST | /v2/subscriptions/search | SearchSubscriptions |
| GET | /v2/subscriptions/{subscription_id} | RetrieveSubscription |
| PUT | /v2/subscriptions/{subscription_id} | UpdateSubscription |
| DELETE | /v2/subscriptions/{subscription_id}/actions/{action_id} | DeleteSubscriptionAction |
| POST | /v2/subscriptions/{subscription_id}/billing-anchor | ChangeBillingAnchorDate |
| POST | /v2/subscriptions/{subscription_id}/cancel | CancelSubscription |
| GET | /v2/subscriptions/{subscription_id}/events | ListSubscriptionEvents |
| POST | /v2/subscriptions/{subscription_id}/pause | PauseSubscription |
| POST | /v2/subscriptions/{subscription_id}/resume | ResumeSubscription |
| POST | /v2/subscriptions/{subscription_id}/swap-plan | SwapPlan |

### team-members
| Method | Path | Description |
|--------|------|-------------|
| POST | /v2/team-members | CreateTeamMember |
| POST | /v2/team-members/bulk-create | BulkCreateTeamMembers |
| POST | /v2/team-members/bulk-update | BulkUpdateTeamMembers |
| GET | /v2/team-members/jobs | ListJobs |
| POST | /v2/team-members/jobs | CreateJob |
| GET | /v2/team-members/jobs/{job_id} | RetrieveJob |
| PUT | /v2/team-members/jobs/{job_id} | UpdateJob |
| POST | /v2/team-members/search | SearchTeamMembers |
| GET | /v2/team-members/{team_member_id} | RetrieveTeamMember |
| PUT | /v2/team-members/{team_member_id} | UpdateTeamMember |
| GET | /v2/team-members/{team_member_id}/wage-setting | RetrieveWageSetting |
| PUT | /v2/team-members/{team_member_id}/wage-setting | UpdateWageSetting |

### terminals
| Method | Path | Description |
|--------|------|-------------|
| POST | /v2/terminals/actions | CreateTerminalAction |
| POST | /v2/terminals/actions/search | SearchTerminalActions |
| GET | /v2/terminals/actions/{action_id} | GetTerminalAction |
| POST | /v2/terminals/actions/{action_id}/cancel | CancelTerminalAction |
| POST | /v2/terminals/actions/{action_id}/dismiss | DismissTerminalAction |
| POST | /v2/terminals/checkouts | CreateTerminalCheckout |
| POST | /v2/terminals/checkouts/search | SearchTerminalCheckouts |
| GET | /v2/terminals/checkouts/{checkout_id} | GetTerminalCheckout |
| POST | /v2/terminals/checkouts/{checkout_id}/cancel | CancelTerminalCheckout |
| POST | /v2/terminals/checkouts/{checkout_id}/dismiss | DismissTerminalCheckout |
| POST | /v2/terminals/refunds | CreateTerminalRefund |
| POST | /v2/terminals/refunds/search | SearchTerminalRefunds |
| GET | /v2/terminals/refunds/{terminal_refund_id} | GetTerminalRefund |
| POST | /v2/terminals/refunds/{terminal_refund_id}/cancel | CancelTerminalRefund |
| POST | /v2/terminals/refunds/{terminal_refund_id}/dismiss | DismissTerminalRefund |

### transfer-orders
| Method | Path | Description |
|--------|------|-------------|
| POST | /v2/transfer-orders | CreateTransferOrder |
| POST | /v2/transfer-orders/search | SearchTransferOrders |
| DELETE | /v2/transfer-orders/{transfer_order_id} | DeleteTransferOrder |
| GET | /v2/transfer-orders/{transfer_order_id} | RetrieveTransferOrder |
| PUT | /v2/transfer-orders/{transfer_order_id} | UpdateTransferOrder |
| POST | /v2/transfer-orders/{transfer_order_id}/cancel | CancelTransferOrder |
| POST | /v2/transfer-orders/{transfer_order_id}/receive | ReceiveTransferOrder |
| POST | /v2/transfer-orders/{transfer_order_id}/start | StartTransferOrder |

### vendors
| Method | Path | Description |
|--------|------|-------------|
| POST | /v2/vendors/bulk-create | BulkCreateVendors |
| POST | /v2/vendors/bulk-retrieve | BulkRetrieveVendors |
| PUT | /v2/vendors/bulk-update | BulkUpdateVendors |
| POST | /v2/vendors/create | CreateVendor |
| POST | /v2/vendors/search | SearchVendors |
| GET | /v2/vendors/{vendor_id} | RetrieveVendor |
| PUT | /v2/vendors/{vendor_id} | UpdateVendor |

### webhooks
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/webhooks/event-types | ListWebhookEventTypes |
| GET | /v2/webhooks/subscriptions | ListWebhookSubscriptions |
| POST | /v2/webhooks/subscriptions | CreateWebhookSubscription |
| DELETE | /v2/webhooks/subscriptions/{subscription_id} | DeleteWebhookSubscription |
| GET | /v2/webhooks/subscriptions/{subscription_id} | RetrieveWebhookSubscription |
| PUT | /v2/webhooks/subscriptions/{subscription_id} | UpdateWebhookSubscription |
| POST | /v2/webhooks/subscriptions/{subscription_id}/signature-key | UpdateWebhookSubscriptionSignatureKey |
| POST | /v2/webhooks/subscriptions/{subscription_id}/test | TestWebhookSubscription |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a authorization-code?" -> POST /mobile/authorization-code
- "Create a revoke?" -> POST /oauth2/revoke
- "Create a token?" -> POST /oauth2/token
- "Create a status?" -> POST /oauth2/token/status
- "List all orders?" -> GET /v1/{location_id}/orders
- "Get order details?" -> GET /v1/{location_id}/orders/{order_id}
- "Update a order?" -> PUT /v1/{location_id}/orders/{order_id}
- "Create a domain?" -> POST /v2/apple-pay/domains
- "List all bank-accounts?" -> GET /v2/bank-accounts
- "Get by-v1-id details?" -> GET /v2/bank-accounts/by-v1-id/{v1_bank_account_id}
- "Get bank-account details?" -> GET /v2/bank-accounts/{bank_account_id}
- "List all bookings?" -> GET /v2/bookings
- "Create a booking?" -> POST /v2/bookings
- "Create a search?" -> POST /v2/bookings/availability/search
- "Create a bulk-retrieve?" -> POST /v2/bookings/bulk-retrieve
- "List all business-booking-profile?" -> GET /v2/bookings/business-booking-profile
- "List all custom-attribute-definitions?" -> GET /v2/bookings/custom-attribute-definitions
- "Create a custom-attribute-definition?" -> POST /v2/bookings/custom-attribute-definitions
- "Delete a custom-attribute-definition?" -> DELETE /v2/bookings/custom-attribute-definitions/{key}
- "Get custom-attribute-definition details?" -> GET /v2/bookings/custom-attribute-definitions/{key}
- "Update a custom-attribute-definition?" -> PUT /v2/bookings/custom-attribute-definitions/{key}
- "Create a bulk-delete?" -> POST /v2/bookings/custom-attributes/bulk-delete
- "Create a bulk-upsert?" -> POST /v2/bookings/custom-attributes/bulk-upsert
- "List all location-booking-profiles?" -> GET /v2/bookings/location-booking-profiles
- "Get location-booking-profile details?" -> GET /v2/bookings/location-booking-profiles/{location_id}
- "List all team-member-booking-profiles?" -> GET /v2/bookings/team-member-booking-profiles
- "Create a bulk-retrieve?" -> POST /v2/bookings/team-member-booking-profiles/bulk-retrieve
- "Get team-member-booking-profile details?" -> GET /v2/bookings/team-member-booking-profiles/{team_member_id}
- "Get booking details?" -> GET /v2/bookings/{booking_id}
- "Update a booking?" -> PUT /v2/bookings/{booking_id}
- "Create a cancel?" -> POST /v2/bookings/{booking_id}/cancel
- "List all custom-attributes?" -> GET /v2/bookings/{booking_id}/custom-attributes
- "Delete a custom-attribute?" -> DELETE /v2/bookings/{booking_id}/custom-attributes/{key}
- "Get custom-attribute details?" -> GET /v2/bookings/{booking_id}/custom-attributes/{key}
- "Update a custom-attribute?" -> PUT /v2/bookings/{booking_id}/custom-attributes/{key}
- "List all cards?" -> GET /v2/cards
- "Create a card?" -> POST /v2/cards
- "Get card details?" -> GET /v2/cards/{card_id}
- "Create a disable?" -> POST /v2/cards/{card_id}/disable
- "List all shifts?" -> GET /v2/cash-drawers/shifts
- "Get shift details?" -> GET /v2/cash-drawers/shifts/{shift_id}
- "List all events?" -> GET /v2/cash-drawers/shifts/{shift_id}/events
- "Create a batch-delete?" -> POST /v2/catalog/batch-delete
- "Create a batch-retrieve?" -> POST /v2/catalog/batch-retrieve
- "Create a batch-upsert?" -> POST /v2/catalog/batch-upsert
- "Create a image?" -> POST /v2/catalog/images
- "Update a image?" -> PUT /v2/catalog/images/{image_id}
- "List all info?" -> GET /v2/catalog/info
- "List all list?" -> GET /v2/catalog/list
- "Create a object?" -> POST /v2/catalog/object
- "Delete a object?" -> DELETE /v2/catalog/object/{object_id}
- "Get object details?" -> GET /v2/catalog/object/{object_id}
- "Create a search?" -> POST /v2/catalog/search
- "Create a search-catalog-item?" -> POST /v2/catalog/search-catalog-items
- "Create a update-item-modifier-list?" -> POST /v2/catalog/update-item-modifier-lists
- "Create a update-item-taxe?" -> POST /v2/catalog/update-item-taxes
- "List all channels?" -> GET /v2/channels
- "Create a bulk-retrieve?" -> POST /v2/channels/bulk-retrieve
- "Get channel details?" -> GET /v2/channels/{channel_id}
- "List all customers?" -> GET /v2/customers
- "Create a customer?" -> POST /v2/customers
- "Create a bulk-create?" -> POST /v2/customers/bulk-create
- "Create a bulk-delete?" -> POST /v2/customers/bulk-delete
- "Create a bulk-retrieve?" -> POST /v2/customers/bulk-retrieve
- "Create a bulk-update?" -> POST /v2/customers/bulk-update
- "List all custom-attribute-definitions?" -> GET /v2/customers/custom-attribute-definitions
- "Create a custom-attribute-definition?" -> POST /v2/customers/custom-attribute-definitions
- "Delete a custom-attribute-definition?" -> DELETE /v2/customers/custom-attribute-definitions/{key}
- "Get custom-attribute-definition details?" -> GET /v2/customers/custom-attribute-definitions/{key}
- "Update a custom-attribute-definition?" -> PUT /v2/customers/custom-attribute-definitions/{key}
- "Create a bulk-upsert?" -> POST /v2/customers/custom-attributes/bulk-upsert
- "List all groups?" -> GET /v2/customers/groups
- "Create a group?" -> POST /v2/customers/groups
- "Delete a group?" -> DELETE /v2/customers/groups/{group_id}
- "Get group details?" -> GET /v2/customers/groups/{group_id}
- "Update a group?" -> PUT /v2/customers/groups/{group_id}
- "Create a search?" -> POST /v2/customers/search
- "List all segments?" -> GET /v2/customers/segments
- "Get segment details?" -> GET /v2/customers/segments/{segment_id}
- "Delete a customer?" -> DELETE /v2/customers/{customer_id}
- "Get customer details?" -> GET /v2/customers/{customer_id}
- "Update a customer?" -> PUT /v2/customers/{customer_id}
- "Create a card?" -> POST /v2/customers/{customer_id}/cards
- "Delete a card?" -> DELETE /v2/customers/{customer_id}/cards/{card_id}
- "List all custom-attributes?" -> GET /v2/customers/{customer_id}/custom-attributes
- "Delete a custom-attribute?" -> DELETE /v2/customers/{customer_id}/custom-attributes/{key}
- "Get custom-attribute details?" -> GET /v2/customers/{customer_id}/custom-attributes/{key}
- "Delete a group?" -> DELETE /v2/customers/{customer_id}/groups/{group_id}
- "Update a group?" -> PUT /v2/customers/{customer_id}/groups/{group_id}
- "List all devices?" -> GET /v2/devices
- "List all codes?" -> GET /v2/devices/codes
- "Create a code?" -> POST /v2/devices/codes
- "Get code details?" -> GET /v2/devices/codes/{id}
- "Get device details?" -> GET /v2/devices/{device_id}
- "List all disputes?" -> GET /v2/disputes
- "Get dispute details?" -> GET /v2/disputes/{dispute_id}
- "Create a accept?" -> POST /v2/disputes/{dispute_id}/accept
- "List all evidence?" -> GET /v2/disputes/{dispute_id}/evidence
- "Create a evidence-file?" -> POST /v2/disputes/{dispute_id}/evidence-files
- "Create a evidence-text?" -> POST /v2/disputes/{dispute_id}/evidence-text
- "Delete a evidence?" -> DELETE /v2/disputes/{dispute_id}/evidence/{evidence_id}
- "Get evidence details?" -> GET /v2/disputes/{dispute_id}/evidence/{evidence_id}
- "Create a submit-evidence?" -> POST /v2/disputes/{dispute_id}/submit-evidence
- "List all employees?" -> GET /v2/employees
- "Get employee details?" -> GET /v2/employees/{id}
- "Create a event?" -> POST /v2/events
- "List all types?" -> GET /v2/events/types
- "List all gift-cards?" -> GET /v2/gift-cards
- "Create a gift-card?" -> POST /v2/gift-cards
- "List all activities?" -> GET /v2/gift-cards/activities
- "Create a activity?" -> POST /v2/gift-cards/activities
- "Create a from-gan?" -> POST /v2/gift-cards/from-gan
- "Create a from-nonce?" -> POST /v2/gift-cards/from-nonce
- "Create a link-customer?" -> POST /v2/gift-cards/{gift_card_id}/link-customer
- "Create a unlink-customer?" -> POST /v2/gift-cards/{gift_card_id}/unlink-customer
- "Get gift-card details?" -> GET /v2/gift-cards/{id}
- "Get adjustment details?" -> GET /v2/inventory/adjustment/{adjustment_id}
- "Get adjustment details?" -> GET /v2/inventory/adjustments/{adjustment_id}
- "Create a batch-change?" -> POST /v2/inventory/batch-change
- "Create a batch-retrieve-change?" -> POST /v2/inventory/batch-retrieve-changes
- "Create a batch-retrieve-count?" -> POST /v2/inventory/batch-retrieve-counts
- "Create a batch-create?" -> POST /v2/inventory/changes/batch-create
- "Create a batch-retrieve?" -> POST /v2/inventory/changes/batch-retrieve
- "Create a batch-retrieve?" -> POST /v2/inventory/counts/batch-retrieve
- "Get physical-count details?" -> GET /v2/inventory/physical-count/{physical_count_id}
- "Get physical-count details?" -> GET /v2/inventory/physical-counts/{physical_count_id}
- "Get transfer details?" -> GET /v2/inventory/transfers/{transfer_id}
- "Get inventory details?" -> GET /v2/inventory/{catalog_object_id}
- "List all changes?" -> GET /v2/inventory/{catalog_object_id}/changes
- "List all invoices?" -> GET /v2/invoices
- "Create a invoice?" -> POST /v2/invoices
- "Create a search?" -> POST /v2/invoices/search
- "Delete a invoice?" -> DELETE /v2/invoices/{invoice_id}
- "Get invoice details?" -> GET /v2/invoices/{invoice_id}
- "Update a invoice?" -> PUT /v2/invoices/{invoice_id}
- "Create a attachment?" -> POST /v2/invoices/{invoice_id}/attachments
- "Delete a attachment?" -> DELETE /v2/invoices/{invoice_id}/attachments/{attachment_id}
- "Create a cancel?" -> POST /v2/invoices/{invoice_id}/cancel
- "Create a publish?" -> POST /v2/invoices/{invoice_id}/publish
- "List all break-types?" -> GET /v2/labor/break-types
- "Create a break-type?" -> POST /v2/labor/break-types
- "Delete a break-type?" -> DELETE /v2/labor/break-types/{id}
- "Get break-type details?" -> GET /v2/labor/break-types/{id}
- "Update a break-type?" -> PUT /v2/labor/break-types/{id}
- "List all employee-wages?" -> GET /v2/labor/employee-wages
- "Get employee-wage details?" -> GET /v2/labor/employee-wages/{id}
- "Create a scheduled-shift?" -> POST /v2/labor/scheduled-shifts
- "Create a bulk-publish?" -> POST /v2/labor/scheduled-shifts/bulk-publish
- "Create a search?" -> POST /v2/labor/scheduled-shifts/search
- "Get scheduled-shift details?" -> GET /v2/labor/scheduled-shifts/{id}
- "Update a scheduled-shift?" -> PUT /v2/labor/scheduled-shifts/{id}
- "Create a publish?" -> POST /v2/labor/scheduled-shifts/{id}/publish
- "Create a shift?" -> POST /v2/labor/shifts
- "Create a search?" -> POST /v2/labor/shifts/search
- "Delete a shift?" -> DELETE /v2/labor/shifts/{id}
- "Get shift details?" -> GET /v2/labor/shifts/{id}
- "Update a shift?" -> PUT /v2/labor/shifts/{id}
- "List all team-member-wages?" -> GET /v2/labor/team-member-wages
- "Get team-member-wage details?" -> GET /v2/labor/team-member-wages/{id}
- "Create a timecard?" -> POST /v2/labor/timecards
- "Create a search?" -> POST /v2/labor/timecards/search
- "Delete a timecard?" -> DELETE /v2/labor/timecards/{id}
- "Get timecard details?" -> GET /v2/labor/timecards/{id}
- "Update a timecard?" -> PUT /v2/labor/timecards/{id}
- "List all workweek-configs?" -> GET /v2/labor/workweek-configs
- "Update a workweek-config?" -> PUT /v2/labor/workweek-configs/{id}
- "List all locations?" -> GET /v2/locations
- "Create a location?" -> POST /v2/locations
- "List all custom-attribute-definitions?" -> GET /v2/locations/custom-attribute-definitions
- "Create a custom-attribute-definition?" -> POST /v2/locations/custom-attribute-definitions
- "Delete a custom-attribute-definition?" -> DELETE /v2/locations/custom-attribute-definitions/{key}
- "Get custom-attribute-definition details?" -> GET /v2/locations/custom-attribute-definitions/{key}
- "Update a custom-attribute-definition?" -> PUT /v2/locations/custom-attribute-definitions/{key}
- "Create a bulk-delete?" -> POST /v2/locations/custom-attributes/bulk-delete
- "Create a bulk-upsert?" -> POST /v2/locations/custom-attributes/bulk-upsert
- "Get location details?" -> GET /v2/locations/{location_id}
- "Update a location?" -> PUT /v2/locations/{location_id}
- "Create a checkout?" -> POST /v2/locations/{location_id}/checkouts
- "List all custom-attributes?" -> GET /v2/locations/{location_id}/custom-attributes
- "Delete a custom-attribute?" -> DELETE /v2/locations/{location_id}/custom-attributes/{key}
- "Get custom-attribute details?" -> GET /v2/locations/{location_id}/custom-attributes/{key}
- "List all transactions?" -> GET /v2/locations/{location_id}/transactions
- "Get transaction details?" -> GET /v2/locations/{location_id}/transactions/{transaction_id}
- "Create a capture?" -> POST /v2/locations/{location_id}/transactions/{transaction_id}/capture
- "Create a void?" -> POST /v2/locations/{location_id}/transactions/{transaction_id}/void
- "Create a account?" -> POST /v2/loyalty/accounts
- "Create a search?" -> POST /v2/loyalty/accounts/search
- "Get account details?" -> GET /v2/loyalty/accounts/{account_id}
- "Create a accumulate?" -> POST /v2/loyalty/accounts/{account_id}/accumulate
- "Create a adjust?" -> POST /v2/loyalty/accounts/{account_id}/adjust
- "Create a search?" -> POST /v2/loyalty/events/search
- "List all programs?" -> GET /v2/loyalty/programs
- "Get program details?" -> GET /v2/loyalty/programs/{program_id}
- "Create a calculate?" -> POST /v2/loyalty/programs/{program_id}/calculate
- "List all promotions?" -> GET /v2/loyalty/programs/{program_id}/promotions
- "Create a promotion?" -> POST /v2/loyalty/programs/{program_id}/promotions
- "Get promotion details?" -> GET /v2/loyalty/programs/{program_id}/promotions/{promotion_id}
- "Create a cancel?" -> POST /v2/loyalty/programs/{program_id}/promotions/{promotion_id}/cancel
- "Create a reward?" -> POST /v2/loyalty/rewards
- "Create a search?" -> POST /v2/loyalty/rewards/search
- "Delete a reward?" -> DELETE /v2/loyalty/rewards/{reward_id}
- "Get reward details?" -> GET /v2/loyalty/rewards/{reward_id}
- "Create a redeem?" -> POST /v2/loyalty/rewards/{reward_id}/redeem
- "List all merchants?" -> GET /v2/merchants
- "List all custom-attribute-definitions?" -> GET /v2/merchants/custom-attribute-definitions
- "Create a custom-attribute-definition?" -> POST /v2/merchants/custom-attribute-definitions
- "Delete a custom-attribute-definition?" -> DELETE /v2/merchants/custom-attribute-definitions/{key}
- "Get custom-attribute-definition details?" -> GET /v2/merchants/custom-attribute-definitions/{key}
- "Update a custom-attribute-definition?" -> PUT /v2/merchants/custom-attribute-definitions/{key}
- "Create a bulk-delete?" -> POST /v2/merchants/custom-attributes/bulk-delete
- "Create a bulk-upsert?" -> POST /v2/merchants/custom-attributes/bulk-upsert
- "Get merchant details?" -> GET /v2/merchants/{merchant_id}
- "List all custom-attributes?" -> GET /v2/merchants/{merchant_id}/custom-attributes
- "Delete a custom-attribute?" -> DELETE /v2/merchants/{merchant_id}/custom-attributes/{key}
- "Get custom-attribute details?" -> GET /v2/merchants/{merchant_id}/custom-attributes/{key}
- "Get location-setting details?" -> GET /v2/online-checkout/location-settings/{location_id}
- "Update a location-setting?" -> PUT /v2/online-checkout/location-settings/{location_id}
- "List all merchant-settings?" -> GET /v2/online-checkout/merchant-settings
- "List all payment-links?" -> GET /v2/online-checkout/payment-links
- "Create a payment-link?" -> POST /v2/online-checkout/payment-links
- "Delete a payment-link?" -> DELETE /v2/online-checkout/payment-links/{id}
- "Get payment-link details?" -> GET /v2/online-checkout/payment-links/{id}
- "Update a payment-link?" -> PUT /v2/online-checkout/payment-links/{id}
- "Create a order?" -> POST /v2/orders
- "Create a batch-retrieve?" -> POST /v2/orders/batch-retrieve
- "Create a calculate?" -> POST /v2/orders/calculate
- "Create a clone?" -> POST /v2/orders/clone
- "List all custom-attribute-definitions?" -> GET /v2/orders/custom-attribute-definitions
- "Create a custom-attribute-definition?" -> POST /v2/orders/custom-attribute-definitions
- "Delete a custom-attribute-definition?" -> DELETE /v2/orders/custom-attribute-definitions/{key}
- "Get custom-attribute-definition details?" -> GET /v2/orders/custom-attribute-definitions/{key}
- "Update a custom-attribute-definition?" -> PUT /v2/orders/custom-attribute-definitions/{key}
- "Create a bulk-delete?" -> POST /v2/orders/custom-attributes/bulk-delete
- "Create a bulk-upsert?" -> POST /v2/orders/custom-attributes/bulk-upsert
- "Create a search?" -> POST /v2/orders/search
- "Get order details?" -> GET /v2/orders/{order_id}
- "Update a order?" -> PUT /v2/orders/{order_id}
- "List all custom-attributes?" -> GET /v2/orders/{order_id}/custom-attributes
- "Delete a custom-attribute?" -> DELETE /v2/orders/{order_id}/custom-attributes/{custom_attribute_key}
- "Get custom-attribute details?" -> GET /v2/orders/{order_id}/custom-attributes/{custom_attribute_key}
- "Create a pay?" -> POST /v2/orders/{order_id}/pay
- "List all payments?" -> GET /v2/payments
- "Create a payment?" -> POST /v2/payments
- "Create a cancel?" -> POST /v2/payments/cancel
- "Get payment details?" -> GET /v2/payments/{payment_id}
- "Update a payment?" -> PUT /v2/payments/{payment_id}
- "Create a cancel?" -> POST /v2/payments/{payment_id}/cancel
- "Create a complete?" -> POST /v2/payments/{payment_id}/complete
- "List all payouts?" -> GET /v2/payouts
- "Get payout details?" -> GET /v2/payouts/{payout_id}
- "List all payout-entries?" -> GET /v2/payouts/{payout_id}/payout-entries
- "List all refunds?" -> GET /v2/refunds
- "Create a refund?" -> POST /v2/refunds
- "Get refund details?" -> GET /v2/refunds/{refund_id}
- "List all sites?" -> GET /v2/sites
- "List all snippet?" -> GET /v2/sites/{site_id}/snippet
- "Create a snippet?" -> POST /v2/sites/{site_id}/snippet
- "Create a subscription?" -> POST /v2/subscriptions
- "Create a bulk-swap-plan?" -> POST /v2/subscriptions/bulk-swap-plan
- "Create a search?" -> POST /v2/subscriptions/search
- "Get subscription details?" -> GET /v2/subscriptions/{subscription_id}
- "Update a subscription?" -> PUT /v2/subscriptions/{subscription_id}
- "Delete a action?" -> DELETE /v2/subscriptions/{subscription_id}/actions/{action_id}
- "Create a billing-anchor?" -> POST /v2/subscriptions/{subscription_id}/billing-anchor
- "Create a cancel?" -> POST /v2/subscriptions/{subscription_id}/cancel
- "List all events?" -> GET /v2/subscriptions/{subscription_id}/events
- "Create a pause?" -> POST /v2/subscriptions/{subscription_id}/pause
- "Create a resume?" -> POST /v2/subscriptions/{subscription_id}/resume
- "Create a swap-plan?" -> POST /v2/subscriptions/{subscription_id}/swap-plan
- "Create a team-member?" -> POST /v2/team-members
- "Create a bulk-create?" -> POST /v2/team-members/bulk-create
- "Create a bulk-update?" -> POST /v2/team-members/bulk-update
- "List all jobs?" -> GET /v2/team-members/jobs
- "Create a job?" -> POST /v2/team-members/jobs
- "Get job details?" -> GET /v2/team-members/jobs/{job_id}
- "Update a job?" -> PUT /v2/team-members/jobs/{job_id}
- "Create a search?" -> POST /v2/team-members/search
- "Get team-member details?" -> GET /v2/team-members/{team_member_id}
- "Update a team-member?" -> PUT /v2/team-members/{team_member_id}
- "List all wage-setting?" -> GET /v2/team-members/{team_member_id}/wage-setting
- "Create a action?" -> POST /v2/terminals/actions
- "Create a search?" -> POST /v2/terminals/actions/search
- "Get action details?" -> GET /v2/terminals/actions/{action_id}
- "Create a cancel?" -> POST /v2/terminals/actions/{action_id}/cancel
- "Create a dismiss?" -> POST /v2/terminals/actions/{action_id}/dismiss
- "Create a checkout?" -> POST /v2/terminals/checkouts
- "Create a search?" -> POST /v2/terminals/checkouts/search
- "Get checkout details?" -> GET /v2/terminals/checkouts/{checkout_id}
- "Create a cancel?" -> POST /v2/terminals/checkouts/{checkout_id}/cancel
- "Create a dismiss?" -> POST /v2/terminals/checkouts/{checkout_id}/dismiss
- "Create a refund?" -> POST /v2/terminals/refunds
- "Create a search?" -> POST /v2/terminals/refunds/search
- "Get refund details?" -> GET /v2/terminals/refunds/{terminal_refund_id}
- "Create a cancel?" -> POST /v2/terminals/refunds/{terminal_refund_id}/cancel
- "Create a dismiss?" -> POST /v2/terminals/refunds/{terminal_refund_id}/dismiss
- "Create a transfer-order?" -> POST /v2/transfer-orders
- "Create a search?" -> POST /v2/transfer-orders/search
- "Delete a transfer-order?" -> DELETE /v2/transfer-orders/{transfer_order_id}
- "Get transfer-order details?" -> GET /v2/transfer-orders/{transfer_order_id}
- "Update a transfer-order?" -> PUT /v2/transfer-orders/{transfer_order_id}
- "Create a cancel?" -> POST /v2/transfer-orders/{transfer_order_id}/cancel
- "Create a receive?" -> POST /v2/transfer-orders/{transfer_order_id}/receive
- "Create a start?" -> POST /v2/transfer-orders/{transfer_order_id}/start
- "Create a bulk-create?" -> POST /v2/vendors/bulk-create
- "Create a bulk-retrieve?" -> POST /v2/vendors/bulk-retrieve
- "Create a create?" -> POST /v2/vendors/create
- "Create a search?" -> POST /v2/vendors/search
- "Get vendor details?" -> GET /v2/vendors/{vendor_id}
- "Update a vendor?" -> PUT /v2/vendors/{vendor_id}
- "List all event-types?" -> GET /v2/webhooks/event-types
- "List all subscriptions?" -> GET /v2/webhooks/subscriptions
- "Create a subscription?" -> POST /v2/webhooks/subscriptions
- "Delete a subscription?" -> DELETE /v2/webhooks/subscriptions/{subscription_id}
- "Get subscription details?" -> GET /v2/webhooks/subscriptions/{subscription_id}
- "Update a subscription?" -> PUT /v2/webhooks/subscriptions/{subscription_id}
- "Create a signature-key?" -> POST /v2/webhooks/subscriptions/{subscription_id}/signature-key
- "Create a test?" -> POST /v2/webhooks/subscriptions/{subscription_id}/test
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
