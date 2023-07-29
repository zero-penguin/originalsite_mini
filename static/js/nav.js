// スクロールイベントを監視し、メニューバーの表示を切り替える
window.addEventListener("scroll", function() {

  var navbar = document.querySelector(".navbar");
  if (window.scrollY > 0) {
    navbar.classList.add("scrolled");
  } else {
    navbar.classList.remove("scrolled");
  }
  
});
