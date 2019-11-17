var body, subject, email;
chrome.storage.sync.get('body', function(data){
	//console.log(data.body);	
	body = data.body;
});

chrome.storage.sync.get('subject', function(data){
	//console.log(data.subject);
		subject = data.subject;
});

chrome.storage.sync.get('email', function(data){
	//console.log(data.email);
	email = data.email;
});
var xhr = new XMLHttpRequest();
xhr.open("POST", "http://localhost:2525", true);
xhr.setRequestHeader('Content-Type', 'application/json');
xhr.send(JSON.stringify({
    email: email,
    subject: subject,
    body: body
}));
