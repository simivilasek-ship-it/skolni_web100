const links = document.querySelectorAll("nav a");
const currentPage = location.pathname.split("/").pop();

links.forEach(link => {
  if (link.getAttribute("href") === currentPage) {
    link.classList.add("active");
  }
});
