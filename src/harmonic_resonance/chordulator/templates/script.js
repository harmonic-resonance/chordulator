var urls = {{ files_with_titles|tojson }};
var index = 0;
var sectionIndex = 0;

function previous() { if (index > 0) { index--; update(); } }
function next() { if (index < urls.length - 1) { index++; update(); } }

var iframe = document.getElementById('iframe');
function scrollSection(dir) {
  iframe.contentWindow.postMessage({ action: 'scrollSection', dir: dir }, '*');
}

// document.getElementById('print-button').addEventListener('click', printIframe);
function printIframe() {
  iframe.contentWindow.postMessage({action: 'print'}, '*');
}

function update() {
  iframe.src = urls[index][0];
  var links = document.querySelectorAll("nav a");
  links.forEach(function(link, i) {
    if (i === index) {
      link.classList.add("selected");
    } else {
      link.classList.remove("selected");
    }
  });
}

document.querySelectorAll("nav a").forEach(function(link, i) {
  link.addEventListener("click", function(event) {
    event.preventDefault();
    index = i;
    update();
  });
});

window.addEventListener('keydown', function(event) {
   if (event.ctrlKey && event.keyCode === 80) {
    // Prevent the default print dialog from showing
    event.preventDefault();
    // Call your custom print function
    printIframe();
  }
  switch (event.keyCode) {
    case 104:  // h
    case 37:   // left arrow
      previous();
      break;
    case 108:  // l
    case 39:   // right arrow
      next();
      break;
    case 107:  // k
    case 38:   // up arrow
      console.log("up")
      scrollSection(-1);
      break;
    case 32:   //space
    case 106:  // j
    case 40:   // down arrow
      console.log("down")
      scrollSection(1);
      break;
  }
});

update();
