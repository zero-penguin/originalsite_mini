// script.js
// ロードが完了したらローディング画面を非表示にしてコンテンツを表示する
window.addEventListener('load', function() {
  const loadingScreen = document.getElementById('loading-screen');
  const content = document.getElementById('content');

  loadingScreen.style.display = 'none';
  content.style.display = 'block';
});

// ページがロードされた後、0.5秒後にusername要素のopacityを1に設定（徐々に表示）
window.onload = function() {
  setTimeout(function() {
      var usernameElement = document.querySelector('.username');
      usernameElement.style.opacity = '1';
  }, 500);
};