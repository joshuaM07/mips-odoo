# In-App Module Integration

## Steps to load the iframe :

1. Create the Class that will redirect user to the success page
2. Generate the Payment URL
3. Generate the Web View using the above Payment URL
4. Enable Javascript usage within Web view
5. Link Webview to class which will redirect to Success page (Created in Step 1). KEEP “JSInterface” as is, do not change.
6. Load the Web View
7. The Payment Interface will automatically appear in the webview : Note that it will be automatically configured (look & feel, auto bankrouting, means of payments, etc.)

## Details:

### Step 1 :  (JAVA example) Create the Class and the Context that will redirect user to the success page

Create a class like this:

```json
public class JavaScriptInterface {
    Context mContext;

    /** Instantiate the interface and set the context */
    JavaScriptInterface(Context c) {
        mContext = c;
    }

    @JavascriptInterface
    public void ResultFromWebview(bool toast) {
        if(toast === true)
        {
              //Redirect to success
        }
    }
}
```

### Step 2: Generate the Payment URL [(API endpoint here)](https://mips.stoplight.io/docs/merchant-api/a4cae076c9b7e-load-payment-zone)

The following is pseudo code. You can adapt to any language.

```json
//Only these 3 data are dynamic and may change on your side
$id_order = 'ord_5125';	// your generated order id, must be unique
$amount = 1.00;  	
$currency = 'MUR';		// possibilities : MUR, USD, GBP, EUR, ZAR

/***Do not change***/
$id_merchant = 'YOUR ID MERCHANT - MIPS WILL PROVIDE';
$id_form = 'YOUR ID FORM - MIPS WILL PROVIDE';
$id_operator = 'YOUR OPERATOR ID - MIPS WILL PROVIDE';
$operator_password = 'YOUR OPERATOR PASSWORD - MIPS WILL PROVIDE';
/***Do not change***/

$complete_array_message = [
	'id_merchant' => $id_merchant,
	'id_entity' => $id_entity,
	'id_operator' => $id_operator,
	'operator_password' => $perator_password,
	'request_mode'=>'simple',
	'touchpoint'=>native_app,
	'order' =>[
		'id_order' => $id_order,
		'amount'=>$amount, // amount in float
		'currency'=> $currency, //MUR,EUR,USD,ZAR,MGA
	],
	'iframe_behavior' =>[
		'custom_redirection_url'=>'',//Can be null, or must be without https:// -> ex: www.google.com
		'height'=>508,//Height of the iframe. Can be null
		'width'=>450,//Width of the Iframe. Can be null
		'language'=>'EN' //EN or FR
	]
];

$curl = curl_init();
$curl_opt = [
    CURLOPT_URL 		=> 'https://api.mips.mu/api/load_payment_zone',
    CURLOPT_USERAGENT 		=> 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36',
    CURLOPT_RETURNTRANSFER 	=> 1,
    CURLOPT_FOLLOWLOCATION 	=> false,
    CURLOPT_FORBID_REUSE 	=> true,
    CURLOPT_FRESH_CONNECT 	=> true,
    CURLOPT_VERBOSE         	=> 1,
    CURLOPT_SSL_VERIFYPEER 	=> true,
    CURLOPT_POST 		=> true,
    CURLOPT_POSTFIELDS 		=> json_encode($complete_array_message),
    CURLOPT_HTTPHEADER 		=> [
      'Authorization: Basic ' . base64_encode('MIPS WILL PROVIDE:MIPS WILL PROVIDE'),
      'Cache-Control: no-cache'
    ]
];
curl_setopt_array($curl,$curl_opt);
$response = curl_exec($curl);
$response = json_decode($response,true);
$final_url = $response['answer']['payment_zone_data'];
```

### Step 3: Generate the WebView using the above Payment URL ($final_url)

If your dev language is Java please refer to this URL for simple integration-> <https://developer.android.com/guide/webapps/webview.html>

```json
//***** Load the WebView here according to the language you are using *******
//*****IMPORTANT: You must adapt the following pseudo code to your own developing language
//***** Please refer to official documentation -> https://developer.android.com/guide/webapps/webview.html
WebView myWebView = (WebView) findViewById(R.id.webview); 
```

### Step 4: Enable Javascript usage within WebView

```json
WebSettings webSettings = myWebView.getSettings();
webSettings.setJavaScriptEnabled(true);
```

### Step 5: Link WebView to class which will redirect to Success page (Created in Step 1). KEEP “JSInterface” as is, do not change.

```json
webView.addJavascriptInterface(new JavaScriptInterface(this), "JSInterface"); 
```

### Step 6: Load the WebView

```json
myWebView.loadUrl("$final_url ");
```

### Step 7: The Payment Interface will automatically appear in the WebView

1. The following parameters will be included in the link via one encrypted parameter : one order id, the amount to be paid in cents and the currency (MUR)
2. With these parameters, the payment module will be able to load. The client will be able to enter his/her Credit/Debit Card informations (Card number, expiration date, CVV)
3. Our system will process the payment, we will then send a notification in a background server to server process on an URL that you will send to us. The URL will contain the code in PART 3 ‘Getting back the payment result’. It is there that you will update your database with the order status that we will send to you.
4. The user can be redirected where you want with the creation of listener described in different step previously. On our side the function will be called as follows in JavaScript:

```json
JSInterface.ResultFromWebview(true);
```

### Help:

<https://stackoverflow.com/questions/11752052/passing-data-from-java-class-to-web-view-html/11752319#11752319>

<https://developer.android.com/guide/webapps/webview.html#BindingJavaScript>

Depending on the language you are using, please visit some documentation that may help on creating a WebView and binding a JavaScript function to a WebView
For iOS adaptation of Screen Redirection, here is a method: <https://stackoverflow.com/questions/37356596/uiwebview-and-javascriptinterface-in-swift/37373745#37373745>
