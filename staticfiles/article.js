(function () {
  "use strict";

  // --- Scroll to share bar when the floating share icon is tapped ---
  var shareTop = document.querySelector(".share-top");
  if (shareTop) {
    shareTop.addEventListener("click", function () {
      var bar = document.querySelector(".feed-share");
      if (bar) bar.scrollIntoView({ behavior: "smooth", block: "center" });
    });
  }

  // --- Copy post link ---
  var copyBtn = document.querySelector(".copy-section button");
  var showLink = document.querySelector("#showlink");
  if (copyBtn && showLink) {
    copyBtn.addEventListener("click", function () {
      var done = document.querySelector("#messageDone");
      var finish = function () { if (done) { done.textContent = "Copied!"; setTimeout(function () { done.textContent = ""; }, 1500); } };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(showLink.value).then(finish, function () {
          showLink.select(); try { document.execCommand("copy"); } catch (e) {} finish();
        });
      } else {
        showLink.select(); try { document.execCommand("copy"); } catch (e) {} finish();
      }
    });
  }
})();
