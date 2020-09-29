const t = document.body.children.item(5).children.item(1);
const div = document.createElement('div');
div.className = "flex-container";
div.style.display="flex";
div.style.flexDirection="column";
div.style.paddingBottom = "50px";


fetch('https://gentle-sea-38259.herokuapp.com/', {
  method: 'POST',
  headers: {
    'Content-Type': 'text/plain'
  },
  body: document.URL
});)
  .then(data => data.json())
  .then(dict => {
const para = document.createElement("P");

if (Object.keys(dict).length === 0) {
	para.innerHTML = "Relevant datasets: None";
} else {
	para.innerHTML = "Relevant datasets:";
}


div.appendChild(para);


for (const [key, value] of Object.entries(dict)) {
	const a = document.createElement('a');
	const linkText = document.createTextNode(key);
	a.appendChild(linkText);
	a.title = key;
	a.href = value;
	a.target = "_blank";

	div.appendChild(a);
}

t.insertBefore(div, t.children.item(1));
});

