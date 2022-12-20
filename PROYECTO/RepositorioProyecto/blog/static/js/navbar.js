(function () {
  const navbar = document.querySelector(".navbar-collapse");
  const links = navbar.querySelectorAll(".nav-link");
  links.forEach((i) => {
    if (location.pathname.includes(i.name)) {
      links.forEach((j) => j.classList.remove("active"));
      i.classList.add("active");
    }
  });
})();
