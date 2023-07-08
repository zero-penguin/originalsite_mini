// static/js/slideshow.js

var slides = document.getElementsByClassName('slide');
var currentSlideIndex = 0;

// 初期表示時に3つのスライドを表示する関数
function showSlides() {
  // すべてのスライドから 'active' クラスを削除します
  for (var i = 0; i < slides.length; i++) {
    slides[i].classList.remove('active');
  }
  
  // 3つのスライドに 'active' クラスを追加します
  for (var i = 0; i < 5; i++) {
    var slideIndex = (currentSlideIndex + i) % slides.length;
    slides[slideIndex].classList.add('active');
  }
}

// 初期表示時に3つのスライドを表示します
showSlides();

// 次のスライドを表示する関数
function nextSlide() {
  // 現在のスライドのインデックスを増やします
  currentSlideIndex++;

  // スライドの数を超えた場合は最初のスライドに戻ります
  if (currentSlideIndex >= slides.length) {
    currentSlideIndex = 0;
  }

  // スライドを更新します
  showSlides();
}

// 3秒ごとに次のスライドを表示するためのインターバルを設定します
var slideshowInterval = setInterval(nextSlide, 3000);

// スライドショーのコンテナ要素を取得します
var slideshowContainer = document.getElementsByClassName('slideshow-container')[0];
