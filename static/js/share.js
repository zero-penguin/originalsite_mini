const link_btn = document.getElementById('link-btn');
link_btn.addEventListener('click', async () => {
  try {
    await navigator.share({ title: document.title, url: "http://127.0.0.1:5000/" });
  } catch (error) {
    console.error(error);
  }
});