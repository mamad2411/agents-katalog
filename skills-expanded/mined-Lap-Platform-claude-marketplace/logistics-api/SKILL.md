---
name: logistics-api
description: "Logistics API skill. Use when working with Logistics for shipment, shipping_quote. Covers 6 endpoints."
version: 1.0.0
generator: lapsh
---

# Logistics API
API version: v1_beta.0.0

## Auth
OAuth2

## Base URL
https://api.ebay.com/sell/logistics/v1_beta

## Setup
1. Configure auth: OAuth2
2. GET /shipment/{shipmentId}/download_label_file -- verify access
3. POST /shipment/{shipmentId}/cancel -- create first cancel

## Endpoints

6 endpoints across 2 groups. See references/api-spec.lap for full details.

### shipment
| Method | Path | Description |
|--------|------|-------------|
| POST | /shipment/{shipmentId}/cancel | This method cancels the shipment associated with the specified shipment ID and the associated shipping label is deleted. When you cancel a shipment, the <b>totalShippingCost</b> of the canceled shipment is refunded to the account established by the user's billing agreement.  <br><br>Note that you cannot cancel a shipment if you have used the associated shipping label. |
| POST | /shipment/create_from_shipping_quote | This method creates a shipment based on the <b>shippingQuoteId</b> and <b>rateId</b> values supplied in the request. The rate identified by the <b>rateId</b> value specifies the carrier and service for the package shipment, and the rate ID must be contained in the shipping quote identified by the <b>shippingQuoteId</b> value. Call <b>createShippingQuote</b> to retrieve a set of live shipping rates.<br><br><span class="tablenote"><b>Note:</b> The Logistics API only supports USPS shipping rates and labels.</span><br/>When you create a shipment, eBay generates a shipping label that you can download and use to ship your package.<br/><br/>In a <b>createFromShippingQuote</b> request, sellers can include a list of shipping options they want to add to the base service quoted in the selected rate. The list of available shipping options is specific to each quoted rate and if available, the options are listed in the rate container of the shipping quote.<br/><br/>In addition to a configurable return-to location and other details about the shipment, the response to this method includes:<ul><li>The shipping carrier and service to be used for the package shipment</li><li>A list of selected shipping options, if any</li><li>The shipment tracking number</li><li>The total shipping cost (the sum cost of the base shipping service and any added options)</li></ul>When you create a shipment, your billing agreement account is charged the sum of the <b>baseShippingCost</b> and the total cost of any additional shipping options you might have selected. Use the URL returned in <b>labelDownloadURL</b> field, or call <b>downloadLabelFile</b> with the <b>shipmentId</b> value from the response, to download a shipping label for your package.<br/><br/><div class="msgbox_important"><p class="msgbox_importantInDiv" data-mc-autonum="&lt;b&gt;&lt;span style=&quot;color: #dd1e31;&quot; class=&quot;mcFormatColor&quot;&gt;Important! &lt;/span&gt;&lt;/b&gt;"><span class="autonumber"><span><b><span style="color: #dd1e31;" class="mcFormatColor">Important!</span></b></span></span> Sellers must set up their payment method before they can use this method to create a shipment and the associated shipping label.</p></div><h3 id="ba">Set up a billing agreement</h3>Prior to using this method to create a shipment, sellers must first set up their billing agreement. Failure to do so will return <code>Error 90030 Payment could not be completed.</code><br/><br/>The preferred method for sellers to set up their billing agreement is to go to <a href="https://gslblui.ebay.com/gslblui/payments " target="_blank">Set up billing agreement</a> and follow the on-screen directions.<br/><br/>Alternatively, sellers can do the following:<ul><li>Go to https://www.ebay.com/ship/single/{order_id}, where {order_id} is that of the order for which the label is being printed.</li><li>When prompted, select <b>PayPal</b>.</li><li>Verify that <b>Save PayPal for future purchases</b> is selected.</li><li>Click <b>Set up Payments</b> which will open PayPal in a pop-up window.</li><li>Log in using <i>PayPal credentials</i>, and then follow the on-screen prompts to set up the billing agreement.</li><li>Once the agreement has been set up, sellers can leave this page as there is no need to actually print a label.</li></ul> |
| GET | /shipment/{shipmentId}/download_label_file | This method returns the shipping label file that was generated for the <b>shipmentId</b> value specified in the request. Call <b>createFromShippingQuote</b> to generate a shipment ID.<br><br><span class="tablenote"><b>Note:</b> The Logistics API only supports USPS shipping rates and labels.</span><br>Use the <code>Accept</code> HTTP header to specify the format of the returned file. The default file format is a PDF file. <!-- Are other options available? --> |
| GET | /shipment/{shipmentId} | This method retrieves the shipment details for the specified shipment ID. Call <b>createFromShippingQuote</b> to generate a shipment ID. |

### shipping_quote
| Method | Path | Description |
|--------|------|-------------|
| POST | /shipping_quote | The <b>createShippingQuote</b> method returns a <i>shipping quote </i> that contains a list of live "rates."  <br><br>Each rate represents an offer made by a shipping carrier for a specific service and each offer has a live quote for the base service cost. Rates have a time window in which they are "live," and rates expire when their purchase window ends. If offered by the carrier, rates can include shipping options (and their associated prices), and users can add any offered shipping option to the base service should they desire.  Also, depending on the services required, rates can also include pickup and delivery windows.<br><br><span class="tablenote"><b>Note:</b> The Logistics API only supports USPS shipping rates and labels.</span><br>Each rate is for a single package and is based on the following information: <ul><li>The shipping origin</li> <li>The shipping destination</li> <li>The package size (weight and dimensions)</li></ul>  Rates are identified by a unique eBay-assigned <b>rateId</b> and rates are based on price points, pickup and delivery time frames, and other user requirements. Because each rate offered must be compliant with the eBay shipping program, all rates reflect eBay-negotiated prices.  <br><br>The various rates returned in a shipping quote offer the user a choice from which they can choose a shipping service that best fits their needs. Select the rate for your shipment and using the associated <b>rateId</b>, call <b>createFromShippingQuote</b> to create a shipment and generate a shipping label that you can use to ship the package. |
| GET | /shipping_quote/{shippingQuoteId} | This method retrieves the complete details of the shipping quote associated with the specified <b>shippingQuoteId</b> value.  <br><br>A "shipping quote" pertains to a single specific package and contains a set of shipping "rates" that quote the cost to ship the package by different shipping carriers and services. The quotes are based on the package's origin, destination, and size.  <br><br>Call <b>createShippingQuote</b> to create a <b>shippingQuoteId</b>. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a cancel?" -> POST /shipment/{shipmentId}/cancel
- "Create a create_from_shipping_quote?" -> POST /shipment/create_from_shipping_quote
- "List all download_label_file?" -> GET /shipment/{shipmentId}/download_label_file
- "Get shipment details?" -> GET /shipment/{shipmentId}
- "Create a shipping_quote?" -> POST /shipping_quote
- "Get shipping_quote details?" -> GET /shipping_quote/{shippingQuoteId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
