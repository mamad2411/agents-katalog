---
name: product_builder_ui_spec
description: PRODUCT BUILDER UI SPEC
---

# PRODUCT BUILDER UI SPEC

This skill defines the autonomous behavior, system prompt, and capabilities for the agent **PRODUCT BUILDER UI SPEC**.

## Source Location
Originally discovered in Rick's Downloads at: `/Users/kalivibecoding/Downloads/angel solutions site/internet_archive_master/prometheus-archive-engine-v3.1-STORAGE-STRIPE-COMPLETE/prometheus-archive-engine/docs/PRODUCT_BUILDER_UI_SPEC.md`

## 🧠 Master Agent Prompt & Capabilities

# 🛍️ PRODUCT BUILDER UI SPECIFICATIONS
## No-Code Product Creation & Management Interface

**Tech Stack**: Next.js 16.2 + React 19.2 + Tailwind 4.2 + shadcn/ui v4 + Stripe Embedded

═══════════════════════════════════════════════════════════════════
## 🏗️ PRODUCT BUILDER DASHBOARD (`/products`)
═══════════════════════════════════════════════════════════════════

### **Main Layout**
```tsx
<ProductDashboard>
  {/* Header */}
  <DashboardHeader>
    <h1>Products</h1>
    <div className="flex gap-2">
      <Button onClick={openProductBuilder}>
        <Plus className="w-4 h-4 mr-2" />
        Create Product
      </Button>
      <Button variant="outline" onClick={importProducts}>
        <Upload className="w-4 h-4 mr-2" />
        Import
      </Button>
    </div>
  </DashboardHeader>
  
  {/* Stats Row */}
  <StatsGrid>
    <StatCard
      title="Total Products"
      value="127"
      icon={<Package />}
      trend="+12 this month"
    />
    <StatCard
      title="Total Revenue"
      value="$45,230"
      icon={<DollarSign />}
      trend="+23% vs last month"
    />
    <StatCard
      title="Active Subscriptions"
      value="234"
      icon={<Repeat />}
      trend="+15%"
    />
    <StatCard
      title="Conversion Rate"
      value="3.2%"
      icon={<TrendingUp />}
      trend="+0.5%"
    />
  </StatsGrid>
  
  {/* Filters & Search */}
  <FilterBar>
    <SearchInput
      placeholder="Search products..."
      value={searchQuery}
      onChange={setSearchQuery}
    />
    
    <FilterGroup>
      <Select
        placeholder="Type"
        options={[
          {value: "all", label: "All Types"},
          {value: "digital", label: "Digital Downloads"},
          {value: "collection", label: "Collections"},
          {value: "course", label: "Courses"},
          {value: "subscription", label: "Subscriptions"}
        ]}
        value={filterType}
        onChange={setFilterType}
      />
      
      <Select
        placeholder="Status"
        options={[
          {value: "all", label: "All"},
          {value: "active", label: "Active"},
          {value: "draft", label: "Draft"},
          {value: "archived", label: "Archived"}
        ]}
        value={filterStatus}
        onChange={setFilterStatus}
      />
      
      <Select
        placeholder="Sort by"
        options={[
          {value: "name_asc", label: "Name (A-Z)"},
          {value: "name_desc", label: "Name (Z-A)"},
          {value: "price_asc", label: "Price (Low to High)"},
          {value: "price_desc", label: "Price (High to Low)"},
          {value: "sales_desc", label: "Best Selling"},
          {value: "created_desc", label: "Newest"},
          {value: "created_asc", label: "Oldest"}
        ]}
        value={sortBy}
        onChange={setSortBy}
      />
    </FilterGroup>
  </FilterBar>
  
  {/* Products Grid */}
  <ProductsGrid>
    {products.map(product => (
      <ProductCard
        key={product.id}
        product={product}
        thumbnail={product.images[0]}
        name={product.name}
        price={formatPrice(product.price)}
        type={product.type}
        sales={product.sales_count}
        revenue={product.total_revenue}
        status={product.status}
        actions={[
          {icon: "Eye", label: "View", onClick: () => viewProduct(product.id)},
          {icon: "Edit", label: "Edit", onClick: () => editProduct(product.id)},
          {icon: "Copy", label: "Duplicate", onClick: () => duplicateProduct(product.id)},
          {icon: "Link", label: "Copy Link", onClick: () => copyPaymentLink(product.id)},
          {icon: "BarChart", label: "Analytics", onClick: () => viewAnalytics(product.id)},
          {separator: true},
          {icon: "Archive", label: "Archive", onClick: () => archiveProduct(product.id)},
          {icon: "Trash", label: "Delete", onClick: () => deleteProduct(product.id), danger: true}
        ]}
      >
        <ProductCardContent>
          <ProductImage src={product.images[0]} alt={product.name} />
          <ProductName>{product.name}</ProductName>
          <ProductPrice>${product.price}</ProductPrice>
          <ProductStats>
            <Stat icon={<ShoppingCart />} value={product.sales_count} label="sales" />
            <Stat icon={<DollarSign />} value={formatPrice(product.total_revenue)} label="revenue" />
          </ProductStats>
          <ProductStatus status={product.status} />
        </ProductCardContent>
      </ProductCard>
    ))}
  </ProductsGrid>
</ProductDashboard>
```

