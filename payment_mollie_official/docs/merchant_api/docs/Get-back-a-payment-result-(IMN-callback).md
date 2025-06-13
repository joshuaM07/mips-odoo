# Get back a payment result (IMN callback)

## Steps

[(Documentation is here)](https://docs.mips.mu/docs/merchant-api/ba8c3e425436b-imn-callback-architecture)

IMPORTANT: THIS CALLBACK IS MADE FROM MIPS TO THE MERCHANT. THE URL IS TO BE CALLED ON THE MERCHANT'S SERVER

![image.png](https://stoplight.io/api/v1/projects/cHJqOjEwODA5NQ/images/rQMWVEiOBsY)

- The IMN URL is called by MiPS upon successful payment.
- The IMN URL is to be hosted on Merchant's server.
- The IMN URL is called in POST mode with tracking IDs. Doc here.
- The crypted callback contains the unique order ID used by the merchant on the payment request creation + other data.

![image.png](https://stoplight.io/api/v1/projects/cHJqOjEwODA5NQ/images/4tyLdHzoE0Y)

- The IMN callback must be decrypted by the merchant using the "decrypt_imn_data" API endpoint

![image.png](https://stoplight.io/api/v1/projects/cHJqOjEwODA5NQ/images/9XvD52irVyk)

- The IMN must echo (print) either "success" or "fail"

![image.png](https://stoplight.io/api/v1/projects/cHJqOjEwODA5NQ/images/Kqmn4wItets)

## Decrypting the IMN data

- MiPS provides the merchant with a special salt and cipher key to send in each IMN decryption.

![image.png](https://stoplight.io/api/v1/projects/cHJqOjEwODA5NQ/images/TAm1BMadcjo)

- send along the received crypted data.

- The merchant receives back all the payment data needful to operate. The token is also sent if the initial request was a Tokenized one (ODRP, warranty, EBS, deposit, etc.)

![image.png](https://stoplight.io/api/v1/projects/cHJqOjEwODA5NQ/images/j8Lm7MpGkSc)
