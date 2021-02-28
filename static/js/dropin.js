 const configuration = {
 paymentMethodsResponse: paymentsMethods ,
 clientKey: clientKey,
 locale: "en-US",
 environment: "test",
 onSubmit: (state, dropin) => {
            console.log(state);
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
     holderNameRequired: true,
     enableStoreDetails: false,
     hideCVC: false, // Change this to true to hide the CVC field for stored cards
     name: 'Credit or debit card',
     billingAddressRequired: true
   }
 }
};

const checkout = new AdyenCheckout(configuration);
const dropin = checkout.create('dropin').mount('#dropin-container');

