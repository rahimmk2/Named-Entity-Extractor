const server_addr = 'http://localhost:8888'

window.onload = function () {
	btn = document.getElementById("highlight-btn");
	btn.addEventListener("click", handler);
}

function main_fn(tab) {
	request = {
		method: 'POST',
		body: JSON.stringify({ url: tab.url }),
		headers: { 'Content-Type': 'application/json' }
	}

	fetch(server_addr, request)
		.then(response => response.json())
		.then(handleData);

	function handleData(data) {
		chrome.tabs.sendMessage(tab.id, data)
	}
}

function handler() {
	chrome.tabs.query(
		{ active: true, currentWindow: true },
		(tabs) => { main_fn(tabs[0]) }
	);
}

