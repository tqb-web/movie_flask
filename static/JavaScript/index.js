
const errorMessage = document.getElementById('error-message');
if (errorMessage) {
  errorMessage.style.display = 'block'; // 显示错误消息
  setTimeout(() => {
    errorMessage.classList.add('show');
  }, 100);
  setTimeout(() => {
    errorMessage.classList.remove('show');
    errorMessage.style.display = 'none'; // 隐藏错误消息
  }, 3000);
}
