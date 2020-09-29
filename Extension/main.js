//Creating Elements
//var btn = document.createElement("BUTTON")
//var t = document.createTextNode("CLICK ME");
//btn.appendChild(t);
//Appending to DOM 
//document.body.appendChild(btn);

fetch('https://gentle-sea-38259.herokuapp.com/')
  .then((data) => {
    console.log(data);
  });

const t = document.body.children.item(5).children.item(1);
const div = document.createElement('div');
div.className = "flex-container";
div.style.display="flex";
div.style.flexDirection="column";
div.style.paddingBottom = "50px";

const dict = {

"'Latent reserves' within the Swiss NFI":"https://search.earthdata.nasa.gov/search/granules?p=C1931110427-SCIOPS",

"(U-Th)/He ages from the Kukri Hills of southern Victoria Land":"https://search.earthdata.nasa.gov/search/granules?p=C1214587974-SCIOPS"

};



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