═══════════════════════════════════════════════════════════════════
## 🎨 PRODUCT BUILDER INTERFACE (`/products/create`)
═══════════════════════════════════════════════════════════════════

### **Step-by-Step Builder**
```tsx
<ProductBuilder>
  {/* Progress Stepper */}
  <StepperHeader>
    <Step number={1} label="Type" active={currentStep === 1} completed={currentStep > 1} />
    <Step number={2} label="Details" active={currentStep === 2} completed={currentStep > 2} />
    <Step number={3} label="Content" active={currentStep === 3} completed={currentStep > 3} />
    <Step number={4} label="Pricing" active={currentStep === 4} completed={currentStep > 4} />
    <Step number={5} label="Preview" active={currentStep === 5} completed={currentStep > 5} />
  </StepperHeader>
  
  {/* STEP 1: Choose Product Type */}
  {currentStep === 1 && (
    <ProductTypeSelector>
      <TypeCard
        icon={<Download />}
        title="Digital Download"
        description="Sell files, ebooks, software, templates"
        selected={productType === "digital"}
        onClick={() => setProductType("digital")}
      />
      
      <TypeCard
        icon={<Package />}
        title="Collection / Bundle"
        description="Group multiple items into a package"
        selected={productType === "collection"}
        onClick={() => setProductType("collection")}
      />
      
      <TypeCard
        icon={<GraduationCap />}
        title="Online Course"
        description="Create structured learning content"
        selected={productType === "course"}
        onClick={() => setProductType("course")}
      />
      
      <TypeCard
        icon={<Hammer />}
        title="Custom Build"
        description="On-demand software compilation"
        selected={productType === "build"}
        onClick={() => setProductType("build")}
        badge="NEW"
      />
      
      <TypeCard
        icon={<Repeat />}
        title="Subscription"
        description="Recurring access or service"
        selected={productType === "subscription"}
        onClick={() => setProductType("subscription")}
      />
    </ProductTypeSelector>
  )}
  
  {/* STEP 2: Product Details */}
  {currentStep === 2 && (
    <ProductDetailsForm>
      <FormSection title="Basic Information">
        <Input
          label="Product Name"
          placeholder="My Awesome Product"
          value={productName}
          onChange={setProductName}
          required
        />
        
        <RichTextEditor
          label="Description"
          placeholder="Describe your product..."
          value={description}
          onChange={setDescription}
          toolbar={["bold", "italic", "link", "list", "heading"]}
          height={200}
        />
        
        <TagInput
          label="Tags"
          placeholder="Add tags..."
          tags={tags}
          onAdd={addTag}
          onRemove={removeTag}
          suggestions={tagSuggestions}
        />
      </FormSection>
      
      <FormSection title="Images">
        <ImageUploader
          images={productImages}
          onUpload={uploadImage}
          onRemove={removeImage}
          onReorder={reorderImages}
          maxImages={10}
          recommended="1200x800px, PNG or JPG"
        />
      </FormSection>
      
      <FormSection title="Features">
        <FeatureList
          features={features}
          onAdd={addFeature}
          onRemove={removeFeature}
          onEdit={editFeature}
        />
        <Button variant="outline" onClick={addFeature}>
          <Plus className="w-4 h-4 mr-2" />
          Add Feature
        </Button>
      </FormSection>
      
      <FormSection title="Category">
        <Select
          label="Primary Category"
          options={categories}
          value={category}
          onChange={setCategory}
        />
        
        <MultiSelect
          label="Subcategories"
          options={subcategories}
          value={selectedSubcategories}
          onChange={setSelectedSubcategories}
        />
      </FormSection>
    </ProductDetailsForm>
  )}
  
  {/* STEP 3: Content */}
  {currentStep === 3 && (
    <ProductContentBuilder>
      {productType === "digital" && (
        <DigitalContentManager>
          <FileUploader
            label="Product Files"
            files={productFiles}
            onUpload={uploadFile}
            onRemove={removeFile}
            maxSize="5GB"
            accept="*/*"
          />
          
          <FileList>
            {productFiles.map(file => (
              <FileItem
                key={file.id}
                name={file.name}
                size={file.size}
                type={file.type}
                onRemove={() => removeFile(file.id)}
              />
            ))}
          </FileList>
        </DigitalContentManager>
      )}
      
      {productType === "collection" && (
        <CollectionBuilder>
          <AvailableItems>
            <h3>Available Items</h3>
            <ItemSearch
              placeholder="Search items..."
              onSearch={searchItems}
            />
            <ItemList
              items={availableItems}
              onAdd={addToCollection}
            />
          </AvailableItems>
          
          <CollectionItems>
            <h3>Collection Items ({collectionItems.length})</h3>
            <DragDropList
              items={collectionItems}
              onReorder={reorderCollectionItems}
              onRemove={removeFromCollection}
            />
          </CollectionItems>
        </CollectionBuilder>
      )}
      
      {productType === "course" && (
        <CourseContentBuilder>
          <ModuleList>
            {modules.map((module, idx) => (
              <ModuleCard key={module.id}>
                <ModuleHeader>
                  <Input
                    value={module.title}
                    onChange={(val) => updateModuleTitle(module.id, val)}
                    placeholder="Module title"
                  />
                  <IconButton onClick={() => deleteModule(module.id)}>
                    <Trash />
                  </IconButton>
                </ModuleHeader>
                
                <LessonList>
                  {module.lessons.map(lesson => (
                    <LessonItem
                      key={lesson.id}
                      lesson={lesson}
                      onEdit={() => editLesson(lesson.id)}
                      onDelete={() => deleteLesson(lesson.id)}
                    />
                  ))}
                </LessonList>
                
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => addLesson(module.id)}
                >
                  <Plus className="w-4 h-4 mr-1" />
                  Add Lesson
                </Button>
              </ModuleCard>
            ))}
          </ModuleList>
          
          <Button onClick={addModule}>
            <Plus className="w-4 h-4 mr-2" />
            Add Module
          </Button>
        </CourseContentBuilder>
      )}
      
      {productType === "build" && (
        <CustomBuildConfig>
          <Input
            label="Source Identifier"
            placeholder="Internet Archive item ID"
            value={sourceId}
            onChange={setSourceId}
          />
          
          <Select
            label="Target Platform"
            options={[
              {value: "linux-x64", label: "Linux (x86_64)"},
              {value: "linux-arm64", label: "Linux (ARM64)"},
              {value: "windows-x64", label: "Windows (x86_64)"},
              {value: "macos-x64", label: "macOS (Intel)"},
              {value: "macos-arm64", label: "macOS (Apple Silicon)"}
            ]}
            value={targetPlatform}
            onChange={setTargetPlatform}
          />
          
          <Textarea
            label="Build Instructions"
            placeholder="Special build requirements..."
            value={buildInstructions}
            onChange={setBuildInstructions}
          />
        </CustomBuildConfig>
      )}
    </ProductContentBuilder>
  )}
  
  {/* STEP 4: Pricing */}
  {currentStep === 4 && (
    <PricingConfiguration>
      <PricingTypeSelector>
        <RadioGroup
          value={pricingType}
          onChange={setPricingType}
          options={[
            {
              value: "one_time",
              label: "One-Time Payment",
              description: "Customer pays once"
            },
            {
              value: "recurring",
              label: "Recurring / Subscription",
              description: "Customer pays regularly"
            },
            {
              value: "usage",
              label: "Usage-Based",
              description: "Pay per use (API calls, storage, etc.)"
            },
            {
              value: "tiered",
              label: "Tiered Pricing",
              description: "Different price levels"
            }
          ]}
        />
      </PricingTypeSelector>
      
      {pricingType === "one_time" && (
        <OneTimePricing>
          <CurrencyInput
            label="Price"
            value={price}
            onChange={setPrice}
            currency="USD"
            placeholder="0.00"
          />
          
          <Checkbox
            label="Allow customers to name their price (Pay what you want)"
            checked={pwyw}
            onChange={setPwyw}
          />
          
          {pwyw && (
            <CurrencyInput
              label="Minimum Price"
              value={minPrice}
              onChange={setMinPrice}
              currency="USD"
            />
          )}
        </OneTimePricing>
      )}
      
      {pricingType === "recurring" && (
        <RecurringPricing>
          <CurrencyInput
            label="Price"
            value={price}
            onChange={setPrice}
            currency="USD"
          />
          
          <Select
            label="Billing Interval"
            options={[
              {value: "day", label: "Daily"},
              {value: "week", label: "Weekly"},
              {value: "month", label: "Monthly"},
              {value: "year", label: "Yearly"}
            ]}
            value={interval}
            onChange={setInterval}
          />
          
          <Input
            label="Free Trial Period (days)"
            type="number"
            value={trialDays}
            onChange={setTrialDays}
            placeholder="0"
          />
        </RecurringPricing>
      )}
      
      {pricingType === "tiered" && (
        <TieredPricing>
          {pricingTiers.map((tier, idx) => (
            <TierCard key={idx}>
              <Input
                label="Tier Name"
                value={tier.name}
                onChange={(val) => updateTier(idx, "name", val)}
                placeholder="Basic, Pro, Enterprise"
              />
              
              <CurrencyInput
                label="Price"
                value={tier.price}
                onChange={(val) => updateTier(idx, "price", val)}
              />
              
              <FeatureList
                features={tier.features}
                onAdd={(feature) => addTierFeature(idx, feature)}
                onRemove={(featureIdx) => removeTierFeature(idx, featureIdx)}
              />
              
              <Button
                variant="destructive"
                size="sm"
                onClick={() => removeTier(idx)}
              >
                Remove Tier
              </Button>
            </TierCard>
          ))}
          
          <Button onClick={addTier}>
            <Plus className="w-4 h-4 mr-2" />
            Add Tier
          </Button>
        </TieredPricing>
      )}
      
      <AdvancedPricingOptions>
        <Accordion>
          <AccordionItem title="Tax Settings">
            <Checkbox
              label="Enable automatic tax calculation (Stripe Tax)"
              checked={autoTax}
              onChange={setAutoTax}
            />
            
            {autoTax && (
              <Select
                label="Product Tax Code"
                options={taxCodes}
                value={taxCode}
                onChange={setTaxCode}
              />
            )}
          </AccordionItem>
          
          <AccordionItem title="Discounts & Coupons">
            <Checkbox
              label="Allow promotion codes at checkout"
              checked={allowCoupons}
              onChange={setAllowCoupons}
            />
          </AccordionItem>
          
          <AccordionItem title="Purchase Limits">
            <Input
              label="Max purchases per customer"
              type="number"
              value={maxPurchases}
              onChange={setMaxPurchases}
              placeholder="Unlimited"
            />
            
            <Input
              label="Total stock available"
              type="number"
              value={stockLimit}
              onChange={setStockLimit}
              placeholder="Unlimited"
            />
          </AccordionItem>
        </Accordion>
      </AdvancedPricingOptions>
    </PricingConfiguration>
  )}
  
  {/* STEP 5: Preview & Publish */}
  {currentStep === 5 && (
    <ProductPreview>
      <PreviewPane>
        <ProductPreviewCard
          name={productName}
          description={description}
          images={productImages}
          price={price}
          features={features}
          type={productType}
        />
        
        {/* Live Checkout Preview */}
        <CheckoutPreview>
          <h3>Checkout Preview</h3>
          <div id="checkout-preview"></div>
        </CheckoutPreview>
      </PreviewPane>
      
      <PublishSettings>
        <FormSection title="Publishing">
          <RadioGroup
            label="Status"
            value={publishStatus}
            onChange={setPublishStatus}
            options={[
              {
                value: "draft",
                label: "Save as Draft",
                description: "Not visible to customers"
              },
              {
                value: "active",
                label: "Publish Live",
                description: "Immediately available for purchase"
              },
              {
                value: "scheduled",
                label: "Schedule Release",
                description: "Publish at a specific time"
              }
            ]}
          />
          
          {publishStatus === "scheduled" && (
            <DateTimePicker
              label="Release Date & Time"
              value={releaseDate}
              onChange={setReleaseDate}
            />
          )}
        </FormSection>
        
        <FormSection title="Sales Channels">
          <Checkbox
            label="Website Store"
            checked={channels.website}
            onChange={(val) => updateChannel("website", val)}
          />
          <Checkbox
            label="Payment Links"
            checked={channels.paymentLinks}
            onChange={(val) => updateChannel("paymentLinks", val)}
          />
          <Checkbox
            label="Embedded Checkout"
            checked={channels.embedded}
            onChange={(val) => updateChannel("embedded", val)}
          />
        </FormSection>
        
        <FormSection title="Post-Purchase">
          <Input
            label="Thank You Page URL"
            type="url"
            value={thankYouUrl}
            onChange={setThankYouUrl}
            placeholder="https://example.com/thank-you"
          />
          
          <Textarea
            label="Email Template"
            value={emailTemplate}
            onChange={setEmailTemplate}
            placeholder="Custom email to send after purchase..."
          />
        </FormSection>
      </PublishSettings>
    </ProductPreview>
  )}
  
  {/* Navigation Buttons */}
  <StepperFooter>
    <Button
      variant="outline"
      onClick={previousStep}
      disabled={currentStep === 1}
    >
      <ChevronLeft className="w-4 h-4 mr-2" />
      Back
    </Button>
    
    <div className="flex gap-2">
      <Button variant="outline" onClick={saveDraft}>
        Save Draft
      </Button>
      
      {currentStep < 5 ? (
        <Button onClick={nextStep}>
          Next
          <ChevronRight className="w-4 h-4 ml-2" />
        </Button>
      ) : (
        <Button onClick={publishProduct}>
          <Rocket className="w-4 h-4 mr-2" />
          {publishStatus === "active" ? "Publish Now" : "Save Product"}
        </Button>
      )}
    </div>
  </StepperFooter>
</ProductBuilder>
```

