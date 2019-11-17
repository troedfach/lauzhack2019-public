// listen for getEmailData request, call getEmailData() which stores the data in chrome 
chrome.runtime.onMessage.addListener(
    function (request, sender, sendResponse) {
        if (request.action === "getEmailData") {
            getEmailData(request, sender, sendResponse);           
        }
    }
);

function getEmailData(request, sender, sendResponse){
	//Subject
	var subject = document.querySelector('input[name="subject"]').value;
	
    //EmailDest
	var emailDest = document.querySelectorAll("div.vR")[0].innerText; // just use a single receiving email for now
	
	//Body Text
	var body = document.querySelector('[contenteditable]').textContent;
	console.log(body);
   
   chrome.storage.sync.set({'body': body}, function(){	   
	  console.log("Stored Body"); 	   
   });
   chrome.storage.sync.set({'subject': subject}, function(){	   
	  console.log("Stored Subject"); 	   
   });
   chrome.storage.sync.set({'email': emailDest}, function(){	   
	  console.log("Stored Email"); 	   
   });
   
}



