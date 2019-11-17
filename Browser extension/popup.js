/* SLIDER BUTTON */
document.addEventListener('DOMContentLoaded', function() {
    var activateButton = document.querySelector('input[type="checkbox"]');
    activateButton.addEventListener('change', function() {
        if (activateButton.checked) {
            btnSource.style.display = "inline-block";
            sendToBlock.style.display = "inline-block";
        } else {
            btnSource.style.display = "none";
            sendToBlock.style.display = "none";
        }
    }, false);
  }, false);
    
  
/* GET and SEND buttons */
document.addEventListener('DOMContentLoaded', function() {
  var btnSource = document.getElementById('btnSource');
  btnSource.addEventListener('click', function() {
    getResults(); 
  }, false);
}, false);

document.addEventListener('DOMContentLoaded', function() {
  var sendToBlock = document.getElementById('sendToBlock');
  sendToBlock.addEventListener('click', function() {
    networkSend();
  }, false);
}, false); 


/* Gets the email data */
function getResults(){
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        chrome.tabs.sendMessage(tabs[0].id, { action: "getEmailData" }, function (response) {
           console.log("DONE");
        });
    });
}


/* Executes content.js which will send data to blockchain*/
function networkSend(){
chrome.tabs.executeScript(null, {file: "content.js"});
};
