var urls = {{ files_with_titles|tojson }};
var index = 0;
var sectionIndex = 0;

function previous() { if (index > 0) { index--; update(); } }
function next() { if (index < urls.length - 1) { index++; update(); } }

var iframe = document.getElementById('iframe');
// iframe.onload = function() {
  // // Reset section index when new content is loaded
  // sectionIndex = 0;
  // var sections = this.contentDocument.getElementsByTagName('section');
// };

function scrollSection(dir) {
  iframe.contentWindow.postMessage({ action: 'scrollSection', dir: dir }, '*');
}

// function scrollSection(dir) {
  // var sections = iframe.contentDocument.getElementsByTagName('section');
  // if (dir > 0) {
    // console.log("up")
    // if (sectionIndex < sections.length - 1) { sectionIndex++; }
  // } else {
    // console.log("down")
    // if (sectionIndex > 0) { sectionIndex--; }
  // }
  // sections[sectionIndex].scrollIntoView({behavior: "smooth", block: "center"});
// }

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
  switch (event.keyCode) {
    case 37: // left arrow
      previous();
      break;
    case 39: // right arrow
      next();
      break;
    case 38: // up arrow
      console.log("up")
      scrollSection(-1);
      // iframe.onload = function() {
        // scrollSection(-1);
      // }
      break;
    case 40: // down arrow
      console.log("down")
      scrollSection(1);
      // iframe.onload = function() {
        // scrollSection(1);
      // }
      break;
  }
});

update();
