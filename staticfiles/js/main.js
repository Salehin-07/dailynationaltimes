(function () {
  "use strict";

  var body = document.body;

  // ---- Mobile navigation drawer ----
  var navToggle = document.getElementById("navToggle");
  var navOverlay = document.getElementById("navOverlay");
  var navEl = document.getElementById("primaryNav");
  var navClose = document.getElementById("navClose");

  function setNav(open) {
    body.classList.toggle("dnt-navopen", open);
    if (navToggle) {
      navToggle.setAttribute("aria-expanded", open ? "true" : "false");
      navToggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    }
  }
  if (navToggle) navToggle.addEventListener("click", function () {
    setNav(!body.classList.contains("dnt-navopen"));
  });
  if (navClose) navClose.addEventListener("click", function () { setNav(false); });
  if (navOverlay) navOverlay.addEventListener("click", function () { setNav(false); });
  if (navEl) navEl.addEventListener("click", function (e) {
    if (e.target.closest("a")) setNav(false);
  });
  window.addEventListener("resize", function () {
    if (window.innerWidth > 900) setNav(false);
  });

  // ---- Mobile search popup ----
  var searchToggle = document.getElementById("searchToggle");
  var searchPopup = document.getElementById("searchPopup");
  var searchBackdrop = document.getElementById("searchBackdrop");

  function setSearch(open) {
    body.classList.toggle("dnt-searchopen", open);
    if (searchToggle) searchToggle.setAttribute("aria-expanded", open ? "true" : "false");
    if (open && searchPopup) {
      var i = searchPopup.querySelector("input");
      if (i) setTimeout(function () { i.focus(); }, 60);
    }
  }
  if (searchToggle) searchToggle.addEventListener("click", function (e) {
    e.stopPropagation();
    setSearch(!body.classList.contains("dnt-searchopen"));
  });
  if (searchBackdrop) searchBackdrop.addEventListener("click", function () { setSearch(false); });
  if (searchPopup) {
    var sf = searchPopup.querySelector("form");
    if (sf) sf.addEventListener("submit", function () { setSearch(false); });
  }

  // ---- Escape closes any overlay ----
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") { setNav(false); setSearch(false); }
  });

  // ---- Social share pop-up windows ----
  var shares = document.querySelectorAll(".window-t");
  Array.prototype.forEach.call(shares, function (el) {
    el.addEventListener("click", function (e) {
      e.preventDefault();
      var url = el.getAttribute("data-url") || "";
      if (!url) return;
      var w = parseInt(el.getAttribute("data-width"), 10) || 550;
      var h = parseInt(el.getAttribute("data-height"), 10) || 460;
      var left = (screen.width - w) / 2;
      var top = (screen.height - h) / 2;
      window.open(url, "_blank", "width=" + w + ",height=" + h + ",left=" + left + ",top=" + top);
    });
  });
})();
