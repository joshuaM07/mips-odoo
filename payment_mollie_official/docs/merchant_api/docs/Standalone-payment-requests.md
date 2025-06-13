# Standalone payment requests

## Introduction

### General concept

The endpoint documentation is here: ([doc here)](https://mips.stoplight.io/docs/merchant-api/b3A6MzcwNTIyMjE-create-payment-request)

- A payment request results in the creation of a payment page.
- The payment page is a standalone page where the client can pay.
- The payment page shows automatically the relevant data related to the payment.
- The payment page URL is given to the merchant as a https link and a QR code.
- The payment page can be whitelabeled
- The payment result is sent through a callback **only** when a successful payment is done by the client.
- The payment result (IMN callback) contains the unique order ID used by the merchant on the payment request creation.

*The following steps are high level steps for this specific use case. Please read the complete API Doc to understand the adequate flows and related parameters (Authentify, etc.)*

**Example of a generated payment page**

![image.png](https://stoplight.io/api/v1/projects/cHJqOjEwODA5NQ/images/GdRQKHExorM)

### Whitelabelling of the payment page

The payment page can be whitelabeled to the merchant's corporate branding. The whitelabeling is made upfront on the account set up of the merchant

- logo, banner and colors
- payment base URL (subdomain.yourdomain.ext). Example: pay.mycompany.com
- email sender if the automatic "mail" option is selected. Example: myname@mycompany.com

The response URL can be sent to your client by the merchant's own means. When the client clicks 

### Special cases (Tokenization)

In some special cases, the payment page can be considered as a Tokenization page (Means of payment memorization). Depending on the case, the payment page can at the same time:

- Take a payment
- Memorize (Tokenize) the mean of payment.

In thoses use cases, a Claim Payment Request API is available. ([Doc here](https://mips.stoplight.io/docs/merchant-api/b3A6MzcwNTIyMjM-claim-payment-request))

Applicable cases are 

- "Warranty" mode
- "Deposit / Auto Balance" mode
- "Extra Billing System" mode (EBS)
- "On Demand Recurring Payment" (ODRP) mode

### Get back a payment result (notification)

The payment result is triggered **only** upon a successful payment. MiPS name it an **IMN Notification** (Instant Merchant Notification).

Documentation of IMN callback is [here](https://mips.stoplight.io/docs/merchant-api/b3A6Mzc0MDg5OTk-imn-callback-architecture).

## Get a payment link

**Summury**

- A standalone payment page is created upon API call by MiPS
- The page URL is given back to the merchant 
- The QR code with the link is given back to the merchant (in PNG base64 encoded)
- When the payment is made by the client, MiPS sends a notification to an URL given by the merchant (IMN Callback)

**Possible usages**

- The merchant wants to send himself the link to his client
- The merchant wants to embed a payment link to his PDF or HTML invoices.
- The merchant wants to show a payment QR code in his invoices.

**High level flow**


**Steps to follow**

- Create payment request
![image.png](https://stoplight.io/api/v1/projects/cHJqOjEwODA5NQ/images/Sz9HedeBOMg)

- use "simple" as "request_mode

![image.png](https://stoplight.io/api/v1/projects/cHJqOjEwODA5NQ/images/ymL8uXQmStM)

- The response contains the url and the QR code
![image.png](https://stoplight.io/api/v1/projects/cHJqOjEwODA5NQ/images/ViKnLz9L36Y)

## Add a warranty security

**Summury**

The merchant can add a warranty option to his ticket or create a pure warranty ticket. 
The client will be informed on the generated payment page that, over and above the order he is paying for, the merchant reserves the right to take another one shot according to his general conditions. The means of payment will be tokenized. The merchant can claim his warranty either through the MiPS back office, either through the claim_warranty API.

*The warranty payment page is autopopulated:*

![image.png](https://stoplight.io/api/v1/projects/cHJqOjEwODA5NQ/images/7PoREZ3NJPk)

**Possible usages**

- The merchant wants to be able to debit an amount from the client if he leaves without paying.
- A hotel or a car rental company who wants to take an unpaid bill after client has left

**Steps to follow**

- create a payment request as in "simple" mode

- use "warranty" mode, max_date is compulsory. No claim will be available after that date.

![image.png](https://stoplight.io/api/v1/projects/cHJqOjEwODA5NQ/images/McPtArP1In0)

- Get back the link and QR code same as "simple" mode.
- Claim the Warranty if needed with the Claim Payment Request API (Doc [here](https://mips.stoplight.io/docs/merchant-api/b3A6MzcwNTIyMjM-claim-payment-request)) by sending back the received Token after a successfull payment

![image.png](https://stoplight.io/api/v1/projects/cHJqOjEwODA5NQ/images/SktH3VSu9tY)

## Create a deposit / Autobalance request

**Summury**

The merchant can ask for a paid deposit and specify the balances he will take automatically on specific conditions.
The deposit is immediately debited and the balances are debited either automatically on a specific date, or manually by API or by clicking on the take balance in the MiPS merchant back office.

*The Deposit/Balance page is autopopulated:*

![image.png](https://stoplight.io/api/v1/projects/cHJqOjEwODA5NQ/images/cmiwLYvVlnU)


**Possible usages**

- The merchant wants to levy the total money due by installments

**Steps to follow**

- create a payment request as in "simple" mode
- use "deposit" mode

![image.png](https://stoplight.io/api/v1/projects/cHJqOjEwODA5NQ/images/pgzyoRGgYfA)

- Insert a deposit amount and create an array of balances

![image.png](https://stoplight.io/api/v1/projects/cHJqOjEwODA5NQ/images/gsZzmwVZJy0)


- Get back the link and same as "simple" mode.
- Claim the balances if needed with the Claim Payment Request API ([Doc here](https://mips.stoplight.io/docs/merchant-api/b3A6MzcwNTIyMjM-claim-payment-request)) by sending back the received Token. Or claim the balance through the backoffice. Or the balance is debited automatically by MiPS at a given date for auto balances.

![image.png](https://stoplight.io/api/v1/projects/cHJqOjEwODA5NQ/images/GL0h8ut5NnE)


## ODRP (On Demand Recurring Payment)

**summury**

The client will be informed on the generated payment page that, over and above the order he is paying for, the merchant reserves the right to take any payment within the specified limits, according to his general conditions.

The means of payment will be tokenized. The merchant can claim a payment either through the MiPS back office, either through the Claim Payment Request API.

**Possible usages**

- Any merchant who wants to have a better liberty on how to leverage his clients himself.
- Any of the previous modes (warranty, deposit/ballance, ebs) can be emulated with "odrp", allowing the merchant to adapt the flows at his conveniance.
- The merchant can manage his own wallets and initiate a payment by any possible trigger he has (NFC wristbands, NFC cards, etc.)

**Steps to follow**

- create a payment request as in "simple" mode
- select the "odrp" mode

![image.png](https://stoplight.io/api/v1/projects/cHJqOjEwODA5NQ/images/HfpPEmddYGc)

- max_amount_per_claim and max_frequency are compulsory. It will show to the client the max claims the Merchant can take.
- Get back the link and same as "simple" mode.
- Claim payments if needed with the Claim Payment Request API ([Doc here](https://mips.stoplight.io/docs/merchant-api/b3A6MzcwNTIyMjM-claim-payment-request)) by sending back the received Token.

![image.png](https://stoplight.io/api/v1/projects/cHJqOjEwODA5NQ/images/GL0h8ut5NnE)

## AutoSend the payment request by mail

**Summury**

- The created request can be sent by mail automatically by MiPS.
- All request_mode are eligible to the automail feature
- The email content is auto generated by MiPS
- The email subject is equal to the order_title
- The client is called by his name in the email
- the email of the client is compulsory

![image.png](https://stoplight.io/api/v1/projects/cHJqOjEwODA5NQ/images/COPVyTdC5ek)


**High level flow**


**Steps to follow**

*The folowwing steps are high level steps for this specific use case. Please read the complete API Doc to understand the adequate flows and related parameters (Authentify, etc.)*

- Same steps as previous one but with "sending_mode" set to "mail"

![image.png](https://stoplight.io/api/v1/projects/cHJqOjEwODA5NQ/images/CYCvtVwilZY)


### Whitelabeling of the email

- The merchant can change the look and content of the autogenerated email in his MiPS back office

![image.png](https://stoplight.io/api/v1/projects/cHJqOjEwODA5NQ/images/gt09xy4IV9M)


- The sender can be whitelabeled on account creation (myname@mycompany.com)


