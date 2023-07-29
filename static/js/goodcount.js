// app.js
new Vue({
  el: '#goodcount',
  data: {
      count: 0, // カウントの初期値
  },
  
  created() {
      // ページが読み込まれた時にLocal Storageからカウントを取得
      const storedCount = localStorage.getItem('count');
      if (storedCount) {
          this.count = parseInt(storedCount);
      }
  },

  methods: {
      handleClick() {
          if (this.count % 2 === 0) {
              this.count += 1; // カウントを増やす
          } else {
              this.count -= 1; // カウントを減らす
          }
          // カウントをLocal Storageに保存
          localStorage.setItem('count', this.count.toString());
      }
  }
});
