function makePayment(data, origin){
    console.log(data);
    data.origin=origin;
    console.log(data);

    let request = new XMLHttpRequest();
    return new Promise(function(resolve, reject) {
     request.open("POST",
                 "/makePayment" ,
                 true
                 );
     request.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
     //request.setRequestHeader('Access-Control-Allow-Origin','*');
	 request.responseType = 'json';
	 request.onload = function () {
     if (request.readyState === request.DONE) {
        if (request.status === 200) {
            resolve(request.response);
            console.log(request.response);
        }
    }
};
    request.send(JSON.stringify(data));
  });
};