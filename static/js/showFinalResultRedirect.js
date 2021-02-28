console.log(resultCode);
    switch (resultCode) {
  case 'Authorised':
    document.getElementById("result_img").src="https://checkoutshopper-test.adyen.com/checkoutshopper/images/components/success.svg";
    document.querySelector('.result_text').innerHTML = 'Payment successful!';
    break;
  case 'Error':
    document.getElementById("result_img").src="https://checkoutshopper-test.adyen.com/checkoutshopper/images/components/error.svg";
    document.querySelector('.result_text').innerHTML = 'Something went wrong.';
    break;
  case 'Refused':
    document.getElementById("result_img").src="https://checkoutshopper-test.adyen.com/checkoutshopper/images/components/error.svg";
    document.querySelector('.result_text').innerHTML = 'The payment was refused. Try with a different payment method or card.';
    break;
  default:
    break;
};
