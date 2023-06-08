var urls = {{ files_with_titles|tojson }};
var index = 0;
function previous() { if (index > 0) { index--; update(); } }
function next() { if (index < urls.length - 1) { index++; update(); } }
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

