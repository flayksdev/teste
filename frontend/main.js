// Comportamento mínimo: ano no rodapé e destaque da seção atual no menu.
(function () {
  "use strict";

  var ano = document.getElementById("ano");
  if (ano) ano.textContent = String(new Date().getFullYear());

  if (!("IntersectionObserver" in window)) return;

  var links = Array.prototype.slice.call(document.querySelectorAll(".nav a"));
  var byId = {};
  links.forEach(function (a) { byId[a.getAttribute("href").slice(1)] = a; });

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      links.forEach(function (a) { a.removeAttribute("aria-current"); });
      var link = byId[entry.target.id];
      if (link) link.setAttribute("aria-current", "true");
    });
  }, { rootMargin: "-40% 0px -55% 0px" });

  Object.keys(byId).forEach(function (id) {
    var el = document.getElementById(id);
    if (el) observer.observe(el);
  });
})();
