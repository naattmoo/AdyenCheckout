const clientKey = JSON.parse(document.getElementById('clientKey').innerHTML);
const type = JSON.parse(document.getElementById('integration-type').innerHTML);
const paymentsMethods = JSON.parse(document.getElementById('paymentsMethods').innerHTML);
var payData;
async function initCheckout() {
	try {
         const configuration = {
         paymentMethodsResponse: paymentsMethods,
         showPayButton: true,
         clientKey: clientKey,
         originKey: "pub.v2.8216209033662207.aHR0cDovL2xvY2FsaG9zdDo4MDAw.qZCAfiQuZ9N-xULgyaqjdXPB-geAEkaHlF0kXEqT1CQ",
         locale: "es-ES",
         environment: "test",
         configuration: {
            gatewayMerchantId: "MerchantTestNatalia"
          },

         onSubmit: (state, dropin) => {
           console.log(state.data);
           console.log(dropin);

                    makePayment(state.data, window.location.origin).then(response => {
                    console.log(response);
                 if (response.action) {

                    if(response.action.type=="redirect"){
                        console.log(response.action.paymentMethodType)
                        dropin.handleAction(response.action)

                        }

                    else{
                        dropin.handleAction(response.action);
                    }
                   // Drop-in handles the action object from the /payments response

                 } else {
                   // Your function to show the final result to the shopper
                   showFinalResult(response);
                 }
               })
               .catch(error => {
                 throw Error(error);
               });
           },
         onAdditionalDetails: (state, dropin) => {
           // Your function calling your server to make a `/payments/details` request
           console.log(JSON.stringify(state));
           makeDetailsCall(state.data)
             .then(response => {
               if (response.action) {
                   dropin.handleAction(response.action);
               } else {
                 // Your function to show the final result to the shopper
                 showFinalResult(response);
               }
             })
             .catch(error => {
               throw Error(error);
             });
         },
         paymentMethodsConfiguration: {
           card: { // Example optional configuration for Cards
             hasHolderName: true,
             holderNameRequired: false,
             enableStoreDetails: true,
             hideCVC: false , // Change this to true to hide the CVC field for stored cards
             name: '',
              onBinLookup: (binLookUpInfo) =>{
         console.log(JSON.stringify(binLookUpInfo));
         },
         onBinValue:(binValueInfo) =>{
         console.log(JSON.stringify(binValueInfo));
         },
             billingAddressRequired: true,
             styles: {
        base: {
                fontFamily: "neue-haas-grotesk-medium"
            },
            placeholder: {
                fontFamily: "neue-haas-grotesk-medium"
            }
      }
           },
           storedCard: {
            hideCVC: false

           },
            threeDS2: { // Web Components 4.0.0 and above: sample configuration for the threeDS2 action type
              challengeWindowSize: '05'
               // Set to any of the following:
               // '02': ['390px', '400px'] -  The default window size
               // '01': ['250px', '400px']
               // '03': ['500px', '600px']
               // '04': ['600px', '400px']
               // '05': ['100%', '100%']
        },
           paypal: {
     //merchantId: 'V8ZBCTZ2DHQ72',
     environment: "test", // Change this to "live" when you're ready to accept live PayPal payments
       countryCode: "NL", // Only needed for test. This will be automatically retrieved when you are in production
       amount: {
            currency: "EUR",
            value: 1000
       }
       //,
       //style: { // Example optional configuration for PayPal.
       //       color: 'blue',
       //layout:'vertical'
       //}
       } ,
           applepay: {
        amount: {
            value: 1000,
            currency: "EUR"
        },
        countryCode: "ES",
        onSubmit: (state) => {
          // Call your server to make `/payments` request
         makePayment(state.data, window.location.origin)
            .then(response => {
              // Your function to show the final result to the shopper
              showFinalResult(response);
            })
            .catch(error => {
              throw Error(error);
            });
        }
      },
          amazonpay: { // Optional configuration for Amazon Pay
                    currency: 'EUR',
                    environment: 'test',
                    returnUrl: 'https://localhost:8000/process_payment',
                    amount:{ value: 1000, currency: 'EUR' }
                },
         paywithgoogle: { //Example required configuration for Google Pay
           environment: "TEST", //Change this to PRODUCTION when you're ready to accept live Google Pay payments
           amount: {
             currency: "EUR",
             value: 1000
           },
           //allowedAuthMethods:['PAN_ONLY'],
           //onSubmit:(state) => {console.log(state)
           //},
           countryCode: "NL",
           buttonType:"plain",
           //buttonColor: "white", //Optional. Use a white Google Pay button.
           //For other optional configuration, see section below.
           emailRequired : true,
           shippingAddressRequired:true,
           billingAddressRequired:true,
           billingAddressParameters: {"format": "FULL", "phoneNumberRequired":true},
           //onAuthorized:(paymentData) => {
           //console.log(paymentData);
           //}
           }
           }
        };

        const checkout = await AdyenCheckout(configuration);
        const dropin = checkout.create(type).mount('#dropin-container');


    if(type=='card'){

        const storedPaymentMethod = checkout.paymentMethodsResponse.storedPaymentMethods;
        console.log(storedPaymentMethod);
        for(i=0;i<storedPaymentMethod.length; i++){
            const cabecera=document.createElement('div');
            cabecera.id='stored';
            const newContent = document.createTextNode(storedPaymentMethod[i].lastFour);
            cabecera.appendChild(newContent);
            const div = document.createElement('div');
            div.id='stored-card'+i.toString();
            cabecera.appendChild(div);
            document.body.appendChild(cabecera);
            storedPaymentMethod[i].hideCVC=true;
            const card = checkout.create(type,storedPaymentMethod[i]).mount("#stored-card"+i.toString());
        }
    }

    } catch (error) {
		console.error(error);
		alert("Error occurred. Look at console for details");
	};
};

initCheckout();

