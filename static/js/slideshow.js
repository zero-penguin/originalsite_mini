// static/js/slideshow.js

var slides = document.getElementsByClassName('slide');
var currentSlideIndex = 0;

function showSlide(slideIndex) {
  for (var i = 0; i < slides.length; i++) {
    slides[i].classList.remove('active');
  }
  slides[slideIndex].classList.add('active');
}

function nextSlide() {
  currentSlideIndex++;
  if (currentSlideIndex >= slides.length) {
    currentSlideIndex = 0;
  }
  showSlide(currentSlideIndex);
}

var slideshowInterval = setInterval(nextSlide, 3000);

var slideshowContainer = document.getElementsByClassName('slideshow-container')[0];

