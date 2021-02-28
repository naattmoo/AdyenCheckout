function showFinalResult(data){
    console.log(data.resultCode);
    console.log(data);
    document.getElementById ("title").style.display = "none";
    switch (data.resultCode) {
  case 'Authorised':
    dropin.setStatus('success', { message: 'Payment successful!' });
    break;
  case 'Error':
    dropin.setStatus('error', { message: 'Something went wrong.' + data.refusalReason});
    break;
  case 'Pending':
  case 'PresentToShopper':
  case 'Received':
    dropin.setStatus('loading', { message: 'You will receive the final result of the payment in an AUTHORISATION notification.'}); // start the loading state
    break;
  case 'Refused':
    dropin.setStatus('error', { message: 'The payment was refused. '+data.refusalReason+'. Try with a different payment method or card.'});
    break;
  default:
    break;
};

};