═══════════════════════════════════════════════════════════════════
## 💳 STRIPE EMBEDDED CHECKOUT INTEGRATION
═══════════════════════════════════════════════════════════════════

### **Frontend Integration**
```tsx
// components/EmbeddedCheckout.tsx
"use client";

import { useEffect, useState } from "react";
import { loadStripe } from "@stripe/stripe-js";
import {
  EmbeddedCheckoutProvider,
  EmbeddedCheckout,
} from "@stripe/react-stripe-js";

const stripePromise = loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!);

export function EmbeddedCheckoutComponent({ productId }: { productId: string }) {
  const [clientSecret, setClientSecret] = useState("");
  
  useEffect(() => {
    // Fetch client secret from backend
    fetch("/api/stripe/create-checkout-session", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ productId }),
    })
      .then((res) => res.json())
      .then((data) => setClientSecret(data.client_secret));
  }, [productId]);
  
  if (!clientSecret) {
    return <div>Loading checkout...</div>;
  }
  
  return (
    <div className="w-full max-w-2xl mx-auto">
      <EmbeddedCheckoutProvider
        stripe={stripePromise}
        options={{ clientSecret }}
      >
        <EmbeddedCheckout />
      </EmbeddedCheckoutProvider>
    </div>
  );
}
```

### **Payment Links Display**
```tsx
<PaymentLinkManager product={product}>
  <LinkDisplay>
    <Input
      value={product.payment_link_url}
      readOnly
      suffix={
        <>
          <CopyButton onClick={() => copyToClipboard(product.payment_link_url)} />
          <QRCodeButton onClick={() => generateQRCode(product.payment_link_url)} />
        </>
      }
    />
  </LinkDisplay>
  
  <EmbedOptions>
    <Tab label="Button">
      <CodeBlock
        language="html"
        code={`<a href="${product.payment_link_url}" class="buy-button">Buy Now</a>`}
        copyable
      />
    </Tab>
    
    <Tab label="QR Code">
      <QRCode value={product.payment_link_url} size={200} />
      <DownloadButton onClick={downloadQRCode} />
    </Tab>
    
    <Tab label="Social Share">
      <ShareButtons
        url={product.payment_link_url}
        platforms={["twitter", "facebook", "linkedin", "email"]}
      />
    </Tab>
  </EmbedOptions>
</PaymentLinkManager>
```

