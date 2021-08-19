function showFinalResult(data){
    console.log(data.resultCode);
    console.log(data);
    document.getElementById ("title").style.display = "none";
    switch (data.resultCode) {
			case "Authorised":
				window.location.href = "/result/success";
				break;
			case "Pending":
			case "Received":
				window.location.href = "/result/pending";
				break;
			case "Refused":
				window.location.href = "/result/failed";
				break;
			default:
				window.location.href = "/result/error";
				break;
	}
};