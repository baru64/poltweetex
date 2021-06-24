const url = "https://poltweetex.northeurope.cloudapp.azure.com";
async function checkBackend() {
    let response = await fetch(url);
    let testbox = document.getElementById('testbox');
    if (response.ok) {
      let respjson = await response.json();
      testbox.innerHTML = JSON.stringify(respjson);
    } else {
      testbox.innerHTML = "response is not ok";
    }
}
checkBackend();