═══════════════════════════════════════════════════════════════════
## 📊 PRODUCT ANALYTICS (`/products/:id/analytics`)
═══════════════════════════════════════════════════════════════════

```tsx
<ProductAnalytics productId={productId}>
  <AnalyticsHeader>
    <h1>{product.name}</h1>
    <DateRangePicker
      value={dateRange}
      onChange={setDateRange}
      presets={["7d", "30d", "90d", "1y", "all"]}
    />
  </AnalyticsHeader>
  
  <MetricsGrid>
    <MetricCard
      title="Revenue"
      value={formatCurrency(analytics.revenue)}
      change={analytics.revenueChange}
      trend={analytics.revenueTrend}
    />
    <MetricCard
      title="Sales"
      value={analytics.salesCount}
      change={analytics.salesChange}
      trend={analytics.salesTrend}
    />
    <MetricCard
      title="Conversion Rate"
      value={`${analytics.conversionRate}%`}
      change={analytics.conversionChange}
      trend={analytics.conversionTrend}
    />
    <MetricCard
      title="Avg. Order Value"
      value={formatCurrency(analytics.avgOrderValue)}
      change={analytics.aovChange}
      trend={analytics.aovTrend}
    />
  </MetricsGrid>
  
  <ChartsGrid>
    <Chart
      title="Revenue Over Time"
      type="line"
      data={analytics.revenueTimeSeries}
    />
    
    <Chart
      title="Sales by Source"
      type="pie"
      data={analytics.salesBySource}
    />
    
    <Chart
      title="Customer Geography"
      type="map"
      data={analytics.customerLocations}
    />
  </ChartsGrid>
  
  <RecentPurchases>
    <h3>Recent Purchases</h3>
    <PurchaseTable
      purchases={analytics.recentPurchases}
      columns={["Customer", "Amount", "Date", "Status"]}
    />
  </RecentPurchases>
</ProductAnalytics>
```

