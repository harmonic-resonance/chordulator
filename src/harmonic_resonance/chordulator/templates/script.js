var urls = {{ files_with_titles|tojson }};
var index = 0;
var sectionIndex = 0;
var sections = document.getElementById('iframe').contentDocument.getElementsByTagName('section');
function previous() { if (index > 0) { index--; update(); } }
function next() { if (index < urls.length - 1) { index++; update(); } }
function scrollSection(dir) {
  if (dir > 0) {
    if (sectionIndex < sections.length - 1) { sectionIndex++; }
  } else {
    if (sectionIndex > 0) { sectionIndex--; }
  }
  sections[sectionIndex].scrollIntoView({behavior: "smooth", block: "center"});
}
function update() {
  document.getElementById("iframe").src = urls[index][0];
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
      scrollSection(-1);
      break;
    case 40: // down arrow
      scrollSection(1);
      break;
  }
});