═══════════════════════════════════════════════════════════════════
## 🔑 KEY FEATURES SUMMARY
═══════════════════════════════════════════════════════════════════

### **Product Builder**
✅ Step-by-step wizard interface  
✅ Multiple product types (digital, collection, course, build, subscription)  
✅ Rich text editor for descriptions  
✅ Image upload & management  
✅ Feature list builder  
✅ Content attachment (files, videos, modules)  
✅ Flexible pricing (one-time, recurring, usage-based, tiered)  
✅ Live preview before publishing  
✅ Draft & schedule support  

### **Stripe Integration**
✅ Embedded Checkout (inline payment form)  
✅ Payment Links (shareable URLs)  
✅ Customer Portal (self-service billing)  
✅ Automatic Tax calculation (Stripe Tax)  
✅ Fraud detection (Stripe Radar)  
✅ Subscription management  
✅ Usage-based billing  
✅ Invoice generation  
✅ Promotion codes  
✅ Webhook handling  

### **Product Management**
✅ Product listing & filtering  
✅ Quick edit & duplicate  
✅ Archive & delete  
✅ Bulk operations  
✅ Analytics & reporting  
✅ Revenue tracking  
✅ Sales performance  

### **Sales Channels**
✅ Website store  
✅ Payment links  
✅ Embedded checkout  
✅ QR codes  
✅ Social sharing  

═══════════════════════════════════════════════════════════════════
## 🎯 IMPLEMENTATION PRIORITY
═══════════════════════════════════════════════════════════════════

**Phase 1 (Week 1):**
1. Product dashboard & listing
2. Basic product creation form
3. Stripe product/price creation
4. Payment link generation

**Phase 2 (Week 2):**
5. Embedded Checkout integration
6. Product content management
7. Image upload & storage
8. Preview functionality

**Phase 3 (Week 3):**
9. Advanced pricing options
10. Subscription support
11. Customer Portal
12. Analytics dashboard

**Phase 4 (Week 4):**
13. Collection builder
14. Course creator
15. Custom build integration
16. Webhook handling
17. Tax & fraud detection

**Total Time:** 4 weeks for complete product builder

═══════════════════════════════════════════════════════════════════

